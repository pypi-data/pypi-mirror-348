"""
Hooks
"""
import os
import re

from .helpers import tipify

# TODO: refactor metadata_from_path in helpers, operating on a simple string

def metadata_from_path(entry, aliases=(), path='_dirname'):
    """
    Return a dictionary of metadata extracted from the `path` of the
    `entry` dictionary.
    """
    # Aliases could be something like
    # aliases = (('T', 'temperature'),
    #            ('P', 'pressure'))
    path = entry[path]
    db = {}
    for entry in os.path.dirname(path).split('/'):
        for sub in entry.split('_'):
            res = re.match('([a-zA-Z]*)([0-9.]*)', sub)
            if len(res.group(1)) > 0 and len(res.group(2)) > 0:
                key = res.group(1)
                for alias in aliases:
                    if key == alias[0]:
                        key = alias[1]
                        break
                db[key] = tipify(res.group(2))
    return db

def absolute_path(entry, root):
    """Hook to add absolute path to entry"""
    if entry['path'].startswith('/'):
        return {'absolute_path': entry['path']}
    else:
        return {'absolute_path': os.path.join(root, entry['path'])}
