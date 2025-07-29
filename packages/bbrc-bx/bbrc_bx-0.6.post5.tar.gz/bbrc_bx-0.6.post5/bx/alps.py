from bx.command import Command
from bx import download as dl


class ALPSCommand(Command):
    """ALPS - Diffusion Tensor Imaging analysis ALong the Perivascular Space

    Available subcommands:
     stats:\t\tcreate an Excel table with `ALPS` metrics
     diffusion:\t\tcreate an Excel table with `FA` and `MD` diffusion metrics in ALPS ROIs
     files:\t\tdownload all `ALPS` outputs (parametric maps, DTI tensors, transformations, everything...)
     snapshot:\t\tdownload snapshots from the `ALPS` pipeline
     report:\t\tdownload the validation report issued by bbrc-validator
     tests:\t\tcreate an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx alps <subcommand> <resource_id>

    References:
      - X. Liu, G. Barisano, et al., Aging and Disease, 2023. DOI: 10.14336/AD.2023.0321-2
      - T. Taoka et al., Magnetic Resonance in Medical Sciences, 2024. DOI: 10.2463/mrms.rev.2023-0175
      - T. Taoka et al. Japanese Journal of Radiology, 2017. DOI: 10.1007/s11604-017-0617-z
    """
    nargs = 2
    resource_name = 'ALPS'
    subcommands = ['stats', 'diffusion', 'files', 'snapshot', 'report', 'tests']
    validator = 'ALPSValidator'
    url = 'https://gitlab.com/bbrc/xnat/docker-images/-/tree/master/alps'

    def __init__(self, *args, **kwargs):
        super(ALPSCommand, self).__init__(*args, **kwargs)

    def parse(self):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand in ['stats', 'diffusion']:
            sf = f'alps_{subcommand}'
            df = self.run_id(id, dl.measurements,
                             resource_name=self.resource_name,
                             subfunc=sf, max_rows=10)
            self.to_excel(df)
        elif subcommand in ['files', 'snapshot', 'report']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        subcommand=subcommand)

        elif subcommand == 'tests':
            version = ['*']
            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=self.validator,
                             version=version, max_rows=25)
            self.to_excel(df)
