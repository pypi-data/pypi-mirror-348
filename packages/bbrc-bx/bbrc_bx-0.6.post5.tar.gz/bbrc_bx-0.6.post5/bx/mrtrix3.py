from bx.command import Command
from bx import download as dl
import logging as log


class MRtrix3Command(Command):
    """MRtrix3 - Diffusion MRI tractography and structural connectivity.

    Available subcommands:
     connectome:\tdownload the structural connectivity matrix (Desikan-Killiany atlas)
     files:\t\tdownload all MRTRIX3 outputs (streamlines, segmentations, everything...)
     report:\t\tdownload the validation report issued by `MRtrix3Validator`
     snapshot:\t\tdownload snapshots from the MRTRIX3 pipeline
     tests:\t\tcreate an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx mrtrix3 <subcommand> <resource_id>

    References:
    - Tournier JD et al., NeuroImage 202 (2019).
    """
    nargs = 2
    resource_name = 'MRTRIX3'
    subcommands = ['connectome', 'files', 'report', 'snapshot', 'tests']
    validator = 'MRtrix3Validator'
    url = 'https://gitlab.com/bbrc/xnat/docker-images/-/tree/master/mrtrix3'

    def __init__(self, *args, **kwargs):
        super(MRtrix3Command, self).__init__(*args, **kwargs)

    def parse(self):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand == 'connectome':
            self.run_id(id, download_connectome, resource_name=self.resource_name,
                        destdir=self.destdir)

        elif subcommand in ['files', 'report', 'snapshot']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        subcommand=subcommand)

        elif subcommand == 'tests':
            version = ['f0eefa95', '*']
            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=self.validator,
                             version=version, max_rows=25)
            self.to_excel(df)


def download_connectome(x, experiments, resource_name, destdir):
    import os.path as op
    from tqdm import tqdm

    for e in tqdm(experiments):
        log.debug('Experiment %s:' % e['ID'])

        r = x.select.experiment(e['ID']).resource(resource_name)
        try:
            df = r.conmat()
        except ValueError:
            log.error('Failed for %s. Skipping it.' % e['ID'])
            continue

        fn = '{}_{}_{}_mrtrix3_connectome.xlsx'.format(e['subject_label'],
                                                       e['label'], e['ID'])
        df.to_excel(op.join(destdir, fn))
