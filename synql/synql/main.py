# system packages 
import os
import json
from typing import Optional, Dict
from types import SimpleNamespace
from pathlib import Path

# internal packages
from .loader import Loader
from .transform import Transform    
from .format import Formatter
from .extractor import Extractor
from .inspector import Inspector    
from .visualizer import Visualizer
from .evaluator import Eval
from .helper import validate_system_path
from .synth import JointGenerationSynth

# external packages
import pandas as pd

class SynSql:
    """A high level class for interfacing with the synsql library."""

    def __init__(self) -> None:
        self.loader = Loader()
        self.transform = Transform(self.loader)
        self.format = Formatter()
        self.extractor = Extractor()    
        self.inspector = Inspector()
        self.visualizer = Visualizer()
        self.evaluator = Eval()

        # generator classes 
        self.joint_generator = JointGenerationSynth()

        # prompts 
        self.prompt_path = Path(__file__).parent / "data" / "prompts.json"

    def load_spider(self, local_path: str) -> None:
        """Load the spider dataset from a local path."""
        self.loader.load_spider(local_path)

    def format_spider_schemas(
            self, 
            db_path: str,
            dev: bool = True,
            train: bool = True,
            schema_serialization_type: Optional[str] = "peteshaw",
            schema_serialization_randomized: Optional[bool] = False,
            schema_serialization_with_db_id: Optional[bool] = True,
            schema_serialization_with_db_content: Optional[bool] = True,
            normalize_query: Optional[bool] = True,
            save_local_path: Optional[str] = None,
        ):
        db_details = self.loader.get_spider_db_details() 
        
        if dev: 
            for d in self.loader.spider['dev']:
                formatted_schema = self.format.format_schema(
                    question=d['question'],
                    db_id=d['db_id'],
                    db_path=db_path,
                    db_column_names=db_details[d['db_id']]['column_names'],
                    db_table_names=db_details[d['db_id']]['table_names'],
                    schema_serialization_type=schema_serialization_type,
                    schema_serialization_randomized=schema_serialization_randomized,
                    schema_serialization_with_db_id=schema_serialization_with_db_id,
                    schema_serialization_with_db_content=schema_serialization_with_db_content,
                    normalize_query=normalize_query,
                )
                d['formatted_schema'] = formatted_schema
        if train:
            for t in self.loader.spider['train']:
                formatted_schema = self.format.format_schema(
                    question=t['question'],
                    db_id=t['db_id'],
                    db_path=db_path,
                    db_column_names=db_details[t['db_id']]['column_names'],
                    db_table_names=db_details[t['db_id']]['table_names'],
                    schema_serialization_type=schema_serialization_type,
                    schema_serialization_randomized=schema_serialization_randomized,
                    schema_serialization_with_db_id=schema_serialization_with_db_id,
                    schema_serialization_with_db_content=schema_serialization_with_db_content,
                    normalize_query=normalize_query,
                )
                t['formatted_schema'] = formatted_schema
        
        if save_local_path:
            with open(save_local_path, 'w') as f:
                json.dump(self.loader.spider, f)
        return self.loader.spider
    
    def assess_spider_difficulty(
            self,
            db_folder_path: Optional[str] = None,): 
        """Assess the difficulty of the Spider dataset."""
        if self.inspector.db_folder is None:
            if db_folder_path is None:
                raise ValueError("Database folder not set.")
            self.inspector.set_db_folder(db_folder_path)

        for d in self.loader.spider['dev']:
            d['difficulty'] = self.inspector.evaluate_difficulty(
                query=d['query'],
                db_id=d['db_id'],
            )
        for t in self.loader.spider['train']:
            t['difficulty'] = self.inspector.evaluate_difficulty(
                query=t['query'],
                db_id=t['db_id'],
            )
        return self.loader.spider
    
    def get_spider_create_statements(
            self, 
            local_path: Optional[str] = None,
    ) -> Dict[str, str]:
        if local_path is not None:
            self.loader.load_spider(local_path)
        elif self.loader.spider is None:
            raise ValueError("Spider data not loaded.")
        tables = self.loader.spider['tables']
        create_statements = {table['db_id']: self.format.get_spider_create_statement(table) for table in tables}
        return create_statements