# basic packages
import re
import string
from IPython.utils import io
from itertools import combinations
from typing import Union, List, Optional, Dict, Type, Any, Callable, Tuple

# external packages
import sqlglot as sg
from sqlglot.diff import Keep
import networkx as nx

class Extractor:
    """A class for extracting and manipulating information in SQL Queries.
    """

    def __init__(self):
        pass

    def get_ast(
            self, 
            query: str,
        ): # TODO: add sqlglot type hints
        """Get the AST of a SQL query.

        :param query: A SQL query.
        :type query: str
        :return: The AST of the SQL query.
        :rtype: sqlglot.AST
        """
        return sg.parse_one(query)
    
    def get_graphs(
            self, 
            ast, # TODO: add sqlglot type hints 
        ): # TODO: add networkx type hints
        # TODO: issue #2
        """Takes an AST representation of a SQL query and returns a directed and undirected graph representation of the query.
        
        :param ast: An AST representation of a SQL query.
        :type ast: sqlglot.AST 
        :return: A directed and undirected graph representation of the query.
        :rtype: nx.DiGraph, nx.Graph
        """ 
        G = nx.Graph()
        Gd = nx.DiGraph()

        for node, *_ in ast.walk():
            G.add_node(node, key=node.key)
            Gd.add_node(node, key=node.key)
            if node.parent:
                G.add_edge(node.parent, node)
                Gd.add_edge(node.parent, node)
        return G, Gd

    def get_leaves(
            self, 
            Gd: nx.DiGraph,
        ) -> List: # TODO: add networkx node type hints
        """Takes a directed graph and returns a list of the leaf nodes.
        
        :param Gd: A directed graph.
        :type Gd: nx.DiGraph
        :return: A list of the leaf nodes.
        :rtype: list
        """
        return [node for node in Gd.nodes() if len(list(Gd.successors(node))) == 0]
    
    def get_pairs(
            self, 
            leaves, # TODO: add networkx node type hints
        ) -> List[Tuple]: 
        """Takes a list of leaf nodes and returns a list of all possible pairs of leaf nodes (mapped by indexes).
        
        :param leaves: A list of leaf nodes.
        :type leaves: list
        :return: A list of all possible pairs of leaf nodes.
        :rtype: list
        """
        count = len(leaves)
        return list(combinations(range(count), 2))
    
    def get_path(
            self, 
            G, # TODO: add networkx type hints
            leaves, # TODO: add networkx type hints
            pair, # TODO: add networkx type hints
        ):
        """Takes two leaf nodes in a graph and returns the shortest path between the two.

        :param G: A graph.
        :type G: nx.Graph
        :param leaves: A list of leaf nodes.
        :type leaves: list
        :param pair: A pair of leaf nodes.
        :type pair: tuple
        :return: The shortest path between the two leaf nodes.
        :rtype: list
        """
        return nx.shortest_path(G, source=leaves[pair[0]], target=leaves[pair[1]])
    
    def get_paths(
            self, 
            G, # TODO: add networkx type hints
            leaves, # TODO: add networkx type hints
            pairs: List[Tuple], 
        ): # TODO: add networkx node type hints
        """Takes a graph, a list of leaf nodes, and a list of pairs of leaf nodes and returns a list of the shortest paths between each pair of leaf nodes.
        
        :param G: A graph.
        :type G: nx.Graph
        :param leaves: A list of leaf nodes.
        :type leaves: list
        :param pairs: A list of pairs of leaf nodes.
        :type pairs: list
        :return: A list of the shortest paths between each pair of leaf nodes.
        :rtype: list
        """
        paths = []
        for pair in pairs:
            print(pair)
            paths.append(self.get_path(G, leaves, pair))
        return paths
    
    def capture_printed_output(
            self, 
            value_to_print,
        ) -> str:
        """Takes an object and captures the printed output of the object to be returned as a string.
        
        :param value_to_print: An object to be printed.
        :type value_to_print: Any
        :return: The printed output of the object.
        :rtype: str
        """
        captured_output = ""
        with io.capture_output() as captured:
            print(value_to_print)
            captured_output = captured.stdout
        captured_output = captured_output.strip('\n')
        return captured_output
    
    def format_path(
            self, 
            path,
        ):
        """Takes a string representation of a path and formats it. leaf,node|node|node,leaf
        
        :param path: A path.
        :type path: list
        :return: The path in string format.
        :rtype: str
        """
        format = ''
        c = 0
        m = len(path)
        for i in path:
            if c == 0: 
                format += i
                format += ','
            elif c == m-1:
                format = format[:-1] 
                format += ','
                format += i
            else:
                format += i
                format += '|'
            c += 1
        format = format.replace(' ', '')
        format = format.replace('\n', '')
        return format

    def path_to_string(
        self, 
        path, # TODO: add sqlglot type hints
    ):
        desc = []
        for node in path:
            if node.key == 'identifier': 
                desc.append(self.capture_printed_output(node))
            elif node.key == 'literal':
                desc.append(self.capture_printed_output(node))
            elif node.key == 'anonymous':
                desc.append(self.capture_printed_output(node))
            else: 
                desc.append(self.capture_printed_output(node.key))
        return self.format_path(desc)
    
    def get_branches(self, query):
        ast = self.get_ast(query)
        G, Gd = self.get_graphs(ast)
        leaves = self.get_leaves(Gd)
        pairs = self.get_pairs(leaves)
        paths = self.get_paths(G, leaves, pairs)
        formatted_paths = [self.path_to_string(path) for path in paths]
        return formatted_paths

    def format_question(self, question):
        question = question.lower()
        question = question.strip()
        question = question.replace('\n', '')
        question = re.sub(f"[{re.escape(string.punctuation)}]", "", question)
        question = question.replace(' ', '|')
        return question

    def format_pair(self, question, query): 
        question = self.format_question(question)
        branches = self.get_branches(query)
        return question + ' ' + ' '.join(branches)

    def map_pairs(self, df, pair_column='pair', question_column='question', query_column='query'):    
        def create_pair(row):
            try:
                return self.format_pair(row[question_column], row[query_column])
            except:
                return None
        df[pair_column] = df.apply(create_pair, axis=1)
        return df  
    
    def to_placeholder(
            self, 
            node, # TODO: add sqlglot type hints
        ): 
        """Takes a node and replaces it with a placeholder given its type. Example: SELECT * FROM table; -> SELECT ? FROM ?;
        
        :param node: A node in an AST.
        :type node: sqlglot.Node
        :return: The node with placeholders.
        :rtype: sqlglot.Node
        """
        # takes a node and replaces it with a placeholder given its type
        if isinstance(node, sg.exp.Column): 
            return node.replace(sg.exp.Placeholder())
        if isinstance(node, sg.exp.Star): 
            return node.replace(sg.exp.Placeholder())
        if isinstance(node, sg.exp.Table):
            return node.replace(sg.exp.Placeholder())
        if isinstance(node, sg.exp.Literal):
            return node.replace(sg.exp.Placeholder())
        return node
    
    def query_to_placeholder(
            self, 
            query: str,
        ) -> str: 
        """Takes a query and replaces all nodes with placeholders.

        :param query: A SQL query.
        :type query: str
        :return: The query with placeholders.
        :rtype: str
        """
        try: # TODO: we need to decide how we want to handle errors
            return sg.parse_one(query).transform(self.to_placeholder).sql()
        except Exception as e:
            print(e)
            return None
        
    @staticmethod
    def ast_diff_dist(a, b):
        # very simple diff function, drops any steps that are not a change
        edit_steps = sg.diff(sg.parse_one(a), sg.parse_one(b))
        edit_steps = [step for step in edit_steps if not isinstance(step, Keep)]
        return len(edit_steps)
    
    @staticmethod
    def json_schema_components(db_schema):
        """A function mainly intended for interacting with schemas stored in a Spider JSON format. It extracts the number of tables, columns, and foreign keys in the schema."""
        schema_components = {
            'tables': len(db_schema['table_names']),
            'columns': len(db_schema['column_names']),
            'foreign_keys': len(db_schema['foreign_keys']),
        }
        return schema_components