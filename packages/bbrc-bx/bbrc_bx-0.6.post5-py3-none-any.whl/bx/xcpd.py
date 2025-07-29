from bx.command import Command
from bx import download as dl
import logging as log


class XCPDCommand(Command):
    """XCP-D - Resting State fMRI postprocessing and functional connectivity.

    Available subcommands:
     conmat:\t\tdownload the functional connectivity matrix (Desikan-Killiany atlas)
     timeseries:\tdownload the parcellated BOLD time-series (Desikan-Killiany atlas)
     files:\t\tdownload all XCP_D outputs (denoised BOLD data, segmentations, everything...)
     report:\t\tdownload the validation report issued by `XCPDValidator`
     snapshot:\t\tdownload snapshots from the XCPD pipeline
     tests:\t\tcreate an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx xcpd <subcommand> <resource_id>

    References:
    - Ciric R. et al., Nat Protoc 13 (2018).
    - Mehta K., Salo T. et al., bioRxiv (2023). DOI: 10.1101/2023.11.20.567926
    """
    nargs = 2
    resource_name = 'XCP_D'
    subcommands = ['conmat', 'timeseries', 'files', 'report', 'snapshot', 'tests']
    validator = 'XCPDValidator'
    url = 'https://gitlab.com/bbrc/xnat/docker-images/-/tree/master/xcp_d'

    def __init__(self, *args, **kwargs):
        super(XCPDCommand, self).__init__(*args, **kwargs)

    def parse(self):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand == 'conmat':
            self.run_id(id, download_conmat, resource_name=self.resource_name,
                        destdir=self.destdir)
        elif subcommand == 'timeseries':
            self.run_id(id, download_ts, resource_name=self.resource_name,
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


def download_conmat(x, experiments, resource_name, destdir, atlas='DK'):
    import os.path as op
    from tqdm import tqdm

    for e in tqdm(experiments):
        log.debug('Experiment %s:' % e['ID'])

        r = x.select.experiment(e['ID']).resource(resource_name)
        try:
            df = r.conmat(atlas)
        except StopIteration:
            log.error('Failed for %s. Skipping it.' % e['ID'])
            continue

        fn = '{}_{}_{}_xcpd_{}_conmat.xlsx'.format(e['subject_label'],
                                                   e['label'], e['ID'],
                                                   atlas)
        df.to_excel(op.join(destdir, fn))


def download_ts(x, experiments, resource_name, destdir, atlas='DK'):
    import os.path as op
    from tqdm import tqdm

    for e in tqdm(experiments):
        log.debug('Experiment %s:' % e['ID'])

        r = x.select.experiment(e['ID']).resource(resource_name)
        try:
            df = r.timeseries(atlas)
        except StopIteration:
            log.error('Failed for %s. Skipping it.' % e['ID'])
            continue

        fn = '{}_{}_{}_xcpd_{}_timeseries.xlsx'.format(e['subject_label'],
                                                       e['label'], e['ID'],
                                                       atlas)
        df.to_excel(op.join(destdir, fn), index=False)
