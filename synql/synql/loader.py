# system packages 
import os
import json
from typing import Optional, Dict, List

# internal packages
from .helper import validate_system_path

# external packages
import pandas as pd
import datasets as ds

class Loader:
    """A class for loading SQL data.
    """

    def __init__(self):
        self.spider = None

    def load_local_spider(self, local_path: str): 
        """A function for loading a local file into memory, helpful for avoiding having to reprocess the dataset every time. 
        
        :param local_path: The path to the local file.
        :type local_path: str
        """
        validate_system_path(local_path)
        with open(local_path, "r") as f: 
            self.spider = json.load(f)

    def save_local_spider(self, local_path: str): 
        """A function for saving the Spider dataset to a local file.
        
        :param local_path: The path to the local file.
        :type local_path: str
        """
        validate_system_path(local_path)
        with open(local_path, "w") as f: 
            json.dump(self.spider, f)

    def load_spider(self, local_path: str):
        # TODO: we should make this download the data from the internet if a local path is not provided
        validate_system_path(local_path)

        file_names = ["dev.json", "train_spider.json", "tables.json"]
        file_paths = {name.split('.')[0]: os.path.join(local_path, name) for name in file_names}

        for key, path in file_paths.items():
            if not os.path.exists(path):
                raise ValueError(f"Invalid path: {path}")
        
        data = {key: json.load(open(path, "r")) for key, path in file_paths.items()}
        self.spider = {
            "dev": data["dev"],
            "train": data["train_spider"],
            "tables": data["tables"],
        }

    def get_spider_db_details(self) -> Dict: 
        """Get the details of the Spider databases."""
        if self.spider is None:
            raise ValueError("Spider data not loaded.")
        
        db_details = {}
        for t in self.spider["tables"]:
            db_id = t["db_id"]
            columns = t['column_names_original']
            table_ids, column_names = zip(*columns)  # Unpack columns into two lists

            db_details[db_id] = {
                'column_names': {
                    'table_id': list(table_ids),
                    'column_name': list(column_names)
                },
                'table_names': t['table_names_original']
            }
        return db_details
    
    def spider_to_pandas(
            self, 
            group: str = "train",
            subset: Optional[List[str]] = ["db_id", "question", "query"]
            ) -> pd.DataFrame:
        """Convert the Spider data to a pandas DataFrame."""
        if self.spider is None:
            raise ValueError("Spider data not loaded.")
        
        if group not in ["train", "dev"]:
            raise ValueError("Invalid group: {}".format(group))
        
        data = self.spider[group]
        return pd.DataFrame(data)[subset]
        