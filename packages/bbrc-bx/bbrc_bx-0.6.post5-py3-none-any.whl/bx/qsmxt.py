from bx.command import Command
from bx import download as dl
import os
import logging as log


class QSMxTCommand(Command):
    """QSMxT - QSM processing and analysis pipeline. Quantitative susceptibility
    mapping (QSM) is an MRI technique for quantifying magnetic susceptibility
    within biological tissue.

    Available subcommands:
     stats:\t\tcreates an Excel table with regional QSM values (in FreeSurfer aseg atlas).
     maps:\t\tdownload the reconstructed QSM maps
     files:\t\tdownload all QSMxT outputs (QSM maps, segmentations, everything...)
     report:\t\tdownload the validation report issued by `QSMxTValidator`
     tests:\t\tcreate an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx qsmxt <subcommand> <resource_id>

    References:
    - Stewart AW et al., Magnetic Resonance in Medicine, 2022.
    """
    nargs = 2
    resource_name = 'QSMXT'
    subcommands = ['stats', 'maps', 'files', 'report', 'tests']
    validator = 'QSMxTValidator'
    url = 'https://gitlab.com/bbrc/xnat/docker-images/-/tree/master/qsmxt'

    def __init__(self, *args, **kwargs):
        super(QSMxTCommand, self).__init__(*args, **kwargs)

    def parse(self):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand == 'stats':
            sf = 'qsmxt_%s' % subcommand
            df = self.run_id(id, dl.measurements, subfunc=sf,
                             resource_name='QSMXT', max_rows=10)
            self.to_excel(df)

        elif subcommand == 'maps':
            self.run_id(id, download_qsm, resource_name=self.resource_name,
                        destdir=self.destdir)

        elif subcommand in ['files', 'report']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        subcommand=subcommand)

        elif subcommand == 'tests':

            version = ['8ea92b93', '*']
            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=self.validator,
                             version=version, max_rows=25)
            self.to_excel(df)


def download_qsm(x, experiments, resource_name, destdir):

    import os.path as op
    from tqdm import tqdm
    from pyxnat.core.errors import DataError

    filename = 'qsm/*_part-phase_MEGRE_scaled_qsm-filled_000_average.nii.gz'

    for e in tqdm(experiments):
        log.debug('Experiment %s:' % e['ID'])

        r = x.select.experiment(e['ID']).resource(resource_name)
        files = r.files(filename)

        for f in files:
            fn = op.basename(f.label())
            try:
                f.get(op.join(destdir, fn))
            except DataError as exc:
                log.error('Failed for %s. Skipping it. (%s)' % (e['ID'], exc))
