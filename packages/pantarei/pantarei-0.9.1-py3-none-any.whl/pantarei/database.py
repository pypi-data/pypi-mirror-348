"""
Database
"""
import os
import tempfile
import hashlib
from itertools import compress

import numpy
from tinydb import Query as _Query
from tinydb.storages import Storage, MemoryStorage
from tinydb.table import Table

from .helpers import _wget, pprint

# Obnubilate pickle because Query objects cannot be pickled
# They are throwaway objects for us anyway
class Query(_Query):

    def __getstate__(self):
        return {}

    def __setstate__(self, value):
        pass


# Default query
query = Query()

def where(key):
    return Query()[key]


class maskablelist(list):
    """
    Data structure for heterogeneous arrays
    """

    def __init__(self, iterable, crop=False):
        super().__init__(iterable)
        self.crop = crop

    # Obnubilate pickle
    def __setstate__(self, value):
        pass

    # Obnubilate pickle
    def __getstate__(self):
        return {}

    def __getitem__(self, index):
        try:
            return super().__getitem__(index)
        except TypeError:
            return maskablelist(compress(self, index))

    def __getattr__(self, name):
        """
        Forward all unknown attribute calls to numpy array
        """
        # TODO: have axis=0 always mean the first one even if not homo
        # TODO: handle case when all shapes are eventually equal because of mask
        # TODO: in callable check value of axis, if axis=0 raise error when not homo and not cropping
        if callable(getattr(numpy.ndarray(1), name)):
            # Return a callable that applies the method on each entry of the masked list
            # along the first dimension and return the results as a list
            def _attr(*args, **kwargs):
                res = []
                for i in range(len(self)):
                    res.append(getattr(numpy.array(list(self[i])), name)(*args, **kwargs))
                return res

            # Crop each dimension to make it a numpy array
            def _attr_crop(*args, **kwargs):
                res = []
                min_shape = None
                for entry in self:
                    # print('*', entry)
                    x = numpy.array(list(entry))
                    if min_shape is None:
                        min_shape = x.shape
                    else:
                        min_shape = numpy.min([x.shape, min_shape], axis=0)
                # minsize = numpy.min([numpy.array(list(self[i]))[-1] for i in range(len(self))])
                ranges = [range(shape) for shape in min_shape]
                idx = numpy.ix_(*ranges)
                for entry in self:
                    # res.append(getattr(numpy.array(list(entry)), name)(*args, **kwargs))
                    res.append(numpy.array(list(entry))[idx])
                # return res
                # print('--', numpy.array(res).shape)
                return getattr(numpy.array(res), name)(*args, **kwargs)

            if self.crop:
                return _attr_crop
            else:
                return _attr

        else:
            return [getattr(numpy.array(entry), name) for entry in self]

    def unique(self, *args, **kwargs):
        # TODO: fix this
        return numpy.unique(self, *args, **kwargs)

    def pprint(self):
        from helpers import pprint
        # TODO: fix this


class ndarray(numpy.ndarray):

    """
    Extend `numpy.ndarray` by adding `unique()`` method
    """

    def __new__(cls, input_array):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = numpy.asarray(input_array).view(cls)
        # Finally, we must return the newly created object:
        return obj

    def unique(self, *args, **kwargs):
        """Return the unique elements of the array"""
        return numpy.unique(self, *args, **kwargs)

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self.info = getattr(obj, 'info', None)

# TODO: can we merge the two classes above?

class Data:

    """
    A container for data with a pandas-like interface
    """

    # TODO: should we call them key and values and perhaps alias key as columns() (accessor like pandas)
    # TODO: hey, if the input is a list of dicts, columns is not needed, can it be dropped from args?
    # TODO: shall we support a seq of seq + separate keys?
    # TODO: store data as _data, accessor data() or view() accepts keys as arguments and return a view on those fields
    def __init__(self, rows, columns, crop=False):
        """
        :param rows: input data as a sequence of dicts
        :param columns:
        """
        self.rows = rows
        self.columns = columns
        self.crop = crop
        self._maskable = False

    def view(self, *args):
        """Return a Data instance with a view on the given keys/fields/columns"""
        return Data([{arg: row[arg] for arg in args} for row in self.rows], args)

    def sort(self, *args, reverse=False):
        """Return a Data instance sorted according to the given keys/fields/columns"""
        entries = sorted(self.rows, key=lambda x: [x[key] for key in args], reverse=reverse)
        return Data(entries, self.columns)

    def __deepcopy__(self, memo):
        """Needed because we have cleared __getstate__"""
        from copy import deepcopy
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def copy(self):
        """Return a deep copy of `self`"""
        from copy import deepcopy
        return deepcopy(self)

    def __repr__(self):
        from .helpers import pprint
        from io import StringIO
        with StringIO() as io:
            pprint(self.rows, columns=self.columns, file=io)
            txt = io.getvalue()
        return txt

    def __len__(self):
        return len(self.rows)

    # Obnubilate pickle
    def __setstate__(self, value):
        pass

    # Obnubilate pickle
    def __getstate__(self):
        return {}

    # def __getattr__(self, name):
    #     """
    #     Forward all unknown attribute calls to numpy array
    #     """
    #     pass

    def __getitem__(self, key):
        if type(self.rows) == list:
            if isinstance(key, str):
                # We access a single row by key
                if self._maskable:
                    return maskablelist([row[key] for row in self.rows], crop=self.crop)
                try:
                    # Homogenous
                    return ndarray(numpy.array([row[key] if key in row else None for row in self.rows]))
                except ValueError:
                    # Non-homogeneous
                    return maskablelist([row[key] if key in row else None for row in self.rows], crop=self.crop)
            elif isinstance(key, int):
                # Access list index
                return self.rows[key]
            elif isinstance(key, slice):
                # Slice
                return Data(self.rows[key], self.columns)
            else:
                # This is a mask
                assert len(key) == len(self.rows), f'{key}'
                return maskablelist([row[key] for row in self.rows], crop=self.crop)
        else:
            return self.rows.__getitem__(key)


# Temporarily for compat
NanoDF = Data

# TODO: shouldnt we call this Dataset too somehow? The interface looks more similar to the one of dataset
class VeryTinyDB:
    """
    A `TinyDB`-like database with

    - a single table
    - hooks to be called at insertion
    - unique variables (aka primary keys)
    - improved columns/rows accessors

    Contrary to the `TinyDB` design, `VeryTinyDB` is not an instance of `Table`,
    but *has* a `Table` (composition, not inheritance).
    """

    default_storage_class = MemoryStorage

    def __init__(self, *args, **kwargs):
        storage = kwargs.pop('storage', self.default_storage_class)
        self.table = Table(storage(*args, **kwargs), '_default')
        """`Table` to store the database"""
        self.unique = ()
        """Unique entry"""
        self._merge_columns = set.union
        self._hooks = []
        self._new_entries = False
        self._sort_by = []

    def __repr__(self):
        from io import StringIO
        with StringIO() as io:
            self.pprint(file=io)
            txt = io.getvalue()
        return txt

    def __iter__(self):
        """
        Return an iterator for the table's documents.
        """
        # return iter(self.rows())
        entries = iter(self.table)
        sort_by = self._sort_by
        if sort_by:
            if not (isinstance(sort_by, list) or isinstance(sort_by, tuple)):
                sort_by = [sort_by]
            entries = sorted(entries, key=lambda x: [x[key] for key in sort_by])
        return iter(entries)

    def __len__(self):
        return len(self.table)

    def add_hook(self, hook, *args, **kwargs):
        """Register a new hook to be applied when accessing the entries"""
        if hook in [hook[0] for hook in self._hooks]:
            return

        self._hooks.append((hook, args, kwargs))
        # If we inserted some entries before adding the hook, we update the db
        if self._new_entries:
            # Apply this hook to entries already in database
            for entry in self:
                result = hook(entry, *args, **kwargs)
                entry.update(result)
                self.table.upsert(entry)
            self._new_entries = False

    def remove_hooks(self):
        """Remove hooks"""
        self._hooks = []

    def sort(self, key):
        """Sort data by `key`, which can be a column or a sequence of columns"""
        if isinstance(key, (list, tuple)):
            for _key in key:
                assert _key in self.columns()
        else:
            assert key in self.columns()

        self._sort_by = key

    def _apply_hooks(self, entry):
        """Apply hooks and store the values in the new entry"""
        for hook in self._hooks:
            result = hook[0](entry, *hook[1], **hook[2])
            entry.update(result)
        return entry

    # TODO: should we keep this to align with TinyDB? I think we can
    # switch to find(),it is shorter, more powerful and does not
    # expose Documents. It alings with Dataset
    def search(self, condition=None):
        """Return entries matching `condition`"""
        if condition is None:
            entries = list(iter(self))
        else:
            entries = self.table.search(condition)
        return entries

    def insert(self, entry):
        """
        Insert `entry` dict in the database

        It walys upserts against the `self.unique` variable. If all
        unique variables of the new entry match an existing one, then
        we only update the entry, because there must be a unique one.
        """
        # Always apply hooks
        self._new_entries = True
        entry = self._apply_hooks(entry)

        if len(self.unique) == 0:
            self.table.insert(entry)
        else:
            # Make sure that all required variables match
            query = Query()
            queries = []
            for var in self.unique:
                queries.append(query[var] == entry[var])
            cond = queries[0]
            for q in queries[1:]:
                cond = cond.__and__(q)
            self.table.upsert(entry, cond)

    # TODO: should we add keys() as alias of columns()
    # TODO: should columns be a property now that it has not args?
    def columns(self):
        """Return columns of database sorted in alphabetical order"""
        # TODO: more pythonic reduction?
        rows = self.table.all()
        if len(rows) == 0:
            return []
        cols = set(rows[0].keys())
        for entry in rows:
            cols = self._merge_columns(cols, set(entry.keys()))
            # cols = merge(cols, entry.dtype.names)
        return sorted(list(cols))

    def find(self, condition=None, sort_by=None, ignore=None, reverse=False):
        """
        Return rows that match `condition` as a `Data` instance,
        optionally sorted according to columns given by `sort_by`.

        :param condition: query condition
        :param sort_by: column or sequence of columns to sort the entries
        :param ignore: sequence of columns to ignore
        :param reverse: reverse sorting globally (for each entry of `sort_by`)
        """
        if condition is None:
            entries = list(iter(self.table))
        else:
            entries = self.table.search(condition)

        # Ignored columns
        if ignore is not None:
            if not (isinstance(ignore, list) or isinstance(ignore, tuple)):
                ignore = (ignore, )
        else:
            ignore = ()

        columns = self.columns()

        # Remove ignored columns and keep columns sorted
        columns = set(columns) - set(ignore)
        columns = list(sorted(columns))

        # Pop entries with missing columns
        if self._merge_columns is not set.union:
            # Find entries that miss at least one column
            partial_entries = []
            for i, row in enumerate(entries):
                for key in columns:
                    if key not in row:
                        partial_entries.append(i)
                        break
            # Now purge them
            for i in partial_entries[-1::-1]:
                entries.pop(i)

        # Sorting
        if sort_by is None and self._sort_by:
            sort_by = self._sort_by

        if sort_by is not None:
            if not isinstance(sort_by, (list, tuple)):
                sort_by = [sort_by]
            entries = sorted(entries, key=lambda x: [x[key] for key in sort_by],
                             reverse=reverse)

        return Data(entries, columns)

    def find_one(self, condition=None, ignore=None):
        """Return a single (scalar) entry matching the `condition`"""
        data = self.rows(condition=condition, ignore=ignore)
        assert len(data) == 1
        return data[0]

    def rows(self, *args, **kwargs):
        """Alias of `find`"""
        return self.find(*args, **kwargs)

    def row(self, *args, **kwargs):
        """Alias of `find_one`"""
        return self.find_one(*args, **kwargs)

    # Obnubilate pickle
    def __setstate__(self, value):
        pass

    # Obnubilate pickle
    def __getstate__(self):
        return {}

    def __getitem__(self, key):
        return self.rows()[key]

    def groupby(self, key, condition=None, reverse=False):
        """
        Return a `Data` instance with entries with common `key` grouped
        along an extra first dimension

        The results are sorted according to the `key`.

        :param key: group entries according to `key` string
        :param condition: only return entries matching query `cond`
        :param reverse: revert the order of the sorting within the group
        """
        # This iterates over groups, hence the first dimension is the number of groups
        # The second dimension is the number of entries in each group
        # Then follows the shape of the data.
        # Hence to average we do:
        #   db.groupby('x').mean(axis=1)
        # TODO: it would be more natural to have the number of entries as first dimension
        # and number of groups as second, so that we can average over axis=0

        # Sort and group (https://stackoverflow.com/questions/38013778/is-there-any-numpy-group-by-function)
        rows = self.find(sort_by=key, condition=condition)
        splits = rows[key].unique(return_index=True)[1][1:]
        groups = numpy.split(rows, splits)

        # Gather entries within group to add a first extra dimension
        # This makes it easy to average within the group in client code
        columns = self.columns()
        data_all = []
        for group in groups:
            data_dict = {}
            for column in columns:
                data_dict[column] = [_group[column] for _group in group]
            data_all.append(data_dict)

        if reverse:
            data_all = sorted(data_all, key=lambda x: x[key], reverse=True)

        data = Data(data_all, columns)
        data._maskable = True
        return data

    def pprint(self, condition=None, **kwargs):
        """Pretty print"""
        if 'ignore' not in kwargs:
            kwargs['ignore'] = ('_dirname', '_path')
        entries = self.search(condition)
        pprint(entries, **kwargs)

    # def close(self):
    #     del self

    # def __enter__(self):
    #     pass

    # def __exit__(self, a, b, c):
    #     del self


# Temporarily for compat
NanoDB = VeryTinyDB


from .parsers import parse_yaml, parse_pickle, parse_txt, parse_path, parser_as_hook

_default_parsers = [
    (parse_yaml, '*.yaml'),
    (parse_pickle, '*.pkl'),
    (parse_pickle, '*.npy'),
    (parse_txt, '*.txt'),
    (parse_txt, '*'),
    (parse_path, '*')
]
_parsers_shortcuts = {
    'yaml': parse_yaml,
    'pickle': parse_pickle,
    'txt': parse_txt,
    'path': parse_path,
}

class Dataset(VeryTinyDB):

    """
    A simple dataset built from file paths or urls

    Examples
    --------

    1) Use custom parsers::

    .. code-block:: python

       ds = Dataset(parsers=[(parse_txt, '*.txt'),
                             (parse_csv, '*.csv')])
       ds.insert('data/**')

    2) Add a custom parser to default ones::

    .. code-block:: python

       ds = Dataset(parsers=[(parse_custom_yaml, '*.txt')],
                    keep_default_parsers=True)
       ds.insert('data/**/*.txt')
    """

    def __init__(self, paths=None, db_path='', parsers=None,
                 keep_default_parsers=False, unique='dirname'):
        """
        :param paths: paths from which data are parsed, optional
        :param db_path: path to database internal file, optional

        :param parsers: list of tuples, each one containing a parser
          function and a regexp of paths to which the parser is
          applied. The parser can also be a shortcut string among:
          `yaml`, `pickle`, `txt`, `path`

        :param keep_default_parsers: if True, `parsers` are added to
          the default parsers and , otherwise they will replace the
          default parsers

        :param unique: which dataset colum to use to gather data in a
          unique dataset entry
        """
        # If a db path is provided, we use JSON storage, else we keep
        # the db in memory
        if db_path is None or len(db_path) == 0:
            from tinydb.storages import MemoryStorage
            super().__init__(storage=MemoryStorage)
        else:
            # Actually, the default
            from tinydb.storages import JSONStorage
            super().__init__(db_path, storage=JSONStorage)

        # Parsers as a dict of (suffix, function) pairs
        if parsers is not None:
            if keep_default_parsers:
                # User-provided parsers have precedence
                self.parsers = parsers
                self.parsers += _default_parsers
            else:
                # Ignore default ones
                self.parsers = parsers
        else:
            self.parsers = _default_parsers

        # Insert parsers
        # What if multiple parsers match the same regexp? I think this is fine.
        # We may want to analyze the same file in different ways. The only edge case is
        # a fallback that should only be executed if the others did not match
        for entry in self.parsers:
            if len(entry) == 2:
                parser, pattern = entry
                args = ()
            else:
                parser, pattern, args = entry
            if parser in _parsers_shortcuts:
                parser = _parsers_shortcuts[parser]
            # TODO: consider a simpler design, without transforming parsers into hooks
            # and apply them directly upon insertion.
            self.add_hook(parser_as_hook(parser, pattern))

        # Make data entries unique, typically by dirname or path or md5_hash
        self.unique = ['_' + unique]

        # Add paths right away, if provided
        if paths is not None:
            self.insert(paths)

    # TODO: deprecate this, keep only one way of doing it
    def _add_parser(self, parser, regexp, update='flat'):
        """Add a parser for files matching regexp"""
        # TODO: document and perhaps rename update
        # TODO: add removing parser, which should clear the hook
        if parser in _parsers_shortcuts:
            parser = _parsers_shortcuts[parser]
        self.parsers.append((parser, regexp))
        self.add_hook(parser_as_hook(self.parsers[-1][0], self.parsers[-1][1], update))

    def _insert(self, input_path, copy=False):
        """
        Insert a new `input_path` in the database. If `copy` is True, the
        file is copied in the database storage.
        """
        # Allow directory
        if os.path.isdir(input_path):
            import glob
            for _path in glob.glob(input_path + '/*'):
                # Recursive call to insert all files in directory
                # This will go into sudirectories...
                self._insert(_path, copy)
                return

        # Set paths
        if input_path.startswith('http'):
            tmpdir = tempfile.mkdtemp()
            basename = os.path.basename(input_path)
            _wget(input_path, tmpdir)
            local_path = os.path.join(tmpdir, basename)
        else:
            local_path = input_path

        # Create the new entry, adding the required unique keys
        # as private (underscored) to avoid possible clashes with
        # variables parsed by parsers
        entry = {}
        entry['_path'] = input_path
        entry['_dirname'] = os.path.dirname(input_path)
        if '_md5_hash' in self.unique:
            with open(local_path, "rb") as fh:
                data = fh.read()
            entry['_md5_hash'] = hashlib.md5(data).hexdigest()

        # Add the entry to the database
        super().insert(entry)

        # TODO: remove _path if it is not in unique
        # if '_path' not in self.unique:
        #     self.remove('_path')

    def insert(self, path, copy=False):
        """
        Insert the file in `path` or all the files matching the `path`
        globbable expression.
        """
        # TODO: perhaps add stright a parser/fmt argument here
        from glob import glob
        if os.path.exists(path):
            self._insert(path, copy)
        else:
            paths = glob(path, recursive=True)
            for _path in paths:
                self._insert(_path, copy)

    def _missing(self):
        """Check that the paths of all the entries exist"""
        # TODO: handle http links (check if accessible)
        # TODO: this does not work
        # query = Query()
        # return self.search(~ (query._path.test(os.path.exists)))
        docs = []
        for entry in self:
            if not os.path.exists(entry['_path']):
                docs.append(entry)
        return docs


# Temporarily for compat
Database = Dataset
