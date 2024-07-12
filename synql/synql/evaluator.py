# system packages 
from typing import Optional, Dict, List

# internal packages
from .external.test_suite_sql_eval.process_sql import get_schema, Schema, get_sql
from .external.test_suite_sql_eval.exec_eval import eval_exec_match
from .external.test_suite_sql_eval.evaluation import evaluate, build_foreign_key_map_from_json, Evaluator, build_valid_col_units, rebuild_sql_val, rebuild_sql_col, print_scores, count_component1, count_component2, count_others, count_agg

# external packages
import sqlite3
import pandas as pd

class Eval:
    """A class for evaluating generated SQL queries.
    """

    def __init__(self) -> None:
        self.eval = Evaluator()
        self.kmaps = None

    def get_kmaps(
            self, 
            table_path: str
    ):
        """Get the foreign key maps from the table path.
        """
        self.kmaps = build_foreign_key_map_from_json(table_path)
        return self.kmaps

    async def test_suite_eval(
            self, 
            gold_path: str,
            pred_path: str,
            db_path: str,
            kmaps: Dict, 
            etype: Optional[str] = "all",    
            plug_value: Optional[bool] = False,
            keep_distinct: Optional[bool] = True,
            progress_bar_for_each_datapoint: Optional[bool] = False,
    ):
        scores, accuracy = await evaluate(gold_path, pred_path, db_path, etype, kmaps, plug_value, keep_distinct, progress_bar_for_each_datapoint)

        evaluation = {}
        evaluation['scores'] = scores
        evaluation['accuracy'] = accuracy
        return evaluation
    
    def build_eval_report(
            self, 
            gold_path: str,
            pred_path: str,
            eval_report: Dict,
    ):
        """Build a basic evaluation report for a single prediction.
        """

        with open(gold_path, 'r') as f:
            golds = [line.strip().split('\t') for line in f.readlines()]
        gs, db_ids = zip(*[(g[0], g[1]) for g in golds])

        with open(pred_path, 'r') as f:
            ps = [line.strip() for line in f.readlines()]

        pred_df = pd.DataFrame({'gold': gs, 'pred': ps, 'db_id': db_ids, 'valid': eval_report['accuracy']})
        return pred_df
    
    def evaluation_to_df(
            self, 
            eval_report: Dict,
    ) -> pd.DataFrame:
        """Convert an evaluation report to a DataFrame.
        """
        categories = ["easy", "medium", "hard", "extra", "all"]
        measurements = ["execution_accuracy", "exact_matching_accuracy"]

        scores = {
            f"{category}_{measurement}": eval_report["scores"][category][measurement]
            for category in categories
            for measurement in measurements
        }

        score_df = pd.DataFrame.from_dict(scores, orient='index').T
        return score_df
    
    def check_validity(
            self,
            query: str, 
            schema: str,
    ): 
        """Check the validity of a query given a schema.
        """
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        try:
            cursor.executescript(schema)
            cursor.execute("BEGIN")
            cursor.execute(query)
            cursor.execute("ROLLBACK")
        except sqlite3.Error as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
        return True, "Query is valid"