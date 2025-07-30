"""
Scheduler
"""
import os
import sys
import time
import subprocess
import concurrent.futures

from .backends import detect
from .helpers import mkdir, serialize_kwargs, rmd
from . import core

# Factory method
def Scheduler(host='localhost', verbose=False, backend='auto', jobs_limit=0):
    """
    Factory to select an appropriate scheduler

    :param host: hostname of the cluster
    :param verbose: verbose output
    :param backend: backend for scheduler (default is auto-detect)
    :param jobs_limit: maximum number of jobs to run concurrently (if 0 no limit)
    """
    if backend in ['thread', 'process']:
        # We request explicitly a thread scheduler
        return ThreadScheduler(max_workers=jobs_limit if jobs_limit > 0 else None,
                               backend=backend)

    # Now we look for a job scheduler
    found_backend = detect(backend)
    if backend not in [None, 'auto'] and found_backend is None:
        raise ValueError(f'cannot find requested scheduler {backend}')

    if found_backend:
        return JobScheduler(host=host, verbose=verbose, backend=found_backend,
                            jobs_limit=jobs_limit)
    # Fallback to thread scheduler with its default backend
    return ThreadScheduler(max_workers=jobs_limit if jobs_limit > 0 else None)


class BareJobScheduler:

    """
    Wrapper to scheduler for execution on a distributed memory environment

    `Scheduler` is entirely decoupled from `Job`. For job submission,
    it only needs a script as a string and the relevant job
    directives.
    """

    # TODO: add custom header or args to __init__ so that we can customize the job at run time

    def __init__(self, host='localhost', verbose=False, backend='auto', jobs_limit=0):
        """
        :param host: hostname of the cluster
        :param verbose: verbose output
        :param backend: backend for scheduler (default is auto-detect)
        :param jobs_limit: maximum number of jobs to run concurrently (if 0 no limit)
        """
        self.host = host
        self.verbose = verbose
        self.path = ''  # working directory?
        self.backend = detect(backend)
        self.jobs_limit = jobs_limit

    def wait(self, job_name=None, max_jobs=None, seconds=5):
        """
        Wait until `job_name` is done or until there are less than `max_jobs`

        The check is done every `seconds` seconds.
        """
        assert not (job_name and max_jobs), 'set only one of these parameters'
        muted = False
        while True:
            reason_to_wait = ''
            if job_name is None:
                if len(self.queue()) > 0 and max_jobs is None:
                    reason_to_wait = 'Waiting for all jobs to end...'
            else:
                # Make sure job_name is a list
                if isinstance(job_name, str):
                    job_name = [job_name]
                if any([self.queued(name) for name in job_name]):
                    n = sum([self.queued(name) for name in job_name])
                    reason_to_wait = f'Waiting for {n} dependent jobs to end...'

            if max_jobs is not None:
                if len(self.queue()) >= max_jobs:
                    n = len(self.queue()) - max_jobs + 1
                    reason_to_wait = f'Waiting for {n} jobs to end...'

            if reason_to_wait:
                if self.verbose and not muted:
                    print(reason_to_wait)
                    muted = True
                if not core.halt:
                    if self.verbose:
                        print('...we exit immediately')
                    sys.exit()
                else:
                    time.sleep(seconds)
            else:
                break

    def queue(self):
        """Return a list of jobs in the scheduler queue"""
        output = subprocess.check_output(self.backend['queue'], shell=True)
        queued_jobs = output.decode().split('\n')[:-1]
        return queued_jobs

    # TODO: this seems redundant, job checks against the fqn so we should test if fqn in queue()
    # This is currently used in Job and in Thread
    def queued(self, job_name):
        """Return `True` the job named `job_name` is queued.

        :param job_name: fqn or a regexp matching a fully qualified name
        """
        import re
        # Check if job_name is fully qualified
        # if re.match('.*-.*', job):
        for queued_job in self.queue():
            # We clear the match afterwards because it cannot be pickled by dill
            match = re.match(job_name, queued_job)
            if match:
                del match
                return True
        return False

    # TODO: perhaps better collect cores, wall, mem as resources right away
    # instead of relying on locals?
    def submit_job(self, script, job_name, job_output=None, job_error=None, cores=1,
                   wall_time=None, memory=None):
        """
        Submit a script for batch execution on the scheduler

        :param script: string of python commands to execute
        :param job_name: name of job
        :param job_output: job output file
        :param job_error: job error file
        :param cores: number of cores for the job
        :param wall_time: wall time limit for the job ([D-]HH:MM:SS)
        :param memory: requested RAM (ex. 5000M or 5G)
        """
        name, output, error = job_name, job_output, job_error
        params = locals()
        # command = 'python -u -'
        # header = ''
        # TODO: not the best place probably
        if self.backend['limit'] and self.jobs_limit == 0:
            ncores = subprocess.check_output(['grep', '-c', '^processor', '/proc/cpuinfo'])
            self.wait(max_jobs=int(ncores))

        if self.jobs_limit > 0:
            self.wait(max_jobs=self.jobs_limit)

        # Assemble script spefications according to backend
        directive = self.backend["directive"]
        args = []
        for name, flag in self.backend['specifications'].items():
            if name not in params:
                continue
            value = params[name]
            if value is not None:
                args.append(f'{directive} {flag} {value}')

        # TODO: strip spaces when preceeded by = (like '-l nodes= 1' should be '-l nodes=1')

        # Define prologue and epilogue
        prologue = ''
        epilogue = ''

        # The backend uses batch jobs
        header = '\n'.join(args)
        # Interpolate script with job header
        if script.startswith('#!'):
            lines = script.split('\n')
            shebang = lines.pop(0)
            body = '\n'.join(lines)
        else:
            body = script
            shebang = '#!/usr/bin/env python'

        # Submit the job
        # TODO: are the env vars propagated here?
        output = subprocess.check_output(f"""{self.backend['submit']} <<'EOF'
{shebang}
{header}
{prologue}
{body}
{epilogue}
EOF""", shell=True)
        if self.verbose:
            print(output.decode().strip())


# Class adapter implementing a TaskScheduler interface
class JobScheduler(BareJobScheduler):

    def submit(self, task, kwargs, wall_time=None, memory=None, cores=1):
        import inspect
        import dill

        name = task.qualified_name(**kwargs)
        path = os.path.join(task.cache.path, name)

        mkdir(path)
        session_pkl = os.path.join(path, '.session.pkl')
        context_pkl = os.path.join(path, '.context.pkl')
        job_state = os.path.join(path, 'job.yaml')
        job_output = os.path.join(path, 'job.out')
        kwargs = serialize_kwargs(kwargs)

        stacks = inspect.stack()
        for n in range(len(stacks)-1, -1, -1):
            if 'job' in stacks[n].frame.f_locals:
                s = stacks[n]
                break

        # Store session and local context separately.
        # The session stores all objects in the module of the frame
        # containing the job instance
        probls_objs = ['__pyfile', '_ih', '_oh', '_dh', 'In', 'Out',
                       'get_ipython', 'exit', 'quit',
                       '__session__', '_i', '_ii', '_iii', '_i1']

        probls = {}
        for f in probls_objs:
            if f in s.frame.f_globals:
                probls[f] = s.frame.f_globals.pop(f)

        dill.dump_module(session_pkl, module=inspect.getmodule(s.frame.f_code),
                         refimported=True)
        # Check if it works, otherwise it makes no sense to submit
        _ = dill.load_module_asdict(session_pkl)

        # The context session stores the job instance itself
        # to cover the case in which this is defined in a function
        from types import ModuleType
        context = ModuleType('context')
        context.job = s.frame.f_locals['job']
        # TODO: query cannot be pickled in context? How come, we only have job here...

        # Here we get warnings sometimes:
        # dill.py:1087: PicklingWarning: Cannot pickle __main__.f has
        # recursive self-references that trigger a RecursionError.
        # However, the dumped context works well, so it is not clear
        # that this is really an issue. The origin of the warning is unclear:
        # there are no self-references in the function.
        # For the time being, we silence these warnings.
        # One day we will perhaps understand what is going on.
        # import dill.detect
        # with dill.detect.trace():
        #     dill.dump_module(context_pkl, module=context, refimported=True)
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=dill.PicklingWarning)
            dill.dump_module(context_pkl, module=context, refimported=True)

        # Check if it works, otherwise it makes no sense to submit
        # _ = dill.load_module_asdict(context_pkl)

        # Finally restore problematic objects in the original frame
        for key in probls:
            s.frame.f_globals[key] = probls[key]

        # https://stackoverflow.com/questions/1253528/is-there-an-easy-way-to-pickle-a-python-function-or-otherwise-serialize-its-cod
        # TODO: process the calling line to get the job object instead of hardcoding job
        script = f"""\
#!/usr/bin/env -S python -u
__name__ = '__main__'
import sys
import os
import time
import signal
import dill
sys.path.append('.')

run = True

def handler_stop_signals(signum, frame):
    global run
    run = False
    raise RuntimeError('received SIGINT/SIGTERM')

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

while True:
    if os.path.exists('{job_state}'): break

hostname = 'unknown'
if 'HOSTNAME' in os.environ:
    hostname = os.environ['HOSTNAME']

# We must unset the env variables else we get a report at the end
if 'pantarei' in os.environ:
    del os.environ['pantarei']
if 'pantarei_report' in os.environ:
    del os.environ['pantarei_report']
# print('mode', 'pantarei' in os.environ)
# print('report', 'pantarei_report' in os.environ)

fh = open('{job_state}', 'a')
print('job_node:', hostname, file=fh, flush=True)
print('job_start:', time.time(), file=fh, flush=True)

try:
    dill.load_module('{session_pkl}')
    context = dill.load_module('{context_pkl}')
    context.job.task({kwargs})
except:
    print('job_fail:', time.time(), file=fh, flush=True)
    raise
else:
    print('job_end:', time.time(), file=fh, flush=True)
finally:
    fh.close()
    # Remove session data when job is over
    os.remove('{session_pkl}')
    os.remove('{context_pkl}')
"""

        # Submit the job script now
        self.submit_job(script, name, job_output=job_output,
                        job_error=None, wall_time=wall_time,
                        memory=memory)

        # Job is queued
        with open(f'{job_state}', 'w') as fh:
            print('job_queue:', time.time(), file=fh, flush=True)


class BareThreadScheduler:

    def __init__(self, max_workers=None, backend='thread'):
        """
        - The `thread` backend has performance issues with extensions, ex. f2py.
        - The `process` backend can have issue with pickling, ex. local functions
        """
        self.max_workers = max_workers
        assert backend in ['thread', 'process'], 'wrong {backend} (not thread/process)'
        if backend == 'thread':
            self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)
        if backend == 'process':
            self.pool = concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers)
        self._futures = []

    def queue(self):
        return [future.name for future in self._futures if not future.done()]
        # self.results = [future.result() for future in futures if not future.done()]

    # TODO: refactor same as JobScheduler -> standalone
    def queued(self, job_name):
        """Return `True` the job named `job_name` is queued.

        :param job_name: fqn or a regexp matching a fully qualified name
        """
        import re
        # Check if job_name is fully qualified
        # if re.match('.*-.*', job):
        for queued_job in self.queue():
            # We clear the match afterwards because it cannot be pickled by dill
            match = re.match(job_name, queued_job)
            if match:
                del match
                return True
        return False

    def submit_thread(self, task, name, *args, **kwargs):
        if len(self.queue()) == 0:
            cls = self.pool.__class__
            self.pool.shutdown()
            self.pool = cls(max_workers=self.max_workers)

        f = self.pool.submit(task, *args, **kwargs)
        f.name = name
        self._futures.append(f)
        return f

    def wait(self, job_name=None, max_jobs=None, seconds=0):
        assert job_name is None
        assert max_jobs is None
        concurrent.futures.wait(self._futures)


# Class adapter implementing a TaskScheduler interface
class ThreadScheduler(BareThreadScheduler):

    def submit(self, task, kwargs, wall_time=None, memory=None, cores=1):
        name = task.qualified_name(**kwargs)
        path = os.path.join(task.cache.path, name)
        mkdir(path)
        job_state = os.path.join(path, 'job.yaml')

        # Here we used to wrap the task with a local function to write the job
        # state in the cache, but it could not be pickled by the 'process'
        # backend. This was needed because of a problematic implementation of
        # callbacks, which now appeared solved.
        # Ref: https://runebook.dev/en/articles/python/library/concurrent.futures/concurrent.futures.Future.add_done_callback

        # Task starts
        with open(f'{job_state}', 'w') as fh:
            print('job_start:', time.time(), file=fh, flush=True)
        future = self.submit_thread(task, name, **kwargs)

        # Task is queued
        with open(f'{job_state}', 'a') as fh:
            print('job_queue:', time.time(), file=fh, flush=True)

        # Add callback to log when it is over
        def _over(f):
            try:
                result = future.result()
            except:
                with open(f'{job_state}', 'a') as fh:
                    print('job_fail:', time.time(), file=fh, flush=True)
                raise
            else:
                with open(f'{job_state}', 'a') as fh:
                    print('job_end:', time.time(), file=fh, flush=True)
        future.add_done_callback(_over)

        return future
