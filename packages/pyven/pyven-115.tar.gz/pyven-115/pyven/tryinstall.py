'Check last release can be installed from PyPI and its tests still pass, for use by CI.'
from .checks import EveryVersion
from .container import bgcontainer, pyimage
from .projectinfo import ProjectInfo, toreleasetag
from argparse import ArgumentParser
from foyndation import initlogging
from lagoon.text import git
from roman import fromRoman
import logging, re

log = logging.getLogger(__name__)

def main():
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('branch')
    branch = parser.parse_args().branch
    headinfo = ProjectInfo.seek('.')
    if not headinfo.config.pypi.participant: # XXX: Or look for tags?
        log.info('Not user-installable.')
        return
    project = headinfo.config.name
    releasematch = re.fullmatch('release/(.+)', branch)
    versionno = max(headinfo.releases()) if releasematch is None else fromRoman(releasematch.group(1))
    req = f"{project}=={versionno}"
    upstream_devel_packages = list(headinfo.config.upstream.devel.packages)
    for pyversion in reversed(headinfo.pyversiontags):
        log.info("Python version: %s", pyversion)
        with bgcontainer(pyimage(pyversion, upstream_devel_packages, [])) as container:
            container.installasuser([req])
    git.checkout[print](toreleasetag(versionno))
    EveryVersion(ProjectInfo.seek('.'), False, False, [], True, True).nose()

if '__main__' == __name__:
    main()
