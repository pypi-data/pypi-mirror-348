from bx.command import Command
from bx import download as dl
import os
import logging as log


class FdgCommand(Command):
    """18F-fluorodeoxyglucose PET imaging data

    Available subcommands:
     landau:\t\tcreates an Excel table with the Landau's metaROI signature
     maps:\t\tdownload the normalized FDG maps in MNI space
     files:\t\tdownload all outputs from the `FDG_QUANTIFICATION2` pipeline
     mri:\t\tcreates an Excel table with details from associated MRI sessions
     aging:\t\tcreates an Excel table with the aging composite ROI
     regional:\t\tcreates an Excel table with the regional quantification results
     snapshot:\t\tdownload snapshots from `FDG_QUANTIFICATION2` pipeline
     report:\t\tdownload the validation report issued by `FDGQuantificationValidator`
     tests:\t\tcollect all automatic tests outcomes from `FDGQuantificationValidator`

    Usage:
     bx fdg <subcommand> <resource_id>

    Reference:
    - Landau et al., Ann Neurol., 2012
    """
    nargs = 2
    subcommands = ['landau', 'maps', 'files', 'mri', 'aging', 'regional',
                   'snapshot', 'report', 'tests']
    resource_name = 'FDG_QUANTIFICATION2'
    url = 'https://gitlab.com/bbrc/xnat/xnat-pipelines/-/tree/master/pet'

    def __init__(self, *args, **kwargs):
        super(FdgCommand, self).__init__(*args, **kwargs)

    def parse(self):
        validator_name = 'FDGQuantificationValidator'

        subcommand = self.args[0]
        id = self.args[1]
        if subcommand == 'tests':
            version = ['*', '0390c55f']

            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=validator_name,
                             version=version, max_rows=25)
            self.to_excel(df)
        elif subcommand == 'landau':
            df = self.run_id(id, dl.measurements,
                             resource_name=self.resource_name,
                             subfunc=subcommand, max_rows=10)
            self.to_excel(df)
        elif subcommand == 'maps':
            fp = 'static_pet.nii.gz'
            if not os.environ.get('CI_TEST', None):
                fp = get_filepath(self.resource_name)
            self.run_id(id, download_pet, resource_name=self.resource_name,
                        filename=fp, destdir=self.destdir,
                        subcommand=subcommand)
        elif subcommand == 'mri':
            df = self.run_id(id, get_mri_table, validator='PetSessionValidator')
            self.to_excel(df)
        elif subcommand == 'aging':
            df = self.run_id(id, dl.measurements,
                             resource_name=self.resource_name,
                             subfunc=subcommand, max_rows=10)
            self.to_excel(df)
        elif subcommand == 'regional':
            atlas = 'hammers'
            if not os.environ.get('CI_TEST', None):
                atlas = get_atlas()
            df = self.run_id(id, dl.measurements,
                             resource_name=self.resource_name,
                             subfunc=f'pet_{atlas}', max_rows=10)
            self.args[0] += f'_{atlas}'
            self.to_excel(df)
        elif subcommand in ['files', 'report', 'snapshot']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=validator_name, destdir=self.destdir,
                        subcommand=subcommand)


class FtmCommand(Command):
    """18F-flutemetamol PET imaging data

    Available subcommands:
     centiloids:\tcreates an Excel table with centiloid scales
     maps:\t\tdownload the normalized FTM maps in MNI space
     files:\t\tdownload all outputs from the `FTM_QUANTIFICATION2` pipeline
     mri:\t\tcreates an Excel table with details from associated MRI sessions
     regional:\t\tcreates an Excel table with the regional quantification results
     snapshot:\t\tdownload snapshots from `FTM_QUANTIFICATION2` pipeline
     report:\t\tdownload the validation report issued by `FTMQuantificationValidator`
     tests:\t\tcollect all automatic tests outcomes from `FTMQuantificationValidator`

    Usage:
     bx ftm <subcommand> <resource_id>

    References:
     - Klunk et al, Alzheimers Dement., 2015
    """
    nargs = 2
    subcommands = ['centiloids', 'maps', 'files', 'mri', 'regional',
                   'snapshot', 'report', 'tests']
    resource_name = 'FTM_QUANTIFICATION2'
    url = 'https://gitlab.com/bbrc/xnat/xnat-pipelines/-/tree/master/pet'

    def __init__(self, *args, **kwargs):
        super(FtmCommand, self).__init__(*args, **kwargs)

    def parse(self):
        validator_name = 'FTMQuantificationValidator'

        subcommand = self.args[0]
        id = self.args[1]
        if subcommand == 'tests':
            version = ['*', '0390c55f']

            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=validator_name,
                             version=version, max_rows=25)
            self.to_excel(df)
        elif subcommand == 'centiloids':
            df = self.run_id(id, dl.measurements,
                             resource_name=self.resource_name,
                             subfunc=subcommand, max_rows=10)
            self.to_excel(df)
        elif subcommand == 'maps':
            fp = 'static_pet.nii.gz'
            if not os.environ.get('CI_TEST', None):
                fp = get_filepath(self.resource_name)
            self.run_id(id, download_pet, resource_name=self.resource_name,
                        filename=fp, destdir=self.destdir,
                        subcommand=subcommand)
        elif subcommand == 'mri':
            df = self.run_id(id, get_mri_table, validator='PetSessionValidator')
            self.to_excel(df)
        elif subcommand == 'regional':
            atlas = 'hammers'
            if not os.environ.get('CI_TEST', None):
                atlas = get_atlas()
            df = self.run_id(id, dl.measurements,
                             resource_name=self.resource_name,
                             subfunc=f'pet_{atlas}', max_rows=10)
            self.args[0] += f'_{atlas}'
            self.to_excel(df)
        elif subcommand in ['files', 'report', 'snapshot']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=validator_name, destdir=self.destdir,
                        subcommand=subcommand) 


class TauCommand(Command):
    """18F-RO-948 tau PET imaging data

    Available subcommands:
     tests:\t\tcollect all automatic tests outcomes from `TauPetSessionValidator`
     mri:\t\tcreates an Excel table with details from associated MRI sessions

    Usage:
     bx tau <subcommand> <resource_id>
    """
    nargs = 2
    subcommands = ['tests', 'mri']
    # resource_name = 'XXX'
    # url = 'https://gitlab.com/bbrc/xnat/xnat-pipelines/-/tree/master/pet'

    def __init__(self, *args, **kwargs):
        super(TauCommand, self).__init__(*args, **kwargs)

    def parse(self):
        validator_name = 'TauPetSessionValidator'

        subcommand = self.args[0]
        id = self.args[1]
        if subcommand == 'tests':
            version = ['*', '0390c55f']

            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=validator_name,
                             version=version, max_rows=25)
            self.to_excel(df)
        elif subcommand == 'mri':
            df = self.run_id(id, get_mri_table, validator=validator_name)
            self.to_excel(df)


def get_filepath(resource_name, debug=False):
    region = None
    options = ['cgm', 'pons', 'wcbs', 'wc', 'wm', 'raw']
    msg = 'Reference region?\n'\
          ' - cgm: Cerebellar gray matter\n'\
          ' - wcbs: Whole cerebellum + Brain stem\n'\
          ' - pons: Pons\n'\
          ' - wc: Whole cerebellum\n'\
          ' - wm: White matter\n'\
          ' - raw: Raw image (not scaled, not normalized)\n> '
    if resource_name.startswith('FDG'):
        msg = msg.replace('Pons\n', 'Pons\n - vermis: Vermis\n')
        options.append('vermis')
    while region not in options and not debug:
        region = input(msg).lower()
        if region not in options:
            m = 'Incorrect option (%s). Please try again.' % region
            print(m)

    fp = ''
    if region == 'raw':
        fp = 'static_pet.nii.gz'
    else:
        fp = f'GLOBAL/wstatic_pet_scaled_{region}.nii.gz'

    return fp


def download_pet(x, experiments, resource_name, filename, destdir, subcommand):
    import os.path as op
    from tqdm import tqdm
    from pyxnat.core.errors import DataError

    for e in tqdm(experiments):
        log.debug('Experiment %s:' % e['ID'])

        r = x.select.experiment(e['ID']).resource(resource_name)
        f = r.file(filename)
        fn = '%s_%s_%s_%s' % (e['subject_label'], e['label'], e['ID'],
                              filename.replace('GLOBAL/', ''))
        try:
            f.get(op.join(destdir, fn))
        except DataError as exc:
            log.error('Failed for %s. Skipping it. (%s)' % (e, exc))


def get_mri_table(x, experiments, validator='PetSessionValidator'):
    import pandas as pd
    from tqdm import tqdm

    table = []
    for e in tqdm(experiments):
        try:
            e_id = e['ID']
            exp = x.array.experiments(experiment_id=e_id,
                                      columns=['date', 'subject_label']).data[0]
            if 'petSessionData' not in exp['xsiType']:
                continue

            row = [e_id, exp['date'], exp['project'], exp['subject_label']]

            r = x.select.experiment(e_id).resource('BBRC_VALIDATOR')
            if list(r.files('{}*'.format(validator))):
                has_t1 = r.tests(validator)['HasUsableT1']
                if has_t1['has_passed']:
                    if not 'notes' in has_t1['data'][0].keys():
                        has_t1['data'][0]['notes'] = None
                    row.extend(has_t1['data'][0].values())
            table.append(row)
        except KeyboardInterrupt:
            break

    cols = ['ID', 'date', 'project', 'subject_label',
            'MRI_ID', 'MRI_date', 'MRI_project', 'MRI_scanID', 'notes']
    df = pd.DataFrame(table, columns=cols).set_index('subject_label').sort_index()
    return df


def get_atlas(debug=False):
    atlas = None
    options = ['hammers', 'aal', 'dk']
    msg = 'Regional quantification atlas?\n'\
          ' - hammers\n'\
          ' - aal\n'\
          ' - dk\n> '
    while atlas not in options and not debug:
        atlas = input(msg).lower()
        if atlas not in options:
            m = 'Incorrect option (%s). Please try again.' % atlas
            print(m)
    return atlas
