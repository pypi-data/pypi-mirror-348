from .container import bgcontainer, Container, pyimage
from .files import Files
from .pipify import InstallDeps
from .projectinfo import ProjectInfo, SimpleInstallDeps
from .util import Excludes, stderr
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from aridity.util import NoSuchPathException, openresource
from foyndation import dotpy, initlogging, singleton
from http import HTTPStatus
from itertools import chain
from lagoon.text import diff, pydoc_markdown, tidy
from lagoon.url import URL
from pathlib import Path
from setuptools import find_packages
from shutil import copy2, copytree, ignore_patterns
from subprocess import DEVNULL
from tempfile import NamedTemporaryFile, TemporaryDirectory
from urllib.error import HTTPError
from urllib.parse import unquote
from venvpool import Pool
from xml.sax.saxutils import escape as xml_escape
import xml.etree.ElementTree as ET, logging, os, re, sys

log = logging.getLogger(__name__)
commentregex = ' \N{NUMBER SIGN} .+'
skip = object()

@singleton
class yesno:

    d = dict(no = False, yes = True)

    def __call__(self, s):
        return self.d[s]

def _localrepo():
    cc = ConfigCtrl()
    cc.loadsettings()
    return Path(cc.node.buildbot.repo)

def _runcheck(variant, check, *args):
    sys.stderr.write(f"{check.__name__}[{variant}]: ")
    sys.stderr.flush()
    stderr('SKIP' if check(*args) is skip else 'OK')

class EveryVersion:

    def __init__(self, info, siblings, userepo, noseargs, docker, transient):
        self.files = Files(info.projectdir)
        self.info = info
        self.siblings = siblings
        self.userepo = userepo
        self.noseargs = noseargs
        self.docker = docker
        self.transient = transient

    def allchecks(self, exclude = ()):
        for check in self.licheck, self.nlcheck, self.execcheck, self.metacheck, self.pyflakes, self.nose, self.readme, self.github, self.linktree, self.wiki:
            if check.__name__ in exclude:
                log.warning("Exclude: %s", check.__name__)
            else:
                check()

    def licheck(self):
        from .licheck import licheck
        def g():
            excludes = Excludes(self.info.config.licheck.exclude.globs)
            for path in self.files.allsrcpaths:
                if os.path.relpath(path, self.files.root) not in excludes:
                    yield path
        _runcheck('*', licheck, self.info, list(g()))

    def nlcheck(self):
        from .nlcheck import nlcheck
        _runcheck('*', nlcheck, self.files.allsrcpaths)

    def execcheck(self):
        from .execcheck import execcheck
        _runcheck('*', execcheck, self.files.pypaths)

    def metacheck(self):
        from .metacheck import metacheck
        _runcheck('*', metacheck, self.info.projectdir, self.info.devversion(), self.docker) # FIXME: Expect devversion specific to commit being built.

    def pyflakes(self):
        paths = [str(path) for excludes in [Excludes(self.info.config.flakes.exclude.globs)]
                for path in self.files.pypaths if os.path.relpath(path, self.files.root) not in excludes]
        def pyflakes():
            if paths:
                with Pool().readonly(SimpleInstallDeps(['pyflakes>=3.2'])) as venv:
                    venv.run('check_call', [], 'pyflakes', paths)
        _runcheck(3, pyflakes)

    basenoseargs = '--capture-output', '--exe', '-v', '--with-doctest', '--doctest-extension', '.mediawiki', '--with-cov', '--cov-report', 'term-missing', '--with-xunit'

    def _spokeurl(self):
        try:
            url = self.info.config.wiki_url
        except AttributeError:
            return
        return URL.text(url[:url.index('/w/')])

    def nose(self):
        url = self._spokeurl()
        doctestpath = self.info.projectdir / 'var' / 'doctest.mediawiki'
        doctestpath.parent.mkdir(exist_ok = True)
        with doctestpath.open('w') as f:
            if url is not None:
                try:
                    result = tidy._asxml(check = False, input = url.w(f"Category:Doctest/{self.info.config.name}"), stderr = DEVNULL)
                except HTTPError as e:
                    if e.code != HTTPStatus.NOT_FOUND:
                        raise
                else:
                    assert result.returncode in {0, 1}
                    for a in ET.fromstring(result.stdout).findall('''.//{http://www.w3.org/1999/xhtml}div[@class='mw-category-group']//{http://www.w3.org/1999/xhtml}a'''):
                        uri = a.get('href')
                        f.write(url('index.php', query = dict(action = 'raw', title = unquote(uri[uri.index('/w/') + 3:]))))
        upstream_devel_packages = list(self.info.config.upstream.devel.packages)
        upstream_devel_scripts = list(self.info.config.upstream.devel.scripts) if self.userepo else []
        # TODO: Facility to freeze test requirements graph.
        with InstallDeps(self.info, ('nose-cov', 'pynose', *self.info.config.test.requires), self.siblings, _localrepo(), self.userepo) as installdeps:
            reportsdir = self.info.projectdir / 'var' / '3'
            reportsdir.mkdir(exist_ok = True, parents = True)
            xmlpath = reportsdir / 'nosetests.xml'
            testpaths = self.files.testpaths([doctestpath], xmlpath)
            if self.docker:
                coveragepath = self.info.projectdir / '.coverage'
                with bgcontainer('-v', "{0}:{0}".format('/var/run/docker.sock'), '--network', 'host', '-v', f"{os.path.abspath(self.info.projectdir)}:{Container.workdir}", pyimage(self.info.pyversiontags[0], upstream_devel_packages, upstream_devel_scripts, *installdeps.corereqslayers())) as container:
                    container.cp(installdeps.workspace, 'installdeps')
                    container.installasuser(installdeps.containerrequires())
                    cpath = lambda p: os.path.relpath(p, self.info.projectdir).replace(os.sep, '/')
                    status = container.inworkdir.nosetests[print](
                        *self.basenoseargs, '--xunit-file', cpath(xmlpath),
                        *sum((['--cov', p] for p in chain(find_packages(self.info.projectdir), self.info.py_modules())), []), *map(cpath, testpaths), *self.noseargs,
                    check = False)
            else:
                coveragepath = Path('.coverage')
                with Pool().readonlyortransient[self.transient](installdeps) as venv:
                    status = venv.run('call', installdeps.localreqs, 'nose', [
                        *self.basenoseargs, '--xunit-file', xmlpath,
                        *sum((['--cov', p] for p in chain(find_packages(self.info.projectdir), self.info.py_modules())), []), *map(str, testpaths), *self.noseargs,
                    ])
            if coveragepath.exists():
                copy2(coveragepath, reportsdir / 'coverage') # Replace whatever the status, as if we configured the location.
                coveragepath.unlink() # Can't simply use rename cross-device in release case.
            assert not status

    def readme(self):
        def first(scope, resolvable):
            for _, o in resolvable.resolve(scope).resolveditems():
                return o
            raise NoSuchPathException('Empty set.')
        def getpydoc(mainmodules):
            with TemporaryDirectory() as pydocparent:
                pydocdir = os.path.join(pydocparent, 'project')
                copytree(self.info.projectdir, pydocdir, ignore = ignore_patterns('test_*'))
                internal = {(os.path.dirname(mm.relpath) if '__init__.py' == os.path.basename(mm.relpath) else mm.relpath[:-len(dotpy)]).replace(os.sep, '.') for mm in mainmodules}
                internal.update(self.info.config.internal_module)
                modules = []
                for dirpath, dirnames, filenames in os.walk(pydocdir):
                    for name in filenames:
                        if name.endswith(dotpy):
                            pypath = os.path.join(dirpath, name)
                            with open(pypath, 'r+') as f:
                                text = f.read()
                                cleantext = re.sub(commentregex, '', text, flags = re.MULTILINE)
                                if cleantext != text:
                                    f.seek(0)
                                    f.write(cleantext)
                                    f.truncate()
                            modules.append(os.path.relpath(dirpath if '__init__.py' == name else pypath[:-len(dotpy)], pydocdir).replace(os.sep, '.'))
                acc = re.sub('^#', '###', pydoc_markdown('--search-path', pydocdir), flags = re.MULTILINE)
                acc = re.split(f"""(?=^<a id="(?:{'|'.join(map(re.escape, modules))})")""", acc, flags = re.MULTILINE) # Module names are markup attribute-safe.
                return ''.join(sorted(block for block in acc if block and re.search('"([^"]+)', block).group(1) not in internal))
        def readme():
            if not (self.info.config.github.participant or self.info.config.pypi.participant):
                return skip
            cc = (-self.info.config).childctrl()
            cc.w.first = first
            if self.info.config.readme_verbose:
                cc.w.verbose_blank = ''
            cc.execute('commands * name = $label()')
            mainmodules = sorted(self.info.mainmodules(), key = lambda mm: mm.command)
            undocumented = [mm.command for mm in mainmodules if mm.doc is None]
            if undocumented:
                raise Exception(f"Undocumented: {undocumented}")
            for mm in mainmodules:
                getattr(cc.w.commands, mm.command).doc = mm.doc
            if self.info.config.pydoc_enabled:
                cc.w.pydoc = getpydoc(mainmodules)
            with NamedTemporaryFile('w') as g:
                with openresource(__name__, 'README.md.aridt') as f:
                    cc.processtemplate(f, g)
                g.flush()
                completed = diff(g.name, self.info.projectdir / 'README.md', check = False)
                sys.stdout.write(completed.stdout)
                assert completed.returncode in {0, 1}
                assert all('<' != l[0] for l in completed.stdout.splitlines())
        _runcheck('*', readme)

    def github(self):
        def github():
            if not self.info.config.github.participant:
                return skip
            description, _ = self.info.descriptionandurl()
            assert self.info.config.tagline == description
        _runcheck('*', github)

    def linktree(self):
        def linktree():
            account = self.info.config.linktree.account
            if account is None:
                return skip
            assert f">{xml_escape(self.info.config.name)} \N{BULLET} {xml_escape(self.info.config.tagline)}<" in URL.text('https://linktr.ee')(account)
        _runcheck('*', linktree)

    def wiki(self):
        def wiki():
            url = self._spokeurl()
            if url is None:
                return skip
            assert url('index.php', query = dict(action = 'raw', title = f"Template:{self.info.config.name}/tagline")) == self.info.config.tagline
        _runcheck('*', wiki)

def main():
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('--docker', action = 'store_true')
    parser.add_argument('--repo', type = yesno, default = True)
    parser.add_argument('--siblings', type = yesno, default = True)
    parser.add_argument('--transient', action = 'store_true')
    args, noseargs = parser.parse_known_args()
    EveryVersion(ProjectInfo.seekany('.'), args.siblings, args.repo, noseargs, args.docker, args.transient).allchecks()
