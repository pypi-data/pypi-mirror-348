from bx.command import Command
from bx import download as dl
import os
import logging as log


class ASL3DCommand(Command):
    """Cerebral perfusion quantification of reconstructed 3D Arterial Spin Labeling MRI.

    Available subcommands:
     perfusion:\t\tcreates an Excel table with global perfusion values.
     aal:\t\tcreates an Excel table with regional perfusion values (in AAL atlas).
     maps:\t\tdownload the calibrated perfusion maps
     files:\t\tdownload all 3D-ASL QUANTIFICATION outputs (perfusion maps, files, everything...)
     snapshot:\t\tdownload a snapshot from the 3D-ASL QUANTIFICATION pipeline
     report:\t\tdownload the validation report issued by bbrc-validator
     tests:\t\tcreate an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx asl3d <subcommand> <resource_id>

    References:
    - Chappell MA. et al., Imaging Neuroscience, 2023. DOI: 10.1162/imag_a_00041
    """
    nargs = 2
    resource_name = '3DASL_QUANTIFICATION'
    subcommands = ['perfusion', 'aal', 'maps', 'files', 'report', 'snapshot', 'tests']
    validator = 'ASL3DQuantificationValidator'
    url = 'https://gitlab.com/bbrc/xnat/xnat-pipelines/-/tree/master/asl#3d-asl-quantification'

    def __init__(self, *args, **kwargs):
        super(ASL3DCommand, self).__init__(*args, **kwargs)

    def parse(self):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand in ['perfusion', 'aal']:
            sf = 'asl3d_%s' % subcommand
            df = self.run_id(id, dl.measurements, subfunc=sf,
                             resource_name=self.resource_name, max_rows=10)
            self.to_excel(df)

        elif subcommand == 'maps':
            debug = os.environ.get('CI_TEST', None)
            if debug:
                space = 'native_space'
            else:
                space = get_space()
            self.run_id(id, download_perfusion, resource_name=self.resource_name,
                        destdir=self.destdir, space=space, subcommand=subcommand)

        elif subcommand in ['files', 'report', 'snapshot']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        subcommand=subcommand)

        elif subcommand == 'tests':

            version = ['##7f43c4c4', '*']
            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=self.validator,
                             version=version, max_rows=25)
            self.to_excel(df)


def get_space():
    space = ''
    options = ['native_space', 'std_space', 'struct_space']
    msg = 'Which space?\n' \
          ' - native_space: native ASL space\n' \
          ' - std_space: MNI152 standard space \n' \
          ' - struct_space: structural T1 space\n'
    while space not in options:
        space = input(msg)
        if space not in options:
            m = 'Incorrect option (%s). Please try again.' % space
            print(m)
        else:
            space = space
    return space


def download_perfusion(x, experiments, resource_name, destdir, space, subcommand):
    import os.path as op
    from tqdm import tqdm
    from pyxnat.core.errors import DataError

    fp_options = {'native_space': 'masked_asl.nii.gz',
                  'std_space': 'asl2std.nii.gz',
                  'struct_space': 'asl2struct.nii.gz'}
    filename = fp_options[space]
    for e in tqdm(experiments):
        log.debug('Experiment %s:' % e['ID'])

        r = x.select.experiment(e['ID']).resource(resource_name)
        f = r.file(filename)

        fn = '%s_%s_%s_%s_%s.nii.gz' % (e['subject_label'], e['label'], e['ID'], 'perfusion', space)
        try:
            f.get(op.join(destdir, fn))
        except DataError as exc:
            log.error('Failed for %s. Skipping it. (%s)' % (e['ID'], exc))
