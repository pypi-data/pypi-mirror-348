import unittest
import os.path as op
import logging as log
import tempfile
import shutil
from pyxnat import Interface
from bx.parse import parse_args


def assert_excel(dd, values):
    import pandas as pd
    from glob import glob
    df = pd.read_excel(glob(op.join(dd, '*.xlsx'))[0], engine="openpyxl")
    df = df.values.tolist().pop()
    print(df)
    assert (df == values)


class RunThemAll(unittest.TestCase):

    def setUp(self):
        import bx
        from bx.parse import create_parser
        self.config_file = op.join(op.dirname(bx.__file__), '..', '.xnat.cfg')
        print(self.config_file)
        self.xnat_instance = Interface(config=self.config_file)
        create_parser()

    def test_check_xnat_item(self):
        from bx import xnat
        assert xnat.check_xnat_item(self.xnat_instance, 'testenv') == 0
        assert xnat.check_xnat_item(self.xnat_instance, 'BBRCDEV_E01613') == 1
        assert xnat.check_xnat_item(self.xnat_instance, 'DEV') == 2
        assert xnat.check_xnat_item(self.xnat_instance, 'foo') == -1

    def test_update_readme(self):
        import update_readme
        update_readme.update()

    def test_001_commands_without_args(self):
        """Command without args"""
        parse_args('scandates', [], self.xnat_instance)
        parse_args('freesurfer6hires', [], self.xnat_instance)
        parse_args('spm12', [], self.xnat_instance)
        parse_args('spm12', ['wrongsub'], self.xnat_instance)
        parse_args('spm12', ['wrongsub', 'testenv'], self.xnat_instance)
        parse_args('spm12', ['wrongsub', 'toto', 'testenv'], self.xnat_instance)

    def test_002_dates(self):
        """Extract imaging scan dates"""
        parse_args('scandates', ['testenv'], self.xnat_instance)
        parse_args('scandates', ['BBRCDEV_E01613'], self.xnat_instance)
        parse_args('scandates', ['toto'], self.xnat_instance)

    def test_003_freesurfer6_files(self):
        """FreeSurfer6 files"""
        dd = tempfile.mkdtemp()
        parse_args('freesurfer6', ['files', 'testenv'], self.xnat_instance,
                   destdir=dd)
        parse_args('freesurfer6', ['files', 'BBRCDEV_E01613'],
                   self.xnat_instance, destdir=dd)
        parse_args('freesurfer6', ['snapshot', 'BBRCDEV_E01613'],
                   self.xnat_instance, destdir=dd)
        parse_args('freesurfer6', ['report', 'BBRCDEV_E01613'],
                   self.xnat_instance, destdir=dd)

        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_004_freesurfer6_measurements(self):
        """FreeSurfer6 measurements"""
        dd = tempfile.mkdtemp()
        parse_args('freesurfer6', ['aparc', 'testenv'], self.xnat_instance, destdir=dd)
        print(dd)
        import pandas as pd
        from glob import glob
        df = pd.read_excel(glob(op.join(dd, '*.xlsx'))[0], engine="openpyxl")
        print(df)
        assert (len(df) > 1)
        eid = 'BBRCDEV_E00375'
        parse_args('freesurfer6', ['aseg', 'testenv'], self.xnat_instance, destdir=dd)
        for e in ['aparc', 'aseg', 'hippoSfVolumes']:
            parse_args('freesurfer6', [e, eid], self.xnat_instance, destdir=dd)
        parse_args('freesurfer6', ['tests', 'testenv'],
                   self.xnat_instance, destdir=dd)
        parse_args('freesurfer6', ['hippoSfVolumes', 'testenv'],
                   self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_005_spm12_project(self):
        """SPM12 project"""

        dd = tempfile.mkdtemp()
        parse_args('spm12', ['files', 'testenv'], self.xnat_instance, destdir=dd)
        parse_args('spm12', ['volumes', 'testenv'], self.xnat_instance,
                   destdir=dd)
        parse_args('spm12', ['tests', 'testenv'], self.xnat_instance, destdir=dd)
        parse_args('spm12', ['rc', 'testenv'], self.xnat_instance, destdir=dd)
        parse_args('spm12', ['rc', 'DEV'], self.xnat_instance, destdir=dd)

        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_006_spm12_experiment(self):
        dd = tempfile.mkdtemp()
        eid = 'BBRCDEV_E01613'
        for e in ['files', 'volumes', 'snapshot', 'rc']:
            parse_args('spm12', [e, eid], self.xnat_instance, destdir=dd)

        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_007_ashs_experiment(self):
        """ASHS experiment"""
        dd = tempfile.mkdtemp()
        eid = 'BBRCDEV_E02443'
        for e in ['files', 'volumes', 'tests', 'snapshot', 'report']:
            parse_args('ashs', [e, eid], self.xnat_instance, destdir=dd)

        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_008_dtifit(self):
        """DTIFIT"""
        dd = tempfile.mkdtemp()
        eid = 'BBRCDEV_E02801'
        for e in ['files', 'report', 'tests', 'snapshot', 'maps']:
            parse_args('dtifit', [e, eid], self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_009_id(self):
        """ID table"""
        dd = tempfile.mkdtemp()
        parse_args('id', ['BBRCDEV_E01613'], self.xnat_instance, destdir=dd)
        parse_args('id', ['testenv'], self.xnat_instance, destdir=dd)

        import pandas as pd
        from glob import glob
        df = pd.read_excel(glob(op.join(dd, '*.xlsx'))[0], engine="openpyxl")
        print(df)
        assert (len(df) > 1)
        shutil.rmtree(dd)

    def test_010_cat12_experiment(self):
        """CAT12 experiment"""
        dd = tempfile.mkdtemp()
        eid = 'BBRCDEV_E00375'
        parse_args('cat12', ['files', eid], self.xnat_instance, destdir=dd)
        parse_args('cat12', ['volumes', eid], self.xnat_instance, destdir=dd)

        values = [eid, 462026.0547849596, 350126.5098604396, 297766.4493393062,
                  'BASELINE_STUDIES']
        assert_excel(dd, values)

        parse_args('cat12', ['snapshot', eid], self.xnat_instance,
                   destdir=dd)
        parse_args('cat12', ['report', eid], self.xnat_instance,
                   destdir=dd)

        parse_args('cat12', ['rc', eid], self.xnat_instance,
                   destdir=dd)
        parse_args('cat12', ['rc', 'testenv'], self.xnat_instance,
                   destdir=dd)
        parse_args('cat12', ['rc', 'DEV'], self.xnat_instance,
                   destdir=dd)
        # parse_args('cat12', ['tests', 'testenv'], self.xnat_instance,
        # destdir=dd)

        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_011_nifti(self):
        """NIFTI"""
        dd1 = tempfile.mkdtemp()
        dd2 = tempfile.mkdtemp()
        eid = 'BBRCDEV_E02920'
        parse_args('nifti', [eid], self.xnat_instance, destdir=dd1)
        parse_args('nifti', ['all', eid], self.xnat_instance, destdir=dd2)
        from glob import glob
        uf = glob(op.join(dd1, '*.nii.gz'))
        af = glob(op.join(dd2, '*.nii.gz'))
        assert (len(uf) < len(af))
        assert (op.join(dd2, op.basename(uf[0])) in af)

        log.debug('Removing %s', dd1)
        shutil.rmtree(dd1)
        log.debug('Removing %s', dd2)
        shutil.rmtree(dd2)

    def test_cache(self):
        dd = tempfile.mkdtemp()
        from bx.cache import cache_freesurfer6, cache_ashs
        cache_freesurfer6(self.xnat_instance, 'testenv', od=dd, max_rows=10)
        cache_freesurfer6(self.xnat_instance, 'testenv', od=dd)
        cache_ashs(self.xnat_instance, 'testenv', od=dd)
        cache_ashs(self.xnat_instance, 'testenv', od=dd)
        shutil.rmtree(dd)

    def test_012_ants(self):
        """ANTS"""
        dd = tempfile.mkdtemp()
        for e in ['files', 'report', 'tests']:
            parse_args('ants', [e, 'BBRCDEV_E01613'], self.xnat_instance,
                       destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_013_archiving(self):
        """Archiving"""
        dd = tempfile.mkdtemp()
        parse_args('archiving', ['tests', 'BBRCDEV_E01613'], self.xnat_instance,
                   destdir=dd)
        parse_args('archiving', ['tests', 'testenv'], self.xnat_instance,
                   destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_014_lists(self):
        """lists"""
        parse_args('lists', ['display'], self.xnat_instance)

    def test_015a_fdg(self):
        """FDG"""
        dd = tempfile.mkdtemp()
        eid = 'BBRCDEV_E00745'
        for e in ['tests', 'landau', 'maps', 'files', 'mri', 'aging',
                  'regional', 'report', 'snapshot']:
            parse_args('fdg', [e, eid], self.xnat_instance, destdir=dd)
        parse_args('fdg', ['tests', 'testenv'],
                   self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_015b_ftm(self):
        """FTM"""
        dd = tempfile.mkdtemp()
        eid = 'BBRCDEV_E02124'
        for e in ['tests', 'centiloids', 'maps', 'files', 'mri',
                  'regional', 'report', 'snapshot']:
            parse_args('ftm', [e, eid], self.xnat_instance, destdir=dd)
        parse_args('ftm', ['tests', 'testenv'],
                   self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_016_signature(self):
        """signature"""
        dd = tempfile.mkdtemp()
        parse_args('signature', ['jack', 'BBRCDEV_E00375'],
                   self.xnat_instance, destdir=dd)
        parse_args('signature', ['dickerson', 'BBRCDEV_E02823'],
                   self.xnat_instance, destdir=dd)
        # parse_args('signature', [e, 'testenv'], self.xnat_instance,
        #           destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_018_jack_signature(self):
        """Jack's signature"""
        from bx import signature
        import bx

        fp = op.join(op.dirname(bx.__file__), '..', '.xnat.cfg')
        x = Interface(config=fp)

        eid = 'BBRCDEV_E00375'
        regions = ['entorhinal', 'inferiortemporal', 'middletemporal', 'fusiform']
        v = signature.__jack_signature__(x, eid, regions, weighted=True,
                                         measurement='ThickAvg', resource_name='FREESURFER6_HIRES')

        assert (v == 2.3719145266138897)

    def test_019_dickerson_signature(self):
        """Dickerson's signature"""
        from bx import signature
        import bx
        from math import isclose

        fp = op.join(op.dirname(bx.__file__), '..', '.xnat.cfg')
        x = Interface(config=fp)

        eid = 'BBRCDEV_E00375'
        d = {'ad': 2.0948601155910653,
             'aging': 2.1147848695063605}
        for sig, val in d.items():
            rois_path = op.join(op.dirname(bx.__file__), 'data',
                                'dickerson', sig)
            v = signature.__signature__(x, eid, rois_path, weighted=True,
                                        resource_name='FREESURFER6_HIRES')
            assert isclose(v, val, rel_tol=1e-05)

    def test_020_bamos(self):
        """BAMOS"""
        dd = tempfile.mkdtemp()
        for e in ['volumes', 'stats', 'files', 'layers']:
            parse_args('bamos', [e, 'BBRCDEV_E02832'],
                       self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_021_braak(self):
        """Braak regions"""
        dd = tempfile.mkdtemp()
        for e in ['volumes', 'thickness']:
            parse_args('braak', [e, 'BBRCDEV_E00375'], self.xnat_instance,
                       destdir=dd)
        parse_args('braak', ['fdg', 'BBRCDEV_E00745'], self.xnat_instance,
                   destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_022_donsurf(self):
        """DONSURF"""
        dd = tempfile.mkdtemp()
        parse_args('donsurf', ['aparc', 'BBRCDEV_E03095'], self.xnat_instance,
                   destdir=dd)
        from glob import glob
        import pandas as pd
        fp = glob(op.join(dd, '*.xlsx'))[0]
        print(fp)
        df = pd.read_excel(fp, engine='openpyxl')
        q = 'measurement == "DiffuAvg" and region == "bankssts" & side == "left"'
        v = df.query(q).value.iloc[0]
        assert (v == 8.013)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_023_freesurfer7(self):
        """FREESURFER7"""
        dd = tempfile.mkdtemp()
        subcommands = ['aparc', 'aseg', 'report', 'snapshot',
                       'hippoSfVolumes', 'tests', 'amygNucVolumes',
                       'brainstem',
                       'thalamus',
                       'hypothalamus']
        for e in subcommands:
            parse_args('freesurfer7', [e, 'BBRCDEV_E00270'], self.xnat_instance,
                       destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_024_spm12_t1t2(self):
        """MULTICHANNEL SPM12"""
        dd = tempfile.mkdtemp()
        subcommands = ['volumes', 'files', 'snapshot', 'report']
        for e in subcommands:
            v = ('SPM12_SEGMENT_T1T2', 'SPM12SegmentT1T2Validator')
            parse_args('spm12', [e, 'BBRCDEV_E02949', v], self.xnat_instance,
                       destdir=dd)
            v = ('SPM12_SEGMENT', 'SPM12SegmentValidator')
            parse_args('spm12', [e, 'BBRCDEV_E02949', v], self.xnat_instance,
                       destdir=dd)
        log.debug('Removing %s', dd)
        fp = op.join(dd, 'BBRCDEV_E02949', 'SPM12_SEGMENT_T1T2.zip')
        assert (op.isfile(fp))
        fp = op.join(dd, 'BBRCDEV_E02949', 'SPM12_SEGMENT.zip')
        assert (op.isfile(fp))
        shutil.rmtree(dd)

    def test_025_dump(self):
        from bx import dump
        dump.dump('/tmp', config=self.config_file, interpreter='python', debug=True)

    def test_026_basil(self):
        """BASIL-ASL"""
        dd = tempfile.mkdtemp()
        for e in ['perfusion', 'aal', 'stats', 'maps', 'files', 'report',
                  'snapshot', 'tests']:
            parse_args('basil', [e, 'BBRCDEV_E00276'], self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_027_freesurfer7extras(self):
        """FREESURFER7_EXTRAS"""
        dd = tempfile.mkdtemp()
        subcommands = ['report', 'snapshot', 'tests', 'files']
        for e in subcommands:
            parse_args('freesurfer7extras', [e, 'BBRCDEV_E02823'],
                       self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_028_tau(self):
        """TAU PET"""
        dd = tempfile.mkdtemp()
        eid = 'BBRCDEV_E02957'
        for e in ['tests', 'mri']:
            parse_args('tau', [e, eid], self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_029_dartel(self):
        """DARTEL"""
        dd = tempfile.mkdtemp()
        v1 = ('DARTEL_NORM2MNI', 'DartelNorm2MNIValidator')
        v2 = ('DARTEL_NORM2MNI_T1T2', 'DartelNorm2MNIT1T2Validator')
        for v in [v1, v2]:
            parse_args('dartel', ['template', 'DARTEL_ALFA_20220301', v],
                       self.xnat_instance, destdir=dd)
        subcommands = ['maps', 'report', 'tests']
        for e in subcommands:
            parse_args('dartel', [e, 'BBRCDEV_E02823', v1],
                       self.xnat_instance, destdir=dd)
            parse_args('dartel', [e, 'BBRCDEV_E02989', v2],
                       self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)

        items = ['Template_6_SPM12_SEGMENT.nii',
                 'Template_6_SPM12_SEGMENT_T1T2.nii',
                 'smwc1_10630_030410020719630_DARTEL_NORM2MNI.nii.gz',
                 'smwc1_12503_040512300518503_DARTEL_NORM2MNI_T1T2.nii.gz']
        for item in items:
            fp = op.join(dd, item)
            assert (op.isfile(fp))
        shutil.rmtree(dd)

    def test_030_qsmxt(self):
        """QSMxT"""
        dd = tempfile.mkdtemp()
        for e in ['stats', 'maps', 'files', 'report', 'tests']:
            parse_args('qsmxt', [e, 'BBRCDEV_E00276'], self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_031_mrtrix3(self):
        """MRtrix3"""
        dd = tempfile.mkdtemp()
        for e in ['connectome', 'report', 'snapshot', 'tests']:
            parse_args('mrtrix3', [e, 'BBRCDEV_E02885'], self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_032_xcpd(self):
        """XCP-D"""
        dd = tempfile.mkdtemp()
        for e in ['conmat', 'timeseries', 'report', 'snapshot', 'tests']:
            parse_args('xcpd', [e, 'BBRCDEV_E03088'], self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_033_fmriprep(self):
        """fMRIPrep"""
        dd = tempfile.mkdtemp()
        eid = 'BBRCDEV_E03098'
        for e in ['files', 'tests', 'report']:
            parse_args('fmriprep', [e, eid], self.xnat_instance, destdir=dd)

        log.debug('Removing %s', dd)
        shutil.rmtree(dd)
    
    def test_034_lcmodel(self):
        """LCModel"""
        dd = tempfile.mkdtemp()
        eid = 'BBRCDEV_E03082'
        for e in ['stats', 'correction', 'files', 'report',
                  'snapshot', 'tests']:
            parse_args('lcmodel', [e, eid], self.xnat_instance, destdir=dd)

        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_035_lcmodel_stats_reformatting(self):
        """LCModel download_stats"""
        from bx.lcmodel import download_stats

        exps = [{"ID": "BBRCDEV_E00398"}, {"ID": "BBRCDEV_E03082"}]
        stats = download_stats(self.xnat_instance, exps)
        stats.sort_values(by=['region', 'subject'], inplace=True)

        assert stats.shape == (6, 72)
        assert list(stats['Cr']) == [7.917, 5.476, 4.544, 5.761, 8.093, 4.664]
        assert list(stats['SNR']) == [23.0, 28.0, 29.0, 33.0, 9.0, 9.0]
        q = 'id == "BBRCDEV_E00398" and region == "cuneus"'
        assert stats.query(q)['NAA+NAAG'].item() == 16.939

    def test_036_lcmodel_correction_merging(self):
        """LCModel download_correction"""
        from bx.lcmodel import download_correction

        exps = [{"ID": "BBRCDEV_E00398"}, {"ID": "BBRCDEV_E03082"}]
        corrs = download_correction(self.xnat_instance, exps)
        corrs.sort_values(by=['region', 'subject'], inplace=True)

        assert corrs.shape == (6, 11)
        assert list(corrs['gm']) == [44.64127726829608, 42.51328813576265,
                                     52.61325203056531, 43.43459982384211,
                                     49.97763657720883, 77.62208767982816]
        assert list(corrs['cov_gm']) == [0.4626002122020262, 0.4782981722285767,
                                         0.6379546884511307, 0.48617843354104,
                                         0.5137290744373951, 0.8719517243928585]
        q = 'id == "BBRCDEV_E00398" and region == "cuneus"'
        assert corrs.query(q)['corrected_csf'].item() == 1.119334437321481

    def test_037_asl3d(self):
        """BASIL-ASL"""
        dd = tempfile.mkdtemp()
        for e in ['perfusion', 'aal', 'maps', 'files',
                  'report', 'snapshot', 'tests']:
            parse_args('asl3d', [e, 'BBRCDEV_E03479'], self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_038_alps(self):
        """ALPS"""
        dd = tempfile.mkdtemp()
        for cmd in ['stats', 'diffusion', 'files', 'snapshot', 'report', 'tests']:
            parse_args('alps', [cmd, 'BBRCDEV_E02949'], self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)

    def test_039_bamos_arterial(self):
        """BAMOS_ARTERIAL"""
        dd = tempfile.mkdtemp()
        for cmd in ['files', 'stats', 'snapshot', 'report', 'tests']:
            parse_args('bamosarterial', [cmd, 'BBRCDEV_E04327'],
                       self.xnat_instance, destdir=dd)
        log.debug('Removing %s', dd)
        shutil.rmtree(dd)        


if __name__ == '__main__':
    unittest.main()
