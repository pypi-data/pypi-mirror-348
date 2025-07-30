"""
Scheduler backends
"""
# TODO: add object attributes to dicts?
# TODO: named tuple?

# SLURM
slurm = dict(
    command='squeue',
    submit='sbatch',
    directive='#SBATCH',
    specifications={
        # Required
        'name': '-J',
        'output': '-o',
        'error': '-e',
        # Optional
        'queue': '-q',
        'cores': '-n',
        'nodes': '-N',
        'memory': '--mem',
        'wall_time': '-t'
    },
    queue='squeue -h -u $USER -o %j',  # names of user jobs in queue
    limit=False,
)
"""SLURM scheduler"""

nohupx = dict(
    command='nohupx',
    submit='nohupx batch',
    directive='#NOHUPX',
    specifications={
        # Required
        'name': '-n',
        'output': '-o',
        'error': '-e',
    },
    queue='nohupx queue | awk "{print \$3}"',  # names of user jobs in queue
    limit=True,
)
"""nohupx scheduler"""

# TODO: add support to at / batch
_backends = {
    'slurm': slurm,
    'nohupx': nohupx
}

def detect(backend='auto'):
    """
    Detect available scheduler

    :arg str, dict backend: if `'auto'`, detect scheduler automatically
      otherwise use `backend` if available

    :raises: 
      - `AssertionError` if no available backend is found
      - `TypeError` if `backend` is not a `str` or `dict`
    """
    import subprocess

    if backend == 'auto':
        backends = _backends.values()
    elif isinstance(backend, str):
        backends = [_backends[backend]]
    elif isinstance(backend, dict):
        backends = [backend]
    else:
        raise TypeError(f'wrong type for {backend}')

    # Detect scheduler backends
    found = []
    for backend in backends:
        try:
            subprocess.check_call(f'{backend["command"]} >/dev/null 2>/dev/null', shell=True)
            found.append(backend)
        except subprocess.CalledProcessError:
            pass

    # Check how many backends we found:
    # 0: return None
    # 1: OK
    # 2: return the first one (the last one is the fallback)
    # 3+: return the first one and issue a warning
    # assert len(found) > 0, 'no available scheduler backend, install nohupx as fallback'
    if len(found) == 0:
        return None
    if len(found) > 2:
        print(f'WARNING: found multiple backends {found}.')
    found = found[0]
    return found
