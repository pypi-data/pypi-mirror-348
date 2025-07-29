'Release project to PyPI, with manylinux wheels as needed.'
from .checks import EveryVersion
from .container import bgcontainer
from .pipify import InstallDeps, pipify, setuptoolsreq
from .projectinfo import ProjectInfo, SimpleInstallDeps, toreleasetag
from .sourceinfo import SourceInfo
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from foyndation import dotpy, initlogging, singleton, solo
from itertools import chain
from lagoon.binary import tidy
from lagoon.program import NOEOL, partial, Program
from lagoon.text import docker, git
from pkg_resources import resource_filename
from shutil import copy2, copytree, rmtree
from tempfile import NamedTemporaryFile, TemporaryDirectory
from urllib.error import HTTPError
from urllib.request import urlopen
from venvpool import Pip, Pool
import xml.dom.minidom as dom, logging, os, re, sys, sysconfig

log = logging.getLogger(__name__)
distrelpath = 'dist'

class Arch:

    def __init__(self, entrypointornone):
        self.entrypoint = [] if entrypointornone is None else [entrypointornone]

def _images():
    archlookup = dict(
        i686 = Arch('linux32'),
        x86_64 = Arch(None),
    )
    archmatch = re.compile(f"_({'|'.join(map(re.escape, archlookup))})$").search
    images = {
        'manylinux_2_34_x86_64': '2024-11-23-da4547b',
        'manylinux_2_28_x86_64': '2024-11-30-fa0d298',
        'manylinux2014_x86_64': '2024-11-24-a3012f3',
        'manylinux2014_i686': '2024-11-23-da4547b',
    }
    for plat, imagetag in images.items():
        yield Image(imagetag, plat, archlookup[archmatch(plat).group(1)])

class Image:

    prefix = 'quay.io/pypa/'

    @singleton
    def pythonexe():
        impl = f"cp{sysconfig.get_config_var('py_version_nodot')}"
        return f"/opt/python/{impl}-{impl}{sys.abiflags}/bin/python"

    def __init__(self, imagetag, plat, arch):
        self.imagetag = imagetag
        self.plat = plat
        self.arch = arch

    def makewheels(self, info): # TODO: This code would benefit from modern syntax.
        log.info("Make wheels for platform: %s", self.plat)
        scripts = list(info.config.devel.scripts)
        packages = list(info.config.devel.packages)
        # TODO: Copy not mount so we can run containers in parallel.
        with bgcontainer('-v', f"{info.projectdir}:/io", f"{self.prefix}{self.plat}:{self.imagetag}") as container:
            def run(execargs, command):
                docker.exec[print](*execargs, container.cid, *self.arch.entrypoint, *command)
            if packages:
                run([], chain(['yum', 'install', '-y'], packages))
            for script in scripts:
                # TODO LATER: Run as ordinary sudo-capable user.
                dirpath = docker.exec[NOEOL](container.cid, 'mktemp', '-d') # No need to cleanup, will die with container.
                log.debug("In container dir %s run script: %s", dirpath, script)
                run(['-w', dirpath, '-t'], ['sh', '-c', script])
            docker.cp[print](resource_filename(__name__, 'patchpolicy.py'), f"{container.cid}:/patchpolicy.py")
            run([], [self.pythonexe, '/patchpolicy.py'])
            docker.cp[print](resource_filename(__name__, 'bdist.py'), f"{container.cid}:/bdist.py")
            run(['-u', f"{os.geteuid()}:{os.getegid()}", '-w', '/io'], [self.pythonexe, '/bdist.py', '--plat', self.plat])

def _uploadableartifacts(artifactrelpaths):
    def acceptplatform(platform):
        return 'any' == platform or platform.startswith('manylinux')
    platformmatch = re.compile('-([^-]+)[.]whl$').search
    for p in artifactrelpaths:
        name = os.path.basename(p)
        if not name.endswith('.whl') or acceptplatform(platformmatch(name).group(1)):
            yield p
        else:
            log.debug("Not uploadable: %s", p)

def _textcontent(node):
    def iterparts(node):
        value = node.nodeValue
        if value is None:
            for child in node.childNodes:
                for text in iterparts(child):
                    yield text
        else:
            yield value
    return ''.join(iterparts(node))

def _nextversionno(name):
    pattern = re.compile('-([0-9]+)[-.]')
    log.debug('Check PyPI for existing release.')
    try:
        with urlopen(f"https://pypi.org/simple/{name}/") as f:
            doc = dom.parseString(tidy._asxml(input = f.read()))
        last = max(int(pattern.search(_textcontent(a)).group(1)) for a in doc.getElementsByTagName('a'))
    except HTTPError as e:
        if 404 != e.code:
            raise
        last = 0
    return max(10, last + 1)

def _warmups(info):
    warmups = [w.split(':') for w in info.config.warmups]
    if warmups:
        # XXX: Use the same transient venv as used for running tests?
        with InstallDeps(info, (), False, None, False) as installdeps, Pool().readonlyortransient[True](installdeps) as venv:
            for m, f in warmups:
                with NamedTemporaryFile('w', suffix = dotpy, dir = info.projectdir) as script:
                    script.write(f"from {m} import {f.split('.')[0]}\n{f}()")
                    script.flush()
                    venv.run('check_call', ['.'] + installdeps.localreqs, os.path.basename(script.name)[:-len(dotpy)], [], cwd = info.projectdir)

def _runsetup(info, commands):
    with Pool().readonly(SimpleInstallDeps([*info.allbuildrequires, setuptoolsreq])) as venv:
        venv.run('check_call', ['.'], 'setup', commands, cwd = info.projectdir) # XXX: Should venvpool automatically include current dir?

def _release(config, srcgit, versionno, info):
    (info.projectdir / '.git' / 'hooks' / 'post-commit').unlink()
    copygit = git[partial](cwd = info.projectdir)
    scrub = copygit.clean._xdi[partial, print](input = 'c')
    scrub()
    releasetag = toreleasetag(versionno)
    if releasetag not in copygit.tag.__points_at().splitlines():
        pkginfo, = info.projectdir.glob('*.egg-info/PKG-INFO')
        lines = pkginfo.read_text('utf-8').splitlines(True)
        lines[solo(i for i, l in enumerate(lines) if l.startswith('Version: '))] = f"Version: {versionno + 1}.dev0\n"
        pkginfo.write_text(''.join(lines), 'utf-8')
        copygit.add[print](pkginfo)
        copygit.commit[print]('-m', 'release')
        copygit.tag[print](releasetag)
    copygit.push[print](config.golden_remote, 'HEAD', releasetag)
    pipify(info, str(versionno))
    EveryVersion(info, False, False, [], False, True).allchecks(exclude = ['metacheck'])
    scrub()
    for dirpath, dirnames, filenames in os.walk(info.projectdir):
        for name in chain(filenames, dirnames):
            if name.startswith('test_'): # TODO LATER: Allow project to add globs to exclude.
                path = os.path.join(dirpath, name)
                log.debug("Delete: %s", path)
                (os.remove if name.endswith('.py') else rmtree)(path)
    _warmups(info)
    pipify(info, str(versionno))
    rmtree(info.projectdir / '.git')
    setupcommands = []
    if SourceInfo(info.projectdir).extpaths:
        for image in _images():
            image.makewheels(info)
    else:
        setupcommands.append('bdist_wheel')
    _runsetup(info, setupcommands + ['sdist'])
    return [os.path.join(distrelpath, name) for name in sorted(os.listdir(info.projectdir / distrelpath))]

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'release.arid')
    parser = ArgumentParser()
    parser.add_argument('--retry', action = 'store_true', help = 'use artifacts in dist dir')
    parser.add_argument('--upload', action = 'store_true')
    parser.add_argument('path', nargs = '?', default = '.')
    parser.parse_args(namespace = config.cli)
    info = ProjectInfo.seek(config.path)
    config.account = info.config.pypi.account # XXX: Load info config to a scope in our config?
    srcgit = git[partial](cwd = info.projectdir)
    if srcgit.status.__porcelain():
        raise Exception('Uncommitted changes!')
    log.debug('No uncommitted changes.')
    versionno = _nextversionno(info.config.name)
    if config.retry:
        allrelpaths = sorted(p.relative_to(info.projectdir) for p in (info.projectdir / distrelpath).iterdir() if re.match(f"[^-]+-{re.escape(str(versionno))}[-.]", p.name) is not None)
    else:
        with TemporaryDirectory() as tempdir:
            copydir = os.path.join(tempdir, os.path.basename(os.path.abspath(info.projectdir)))
            log.info("Copying project to: %s", copydir)
            copytree(info.projectdir, copydir)
            allrelpaths = _release(config, srcgit, versionno, ProjectInfo.seek(copydir))
            for relpath in allrelpaths:
                log.info("Replace artifact: %s", relpath)
                destpath = info.projectdir / relpath
                destpath.parent.mkdir(exist_ok = True, parents = True)
                copy2(os.path.join(copydir, relpath), destpath)
    uploadablerelpaths = _uploadableartifacts(allrelpaths)
    if config.upload:
        with config.token as token:
            Program.text(sys.executable)._m.twine.upload[print]('-u', '__token__', '-p', token, *uploadablerelpaths, cwd = info.projectdir, env = Pip.envpatch)
    else:
        log.warning("Upload skipped, use --upload to upload: %s", ' '.join(map(str, uploadablerelpaths)))

if '__main__' == __name__:
    main()
