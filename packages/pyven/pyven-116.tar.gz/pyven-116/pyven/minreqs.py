'Pin requires to their minimum allowed versions.'
from .metacheck import egginfodir
from .projectinfo import ProjectInfo
from foyndation import initlogging
from shutil import copy2

def main():
    initlogging()
    info = ProjectInfo.seek('.')
    with (info.projectdir / ProjectInfo.projectaridname).open('a') as f:
        print(f"requires = $list({' '.join(r.minstr() for r in info.parsedrequires())})", file = f)
    with egginfodir(info.projectdir, info.devversion(), True) as (tempdir, d):
        for name in 'PKG-INFO', 'requires.txt':
            p = d / name
            q = info.projectdir / p.relative_to(tempdir)
            if p.exists():
                copy2(p, q)
            elif q.exists():
                q.unlink()

if '__main__' == __name__:
    main()
