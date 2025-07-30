from aridity.config import ConfigCtrl
from contextlib import contextmanager
from dkrcache.util import iidfile
from importlib.resources import files
from lagoon.program import NOEOL, partial
from lagoon.text import docker
from lagoon.util import mapcm
from pathlib import Path
from tempfile import TemporaryDirectory
import os, shlex

@contextmanager
def bgcontainer(*dockerrunargs):
    cid = docker.run._d[NOEOL](*dockerrunargs, 'sleep', 'inf')
    try:
        yield Container(cid)
    finally:
        docker.rm._f[print](cid)

def pyimage(pyversiontag, packages, scripts, *requireslayers):
    cc = ConfigCtrl()
    cc.execute('package := $list()')
    cc.execute('pipinstallsh := $list()')
    cc.execute('script := $list()')
    cc.w.docker_gid = Path('/var/run/docker.sock').stat().st_gid
    for p in packages:
        cc.w.package += p
    for requires in requireslayers:
        cc.w.pipinstallsh += f"sudo -u pyvenuser pip install --user --no-warn-script-location {' '.join(map(shlex.quote, requires))}"
    cc.w.pyven_gid = os.getegid()
    cc.w.pyven_uid = os.geteuid()
    cc.w.pyversiontag = pyversiontag
    for script in scripts:
        cc.w.script += script
    with mapcm(Path, TemporaryDirectory()) as tempdir:
        with (files() / 'Dockerfile.aridt').open() as f, (tempdir / 'Dockerfile').open('w') as g:
            cc.processtemplate(f, g)
        with iidfile() as iid:
            docker.build[print](*iid.args, tempdir)
            return iid.read()

class Container:

    workdir = '/io'

    def __init__(self, cid):
        self.inworkdir = docker.exec[partial]('-w', self.workdir, cid).sudo._u.pyvenuser[partial]('PATH=/home/pyvenuser/.local/bin:/usr/local/bin:/usr/bin:/bin').env
        self.cid = cid

    def installasuser(self, requires):
        if requires:
            docker.exec[print](self.cid, 'sudo', '-u', 'pyvenuser', 'pip', 'install', '--user', '--no-warn-script-location', *requires)

    def cp(self, src, dest):
        docker.cp[print](src, f"{self.cid}:{dest}")
