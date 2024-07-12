# system packages 
from typing import Optional, Dict, List

# internal packages
from .external.picard.schema_encoding import serialize_schema

# external packages
import sqlparse

class Formatter: 
    """A class for formatting SQL data, typically for prompting.
    """

    def __init__(self):
        pass

    def format_schema(
            self, 
            question: str,
            db_id: str, 
            db_path: str,
            db_column_names: Dict[str, str],
            db_table_names: List[str],
            schema_serialization_type: Optional[str] = "peteshaw",
            schema_serialization_randomized: Optional[bool] = False,
            schema_serialization_with_db_id: Optional[bool] = True,
            schema_serialization_with_db_content: Optional[bool] = True,
            normalize_query: Optional[bool] = True,
    ): 
        if schema_serialization_type != "peteshaw": 
            raise ValueError("Only peteshaw schema serialization is supported at this time.")
        return serialize_schema(
            question=question,
            db_path=db_path,
            db_id=db_id,
            db_column_names=db_column_names,
            db_table_names=db_table_names,
            schema_serialization_randomized=schema_serialization_randomized,
            schema_serialization_with_db_id=schema_serialization_with_db_id,
            schema_serialization_with_db_content=schema_serialization_with_db_content,
            normalize_query=normalize_query,
        )
    
    @staticmethod 
    def generate_spider_create_statements(db_schema):
        create_statements = []

        db_schema['table_names'] = [table.replace(' ', '_') for table in db_schema['table_names']]

        # Helper function to find column name by index
        def find_column_name(col_index):
            return db_schema['column_names'][col_index][1].replace(' ', '_')

        # Loop through each table and its columns to create table statements
        for table_index, table in enumerate(db_schema['table_names']):
            columns = [col for col in db_schema['column_names'] if col[0] == table_index]
            column_definitions = []

            for col in columns:
                col_name = col[1].replace(' ', '_')
                col_type = db_schema['column_types'][db_schema['column_names'].index(col)]
                col_definition = f"{col_name} {col_type.upper()}"

                # Check if the column is a primary key
                if col[1] in [find_column_name(pk) for pk in db_schema['primary_keys'] if pk == db_schema['column_names'].index(col)]:
                    col_definition += " PRIMARY KEY"

                column_definitions.append(col_definition)

            # Handling foreign key constraints within the table
            foreign_keys = [fk for fk in db_schema['foreign_keys'] if db_schema['column_names'][fk[0]][0] == table_index]
            for fk in foreign_keys:
                child_col = find_column_name(fk[0])
                parent_col = find_column_name(fk[1])
                parent_table = db_schema['table_names'][db_schema['column_names'][fk[1]][0]]

                fk_definition = f"FOREIGN KEY ({child_col}) REFERENCES {parent_table}({parent_col})"
                column_definitions.append(fk_definition)

            # Creating the CREATE TABLE statement
            create_statement = f"CREATE TABLE {table} ({', '.join(column_definitions)});"
            create_statements.append(create_statement)

        return create_statements
    
    @staticmethod
    def format_spider_create(create_statements):
        cs = ''
        for create in create_statements: 
            cs += sqlparse.format(create, reindent=True, keyword_case='upper') + '\n'
        return cs

    @staticmethod
    def get_spider_create_statement(
            db_schema, # this must match the structure of the tables in the Spider database file
    ): 
        return Formatter.format_spider_create(Formatter.generate_spider_create_statements(db_schema))