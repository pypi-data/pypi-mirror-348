from .checks import skip
from .container import bgcontainer, Container, pyimage
from .pipify import pipify, setupcommand, setuptoolsreq
from .projectinfo import ProjectInfo
from contextlib import contextmanager
from lagoon.text import diff
from pathlib import Path
from shutil import copy2
from tempfile import TemporaryDirectory

@contextmanager
def egginfodir(projectdir, version, dockerenabled):
    with TemporaryDirectory() as tempdir:
        copy2(projectdir / ProjectInfo.projectaridname, tempdir)
        for glob in 'README.md', 'LICEN[CS]E*', 'COPYING*', 'NOTICE*', 'AUTHORS*':
            for p in projectdir.glob(glob):
                copy2(p, tempdir)
        copyinfo = ProjectInfo.seek(tempdir)
        pipify(copyinfo, version)
        if dockerenabled and {'setuptools', 'wheel'} != set(copyinfo.allbuildrequires):
            with bgcontainer('-v', f"{tempdir}:{Container.workdir}", pyimage(copyinfo.pyversiontags[0], [], [], [*copyinfo.allbuildrequires, setuptoolsreq])) as container:
                container.inworkdir.python[print]('setup.py', 'egg_info')
        else:
            setupcommand(copyinfo, False, 'egg_info')
        d, = Path(tempdir).glob('*.egg-info')
        yield tempdir, d

def metacheck(projectdir, version, dockerenabled):
    if not (projectdir / ProjectInfo.projectaridname).exists():
        return skip
    with egginfodir(projectdir, version, dockerenabled) as (tempdir, d):
        p = d / 'PKG-INFO'
        diff[print](p, projectdir / p.relative_to(tempdir))
