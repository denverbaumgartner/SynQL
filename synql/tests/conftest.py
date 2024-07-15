# internal packages
import os
from typing import List

# external packages
from pytest import fixture
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv("../.env")

# internal packages
from synql import SynQL

@fixture
def syn() -> SynQL:
    synql = SynQL()
    spider_path = "tests/local_data/spider/"
    db_path = "tests/local_data/spider/database/"
    synql.inspector.set_db_folder(db_path)
    synql.loader.load_spider(spider_path)
    return synql 

@fixture
def gold_diffs() -> List[List]: 
    queries = []
    dbs = []
    diffs = []
    with open("tests/local_data/eval/gold_difficulty.txt", "r") as f:
        lines = f.readlines()
        for line in lines: 
            vals = line.split("|")
            queries.append(vals[0])
            dbs.append(vals[1])
            diffs.append(vals[2])
    return [queries, dbs, diffs]

@fixture
def open_ai_client() -> OpenAI:
    return OpenAI(
        api_key = os.getenv("OPENAI_API_KEY"),
    )