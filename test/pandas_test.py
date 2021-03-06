from socrata import Socrata
from socrata.authorization import Authorization
from auth import auth, TestCase
try:
    import pandas as pd
except ImportError:
    print("Pandas is required for this test")
    exit()
class TestPandas(TestCase):
    def test_create_source(self):
        rev = self.create_rev()

        (ok, source) = rev.create_upload('foo.csv')
        self.assertTrue(ok)
        self.assertEqual(source.attributes['source_type']['filename'], 'foo.csv')

        assert 'show' in source.list_operations()
        assert 'bytes' in source.list_operations()

    def test_source_csv(self):
        rev = self.create_rev()
        (ok, source) = rev.create_upload('foo.csv')
        assert ok

        df = pd.read_csv('test/fixtures/simple.csv')
        (ok, source) = source.df(df)
        input_schema = source.get_latest_input_schema()
        self.assertTrue(ok)
        self.assertEqual(input_schema.attributes['total_rows'], 4)

        names = sorted([ic['field_name'] for ic in input_schema.attributes['input_columns']])
        self.assertEqual(['a', 'b', 'c'], names)

        assert 'show' in input_schema.list_operations()

    def test_create_source_outside_rev(self):
        pub = Socrata(auth)

        (ok, source) = pub.sources.create_upload('foo.csv')
        self.assertTrue(ok, source)
        self.assertEqual(source.attributes['source_type']['filename'], 'foo.csv')

        assert 'show' in source.list_operations()
        assert 'bytes' in source.list_operations()

    def test_source_csv_outside_rev(self):
        pub = Socrata(auth)

        (ok, source) = pub.sources.create_upload('foo.csv')
        self.assertTrue(ok, source)
        df = pd.read_csv('test/fixtures/simple.csv')
        (ok, source) = source.df(df)
        self.assertTrue(ok, source)
        input_schema = source.get_latest_input_schema()
        names = sorted([ic['field_name'] for ic in input_schema.attributes['input_columns']])
        self.assertEqual(['a', 'b', 'c'], names)

    def test_put_source_in_revision(self):
        pub = Socrata(auth)

        (ok, source) = pub.sources.create_upload('foo.csv')
        self.assertTrue(ok, source)

        df = pd.read_csv('test/fixtures/simple.csv')
        (ok, input_schema) = source.df(df)
        self.assertTrue(ok, input_schema)

        rev = self.create_rev()

        (ok, source) = source.add_to_revision(rev)
        self.assertTrue(ok, source)
