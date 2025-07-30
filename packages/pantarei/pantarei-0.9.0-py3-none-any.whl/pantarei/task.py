"""
Task
"""
import os
import time
import numpy
from .helpers import arguments, actual_kwargs, all_actual_kwargs, rmd, rmf
from . import core


def _iterable(x):
    return hasattr(x, '__iter__') and not isinstance(x, str)

def _serialize_scientific(**kwargs):
    """
    Unique name of task based on predictable rounding, courtesy of
    `numpy.format_float_scientific()`.
    """
    from hashlib import md5

    # Old version
    # Sort dict keys else the fqn is not permutation invariant
    # selected_kwargs = {key: selected_kwargs[key] for key in sorted(selected_kwargs)}
    # hash_args = md5(str(selected_kwargs).encode()).hexdigest()
    params = dict(unique=True, precision=12)
    numpy.set_printoptions(formatter={'float_kind': lambda x: numpy.format_float_scientific(x, **params)})
    # serialized_args = []
    selected_kwargs = {}
    # Sort dict keys to nesure permutation invariance (not need since 3. something, but still to be sure)
    for key in sorted(kwargs):
        var = kwargs[key]
        if not _iterable(var):
            if isinstance(var, float):
                var = numpy.format_float_scientific(var, **params)
            else:
                var = repr(var)
        else:
            if hasattr(var, 'shape') and len(var.shape) == 0:
                var = numpy.format_float_scientific(var, **params)
            else:
                # Delegate all the rest to numpy.
                # It is more time-consuming, but will work systematically
                var = repr(numpy.array(var))
        selected_kwargs[key] = var
        # serialized_args.append(key + ': ' + var)
    numpy.set_printoptions()
    # serialized_args = ', '.join(serialized_args)
    serialized_args = str(selected_kwargs)
    # with numpy.printoptions(formatter={'float_kind': lambda x: numpy.format_float_scientific(x, **params)}):
    #     serialized_args = str(selected_kwargs)
    hash_args = md5(serialized_args.encode()).hexdigest()
    return hash_args, serialized_args

class Task:

    """Cached execution of function"""

    # TODO: rename arguments in next major realease
    # clear -> clear_callback, done -> done_callback
    # clear_first -> clear
    def __init__(self, func, cache=None, done=None, clear=None, ignore=None,
                 artifacts=None, tag="", clear_first=False,
                 # These are needed when the function is None
                 # TODO: why should func be None??
                 name='', qualified_name='', docstring='', signature_args=None, signature_kwargs=None):
        """
        :param func: function to be executed and/or cached
        :param cache: cache instance to use (default: use a default cache)
        :param done: optional function to tell whether task is done
        :param clear: optional function to execute to clear the task
        :param ignore:
        :param artifacts: sequence of paths of task artifacts
        :param tag: string description of the task
        :param clear_first: clear task cache and artifacts before execution
        :param name: string name of the function `func`; the default is to use `func.__name__`
        :param qualified_name: string with the fully qualified name; the default is to build it from the arguments
        """
        # We assume that done and cache receive only the kwargs of the function
        # If we assume the kwargs are the full signature, then the function is not
        # needed anymore and this simplifies the interface. Check if we may need it.
        # TODO: func should be private and not allowed to change because we inspect signature
        self.func = func
        self.cache = cache
        self._done = done
        self._clear = clear
        self.ignore = ignore
        # TODO: deprecate artifacts: it must be parametrized by the arguments and returned by the call
        # self.artifacts = artifacts
        assert artifacts is None, 'artifacts is deprecated'
        # The task name is inferred from func, unless it is None and name is provided
        if func is None:
            assert len(name) > 0, 'provide name is func is None'
            assert signature_args and signature_kwargs, 'provide args and kwargs'
            self.__name__ = name
            self._signature_args = signature_args
            self._signature_kwargs = signature_kwargs
            self.doc = docstring
        else:
            self.__name__ = func.__name__
            self.doc = func.__doc__
            self._signature_args, self._signature_kwargs = arguments(func)
        self._qualified_name = None
        if qualified_name:
            self._qualified_name = qualified_name
        self.tag = tag
        if self.cache is None:
            self.cache = core.cache
        self.clear_first = clear_first

    def __call__(self, *args, **kwargs):
        # all_kwargs = all_actual_kwargs(self.func, *args, **kwargs)
        # kwargs = actual_kwargs(self.func, *args, **kwargs)
        # name = self.qualified_name(**kwargs)
        all_kwargs = all_actual_kwargs(self._signature_args, self._signature_kwargs, args, kwargs)
        kwargs = actual_kwargs(self._signature_args, self._signature_kwargs, args, kwargs)
        name = self.qualified_name(**kwargs)

        # Clear cache before calling function if requested
        if self.clear_first and self.cache.is_setup(name):
            self.clear(*args, **kwargs)

        # Function cache
        # This is the function-tag identifier
        # TODO: it is crucial to lock the file if we keep this
        # TODO: it is crucial to only update the file, else the locks will slow down

        # identifier = '-'.join([self.name(), self.tag]).strip('-')
        # self.cache.setup_any('metadata',
        #                      identifier,
        #                      {
        #                          'function': self.__name__,
        #                          'tag': self.tag,
        #                          'docstring': self.func.__doc__,
        #                          'args': self._signature_args,
        #                          'kwargs': self._signature_kwargs,
        #                      })

        # We do not set up cache if done already
        if not self.cache.is_setup(name):
            self.cache.setup(name, **all_kwargs)

        # Store tasks qns in core._tasks
        # If this is wrapped by a Job, the job call will just have added it
        from . import core
        if len(core._tasks) == 0 or core._tasks[-1] != self.cache._storage(name):
            # We now avoid storing multiple calls to the same task
            # The overhead of this is small (tested up to ~10000 tasks)
            # Beware of regressions though...
            if self.cache._storage(name) not in core._tasks:
                core._tasks.append(self.cache._storage(name))
            
        if self.done(**kwargs):
            # Task found in cache
            results = self.cache.read(name)
        else:
            # Execute task
            # The logging is almost identical to job, the latter may be avoided?
            hostname = 'unknown'
            if 'HOSTNAME' in os.environ:
                hostname = os.environ['HOSTNAME']
            path = os.path.join(self.cache.path, name)
            # Note: task.yaml used to be opened in append mode
            fh = open(os.path.join(path, 'task.yaml'), 'w')
            print('task_node:', hostname, file=fh, flush=True)
            print('task_start:', time.time(), file=fh, flush=True)
            try:
                results = self.func(**kwargs)
                print('task_end:', time.time(), file=fh, flush=True)
            except:
                print('task_fail:', time.time(), file=fh, flush=True)
                raise
            finally:
                fh.close()
            self.cache.write(name, results)
        # # Check whether task returned an artifacts entry and if so, store it
        # try:
        #     self.artifacts = results['artifacts']
        # except:
        #     pass
        return results

    def qualified_name(self, **kwargs):
        """
        Unique name of task based on keyword arguments `kwargs`

        Serialization takes place with a custom procedure so that
        floating point arguments are rounded consistently to 12
        significant digits (could be parametrized). Also, 0-sized
        arrays and floats are indistinguishable as input arguments.
        """
        from hashlib import md5
        # TODO: this really breaks the expected interface...
        if self._qualified_name is not None:
            return self._qualified_name
        if self.ignore is None:
            selected_kwargs = kwargs
        else:
            selected_kwargs = {}
            for key in kwargs:
                if key not in self.ignore:
                    selected_kwargs[key] = kwargs[key]

        hash_args, _ = _serialize_scientific(**selected_kwargs)

        # func_name = self.func.__name__
        func_name = self.name()
        if len(self.tag) > 0:
            return f'{func_name}-{self.tag}/{hash_args}'
        else:
            return f'{func_name}/{hash_args}'

    # TODO: add tag already here?
    def name(self):
        """Name of task"""
        return self.__name__

    def clear(self, *args, **kwargs):
        """Remove task data from cache and its artifacts"""
        # Store references to artifacts. Once cleared, we wont have it
        # anymore
        artifacts = self.artifacts(*args, **kwargs)
        # all_kwargs = all_actual_kwargs(self.func, *args, **kwargs)
        # kwargs = actual_kwargs(self.func, *args, **kwargs)
        all_kwargs = all_actual_kwargs(self._signature_args, self._signature_kwargs, args, kwargs)
        kwargs = actual_kwargs(self._signature_args, self._signature_kwargs, args, kwargs)
        name = self.qualified_name(**kwargs)
        self.cache.clear(name)

        # Clear task artifacts
        if artifacts is not None:
            print('remove artifacts', artifacts)
            # Assume it is a single folder
            # artifact_path = all_kwargs[self.artifacts]
            # artifact_path = artifact_path.format(**all_kwargs)
            if os.path.exists(artifacts):
                rmf(artifacts)
                rmd(artifacts)
            else:
                for path in artifacts:
                    rmf(path)
                    rmd(path)

        # Additional clear function
        if self._clear is not None:
            self._clear(**all_kwargs)

    def done(self, *args, **kwargs):
        """
        Return True is task has been already execution with given position
        and keyword arguments
        """
        # all_kwargs = all_actual_kwargs(self.func, *args, **kwargs)
        # kwargs = actual_kwargs(self.func, *args, **kwargs)
        all_kwargs = all_actual_kwargs(self._signature_args, self._signature_kwargs, args, kwargs)
        kwargs = actual_kwargs(self._signature_args, self._signature_kwargs, args, kwargs)
        name = self.qualified_name(**kwargs)
        if self.clear_first:
            # In this case, we will always call the function again
            return False

        if self._done is None:
            return self.cache.found(name)
        else:
            return self._done(**all_kwargs) and self.cache.found(name)

    # TODO: support sequence of artifacts (also in task.clear)
    def artifacts(self, *args, **kwargs):
        """
        Job artifacts, possibly as a sequence

        Two ways to specify them:

        1. if the `task` arguments have an `artifacts` argument, this is
        returned, possibly interpolated with the arguments values
        themselves

        2. if the `task` results return a dict and the latter contains
        an artifacts key, the corresponding value is returned

        Option 2. is more flexible and handles the case of artifacts
        not known in advance. However, it will not work well when the
        job fails, because some artifacts may be ignored.
        """
        # all_kwargs = all_actual_kwargs(self.func, *args, **kwargs)
        # kwargs = actual_kwargs(self.func, *args, **kwargs)
        all_kwargs = all_actual_kwargs(self._signature_args, self._signature_kwargs, args, kwargs)
        kwargs = actual_kwargs(self._signature_args, self._signature_kwargs, args, kwargs)
        name = self.qualified_name(**kwargs)

        _artifacts = None
        if "artifacts" in all_kwargs:
            _artifacts = all_kwargs["artifacts"].format(**all_kwargs)

        if self.done(**kwargs):
            results = self.cache.read(name)
            try:
                _artifacts = results.get('artifacts')
            except:
                pass
        return _artifacts
