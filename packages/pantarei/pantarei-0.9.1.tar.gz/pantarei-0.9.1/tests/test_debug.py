import unittest
import os

from pantarei import *

class Test(unittest.TestCase):

    def setUp(self):
        import pantarei.core
        pantarei.core.cache = Cache('/tmp/data')

#     def test_itemize(self):
#         import numpy
#         from pantarei.cache import _itemize
#         a = numpy.array([numpy.array(1.0)])
#         #print(type(a[0]), type(_itemize(a)[0]))
#         self.assertTrue(isinstance(_itemize(a), list))
#         self.assertTrue(isinstance(_itemize(a)[0], float))        
#         b = {'a': a}
#         self.assertTrue(isinstance(_itemize(b)['a'], list))
#         self.assertTrue(isinstance(_itemize(b)['a'][0], float))
#         a = numpy.array([numpy.array(1)])
#         self.assertTrue(isinstance(_itemize(a)[0], int))
#         b = {'a': a}
#         self.assertTrue(isinstance(_itemize(b)['a'][0], int))
#         import yaml

#         a = numpy.array([1.0])[0]
#         self.assertTrue(isinstance(_itemize(a), float))        
#         # print(type(a))
#         # print(yaml.dump(_itemize({'a': [1,2,3]})))
        
#     def test_task_cache(self):
#         import time
#         def f(x):
#             time.sleep(1)
#             return x
#         cache = Cache('/tmp/data')
#         task = Task(f, cache=cache)
#         data = task(x=1)
#         self.assertEqual(data, 1)
#         self.assertTrue(task.done(x=1))
#         ti = time.time()
#         task(x=1)
#         tf = time.time()
#         self.assertLess(tf-ti, 0.9)
#         task.clear(x=1)
#         self.assertFalse(task.done(x=1))
#         ti = time.time()
#         task(x=1)
#         tf = time.time()
#         self.assertGreater(tf-ti, 0.9)

#         # Check with arrays
#         # We should have a look at the .*.yaml files
#         import numpy
#         data = task(x=numpy.ndarray([1]))
#         data = task(x=numpy.ndarray([1]))
        
#     def test_task_ignore(self):
#         import time
#         def f(x, debug):
#             return x
#         cache = Cache('/tmp/data')
#         task = Task(f, cache=cache, ignore=['debug'])
#         task(x=1, debug=False)
#         self.assertTrue(task.done(x=1, debug=True))
#         self.assertTrue(task.done(x=1, debug=False))

#     def test_task_default_args(self):
#         import time
#         def f(x):
#             return x
#         cache = Cache('/tmp/data')
#         task = Task(f, cache=cache)
#         qn1 = task.qualified_name(x=1)
#         # Now add an optional argument
#         def f(x, y=0):
#             return x
#         # The qualified name must be the same
#         qn2 = task.qualified_name(x=1)
#         self.assertEqual(qn1, qn2)

#     def test_precision(self):
#         """
#         If relative difference between input floats is less than 1e-12
#         then two tasks have the same qualified name (same hash). Also
#         check that 0-sized arrays and floats are indistinguishable.
#         """
#         import time
#         import numpy
#         def f(x):
#             return x
#         cache = Cache('/tmp/data')
#         task = Task(f, cache=cache)
#         qn1 = task.qualified_name(x=numpy.pi)
#         qn2 = task.qualified_name(x=numpy.pi + 1e-14)
#         self.assertEqual(qn1, qn2)
#         qn3 = task.qualified_name(x=numpy.pi + 1e-10)
#         self.assertNotEqual(qn1, qn3)
#         qn1 = task.qualified_name(x=numpy.array(numpy.pi))
#         qn2 = task.qualified_name(x=numpy.pi)
#         self.assertEqual(qn1, qn2)
        
#     def test_task_clear_first(self):
#         import time
#         def f(x):
#             return x
#         cache = Cache('/tmp/data')
#         task = Task(f, cache=cache, clear_first=True)
#         task(x=2)

#         # We now change the function output.
#         # The cache will be used, unless we force execution
#         # by first clearing the cache
#         def f(x):
#             return x**2
#         task = Task(f, cache=cache, clear_first=True)
#         self.assertFalse(task.done(x=2))
#         self.assertEqual(task(x=2), 4)

#     def test_task_artifacts_results(self):
#         import time
#         from pantarei.helpers import mkdir
#         def f(x):
#             output = '/tmp/artifacts_bis'
#             mkdir(output)
#             return {'y': x, 'artifacts': output}
#         cache = Cache('/tmp/data')
#         task = Task(f, cache=cache)
#         task(x=1)
#         self.assertTrue(os.path.exists('/tmp/artifacts_bis'))
#         self.assertTrue(os.path.exists(cache._storage(task.qualified_name(x=1))))
#         task.clear(x=1)
#         self.assertFalse(os.path.exists('/tmp/artifacts_bis'))
#         self.assertFalse(os.path.exists(cache._storage(task.qualified_name(x=1))))

#     def test_task_artifacts(self):
#         import time
#         from pantarei.helpers import mkdir
#         def f(x, output='/tmp/artifacts', artifacts='/tmp/artifacts'):
#             mkdir(output)
#             return x
#         cache = Cache('/tmp/data')
#         task = Task(f, cache=cache)
#         task(x=1)
#         self.assertTrue(os.path.exists(cache._storage(task.qualified_name(x=1))))
#         self.assertTrue(os.path.exists('/tmp/artifacts'))
#         task.clear(x=1)
#         self.assertFalse(os.path.exists('/tmp/artifacts'))
#         self.assertFalse(os.path.exists(cache._storage(task.qualified_name(x=1))))

#     #@unittest.skip('Job not working from unittest')
#     def test_job(self):
#         import pantarei.job
#         from pantarei import Task, Job, Scheduler, Cache
#         #pantarei.job._stack_index = 2 #-1
#         def f(x):
#             import time
#             time.sleep(1)
#             return x
#         task = Task(f, cache=Cache('/tmp/data'))
#         job = Job(task, scheduler=Scheduler(backend='nohupx', verbose=False))
#         job(x=1)
#         job.scheduler.wait(seconds=1.5)        

    # TODO: this one has issues with multithread when executed with others
    # def test_job_wrap_func(self):
    #     from pantarei import Job
    #     import pantarei.cache
    #     import pantarei.core
    #     import pantarei.reports
    #     def f(x):
    #         import time
    #         time.sleep(1)
    #         return x
    #     pantarei.core.scheduler.verbose = True
    #     scheduler = Scheduler(backend='nohupx', verbose=False)
    #     if scheduler is None:
    #         self.skipTest('missing nohupx')
    #     job = Job(f, scheduler=scheduler)
    #     res = job(x=1)
    #     job.scheduler.wait(seconds=1.5)
    #     res = job(x=1)
    #     self.assertEqual(res, 1)

    #     # Reports
    #     # TODO: improve path joining
    #     import pantarei.core
    #     jobs = []
    #     from pantarei.helpers import _Job
    #     for qn in pantarei.core.jobs:
    #         job = _Job(pantarei.core.cache.path + '/' + qn)
    #         jobs.append(job)
    #     s = pantarei.reports._report_oneline(jobs)
    #     s = pantarei.reports._report_summary(jobs)
    #     s = pantarei.reports._report(jobs)
        
#     def test_job_cmd(self):
#         self.skipTest('broken on CI')
#         script = """
# from pantarei import Task, Job, Scheduler, Cache

# def f(x):
#     import time
#     time.sleep(1)
#     return x
# task = Task(f, cache=Cache('/tmp/data'))
# job = Job(task, scheduler=Scheduler(backend='nohupx', verbose=False))
# job(x=1)
# job.scheduler.wait(seconds=1.5)

# from pantarei.core import orphans, _report, _jobs
# missing = orphans()
# _report(_jobs)
# """
#         with open('test_pantarei.py', 'w') as fh:
#             fh.write(script)
#         import subprocess
#         output = subprocess.check_output(['python', 'test_pantarei.py'])
#         # print(output.decode())
#         from pantarei.helpers import rmf
#         rmf('test_pantarei.py')

#     def test_task_artifact_custom(self):
#         import os
#         def f(x, y, path='/tmp/data_y{y}.txt'):
#             with open(path.format(**locals()), 'w') as fh:
#                 fh.write(f'x={x}')
#             return x
#         def done(**kwargs):
#             # This will work as long as there is a path argument
#             path = kwargs['path'].format(**kwargs)
#             return os.path.exists(path)
#         def clear(**kwargs):
#             from pantarei.helpers import rmd
#             path = kwargs['path'].format(**kwargs)
#             rmd(path)

#         cache = Cache('/tmp/data')
#         task = Task(f, cache=cache, done=done, clear=clear)
#         task(x=1, y=0)
#         self.assertTrue(task.done(x=1, y=0))
#         task.clear(x=1, y=0)
#         self.assertFalse(task.done(x=1, y=0))

#     def test_task_tag(self):
#         def f(x, debug=0):
#             return x
#         cache = Cache('/tmp/data')
#         task = Task(f, cache=cache, tag='star')
#         defaults = {'debug': True}
#         task(x=1, **defaults)
#         self.assertTrue(task.done(x=1, debug=True))
#         import glob
#         self.assertEqual(glob.glob('/tmp/data/f-star'), ['/tmp/data/f-star'])

#     def test_browse(self):
#         from pantarei import pantarei
#         def f(x, debug):
#             return x
#         cache = Cache('/tmp/data')
#         task = Task(f, cache=cache)
#         db = pantarei.browse(path='/tmp/data')
#         self.assertTrue(repr(db) == '')

#         task(x=1, debug=False)
#         db = pantarei.browse(path='/tmp/data')
#         self.assertTrue(len(db) == 1)
#         self.assertTrue(db['x'] == [1])
#         self.assertTrue(db['debug'] == [False])

#         # Check that order is preserved
#         task(x=0, debug=False)
#         db = pantarei.browse(path='/tmp/data')
#         self.assertTrue(list(db['x']), [1, 0])

#     # def test_syncer(self):
#     #     from pantarei.helpers import mkdir
#     #     from pantarei.syncer import rsync, Syncer

#     #     mkdir('/tmp/data')
#     #     with open('/tmp/data/hello.txt', 'w') as fh:
#     #         fh.write('hello')

#     #     with Syncer(source="/tmp/data",
#     #                 dest="tmp",
#     #                 dest_ssh="varda") as s:
#     #         s.run()        

#     def test_hash(self):
#         import pantarei.job
#         from pantarei import Task, Job, Scheduler, Cache
#         def f(x=1.0):
#             return x
#         task = Task(f, cache=Cache('/tmp/data'))
#         job = Job(task, scheduler=Scheduler(backend='nohupx', verbose=False))
#         job(x=1)
#         job.scheduler.wait()
#         self.assertEqual(job.task.qualified_name(x=1), 'f/216ec88e5485e1ae439c37d3f94cab8f')
#         self.assertEqual(job.task.qualified_name(x=1.0), 'f/3de5a949fa3c880e35165fc6820ce82e')

#     def test_queue(self):
#         import time
#         import numpy
#         from pantarei import Job, Scheduler
#         import pantarei.core

#         pantarei.core.scheduler.verbose = True
        
#         def f(x):
#             time.sleep(5)
#             return numpy.array(x)

#         cache = Cache('/tmp/data')
#         task = Task(f, cache=cache)
#         job = Job(task)
#         for x in [1.0, 2.0]:
#             job(x=x)
#         time.sleep(1)
#         scheduler = pantarei.core.scheduler        
#         self.assertEqual(len(scheduler.queue()), 2)
#         scheduler.wait()
#         for x in [1.0, 2.0]:
#             res = job(x=x)
#             self.assertEqual(res, numpy.array(x))

#     def test_job_in_function(self):
#         import time
#         from pantarei.helpers import rmd
#         def f_context_func(x):
#             return x
        
#         rmd('.pantarei/f_context_func')
#         time.sleep(.1)

#         def submit():
#             task = Task(f_context_func)  #, cache=Cache('/tmp/data'))
#             job = Job(task)
#             res = job(x=1)
#             return res

#         res = submit()
#         assert res is None
#         time.sleep(1)
#         res = submit()
#         assert res == 1
#         rmd('.pantarei/f_context_func')

#     def test_thread(self):
#         import time
#         from pantarei import Task, Job
#         from pantarei.scheduler import ThreadScheduler

#         def f(x):
#             # print('hello', x)
#             time.sleep(2)
#             return {'x': x}

#         task = f
#         task = Task(f, clear_first=True)
#         # This block works too
#         # s = ThreadScheduler()
#         # f = s.submit(task, task.qualified_name, x=1)
#         # print(s.queue())
#         # s.wait()
#         # print(f.result())

#         from pantarei.thread import Thread
#         task = Thread(task)
#         f = task(x=1)
#         task.scheduler.wait()
#         self.assertEqual(len(task.scheduler.queue()), 0)

    def test_thread(self):
        from pantarei import Task
        # from pantarei.parallel import Parallel
        from pantarei.scheduler import ThreadScheduler, JobScheduler

        def f(x):
            import time
            time.sleep(2)
            return {'x': x}
        
        task = f
        task = Task(f, clear_first=True)        
        job = Job(task, scheduler=ThreadScheduler())
        job(x=1)
        job(x=2)

        job = Job(task)
        job(x=1)
        job(x=2)

        job.scheduler.wait()
        
        # job = Parallel(task, scheduler='thread')
        # job.scheduler = ThreadScheduler()
        # job(x=1)
        # job(x=2)

        # job = Parallel(task, scheduler='job')
        # job.scheduler = JobScheduler()
        # job(x=1)
        # job(x=2)

    def tearDown(self):
        from pantarei.helpers import rmd
        import pantarei.core
        pantarei.core.scheduler.wait()
        rmd('/tmp/data')        

if __name__ == '__main__':
    unittest.main()
