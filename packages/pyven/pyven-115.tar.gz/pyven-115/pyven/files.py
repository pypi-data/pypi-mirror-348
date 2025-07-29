from collections import defaultdict
from foyndation import dotpy
from lagoon.program import partial
from lagoon.text import git
from pathlib import Path
import xml.dom.minidom as dom, os

class Files:

    @staticmethod
    def _findfiles(walkpath, suffixes, prefixes):
        for dirpath, dirnames, filenames in os.walk(walkpath):
            for name in sorted(filenames):
                if any(name.endswith(suffix) for suffix in suffixes) or any(name.startswith(prefix) for prefix in prefixes):
                    yield Path(dirpath, name).relative_to(walkpath)
            dirnames.sort()

    @classmethod
    def relpaths(cls, root, suffixes, prefixes):
        paths = list(cls._findfiles(root, suffixes, prefixes))
        if paths:
            with git.check_ignore[partial](*paths, check = False, cwd = root) as p:
                ignored = set(p.stdout.read().splitlines())
                assert p.wait() in [0, 1]
            for path in paths:
                if str(path) not in ignored:
                    yield path

    def __init__(self, root):
        srcsuffixes = [x for s in ['.py', '.py3', '.pyx', '.s', '.sh', '.h', '.cpp', '.cxx', '.arid', '.gradle', '.java', '.mk', '.md'] for x in [s, f"{s}.aridt"]]
        self.allsrcpaths = [root / p for p in self.relpaths(root, srcsuffixes, ['Dockerfile', 'Makefile'])]
        self.pypaths = [p for p in self.allsrcpaths if p.name.endswith('.py')]
        self.root = root

    def testpaths(self, docpaths, reportpath):
        paths = [p for p in self.pypaths if os.path.basename(p).startswith('test_')] + docpaths
        if reportpath.exists():
            with reportpath.open() as f:
                doc = dom.parse(f)
            nametopath = {'.'.join(p.relative_to(self.root).parts)[:-len(dotpy)]: p for p in paths} # FIXME: Correctly handle docpaths.
            pathtotime = defaultdict(int)
            for e in doc.getElementsByTagName('testcase'):
                name = e.getAttribute('classname')
                while True:
                    i = name.rfind('.')
                    if -1 == i:
                        break
                    name = name[:i]
                    if name in nametopath:
                        pathtotime[nametopath[name]] += float(e.getAttribute('time'))
                        break
            paths.sort(key = lambda p: pathtotime.get(p, float('inf')))
        return paths
