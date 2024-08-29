import time
import sqlite3
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Database and DataFrame setup
db_path = "../local_data/spider/database/{db_id}/{db_id}.sqlite"
df = pd.read_csv("synql_spider_dev_original.csv")
df["execution_status"] = None

# Load unique database paths
db_ids = df["db_id"].unique()
db_paths = {db_id: db_path.format(db_id=db_id) for db_id in db_ids}
print("Loaded database paths for all databases")

# Create thread-local storage for database connections
thread_local = threading.local()

def get_connection(db_id):
    if not hasattr(thread_local, 'connections'):
        thread_local.connections = {}
    if db_id not in thread_local.connections:
        thread_local.connections[db_id] = sqlite3.connect(db_paths[db_id])
    return thread_local.connections[db_id]

def try_query(index, db_id, query):
    conn = get_connection(db_id)
    cur = conn.cursor()
    try:
        cur.execute(query)
        return index, True
    except:
        return index, False

# Function to execute queries concurrently
def check_queries_concurrently(df, num_workers=4):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(try_query, i, df.loc[i, "db_id"], df.loc[i, "query"])
            for i in range(len(df))
        ]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing queries", unit=" query"):
            i, valid = future.result()
            df.loc[i, "execution_status"] = valid

# Check the execution status of all queries
print("Checking execution status of all queries")
start_time = time.time()

# Adjust number of workers based on system resources
num_workers = 8
check_queries_concurrently(df, num_workers)

print("Saving to csv")
df.to_csv("synql_spider_dev_original_check.csv", index=False)

print("Time taken:", time.time() - start_time)