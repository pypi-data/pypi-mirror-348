"""
Parsers
"""
import os
import re
import functools

__all__ = ['parser_as_hook', 'parse_pickle', 'parse_yaml', 'parse_txt',
           'parse_txt_unpack', 'parse_path']


def parse_path(path, aliases=()):
    """Parse metadata from path itself"""
    # Aliases can be something like
    # aliases = (('T', 'temperature'),
    #            ('P', 'pressure'))
    from .helpers import tipify
    db = {}
    for entry in os.path.dirname(path).split('/'):
        for sub in entry.split('_'):
            res = re.match('([a-zA-Z]*)([0-9.]*)', sub)
            if len(res.group(2)) > 0:
                key = res.group(1)
                for alias in aliases:
                    if key == alias[0]:
                        key = alias[1]
                        break
                db[key] = tipify(res.group(2))
    return db

def parse_absolute_path(path):
    """Return a dict with the absolute path of `path`"""
    return {'absolute_path': os.path.abspath(path)}

def parse_pickle(path):
    """Parse a numpy pickled file"""
    import pickle
    with open(path, 'rb') as fh:
        data = pickle.load(fh)
    if data is None:
        data = {}
    return data

def parse_yaml(path):
    """Parse a yaml formatted file"""
    import yaml
    with open(path, 'r') as fh:
        data = yaml.safe_load(fh)
    if data is None:
        data = {}
    return data

# TODO: deprecate this
def parse_txt_unpack(path):
    import numpy
    import re
    with open(path, 'r') as fh:
        # Fail with binary files
        try:
            data = numpy.loadtxt(fh, unpack=True)
        except:
            print('FAIL!!')
            raise
            # return {}

        # Guess column names
        columns = None
        fh.seek(0)
        for line in fh:
            if line.startswith('#'):
                match = re.match('# columns:', line)
                if match is not None:
                    columns = line.split(':')[1]
                    columns = re.sub(r'\(([a-z]+),(\s*[a-z]+)\)', r'(\1;\2)', columns)
                    columns = columns.split(',')
                    columns = [_.replace(';', ',') for _ in columns]
            else:
                break

        # No luck try again
        if columns is None:
            fh.seek(0)
            for line in fh:
                if line.startswith('#'):
                    if ',' in line:
                        columns = line[2:].split(',')
                else:
                    break
            fh.seek(0)

        # Fallback
        if columns is None:
            columns = [f'column{i}' for i in range(len(data))]

    # Clean up and collect in dict
    columns = [column.strip() for column in columns]
    db = {}
    for key, value in zip(columns, data):
        db[key] = value
    return db

def parse_txt(path, columns=None):
    """
    Parse a simple columnar file

    This function assumes columnar data of the form: x, y, ..., f(x,
    y, ...) and returns a dict with a single (key, value), where the
    value is an (N, M) array.

    The keys of the return dictionary are parsed from a line (if present) of these form:
    # columns: <column1>, <column2>, ...
    or
    # <column1>, <column2>, ...
    """
    import numpy
    import re

    with open(path, 'r') as fh:
        # Fail with binary files. We used to stop execution here.
        try:
            fh.readline()
            fh.seek(0)
        except UnicodeDecodeError:
            # This can pass silently.
            return {}

        if columns is None:
            # Guess column names
            for line in fh:
                if line.startswith('#'):
                    match = re.match('# columns:', line)
                    if match is not None:
                        columns = line.split(':')[1]
                        columns = re.sub(r'\(([a-z]+),(\s*[a-z]+)\)', r'(\1;\2)', columns)
                        columns = columns.split(',')
                        columns = [_.replace(';', ',') for _ in columns]
                else:
                    break

            # No luck try again
            if columns is None:
                fh.seek(0)
                for line in fh:
                    if line.startswith('#'):
                        if ',' in line:
                            columns = line[2:].split(',')
                    else:
                        break

            # We cannot parse anything meaningful
            if columns is None:
                # print(f'Warning: no column names could be inferred for {fh.name}')
                return {}

        try:
            fh.seek(0)
            data = numpy.loadtxt(fh, unpack=True)
        except ValueError:
            # Fail with files formatted in other ways
            return {}

    # Clean up and return data as dict
    last_key = columns[-1].strip()
    # If the last key is of the type f(x, y, ...), return a single
    # (key, value) pair, with the unpacked data array as value.
    # Else, provide individual (key, value) pairs, one for each column
    if '(' in last_key and ')' in last_key:
        return {last_key: data}
    else:
        columns = [column.strip() for column in columns]
        return {key.strip(): value for key, value in zip(columns, data)}

# This is a bit of a convoluted way to reuse VeryTinyDB hooks to apply parsers
# Alternative: duplicate the logic for parsers in Dataset
# TODO: find a better name for flat
def parser_as_hook(parser, regexp, update='flat', update_key='{basename}.{key}'):
    """
    Decorator to turn parser into a database hook.    
    """
    @functools.wraps(parser)
    def parser_as_hook(entry):
        import re
        import fnmatch
        path = entry['_path']
        basename = os.path.basename(path)
        # TODO: fnmatch earlier
        # Always ignore hidden files (.*)
        if not basename.startswith('.') and \
           re.match(fnmatch.translate(regexp), basename):
            data = parser(path)
            # TODO: perhaps move this logic up the chain directly in DB?
            if update == 'flat':
                entry.update(data)
            elif update == 'dict':
                entry[basename] = data
            elif update == 'key':
                # Format key using update_key f-string
                for key, value in list(data.items()):
                    new_key = update_key.format(basename=basename,
                                                key=key, entry=entry)
                    data[new_key] = data.pop(key)
                entry.update(data)
            else:
                raise ValueError('unknown update scheme {update}')
        return entry
    return parser_as_hook
