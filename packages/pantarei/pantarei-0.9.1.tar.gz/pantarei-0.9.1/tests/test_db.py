import unittest
import os
import numpy
from pantarei import *
from pantarei.helpers import mkdir, rmd
from pantarei.database import Query, VeryTinyDB, where

query = Query()

class Test(unittest.TestCase):

    def setUp(self):
        import yaml, pickle
        for rho in [1.0]:
            for n in range(2):
                outdir = f"/tmp/dataset/rho{rho}/n{n}"
                mkdir(outdir)
                data = {'N': 10*n*rho}
                with open(os.path.join(outdir, 'data.yaml'), 'w') as fh:
                    yaml.dump(data, fh)
                data = {'M': 10*n*rho}
                with open(os.path.join(outdir, 'data.pkl'), 'wb') as fh:
                    pickle.dump(data, fh)
                data = {'S': 10*n*rho}
                with open(os.path.join(outdir, 'data.s'), 'wb') as fh:
                    pickle.dump(data, fh)
                # File without explicit column info
                with open(os.path.join(outdir, 'data.bla'), 'w') as fh:
                    fh.write('x y\n')
                    fh.write('1 2\n')
                    fh.write('2 3\n')
                x = [1, 2, 3]
                y = [10, 20, 30]
                with open(os.path.join(outdir, 'data.1'), 'w') as fh:
                    numpy.savetxt(fh, list(zip(x, y)), header='columns: x, y')
                with open(os.path.join(outdir, 'data.2'), 'w') as fh:
                    numpy.savetxt(fh, list(zip(x, y)), header='z, w')

    def _check_ds(self, ds):
        self.assertTrue(all(ds['rho'] == [1, 1]))
        self.assertTrue(all(ds['n'] == [0, 1]))
        self.assertTrue(all(ds['N'] == [0, 10]))
        self.assertTrue(all(ds['M'] == [0, 10]))
        self.assertTrue(all(ds.rows(query.n == 0)['rho'] == [1, ]))
        self.assertTrue(all(ds.rows(where('n') == 0)['rho'] == [1, ]))

    def test_basic(self):
        ds = Dataset()
        ds.insert('/tmp/dataset/**/data.*')
        self._check_ds(ds)
        ds._missing()

    def test_verytinydb(self):
        from pantarei.database import VeryTinyDB
        db = VeryTinyDB()
        db.insert({'x': 1, 'tag': 'a'})
        db.insert({'x': 2, 'tag': 'a'})
        rows = db.search(query.tag == 'a')
        rows = db.rows()
        with open('/tmp/1', 'w') as fh:
            db.pprint(file=fh)

    def test_pprint(self):
        import os
        from pantarei.database import VeryTinyDB
        db = VeryTinyDB()
        db.insert({'x': 1.12121, 'tag': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'})
        db.insert({'x': 2, 'tag': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'})
        fh = open(os.devnull, 'w')
        db.pprint(max_width=30, file=fh)
        db = VeryTinyDB()
        db.insert({'x': 1.12121, 'tag': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'one': list(range(100))})
        db.insert({'x': 2, 'tag': 'bbb', 'one': list(range(100, 200))})
        db.pprint(max_width=80, file=fh)
        fh.close()

    def test_nanodb_2(self):
        from pantarei.database import VeryTinyDB
        db = VeryTinyDB()
        db.insert({'x': {'y': 1}, 'tag': 'a'})
        db.insert({'x': {'y': 2}, 'tag': 'a'})
        rows = db.search(query.tag == 'a')
        rows = db.rows()
        with open('/tmp/1', 'w') as fh:
            db.pprint(file=fh)
        #  print(rows['x']) # this would fail if we have a list of Documents

    def test_constructor(self):
        # Add parser at construction to allow customization
        def my_parse_yaml(path):
            import yaml
            with open(path, 'r') as fh:
                data = yaml.safe_load(fh)
            return data
        ds = Dataset(paths='/tmp/dataset/**/data.yaml',
                      parsers=[(my_parse_yaml, '*.yaml')])
        self.assertTrue(all(ds['N'] == [0, 10]))

        # Super compact
        data = Dataset(paths='/tmp/dataset/**/data.*')['N']
        self.assertEqual(list(data), [0, 10])

    def test_parser(self):
        # More control on parser for files with non standard extensions
        from pantarei.database import parse_pickle, parse_txt
        ds = Dataset(parsers=[(parse_pickle, '*.s')])
        ds.insert('/tmp/dataset/**/data.s')
        self.assertEqual(list(ds['S']), [0, 10])

    def test_parser_2(self):
        # More control on parser for files with non standard extensions
        ds = Dataset(parsers=[('txt', 'data.[1-2]'), ('path', '*')])
        # This will store x and w flattened in the database
        # This is not good if the column names are generic, use "key" update
        ds.insert('/tmp/dataset/**/data.*')
        self.assertTrue(all(ds.rows(query.n == 1)['x'][0] == [1, 2, 3]))
        self.assertTrue(all(ds.rows(query.n == 1)['w'][0] == [10, 20, 30]))

    def test_parser_3(self):
        self.skipTest('')
        from pantarei.database import parse_pickle, parse_txt_unpack
        ds = Dataset()
        ds.add_parser(parse_txt_unpack, 'data.[1-2]', update='key')
        ds.insert('/tmp/dataset/**/data.*')
        self.assertTrue('data.1.x' in ds.columns())
        self.assertTrue('data.1.y' in ds.columns())
        self.assertTrue('data.2.w' in ds.columns())
        self.assertTrue('data.2.z' in ds.columns())
        # self.assertEqual(list(ds['data.1'][0]['x']), [1, 2, 3])

    def test_parser_4(self):
        """Test straight parsing"""
        ds = Dataset('/tmp/dataset/**/data.s', parsers=[('pickle', '*')])
        self.assertTrue(numpy.all(ds.rows()['S'] == [0.0, 10.0]))

    def test_parser_binary(self):
        """Check that parse_txt fails silently with binary files"""
        ds = Dataset('/tmp/dataset/**/data.s', parsers=[('txt', '*')])
        # try:
        #     ds = Dataset('/tmp/dataset/**/data.s', parsers=[('txt', '*')])
        # except:
        #    self.assertTrue(False)

    def test_parser_no_columns(self):
        """Check that parse_txt does nothint when no column metadata is found"""
        ds = Dataset('/tmp/dataset/rho1.0/n1/data.bla', keep_default_parsers=False,
                      parsers=[('txt', '*')])
        # Little fragile
        self.assertEqual(set(ds.columns()), set(['_dirname', '_path']))

    # def test_parser_pantarei(self):
    #     from pantarei.database import parse_pickle, parse_txt
    #     ds = Dataset()
    #     ds.insert('run_data/**/*.*')
    #     # print(ds.columns())
    #     # print(ds.pprint(ignore=('fskt',)))
    #     # print(ds.rows()[0])
    #     #for row in ds.rows():
    #     #    print(row)

    def test_rows(self):
        # If the rows cannot be casted into a structured array
        # getting a column should return a numpy array, which can be masked
        # and then used to get arbitrary columns, even with heterogeneous data
        db = VeryTinyDB()
        db.insert({'x': numpy.array([1, 2]), 'tag': 'a'})
        db.insert({'x': numpy.array([1, 2]), 'tag': 'a'})

        # Homogeneous arrays
        df = db.rows()
        for row in df:
            pass
        self.assertEqual(df.columns, ['tag', 'x'])
        # pandas has it as function, we adhere to this design
        self.assertEqual(df['tag'].unique(), ['a'])
        self.assertEqual(list(df['tag']), ['a', 'a'])
        self.assertEqual(list(df['x'].mean(axis=0)), [1, 2])
        mask = df['tag'] == 'a'
        self.assertTrue(numpy.all(df['x'][mask] == [[1, 2], [1, 2]]))
        self.assertTrue(numpy.all(df['x'][mask].mean(axis=0) == [1, 2]))

        # Inhomogeneous arrays
        db.insert({'x': numpy.array([1, 2, 3]), 'tag': 'b'})
        df = db.rows()

        # Access
        for row in df:
            pass
        self.assertEqual(df.columns, ['tag', 'x'])
        # pandas has it as function, we adhere to this design
        self.assertEqual(list(df['tag'].unique()), ['a', 'b'])
        self.assertEqual(list(df['tag']), ['a', 'a', 'b'])

        data = df['x']
        data.crop = True
        #print(type(df['x']), data.shape, data.mean(axis=0))
        self.assertEqual(list(data.mean(axis=0)), [1, 2])

        mask = df['tag'] == 'a'

        self.assertTrue(numpy.all(df['x'][mask][0] == [1, 2]))
        self.assertTrue(numpy.all(df['x'][mask][1] == [1, 2]))

        # TODO: this fals atm, because along the first dimension we get a list
        # print(data[mask].mean(axis=0))
        #self.assertTrue(numpy.all(df['x'][mask].mean(axis=0) == [1, 2]))
        self.assertTrue(numpy.all(df['x'][df['tag'] == 'b'][0] == [1, 2, 3]))
        self.assertEqual(list(df['tag']), ['a', 'a', 'b'])

    def db_variable_string(self):
        db = VeryTinyDB()
        db.insert({'tag': 'a'})
        db.insert({'tag': 'abc'})
        self.assertEqual(str(db.rows()), str(db))
        self.assertTrue(all(db.rows()['tag'] == ['a', 'abc']))

    def test_groupby(self):
        from pantarei.database import Data

        db = VeryTinyDB()
        db.insert({'T': 1, 'x': numpy.array([1, 2, 3]), 'y': 20, 'seed': 1})
        db.insert({'T': 1, 'x': numpy.array([2, 3, 4]), 'y': 22, 'seed': 2})
        db.insert({'T': 2, 'x': numpy.array([10, 20, 30]), 'y': 10, 'seed': 1})
        db.insert({'T': 2, 'x': numpy.array([20, 30, 40]), 'y': 12, 'seed': 2})
        db.insert({'T': 3, 'x': numpy.array([100, 200, 300]), 'y': 30, 'seed': 1})
        db.insert({'T': 3, 'x': numpy.array([200, 300, 400]), 'y': 32, 'seed': 2})

        # Note: groupby() always returns a maskablelist.
        # We get a (M, ...) array ,where M is the number of occurrences of the key
        # in the group. Then that array can be averaged with numpy methods
        dg = db.groupby('T')
        self.assertEqual(list(dg['x'].mean(axis=0)[0]), [1.5, 2.5, 3.5])

        db = VeryTinyDB()
        db.insert({'T': 1, 'x': numpy.array([1, 2, 3]), 'y': 20, 'seed': 1})
        db.insert({'T': 1, 'x': numpy.array([2, 3, 4]), 'y': 21, 'seed': 2})
        db.insert({'T': 1, 'x': numpy.array([1, 2, 3]), 'y': 22, 'seed': 3})
        db.insert({'T': 1, 'x': numpy.array([2, 3, 4]), 'y': 23, 'seed': 4})
        db.insert({'T': 2, 'x': numpy.array([10, 20, 30]), 'y': 10, 'seed': 1})
        db.insert({'T': 2, 'x': numpy.array([20, 30, 40]), 'y': 11, 'seed': 2})
        dg = db.groupby('T')
        self.assertEqual(list(dg['x'].mean(axis=0)[1]), [15, 25, 35])
        
        # from pantarei.database import Data
        # def groupby(db, key):
        #     rows = db.find(sort_by=key)
        #     splits = rows[key].unique(return_index=True)[1][1:]
        #     return numpy.split(rows, splits) #, db.columns()

        # def groupby_one(db, key, what):
        #     groups = groupby(db, key)
        #     columns = db.columns()
        #     data_all = []
        #     for group in groups:
        #         data = Data(list(group), columns)
        #         data_all.append(data[what])
        #     Data(data_mean, columns)

        # def groupbyby(db, key, include=()):
        #     groups = groupby(db, key)
        #     columns = db.columns()
        #     columns.remove(key)
        #     columns = include
        #     for group in groups:
        #         for entry in group:
        #             #data = Data(list(group), columns)
        #             data_dict = {}
        #             for column in columns:
        #                 #data_dict[column] = data[column] #[0]
        #                 print(group)
        #                 data_dict[column] = group[column] #[0]
        #         data_mean.append(data_dict)
        #     return Data(data_mean, columns)

        # def groupby(db, key):
        #     groups = groupby(db, key)
        #     columns = db.columns()
        #     data_all = []
        #     for group in groups:
        #         data_dict = {}
        #         for column in columns:
        #             data_dict[column] = [_group[column] for _group in group]
        #         data_all.append(data_dict)
        #     return Data(data_all, columns)

    def test_maskable_attr(self):
        """Test dataset with inhomogeneous sizes forward attributes correctly"""
        from pantarei.database import Data

        db = VeryTinyDB()
        db.insert({'x': numpy.array([1, 2, 3]), 'y': 1, 'z': [1, 2]})
        db.insert({'x': numpy.array([2, 4]), 'y': 1, 'z': [1, 2, 3]})
        # Compute the mean for each entry
        self.assertEqual(db['x'].mean(), [2, 3])
        # Access a simple attribute
        self.assertEqual(db['x'].shape, [(3, ), (2, )])
        # Unique
        self.assertEqual(db['y'].unique(), 1)

    @unittest.skip('known failure')
    def test_maskable_unique(self):
        # TODO: fix this in maskablelist.unique()
        db = VeryTinyDB()
        db.insert({'z': [1, 2]})
        db.insert({'z': [1, 2, 3]})
        # Broken
        self.assertEqual(db['z'].unique(), [[1, 2], [1, 2, 3]])

    def test_maskable_inhomogeneous(self):
        # This works
        db = VeryTinyDB()
        db.insert({'x': [1, 2]   , 'y': 1})
        db.insert({'x': [1, 2, 3], 'y': 1})
        data = db.find()
        data.crop = True
        print(data['x'].mean(axis=0))

    def test_maskable_grouby_inhomogeneous(self):
        # This does not work: any access to attributes or mathods of something
        # return by groupby() fails, because we try to turn it into an ndarray
        db = VeryTinyDB()
        db.insert({'x': [1, 2]   , 'y': 1})
        db.insert({'x': [1, 2, 3], 'y': 1})
        data = db.groupby('y')
        data.crop = True
        # Groupby returns a list???
        # print(type(data))
        # print(data['x'][0])
        # This fails
        # print(data['x'].mean(axis=0))
        from pantarei.database import Data, maskablelist
        # print(maskablelist(data['x'][0], crop=True).mean(axis=0))
        # print(Data({'x': data['x'][0]}, ['x'], crop=True)['x'])
        # print([maskablelist(group['x'], crop=True).mean(axis=0) for group in data])
        for entry in data:
            print(maskablelist(entry['x'], crop=True).mean(axis=0))

    def test_sort(self):
        from pantarei.database import VeryTinyDB
        db = VeryTinyDB()
        db.insert({'x': 1, 'tag': 'b'})
        db.insert({'x': 3, 'tag': 'a'})
        db.insert({'x': 2, 'tag': 'c'})
        db.sort('x')
        self.assertEqual(list(db['x']), [1, 2, 3])
        db.insert({'x': 1, 'tag': 'a'})
        db.sort(('x', 'tag'))
        self.assertEqual(list(db['x']), [1, 1, 2, 3])
        self.assertEqual(list(db['tag']), ['a', 'b', 'c', 'a'])
            
    def tearDown(self):
        rmd('/tmp/dataset')

if __name__ == '__main__':
    unittest.main()
