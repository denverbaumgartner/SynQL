import pytest 
from synsql import SynSql

class TestMain:

    def test_load_spider(self, syn: SynSql):
        # test that spider data was loaded
        assert syn.loader.spider is not None

        # test that we are loading the table information correctly, so that every entity in the list is associated with a database id
        for table in syn.loader.spider['tables']:
            assert table['db_id'] is not None   