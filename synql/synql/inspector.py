# system packages 
import os
import math
from functools import cache
from typing import Optional, List, Dict

# internal packages
from .external.test_suite_sql_eval.process_sql import get_schema, Schema, get_sql
from .external.test_suite_sql_eval.exec_eval import eval_exec_match
from .external.test_suite_sql_eval.evaluation import evaluate, build_foreign_key_map_from_json, Evaluator, build_valid_col_units, rebuild_sql_val, rebuild_sql_col, print_scores, count_component1, count_component2, count_others, count_agg

# external packages 
import pandas as pd
from sqlglot import diff, parse_one, exp
import sqlglot as sg

class Inspector: 
    """A class for inspecting and comparing information in SQL Queries.
    """

    def __init__(self): 
        """Initializes the Inspector class.
        """
        self.evaluator = Evaluator()
        self.db_folder = None

    def set_db_folder(
            self, 
            db_folder_path: str,
        ): 
        """Sets the path to the database folder.
        
        :param db_path: The path to the database folder.
        :type db_path: str
        """
        
        if not os.path.exists(db_folder_path):
            raise ValueError("Invalid path: {}".format(db_folder_path))
        
        if not os.path.isdir(db_folder_path):
            raise ValueError("Path is not a directory: {}".format(db_folder_path))
        
        self.db_folder = db_folder_path
    
    @cache # TODO: how we want to handle caching
    def get_schema(
            self, 
            db_id: str,
        ) -> Schema:
        """Gets the schema of a database.
        
        :param db_id: The ID of the database.
        :type db_id: str
        :return: The schema of the database.
        :rtype: Schema
        """
        if self.db_folder is None:
            raise ValueError("Database folder not set.")
        
        db_path = os.path.join(self.db_folder, db_id, db_id + ".sqlite")
        if not os.path.exists(db_path):
            raise ValueError("Database not found: {}".format(db_path))
        
        try: 
            return Schema(get_schema(db_path))
        except Exception as e:
            raise ValueError("Error getting schema: {}".format(e)) # TODO: check if this is correct error type 

    def string_to_sql(
            self, 
            query: str,
            db_id: str,
        ) -> str:
        """Converts a string to a SQL query.
        
        :param db_id: The ID of the database.
        :type db_id: str
        :param query: The query to convert.
        :type query: str
        :return: The SQL query.
        :rtype: str
        """
        schema = self.get_schema(db_id)
        return get_sql(schema, query)
    
    def clean_spider_query(
            self,
            query: str,
    ) -> str:
        """Cleans a query to remove any special characters (Spider Specific).
        
        :param query: The query to clean.
        :type query: str
        """
        query = query.replace("<>", "!=")   
        return query
    
    @cache
    def evaluate_difficulty(
            self, 
            query: str,
            db_id: str,
            clean_query: Optional[bool] = True, # TODO: we can remove this once we move to using sqlglot to calculate difficulty   
        ) -> str:
        """Evaluates the hardness of a query.
        
        :param db_id: The ID of the database.
        :type db_id: str
        :param query: The query to evaluate.
        :type query: str
        :return: The hardness of the query.
        :rtype: str
        """
        if clean_query:
            query = self.clean_spider_query(query)
        try: 
            sql = self.string_to_sql(query, db_id)
            return self.evaluator.eval_hardness(sql)
        except Exception as e:
            print("Error evaluating hardness: {}".format(e)) # TODO: we should add logging
            return None
            #raise ValueError("Error evaluating hardness: {}".format(e))
        
    ##############################
    # Dataframe Specific Methods #
    ##############################
    # TODO: decide if we want to keep these methods, remove/move them, or refactor them so the dataframe is a class attribute

    def df_sql_difficulty(
            self, 
            df: pd.DataFrame,
            query_col: Optional[str] = "query",
            db_col: Optional[str] = "db_id",
            difficulty_col: Optional[str] = "difficulty",
            categorizer: Optional[str] = "spider"
        ) -> pd.DataFrame:
        """Evaluates the hardness of a query in a dataframe.
        
        :param df: The dataframe.
        :type df: pd.DataFrame
        :param query_col: The column containing the queries.
        :type query_col: str
        :param db_col: The column containing the database IDs.
        :type db_col: str
        :return: The dataframe with the hardness of the queries.
        :rtype: pd.DataFrame
        """
        if categorizer == "spider":
            df[difficulty_col] = df.apply(lambda x: self.evaluate_difficulty(x[query_col], x[db_col]), axis=1)
            return df
        elif categorizer == "sqlglot":
            df[difficulty_col] = df[query_col].apply(lambda x: self.spider_eval_hardness(x))
            return df
        else: 
            raise ValueError("Invalid categorizer: {}".format(categorizer))
    
    ############################
    # SQLGlot Query Inspection #
    ############################

    def get_group_bys(self, sql): 
        '''returns all group by statements within the sql query'''
        # TODO: we can get more granular here, and record the number of tables & columns in the group by statement, but for now, we'll just record the group by statement
        group_bys = []
        for group_by in parse_one(sql).find_all(exp.Group):
            group_bys.append(group_by)
        return group_bys
    
    def get_where_statements(self, sql):
        '''returns all where statements within the sql query'''
        where_statements = []
        for where_statement in parse_one(sql).find_all(exp.Where):
            where_statements.append(where_statement)
        return where_statements
    
    def get_first_select_where_statement(self, sql):
        where_statement = []
        first_select = self.get_first_select_statement(sql)
        for where in parse_one(sql).find_all(exp.Where):
            if where.parent == first_select:
                where_statement.append(where)
        return where_statement
    
    def get_functions(self, sql): 
        '''returns all functions within the sql query'''
        functions = []
        for function in parse_one(sql).find_all(exp.Func):
            functions.append(function)
        return functions
    
    def get_unions(self, sql): 
        '''returns all union statements within the sql query'''
        unions = []
        for union in parse_one(sql).find_all(exp.Union):
            unions.append(union)
        for intersect in parse_one(sql).find_all(exp.Intersect): # TODO: temporary fix for intersect statements
            if intersect in unions: 
                unions.remove(intersect)
        for except_ in parse_one(sql).find_all(exp.Except): # TODO: temporary fix for except statements
            if except_ in unions: 
                unions.remove(except_)
        return unions
    
    def get_except_statements(self, sql): 
        '''returns all except statements within the sql query'''
        except_statements = []
        for except_statement in parse_one(sql).find_all(exp.Except):
            except_statements.append(except_statement)
        return except_statements
    
    def get_intersect_statements(self, sql):
        '''returns all intersect statements within the sql query'''
        intersect_statements = []
        for intersect_statement in parse_one(sql).find_all(exp.Intersect):
            intersect_statements.append(intersect_statement)
        return intersect_statements
    
    def get_selects(self, sql): 
        '''returns all select statements within the sql query'''
        projections = []
        for projection in parse_one(sql).find_all(exp.Select):
            projections.append(projection)
        return projections
    
    def get_or_statements(self, sql): 
        '''returns all or statements within the sql query'''
        or_statements = []
        for or_statement in parse_one(sql).find_all(exp.Or):
            or_statements.append(or_statement)
        return or_statements
    
    def get_like_statements(self, sql): 
        '''returns all like statements within the sql query'''
        like_statements = []
        for like_statement in parse_one(sql).find_all(exp.Like):
            like_statements.append(like_statement)
        return like_statements
    
    def get_joins(self, sql): 
        '''returns all join statements within the sql query'''
        joins = []
        for join in parse_one(sql).find_all(exp.Join):
            joins.append(join)
        return joins
    
    def get_limits(self, sql):
        '''returns all limit statements within the sql query'''
        limits = []
        for limit in parse_one(sql).find_all(exp.Limit):
            limits.append(limit)
        return limits
    
    def get_first_select_limit(self, sql):  
        limit = []
        first_select = self.get_first_select_statement(sql)
        for limit_statement in parse_one(sql).find_all(exp.Limit):
            if limit_statement.parent == first_select:
                limit.append(limit_statement)
        return limit
    
    def get_order_bys(self, sql):
        '''returns all order by statements within the sql query'''
        order_bys = []
        for order_by in parse_one(sql).find_all(exp.Order):
            order_bys.append(order_by)
        return order_bys
    
    def get_first_select_order_by(self, sql):
        order_by = []
        first_select = self.get_first_select_statement(sql)
        for order in parse_one(sql).find_all(exp.Order):
            if order.parent == first_select:
                order_by.append(order)
        return order_by
    
    def get_having_statements(self, sql):   
        '''returns all having statements within the sql query'''
        having_statements = []
        for having_statement in parse_one(sql).find_all(exp.Having):
            having_statements.append(having_statement)
        return having_statements
    
    # TODO: we can refactor this so we only parse the sql query once
    def get_columns(self, sql): 
        '''return all columns that are being selected within the sql query'''
        columns = []
        for column in parse_one(sql).find_all(exp.Column):
            columns.append(column.alias_or_name)
        return columns

    def get_stars(self, sql):
        '''returns all star statements within the sql query'''
        stars = []
        for star in parse_one(sql).find_all(exp.Star):
            stars.append(star)
        return stars
    
    def get_subqueries(self, sql):
        '''returns all subqueries within the sql query'''
        subqueries = []
        for subquery in parse_one(sql).find_all(exp.Subquery):
            subqueries.append(subquery)
        return subqueries
    
    def strip_nodes(self, node): 
        # TODO: we should handle this in a better way
        """The goal of this function is to leave us with JUST the base select statement and its columns"""
        if isinstance(node, sg.exp.Where):
            return 
        if isinstance(node, sg.exp.Having):
            return 
        if isinstance(node, sg.exp.Intersect):
            return 
        if isinstance(node, sg.exp.Except):
            return 
        if isinstance(node, sg.exp.Like):
            return 
        if isinstance(node, sg.exp.Or):
            return 
        if isinstance(node, sg.exp.Order):
            return 
        if isinstance(node, sg.exp.Group):
            return 
        return node

    def strip_query(self, sql):
        # TODO: we should handle this in a better way
        try: # TODO: we need to decide how we want to handle errors
            return sg.parse_one(sql).transform(self.strip_nodes).sql()
        except Exception as e:
            # print(e) # TODO: implement logging
            return sql
        
    def get_first_select_statement(self, sql):
        for s in sg.parse_one(sql).find_all(exp.Select):
            return s
        
    # Temporary solution to bug in sqlglot
    def get_select_statements_in_parents(self, sql):
        subqueries = []
        for s in sg.parse_one(sql).find_all(exp.Select):
            if isinstance(s.parent, exp.In):
                subqueries.append(s.parent)
        return subqueries
    
    def get_select_columns(self, sql):
        # TODO: Note, this does not work well with subqueries, as it will parse out those columns
        try:
            return self.get_columns(self.strip_query(sql)) + self.get_stars(self.strip_query(sql))
        except: 
            return self.get_columns(sql) + self.get_stars(sql) # TODO: we should handle errors more gracefully here. we do this for instances where the FROM statement is a nested query as that was previously failing. ex: 'SELECT COUNT(*) FROM (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "Dutch")'

    
    ###########################################################
    # Spider Based Difficulty Scores (sqlglot implementation) #
    ###########################################################
    
    def get_first_select_columns(self, sql):
        # TODO: this is a hacky way to get the first select column and is known to fail on nested from statements
        sql = self.get_first_select_statement(sql).sql()
        sql_s = self.strip_query(sql)
        try:
            return self.get_columns(sql_s) + self.get_stars(sql_s)
        except:
            return self.get_columns(sql) + self.get_stars(sql)

    def spider_count_component1(self, sql):
        count = 0 
        if len(self.get_where_statements(sql)) > 0: # NOTE: within the Spider evaluation script, they only evaluate the WHERE statements within the first SELECT statement. this appears to be an error in their parser more than anything else, so we choose to go with what we believe is a corrected version of their implementation. 
            count += 1
        if len(self.get_group_bys(sql)) > 0: 
            count += 1
        if len(self.get_order_bys(sql)) > 0: # NOTE: within the Spider evaluation script, they only evaluate the ORDER_BY statements within the first SELECT statement. this appears to be an error in their parser more than anything else, so we choose to go with what we believe is a corrected version of their implementation. 
            count += 1
        if len(self.get_limits(sql)) > 0: # NOTE: within the Spider evaluation script, they only evaluate the LIMIT statements within the first SELECT statement. this appears to be an error in their parser more than anything else, so we choose to go with what we believe is a corrected version of their implementation. 
            count += 1
        # TODO: we should sanity check that this only cou
        if len(self.get_joins(sql)) > 0: # JOIN # NOTE: we just count the number of joins here, but spider opted to count number of tables and subtract one from that count
            count += len(self.get_joins(sql)) # - 1 # NOTE: there is no need to subtract 1, spider does this to not double count the first select statement
        count += len(self.get_or_statements(sql))
        count += len(self.get_like_statements(sql))
        return count

    def spider_count_component2(self, sql):
        # in the spider implementation, this function simply wraps `get_nestedSQL`. in short, this is a count of the number of nested select statements, interserct, except, and union
        count = 0 
        count += len(self.get_subqueries(sql))
        count += len(self.get_select_statements_in_parents(sql)) # TODO: this is a temporary solution due to a bug where IN subqueries are not recognized

        count += len(self.get_intersect_statements(sql))
        count += len(self.get_except_statements(sql))
        count += len(self.get_unions(sql))
        return count

    def spider_count_others(self, sql):
        count = 0 
        agg_count = len(self.get_functions(sql))
        if agg_count > 1: # if more than one function, increase count by 1
            count += 1
        # TODO: we do not gracefully handle errors yet, which could result in an overcount of columns (counting columns in WHERE statements, etc.)
        # TODO: a temporary solution would be to count number of WHERE, HAVING, etc. occurances and decrement count accordingly
        if len(self.get_select_columns(sql)) > 1: # NOTE: this will drop subqueries and not include those columns. in spider, they only count the first select statements columns, so that is fine for now.
            count += 1
        if len(self.get_where_statements(sql)) > 1:
            count += 1
        if len(self.get_group_bys(sql)) > 1:
            count += 1
        return count

    def spider_eval_difficulty(self, sql):
        count_comp1_ = self.spider_count_component1(sql)
        count_comp2_ = self.spider_count_component2(sql)
        count_others_ = self.spider_count_others(sql)

        if count_comp1_ <= 1 and count_others_ == 0 and count_comp2_ == 0:
            return "easy"
        elif (count_others_ <= 2 and count_comp1_ <= 1 and count_comp2_ == 0) or \
                (count_comp1_ <= 2 and count_others_ < 2 and count_comp2_ == 0):
            return "medium"
        elif (count_others_ > 2 and count_comp1_ <= 2 and count_comp2_ == 0) or \
                (2 < count_comp1_ <= 3 and count_others_ <= 2 and count_comp2_ == 0) or \
                (count_comp1_ <= 1 and count_others_ == 0 and count_comp2_ <= 1):
            return "hard"
        else:
            return "extra"
        
    ###########################################################
    # Schema based Difficulty Scores (spider implementation)  #
    ###########################################################

    @staticmethod
    def get_dynamic_difficulty_ranges(
        table_components: Dict[str, Dict[str, int]]
    ):
        df = pd.DataFrame(table_components)
        value_avgs = df.mean(axis=1).to_dict()
        value_stds = df.std(axis=1).to_dict()

        ranges = {
            "easy": {
                "greater_than": {
                    "tables": 0,
                    "columns": 0,
                    "foreign_keys": 0,
                },
                "less_than": {
                    "tables": value_avgs['tables'] - (value_stds['tables'] / 2),
                    "columns": value_avgs['columns'] - (value_stds['columns'] / 2),
                    "foreign_keys": value_avgs['foreign_keys'] - (value_stds['foreign_keys'] / 2),
                },
            },
            "medium": {
                "greater_than": {
                    "tables": value_avgs['tables'] - (value_stds['tables'] / 2),
                    "columns": value_avgs['columns'] - (value_stds['columns'] / 2),
                    "foreign_keys": value_avgs['foreign_keys'] - (value_stds['foreign_keys'] / 2),
                },
                "less_than": {
                    "tables": value_avgs['tables'],
                    "columns": value_avgs['columns'],
                    "foreign_keys": value_avgs['foreign_keys'],
                },
            },
            "hard": {
                "greater_than": {
                    "tables": value_avgs['tables'],
                    "columns": value_avgs['columns'],
                    "foreign_keys": value_avgs['foreign_keys'],
                },
                "less_than": {
                    "tables": value_avgs['tables'] + (value_stds['tables'] / 2),
                    "columns": value_avgs['columns'] + (value_stds['columns'] / 2),
                    "foreign_keys": value_avgs['foreign_keys'] + (value_stds['foreign_keys'] / 2),
                },
            },
            "extra": {
                "greater_than": {
                    "tables": value_avgs['tables'] + (value_stds['tables'] / 2),
                    "columns": value_avgs['columns'] + (value_stds['columns'] / 2),
                    "foreign_keys": value_avgs['foreign_keys'] + (value_stds['foreign_keys'] / 2),
                },
                "less_than": {
                    "tables": 1000,
                    "columns": 1000,
                    "foreign_keys": 1000,
                },
            },
        }
        return ranges

    @staticmethod
    def spider_component_difficulty(table_components, ranges, categories=["extra", "hard", "medium", "easy"], components=["tables", "columns", "foreign_keys"]):
        table_difficulty = None
        column_difficulty = None
        foreign_key_difficulty = None

        for category in categories:
            lower_bound = ranges[category]["greater_than"]
            upper_bound = ranges[category]["less_than"]
            for component in components: 
                lower_bound_component = lower_bound[component]
                upper_bound_component = upper_bound[component]
                # print(f"component: {component}, score: {table_components[component]}")
                # print(f"lower_bound: {lower_bound_component}, upper_bound: {upper_bound_component}")
                if table_components[component] >= lower_bound_component and table_components[component] < upper_bound_component:
                    if component == "tables":
                        table_difficulty = category
                    elif component == "columns":
                        column_difficulty = category
                    elif component == "foreign_keys":
                        foreign_key_difficulty = category
        return table_difficulty, column_difficulty, foreign_key_difficulty

    @staticmethod
    def spider_schema_difficulty(table_difficulty, column_difficulty, foreign_key_difficulty): 
        points = {"easy": 1, "medium": 2, "hard": 3, "extra": 4}
        categories = {1: "easy", 2: "medium", 3: "hard", 4: "extra"}
        avg = math.ceil((points[table_difficulty] + points[column_difficulty] + points[foreign_key_difficulty]) / 3)
        return categories[avg]