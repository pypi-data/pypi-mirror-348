"""
Core functions and global variables
"""
import os
import glob
import atexit


# Possible execution modes: safe, brave, dry
mode = 'safe'
if 'pantarei' in os.environ:
    mode = os.environ['pantarei']
assert mode in ['safe', 'brave', 'dry']

# Halt mode
halt = True
if 'pantarei_nohalt' in os.environ:
    halt = False

# Default scheduler is autodetected on localhost
from .scheduler import Scheduler, ThreadScheduler, JobScheduler
scheduler = Scheduler(backend='auto')
if 'pantarei_jobs_limit' in os.environ:
    scheduler.jobs_limit = int(os.environ['pantarei_jobs_limit'])
if 'pantarei_verbose' in os.environ:
    scheduler.verbose = True
    
# Default cache
from .cache import Cache
cache = Cache('.pantarei')

# Fully qualified names of jobs run in the current session are stored in
# pantarei.jobs list. It is meant to be a public variable, which can be reset
# at will.
jobs = []
_tasks = []

def browse(name='', qualified_names=(), tag='', path='.pantarei'):
    """Convenience function that returns a `Dataset` of tasks' metadata

    If `qualified_names` is given, then we browse
    only the tasks corresponding to that list (or tuple) of fully
    qualified names (as returned by `~pantarei.task.Task.qualified_name()`).

    :param name: name of function to browse
    :param qualified_names: list of qualified names of cached results to browse
    :param tag: tag of task
    :param path: path of pantarei cache
    """
    from .database import Dataset
    from .parsers import parse_yaml, parse_pickle
    ds = Dataset(parsers=[(parse_yaml, '*.yaml'),
                          (parse_pickle, '*.pkl')], keep_default_parsers=False)

    if len(qualified_names) > 0:
        # We provide a specific list of tasks
        assert len(name) == 0 and len(tag) == 0

        for fqn in qualified_names:
            ds.insert(f'{path}/{fqn}/arguments.pkl')
            ds.insert(f'{path}/{fqn}/job.yaml')
            try:
                ds.insert(f'{path}/{fqn}/results.pkl')
            except TypeError:
                pass
    else:
        # Browse the full dataset
        if len(name) == 0:
            name = '*'
        if len(name) > 0 and len(tag) > 0:
            name = f'{name}-{tag}'

        # Sort paths by task start
        # TODO: but certainly safer than modification, but likely slower. How much?
        def _sorted_task(paths):
            times = []
            _paths = glob.glob(paths)
            for _path in _paths:
                t = parse_yaml(os.path.join(_path, 'task.yaml'))['task_start']
                times.append(t)
            return [y[0] for y in sorted(zip(_paths, times), key=lambda x: x[1])]

        # This first insertion of the arguments defines the order of
        # the dataset entries (according to task start)
        for _path in _sorted_task(f'{path}/{name}/*/'):
            ds.insert(os.path.join(_path, 'arguments.pkl'))
        # Insertion of job metadata and results will go into the unique
        # entry defined by the dirname of the path
        # TODO: shall we include task metadata, postprocessed to just include duration?
        # TODO: add flags to include/exclde/postprocess metadata
        ds.insert(f'{path}/{name}/*/job.yaml')
        try:
            ds.insert(f'{path}/{name}/*/results.pkl')
        except TypeError:
            print(f'WARNING: could not insert results of {path}/{name}/*/results.pkl (most likely not a dict)')

    return ds

class block:

    """Wait until all submitted jobs have finished via scheduler wait method"""
    
    def __enter__(self):
        global jobs
        jobs = []

    def __exit__(self, exc_type, exc_value, exc_tb):
        global jobs
        from .scheduler import Scheduler
        Scheduler().wait(jobs)


# Log at the end of scripts
# We should not do this during unit tests
# The jobs will be there but the cache may be gone
# This will give a spurious final line
# TODO: register these hooks somewhere else, this must not be done globally!
from .reports import __report
atexit.register(__report)
