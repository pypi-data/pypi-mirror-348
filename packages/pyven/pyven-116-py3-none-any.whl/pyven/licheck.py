import hashlib, re, shlex, sys

gpltemplate = """# Copyright {years} {author}

# This file is part of {name}.
#
# {name} is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# {name} is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with {name}.  If not, see <http://www.gnu.org/licenses/>.
"""
intersection = '''# This file incorporates work covered by the following copyright and
# permission notice:
'''

def _hassuffix(name, *suffixes):
    return name.endswith(suffixes) or name.endswith(tuple(f"{s}.aridt" for s in suffixes))

def _checkmd5(info, name, expected):
    licpath = info.projectdir / name
    md5 = hashlib.md5()
    with licpath.open() as f:
        md5.update(f.read().encode('utf_8'))
    if expected != md5.hexdigest():
        raise Exception(licpath)

def licheck(info, paths):
    if not info.config.licheck.enabled:
        sys.stderr.write('SKIP ')
        return
    sections = []
    for name in info.config.licenses:
        if sections:
            sections.append(intersection)
        if 'GPL' == name:
            sections.append(gpltemplate.format(
                years = ', '.join(map(str, info.config.years)),
                author = info.config.author,
                name = info.config.name,
            ))
        elif 'MIT' == name:
            with info.mitpath().open() as f:
                sections.append(''.join(('# ' if l.rstrip() else '#') + l for l in f))
        elif 'UNLICENSE' == name:
            pass
        else:
            raise Exception(name)
    master = ''.join(s + '\n' for s in sections) # Check each section ends with 2 newlines.
    def checkone(path):
        with path.open() as f:
            text = f.read()
        if text.startswith('#!'):
            for _ in range(2):
                text = text[text.index('\n') + 1:]
        if _hassuffix(path.name, '.s'):
            text = re.sub('^;', '#', text, flags = re.MULTILINE)
        elif _hassuffix(path.name, '.h', '.cpp', '.cxx', '.gradle', '.java'):
            text = re.sub('^//', '#', text, flags = re.MULTILINE)
        elif _hassuffix(path.name, '.arid'):
            text = re.sub('^:', '#', text, flags = re.MULTILINE)
        return master == text[:len(master)]
    badpaths = [p for p in paths if not checkone(p)]
    if badpaths:
        raise Exception(' '.join(map(shlex.quote, map(str, badpaths))))
    if 'GPL' in info.config.licenses:
        _checkmd5(info, 'COPYING', 'd32239bcb673463ab874e80d47fae504')
    if 'UNLICENSE' in info.config.licenses:
        _checkmd5(info, 'UNLICENSE', '7246f848faa4e9c9fc0ea91122d6e680')
