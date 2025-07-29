import logging as log
from bx.spm12 import SPM12Command
from bx import download as dl


class DARTELCommand(SPM12Command):
    """DARTEL - Smoothed, spatially normalized and Jacobian scaled gray matter images in MNI space

    Available subcommands:
     maps:\t\tdownload the MNI-normalized gray matter maps
     template:\t\tdownload cohort-specific DARTEL template
     report:\t\tdownload the validation report issued by `DartelNorm2MNIValidator`
     tests:\t\tcreate an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx dartel <subcommand> <resource_id>

    References:
     Ashburner J., Neuroimage, 2007. DOI: 10.1016/j.neuroimage.2007.07.007
    """
    nargs = 2
    resource_name = 'DARTEL_NORM2MNI'
    subcommands = ['maps', 'template', 'report', 'tests']
    validator = 'DartelNorm2MNIValidator'
    url = 'https://gitlab.com/bbrc/xnat/xnat-pipelines/-/tree/master/spm#dartel-norm2mni'

    def __init__(self, *args, **kwargs):
        super(DARTELCommand, self).__init__(*args, **kwargs)

    def parse(self):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand in ['template']:
            download_template(self.xnat, template_label=id,
                              resource_name=self.resource_name,
                              destdir=self.destdir)

        elif subcommand in ['maps']:
            self.run_id(id, download_gm, resource_name=self.resource_name,
                        destdir=self.destdir)

        elif subcommand in ['report']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        subcommand=subcommand)

        elif subcommand == 'tests':
            version = ['*', '1229d1b7']
            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=self.validator,
                             version=version, max_rows=25)
            self.to_excel(df)


def download_gm(x, experiments, resource_name, destdir):
    import os.path as op
    from tqdm import tqdm

    filename = 'smw*'

    for e in tqdm(experiments):
        log.debug('Experiment {}:'.format(e['ID']))
        try:
            r = x.select.experiment(e['ID']).resource(resource_name)
            f = list(r.files(filename))[0]

            fn = 'smwc1_{}_{}_{}.nii.gz'.format(e['subject_label'],
                                                e['label'],
                                                resource_name)
            f.get(op.join(destdir, fn))
        except IndexError:
            log.error('Failed for {}. Skipping it.'.format(e['ID']))


def download_template(x, template_label, resource_name, destdir):
    import os.path as op

    filename = 'Template_6.nii'
    spm_res = 'SPM12_SEGMENT'
    if resource_name == 'DARTEL_NORM2MNI_T1T2':
        spm_res = 'SPM12_SEGMENT_T1T2'

    template_lib = x.select.project('DARTEL_TEMPLATES').subject(template_label)
    if not template_lib.exists():
        msg = '`{}` is not a template label'.format(template_label)
        raise ValueError(msg)
    log.info('List detected: {}'.format(template_label))

    f = template_lib.experiment(spm_res).resource('DARTEL').file(filename)
    fn = '{}_{}.nii'.format(op.splitext(filename)[0], spm_res)

    log.info('Saving template in {}'.format(op.join(destdir, fn)))
    f.get(op.join(destdir, fn))
