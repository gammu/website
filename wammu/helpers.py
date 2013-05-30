import re

BUG_RE = re.compile('(bug ?#([0-9]*))')
ISSUE_RE = re.compile('(issue ?#([0-9]*))')
LP_RE = re.compile('(LP ?#([0-9]*))')
BDO_RE = re.compile('(bdo ?#([0-9]*))')

def process_bug_links(text):
    '''
    Makes links in form bug #123 clickable to bugs.cihar.com.
    '''
    text = LP_RE.sub(r'[\1](https://bugs.launchpad.net/bugs/\2)', text)
    text = BDO_RE.sub(r'[\1](http://bugs.debian.org/\2)', text)
    text = ISSUE_RE.sub(r'[\1](https://github.com/gammu/gammu/\2)', text)
    return BUG_RE.sub(r'[\1](https://bugs.cihar.com/\2)', text)
