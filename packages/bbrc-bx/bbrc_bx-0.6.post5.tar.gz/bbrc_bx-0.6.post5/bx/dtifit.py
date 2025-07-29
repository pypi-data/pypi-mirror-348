from bx.command import Command
from bx import download as dl
from bx.spm12 import SPM12Command

class DTIFITCommand(SPM12Command):
    """DTIFIT - Processing of Diffusion-weighted Imaging data

    Available subcommands:
     maps:\t\tdownload parametric maps (FA, MD, AxD, RD)
     files:\t\tdownload all `*DTIFIT` outputs (including parametric maps)
     report:\t\tdownload the validation report issued by `*DTIFITValidator`
     snapshot:\t\tdownload snapshots of the FA map, RGB tensor and TOPUP distortion correction map
     tests:\t\tcreate an Excel table with all automatic tests outcomes from bbrc-validator


    Usage:
     bx dtifit <subcommand> <resource_id>
    """
    nargs = 2
    resource_name = 'TOPUP_DTIFIT'
    subcommands = ['files', 'report', 'snapshot', 'tests', 'maps']
    validator = 'DTIFITValidator'
    url = 'https://gitlab.com/bbrc/xnat/xnat-pipelines/-/tree/master/dtifit'

    def __init__(self, *args, **kwargs):
        super(DTIFITCommand, self).__init__(*args, **kwargs)
        if self.resource_name == 'DWIFSLPREPROC_DTIFIT':
            self.url = 'https://gitlab.com/bbrc/xnat/docker-images/-/tree/master/dwifslpreproc_dtifit'

    def parse(self):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand in ['files', 'report', 'snapshot', 'maps']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        subcommand=subcommand)

        elif subcommand == 'tests':
            version = ['*', '4e37c9d0']
            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=self.validator,
                             version=version, max_rows=25)
            self.to_excel(df)
