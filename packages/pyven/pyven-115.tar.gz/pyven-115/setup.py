from setuptools import setup
try:
    from Cython.Build import cythonize
except ModuleNotFoundError:
    pass
from pathlib import Path
from setuptools import find_packages
import os

class SourceInfo:

    class PYXPath:

        def __init__(self, module, path):
            self.module = module
            self.path = path

        def make_ext(self):
            g = {}
            with open(f"{self.path}bld") as f: # Assume project root.
                exec(f.read(), g)
            return g['make_ext'](self.module, self.path)

    def __init__(self, rootdir):
        def addextpaths(dirpath, moduleprefix, suffix = '.pyx'):
            for name in sorted(os.listdir(os.path.join(rootdir, dirpath))):
                if name.endswith(suffix):
                    module = f"{moduleprefix}{name[:-len(suffix)]}"
                    if module not in extpaths:
                        extpaths[module] = self.PYXPath(module, os.path.join(dirpath, name))
        self.packages = find_packages(rootdir)
        extpaths = {}
        addextpaths('.', '')
        for package in self.packages:
            addextpaths(package.replace('.', os.sep), f"{package}.")
        self.extpaths = extpaths.values()

    def setup_kwargs(self):
        kwargs = dict(packages = self.packages)
        try:
            kwargs['long_description'] = Path('README.md').read_text()
            kwargs['long_description_content_type'] = 'text/markdown'
        except FileNotFoundError:
            pass
        if self.extpaths:
            kwargs['ext_modules'] = cythonize([path.make_ext() for path in self.extpaths])
        return kwargs

sourceinfo = SourceInfo('.')
setup(
    name = 'pyven',
    version = '115',
    description = 'Manage development of multiple Python projects',
    url = 'https://pypi.org/project/pyven/',
    author = 'Homsar',
    author_email = 'homsar@foyono.com',
    py_modules = [],
    install_requires = ['aridity>=85', 'diapyr>=31', 'foyndation>=10', 'lagoon>=49', 'pydoc-markdown>=3.3', 'roman>=5', 'setuptools>=44.1.1', 'twine>=1.15.0', 'venvpool>=18'],
    package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
    entry_points = {'console_scripts': ['minreqs=pyven.minreqs:main', 'pipify=pyven.pipify:main', 'release=pyven.release:main', 'tasks=pyven.tasks:main', 'tryinstall=pyven.tryinstall:main', 'tests=pyven.tests.__init__:main']},
    **sourceinfo.setup_kwargs(),
)
