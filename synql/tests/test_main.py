import pytest 
from synql import SynQL

class TestMain:

    def test_get_spider_create_statements(self, syn: SynQL):
        create_statements = syn.get_spider_create_statements()
        assert create_statements is not None
        print(create_statements['perpetrator'])
        assert isinstance(create_statements['perpetrator'], str)
        
        # perpetrator_schema = """CREATE TABLE perpetrator (perpetrator_id NUMBER, people_id NUMBER, date TEXT, YEAR NUMBER, LOCATION TEXT, country TEXT, killed NUMBER, injured NUMBER,
        #                         FOREIGN KEY (people_id) REFERENCES people(people_id));
        #                         CREATE TABLE people (people_id NUMBER, name TEXT, height NUMBER, weight NUMBER, home_town TEXT);"""

        # assert create_statements['perpetrator'] == perpetrator_schema
