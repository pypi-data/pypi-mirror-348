from foyndation import rmsuffix
from pathlib import Path
import os, re, sys

def stderr(obj):
    sys.stderr.write(str(obj))
    sys.stderr.write(os.linesep)

class Excludes:

    def __init__(self, globs):
        def disjunction():
            sep = re.escape(os.sep)
            star = f"[^{sep}]*"
            def components():
                for word in glob.split('/'):
                    if '**' == word:
                        yield f"(?:{star}{sep})*"
                    else:
                        yield star.join(re.escape(part) for part in word.split('*'))
                        yield sep
            for glob in globs:
                assert (regex := rmsuffix(''.join(components()), sep)) is not None
                yield regex
        self.pattern = re.compile(f"^{'|'.join(disjunction())}$")

    def __contains__(self, relpath):
        return self.pattern.search(relpath) is not None

class Seek:

    @classmethod
    def seek(cls, dirpath, name):
        dirpath = Path(dirpath)
        while True:
            path = dirpath / name
            if path.exists():
                seek = cls()
                seek.path = path
                seek.parent = dirpath
                return seek
            parent = dirpath / '..'
            if os.path.abspath(parent) == os.path.abspath(dirpath):
                break
            dirpath = parent
