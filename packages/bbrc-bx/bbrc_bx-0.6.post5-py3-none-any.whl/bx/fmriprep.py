from bx.command import Command
from bx import download as dl


class FMRIPrepCommand(Command):
    """fMRIPrep - Preprocessing of fMRI data.

    Available subcommands:
    files:\t\tdownload all `FMRIPREP` outputs (preprocessed BOLD, confounds, segmentations, everything...)
    report:\t\tdownload the validation report issued by `FMRIPrepValidator`
    tests:\t\tcreate an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx fmriprep <subcommand> <resource_id>

    References:
    - Esteban O, et al., Nat Methods 16, 111–116 (2019).
    """
    nargs = 2
    resource_name = 'FMRIPREP'
    subcommands = ['files', 'report', 'tests']
    validator = 'FMRIPrepValidator'
    url = 'https://gitlab.com/bbrc/xnat/docker-images/-/tree/master/fmriprep'

    def __init__(self, *args, **kwargs):
        super(FMRIPrepCommand, self).__init__(*args, **kwargs)

    def parse(self):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand in ['files', 'report']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        subcommand=subcommand)

        elif subcommand == 'tests':
            version = ['0f31a8ea', '*']
            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=self.validator,
                             version=version, max_rows=25)
            self.to_excel(df)
