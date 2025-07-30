'Show all XX''X/TO''DO/FIX''ME comments in project.'
from .files import Files
from argparse import ArgumentParser
from lagoon.program import NOEOL, partial
from lagoon.text import ag, git

def main():
    parser = ArgumentParser()
    parser.add_argument('-q', action = 'count', default = 0)
    config = parser.parse_args()
    root = git.rev_parse.__show_toplevel[NOEOL]()
    agcommand = ag.__noheading.__nobreak[partial, print](cwd = root, check = False)
    # XXX: Integrate with declared project resource types?
    paths = list(Files.relpaths(root, ['.py', '.pyx', '.h', '.cpp', '.ui', '.java', '.kt', '.c', '.s', '.sh', '.arid', '.aridt', '.gradle', '.java', '.mk', '.js'], ['Dockerfile', 'Makefile']))
    for tag in ['XX''X', 'TO''DO', 'FIX''ME'][config.q:]:
        agcommand(f"{tag} LATER", *paths)
        agcommand(f"{tag}(?! LATER)", *paths)

if '__main__' == __name__:
    main()
