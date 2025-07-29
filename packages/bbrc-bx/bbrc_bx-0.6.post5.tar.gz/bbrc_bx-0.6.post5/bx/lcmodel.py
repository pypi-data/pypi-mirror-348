import logging as log
from bx.command import Command
from bx import download as dl


class LCModelCommand(Command):
    """LCModel - Quantification and tissue-correction of MR Spectroscopy images.

    Available subcommands:
     stats:\t\tcreates an Excel table with metabolite concentrations and global signal quality stats
     correction:\tcreates an Excel table with tissue correction parameters
     files:\t\tdownload all LCModel outputs (stats, tissue correction, masks, everything...)
     snapshot:\t\tdownload snapshots from the LCMODEL pipeline
     report:\t\tdownload the validation report issued by `LCModelValidator`
     tests:\t\tcreate an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx lcmodel <subcommand> <resource_id>

    References:
    - Provencher SW., Magnetic Resonance in Medicine, 1993.
    """
    nargs = 2
    resource_name = 'LCMODEL'
    subcommands = ['stats', 'correction', 'files', 'report', 'snapshot', 'tests']
    validator = 'LCModelValidator'
    url = 'https://gitlab.com/bbrc/xnat/xnat-pipelines/-/tree/master/lcmodel'

    def __init__(self, *args, **kwargs):
        super(LCModelCommand, self).__init__(*args, **kwargs)

    def parse(self):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand == 'stats':
            df = self.run_id(id, download_stats)
            self.to_excel(df, index=False)

        if subcommand == 'correction':
            df = self.run_id(id, download_correction)
            self.to_excel(df, index=False)

        elif subcommand in ['files', 'report', 'snapshot']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        subcommand=subcommand)

        elif subcommand == 'tests':
            version = ['fd3dfdbd', '*']
            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=self.validator,
                             version=version, max_rows=25)
            self.to_excel(df)


def download_stats(x, experiments):
    """Download LCModel metabolite concentrations and other miscellaneous
    stats for a list of experiments and merge them in a single table"""
    import pandas as pd
    from tqdm import tqdm
    import io

    reshaped_df = pd.DataFrame()
    for e in tqdm(experiments):
        log.debug('Experiment %s:' % e['ID'])

        r = x.select.experiment(e['ID']).resource('LCMODEL')
        try:
            f = r.files('*lcmodel.xlsx')[0]
        except StopIteration:
            log.error('Failed for %s. Skipping it.' % e['ID'])
            continue

        with io.BytesIO(x.get(f._uri).content) as file_content:
            lcmodel_df = pd.read_excel(file_content)
        for reg in set(lcmodel_df.region):
            subj_region_df = lcmodel_df[lcmodel_df.region == reg]
            row_dict = {}
            for item in subj_region_df.to_dict('records'):
                for k in ['id', 'subject', 'region']:
                    row_dict[k] = item[k]
                if item['table'] in ['concentration', 'miscellaneous']:
                    row_dict[f"{item['measurement']}"] = item['value']
                    # row_dict[f"{item['measurement']}_units"] = item['units']
                elif item['table'] == 'concentration_SD':
                    row_dict[f"{item['measurement']}_SD"] = item['value']
                    # row_dict[f"{item['measurement']}_SD_units"] = item['units']
            row_df = pd.DataFrame(row_dict, index=[0])
            reshaped_df = pd.concat([reshaped_df, row_df])
    reshaped_df.reset_index(drop=True, inplace=True)
    return reshaped_df


def download_correction(x, experiments):
    """Download LCModel tissue correction values for a list of experiments
    and merge them in a single table"""
    import pandas as pd
    from tqdm import tqdm
    import io

    tissue_correction_df = pd.DataFrame()
    for e in tqdm(experiments):
        log.debug('Experiment %s:' % e['ID'])

        r = x.select.experiment(e['ID']).resource('LCMODEL')
        try:
            f = r.files('*mrs_tissue_corr.xlsx')[0]
        except StopIteration:
            log.error('Failed for %s. Skipping it.' % e['ID'])
            continue

        with io.BytesIO(x.get(f._uri).content) as file_content:
            df = pd.read_excel(file_content)
        tissue_correction_df = pd.concat([tissue_correction_df, df])
    tissue_correction_df.reset_index(drop=True, inplace=True)
    return tissue_correction_df
