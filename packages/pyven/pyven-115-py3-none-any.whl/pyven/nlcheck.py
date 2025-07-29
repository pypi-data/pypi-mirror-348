import re

class MoreThanOneEolStyleException(Exception): pass

def nlcheck(paths):
    for path in paths:
        with path.open('rb') as f:
            text = f.read().decode()
        eols = set(re.findall(r'\r\n|[\r\n]', text))
        if len(eols) > 1:
            raise MoreThanOneEolStyleException(path)
