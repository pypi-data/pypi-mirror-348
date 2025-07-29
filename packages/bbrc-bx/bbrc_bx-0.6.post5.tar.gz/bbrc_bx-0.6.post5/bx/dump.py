
commands = ['archiving tests',
            'ashs volumes',
            'ashs tests',
            'bamos volumes',
            'bamos stats',
            'bamos tests',
            'donsurf aparc',
            'donsurf tests',
            'dtifit tests',
            #'freesurfer6hires aparc',
            #'freesurfer6hires aseg',
            #'freesurfer6hires tests',
            #'freesurfer6hires hippoSfVolumes',
            'freesurfer7 aparc',
            'freesurfer7 aseg',
            'freesurfer7 tests',
            'freesurfer7 amygNucVolumes',
            'freesurfer7 hippoSfVolumes',
            'freesurfer7 hypothalamus',
            'freesurfer7 thalamus',
            'freesurfer7 brainstem',
            'fdg landau',
            'fdg aging',
            'fdg regional',
            'fdg tests',
            'fdg mri',
            'ftm centiloids',
            'ftm regional',
            'ftm tests',
            'ftm mri',
            'tau mri',
            'basil aal',
            'basil stats',
            'basil perfusion',
            'basil tests',
            'asl3d aal',
            'asl3d perfusion',
            'asl3d tests',
            'braak volumes',
            'braak thickness',
            'braak fdg',
            'signature jack',
            'signature dickerson',
            'scandates']


def dump(wd, config=None, interpreter='python', bash_command='/usr/bin/bash', debug=False):
    """ Call every command among those which return numeric endpoints
    (FreeSurfer thickness, volumes, hippocampal subfields, centiloids,
    signatures, Braak regions, etc). This results in a collection of
    spreadsheets to be served by dashboards."""
    import os
    import os.path as op
    import tempfile
    import bx

    alfa_projects = ['ALFA_PLUS_V1_20231120', 'ALFA_PLUS_V2_20230518', 'ALFA_20220301']
    fh, fp = tempfile.mkstemp(suffix='.sh')
    print(fp)
    os.close(fh)
    w = open(fp, 'w')
    cmd = 'mkdir %s' % op.join(wd, 'bx.new')
    w.write('export BX_DUMP=1\n')
    bx_fp = op.join(op.dirname(op.dirname(bx.__file__)), 'bin', 'bx')
    w.write(cmd + '\n')
    for c in commands:
        if 'fdg' in c:
            projects = ['ALFA_PET_FDG_20210421']
        elif 'ftm' in c:
            projects = ['ALFA_PET_FTM_20210421', 'ALFA_PLUS_V2_PET']
        elif 'tau' in c:
            projects = ['ALFA_PLUS_TAU']
        elif 'basil' in c:
            projects = ['ALFA_PLUS2']
        elif 'asl3d' in c:
            projects = ['ALFA_PLUS2_V2']
        else:
            projects = alfa_projects
        for p in projects:
            cmd = ' '.join([interpreter, bx_fp, c, p, '--dest', op.join(wd, 'bx.new')])
            if config:
                cmd += ' --config {}'.format(config)
            print(cmd)
            w.write(cmd + '\n')

    last_commands = ['rm -rf %s/bx.bak' % wd,
                     'mv %s/bx %s/bx.bak' % (wd, wd),
                     'mv %s/bx.new %s/bx' % (wd, wd)]
    for cmd in last_commands:
        w.write(cmd + '\n')

    w.close()

    if not debug:
        os.system('%s %s' % (bash_command, fp))

    # convert excel to csv
    from glob import glob
    import os.path as op
    import subprocess
    xlsx = glob(op.join(wd, 'bx', '*.xlsx'))
    for each in xlsx:
        fn = each.split('.xlsx')[0]
        call = [op.join(op.dirname(interpreter), 'xlsx2csv'), each, op.join(wd, 'bx', fn + '.csv')]
        print(' '.join(call))
        if not debug:
            subprocess.call(call)
