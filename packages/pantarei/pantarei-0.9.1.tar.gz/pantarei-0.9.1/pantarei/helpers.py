"""
Helper functions
"""

import sys
import os
import shutil
import hashlib
import inspect
from .parsers import parse_yaml, parse_pickle

def arguments(func):
    """
    Return arguments without default value (positional) and with
    default value (keyword) in function `func`
    """
    signature = inspect.signature(func)
    args = tuple(param.name
                 for param in signature.parameters.values()
                 if param.default is param.empty)
    kwargs = {param.name: param.default
              for param in signature.parameters.values()
              if param.default is not param.empty}
    return args, kwargs

def _actual_kwargs(func, *args, **kwargs):
    """Return all the arguments of a function as keyword arguments."""
    signature = inspect.signature(func)
    arg_names = tuple(param.name
                      for param in signature.parameters.values()
                      if param.default is param.empty)
    # TODO: check if we passed a keyword argument with the same value as default
    # Default keyword arguments
    # actual_args = {param.name: param.default
    #               for param in signature.parameters.values()
    #               if param.default is not param.empty}
    actual_args = {}
    actual_args.update({name: arg for name, arg in zip(arg_names, args)})
    actual_args.update(kwargs)
    return actual_args

def _all_actual_kwargs(func, *args, **kwargs):
    """Return all the arguments of a function as keyword arguments."""
    signature = inspect.signature(func)
    arg_names = tuple(param.name
                      for param in signature.parameters.values()
                      if param.default is param.empty)
    # TODO: check if we passed a keyword argument we the same value as default
    # Default keyword arguments
    actual_args = {param.name: param.default
                   for param in signature.parameters.values()
                   if param.default is not param.empty}
    # actual_args = {}
    actual_args.update({name: arg for name, arg in zip(arg_names, args)})
    actual_args.update(kwargs)
    return actual_args

def actual_kwargs(signature_args, signature_kwargs, args, kwargs):
    """Return all the arguments of a function as keyword arguments."""
    # TODO: check if we passed a keyword argument with the same value as default
    actual_args = {}
    actual_args.update({name: arg for name, arg in zip(signature_args, args)})
    actual_args.update(kwargs)
    return actual_args

def all_actual_kwargs(signature_args, signature_kwargs, args, kwargs):
    """Return all the arguments of a function as keyword arguments."""
    actual_args = signature_kwargs
    actual_args.update({name: arg for name, arg in zip(signature_args, args)})
    actual_args.update(kwargs)
    return actual_args

def mkdir(dirname):
    """
    Create a directory `dirname` or a list `dirname` of directories,
    silently ignoring existing directories.

    This is just a wrapper to `os.makedirs`. All intermediate
    subdirectories are created as needed.
    """
    import os
    if dirname is None:
        return
    if isinstance(dirname, str):
        dirs = [dirname]
    else:
        dirs = dirname

    for dd in dirs:
        try:
            os.makedirs(dd)
        except OSError:
            pass

def rmd(files):
    """Totally silent wrapper to shutil.rmtree."""
    import shutil
    try:
        shutil.rmtree(files)
    except BaseException:
        pass

def rmf(files):
    """
    Remove `files` without complaining.

    The variable `files` can be a list or tuple of paths or a single
    string parseable by glob.glob().
    """
    import glob
    try:
        # This a single pattern
        for pathname in glob.glob(files):
            try:
                os.remove(pathname)
            except OSError:
                # File does not exists or it is a folder
                pass
    except (TypeError, AttributeError):
        # This is a list
        for pathname in files:
            try:
                os.remove(pathname)
            except OSError:
                # File does not exists or it is a folder
                pass

def serialize_kwargs(kwargs):
    """Return a string from the `kwargs` dictionary"""
    args = []
    for key in kwargs:
        if isinstance(kwargs[key], str):
            args.append(f'{key}="{kwargs[key]}"')
        else:
            args.append(f'{key}={kwargs[key]}')
    return ','.join(args)

def tag_function(f, name, doc=None):
    """Tag a function with `name` suffix"""
    from types import FunctionType
    func = FunctionType(f.__code__, f.__globals__, f.__name__ + '_' + name,
                        f.__defaults__, f.__closure__)
    if doc is not None:
        # func.__doc__ = '\n'.join((func.__doc__, doc))
        func.__doc__ = doc
    return func

def pprint(rows, columns=None, ignore=(), sort_by=None, max_rows=100, file=sys.stdout, max_width=100):
    """Pretty print `rows` (a list of dicts)"""

    def _tabular(data, max_len=max_width):
        """General function to format `data` list in tabular table"""

        # Predict formatting
        col_lens = [len(entry) for entry in data[0]]
        lens = [0 for _ in range(len(data[0]))]
        for entry in data:
            for i, value in enumerate(entry):
                lens[i] = max(lens[i], len(str(value)))

        crop = [False] * len(lens)
        ave_len = max_len // len(lens)
        if sum(lens) > max_len:
            # Squeeze: try to to fit by fitting to column widths
            for i in range(len(lens)):
                if max(lens[i], col_lens[i]) > ave_len:
                    lens[i] = ave_len
                    col_lens[i] = ave_len
                    crop[i] = True

        # Store list of lines
        fmts = [f'{{:{lens[i]}.{lens[i]}s}}' for i in range(len(lens))]
        fmt = ' '.join(fmts)
        lines = []
        lines.append(fmt.format(*data[0]))
        lines.append('-'*(sum(lens) + len(lens) - 1))
        for entry in data[1:]:
            entry = [str(_) for _ in entry]
            entry = [_[:ave_len-3] + '...' if len(_) > ave_len else _ for _ in entry]
            lines.append(fmt.format(*entry))
            if 0 < max_rows < len(lines):
                lines.append(f'... {len(data) - max_rows} entries not shown')
                break

        # Limit columns
        if sum(lens) > max_len:
            for i, line in enumerate(lines):
                if i < 2:
                    fill = '     '
                else:
                    fill = ' ... '
                lines[i] = line[:max_len//2] + fill + line[sum(lens) - max_len//2:]
        return lines

    if len(rows) == 0:
        return ''

    # Format and sort the data
    row = rows[0]
    if hasattr(row, 'keys'):
        keys = row.keys()
    else:
        keys = row.dtype.names
    # TODO: fix this, with structured arrays the column order must be the prescribed one
    if columns is None:
        columns = set([e for e in keys if not e.startswith('__')])
        for entry in rows:
            new_columns = set([e for e in entry if not e.startswith('__')])
            columns = set.union(columns, new_columns)
        columns = sorted(columns)

    # Ignore some columns
    for ignored in ignore:
        if ignored in columns:
            columns.pop(columns.index(ignored))

    if sort_by is not None:
        if not (isinstance(sort_by, list) or isinstance(sort_by, tuple)):
            sort_by = [sort_by]
        rows = sorted(rows, key=lambda x: [x[_] for _ in sort_by])

    # Tabularize lines and join them
    rows = [columns] + [[str(entry.get(key)) for key in columns] for entry in rows]
    lines = _tabular(rows)
    print('\n'.join(lines), file=file)

def _wget(url, output_dir):
    """Like wget on the command line"""
    try:
        from urllib.request import urlopen  # Python 3
    except ImportError:
        from urllib2 import urlopen  # Python 2

    basename = os.path.basename(url)
    output_file = os.path.join(output_dir, basename)
    response = urlopen(url)
    length = 16*1024
    with open(output_file, 'wb') as fh:
        shutil.copyfileobj(response, fh, length)

# TODO: do not rely on entry
def copy(entry, path='/tmp/{path}', root=''):
    """Get a copy of `path` in the samples database and return the path to it"""
    import tempfile

    # Handle output path
    if path is None:
        # Output path is a temporary directory
        outdir = tempfile.mkdtemp()
        basename = os.path.basename(entry['path'])
        path = os.path.join(outdir, basename)
    else:
        # Interpolate path with entry fields
        path = path.format(**entry)
        outdir = os.path.dirname(path)

    # Now copy
    if entry['path'].startswith('http'):
        # Over the network
        _wget(entry['path'], outdir)
    else:
        # Local storage
        mkdir(os.path.dirname(path))
        if entry['path'].startswith('/'):
            # Absolute path, so ignore root variable
            shutil.copy(entry['path'], path)
        else:
            # Path is relative to root, most likely database folder
            shutil.copy(os.path.join(root, entry['path']), path)

    return path

def tipify(s):
    """
    Convert a string into the best matching type.

    Examples
    --------

    .. code-block:: python

        type(tipify("2.0")) is float
        type(tipify("2")) is int
        type(tipify("t2")) is str
        map(tipify, ["2.0", "2"])

    The only risk is if a variable is required to be float,
    but is passed without dot.
    """
    if '_' in s:
        return s
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

# def debug_stacks(stacks):
#     import dill
#     # DEBUG Try to fix...
#     # dill.settings['recurse'] = True
#     # print(s.frame.f_locals)
#     print('******')
#     for i, ss in enumerate(stacks):
#         print('-'*50)
#         print('Level:', i)
#         import pprint
#         print(ss.frame)
#         pprint.pprint(ss.frame.f_locals)
#         try:
#             dill.dump_module(f'/tmp/s{i}.pkl', module=inspect.getmodule(ss.frame.f_code), refimported=False)
#         except TypeError:
#             print('*WARNING*: cannot dill this frame!')
#         print('Source:')
#         print(dill.source.getsource(ss.frame.f_code))
#         print()
#         print('Trace:')
#         with dill.detect.trace():
#             dill.dumps(ss.frame.f_code)
#         print()


import subprocess

class _PossiblyZippedFile:

    """
    Decorator of io stream objects optimized for zipped files.

    Reading gzipped files with gzip is very slow.
    We use a simpler and faster approach, which is to unzip
    the file in a temporary directory and return that file instance.
    The temporary file is removed when closing the instance.

    Example:

    > with ZippedFile('test.gz') as fh:
    >     print(fh.read())
    """

    def __init__(self, filename, mode='r'):
        self._file_tmp = None
        base, ext = os.path.splitext(filename)

        # Optimize reading
        if mode == 'r':
            # Unzip compressed files when reading
            # This is much faster than reading the gzipped object
            import tempfile
            tmp_dir = tempfile.mkdtemp()
            self._file_tmp = os.path.join(tmp_dir, os.path.basename(base))
            if ext in ['.gz', '.bz2']:
                cmd = 'gunzip'
                if ext == '.bz2':
                    cmd = 'bunzip2'
                subprocess.check_call(f'{cmd} -c {filename} > {self._file_tmp}', shell=True)
                self._file = open(self._file_tmp, mode)
            else:
                self._file = open(filename, mode)
        else:
            # Use gzip and bz2 modules for writing
            if ext == '.gz':
                import gzip
                self._file = gzip.open(filename, mode + 't')
            elif ext == '.bz2':
                import bz2
                self._file = bz2.BZ2File(filename, mode)
            else:
                self._file = open(filename, mode)

    def __getattr__(self, name):
        """
        Forward all unknown attribute calls to file stream
        """
        return getattr(self._file, name)

    def __enter__(self):
        return self

    # TODO: is this trapped when there is an exception?
    def __exit__(self, type, value, traceback):
        self._file.close()

    def close(self):
        self._file.close()
        if self._file_tmp:
            rmd(os.path.dirname(self._file_tmp))

# Internal helper functions to create read-only Job instances

def _state(path):
    job_file = os.path.join(path, 'job.yaml')
    task_file = os.path.join(path, 'task.yaml')
    state = ''
    if not os.path.exists(job_file):
        if os.path.exists(task_file):
            db = parse_yaml(task_file)
            if 'task_fail' in db:
                state = 'failed'
            elif 'task_end' in db:
                state = 'ended'
            elif 'task_start' in db:
                state = 'running'
            elif len(db) == 0:
                state = 'unknown'
    else:
        db = parse_yaml(job_file)
        if 'job_fail' in db:
            state = 'failed'
        elif 'job_end' in db:
            state = 'ended'
        elif 'job_start' in db:
            state = 'running'
        elif 'job_queue' in db:
            state = 'queued'
        elif len(db) == 0:
            state = 'unknown'
        else:
            raise ValueError(f'wrong state {list(db.keys())} in {path}')
    return state

def _kind(path):
    job_file = os.path.join(path, 'job.yaml')
    task_file = os.path.join(path, 'task.yaml')
    if os.path.exists(job_file):
        return 'job'
    if os.path.exists(task_file):
        return 'task'
    return 'unknown'

def _duration(path):
    # TODO: refactor, code is duplicated in Job
    """Current duration of job. If job is ended, return the elapsed duration"""
    import time
    import datetime

    db = {}
    task_file = os.path.join(path, 'task.yaml')
    if not os.path.exists(task_file):
        return datetime.timedelta(seconds=0)
    db.update(parse_yaml(task_file))

    job_file = os.path.join(path, 'job.yaml')
    if os.path.exists(job_file):
        db.update(parse_yaml(job_file))

    if 'task_start' in db and 'task_end' in db:
        delta = float(db['task_end']) - float(db['task_start'])
    elif 'job_start' in db and 'job_fail' in db:
        delta = float(db['job_fail']) - float(db['job_start'])
    elif 'task_start' in db:
        delta = time.time() - float(db['task_start'])
    else:
        delta = 0
    return datetime.timedelta(seconds=int(delta))

def _split_names(path):
    root, base = os.path.split(path.rstrip('/'))
    root, func_tag = os.path.split(root.rstrip('/'))
    qn = func_tag + '/' + base
    func_tag = func_tag.split('-')
    if len(func_tag) == 1:
        func, tag = func_tag[0], ''
    else:
        func = func_tag[0]
        tag = '-'.join(func_tag[1:])
    return func, tag, qn

def _arguments(path):
    job_file = os.path.join(path, 'arguments.pkl')
    if os.path.exists(job_file):
        return parse_pickle(job_file)
    return {}

def _artifacts(path):
    if os.path.exists(os.path.join(path, 'arguments.pkl')):
        args = parse_pickle(os.path.join(path, 'arguments.pkl'))
        if "artifacts" in args:
            return args["artifacts"].format(**args)
    if os.path.exists(os.path.join(path, 'results.pkl')):
        results = parse_pickle(os.path.join(path, 'results.pkl'))
        if isinstance(results, dict) and 'artifacts' in results:
            return results['artifacts']
    return ''


class _Job:

    """Private class to recreate readonly job instances"""

    def __init__(self, path):
        self.path = path
        self._setup(path)

    def _setup(self, path):
        from .reports import logos

        self.state = _state(path)
        self.duration = _duration(path)
        self.name, self.tag, self.qualified_name = _split_names(path)
        self.artifacts = _artifacts(path)
        self.logo = logos[self.state]
        self.kind = _kind(path)
        if self.state == '':
            self.kwargs = []
            self.pretty_name = f'{self.name}(...?...)'
        else:
            self.kwargs = _arguments(path)
            args = []
            for key in self.kwargs:
                # if self.task.ignore is not None:
                #     if key in self.task.ignore:
                #         continue
                if isinstance(self.kwargs[key], str):
                    args.append(f'{key}="{self.kwargs[key]}"')
                else:
                    args.append(f'{key}={self.kwargs[key]}')
            kwargs = ','.join(args)
            self.pretty_name = f'{self.name}({kwargs})'

        # if os.path.join(os.path.dirname(path), 'metadata.pkl'):
        #     func_md = parse_pickle(os.path.join(os.path.dirname(path), 'metadata.pkl'))
        # self.docstring = func_md['docstring']
        # self.signature_args = func_md['args']
        # self.signature_kwargs = func_md['kwargs']

    def clear(self):
        print('rm', os.path.join('.pantarei', self.qualified_name))
        print('rm', self.artifacts)
