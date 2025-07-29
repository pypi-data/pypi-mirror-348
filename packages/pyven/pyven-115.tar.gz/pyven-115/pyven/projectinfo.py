from . import mainmodules
from .files import Files
from .util import Seek
from aridity.config import ConfigCtrl
from aridity.model import Entry, Resource
from aridity.util import openresource
from foyndation import dotpy, rmsuffix, solo
from inspect import getsource
from lagoon.program import Program
from lagoon.text import git
from pkg_resources import parse_requirements
from roman import fromRoman, toRoman
from setuphacks import getsetupkwargs
from urllib.error import HTTPError
from urllib.request import urlopen
from venvpool import ParsedRequires, TemporaryDirectory
import json, logging, os, re, time, venvpool

log = logging.getLogger(__name__)

def toreleasetag(versionno):
    return f"release/{toRoman(versionno).lower()}"

class ProjectInfoNotFoundException(Exception): pass

class Req:

    namematch = re.compile(r'\S+').search

    @classmethod
    def parselines(cls, lines):
        return [cls(parsed) for parsed in parse_requirements(lines)]

    @property
    def namepart(self):
        return self.parsed.name

    @property
    def extras(self):
        return self.parsed.extras

    @property
    def reqstr(self):
        return str(self.parsed)

    @property
    def specifierset(self):
        return self.parsed.specifier

    def __init__(self, parsed):
        self.parsed = parsed

    def acceptversion(self, versionstr):
        return versionstr in self.parsed

    def siblingpath(self, workspace):
        return workspace / self.namepart

    def isproject(self, info):
        return self.siblingpath(info.contextworkspace()).exists()

    def minversion(self):
        return solo(s.version for s in self.specifierset if s.operator in {'>=', '=='})

    def minstr(self):
        return f"{self.namepart}=={self.minversion()}"

    def accept(self):
        marker = self.parsed.marker
        try:
            if marker is None or marker.evaluate():
                assert not self.parsed.extras # Not supported.
                return True
        except ValueError as e:
            if 'UndefinedEnvironmentName' != type(e).__name__:
                raise

    def keyversion(self):
        s, = self.specifierset
        return self.parsed.key, s.version

class SimpleInstallDeps(ParsedRequires):

    parselines = staticmethod(Req.parselines)

class ProjectInfo:

    projectaridname = 'project.arid'

    @classmethod
    def seek(cls, realdir):
        seek = Seek.seek(realdir, cls.projectaridname)
        if seek is None:
            raise ProjectInfoNotFoundException(realdir)
        return cls(seek.parent, seek.path)

    @classmethod
    def seekany(cls, realdir):
        try:
            return cls.seek(realdir)
        except ProjectInfoNotFoundException:
            pass
        setupseek = Seek.seek(realdir, 'setup.py')
        if setupseek is not None:
            log.info('Use setuptools mode.')
            return cls._setuptoolsinfo(setupseek.path)
        log.info('Use uninstallable mode.')
        projectdir = Seek.seek(realdir, '.git').path.parent
        with openresource(__name__, 'setuptools.arid') as f:
            info = cls(projectdir, f)
        info.config.name = os.path.basename(os.path.abspath(projectdir))
        try:
            info.allrequires.extend((projectdir / 'requirements.txt').read_text().splitlines())
        except FileNotFoundError:
            pass
        return info

    @classmethod
    def _setuptoolsinfo(cls, setuppath):
        with openresource(__name__, 'setuptools.arid') as f:
            info = cls(setuppath.parent, f)
        setupkwargs = getsetupkwargs(setuppath, ['name', 'install_requires', 'entry_points'])
        if 'name' in setupkwargs:
            info.config.name = setupkwargs['name']
        info.allrequires.extend(setupkwargs.get('install_requires', []))
        console_scripts = setupkwargs.get('entry_points', {}).get('console_scripts')
        info.console_scripts = lambda: console_scripts
        return info

    def __init__(self, projectdir, infopathorstream):
        cc = ConfigCtrl()
        Resource(__name__, 'projectinfo.arid', 'utf-8').source(cc.scope, Entry([])) # TODO: Should be explicit project.arid include.
        cc.load(infopathorstream)
        self.allbuildrequires = list(cc.r.build.requires)
        self.allrequires = list(cc.r.requires)
        self.pyversiontags = list(map(str, cc.r.pyversiontag)) # TODO: API to unparse instead of best scalar.
        self.config = cc.node
        self.projectdir = projectdir

    def mitpath(self):
        return self.projectdir / self.config.MIT.path

    def contextworkspace(self):
        return self.projectdir / '..'

    def parsedrequires(self):
        return Req.parselines(self.allrequires)

    def localrequires(self):
        return [r.namepart for r in self.parsedrequires() if r.isproject(self)]

    def descriptionandurl(self):
        urlpath = f"{self.config.github.account}/{self.config.name}"
        while True:
            try:
                with urlopen(f"https://api.github.com/repos/{urlpath}") as f:
                    return json.loads(f.read().decode())['description'], f"https://github.com/{urlpath}"
            except HTTPError as e:
                if 403 != e.code:
                    raise
                log.info("Sleep 1 minute due to: %s", e)
                time.sleep(60)

    def py_modules(self):
        return [stem for name in os.listdir(self.projectdir) if (stem := rmsuffix(name, dotpy)) is not None and 'setup.py' != name and not name.startswith('test_')]

    def mainmodules(self):
        paths = list(Files.relpaths(self.projectdir, [mainmodules.extension], []))
        with TemporaryDirectory() as tempdir:
            scriptpath = os.path.join(tempdir, 'mainmodules.py')
            with open(scriptpath, 'w') as f:
                f.write(getsource(mainmodules))
            with open(os.path.join(tempdir, 'venvpool.py'), 'w') as f:
                f.write(getsource(venvpool))
            for line in Program.text('python3')(scriptpath, self.projectdir, *paths).splitlines():
                yield MainModule(eval(line))

    def console_scripts(self):
        return [mm.console_script for mm in self.mainmodules()]

    def releases(self):
        for tag in git.tag(cwd = self.projectdir).splitlines():
            m = re.fullmatch('release/(.+)', tag)
            if m is not None:
                versionstr = m.group(1)
                try:
                    yield int(versionstr)
                except ValueError:
                    yield fromRoman(versionstr)

    def devversion(self):
        return f"{max(self.releases(), default = 0) + 1}.dev0"

class MainModule:

    def __init__(self, d):
        for k, v in d.items():
            setattr(self, k, v)
