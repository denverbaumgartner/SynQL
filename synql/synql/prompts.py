from packaging.version import Version

# TODO: It would be nice to move to an external source for prompts, this will allow us to easily update and version the prompts

# TODO: There are several things we can do to improve this process, we will tackle these in order of priority: 
#   1) We should have a function that takes the contents of this file and compiles a dataframe accordingly
#   2) We should have a function to ensure that the versions are compatible
#   3) We should have a function to automatically generate the joint structure

############################################
# General Variables                        # TODO: generally, this version is just for tracking and is not incredibly useful at the moment, let's get smarter here!
############################################
v1_0_0 = Version("1.0.0")
v1_1_0 = Version("1.1.0")
v1_2_0 = Version("1.2.0")   
v1_3_0 = Version("1.3.0")
v1_4_0 = Version("1.4.0")

############################################
# Seed Generation Variables                #
############################################

seed = {
    "topic": {
        "user": {
            v1_0_0: (
                "Provided here are the create statements for tables in a database. Your job is to return distinct topics of questions can be asked about the database.\n"
                "\n"
                "schema: {schema}\n"
                "\n"
                "Example Topics: \n"
                "    1: 'College Information (Questions specifically related to the colleges. Avoid questions related to players or tryouts)'\n"
                "    2: 'Player Information (Questions specifically related to players. Avoid questions related to colleges or tryouts)'\n"
                "    3: 'Tryout Information (Questions specifically related to tryouts. Avoid questions related to colleges or players)'\n"
                "\n"
                "Only respond with the topic of the question, not the question itself, formatted as the Example Topics are. Return them in a numbered list, separated by commas."
            ),
            v1_1_0: (
                "Provided here are the create statements for tables in a database. Your job is to return distinct topics of questions can be asked about the database.\n"
                "\n"
                "schema: {schema}\n"
                "\n"
                "Example Topics: \n"
                "{"
                '    "1": "College Information (Questions specifically related to the colleges. Avoid questions related to players or tryouts)"\n'
                '    "2": "Player Information (Questions specifically related to players. Avoid questions related to colleges or tryouts)"\n'
                '    "3": "Tryout Information (Questions specifically related to tryouts. Avoid questions related to colleges or players)"\n'
                "}"
                "\n"
                "Only respond with the topic of the question, not the question itself, formatted as the Example Topics are. Please return the topics as a numbered list within a JSON object."
            ),
        },
        "system": { 
            v1_0_0: (
                "Your job is to provide distinct topics that encapsulate a specific subset of questions that can be asked about a database.\n"
                "\n"
                "The goal is to generate distinct topics for the database. The topics should not overlap. Return the topics as a numbered list, seperated by commas."
            ),
            v1_1_0: (
                "Your job is to provide distinct topics that encapsulate a specific subset of questions that can be asked about a database.\n"
                "\n"
                "The goal is to generate distinct topics for the database. The topics should not overlap. Please return the topics as a numbered list within a JSON object. The list should have integer keys for each topic and the value should be the topic description itself. Ensure that the numbering starts at 1 and each entry is unique."
                "\n"
                "{"
                '"1": "Topic Description for the first topic",'
                '"2": "Topic Description for the second topic",'
                '"3": "Topic Description for the third topic"'
                "}"
            ),
        },
    },
}

############################################
# Question First Variables                 #
############################################

# Topic and Sample Questions must match on the major version to be compatible
# A major version change indicates a change in the number of topics, or a complete change in one of the topics (not just minor changes)
# A minor version change indicates a change in the number of sample questions, or a complete change in one of the sample questions (not just minor changes)
# A patch version change indicates a minor change to an existing value (e.g. a typo fix, or a minor change to a sample question)

topics = {
    "soccer_2": {
        v1_0_0: {
            1: "College Information (Questions specifically related to the colleges. Avoid questions related to players or tryouts)",
            2: "Player Information (Questions specifically related to players. Avoid questions related to colleges or tryouts)",
            3: "Tryout Information (Questions specifically related to tryouts. Avoid questions related to colleges or players)",
        },
    },
    "music_1": {
        v1_0_0: {
            1: "Genre Information (Questions specifically related to genres. Avoid questions related to artists or songs/files)",
            2: "Artist Information (Questions specifically related to artists. Avoid questions related to genres or songs/files)",
            3: "Song Information (Questions specifically related to songs. Avoid questions related to genres or artists)",
        },
    },
    "dorm_1": {
        v1_0_0: {
            1: "Student Information (Questions specifically related to the students. Avoid questions related to dorms or amenities)", 
            2: "Dormitory Information (Questions specifically related to the dorms. Avoid questions related to students or amenities)", 
            3: "Dormitory Amenities (Questions specifically related to the dorm amenities. Avoid questions related to students or dorms)", 
            4: "Student-Dormitory Allocation (Questions specifically related to how students are distributed throughout the dorms. Avoid questions related to students details or dorm amenities)", 
        },
    },
}

sample_questions = {
    "soccer_2": {
        v1_0_0: {
            1: ("Which state has the most colleges?\n"
                "What is the total number of enrolled students in each state?\n"
                "In the state of California, which college has the most students?\n"),
            2: ("What is the average amount of training hours per player?\n"
                "What is the most common name of players?\n"
                "What are the total number of players whose yes_card was true?\n"),
            3: ("What are the total number of tryouts per college?\n"
                "What are the total number of each decision type?\n"
                "Which position had the most amount of students tryout?\n"),
        },
    },
    "music_1": {
        v1_0_0: {
            1: ("What are the total number of genres?\n"
                "What is the average rating of the genres?\n"
                "Where is the jazz genre most popular?\n"),
            2: ("What are the total number of artists?\n"
                "Which country has the most arists?\n"
                "What is the count of artists by gender?\n"),
            3: ("What is the most common language of songs?\n"
                "Which country has the most songs?\n"
                "What is the average rating of songs per month?\n"),
        },
    },
    "dorm_1": {
        v1_0_0: {
            1: ("How many students are currently enrolled in the university?\n"
                "What is the most popular major for students at the university?\n"
                "What is the average age of students, broken down by major?\n"),
            2: ("What is the name of the dormitory with the most rooms?\n"
                "How much capacity does every dormitory have?\n"
                "What are the total number of dormitories, based upon the gender of the dorm?\n"),
            3: ("Which dorm has the most amenities?\n"
                "What is the most common amenity for all the dorms?\n"
                "What are the total amount of unique amenities, based on gender of the dorms?\n"),
            4: ("Group the students by their major and dormitory, what is the dorm with the highest density of Computer Science majors (major = 42)?\n"
                "What is the average age of students in each dorm?\n"
                "Which dorm has the most amount of students named Tomasz?\n"),
        },
    },
}

############################################
# Query First Variables                    # 
############################################

# Query Structure and Query Structure Type must match on the major version to be compatible

query_structures = {
    v1_0_0: {
        1: "SELECT column1, column2, ... FROM table_name WHERE condition;",
        2: "SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;",
        3: "SELECT sq.aggregated_column, FROM (SELECT FUNCTION(column1) as aggregated_column FROM table_name WHERE condition GROUP BY column2) as sq;",
    },
    v1_1_0: {
        1: "SELECT column1, column2, ... FROM table_name WHERE condition;", # cluster 0
        2: "SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;", # cluster 0 
        3: "SELECT table1.column1, table2.column1 FROM table1 JOIN table2 ON table1.column2 = table2.column2;", # cluster 2
        4: "SELECT column1 FROM table1 WHERE condition (SELECT FUNCTION(column3) FROM table1 WHERE condition);" # cluster 13
    }
    # v1_2_0: see query_templates
}

query_structure_types = {
    v1_0_0: {
        1: "Basic Data Retrieval with Filtering",
        2: "Aggregation and Grouping",
        3: "Data Retrieval with Subqueries",
    },
    v1_1_0: {
        1: "Basic Data Retrieval with Filtering",
        2: "Aggregation and Grouping",
        3: "Basic Join Statement",
        4: "Basic Retrieval with Subquery Condition",
    },
}

query_examples = {
    v1_1_0: {
        1: (
            "SELECT count(*) FROM head WHERE age > 56;\n"
            "SELECT born_state FROM head GROUP BY born_state HAVING count(*) >= 3;\n" # should we have this be an example? 
            "SELECT head_id, name FROM head WHERE name LIKE '%Ha%';\n"
        ),
        2: (
            "SELECT Status, avg(Population) FROM city GROUP BY Status;\n"
            "SELECT city, max(lat) FROM station GROUP BY city;\n"
            "SELECT city, count(*) FROM station GROUP BY city HAVING count(*) >= 3;\n" # should we have this be an example?
        ),
        3: (
            "SELECT T2.Year, T1.Official_Name FROM city AS T1 JOIN farm_competition AS T2 ON T1.City_ID = T2.Host_city_ID;\n"
            "SELECT DISTINCT T1.city FROM addresses AS T1 JOIN people_addresses AS T2 ON T1.address_id = T2.address_id;\n"
            'SELECT count(*) FROM trip AS T1 JOIN station AS T2 ON T1.end_station_id = T2.id WHERE T2.city != "San Francisco";\n' # should we have this be an example?
        ),
        4: (
            "SELECT date, zip_code FROM weather WHERE min_dew_point_f < (SELECT min(min_dew_point_f) FROM weather WHERE zip_code = 94107);\n"
            "SELECT id FROM trip WHERE duration >= (SELECT avg(duration) FROM trip WHERE zip_code = 94103);\n"
            'SELECT song_name FROM song WHERE rating < (SELECT max(rating) FROM song WHERE genre_is = "blues");\n'
        ),
    },
}

############################################
# Joint Generation Variables               #
############################################

# TODO: we can abstract this to be a function that takes the prior components and generates the joint structure
# The structure we follow is: 
# {
#     db_id: {
#         query_structure_version: {
#             1: { # maps to the number of query structures in the version
#                 topic_version: {
#                     1: # maps to the number of topics in the version
#                 },
#             },
#         },
#     },
# }

joint_query_examples = {
    # db_id
    "soccer_2": {
        # Query Structure
        v1_0_0: {
            1: {
                # Topic
                v1_0_0: {
                    1: (
                        "Query Structure: SELECT column1, column2, ... FROM table_name WHERE condition;\n"
                        "Example: SELECT college_name, enrollment FROM college WHERE state = 'California';"
                    ),
                    2: (
                        "Query Structure: SELECT column1, column2, ... FROM table_name WHERE condition;\n"
                        "Example: SELECT player_id, player_name, yes_card FROM player WHERE training_hours > 10;"
                    ),
                    3: (
                        "Query Structure: SELECT column1, column2, ... FROM table_name WHERE condition;\n"
                        "Example: SELECT college_name, player_id, decision_type FROM tryout WHERE player_position = 'Forward';"
                    ),
                },
            },
            2: {
                v1_0_0: {
                    1: (
                        "Query Structure: SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;\n"
                        "Example: SELECT state, SUM(enrollment) as state_enrollment FROM college GROUP BY state;"
                    ),
                    2: (
                        "Query Structure: SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;\n"
                        "Example: SELECT yes_card, AVG(training_hours) average_training FROM player GROUP BY yes_card;"
                    ),
                    3: (
                        "Query Structure: SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;\n"
                        "Example: SELECT player_position, COUNT(DISTINCT player_id) as player_count FROM tryout GROUP BY player_position;"
                    ),
                },
            },
            3: {
                v1_0_0: {
                    1: (
                        "Query Structure: SELECT sq.aggregated_column, FROM (SELECT FUNCTION(column1) as aggregated_column FROM table_name WHERE condition GROUP BY column2) as sq;\n",
                        "Example: SELECT sq.state_enrollment FROM (SELECT state, SUM(enrollment) as state_enrollment FROM college GROUP BY state) as sq;" 
                    ),
                    2: (
                        "Query Structure: SELECT sq.aggregated_column, FROM (SELECT FUNCTION(column1) as aggregated_column FROM table_name WHERE condition GROUP BY column2) as sq;\n",
                        "Example: SELECT sq.average_training FROM (SELECT AVG(training_hours) as average_training FROM player GROUP BY yes_card) as sq;" 
                    ),
                    3: (
                        "Query Structure: SELECT sq.aggregated_column, FROM (SELECT FUNCTION(column1) as aggregated_column FROM table_name WHERE condition GROUP BY column2) as sq;\n",
                        "Example: SELECT sq.player_count FROM (SELECT player_position, COUNT(DISTINCT player_id) as player_count FROM tryout GROUP BY player_position) as sq;" 
                    ),
                },
            },
        },
    },
    "music_1": {
        v1_0_0: {
            1: {
                v1_0_0: {
                    1: (
                        "Query Structure: SELECT column1, column2, ... FROM table_name WHERE condition;\n"
                        "Example: SELECT most_popular_in FROM genre WHERE genre_name = 'Jazz';"
                    ),
                    2: (
                        "Query Structure: SELECT column1, column2, ... FROM table_name WHERE condition;\n"
                        "Example: SELECT country FROM artist WHERE artist_name = 'The Beatles';"
                    ),
                    3: (
                        "Query Structure: SELECT column1, column2, ... FROM table_name WHERE condition;\n"
                        "Example: SELECT song_name FROM song WHERE song_language = 'English';"
                    ),
                },
            },
            2: {
                v1_0_0: {
                    1: (
                        "Query Structure: SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;\n"
                        "Example: SELECT genre_name, AVG(rating) as average_rating FROM genre GROUP BY genre_name;"
                    ),
                    2: (
                        "Query Structure: SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;\n"
                        "Example: SELECT gender, COUNT(DISTINCT artist_name) as artist_count FROM artist GROUP BY gender;"
                    ),
                    3: (
                        "Query Structure: SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;\n"
                        "Example: SELECT country, AVG(rating) as average_rating FROM song GROUP BY country;"
                    ),
                },
            },
            3: {
                v1_0_0: {
                    1: (
                        "Query Structure: SELECT sq.aggregated_column, FROM (SELECT FUNCTION(column1) as aggregated_column FROM table_name WHERE condition GROUP BY column2) as sq;\n",
                        "Example: SELECT sq.average_rating FROM (SELECT AVG(rating) as average_rating FROM song WHERE genre = 'Pop' GROUP BY genre) as sq;" 
                    ),
                    2: (
                        "Query Structure: SELECT sq.aggregated_column, FROM (SELECT FUNCTION(column1) as aggregated_column FROM table_name WHERE condition GROUP BY column2) as sq;\n",
                        "Example: SELECT sq.total_women FROM (SELECT COUNT(artist_name) as total_women FROM artist WHERE gender = 'Female') as sq;" 
                    ),
                    3: (
                        "Query Structure: SELECT sq.aggregated_column, FROM (SELECT FUNCTION(column1) as aggregated_column FROM table_name WHERE condition GROUP BY column2) as sq;\n",
                        "Example: SELECT sq.genre, sq.max_rating FROM (SELECT genre, MAX(rating) as max_rating FROM song GROUP BY genre_is) as sq;"    
                    ),
                },
            },
        },
    },
    "dorm_1": {
        v1_0_0: {
            1: {
                v1_0_0: {
                    1: (
                        "Query Structure: SELECT column1, column2, ... FROM table_name WHERE condition;\n"
                        "Example: SELECT student_id, last_name, first_name FROM student WHERE age > 25;"
                    ),
                    2: (
                        "Query Structure: SELECT column1, column2, ... FROM table_name WHERE condition;\n"
                        "Example: SELECT dorm_id, dorm_name, student_capcity FROM dorm WHERE gender = 'Male';"
                    ),
                    3: (
                        "Query Structure: SELECT column1, column2, ... FROM table_name WHERE condition;\n"
                        "Example: SELECT amenity_id FROM dorm_amenity WHERE amenity_name = 'Pool';"
                    ),
                    4: (
                        "Query Structure: SELECT column1, column2, ... FROM table_name WHERE condition;\n"
                        "Example: SELECT student_id, room_number FROM lives_in WHERE dorm_id = 100;"
                    ),
                },
            },
            2: {
                v1_0_0: {
                    1: (
                        "Query Structure: SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;\n"
                        "Example: SELECT major, AVG(age) as average_age FROM student GROUP BY major;"
                    ),
                    2: (
                        "Query Structure: SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;\n"
                        "Example: SELECT gender, SUM(student_capcity) FROM dorm GROUP BY gender;"
                    ),
                    3: (
                        "Query Structure: SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;\n"
                        "Example: SELECT dorm_id, COUNT(DISTINCT amenity_id) FROM has_amenity GROUP BY dorm_id;"
                    ),
                    4: (
                        "Query Structure: SELECT column1, FUNCTION(column2), FUNCTION(*) FROM table_name GROUP BY column1;\n"
                        "Example: SELECT room_number, AVG(COUNT(DISTINCT student_id)) FROM lives_in GROUP BY room_number;"
                    ),
                },
            },
            3: {
                v1_0_0: {
                    1: (
                        "Query Structure: SELECT sq.aggregated_column, FROM (SELECT FUNCTION(column1) as aggregated_column FROM table_name WHERE condition GROUP BY column2) as sq;\n",
                        "Example: SELECT sq.major, sq.average_age FROM (SELECT major, AVG(age) as average_age FROM student GROUP BY major) as sq;" 
                    ),
                    2: (
                        "Query Structure: SELECT sq.aggregated_column, FROM (SELECT FUNCTION(column1) as aggregated_column FROM table_name WHERE condition GROUP BY column2) as sq;\n",
                        "Example: SELECT sq.gender, sq.average_capacity FROM (SELECT gender, AVG(student_capacity) FROM dorm GROUP BY gender) as sq;"
                    ),
                    3: (
                        "Query Structure: SELECT sq.aggregated_column, FROM (SELECT FUNCTION(column1) as aggregated_column FROM table_name WHERE condition GROUP BY column2) as sq;\n",
                        "Example: SELECT sq.dorm_id, sq.amenity_count FROM (SELECT dorm_id, COUNT(DISTINCT amenity_id) as amenity_count FROM has_amenity GROUP BY dorm_id) as sq;"
                    ),
                    4: (
                        "Query Structure: SELECT sq.aggregated_column, FROM (SELECT FUNCTION(column1) as aggregated_column FROM table_name WHERE condition GROUP BY column2) as sq;\n",
                        "Example: SELECT sq.room_number, sq.average_students FROM (SELECT room_number, AVG(COUNT(DISTINCT student_id)) as average_students FROM lives_in GROUP BY room_number) as sq;"
                    ),
                },
            },
        },
    },
}


############################################
# Contexts                                 #
############################################

contexts = {
    "question": {
        v1_0_0: (
                "Your job is to create questions based on a given topic, and the SQL query that answers that question given a database schema.\n"       
                "Here are guidelines to follow:\n"
                    "1) The Question must apply to the provided schema.\n"
                    "2) The SQL Query must answer the generated Question, and be valid given the schema.\n"
                    "3) Generate questions similar to the examples provided.\n"
                    "4) Only respond with a Question and SQL Query in the desired format (Question: <Question> Query: <SQL Query>)\n"
                    "5) Do not repeat any of the questions or queries that are provided.\n" 
                "Format: Question: <Question> Query: <SQL Query>"
        ), 
        v1_1_0: (
                "Your job is to create questions based on a given topic, and the SQL query that answers that question given a database schema.\n"       
                "Here are guidelines to follow:\n"
                    "1) The Question must apply to the provided schema.\n"
                    "2) The SQL Query must answer the generated Question, and be valid given the schema.\n"
                    "3) Generate questions that are not the same as the provided questions.\n"
                    "4) Only respond with a Question and SQL Query in the desired format (Question: <Question> Query: <SQL Query>)\n"
                    "5) Do not repeat any of the questions or queries that are provided.\n" 
                "Format: Question: <Question> Query: <SQL Query>"
        ), 
        v1_2_0: (
                "Your job is to create questions based on a given topic, and the SQL query that answers that question given a database schema.\n"       
                "Here are guidelines to follow:\n"
                    "1) The Question must apply to the provided schema.\n"
                    "2) The SQL Query must answer the generated Question, and be valid given the schema.\n"
                    "3) Generate questions that do not fall into the category of topics that have been specified to avoid.\n"
                    "4) Only respond with a Question and SQL Query in the desired format (Question: <Question> Query: <SQL Query>)\n"
                    "5) Do not repeat any of the questions or queries that are provided. Do not create slight variants of provided questions.\n" 
                "Format: Question: <Question> Query: <SQL Query>"
        ), 
    },
    "query": {
        v1_0_0: (
                "Your job is to create a query based on the provided query structure and schema. The query must match the structure. After you have created the query, you will generate the question that is associated with that query. Only respond with the query and question in the format provided. The query must be a valid SQL query.\n"
                "\n"
                "Do not modify the query structure. For example:\n"
                "Query Structure: SELECT Function(Column) From Table\n"
                "Generated Query: SELECT AVG(Column) FROM Table\n"
                "\n"
                "Do not duplicate any queries. The prompt will include a list of queries that have already been generated.\n"
                "Format: Query: <SQL Query> Question: <Question>"
        ),
        v1_1_0: (
                "Your job is to create a query based on the provided query structure and schema. The query must match the structure. After you have created the query, you will generate the question that is associated with that query. Only respond with the query and question in the format provided. The query must be a valid SQL query.\n"
                "\n"
                "Do not modify the query structure. For example:\n"
                "Query Structure: SELECT ?, ?, ? FROM ?\n"
                "Generated Query: SELECT column1, column2, column3 FROM table\n"
                "\n"
                "Format: Query: <SQL Query> Question: <Question>"
        ),
    },
    "joint": {
        v1_0_0: (
                "Your job is to create a question and SQL query based on a given subject, query structure, and schema. \n"
                "\n"
                "Here are guidelines to follow:\n"
                "1) The question must match the topic of the subject.\n"
                "2) The query must answer the question.\n"
                "3) The query must be valid SQL.\n"
                "4) The query must match the query structure.\n"
                "5) The query must comply with the table schema.\n"
                "\n"
                "Do not modify the query structure. For example:\n"
                "Query Structure: SELECT column1, column2, ... FROM table_name WHERE condition;\n"
                "Example: SELECT college_name, enrollment FROM college WHERE state = 'California';\n"
                "\n"
                "Do not duplicate any questions or queries. The prompt will include a list of questions and queries that have already been generated.\n"
                "\n"
                "The response must be in the following format:\n"
                "Format: Question: <Question> Query: <SQL Query>"
        ),
        v1_1_0: (
                "Your job is to create a query based on the provided query structure and schema. The query must match the structure. After you have created the query, you will generate the question that is associated with that query. Only respond with the query and question in the format provided. The query must be a valid SQL query.\n"
                "Your job is to create a question and SQL query based on a given subject, query structure, and schema. \n"
                "\n"
                "Here are guidelines to follow:\n"
                "1) The query must match the query structure.\n"                
                "2) The query must answer the question.\n"
                "3) The query must be valid SQL.\n"
                "4) The question must match the topic of the subject.\n"
                "5) The query must comply with the table schema.\n"
                "\n"
                "Do not modify the query structure. For example:\n"
                "Query Structure: SELECT ? FROM ?;\n"
                "Example #1: SELECT * FROM Table;\n"
                "\n"
                "Do not duplicate any questions or queries. The prompt will include a list of questions and queries that have already been generated.\n"
                "\n"
                "The response must be in the following json format:\n"
                'Format: {"question": Question, "query": Query}'
        ),
        v1_2_0: (
                "Your task is to create a SQL query and an associated question based on a given subject, query structure, and schema. The query must strictly adhere to the provided query structure and be a valid SQL query. The question should be relevant to the subject and accurately answered by the query. Follow these guidelines:\n"
                "\n"
                "1) The query must match the query structure exactly.\n"
                "2) The query must answer the question.\n"
                "3) The query must be valid SQL.\n"
                "4) The question must match the topic of the subject.\n"
                "5) The query must comply with the given table schema.\n"
                "\n"
                "Do not modify the query structure. For example:\n"
                "Query Structure #1: SELECT ? FROM ?;\n"
                "Example #1: SELECT * FROM Table;\n"
                "Query Structure #2: SELECT MAX(?) FROM ?;\n"
                "Example #2: SELECT MAX(Column) FROM Table;\n"
                "Query Structure #3: SELECT ?, ?, ? FROM ?\n"
                "Generated Query #3: SELECT column1, column2, column3 FROM table\n"
                "\n"
                "Avoid duplicating any questions or queries. The prompt will include a list of questions and queries that have already been generated.\n"
                "\n"
                "The response must be in the following JSON format:\n"
                'Format: {"question": "[generated question]", "query": "[generated query]"}'
        ),
        v1_3_0: (
                "Your task is to create a SQL query and an associated question based on a given subject, query structure, and schema. The query must strictly adhere to the provided query structure and be a valid SQL query. The question should be relevant to the subject and accurately answered by the query. Follow these guidelines:\n"
                "\n"
                "1) The query must be valid and logical SQL.\n"
                "2) The query must match the query structure exactly.\n"
                "3) The question must match the topic of the subject.\n"
                "4) The query must answer the question.\n"
                "5) The query must comply with the given table schema.\n"
                "\n"
                "Do not modify the query structure. For example:\n"
                "Query Structure: SELECT ? FROM ?;\n"
                "Example: SELECT * FROM Table;\n"
                "\n"
                "Avoid duplicating any questions or queries. The prompt will include a list of questions and queries that have already been generated.\n"
                "\n"
                "The response must be in the following JSON format:\n"
                'Format: {"question": "[generated question]", "query": "[generated query]"}'
        ),
    },
}

############################################
# Prompts                                  #
############################################

prompts = {
    "question": {
        v1_0_0: (
                "Given the following topic, and schema, generate a unique question, and the query associated with that question. Make sure the question matches the topic and are similar to the example questions.\n"
                "\n"
                "Question Topic: {question_topic}\n"
                "Topic Question Examples: {question_examples}\n"
                "\n"
                "Schema: {schema}\n"
                "\n"
                "List of Questions to not Duplicate: {list_of_questions}\n"
                "List of Queries to not Duplicate: {list_of_queries}\n"
                "\n"
                "Response (Question: <Question> Query: <SQL Query>): "
        ),
        v1_1_0: (
                "Given the following topic, and schema, generate a unique question, and the query associated with that question. Make sure the question matches the topic. Make sure the questions are different from each other.\n"
                "\n"
                "Question Topic: {question_topic}\n"
                "\n"
                "Schema: {schema}\n"
                "\n"
                "List of Questions to not Duplicate or Replicate: {list_of_questions}\n"
                "List of Queries to not Duplicate: {list_of_queries}\n"
                "\n"
                "Response (Question: <Question> Query: <SQL Query>): "
        ), 
        v1_2_0 : (
                "Given the the specific topic, and schema, generate a unique question, and the query associated with that question. Make sure the question matches the topic. Make sure the questions are different from each other. You will be provided with topics that should be avoided in generation.\n"
                "\n"
                "This is the specific topic that you should focus on."
                "Question Topic: {question_topic}\n"
                "\n"
                "These are the other topics that you should avoid.\n"
                "Question Topics to Avoid: {question_topics_to_avoid}\n"
                "\n"
                "Schema: {schema}\n"
                "\n"
                "List of Questions to not Duplicate or Replicate: {list_of_questions}\n"
                "List of Queries to not Duplicate: {list_of_queries}\n"
                "\n"
                "Response (Question: <Question> Query: <SQL Query>): "
        ),
        v1_3_0 : (
                "Given the the specific topic, and schema, generate a unique question, and the query associated with that question. Make sure the question matches the topic. Make sure the questions are different from each other. You will be provided with topics that should be avoided in generation.\n"
                "\n"
                "This is the specific topic that you should focus on."
                "Question Topic: {question_topic}\n"
                "Question Topic Examples: {question_examples}\n"
                "\n"
                "These are the other topics that you should avoid."
                "Question Topics to Avoid: {question_topics_to_avoid}\n"
                "\n"
                "Schema: {schema}\n"
                "\n"
                "List of Questions to not Duplicate or Replicate: {list_of_questions}\n"
                "List of Queries to not Duplicate: {list_of_queries}\n"
                "\n"
                "Response (Question: <Question> Query: <SQL Query>): "
        ),
    },
    "query": {
        v1_0_0: (
                "Given the following query structure and schema, generate a unique query, and the question associated with that query.\n"
                "\n"
                "Query Structure: {query_structure}\n"
                "Query Type: {query_type}\n"
                "\n"
                "Schema: {schema}\n"
                "\n"
                "List of Queries to not Duplicate: {list_of_queries}\n"
                "\n"
                "Response (Query: <SQL Query> Question: <Question>): "
        ),
        v1_1_0: (
                "Given the following query structure and schema, generate a unique query, and the question associated with that query.\n"
                "\n"
                "Query Structure: {query_structure}\n"
                "Query Type: {query_type}\n"
                "Query Examples: {query_examples}\n"
                "\n"
                "Schema: {schema}\n"
                "\n"
                "List of Queries to not Duplicate: {list_of_queries}\n"
                "\n"
                "Response (Query: <SQL Query> Question: <Question>): "
        ),
        v1_2_0: (
                "Given the following query structure and schema, generate a unique query, and the question associated with that query.\n"
                "\n"
                "Query Structure: {query_structure}\n"
                "\n"
                "Schema: {schema}\n"
                "\n"
                "Response (Query: <SQL Query> Question: <Question>): "
        ),
    },
    "joint": {
        v1_0_0: (
                "Given the following topic, query structure, and schema, generate a unique question and query. Make sure the question matches the topic of the subject, and the query answers the question given the schema and query structure.\n"
                "\n"
                "The query structure must be strictly followed. The query must be valid SQL. For example:\n"
                "{query_structure_example}\n"
                "\n"
                "Question Topic: {question_subject}\n"
                "Query Structure (Type: {query_type}): {query_structure}\n"
                "Schema: {schema}\n"
                "\n"
                "List of Questions to not Duplicate: {list_of_questions}\n"
                "List of Queries to not Duplicate: {list_of_queries}\n"
                "\n"
                "Response (Question: <Question> Query: <SQL Query>): "
        ),
        v1_1_0: (
                "Given the following topic, query structure, and schema, generate a unique question and query. Only generate queries that match the query structure. Make sure the question matches the topic of the subject, and the query answers the question given the schema and query structure.\n"
                "\n"
                "The query structure must be strictly followed. The query must be valid SQL."
                "\n"
                "Question Topic: {question_subject}\n"
                "Query Structure: {query_structure}\n"
                "Schema: {schema}\n"
                "\n"
                "List of Questions to not Duplicate: {list_of_questions}\n"
                "List of Queries to not Duplicate: {list_of_queries}\n"
                "\n"
                "Response: (question: question, query: query):"
        ),
        v1_2_0: (
                "Given the following topic, query structure, and schema, generate a unique question and SQL query. The query must strictly adhere to the provided query structure and be valid SQL. The question should be relevant to the topic, and the query should accurately answer the question using the given schema.\n"
                "\n"
                "- Question Topic: {question_subject}\n"
                "- Query Structure: {query_structure}\n"
                "- Schema: {schema}\n"
                "\n"
                "Avoid duplicating any questions or queries from the following lists:\n"
                "- List of Questions to not Duplicate: {list_of_questions}\n"
                "- List of Queries to not Duplicate: {list_of_queries}\n"
                "\n"
                "Response Format: (question: [generated question], query: [generated query])"
        ),
        v1_3_0: (
                "Given the following topic, query structure, and schema, generate a unique question and SQL query. The query must strictly adhere to the provided query structure and be valid, logical, SQL. The question should be relevant to the topic, and the query should accurately answer the question using the given schema.\n"
                "Do not generate low quality questions or queries. These include queries that have irelevant structure, such as uneccessary joins. The SQL query must be valid, both in its syntax and relation to the database schema.\n"
                "\n"
                "- Question Topic: {question_subject}\n"
                "- Query Structure: {query_structure}\n"
                "- Schema: {schema}\n"
                "\n"
                "Avoid duplicating any questions or queries from the following lists:\n"
                "- List of Questions to not Duplicate: {list_of_questions}\n"
                "- List of Queries to not Duplicate: {list_of_queries}\n"
                "\n"
                "Response Format: (question: [generated question], query: [generated query])"
        ),
    },
}

############################################
# Prompt Modifiers                         #
############################################

modifiers = {
    "contexts": {
        "query": {
            v1_0_0: ( # Intended to go at the end of the prompt
                "\n"
                "You have previously failed to generate a valid query for this template: {template}. " 
                "The query you generated required {dist} edit steps to equal the template. " 
                "Follow the template structure exactly as it is given. The generated query must match the template exactly."
                "\n" 
                "The query you previously generated that was incorrect had the following structure: {gen_temp}. "
                "Make sure to utilize the correct structure this time."
            )
        }
    },
    "prompts": {
        "query": {
            v1_0_0: ( # Intended to go at the beginning of the prompt
                "Note, when requested to generate a query following the format: {template}, you generated an incorreqt query with the format: {gen_temp}. "
                "Make sure to not make the same mistake again." 
                "\n " 
            )
        },
    }
}

############################################
# Query Templates                          #
############################################

query_templates = { 
    # we set this to 1_2_0 so that our dataframes are backwards compatible with the more general query structures we previously defined
    v1_2_0: # these are collected from spider (subset by db_ids: ['movie_1', 'music_2', 'music_1', 'allergy_1', 'store_1', 'college_1', 'dorm_1', 'hospital_1', 'activity_1', 'soccer_2', 'hr_1', 'flight_1'])
    {
        '0': 'select ?, ? from ? join ? on ? = ? where ? <> ? order by ?, ?',
        '1': 'select ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ?',
        '2': 'select max(?), max(?), ? from ? join ? on ? = ? group by ? order by ?',
        '3': 'select ? from ? where ? = ?',
        '4': 'select count(?), ? from ? where ? > (select avg(?) from ?) group by ?',
        '5': 'select distinct ? from ? join ? on ? = ? except select ? from ? join ? on ? = ? where ? = ?',
        '6': 'select count(distinct ?), ? from ? group by ?',
        '7': 'select ? from ? group by ? order by count(?) desc limit ?',
        '8': 'select ? from ? where ? = ? union select ? from ? where ? > ?',
        '9': 'select avg(?), ? from ? group by ?',
        '10': 'select ?, ? from ? order by ?',
        '11': 'select ? from ? join ? on ? = ? group by ? having count(?) >= ?',
        '12': 'select ?, count(?) from ? group by ? order by count(?) desc limit ?',
        '13': 'select ?, ? from ? join ? on ? = ? group by ? order by count(?) limit ?',
        '14': 'select ?, ? from ? join ? on ? = ? group by ? order by count(?) desc limit ?',
        '15': 'select count(distinct ?) from ?',
        '16': 'select distinct ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '17': 'select ? from ? where ? like ?',
        '18': 'select count(?), ? from ? group by ? order by count(?) desc',
        '19': 'select ?, count(?) from ? group by ?',
        '20': 'select ?, ? from ? where ? = ?',
        '21': 'select sum(?), ? from ? group by ?',
        '22': 'select ? from ? join ? on ? = ? where ? = ? intersect select ? from ? join ? on ? = ? where ? = ?',
        '23': 'select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ?',
        '24': 'select ?, ?, count(?) from ? join ? on ? = ? group by ? order by count(?) desc limit ?',
        '25': 'select ? from ? join ? on ? = ? where ? = (select ? from ? order by ? desc limit ?)',
        '26': 'select count(?) from ? join ? on ? = ? where ? = ?',
        '27': 'select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? or ? = ?',
        '28': 'select ?, ?, ? from ? where ? in (select ? from ? where ? like ?)',
        '29': 'select ? from ? join ? on ? = ? where ? = ? and ? = ?',
        '30': 'select count(?), ? from ? join ? on ? = ? join ? on ? = ? group by ?',
        '31': 'select ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '32': 'select distinct ? from ? join ? on ? = ?',
        '33': 'select count(?) from ? where not ? in (select ? from ? join ? on ? = ? where ? = ?)',
        '34': 'select ?, ?, ? from ? where ? = ?',
        '35': 'select distinct ? from ? join ? on ? = ? where ? = ?',
        '36': 'select ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ? order by ?',
        '37': 'select count(?) from ?',
        '38': 'select distinct ? from ? join ? on ? = ? join ? on ? = ? where ? = ? or ? = ?',
        '39': 'select distinct ? from ? where ? < (select max(?) from ?)',
        '40': 'select ? from ? join ? on ? = ? group by ? having count(?) > ?',
        '41': 'select ?, ? from ? where ? = ? or ? = ?',
        '42': 'select count(distinct ?) from ? join ? on ? = ? where ? = ?',
        '43': 'select ? from ? except select ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '44': 'select ? from ? join ? on ? = ? group by ? order by count(?) desc limit ?',
        '45': 'select ? from ? order by ? desc limit ?',
        '46': 'select count(?) from ? where ? > ?',
        '47': 'select ? from ? join ? on ? = ? join ? on ? = ? group by ? order by sum(?) desc limit ?',
        '48': 'select ?, ? from ? join ? on ? = ? order by ? desc limit ?',
        '49': 'select ? from ? join ? on ? = ? order by ? limit ?',
        '50': 'select ?, ? from ? join ? on ? = ? where ? = ?',
        '51': 'select ? from ? join ? on ? = ? where ? = ? or ? = ?',
        '52': 'select distinct ? from ?',
        '53': 'select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ?',
        '54': 'select sum(?) from ? join ? on ? = ? where ? = ? and ? = ?',
        '55': 'select avg(?), avg(?) from ? where ? = ?',
        '56': 'select ? from ? where ? > (select avg(?) from ? where ? = ?)',
        '57': 'select count(?) from ? where ? = ? and ? = ?',
        '58': 'select min(?), ? from ? group by ?',
        '59': 'select ? from ? except select ? from ?',
        '60': 'select ? from ? except select ? from ? join ? on ? = ?',
        '61': 'select ? from ? where ? <> ?',
        '62': 'select count(distinct ?) from ? where ? > (select avg(?) from ?)',
        '63': 'select ?, ? from ? where ? < (select avg(?) from ?)',
        '64': 'select count(?) from ? where ? = ? and ? < ?',
        '65': 'select ? from ? join ? on ? = ? where ? = ?',
        '66': 'select ? from ? where ? = ? and ? = ?',
        '67': 'select ?, avg(?) from ? join ? on ? = ? group by ?',
        '68': 'select ?, ? from ? join ? on ? = ? where ? in (select ? from ? join ? on ? = ? where ? = ?)',
        '69': 'select ? from ? join ? on ? = ? where ? like ?',
        '70': 'select ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '71': 'select count(?) from ? where ? = ?',
        '72': 'select count(distinct ?) from ? where ? < (select avg(?) from ?)',
        '73': 'select count(?), ? from ? where ? = ? group by ?',
        '74': 'select ?, count(?) from ? join ? on ? = ? group by ?',
        '75': 'select sum(?) from ? where not ? in (select ? from ? where ? = ?)',
        '76': 'select count(?) from ? where ? = ? or ? = ?',
        '77': 'select count(?), ? from ? join ? on ? = ? join ? on ? = ? where ? > ? group by ?',
        '78': 'select min(?), avg(?), max(?) from ?',
        '79': 'select ? from ? join ? on ? = ? where ? >= ?',
        '80': 'select ?, ?, ?, ?, ? from ? where not ? like ?',
        '81': 'select ? from ? join ? on ? = ? order by ?',
        '82': 'select count(?), ? from ? group by ?',
        '83': 'select ?, count(?), sum(?) from ? where ? = ?',
        '84': 'select ?, ?, ? from ? where ? like ?',
        '85': 'select max(?), min(?) from ?',
        '86': 'select distinct ? from ? join ? on ? = ? where ? >= ? order by ?',
        '87': 'select ? from ? where not ? like ?',
        '88': 'select count(distinct ?) from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '89': 'select ? from ? order by ? limit ?',
        '90': 'select ? from ? where not ? in (select ? from ? where ? between ? and ?)',
        '91': 'select ?, ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ?',
        '92': 'select ?, ? from ? join ? on ? = ? where not ? in (select ? from ? join ? on ? = ? where ? = ?)',
        '93': 'select ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? <> ?',
        '94': 'select ? from ? where not ? in (select ? from ?)',
        '95': 'select ?, ? from ? join ? on ? = ? where ? = ? group by ? order by count(?) desc limit ?',
        '96': 'select ?, ? from ? order by ? desc limit ?',
        '97': 'select count(?) from ? join ? on ? = ? where ? = ? and ? = ?',
        '98': 'select ? from ? order by ?',
        '99': 'select count(?) from ? where ? < ?',
        '100': 'select avg(?) from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '101': 'select ? from ? where ? = ? and ? = ? union select ? from ? where ? = ? and ? < ?',
        '102': 'select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? except select ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '103': 'select ?, ? from ? order by ? limit ?',
        '104': 'select ?, ? from ?',
        '105': 'select ? from ? where ? between ? and ?',
        '106': 'select ?, ?, ? from ? join ? on ? = ? where ? = ? order by ?',
        '107': 'select ?, ?, ?, min(?) from ? join ? on ? = ? group by ?',
        '108': 'select ?, ? from ? join ? on ? = ? where ? like ?',
        '109': 'select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '110': 'select ? from ? where ? > ?',
        '111': 'select ?, ? from ? join ? on ? = ? where ? = ? and ? = ?',
        '112': 'select count(distinct ?), ? from ? group by ? having count(distinct ?) < ?',
        '113': 'select ? from ? where ? < ?',
        '114': 'select distinct ? from ? where ? > (select min(?) from ? where ? = ?)',
        '115': 'select ? from ? group by ? order by count(?) limit ?',
        '116': 'select avg(?) from ?',
        '117': 'select distinct ? from ? group by ?, ? having count(?) >= ?',
        '118': 'select ? from ?',
        '119': 'select ? from ? group by ? having count(?) >= ?',
        '120': 'select ?, ?, ? from ? join ? on ? = ? join ? on ? = ? where ? like ?',
        '121': 'select count(?), ? from ? join ? on ? = ? and ? = ? group by ?',
        '122': 'select ? from ? where ? = ? and ? between ? and ?',
        '123': 'select min(?), ? from ? join ? on ? = ? group by ?',
        '124': 'select sum(?) from ?',
        '125': 'select ? from ? group by ? having count(?) = ?',
        '126': 'select count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ?',
        '127': 'select ?, ?, ? from ? order by ? desc limit ?',
        '128': 'select count(?) from ? where ? between ? and ?',
        '129': 'select ?, avg(?) from ? join ? on ? = ? group by ? order by avg(?) limit ?',
        '130': 'select distinct ? from ? order by ?',
        '131': 'select ?, ?, count(?) from ? group by ?, ?',
        '132': 'select ? from ? where ? > (select max(?) from ? where ? = ?)',
        '133': 'select ?, ? from ? join ? on ? = ? order by ? limit ?',
        '134': 'select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? except select ? from ? join ? on ? = ?',
        '135': 'select ?, ?, ? from ? where ? > ? order by ? desc limit ?',
        '136': 'select distinct ?, ? from ? join ? on ? = ? where ? > ?',
        '137': 'select ?, avg(?) from ? where ? <> ? group by ?',
        '138': 'select ? from ? union select ? from ?',
        '139': 'select ?, ? from ? where ? like ?',
        '140': 'select ? from ? where ? = (select max(?) from ?)',
        '141': 'select ?, ? from ? where ? = ? and ? = ?',
        '142': 'select ?, ? from ? where ? > ? and ? = ?',
        '143': 'select ? from ? where ? like ? order by ?',
        '144': 'select distinct ?, ? from ? join ? on ? = ? where ? = ?',
        '145': 'select max(?), min(?), avg(?) from ?',
        '146': 'select ?, ?, ?, ?, ? from ? where not ? like ? order by ?',
        '147': 'select ? from ? where ? = ? order by ? desc limit ?',
        '148': 'select ?, ? from ? where ? < ?',
        '149': 'select ?, ?, ? from ? where ? in (select min(?) from ? group by ?)',
        '150': 'select ? from ? where ? = ? and ? between ? and ? and ? = ?',
        '151': 'select ? from ? where ? < ? intersect select ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '152': 'select count(?), ? from ? join ? on ? = ? group by ?',
        '153': 'select avg(?) from ? where ? in (select ? from ? join ? on ? = ? where ? = ? intersect select ? from ? join ? on ? = ? where ? = ?)',
        '154': 'select ?, ?, sum(?) from ? join ? on ? = ? group by ? order by sum(?) desc limit ?',
        '155': 'select ? from ? group by ? having count(?) > ?',
        '156': 'select avg(?), max(?), min(?) from ?',
        '157': 'select ? from ? join ? on ? = ? where ? = ? group by ? order by count(?) desc limit ?',
        '158': 'select avg(?) from ? join ? on ? = ? join ? on ? = ? where ? = (select max(?) from ?)',
        '159': 'select ?, ? from ? join ? on ? = ?',
        '160': 'select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '161': 'select ? from ? join ? on ? = ? join ? on ? = ? group by ? order by count(?) desc limit ?',
        '162': 'select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? order by ?',
        '163': 'select avg(?), ? from ? join ? on ? = ? where ? = (select min(?) from ?)',
        '164': 'select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? like ?',
        '165': 'select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? intersect select ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '166': 'select ?, ?, ?, ?, max(?) from ? group by ?',
        '167': 'select ?, ? from ? where ? <> (select ? from ? group by ? order by count(?) desc limit ?)',
        '168': 'select ? from ? except select ? from ? join ? on ? = ? where ? = ?',
        '169': 'select ? from ? where ? = ? except select distinct ? from ? join ? on ? = ? join ? on ? = ? where ? = ? or ? = ?',
        '170': 'select ? from ? where ? > ? union select ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '171': 'select ? from ? join ? on ? = ? join ? on ? = ? where ? > ? group by ? order by count(?) desc limit ?',
        '172': 'select ? from ? order by ? asc limit ?',
        '173': 'select ? from ? join ? on ? = ? group by ? order by count(?) limit ?',
        '174': 'select ?, ? from ? where ? < (select min(?) from ? where ? = ?)',
        '175': 'select ?, ?, ?, ? from ? where ? > (select max(?) from ? where ? = ?)',
        '176': 'select count(?), avg(?), ? from ? where ? = ? group by ?',
        '177': 'select distinct ? from ? where ? = ?',
        '178': 'select ? from ? where ? - ? > ? group by ? having count(?) >= ?',
        '179': 'select ?, count(?) from ? where ? = ? group by ? order by count(?) desc limit ?',
        '180': 'select ?, ? from ? where ? between ? and ?',
        '181': 'select ? from ? where ? = ? intersect select ? from ? where ? = ?',
        '182': 'select ? from ? join ? on ? = ? where ? in (select ? from ? join ? on ? = ? join ? on ? = ? group by ? order by count(?) desc limit ?)',
        '183': 'select ?, ? from ? where ? in (select ? from ? where ? = ? intersect select ? from ? where ? = ?)',
        '184': 'select ?, ?, ?, ? from ? where ? > (select avg(?) from ?) and ? in (select ? from ? where ? like ?)',
        '185': 'select ? from ? where ? < ? and ? = ? union select ? from ? where ? > ? and ? = ?',
        '186': 'select distinct ? from ? except select ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '187': 'select ? from ? join ? on ? = ? order by ? desc limit ?',
        '188': 'select avg(?), max(?) from ? join ? on ? = ? where ? = ?',
        '189': 'select ?, ? from ? order by ? asc limit ?',
        '190': 'select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? intersect select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '191': 'select ?, ?, min(?) from ? group by ?',
        '192': 'select ? from ? where ? = ? or ? = ?',
        '193': 'select ? from ? where ? = ? group by ? having count(?) >= ?',
        '194': 'select count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '195': 'select ?, ?, ? from ? where ? = ? order by ?',
        '196': 'select ?, ? from ? join ? on ? = ? where ? > ? group by ? having count(?) >= ?',
        '197': 'select ? from ? where ? = ? except select ? from ? join ? on ? = ?',
        '198': 'select ?, avg(?) from ? where not ? in (select ? from ? join ? on ? = ? where ? = ?) group by ?',
        '199': 'select ?, ? from ? join ? on ? = ? where ? <> ?',
        '200': 'select ? from ? join ? on ? = ? join ? on ? = ? order by ? desc limit ?',
        '201': 'select avg(?) from ? join ? on ? = ? where ? = ?',
        '202': 'select ? from ? join ? on ? = ? where ? > ? group by ? order by count(?) >= ?',
        '203': 'select ?, ? from ? where ? in (select ? from ? where ? = ? except select ? from ? where ? = ?)',
        '204': 'select min(?), min(?), ? from ? join ? on ? = ? group by ? order by ?',
        '205': 'select ? from ? intersect select ? from ?',
        '206': 'select max(?), min(?) from ? join ? on ? = ? where ? like ?',
        '207': 'select ? from ? where ? <> ? group by ? having count(?) = ?',
        '208': 'select max(?), ? from ? join ? on ? = ? where ? = (select max(?) from ?)',
        '209': 'select count(distinct ?) from ? where ? = ?',
        '210': 'select avg(?), max(?) from ?',
        '211': 'select ?, ? from ? where not ? in (select ? from ? where ? = ?)',
        '212': 'select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '213': 'select ? from ? group by ? having avg(?) > ?',
        '214': 'select ? from ? where ? = ? order by ?',
        '215': 'select ? from ? where ? between ? and ? and ? <> ? or ? <> ?',
        '216': 'select ?, ? from ? where not ? in (select ? from ? join ? on ? = ? where ? = ?)',
        '217': 'select ?, ?, ? from ? order by ?',
        '218': 'select count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '219': 'select sum(?), ? from ? join ? on ? = ? group by ?',
        '220': 'select ? from ? join ? on ? = ? where ? = ? intersect select ? from ? where ? < ?',
        '221': 'select ? from ? join ? on ? = ? join ? on ? = ? where ? > ?',
        '222': 'select count(distinct ?), count(distinct ?) from ?',
        '223': 'select ? from ? join ? on ? = ? where ? between ? and ?',
        '224': 'select ?, avg(?) from ? join ? on ? = ? group by ? order by avg(?) desc limit ?',
        '225': 'select ?, ? from ? where ? > ? or ? < ?',
        '226': 'select distinct ? from ? where ? = ? except select distinct ? from ? where ? > ?',
        '227': 'select ? from ? where ? < (select max(?) from ? where ? = ?)',
        '228': 'select ?, ?, ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ?',
        '229': 'select count(?) from ? where ? > ? and not ? in (select ? from ? join ? on ? = ? where ? = ? or ? = ?)',
        '230': 'select ? from ? except select ? from ? where ? = ?',
        '231': 'select ?, sum(?) from ? group by ? having count(?) >= ?',
        '232': 'select ?, ?, ?, max(?) from ? join ? on ? = ? where ? <> ? group by ?',
        '233': 'select ?, ?, ? from ?',
        '234': 'select ? from ? where ? > ? order by ?',
        '235': 'select ? from ? group by ? order by count(?) asc limit ?',
        '236': 'select ? from ? where ? like ? or ? like ? order by ? desc',
        '237': 'select max(?), ? from ? join ? on ? = ? where ? > ? group by ?',
        '238': 'select ?, count(?) from ? where ? = ? group by ?',
        '239': 'select ?, ? from ? join ? on ? = ? join ? on ? = ? group by ? order by count(?) limit ?',
        '240': 'select distinct ? from ? join ? on ? = ? join ? on ? = ? where ? = ? or ? > ?',
        '241': 'select distinct ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '242': 'select count(?) from ? join ? on ? = ? where ? = ? and ? = ? or ? = ?',
        '243': 'select ?, ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '244': 'select count(?) from (select ? from ? where ? = ? intersect select ? from ? where ? = ?)',
        '245': 'select ?, count(?) from ? join ? on ? = ? where ? = ? group by ? having count(?) >= ?',
        '246': 'select ?, ? - ? from ? where ? between ? and ?',
        '247': 'select count(?), ? from ? group by ? having count(?) > ?',
        '248': 'select distinct ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '249': 'select count(?) from ? join ? on ? = ? where ? = ? or ? = ?',
        '250': 'select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ? and ? = ?',
        '251': 'select ?, max(?) from ? group by ?',
        '252': 'select sum(?) from ? where ? = ? and ? = ?',
        '253': 'select distinct ? from ? where ? like ?',
        '254': 'select count(?), ? from ? group by ? having count(?) >= ?',
        '255': 'select avg(?) from ? where ? = ?',
        '256': 'select avg(?), sum(?) from ? where ? = ?',
        '257': 'select distinct ?, ? from ? join ? on ? = ? where ? < ?',
        '258': 'select distinct ?, ? from ? join ? on ? = ? where ? = ? or ? = ?',
        '259': 'select count(?), avg(?), ? from ? group by ?',
        '260': 'select ?, ? from ? join ? on ? = ? group by ? having count(?) > ?',
        '261': 'select ? from ? where ? > ? group by ? order by count(?) desc limit ?',
        '262': 'select ?, ? from ? where ? > (select ? from ? where ? = ?)',
        '263': 'select ? from ? where ? > ? except select ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '264': 'select ?, count(?) from ? join ? on ? = ? group by ? order by count(?) desc limit ?',
        '265': 'select ?, ?, ? from ? where ? < ?',
        '266': 'select ?, ? from ? where ? > ?',
        '267': 'select ?, ?, ? from ? where ? = (select ? from ? where ? = ?) and ? <> ?',
        '268': 'select avg(?) from ? where ? = ? and ? = ?',
        '269': 'select ? from ? join ? on ? = ?',
        '270': 'select distinct ?, ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ?',
        '271': 'select ? from ? where ? = (select min(?) from ?)',
        '272': 'select ? from ? where ? = ? or ? < ?',
        '273': 'select ?, ?, ? from ? join ? on ? = ?',
        '274': 'select ? from ? where ? > (select avg(?) from ?)',
        '275': 'select count(?), sum(?), ? from ? group by ?',
        '276': 'select ? from ? where ? = ? intersect select ? from ? join ? on ? = ? where ? = ?',
        '277': 'select ?, ? from ? where ? <> ? order by ?',
        '278': 'select ?, ?, ? from ? where ? = ? and ? = ?',
        '279': 'select count(?) from (select ? from ? join ? on ? = ? where ? = ? except select ? from ? join ? on ? = ? where ? = ?)',
        '280': 'select ?, ?, ? from ? where ? = (select ? from ? where ? = ?)',
        '281': 'select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ?',
        '282': 'select ? from ? join ? on ? = ? where ? = ? except select ? from ? join ? on ? = ? where ? = ?',
        '283': 'select ? from ? where ? = ? except select ? from ? where ? = ?',
        '284': 'select ?, ?, count(?), ? from ? join ? on ? = ? group by ?',
        '285': 'select ? from ? where ? between (select min(?) from ?) and ?',
        '286': 'select ?, ?, ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ?',
        '287': 'select avg(?), ? from ? join ? on ? = ? join ? on ? = ? group by ?',
        '288': 'select max(?), avg(?), min(?), ? from ? group by ?',
        '289': 'select ?, ?, ?, ? from ? join ? on ? = ? join ? on ? = ? order by ?, ?, ?',
        '290': 'select ?, ? from ? where ? = (select ? from ? where ? = ?)',
        '291': 'select ?, ? from ? join ? on ? = ? where ? = ? or ? = ?',
        '292': 'select ? from ? where ? = ? order by ? desc',
        '293': 'select count(?) from ? where ? = ? and ? in (select ? from ? join ? on ? = ? where ? = ?)',
        '294': 'select ?, sum(?) from ? group by ? order by sum(?) desc limit ?',
        '295': 'select count(?), ? from ? join ? on ? = ? where ? > ? group by ?',
        '296': 'select ? from ? join ? on ? = ? where ? > ?',
        '297': 'select count(?) from ? where ? like ?',
        '298': 'select ?, ?, ?, ?, ? from ? join ? on ? = ? join ? on ? = ?',
        '299': 'select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? group by ? order by count(?) desc limit ?',
        '300': 'select ? from ? join ? on ? = ? group by ? having count(?) = ?',
        '301': 'select ?, ? from ? order by ? desc',
        '302': 'select ? from ? where ? > (select max(?) from ? where ? < ?)',
        '303': 'select ?, avg(?) from ? group by ? having count(?) >= ?',
        '304': 'select avg(?), max(?), ? from ? group by ?',
        '305': 'select ?, ? from ? join ? on ? = ? order by ?',
        '306': 'select ? from ? where ? = ? intersect select ? from ? where ? < ?',
        '307': 'select ? from ? where ? < (select min(?) from ? where ? = ?)',
        '308': 'select ? from ? join ? on ? = ? where ? like ? union select ? from ? where ? = ?',
        '309': 'select ?, ? from ? join ? on ? = ? where ? > (select avg(?) from ? join ? on ? = ? where ? = ?)'
    },
    v1_3_0: # these are sourced from Wang et al. 2021: https://arxiv.org/abs/2104.05827 # TODO: direclty link to the dataset used to extract these queries
    {
        "0": "select avg(?), count(count(?)) from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where avg(?) = ?",
        "1": "select ? from ?",
        "2": "select ?, ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? group by ?",
        "3": "select avg(?) from ?",
        "4": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? group by ?",
        "5": "select avg(?) from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "6": "select ? from ? where ? > ?",
        "7": "select ?, ? from ?",
        "8": "select ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?",
        "9": "select max(avg(?)) from ? where count(?) = ?",
        "10": "select ?, count(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?",
        "11": "select ?, ? from ? join ? on ? = ? where ? > ?",
        "12": "select min(?) from ? intersect select ? from ?",
        "13": "select ?, ? from ? join ? on ? = ? where count(?) = ?",
        "14": "select avg(?), ?, ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where count(?) = (select ?, avg(?), ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?)",
        "15": "select ?, count(?) from ? join ? on ? = ?",
        "16": "select ? from ?, ? join ? on ? = ? and ? = ? where count(?) = ? group by ? order by count(?) desc",
        "17": "select ?, avg(?) from ?",
        "18": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "19": "select count(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "20": "select ? from ? where ? = ?",
        "21": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ? and count(?) > ?",
        "22": "select ?, min(max(?)), ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? and ? = ?",
        "23": "select count(?) from ?, ? join ? on ? = ? and ? = ? where ? = ? intersect select ?, count(?) from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "24": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = ? except select count(?) from ?",
        "25": "select distinct ? from ?, ? join ? on ? = ? and ? = ? where ? between ? and ?",
        "26": "select ?, avg(distinct ?) from ? join ? on ? = ?",
        "27": "select avg(?) from ? group by count(?)",
        "28": "select ?, count(?) from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "29": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "30": "select ?, ? from ? where ? = ?",
        "31": "select count(?) from ?",
        "32": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = ? group by ?",
        "33": "select count(?) from ? join ? on ? = ? where ? > ?",
        "34": "select max(min(?)) from ? where ? = ?",
        "35": "select count(?) from ?, ? join ? on ? = ? and ? = ? where ? = (select min(?), count(?) from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? > ?)",
        "36": "select ?, ? from ? join ? on ? = ? where ? = ?",
        "37": "select ?, ?, ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ?",
        "38": "select ?, ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where max(?) > (select ? from ? order by ? desc limit ?) group by ?",
        "39": "select ? from ? join ? on ? = ? group by count(?)",
        "40": "select ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? group by ? order by ? asc",
        "41": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "42": "select count(?) from ? where ? = ?",
        "43": "select avg(?), avg(?) from ? where count(?) > ?",
        "44": "select ? from ? join ? on ? = ? where ? = (select ? from ?)",
        "45": "select ? from ? join ? on ? = ? where ? = ?",
        "46": "select ? from ? join ? on ? = ? where avg(?) > ?",
        "47": "select ? from ? join ? on ? = ? where ? > ?",
        "48": "select ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where count(?) > ?",
        "49": "select ?, avg(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "50": "select avg(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where avg(?) = ? and ? = ?",
        "51": "select ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? > ? group by ?",
        "52": "select count(?) from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ? group by ?",
        "53": "select ?, count(?) from ? where ? between ? and ?",
        "54": "select ? from ?, ? join ? on ? = ? and ? = ? where avg(?) = ?",
        "55": "select count(?), ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?",
        "56": "select avg(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "57": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "58": "select ? from ? join ? on ? = ? where ? > (select ?, ? from ?)",
        "59": "select ? from ? where ? between ? and ?",
        "60": "select ?, count(?), ? from ? except select ? from ?",
        "61": "select count(?), ? from ? join ? on ? = ?",
        "62": "select ?, count(?) from ? join ? on ? = ? where ? = ?",
        "63": "select ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "64": "select ? from ? join ? on ? = ? join ? on ? = ? where ? = (select ?, count(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?)",
        "65": "select count(?), ? from ? where ? between ? and ?",
        "66": "select ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "67": "select ? from ? where ? >= ?",
        "68": "select ?, ?, count(count(?)) from ? join ? on ? = ? where ? = ?",
        "69": "select count(?), ? from ? where ? > ?",
        "70": "select ?, ? from ?, ? join ? on ? = ? and ? = ? group by ? having ? = ?",
        "71": "select ?, ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "72": "select ? from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "73": "select ?, ? from ?, ? join ? on ? = ? and ? = ?",
        "74": "select count(?) from ? join ? on ? = ? where avg(?) > ?",
        "75": "select ?, max(?) from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "76": "select ? from ? where ? = ? except select ?, ? from ?, ? join ? on ? = ? and ? = ?",
        "77": "select count(avg(?)), ? from ? join ? on ? = ?",
        "78": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? > ? and ? = (select ? from ? where ? = ?)",
        "79": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? > ? group by avg(?)",
        "80": "select ?, ? from ? where count(?) = ?",
        "81": "select ?, ? from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "82": "select ? from ?, ? join ? on ? = ? and ? = ? where ? > ? intersect select ? from ? where ? > ?",
        "83": "select ? from ?, ? join ? on ? = ? and ? = ? where ? between ? and ?",
        "84": "select count(?), count(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "85": "select distinct ? from ?",
        "86": "select ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where avg(?) > ?",
        "87": "select ? from ? where avg(?) between ? and ?",
        "88": "select distinct ? from ? where ? > ?",
        "89": "select ?, ? from ? except select ? from ? where ? = ?",
        "90": "select ? from ? intersect select ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and count(?) > ?",
        "91": "select count(?), ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?",
        "92": "select count(?) from ? join ? on ? = ? where ? = ?",
        "93": "select ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "94": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "95": "select count(?), ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? > ?",
        "96": "select avg(?), ? from ? join ? on ? = ? where ? = ?",
        "97": "select count(avg(?)), avg(?) from ? where ? > ?",
        "98": "select ? from ? group by ?",
        "99": "select count(?), ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? and ? = ? where ? > ? group by ?",
        "100": "select min(?), count(?) from ?",
        "101": "select count(?), max(?) from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? > (select ? from ? join ? on ? = ? group by count(?))",
        "102": "select count(?), ? from ?",
        "103": "select ?, ? from ? where ? between ? and ?",
        "104": "select min(?), ? from ? join ? on ? = ?",
        "105": "select ?, ?, ? from ? join ? on ? = ? where avg(?) > ?",
        "106": "select ? from ? where count(?) > ?",
        "107": "select max(?), ? from ?",
        "108": "select ?, ? from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "109": "select ?, count(?), ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where count(?) = ?",
        "110": "select ? from ? where count(?) = ? group by ?",
        "111": "select count(?) from ? join ? on ? = ? where max(?) > ?",
        "112": "select ?, count(?) from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "113": "select ?, ? from ? where ? = ? except select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and ? between ? and ?",
        "114": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? > ? and ? = ?",
        "115": "select ?, ?, ? from ?",
        "116": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? between ? and ?",
        "117": "select max(?) from ? join ? on ? = ? where ? > ?",
        "118": "select avg(count(?)) from ?",
        "119": "select count(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ? intersect select ? from ? join ? on ? = ? where ? = ?",
        "120": "select ?, ? from ? join ? on ? = ?",
        "121": "select count(?), ? from ?, ? join ? on ? = ? and ? = ?",
        "122": "select ?, ?, ? from ? join ? on ? = ? and ? = ? and ? = ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ?",
        "123": "select ?, count(?), ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ?",
        "124": "select count(?), ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "125": "select ?, ?, ? from ?, ? join ? on ? = ? and ? = ?",
        "126": "select distinct ? from ? where ? = ?",
        "127": "select count(?) from ? join ? on ? = ? where count(?) > ?",
        "128": "select ?, ?, count(?) from ? join ? on ? = ? where count(?) = ?",
        "129": "select count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "130": "select ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "131": "select ?, ? from ? where ? in (select count(distinct ?) from ?)",
        "132": "select distinct ? from ? join ? on ? = ? where ? > (select ? from ? group by)",
        "133": "select max(?) from ?",
        "134": "select ? from ? join ? on ? = ? join ? on ? = ? where ? in (select ? from ? join ? on ? = ? where ? = ?)",
        "135": "select distinct count(?) from ?",
        "136": "select ?, ? from ? where ? > ?",
        "137": "select max(?) from ? where max(?) = ?",
        "138": "select count(count(?)), ? from ? join ? on ? = ? join ? on ? = ?",
        "139": "select avg(?) from ? join ? on ? = ? where ? = ?",
        "140": "select distinct ?, count(count(?)) from ? join ? on ? = ? join ? on ? = ?",
        "141": "select ?, count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "142": "select count(?) from ? join ? on ? = ? join ? on ? = ? where count(?) in \"milk\"",
        "143": "select count(?) from ? join ? on ? = ? where ? in \"food\"",
        "144": "select ? from ? join ? on ? = ? where ? >= ?",
        "145": "select ? from ? join ? on ? = ? join ? on ? = ? where count(?) = ?",
        "146": "select ?, min(?) from ? join ? on ? = ? join ? on ? = ?",
        "147": "select distinct ?, ?, ? from ?",
        "148": "select count(?) from ? join ? on ? = ? where ? in \"soy\"",
        "149": "select distinct ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "150": "select count(?) from ? group by ?",
        "151": "select ? from ? where count(?) = ?",
        "152": "select count(distinct ?), ? from ? join ? on ? = ? where ? = ?",
        "153": "select distinct ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "154": "select count(count(?)), ? from ? join ? on ? = ? where not ? = ? intersect select ? from ? join ? on ? = ? where ? = ?",
        "155": "select ? from ? join ? on ? = ? where count(?) = ?",
        "156": "select count(?) from ? where count(?) = (select count(?) from ? where ? = ?)",
        "157": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? in \"eggs\"",
        "158": "select ? from ? join ? on ? = ? where ? = (select count(?) from ? join ? on ? = ? where ? = (select ? from ? where not ? = ?))",
        "159": "select ? from ? except select ? from ? where ? in ?",
        "160": "select ?, ? from ? join ? on ? = ? join ? on ? = ? except select ? from ? join ? on ? = ? where count(?) in \"hkg\"",
        "161": "select ?, count(?) from ? join ? on ? = ? join ? on ? = ?",
        "162": "select ? from ? where count(?) = (select count(?) from ?)",
        "163": "select count(count(?)), ? from ?",
        "164": "select ? from ? join ? on ? = ? join ? on ? = ? where ? in \"eggs\"",
        "165": "select count(?) from ? where ? = (select ? from ?)",
        "166": "select ?, ? from ? join ? on ? = ? where not ? = ?",
        "167": "select ?, count(?) from ? join ? on ? = ? where ? in \"animal\" and ? = ? and not ? = ? group by ?",
        "168": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? group by count(?) order by ? desc limit ?",
        "169": "select ? from ? join ? on ? = ? join ? on ? = ? where ? = (select count(?) from ?) group by ?",
        "170": "select max(?) from ? where ? = ?",
        "171": "select max(?), ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "172": "select count(?) from ? join ? on ? = ? where avg(?) = ? group by min(?)",
        "173": "select ? from ? join ? on ? = ? join ? on ? = ? where ? in (select count(?) from ? join ? on ? = ? join ? on ? = ? where count(?) = ? group by)",
        "174": "select count(?) from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? group by ? order by ? asc limit ?",
        "175": "select count(count(?)) from ?",
        "176": "select ? from ? intersect select ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "177": "select count(?), ? from ? where ? = ?",
        "178": "select max(?) from ? join ? on ? = ? join ? on ? = ? where count(?) = ? group by count(?)",
        "179": "select count(distinct ?), ? from ?",
        "180": "select count(?) from ? join ? on ? = ? where max(?) = ?",
        "181": "select count(?), ?, count(?) from ?",
        "182": "select ? from ? join ? on ? = ? join ? on ? = ? where ? > ?",
        "183": "select count(?), ? from ? join ? on ? = ? where ? = (select ? from ? join ? on ? = ? where ? = (select count(?), ?, ? from ? join ? on ? = ? order by ? desc limit ?) group by)",
        "184": "select ? from ? join ? on ? = ? join ? on ? = ? group by ? order by ? desc limit ?",
        "185": "select ?, ?, count(distinct ?) from ?",
        "186": "select count(?) from ? join ? on ? = ? join ? on ? = ? where ? in \"f\"",
        "187": "select ? from ? join ? on ? = ? join ? on ? = ? where count(?) = (select ? from ? except select ? from ?)",
        "188": "select distinct ? from ? join ? on ? = ? where ? = ?",
        "189": "select count(?) from ? where ? = (select ?, ?, ? from ? join ? on ? = ? where ? in ?)",
        "190": "select ? from ? join ? on ? = ? where ? in ?",
        "191": "select count(distinct ?) from ?",
        "192": "select count(?), max(?) from ?",
        "193": "select ? from ? join ? on ? = ? join ? on ? = ? group by ?",
        "194": "select ? from ? where ? = (select ? from ? where ? = (select distinct ? from ?)) or count(?) in \"eggs\"",
        "195": "select ? from ? where count(?) in (select max(distinct ?) from ?)",
        "196": "select ?, ? from ? where not ? = ?",
        "197": "select distinct count(?), ? from ? join ? on ? = ? join ? on ? = ? where ? in \"food\" intersect select ?, ? from ? join ? on ? = ?",
        "198": "select distinct count(?), ? from ?",
        "199": "select ?, ? from ? join ? on ? = ? join ? on ? = ?",
        "200": "select min(?) from ? join ? on ? = ? where ? in \"food\"",
        "201": "select distinct ? from ? join ? on ? = ? where ? = ? or ? = ? or ? >= ?",
        "202": "select ? from ? where ? = (select ?, count(?) from ? join ? on ? = ?)",
        "203": "select ? from ? join ? on ? = ? join ? on ? = ? where ? in \"eggs\" group by ?",
        "204": "select ?, ? from ? join ? on ? = ? join ? on ? = ? where not ? = ? group by ?",
        "205": "select count(?) from ? join ? on ? = ? where ? = (select ? from ?)",
        "206": "select ? from ? where ? in \"milk\"",
        "207": "select ?, count(?) from ? where count(?) = ?",
        "208": "select ?, ?, count(?) from ? join ? on ? = ?",
        "209": "select ? from ? join ? on ? = ? where ? = (select ?, count(?), ? from ? join ? on ? = ?) or ? = ?",
        "210": "select ? from ? where avg(?) = (select count(?) from ? join ? on ? = ? where ? = ?)",
        "211": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where count(?) > ?",
        "212": "select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? group by count(?)",
        "213": "select ?, ?, avg(distinct ?) from ? join ? on ? = ?",
        "214": "select avg(?), ? from ? join ? on ? = ? group by count(?)",
        "215": "select ?, ? from ? where ? = (select count(count(?)) from ? join ? on ? = ? join ? on ? = ? where ? = ?)",
        "216": "select count(?), ? from ? join ? on ? = ? join ? on ? = ?",
        "217": "select ? from ? where count(?) in (select ? from ? where ? in (select distinct count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ? group by))",
        "218": "select min(?) from ? join ? on ? = ? where ? = ?",
        "219": "select count(?) from ? join ? on ? = ?",
        "220": "select ? from ? join ? on ? = ? where ? in \"milk\"",
        "221": "select ? from ? join ? on ? = ? join ? on ? = ? where min(?) in ?",
        "222": "select ?, count(distinct ?) from ?",
        "223": "select distinct count(?), ?, ? from ?",
        "224": "select distinct max(?) from ?",
        "225": "select ? from ? join ? on ? = ? where ? = ? and ? = ? and ? = ?",
        "226": "select count(min(?)), ? from ? join ? on ? = ? where count(?) = ?",
        "227": "select avg(?) from ? where ? = ?",
        "228": "select max(?), ? from ? join ? on ? = ? join ? on ? = ? where ? in \"cat\"",
        "229": "select ? from ? where ? in \"eggs\"",
        "230": "select ? from ? join ? on ? = ? where ? = ? group by ?",
        "231": "select min(?) from ?",
        "232": "select count(?), ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? in \"cat\"",
        "233": "select avg(?), max(distinct ?) from ? join ? on ? = ? join ? on ? = ?",
        "234": "select count(?), ? from ? join ? on ? = ? where count(?) = ?",
        "235": "select count(distinct ?), ?, ? from ?",
        "236": "select ? from ? join ? on ? = ? join ? on ? = ? where count(?) in (select ? from ? group by)",
        "237": "select ? from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "238": "select ?, count(?), count(?) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "239": "select count(?) from ? where sum(?) = ?",
        "240": "select ?, count(?) from ?, ?, ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? or ? = ?",
        "241": "select ?, count(?) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where count(?) = ?",
        "242": "select ?, count(?) from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "243": "select ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? group by count(?) order by ? desc limit ?",
        "244": "select ?, count(?) from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and count(?) = ?",
        "245": "select ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "246": "select ? from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? order by ? desc limit ? intersect select count(?), ? from ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where count(?) = ? group by ? order by ? desc limit ?",
        "247": "select ?, sum(?), count(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?",
        "248": "select sum(?), count(?) from ?, ? join ? on ? = ? and ? = ?",
        "249": "select ? from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "250": "select ? from ? join ? on ? = ? where ? = ? except select count(?) from ?",
        "251": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "252": "select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? and count(?) > ? and count(?) = ?",
        "253": "select ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "254": "select ?, ?, count(?) from ?",
        "255": "select ?, count(?), count(?) from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ?",
        "256": "select ? from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "257": "select sum(?) from ?",
        "258": "select ? from ?, ? join ? on ? = ? and ? = ? where count(?) = ?",
        "259": "select ?, sum(?) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ? group by ? intersect select count(?) from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and ? = ?",
        "260": "select ?, ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "261": "select ?, ?, ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where count(?) = ? or ? = ?",
        "262": "select avg(?) from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "263": "select count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ? group by ?",
        "264": "select distinct ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "265": "select ? from ? join ? on ? = ? where sum(?) = ?",
        "266": "select ? from ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "267": "select ?, ?, ? from ? join ? on ? = ?",
        "268": "select count(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "269": "select count(?) from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? > ?",
        "270": "select ?, count(?), count(?) from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ?",
        "271": "select sum(?), count(?) from ? join ? on ? = ? where ? = ? and ? = ?",
        "272": "select ? from ? join ? on ? = ? where avg(?) = ?",
        "273": "select ? from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "274": "select ? from ? join ? on ? = ? where ? like ?",
        "275": "select ?, ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?",
        "276": "select ? from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "277": "select count(?), ? from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and ? = ? and ? = ?",
        "278": "select ?, count(?) from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "279": "select count(?), ? from ? join ? on ? = ? and ? = ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "280": "select ?, ? from ? join ? on ? = ? group by ?",
        "281": "select avg(?) from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? group by ?",
        "282": "select ? from ? join ? on ? = ? and ? = ? and ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and ? = ? and ? = ? and ? > ? and ? = ?",
        "283": "select count(?) from ? where count(?) = ?",
        "284": "select avg(?) from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "285": "select count(?), count(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "286": "select count(?) from ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "287": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "288": "select ?, count(?), ? from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? except select ? from ?, ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and ? = ? and count(?) = ?",
        "289": "select ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ?",
        "290": "select ?, ? from ? join ? on ? = ? join ? on ? = ? where sum(?) = ?",
        "291": "select count(distinct ?), ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "292": "select count(?), ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "293": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ?",
        "294": "select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ?",
        "295": "select avg(?), count(?) from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "296": "select sum(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "297": "select count(?), ?, ? from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "298": "select ? from ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? group by ?",
        "299": "select count(?) from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where count(?) = ?",
        "300": "select ? from ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ? and count(?) = ? and ? = ?",
        "301": "select ?, sum(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where count(?) = ?",
        "302": "select ? from ? join ? on ? = ? where ? = ? and ? = ?",
        "303": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where sum(?) = ? and ? = ? and ? = ? and ? = ?",
        "304": "select count(?), sum(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "305": "select count(?), ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where sum(?) = ? and ? = ? intersect select count(?) from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "306": "select count(?) from ?, ? join ? on ? = ? and ? = ? group by ?",
        "307": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "308": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? like ? and ? = ?",
        "309": "select ? from ? intersect select ? from ?",
        "310": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "311": "select ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? like ? group by ?",
        "312": "select ?, ?, ? from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "313": "select count(?), ?, ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "314": "select ? from ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where count(?) = ?",
        "315": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? and ? = ? and ? = ?",
        "316": "select ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and ? = ? and ? = ?",
        "317": "select ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? group by ? order by ? asc limit ?",
        "318": "select ?, count(?) from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "319": "select avg(?) from ?, ? join ? on ? = ? and ? = ? where ? = ? and count(?) > ?",
        "320": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and ? = ? group by count(?) order by ? desc limit ?",
        "321": "select ? from ? where ? = ? group by ?",
        "322": "select sum(?), ? from ? join ? on ? = ?",
        "323": "select ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "324": "select count(?) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "325": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where count(?) = ?",
        "326": "select ?, count(?) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "327": "select ?, sum(?) from ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "328": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? and ? = ?",
        "329": "select count(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "330": "select ?, ?, count(sum(?)) from ?, ? join ? on ? = ? and ? = ?",
        "331": "select sum(?), ? from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ?",
        "332": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "333": "select ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and ? = ? and ? = ? and sum(?) = ? and ? = ?",
        "334": "select ?, ? from ? join ? on ? = ? and ? = ? and ? = ?, ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ? or count(?) = ? or ? = ?",
        "335": "select ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ? or ? > ?",
        "336": "select ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and count(?) = ? and ? = ?",
        "337": "select count(?) from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "338": "select ?, ?, ? from ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ?",
        "339": "select count(?), count(?) from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "340": "select ?, sum(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "341": "select avg(?) from ? except select sum(distinct ?) from ?",
        "342": "select sum(?) from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "343": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "344": "select count(?), ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "345": "select ?, ? from ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "346": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "347": "select ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "348": "select ?, count(?) from ?",
        "349": "select ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and ? = ? and count(?) = ? and ? = ?",
        "350": "select ?, ?, count(?) from ?, ? join ? on ? = ? and ? = ?",
        "351": "select ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "352": "select ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "353": "select ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ? group by count(?)",
        "354": "select ? from ? join ? on ? = ? where sum(?) = ? group by ?",
        "355": "select ? from ? where ? = ? intersect select ? from ? intersect select ? from ? where ? = ?",
        "356": "select ?, count(?) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? > ?",
        "357": "select ?, count(?), count(?) from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "358": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where sum(?) = ?",
        "359": "select count(?) from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "360": "select ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where count(?) = ?",
        "361": "select ? from ? join ? on ? = ? and ? = ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ? or ? = ?",
        "362": "select ?, ?, count(?) from ? join ? on ? = ? where ? = ?",
        "363": "select ? from ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "364": "select ? from ? join ? on ? = ? and ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? group by ? having ? = ?",
        "365": "select ?, count(?), ? from ?, ? join ? on ? = ?, ? join ? on ? = ? and ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and ? = ?",
        "366": "select sum(?) from ? join ? on ? = ? where ? = ? group by ?",
        "367": "select ?, ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? group by ?",
        "368": "select ?, count(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and avg(?) = ?",
        "369": "select ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ? group by ?",
        "370": "select count(?), sum(?) from ?",
        "371": "select ? from ? where sum(?) = ?",
        "372": "select ?, ?, sum(?) from ? join ? on ? = ? and ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "373": "select count(?) from ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where sum(?) = ?",
        "374": "select ?, ? from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ?",
        "375": "select sum(?), ? from ? join ? on ? = ? join ? on ? = ? where ? = ? except select ? from ?",
        "376": "select ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? and ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where avg(?) = ? and ? = ? and ? = ? and ? = ?",
        "377": "select count(?) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? group by ? order by count(?) desc limit ?",
        "378": "select count(avg(?)) from ?",
        "379": "select ?, count(?), ? from ?, ?, ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "380": "select count(count(?)), count(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? group by ?",
        "381": "select ?, ? from ? join ? on ? = ? join ? on ? = ? where count(?) = ?",
        "382": "select ? from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where count(?) > ?",
        "383": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "384": "select ? from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where sum(?) = ?",
        "385": "select ? from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? = ? and sum(?) = ?",
        "386": "select ?, count(sum(?)), ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "387": "select ?, sum(?) from ? join ? on ? = ?",
        "388": "select ? from ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "389": "select ?, ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "390": "select count(?) from ? join ? on ? = ? join ? on ? = ?",
        "391": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ? group by ?",
        "392": "select ?, avg(?) from ? join ? on ? = ? where ? = ? except select ? from ? join ? on ? = ? where ? < (select ?, ? from ? join ? on ? = ? where ? = ?)",
        "393": "select ? from ? join ? on ? = ? where ? <> ? union select ?, max(?) from ? join ? on ? = ? where ? = ?",
        "394": "select count(?), ?, ? from ? join ? on ? = ? where ? <> ?",
        "395": "select ?, ? from ? where count(?) = ? or ? <> ?",
        "396": "select count(?), ?, ?, ? from ? join ? on ? = ?",
        "397": "select ? from ? where max(?) like ?",
        "398": "select ? from ? join ? on ? = ? where ? in year",
        "399": "select min(distinct ?) from ? join ? on ? = ? where ? <> ?",
        "400": "select ? from ? except select ?, ? from ? join ? on ? = ?",
        "401": "select ? from ? join ? on ? = ?",
        "402": "select ? from ? where ? = (select ? from ? where ? > ? group by)",
        "403": "select count(?) from ? where ? <> (select count(?) from ? where max(?) > (select ? from ? join ? on ? = ? where ? = ? group by))",
        "404": "select ?, ?, max(?) from ? join ? on ? = ? where ? = ?",
        "405": "select ? from ? where ? <> ?",
        "406": "select max(?) from ? where ? <> ?",
        "407": "select ?, ? from ? join ? on ? = ? where ? = ? group by ? having ? > ?",
        "408": "select ? from ? join ? on ? = ? where ? in \"steven spielberg\"",
        "409": "select ?, ? from ?, ? join ? on ? = ? and ? = ? where ? <> ? or ? = ? except select ?, count(?), ? from ? join ? on ? = ?",
        "410": "select ?, ?, ?, avg(?) from ? join ? on ? = ? intersect select ? from ?",
        "411": "select ? from ? join ? on ? = ? where ? between ? and ?",
        "412": "select ? from ? join ? on ? = ? where ? >= (select avg(?) from ?)",
        "413": "select ?, max(?) from ?",
        "414": "select avg(?) from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "415": "select ?, count(?) from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? > ?",
        "416": "select ? from ?, ? join ? on ? = ? and ? = ? group by ?",
        "417": "select ? from ? where ? = ? intersect select avg(?) from ?",
        "418": "select ?, ?, count(?), ? from ? join ? on ? = ?",
        "419": "select max(?) from ? join ? on ? = ?",
        "420": "select count(?) from ? join ? on ? = ? where ? = ? except select ?, ? from ?",
        "421": "select ? from ? join ? on ? = ? where max(?) <> ?",
        "422": "select ? from ? join ? on ? = ? where ? <> ? group by ?",
        "423": "select distinct ? from ? where ? <> ?",
        "424": "select ? from ? join ? on ? = ? where ? <> ?",
        "425": "select ?, count(?) from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? < (select max(?) from ?)",
        "426": "select ?, max(?) from ? join ? on ? = ? where ? = ?",
        "427": "select ?, avg(?) from ? join ? on ? = ? where ? <> ? except select ?, avg(?) from ? join ? on ? = ? where ? > ?",
        "428": "select avg(?), ? from ? join ? on ? = ?",
        "429": "select ?, ? from ? join ? on ? = ? where avg(?) = ?",
        "430": "select ? from ? intersect select ? from ?, ? join ? on ? = ? and ? = ? where ? <> ?",
        "431": "select ? from ? where ? < ?",
        "432": "select ?, ? from ? join ? on ? = ? where ? <> ?",
        "433": "select ?, avg(?) from ?, ? join ? on ? = ? and ? = ? where ? = ? group by ?",
        "434": "select ?, ? from ?, ? join ? on ? = ? and ? = ? where not ? = (select ? from ?)",
        "435": "select ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where avg(?) = ?",
        "436": "select ? from ? where ? = (select ?, ?, ?, ? from ? join ? on ? = ? where ? like ?)",
        "437": "select ?, count(?) from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ?",
        "438": "select count(?), avg(?) from ? join ? on ? = ? where ? <> ?",
        "439": "select ? from ? where ? = ? and count(?) = ?",
        "440": "select ?, ? from ?, ? join ? on ? = ? and ? = ? where ? = (select ? from ? where ? = ?)",
        "441": "select ?, max(?) from ? join ? on ? = ? where ? = ? group by ?",
        "442": "select ? from ? join ? on ? = ? where not ? = ?",
        "443": "select ? from ? where not ? = ?",
        "444": "select ? from ? where max(?) = ? group by ?",
        "445": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = ? except select ?, ? from ?, ? join ? on ? = ? and ? = ?",
        "446": "select count(?) from ? join ? on ? = ? where ? in ?",
        "447": "select ? from ? where ? <> ? except select max(?) from ? where ? = ?",
        "448": "select count(?) from ? where ? >= ?",
        "449": "select ?, ?, ?, avg(?) from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ?",
        "450": "select ? from ?, ? join ? on ? = ? and ? = ? where not ? = ?",
        "451": "select ? from ? where ? in ?",
        "452": "select min(count(?)), ?, ?, max(?) from ? join ? on ? = ?",
        "453": "select ?, max(?) from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? > ?",
        "454": "select ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? between ? and ? group by ? having ? = ? order by ? desc",
        "455": "select ?, ? from ? join ? on ? = ? where ? = (select ? from ?) intersect select ? from ? where ? = ?",
        "456": "select count(?), count(?) from ?",
        "457": "select distinct ?, ? from ? join ? on ? = ?",
        "458": "select distinct ?, ?, ?, max(?) from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ? intersect select ? from ? join ? on ? = ? where ? <> ?",
        "459": "select ? from ? join ? on ? = ? where ? = ? or ? = ? or ? >= ?",
        "460": "select min(?) from ? join ? on ? = ? where ? in \"daniel lewis\"",
        "461": "select max(?) from ? join ? on ? = ? where not ? >= ?",
        "462": "select distinct avg(?) from ?",
        "463": "select ? from ? union select max(?) from ? join ? on ? = ? where ? = ?",
        "464": "select ?, count(?) from ? where ? < ?",
        "465": "select ? from ? where ? = (select ?, ? from ? join ? on ? = ? where ? > ?)",
        "466": "select ?, ? from ? except select ? from ? except select min(?) from ? where ? > ?",
        "467": "select ?, ?, ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ?",
        "468": "select ?, ? from ? where avg(?) = ?",
        "469": "select ? from ? where ? between (select ? from ? join ? on ? = ? where ? = ?) and ?",
        "470": "select ?, ? from ? where ? <> ?",
        "471": "select ?, ? from ?, ? join ? on ? = ? and ? = ? where avg(?) = ?",
        "472": "select ?, ?, ? from ?, ? join ? on ? = ? and ? = ? where ? <> ?",
        "473": "select ? from ? where ? <> (select min(?), ? from ? join ? on ? = ? where ? = (select ?, ? from ?))",
        "474": "select avg(?) from ? where min(?) = ?",
        "475": "select count(?), ? from ? join ? on ? = ? where count(?) <> ?",
        "476": "select count(?) from ? where ? between ? and ?",
        "477": "select ?, ?, ?, ? from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "478": "select ? from ? where ? = ? except select ? from ? where ? = ?",
        "479": "select ?, ? from ? join ? on ? = ? where ? between ? and ? and not ? = ? group by max(?) having ? in year",
        "480": "select max(?) from ? where ? < ?",
        "481": "select ?, avg(?), ?, count(?) from ? join ? on ? = ?",
        "482": "select ? from ? where ? like ?",
        "483": "select ? from ? join ? on ? = ? where ? = ? and ? <> ? and ? = ?",
        "484": "select ? from ? where ? > (select ? from ?)",
        "485": "select ?, ? from ? join ? on ? = ? where ? <> ? except select ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? > ?",
        "486": "select ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ? and ? between ? and ?",
        "487": "select ? from ?, ? join ? on ? = ? and ? = ? where ? <> ?",
        "488": "select ? from ? where ? in \"brittany harris\"",
        "489": "select avg(?) from ? join ? on ? = ? where ? = (select ? from ?, ? join ? on ? = ? and ? = ? where ? = ?) and ? > ?",
        "490": "select ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ?",
        "491": "select ?, ? from ? join ? on ? = ? where avg(?) > ?",
        "492": "select distinct ? from ? join ? on ? = ? where ? < ?",
        "493": "select ? from ? where avg(?) > ?",
        "494": "select ? from ? join ? on ? = ? where ? > (select ? from ? where ? = ? group by)",
        "495": "select ? from ? where min(distinct ?) >= (select ? from ?)",
        "496": "select ? from ? where ? = ? except select ? from ?",
        "497": "select ?, ?, ?, ? from ? where ? = (select ?, count(avg(?)) from ? join ? on ? = ? where not ? = ?)",
        "498": "select ?, ? from ? join ? on ? = ? where ? > (select avg(min(?)) from ? join ? on ? = ? where ? = ?)",
        "499": "select distinct ?, ?, ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ?",
        "500": "select ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? <> ?",
        "501": "select ?, ?, count(?), ? from ?, ? join ? on ? = ? and ? = ? and ? = ? group by ? having ? = ?",
        "502": "select ? from ? where ? = ? except select ? from ? join ? on ? = ? where ? >= ?",
        "503": "select distinct ?, ? from ?",
        "504": "select max(?) from ? join ? on ? = ? where min(distinct ?) > ?",
        "505": "select avg(?) from ?, ? join ? on ? = ? and ? = ? where ? <> ?",
        "506": "select ?, ?, ?, count(?) from ? join ? on ? = ?",
        "507": "select ? from ? except select ? from ? intersect select ? from ? join ? on ? = ? where ? = (select ?, ? from ? join ? on ? = ?)",
        "508": "select ? from ? where ? = (select ? from ? where count(?) like ?)",
        "509": "select avg(?) from ? where ? in (select count(?) from ? where ? = ?)",
        "510": "select ?, ? from ? where not count(?) = ? or ? = ?",
        "511": "select ? from ? where not avg(?) = ?",
        "512": "select ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ?",
        "513": "select ? from ?, ? join ? on ? = ? and ? = ? where ? > ? except select avg(?), max(?), ? from ? join ? on ? = ? where ? = ?",
        "514": "select ?, max(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "515": "select distinct ? from ? join ? on ? = ? where ? = ? group by max(?) having ? = ? order by ? desc limit ?",
        "516": "select ?, ? from ? join ? on ? = ? where avg(?) = ? or not ? < ?",
        "517": "select ? from ? join ? on ? = ? where max(?) = ? group by ? having count(distinct ?) <> ?",
        "518": "select ? from ? join ? on ? = ? where ? = ? or not ? <> ?",
        "519": "select ?, ?, ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? > ?",
        "520": "select distinct ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "521": "select sum(?) from ? join ? on ? = ? join ? on ? = ? where count(?) = ?",
        "522": "select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? group by ?",
        "523": "select ?, ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "524": "select count(?), count(?) from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ? intersect select distinct ?, ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "525": "select distinct count(?) from ? join ? on ? = ? join ? on ? = ? where count(?) = ?",
        "526": "select ?, ? from ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by avg(?)",
        "527": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where avg(?) = ? and ? = ?",
        "528": "select ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ? or ? = ?",
        "529": "select count(?), ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "530": "select ?, avg(?) from ? join ? on ? = ? where ? like ?",
        "531": "select ?, ? from ? intersect select ? from ? join ? on ? = ? where ? = ?",
        "532": "select ? from ? join ? on ? = ? where ? < ?",
        "533": "select ? from ? join ? on ? = ? join ? on ? = ? where avg(?) = ?",
        "534": "select ? from ? join ? on ? = ? where count(?) < ? and ? = ?",
        "535": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? group by ?",
        "536": "select sum(?), count(?) from ? where ? = ?",
        "537": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ? having ? = ? or count(?) = ?",
        "538": "select ? from ? join ? on ? = ? join ? on ? = ? group by ? intersect select ? from ? join ? on ? = ? where ? = ?",
        "539": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where count(?) = ? group by ?",
        "540": "select sum(count(?)) from ? where ? like ?",
        "541": "select max(?), max(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ?",
        "542": "select ?, count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ? group by ?",
        "543": "select count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "544": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "545": "select ?, ?, count(?), ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "546": "select count(?), avg(?) from ? join ? on ? = ?",
        "547": "select ? from ? join ? on ? = ? where ? > ? except select ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "548": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? group by ? having count(?) = (select ?, ? from ? join ? on ? = ?) or ? = ?",
        "549": "select ?, avg(?) from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "550": "select ?, ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "551": "select count(count(?)) from ? where ? = ?",
        "552": "select distinct ?, ? from ? join ? on ? = ? where ? = ?",
        "553": "select count(distinct ?), ? from ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where avg(?) = ?",
        "554": "select ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ? group by ?",
        "555": "select distinct ? from ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ? having ? = ? and ? < ? or ? = ? or ? = ?",
        "556": "select ? from ? join ? on ? = ? join ? on ? = ? where ? < ?",
        "557": "select count(?), count(count(distinct ?)) from ? join ? on ? = ? where ? = ?",
        "558": "select ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ? group by ?",
        "559": "select avg(?) from ? where ? > ?",
        "560": "select avg(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? or ? > ? and ? = ?",
        "561": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? group by ?",
        "562": "select ?, ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "563": "select ?, count(?) from ? intersect select ? from ?",
        "564": "select count(?), ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? group by ? having count(?) = ?",
        "565": "select ?, ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? group by ?",
        "566": "select ? from ? join ? on ? = ? where count(?) = ? group by ?",
        "567": "select ? from ? join ? on ? = ? where count(?) = ? or ? = ?",
        "568": "select sum(?), ? from ? join ? on ? = ? join ? on ? = ?",
        "569": "select count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? group by ? order by count(?) asc limit ?",
        "570": "select count(distinct ?) from ? join ? on ? = ? join ? on ? = ? where ? > ?",
        "571": "select ?, count(count(?)) from ? join ? on ? = ?",
        "572": "select ?, count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "573": "select ? from ? join ? on ? = ? join ? on ? = ? where min(?) = ?",
        "574": "select count(?), ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "575": "select count(?), count(?) from ? join ? on ? = ? join ? on ? = ?",
        "576": "select sum(sum(?)), ? from ? join ? on ? = ? join ? on ? = ?",
        "577": "select ? from ? except select ? from ? join ? on ? = ? where ? = ?",
        "578": "select ?, ? from ? join ? on ? = ? where ? = (select ? from ? join ? on ? = ? where ? = ?) or ? = ?",
        "579": "select count(count(?)), count(?), ? from ? join ? on ? = ? join ? on ? = ?",
        "580": "select min(?), ? from ? join ? on ? = ? join ? on ? = ?",
        "581": "select count(?), count(?) from ? join ? on ? = ?",
        "582": "select sum(?), count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "583": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where count(?) = ?",
        "584": "select ?, ?, ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "585": "select count(?) from ? join ? on ? = ? join ? on ? = ? where ? > ?",
        "586": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? like ? and ? = ? and count(distinct ?) = ?",
        "587": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "588": "select sum(?), ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "589": "select ? from ? join ? on ? = ? group by ?",
        "590": "select ?, ? from ? join ? on ? = ? join ? on ? = ? group by ?",
        "591": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where sum(?) = ? or count(?) = ?",
        "592": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? like ? group by ?",
        "593": "select ?, ? from ? join ? on ? = ? where ? > ? group by ?",
        "594": "select ?, ? from ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where count(?) = ? or ? < ? or ? = ?",
        "595": "select count(?), count(?) from ? join ? on ? = ? where ? = ?",
        "596": "select ? from ? join ? on ? = ? join ? on ? = ?",
        "597": "select ?, ? from ? join ? on ? = ? where ? like ?",
        "598": "select ? from ? where count(distinct ?) = ?",
        "599": "select sum(?), count(?), ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "600": "select sum(sum(?)) from ?",
        "601": "select count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ? intersect select ? from ? join ? on ? = ? where ? <> ? order by ? asc limit ?",
        "602": "select ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where count(?) = ? or ? < ?",
        "603": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ? having ? = ?",
        "604": "select avg(?) from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? < ?",
        "605": "select distinct ?, ?, ? from ? join ? on ? = ? join ? on ? = ?",
        "606": "select count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ?",
        "607": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? or ? = ?",
        "608": "select ?, ? from ? join ? on ? = ? intersect select ?, count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "609": "select ?, count(?), ? from ? join ? on ? = ? join ? on ? = ? group by ?",
        "610": "select count(?), ? from ? join ? on ? = ? where ? = ? and count(?) = ?",
        "611": "select ?, count(?) from ? join ? on ? = ? join ? on ? = ? group by ?",
        "612": "select ?, ? from ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ? order by ? desc limit ?",
        "613": "select count(?) from ? join ? on ? = ? group by ?",
        "614": "select ?, ?, avg(?), ? from ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ?",
        "615": "select ? from ? join ? on ? = ? join ? on ? = ? where sum(?) = ?",
        "616": "select count(distinct ?), avg(?), ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ?",
        "617": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ?",
        "618": "select count(?), ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ? having ? = ?",
        "619": "select ?, ?, count(?) from ? join ? on ? = ? join ? on ? = ?",
        "620": "select count(distinct ?) from ? join ? on ? = ? where ? < ? and ? = ?",
        "621": "select ?, count(count(?)) from ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "622": "select distinct ? from ?, ? join ? on ? = ? and ? = ? and ? = ? group by ? order by sum(?) asc",
        "623": "select ? from ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ? or min(?) = ?",
        "624": "select distinct count(count(distinct ?)) from ?",
        "625": "select ?, count(?) from ? join ? on ? = ? join ? on ? = ? where ? < ?",
        "626": "select ?, count(?) from ? join ? on ? = ? where ? like ?",
        "627": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ? having ? = ? order by ? desc limit ?",
        "628": "select sum(?) from ? join ? on ? = ? where ? = ?",
        "629": "select ? from ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ? order by ? asc limit ?",
        "630": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where count(?) = ? or ? = ? and ? = ? and count(?) = ?",
        "631": "select ?, ? from ? join ? on ? = ? join ? on ? = ? except select ?, ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "632": "select ? from ? join ? on ? = ? where ? = ? and ? = ? or ? = ?",
        "633": "select ?, ? from ?, ? join ? on ? = ? and ? = ? group by ?",
        "634": "select avg(?) from ? join ? on ? = ? join ? on ? = ? where ? = ? or count(?) = ?",
        "635": "select avg(?) from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? and ? < ? and ? = ?",
        "636": "select min(?) from ? where ? = ?",
        "637": "select ?, avg(?) from ? join ? on ? = ?",
        "638": "select ? from ? join ? on ? = ? where ? = ? or ? = ? group by ?",
        "639": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ?",
        "640": "select ?, ?, min(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? group by ? having ? = ?",
        "641": "select ? from ? join ? on ? = ? join ? on ? = ? where count(?) = (select count(?) from ? join ? on ? = ? where count(?) = ? and count(?) = ?)",
        "642": "select ? from ? join ? on ? = ? join ? on ? = ? group by count(?)",
        "643": "select distinct ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? or ? = ?",
        "644": "select ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? and ? = ?",
        "645": "select ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? group by count(?)",
        "646": "select min(count(?)) from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "647": "select distinct ? from ? where count(?) = ?",
        "648": "select ?, ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? and count(?) = ?",
        "649": "select count(?) from ? join ? on ? = ? join ? on ? = ? group by ?",
        "650": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ?",
        "651": "select ?, ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "652": "select distinct ?, sum(?) from ? join ? on ? = ?",
        "653": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ? having ? = ? and ? = ? order by ? desc limit ?",
        "654": "select avg(?), count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ? or ? = ? or ? = ?",
        "655": "select count(?) from ? join ? on ? = ? join ? on ? = ? group by ? having ? = ?",
        "656": "select distinct ? from ? join ? on ? = ? where count(?) = ? group by ?",
        "657": "select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? group by ? having count(?) > ?",
        "658": "select ?, sum(?) from ? join ? on ? = ? join ? on ? = ? where ? like ?",
        "659": "select avg(?), ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where avg(?) like ? group by ?",
        "660": "select ?, count(?), ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? group by ? having ? < ?",
        "661": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ?",
        "662": "select distinct ?, ? from ? join ? on ? = ? join ? on ? = ? group by ?",
        "663": "select ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where count(?) = ? and ? = ? and ? = ? group by ?",
        "664": "select distinct count(?), ? from ? join ? on ? = ?",
        "665": "select ? from ? join ? on ? = ? where avg(?) <> ?",
        "666": "select ?, ? from ? where ? like ?",
        "667": "select min(?), ?, ? from ?",
        "668": "select ? from ? join ? on ? = ? where ? >= (select ?, ?, ?, min(?) from ? join ? on ? = ?)",
        "669": "select ?, ?, ?, ?, ? - ? from ?",
        "670": "select ?, ? from ? join ? on ? = ? where ? = (select ? from ?) or ? <> ?",
        "671": "select ? from ?, ? where not ? <> ?",
        "672": "select ?, ? from ? where ? >= ?",
        "673": "select ?, ?, ?, ?, ? from ? join ? on ? = ? where ? = ?",
        "674": "select ? from ? where count(?) in \"%s%\"",
        "675": "select ?, count(?) from ? where avg(?) <> ? and ? < ?",
        "676": "select max(?) from ?, ? where ? = ?",
        "677": "select count(?) from ? where count(?) between ? and ?",
        "678": "select ?, ? from ? where count(?) > ?",
        "679": "select ?, max(?), ? from ? where ? <> ?",
        "680": "select ?, ?, ?, ?, ? from ? join ? on ? = ? where ? between ? and ?",
        "681": "select ? from ? join ? on ? = ? where ? in \"marketing\"",
        "682": "select ? from ? where ? > ? or ? between ? and ?",
        "683": "select ?, count(?) from ? where ? = (select count(?) from ?) group by ?",
        "684": "select count(?), ? from ? join ? on ? = ? join ? on ? = ? where count(?) < ?",
        "685": "select ?, ?, ?, ? from ? where ? like (select ? from ? where ? = ?)",
        "686": "select ?, ? from ?, ? where ? in ? or max(?) like ?",
        "687": "select ? from ?, ? where ? > (select ?, ? from ?, ? where ? = ? or ? in \"clara\")",
        "688": "select ? from ? where not ? in \"pu_man\"",
        "689": "select max(?), ?, ? from ?",
        "690": "select max(?), ? from ? join ? on ? = ?",
        "691": "select count(?), ? from ? where ? like ?",
        "692": "select ?, ? from ?, ?",
        "693": "select ?, ?, ?, ? from ? where ? < ?",
        "694": "select ?, avg(?), ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "695": "select ?, ?, ?, ? from ? join ? on ? = ?, ?",
        "696": "select ? from ?, ? where min(?) = ?",
        "697": "select ?, ?, count(?), ?, ? from ? where ? like ?",
        "698": "select ?, ?, ? from ? join ? on ? = ? join ? on ? = ? where ? >= ?",
        "699": "select ?, ?, ?, ? from ?",
        "700": "select count(?), ?, ?, ?, ? from ? join ? on ? = ? where ? between ? and ?",
        "701": "select ?, avg(?), ? from ?, ? where ? like (select ?, ? from ? where ? <> ?)",
        "702": "select ?, ? from ? where ? in (select ? from ? where ? = ?)",
        "703": "select ? - ? from ? join ? on ? = ? where ? = ?",
        "704": "select ?, ? from ? join ? on ? = ? where ? in \"marketing\"",
        "705": "select ?, ?, ? from ? where ? between ? and (select ?, avg(? - ?) from ? join ? on ? = ? where ? like ?)",
        "706": "select ? from ? where ? - ? > ?",
        "707": "select ? from ? join ? on ? = ? where ? = (select ?, ? from ?)",
        "708": "select ? from ? where not ? >= (select distinct ?, ?, ?, ?, ? from ?, ?, ?, ? where ? in \"null\")",
        "709": "select ?, ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "710": "select ?, ? from ? join ? on ? = ? where ? between ? and (select ? from ?, ? where ? = ? and ? like ?)",
        "711": "select ? from ? join ? on ? = ? where not ? >= (select ?, count(?) from ?) or ? > ?",
        "712": "select ?, ?, ?, ?, ? from ? join ? on ? = ?",
        "713": "select ? from ? group by avg(?)",
        "714": "select ?, ?, count(?) from ? where count(?) = (select ? from ? join ? on ? = ? where count(?) = (select ? from ?))",
        "715": "select ?, ?, ?, ?, ? from ? join ? on ? = ? where max(?) like ?",
        "716": "select ? - ?, count(?) from ? where ? <> ?",
        "717": "select ?, ? from ? join ? on ? = ? where not avg(?) >= ? group by ? having ? = ?",
        "718": "select ?, ?, ?, ? from ? where count(?) in ? group by ? having min(?) = ?",
        "719": "select ?, ?, ? from ? where ? = ?",
        "720": "select ? from ?, ? join ? on ? = ? and ? = ? and ? = ? group by ? having ? <> ?",
        "721": "select ?, ? from ? where ? in \"pu_man\"",
        "722": "select count(?) from ? where ? like ?",
        "723": "select ? from ? where ? between ? and (select ? from ? where avg(?) between ? and ?)",
        "724": "select ?, ? from ? where ? = (select min(distinct ?), ?, count(max(?)), ?, ? from ?, ? where ? > ?)",
        "725": "select count(?), ? from ? join ? on ? = ?, ? where ? = ?",
        "726": "select ?, ? from ? join ? on ? = ?, ? where ? = ?",
        "727": "select ? - ? from ? join ? on ? = ? where ? < ?",
        "728": "select ?, ?, ? from ?, ? join ? on ? = ? and ? = ?, ? where ? >= (select ? from ?)",
        "729": "select ? from ? join ? on ? = ? where count(?) >= ?",
        "730": "select ?, count(?), ? from ? where ? between ? and ?",
        "731": "select ?, ? from ? join ? on ? = ? where ? >= ?",
        "732": "select ?, ?, ? from ? where ? between (select count(?) from ?, ? where ? <> ? or ? in \"marketing\" group by) and ?",
        "733": "select ?, ? from ?, ? where ? > ?",
        "734": "select ? from ? where ? = ? and ? like ?",
        "735": "select avg(?), ? from ? join ? on ? = ? join ? on ? = ? group by ?, ? having count(?) >= (select ? from ? join ? on ? = ? where ? = ?)",
        "736": "select ? from ?, ? where ? >= ?",
        "737": "select ?, ?, ? from ?, ?",
        "738": "select ? from ? where ? = (select ?, ?, ?, ? from ?, ? where ? < ?)",
        "739": "select ?, min(?) from ? where ? > ?",
        "740": "select ?, ?, avg(?) from ? join ? on ? = ? where ? between ? and (select ?, ? from ? where ? > ? group by ?)",
        "741": "select ?, ? from ? join ? on ? = ? where ? > ? or ? between ? and ?",
        "742": "select distinct ?, ?, ?, ?, ? from ? join ? on ? = ? join ? on ? = ?",
        "743": "select ?, ?, count(?) from ? where ? = ?",
        "744": "select ?, ? from ? join ? on ? = ? where ? >= ? and ? in (select ? from ? where ? = ?)",
        "745": "select ? from ? join ? on ? = ? where avg(?) in (select ?, ?, ? from ? where ? between ? and (select ? from ?) group by)",
        "746": "select ?, ?, avg(?) from ? where ? > ?",
        "747": "select ? from ? join ? on ? = ? where ? in \"mcewen\"",
        "748": "select count(?), ? from ? join ? on ? = ? where ? in manager_id",
        "749": "select ?, ? from ? where ? <> (select ? from ? join ? on ? = ? where ? <> ? or ? like ?)",
        "750": "select ?, min(?), ? from ? join ? on ? = ? where ? in \"1987-09-07\"",
        "751": "select ?, ? - ? from ?, ?",
        "752": "select ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? > ? and ? in (select ? from ?) group by ?",
        "753": "select ? from ? where ? between ? and (select ? from ? where ? = ? group by ? having ? >= ?)",
        "754": "select ?, count(?) from ?, ? where ? > ?",
        "755": "select ?, ?, ?, ? from ?, ?",
        "756": "select ?, ? from ? join ? on ? = ? where ? >= ? group by ?",
        "757": "select ? from ? where min(?) in ?",
        "758": "select ?, ? from ?, ? where ? like ?",
        "759": "select ?, ? from ? where ? < ?",
        "760": "select ? from ? join ? on ? = ? where ? <> ? group by ? having ? = ?",
        "761": "select ? from ? join ? on ? = ? where ? like ? and ? like ?",
        "762": "select distinct max(?), ? from ?",
        "763": "select ? from ? where ? in \"2007-11-05\"",
        "764": "select ?, ?, ?, ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where avg(?) = ?",
        "765": "select ?, ?, ?, ?, count(?) from ? join ? on ? = ? where ? = (select ? from ? where ? like ?)",
        "766": "select ?, avg(?), ? from ? where avg(?) > (select ?, avg(?) from ? join ? on ? = ?)",
        "767": "select ?, ?, ?, ?, max(?) from ? join ? on ? = ?, ? where ? in (select ?, ? from ?)",
        "768": "select ? from ? join ? on ? = ? where ? in \"mk_man\"",
        "769": "select ?, ? from ? join ? on ? = ? where ? >= ? group by ? having ? in \"payam\"",
        "770": "select distinct ? from ? where ? >= ?",
        "771": "select ?, ?, sum(?) from ?, ?",
        "772": "select ? from ?, ? where ? < ?",
        "773": "select ?, ?, ?, ?, count(?) from ? where ? like ?",
        "774": "select ? from ? where ? between ? and (select ? from ? group by ?) group by ?",
        "775": "select ?, ?, count(?), ? from ? join ? on ? = ? where ? = ?",
        "776": "select ?, ? from ? where avg(?) = (select ? from ?)",
        "777": "select ? from ? join ? on ? = ? where not ? in ?",
        "778": "select ?, ?, ? from ? join ? on ? = ? group by ?",
        "779": "select ?, ?, ? from ? where ? in ?",
        "780": "select ?, count(?), ? from ? join ? on ? = ?",
        "781": "select ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where not ? > ?",
        "782": "select max(?), ? from ? where ? in last_name",
        "783": "select ?, ? from ? join ? on ? = ? where ? between ? and ?",
        "784": "select ?, ?, ? from ? join ? on ? = ? where ? in ?",
        "785": "select ?, ?, ? from ? where ? <> ?",
        "786": "select ? from ? where ? in \"1987-09-07\"",
        "787": "select ?, count(count(distinct ?)) from ? where ? <> ? or ? > ?",
        "788": "select ? from ? join ? on ? = ? where ? in \"null\"",
        "789": "select ?, ?, ? from ? where ? >= ?",
        "790": "select ? from ? join ? on ? = ? where not ? > ?",
        "791": "select avg(?), ? from ?",
        "792": "select ?, ? - ?, ? from ?, ?",
        "793": "select ?, min(?) from ? where ? >= ?",
        "794": "select ? from ?, ? where count(?) between ? and ?",
        "795": "select ?, ?, ?, ?, ? from ? join ? on ? = ? where ? - ? between ? and ?",
        "796": "select ?, ?, ?, ? from ? join ? on ? = ? where ? >= ?",
        "797": "select count(?), ?, ?, ?, max(?) from ?, ? where not ? = ? group by ?",
        "798": "select ?, ?, ?, ?, ? from ? where ? <> ?",
        "799": "select ?, ?, count(?), ? from ? where ? < ?",
        "800": "select ?, max(?), ? from ?",
        "801": "select min(?), ?, ? from ? join ? on ? = ?",
        "802": "select ? from ? where ? between ? and ? or ? >= ?",
        "803": "select ?, ? from ? where ? = (select ?, count(?) from ? where ? between ? and ?)",
        "804": "select ? from ?, ? where ? in (select ? from ?, ? where ? < ?)",
        "805": "select avg(?), ? from ? where ? > (select ? from ? where ? between ? and ?)",
        "806": "select ?, ? from ? join ? on ? = ? join ? on ? = ? where ? <> ? group by ? having ? = ?",
        "807": "select ? from ?, ? where ? like ?",
        "808": "select ?, ?, ? from ? where ? < ?",
        "809": "select count(?), ?, ?, ? from ? join ? on ? = ?, ?",
        "810": "select ?, ? from ?, ? where ? = ? or ? = ?",
        "811": "select ? from ? join ? on ? = ?, ? where ? > ? and ? in ?",
        "812": "select ?, ?, ? from ?, ? where ? between ? and ?",
        "813": "select count(?), ?, ?, ?, ? from ? join ? on ? = ?",
        "814": "select ?, ? from ? where ? = (select ? from ? where ? = ?)",
        "815": "select ?, ? from ? where ? = (select ?, ?, ? from ? join ? on ? = ? where ? <> ?) and ? >= ?",
        "816": "select min(?) from ? where ? like ?",
        "817": "select ?, ? from ? where ? >= ? group by ?",
        "818": "select ? - ? from ? join ? on ? = ? where not ? <> (select ?, ? from ? where ? < ? or ? >= ? group by)",
        "819": "select ? from ?, ? where ? > ?",
        "820": "select ?, ?, ?, ?, ? from ? join ? on ? = ? join ? on ? = ? where ? between ? and ?",
        "821": "select ? from ? where ? <> ? and ? = ? and ? <> ?",
        "822": "select ? from ? where ? >= ? group by ?",
        "823": "select ?, ?, ? from ? join ? on ? = ? where ? like ?",
        "824": "select ?, ? - ?, ? from ? where ? in \"marketing\"",
        "825": "select ? from ? where ? = ? group by ?, ?",
        "826": "select ?, ? from ? join ? on ? = ? where not ? >= (select ? from ?)",
        "827": "select count(?), ?, ?, ? from ? where ? like ?",
        "828": "select ? from ? join ? on ? = ? where count(?) > ?",
        "829": "select ?, ? from ?, ? where min(?) > ? group by ?",
        "830": "select sum(?) from ? where ? like ?",
        "831": "select ?, ? from ? join ? on ? = ? where ? = (select avg(?), ? from ? where ? >= ?)",
        "832": "select ?, ?, ?, ?, max(?) from ?",
        "833": "select ? from ? join ? on ? = ? join ? on ? = ? group by ?, ? having not ? = ?",
        "834": "select count(?), ?, ?, ?, ? from ?, ? where min(?) in \"payam\"",
        "835": "select ?, avg(?), ? from ? join ? on ? = ? where ? <> ?",
        "836": "select ?, ?, ? from ? join ? on ? = ?, ?",
        "837": "select ?, ?, sum(distinct ?), ?, ? from ?, ? where ? >= ?",
        "838": "select ?, ?, ?, ?, ? from ? join ? on ? = ?, ?",
        "839": "select min(?), ?, ?, ? from ? join ? on ? = ?",
        "840": "select min(?), ? from ? where ? < ?",
        "841": "select ? from ? join ? on ? = ? where ? = ? group by ? order by ? asc",
        "842": "select ?, ?, avg(?) from ? join ? on ? = ? group by ?",
        "843": "select ?, ?, ? from ? join ? on ? = ? where ? = ?",
        "844": "select ? from ? where ? > (select ?, ? from ? where ? = ?)",
        "845": "select ? from ? intersect select min(?), ? from ? join ? on ? = ? where ? = ?",
        "846": "select ?, ? from ? join ? on ? = ? where ? = ? except select ? from ? join ? on ? = ? where ? = ?",
        "847": "select count(?) from ? where ? < ?",
        "848": "select ?, count(?), ? from ? join ? on ? = ? where ? like ?",
        "849": "select distinct ? from ? where ? like ?",
        "850": "select ? from ? where ? = ? group by ? intersect select ? from ? join ? on ? = ? where ? = ?",
        "851": "select count(?) from ? union select ? from ? join ? on ? = ? where ? < ?",
        "852": "select count(?), ?, ? from ? join ? on ? = ?",
        "853": "select ? from ? join ? on ? = ? where ? like (select ? from ? join ? on ? = ? where ? = ?)",
        "854": "select ? from ? join ? on ? = ? where ? = ? intersect select avg(?) from ? where ? > ?",
        "855": "select ? from ? join ? on ? = ? group by ? order by ? asc limit ?",
        "856": "select ? from ? join ? on ? = ? where ? = ? and ? = ? union select distinct ? from ? join ? on ? = ? where min(?) < ? or ? < ?",
        "857": "select min(?), count(?) from ? join ? on ? = ? where ? = ?",
        "858": "select min(?), avg(?) from ? join ? on ? = ?",
        "859": "select avg(?) from ? join ? on ? = ? where ? > ?",
        "860": "select ? from ? where avg(?) >= ?",
        "861": "select ?, max(?) from ? join ? on ? = ?",
        "862": "select ? from ? join ? on ? = ? where ? = ? intersect select max(?) from ? join ? on ? = ? group by ?",
        "863": "select ?, ? from ? join ? on ? = ? where ? = ? group by ?",
        "864": "select ?, count(?), ? from ? join ? on ? = ? where ? = ?",
        "865": "select ? from ? where ? = ? and ? = ?",
        "866": "select min(?) from ? where ? > ?",
        "867": "select distinct min(?), ? from ?",
        "868": "select ? from ? join ? on ? = ? where ? = ? and ? like ?",
        "869": "select ?, count(?) from ? join ? on ? = ? where count(?) = (select ?, ? from ? join ? on ? = ? group by ? order by ? asc limit ?)",
        "870": "select avg(?), ? from ? join ? on ? = ? where ? like ?",
        "871": "select ?, ? from ? join ? on ? = ? join ? on ? = ? where avg(?) = ?",
        "872": "select ? from ? where ? = ? group by ? order by ? asc",
        "873": "select distinct ? from ? where ? = (select ?, max(?), ? from ? join ? on ? = ? where count(?) like ?) group by ? order by ? desc limit ?",
        "874": "select count(?), count(?), ? from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "875": "select ? from ? join ? on ? = ? join ? on ? = ? where ? > ? and ? = ? intersect select max(?) from ? where ? = ?",
        "876": "select ?, ?, max(distinct ?) from ? join ? on ? = ?",
        "877": "select count(?), avg(?) from ? join ? on ? = ? where ? > ?",
        "878": "select min(max(?)), count(?) from ? join ? on ? = ? where ? = ?",
        "879": "select ? from ? except select ? from ? join ? on ? = ? where ? like ?",
        "880": "select count(?), count(distinct ?) from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "881": "select count(?), ? from ? join ? on ? = ? where ? > ?",
        "882": "select ? from ? join ? on ? = ? where ? < ? and ? < ?",
        "883": "select count(?), ? from ? join ? on ? = ? group by ?",
        "884": "select ?, min(?) from ? where ? = ?",
        "885": "select min(?), max(?) from ?",
        "886": "select count(?) from ? where ? > ?",
        "887": "select ? from ? join ? on ? = ? where ? = (select ?, ? from ? where ? > ? group by)",
        "888": "select ? from ? where ? = (select ? from ? group by)",
        "889": "select count(?), ? from ? join ? on ? = ? where ? = ?",
        "890": "select min(?) from ? join ? on ? = ? where count(?) = ? and ? = ?",
        "891": "select ?, min(?) from ? join ? on ? = ? where ? like ? except select ? from ? join ? on ? = ? where ? = ?",
        "892": "select ? from ? join ? on ? = ? where ? = ? and ? > ? and max(?) = ?",
        "893": "select distinct ? from ? except select ? from ? join ? on ? = ? where ? = ?",
        "894": "select ? from ? join ? on ? = ? join ? on ? = ? where min(?) like ? and ? = ?",
        "895": "select ? from ? where ? = ? except select ?, ? from ? join ? on ? = ?",
        "896": "select ? from ? where min(?) = ?",
        "897": "select min(?) from ? join ? on ? = ? where ? like ?",
        "898": "select ?, ?, count(?) from ? join ? on ? = ? where ? = ? intersect select ? from ? where ? = ?",
        "899": "select avg(?) from ? join ? on ? = ? where ? > ? group by ? order by ? desc limit ?",
        "900": "select avg(?), ? from ? where ? > ?",
        "901": "select ?, ? from ? join ? on ? = ? where ? > ? group by ? having ? > ?",
        "902": "select count(?) from ? join ? on ? = ? where ? = ? group by ?",
        "903": "select ?, ? from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? < (select ? from ? join ? on ? = ? where ? = ?)",
        "904": "select ? from ? except select ?, count(?), ? from ? join ? on ? = ? where ? = ?",
        "905": "select ?, ? from ? where ? = ? union select avg(?) from ?",
        "906": "select count(count(distinct ?)) from ?",
        "907": "select ?, ?, ? from ? join ? on ? = ? where ? > (select ? from ?) except select ? from ? where ? = ?",
        "908": "select ?, count(?) from ? join ? on ? = ? join ? on ? = ? where ? > ?",
        "909": "select count(?) from ? where ? > ? intersect select ?, ? from ? join ? on ? = ? where ? = (select count(?) from ? join ? on ? = ? where ? > ?)",
        "910": "select ?, ? from ? where ? like ? except select ? from ? where ? = ?",
        "911": "select ? from ? except select avg(?), ? from ? join ? on ? = ? where ? = ? and avg(?) = ?",
        "912": "select count(?), ?, ? from ? where ? = ?",
        "913": "select ? from ? join ? on ? = ? where ? = (select ? from ? join ? on ? = ? where ? = ?) union select ?, max(?) from ? join ? on ? = ? join ? on ? = ? where ? like ?",
        "914": "select ? from ? order by ? desc limit ? intersect select ?, ? from ? where ? > ? group by ?",
        "915": "select count(?) from ? join ? on ? = ? where avg(?) = ?",
        "916": "select min(?), ? from ? join ? on ? = ? where ? > ?",
        "917": "select ?, count(?) from ? join ? on ? = ? where count(?) = ?",
        "918": "select ?, count(?) from ? where ? = ?",
        "919": "select avg(count(?)), ?, ? from ? join ? on ? = ? where ? = ?",
        "920": "select ?, count(?) from ? join ? on ? = ? where ? > ?",
        "921": "select count(?), ?, ? from ? join ? on ? = ? where ? = ?",
        "922": "select ? from ? join ? on ? = ? where ? = ? group by ? order by ? desc limit ?",
        "923": "select ?, ? from ? join ? on ? = ? where ? = ? except select ?, count(?) from ? join ? on ? = ?",
        "924": "select distinct avg(?), ? from ?",
        "925": "select max(?) from ? join ? on ? = ? join ? on ? = ? where ? = ? group by ? order by ? desc limit ?",
        "926": "select min(?), ?, avg(?) from ? where ? = ?",
        "927": "select ?, ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? group by ?",
        "928": "select ?, count(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "929": "select ?, count(?) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where count(?) = ?",
        "930": "select ?, count(?) from ?, ? join ? on ? = ? and ? = ?",
        "931": "select ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? group by ? order by ? desc",
        "932": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "933": "select ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ? group by ? having ? = ?",
        "934": "select ? from ? intersect select avg(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "935": "select count(?) from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "936": "select count(?) from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? or ? = ?",
        "937": "select ?, ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "938": "select distinct ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "939": "select ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "940": "select ? from ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "941": "select count(?) from ? join ? on ? = ? and ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ?",
        "942": "select ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? > ?",
        "943": "select distinct ? from ? join ? on ? = ? join ? on ? = ? where ? > ?",
        "944": "select count(?) from ?, ? join ? on ? = ? and ? = ? where ? like ?",
        "945": "select ?, ?, ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ?",
        "946": "select avg(avg(?)), ? from ? join ? on ? = ?",
        "947": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? group by ? order by ? desc limit ?",
        "948": "select ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "949": "select ?, ? from ? join ? on ? = ? where ? = ? intersect select ? from ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? like ?",
        "950": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? > ?",
        "951": "select ? from ?, ?, ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? group by ? except select ? from ?",
        "952": "select ? from ? union select ? from ? join ? on ? = ? where ? = ?",
        "953": "select ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? < ?",
        "954": "select min(?) from ?, ? join ? on ? = ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "955": "select ?, count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "956": "select ?, ?, ? from ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "957": "select distinct ? from ? join ? on ? = ? join ? on ? = ? where ? < ?",
        "958": "select count(?) from ? except select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "959": "select ?, ? from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "960": "select ?, ? from ? join ? on ? = ? where max(?) > ?",
        "961": "select count(?) from ?, ? join ? on ? = ? and ? = ? group by ? order by ? desc limit ? union select ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "962": "select count(?) from ? union select ? from ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "963": "select distinct ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "964": "select ?, ? from ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ? group by ?",
        "965": "select distinct ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "966": "select distinct ?, min(?) from ? join ? on ? = ?",
        "967": "select count(?) from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "968": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = ? intersect select ? from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "969": "select ? from ?, ? join ? on ? = ? and ? = ? where ? like ?",
        "970": "select min(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "971": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where count(?) = ?",
        "972": "select distinct ? from ? join ? on ? = ? where ? > ?",
        "973": "select ? from ? except select ? from ?",
        "974": "select count(distinct ?), ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? > ? group by count(?)",
        "975": "select ? from ? union select count(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "976": "select ?, ? from ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ?",
        "977": "select count(?) from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "978": "select ? from ? join ? on ? = ? join ? on ? = ? where not ? > ?",
        "979": "select count(?) from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "980": "select ?, ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ?",
        "981": "select ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? except select ? from ?",
        "982": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? like ? intersect select ?, ? from ?, ? join ? on ? = ? and ? = ?",
        "983": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where avg(?) = ?",
        "984": "select count(?) from ? except select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "985": "select ?, ?, avg(?) from ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "986": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ?",
        "987": "select ? from ? intersect select ?, ? from ?, ? join ? on ? = ? and ? = ?",
        "988": "select avg(?) from ? join ? on ? = ? where not ? = ?",
        "989": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where count(?) > ? or ? = ? or ? = ?",
        "990": "select ?, ? from ? join ? on ? = ? join ? on ? = ?, ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "991": "select count(?) from ? intersect select ?, count(?) from ?, ? join ? on ? = ? and ? = ?",
        "992": "select min(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "993": "select ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "994": "select count(?), ?, ? from ? join ? on ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ?",
        "995": "select distinct ? from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "996": "select ?, ? from ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? in ?",
        "997": "select distinct ? from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "998": "select ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ?, ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and ? > ?",
        "999": "select ? from ? intersect select distinct ? from ?",
        "1000": "select ? from ? union select distinct ? from ?",
        "1001": "select distinct ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "1002": "select ?, ? from ?, ? join ? on ? = ? and ? = ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "1003": "select ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ? and ? in \"yes\"",
        "1004": "select ?, ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ?",
        "1005": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = ? intersect select min(?) from ?",
        "1006": "select avg(?) from ? where min(?) = ? and ? = ? and ? = ? and ? = (select distinct min(?) from ?)",
        "1007": "select sum(?) from ?, ? join ? on ? = ? and ? = ? where ? > (select ?, ? from ? join ? on ? = ?)",
        "1008": "select avg(?), ? from ? join ? on ? = ? except select ? from ?",
        "1009": "select ? from ? union select ? from ? join ? on ? = ? where max(?) = ?",
        "1010": "select ? from ? where ? = (select ? from ? join ? on ? = ? where sum(?) < ?)",
        "1011": "select avg(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "1012": "select max(?) from ? join ? on ? = ? where ? = ?",
        "1013": "select ? from (select distinct ? from ? where min(?) > ?) where ? = ?",
        "1014": "select ? from ? join ? on ? = ? where count(?) in \"goalie\"",
        "1015": "select ?, ? from ? except select max(avg(?)) from ?",
        "1016": "select count(?) from ? join ? on ? = ? where ? > ? intersect select distinct max(?) from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "1017": "select ?, avg(?), ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where count(?) = ?",
        "1018": "select ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? > ?",
        "1019": "select ? from ? join ? on ? = ? where ? in (select ?, ? from ? join ? on ? = ?)",
        "1020": "select min(count(?)), ? from ?",
        "1021": "select min(?) from ? join ? on ? = ? where ? < ?",
        "1022": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = (select ? from ? join ? on ? = ? where ? > ?)",
        "1023": "select ?, count(?), max(?) from ? join ? on ? = ? where ? = ?",
        "1024": "select ?, ?, ? from ? join ? on ? = ? where ? > ? intersect select ? from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "1025": "select ? from ? join ? on ? = ? where ? < ? except select ? from ? where ? > ?",
        "1026": "select max(?) from ?, ? join ? on ? = ? and ? = ? where ? < (select ? from ?, ? join ? on ? = ? and ? = ? where ? < ?)",
        "1027": "select ?, ? from ? join ? on ? = ? group by ? order by ? desc",
        "1028": "select ?, ? from ?, ? join ? on ? = ? and ? = ? where ? < ?",
        "1029": "select ? from ? where max(?) = ?",
        "1030": "select ?, ?, ? from ? join ? on ? = ? where count(?) = (select avg(?) from ?) intersect select ? from ? join ? on ? = ? where max(?) = ?",
        "1031": "select ? from ? join ? on ? = ? where ? in \"mid\"",
        "1032": "select ?, avg(?), avg(?) from ? join ? on ? = ? where ? = (select ?, ? from ?, ? join ? on ? = ? and ? = ? where ? = ?)",
        "1033": "select distinct ? from ?, ? join ? on ? = ? and ? = ? where ? = ? intersect select ? from ?, ? join ? on ? = ? and ? = ? where ? = ? and ? like ?",
        "1034": "select count(?), ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? > ? and ? = ?",
        "1035": "select count(?) from ?, ? join ? on ? = ? and ? = ? where count(?) = ?",
        "1036": "select ? from ? join ? on ? = ? where ? in \"d%\"",
        "1037": "select ? from ? where ? < (select ?, ? from ?, ? join ? on ? = ? and ? = ? where ? > ?)",
        "1038": "select ? from ? join ? on ? = ? where avg(?) = ? except select count(?) from ? join ? on ? = ? where avg(?) > ?",
        "1039": "select ? from ? where ? = (select ? from ? join ? on ? = ? where ? = (select min(?) from ? join ? on ? = ? where ? < ?) and ? between ? and ? and ? = ?)",
        "1040": "select avg(?) from (select ? from ?) where min(?) = (select max(?) from ? where ? = ?)",
        "1041": "select max(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "1042": "select ? from ? join ? on ? = ? where ? = (select ? from ? join ? on ? = ? where ? = (select ? from ?) group by)",
        "1043": "select ?, ? from ? where max(?) = ?",
        "1044": "select distinct ? from ?, ? join ? on ? = ? and ? = ? where ? < ?",
        "1045": "select ? from ? where ? > ? except select distinct avg(?) from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? > ? and ? = ?",
        "1046": "select sum(?) from ?, ? join ? on ? = ? and ? = ? where count(?) = ? except select distinct ? from ?",
        "1047": "select count(distinct ?), ? from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "1048": "select ? from ? join ? on ? = ? where ? like (select ?, ? from ? where ? = ?)",
        "1049": "select ? from ? where ? like ? intersect select ? from ? join ? on ? = ? where ? = ?",
        "1050": "select ? from (select ? from ? where ? = ?) where ? = ?",
        "1051": "select avg(?) from ? where ? between ? and ?",
        "1052": "select count(max(?)) from ?",
        "1053": "select distinct ? from ? where max(?) > ?",
        "1054": "select ? from ?, ? join ? on ? = ? and ? = ? where ? in \"mid\"",
        "1055": "select ? from ? join ? on ? = ? where min(?) < ?",
        "1056": "select max(?), min(?) from ? where count(?) < ?",
        "1057": "select min(?) from (select ? from ? except select min(?) from ?, ? join ? on ? = ? and ? = ? where count(?) = ? and min(?) = ? group by) where ? = ?",
        "1058": "select ?, count(?) from ? where ? = ? and ? < ?",
        "1059": "select avg(?) from ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "1060": "select avg(?), ?, ? from ? join ? on ? = ? where ? = ?",
        "1061": "select ? from ? where ? > (select ? from ? where ? = ?)",
        "1062": "select ? from ? where ? < ? except select ? from ?",
        "1063": "select avg(?), ? from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "1064": "select ? from ? join ? on ? = ? where ? = ? and ? < ? intersect select ? from ?, ? join ? on ? = ? and ? = ? where ? = (select ? from ?) and count(?) like ?",
        "1065": "select sum(?) from ? join ? on ? = ? where count(?) = (select ? from ?)",
        "1066": "select ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = (select distinct ? from ? group by) order by ? desc",
        "1067": "select count(?) from ? where min(?) = ?",
        "1068": "select ? from ? where ? = ? intersect select count(?) from ? except select ? from ? where ? < ?",
        "1069": "select distinct ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ?",
        "1070": "select count(?) from ? union select min(?) from ? where avg(?) < ?",
        "1071": "select max(?), ?, count(distinct ?) from ?, ? join ? on ? = ? and ? = ? and ? = ? where sum(?) > ? and ? between ? and ?",
        "1072": "select ? from ? where ? in \"yes\"",
        "1073": "select max(?), ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? between ? and (select avg(distinct ?) from ? where ? > ?)",
        "1074": "select ?, min(?) from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "1075": "select sum(min(?)) from ? join ? on ? = ? where ? = ?",
        "1076": "select ?, ?, count(distinct ?) from ? except select ? from ? join ? on ? = ? where ? > ?",
        "1077": "select count(min(?)) from ? where ? = ?",
        "1078": "select ? from ? join ? on ? = ? where ? = (select ? from ? join ? on ? = ? where ? = ? group by)",
        "1079": "select ? from ? except select avg(?) from ?",
        "1080": "select ? from ? join ? on ? = ? where ? = (select ? from ? where ? < ?)",
        "1081": "select max(?) from ? union select count(?) from ? join ? on ? = ? where ? > ?",
        "1082": "select ? from (select distinct ? from ?) where ? > ?",
        "1083": "select ? from ? where count(?) = (select count(distinct ?) from ?, ? join ? on ? = ? and ? = ? where not max(?) > ?)",
        "1084": "select sum(?) from ? where avg(?) = ?",
        "1085": "select ? from ? intersect select ? from ? join ? on ? = ? where ? = ?",
        "1086": "select ? from ? join ? on ? = ? where ? = ? intersect select ? from ? join ? on ? = ? where ? > ?",
        "1087": "select avg(max(?)) from ? where ? = ?",
        "1088": "select ? from ? join ? on ? = ? where max(?) = ?",
        "1089": "select ? from ? where ? = ? union select ? from ? where ? = ?",
        "1090": "select max(max(?)) from ?",
        "1091": "select avg(avg(?)) from ? join ? on ? = ? where ? = ?",
        "1092": "select ? from ? join ? on ? = ? where count(?) = ? except select ? from ? join ? on ? = ? join ? on ? = ? group by ?",
        "1093": "select distinct count(count(?)) from ?",
        "1094": "select count(?), count(?) from ?, ? join ? on ? = ? and ? = ? where count(distinct ?) = ? group by ?",
        "1095": "select count(?) from ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "1096": "select distinct ? from ? join ? on ? = ? where count(?) = ? except select distinct ? from ? join ? on ? = ? where ? = ?",
        "1097": "select ? from ? join ? on ? = ? where count(?) = ? and ? = ?",
        "1098": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = ? except select ?, ? from ? join ? on ? = ? where ? = ?",
        "1099": "select distinct count(?) from ? join ? on ? = ? where count(?) = ?",
        "1100": "select ? from ? join ? on ? = ? where ? = ? except select distinct ? from ? join ? on ? = ? where count(?) = ?",
        "1101": "select distinct ? from ? join ? on ? = ? where ? = ? group by ?",
        "1102": "select ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ?",
        "1103": "select ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where count(?) = ?",
        "1104": "select count(?) from ? join ? on ? = ? where count(?) = ?",
        "1105": "select ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? and ? = ?",
        "1106": "select ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "1107": "select count(?) from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? and ? = ? and ? = ? and ? = ?",
        "1108": "select ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? join ? on ? = ? where ? = ? and ? = ?",
        "1109": "select distinct ? from ? where ? = ? except select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ?",
        "1110": "select count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? group by ?",
        "1111": "select count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "1112": "select ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ? group by ?",
        "1113": "select distinct ? from ? join ? on ? = ? join ? on ? = ? where count(?) = ? group by ?",
        "1114": "select distinct count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "1115": "select ?, count(?) from ?, ? join ? on ? = ? and ? = ? except select ? from ? where ? = ?",
        "1116": "select distinct count(distinct ?) from ?",
        "1117": "select ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? group by ?",
        "1118": "select ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "1119": "select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ? and count(?) = ? except select distinct ? from ? join ? on ? = ? where ? = ?",
        "1120": "select distinct ? from ? join ? on ? = ?",
        "1121": "select count(distinct ?) from ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "1122": "select ?, count(count(?)) from ? join ? on ? = ? where ? = ?",
        "1123": "select count(?) from ? except select count(count(?)) from ? where ? = ?",
        "1124": "select count(count(?)) from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "1125": "select ? from ? except select distinct ? from ?",
        "1126": "select distinct ? from ?, ? join ? on ? = ? and ? = ? and ? = ?",
        "1127": "select count(count(?)) from ? join ? on ? = ? where ? = ?",
        "1128": "select ? from ? where count(?) like ? and ? = ? except select ? from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "1129": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where count(?) = ?",
        "1130": "select distinct count(?) from ? join ? on ? = ? and ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ?",
        "1131": "select ?, count(distinct ?) from ? join ? on ? = ? where ? = ?",
        "1132": "select ? from ? except select count(count(?)) from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? and ? = ?",
        "1133": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "1134": "select distinct ?, count(?) from ? join ? on ? = ?",
        "1135": "select ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where count(?) = ? and ? = ? group by ?",
        "1136": "select ?, ? from ?, ? join ? on ? = ? and ? = ? where ? = ? group by count(?)",
        "1137": "select ? from ?, ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? and ? = ? group by ?",
        "1138": "select ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where count(?) = ? and ? = ?",
        "1139": "select ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? < ?",
        "1140": "select ?, ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? in \"tv lounge\" group by count(?) having ? <> ?",
        "1141": "select distinct ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "1142": "select ? from ?, ? join ? on ? = ? and ? = ? where ? < ?",
        "1143": "select distinct ?, ? from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "1144": "select ?, count(?), ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? > ?",
        "1145": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = (select ? from ?) and ? = (select ?, ?, ? from ?, ? join ? on ? = ? and ? = ? where ? in \"f\")",
        "1146": "select distinct ? from ?, ? join ? on ? = ? and ? = ? where sum(?) = (select ? from ?)",
        "1147": "select ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where avg(?) = ? or ? = ?",
        "1148": "select ?, count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where count(?) in \"f\"",
        "1149": "select count(?), ? from ?, ? join ? on ? = ? and ? = ? where count(?) > ?",
        "1150": "select avg(distinct ?), ? from ?, ? join ? on ? = ? and ? = ?",
        "1151": "select ? from ?, ? join ? on ? = ? and ? = ? where not ? < ? and ? > ?",
        "1152": "select ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where not avg(?) = ?",
        "1153": "select ? from ? where ? = ? and ? between ? and ?",
        "1154": "select ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? group by ?",
        "1155": "select count(?), ? from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "1156": "select count(sum(?)) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "1157": "select ?, count(?) from ?, ? join ? on ? = ? and ? = ? and ? = ? where count(?) = (select max(?) from ? where ? = ? group by) and avg(?) < ?",
        "1158": "select ? from ? join ? on ? = ? where not avg(?) in \"hkg\"",
        "1159": "select ?, max(?), ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? group by ?",
        "1160": "select ?, max(?), ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? and ? = (select ? from ?)",
        "1161": "select ? from ? where not ? = (select ?, ? from ?, ? join ? on ? = ? and ? = ? where ? = ? group by)",
        "1162": "select ?, ? from ? where ? between (select distinct ?, ? from ?, ? join ? on ? = ? and ? = ? where ? = ?) and ?",
        "1163": "select ?, ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ?",
        "1164": "select avg(?), ? from ?, ? join ? on ? = ? and ? = ? group by ?",
        "1165": "select sum(?), ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "1166": "select avg(count(?)), ?, ? from ?, ? join ? on ? = ? and ? = ?",
        "1167": "select avg(?) from ?, ? join ? on ? = ? and ? = ? where ? < (select ?, avg(?) from ?, ? join ? on ? = ? and ? = ? where ? = ? group by)",
        "1168": "select ?, ? from ? where ? in \"smith hall\"",
        "1169": "select avg(?), ? from ?, ? join ? on ? = ? and ? = ? where ? <> ?",
        "1170": "select ? from ?, ? join ? on ? = ? and ? = ? where not ? = ? and avg(?) in \"phl\" and ? = ? or ? = ? and ? = ?",
        "1171": "select ?, ?, ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? and ? = ?",
        "1172": "select ?, ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where count(?) < ?",
        "1173": "select count(?) from ? where ? = (select ?, ?, ? from ?, ? join ? on ? = ? and ? = ? group by)",
        "1174": "select ? from ?, ? join ? on ? = ? and ? = ? where ? > (select count(?) from ?, ? join ? on ? = ? and ? = ? where ? = ? and ? = ?)",
        "1175": "select sum(?) from ?, ? join ? on ? = ? and ? = ? where ? = ? and ? in \"study room\"",
        "1176": "select ?, ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? in \"anonymous donor hall\"",
        "1177": "select avg(?) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? in \"f\"",
        "1178": "select ?, ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? group by ?",
        "1179": "select count(?) from ?, ? join ? on ? = ? and ? = ? where ? in (select ? from ?)",
        "1180": "select max(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "1181": "select ? from ?, ?, ? join ? on ? = ? and ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ?",
        "1182": "select count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? between (select ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? group by count(?)) and ?",
        "1183": "select ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? <> ?",
        "1184": "select ? from ?, ? join ? on ? = ? and ? = ? where count(?) > ?",
        "1185": "select distinct ?, ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "1186": "select ?, ?, ? from ? join ? on ? = ? where ? = (select avg(?) from ? where ? = (select ?, ?, ? from ?, ? join ? on ? = ? and ? = ? where ? = ?))",
        "1187": "select distinct ?, ? from ?, ? join ? on ? = ? and ? = ?",
        "1188": "select ?, count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "1189": "select max(?), max(?) from ? join ? on ? = ?",
        "1190": "select ? from ?, ? join ? on ? = ? and ? = ? where not ? in \"f\"",
        "1191": "select ? from ? where ? like (select ? from ? where ? = ? group by)",
        "1192": "select ?, count(count(?)) from ?, ? join ? on ? = ? and ? = ?",
        "1193": "select sum(?), count(?) from ?, ? join ? on ? = ? and ? = ? where ? < ?",
        "1194": "select ?, max(?), count(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "1195": "select sum(?) from ? where avg(?) > ?",
        "1196": "select ?, ? from ?, ? join ? on ? = ? and ? = ? where ? > (select avg(?), sum(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? group by ?) order by ? asc limit ?",
        "1197": "select ?, avg(?) from ?, ? join ? on ? = ? and ? = ? where count(?) like ?",
        "1198": "select ?, count(?) from ?, ? join ? on ? = ? and ? = ? where ? = ?",
        "1199": "select ?, max(?), ? from ?, ? join ? on ? = ? and ? = ?",
        "1200": "select ?, max(?) from ? join ? on ? = ? where ? > ?",
        "1201": "select avg(?), count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? group by ? except select avg(?) from ?",
        "1202": "select max(?) from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? > (select distinct ? from ? where ? = ? group by) order by ? asc",
        "1203": "select count(?), ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where avg(?) = ?",
        "1204": "select sum(?), count(?) from ?, ? join ? on ? = ? and ? = ? where ? < (select ?, ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where not ? = ?)",
        "1205": "select count(?) from ? where not ? = ?",
        "1206": "select count(?) from ?, ? join ? on ? = ? and ? = ? where ? in \"smith hall\" group by ? order by count(?) desc",
        "1207": "select ? from ? where ? > ? except select avg(?), ? from ? join ? on ? = ? where max(?) = ?",
        "1208": "select count(count(?)), ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? in \"hkg\" and ? = ?",
        "1209": "select count(?), count(?) from ?, ? join ? on ? = ? and ? = ?",
        "1210": "select ?, ? from ?, ? join ? on ? = ? and ? = ? group by count(?)",
        "1211": "select ?, avg(count(?)), ? from ?, ? join ? on ? = ? and ? = ? and ? = ?",
        "1212": "select distinct ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ? or ? = ?",
        "1213": "select ?, count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where count(?) = (select ? from ? group by)",
        "1214": "select ?, count(?) from ?, ? join ? on ? = ? and ? = ? group by ? order by ? desc",
        "1215": "select avg(?) from ?, ? join ? on ? = ? and ? = ? where max(?) > ?",
        "1216": "select count(?), count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ?",
        "1217": "select ? from ?, ? join ? on ? = ? and ? = ? where count(?) = (select avg(?) from ? where ? in \"f\" group by) order by ? asc",
        "1218": "select count(?) from ? where ? = ? union select count(?) from ? where ? = ?",
        "1219": "select avg(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? where ? in (select ?, ?, count(?) from ?, ? join ? on ? = ? and ? = ? group by) and ? = ? group by ?",
        "1220": "select ?, ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ? group by ?",
        "1221": "select ?, ?, count(count(?)) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? between ? and ? and ? > ? and ? > ? and ? > ?",
        "1222": "select ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ?",
        "1223": "select ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? and ? > ? group by ? having ? = (select ? from ?) and ? = (select max(?) from ?)",
        "1224": "select ? from ?, ? join ? on ? = ? and ? = ? where ? like (select ? from ?)",
        "1225": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where not sum(?) < ? and ? <> ? and ? = ? and ? > ?",
        "1226": "select ?, ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "1227": "select ?, sum(?) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ?",
        "1228": "select count(?) from ?, ? join ? on ? = ? and ? = ? where ? = (select count(?), ? from ?, ? join ? on ? = ? and ? = ?)",
        "1229": "select ?, ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? or ? > ?",
        "1230": "select sum(?), ? from ?, ? join ? on ? = ? and ? = ?",
        "1231": "select ?, ?, count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ?",
        "1232": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = (select ? from ? group by)",
        "1233": "select count(?), ? from ?, ? join ? on ? = ? and ? = ? where sum(?) in \"anonymous donor hall\"",
        "1234": "select ? from ? where ? = ? union select ? from ?, ? join ? on ? = ? and ? = ? where ? in \"bal\" group by ?",
        "1235": "select sum(?), ? from ?, ? join ? on ? = ? and ? = ? where ? = ? or ? = ?",
        "1236": "select count(?), ? from ?, ? join ? on ? = ? and ? = ? where sum(?) > ?",
        "1237": "select count(?), ? from ?, ? join ? on ? = ? and ? = ? where not ? = ? intersect select count(count(?)), count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ?",
        "1238": "select ?, ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? where ? = ? union select count(?) from ?",
        "1239": "select count(?) from ?, ? join ? on ? = ? and ? = ? where ? < ?",
        "1240": "select ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ? group by ?",
        "1241": "select ? from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where ? = ? group by ?",
        "1242": "select count(?), ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? = ?",
        "1243": "select ?, avg(?) from ?, ? join ? on ? = ? and ? = ? where ? > ?",
        "1244": "select ?, count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ?",
        "1245": "select ?, ? from ?, ? join ? on ? = ? and ? = ? where count(?) = ? and count(?) = (select ? from ?) and ? > ?",
        "1246": "select ? from ?, ? join ? on ? = ? and ? = ? where avg(?) in ?",
        "1247": "select count(?) from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? where ? in \"tv lounge\"",
        "1248": "select ? from ?, ?, ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? and ? = ? and ? = ? where avg(?) = ? and ? = ?",
        "1249": "select avg(?) from ? join ? on ? = ? join ? on ? = ?",
        "1250": "select ?, ?, ? from ? join ? on ? = ? where ? in ? except select ?, ? from ?, ? join ? on ? = ? and ? = ? and ? = ? where ? = ?",
        "1251": "select count(distinct ?) from ? where ? = ?",
        "1252": "select ? from ?, ? join ? on ? = ? and ? = ? where ? = (select count(distinct ?) from ? join ? on ? = ? where ? = ?)",
        "1253": "select avg(?) from ? where count(?) = ?",
        "1254": "select sum(?), ?, ? from ?, ? join ? on ? = ? and ? = ? where ? in \"smith hall\"",
        "1255": "select count(?) from ?, ? join ? on ? = ? join ? on ? = ? and ? = ? group by ?",
        "1256": "select ?, count(?), ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "1257": "select ?, ?, ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? except select count(?) from ? where ? = ?",
        "1258": "select ? from ? except select ? from ? where ? = ?",
        "1259": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "1260": "select ? from ? join ? on ? = ? join ? on ? = ? where ? >= ? and ? = ?",
        "1261": "select ? from ? group by ? order by ? desc limit ?",
        "1262": "select count(?), ? from ? where ? = ? intersect select ? from ?",
        "1263": "select count(distinct ?), count(?), ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? group by ?",
        "1264": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "1265": "select count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ? group by count(?) having count(?) = ?",
        "1266": "select ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? and ? = ? join ? on ? = ? group by ?",
        "1267": "select ?, ? from ? group by ? order by ? desc limit ?",
        "1268": "select count(?), ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "1269": "select ?, ?, ?, ? from ? join ? on ? = ? join ? on ? = ? where count(?) = ?",
        "1270": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and count(?) = ? except select ? from ? where ? = ?",
        "1271": "select count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? group by count(?) having ? = ?",
        "1272": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? >= ?",
        "1273": "select ? from ? except select count(?), ?, count(?) from ? join ? on ? = ? join ? on ? = ?",
        "1274": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and count(?) >= ?",
        "1275": "select count(?) from ? where ? = ? group by ? order by ? asc limit ? except select ? from ?",
        "1276": "select ?, ?, ? from ? join ? on ? = ? join ? on ? = ?",
        "1277": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "1278": "select count(?) from ? intersect select ?, ? from ?",
        "1279": "select ?, count(?), ? from ? join ? on ? = ? group by ?",
        "1280": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and ? = ? and ? >= ? and ? = ?",
        "1281": "select ?, count(?) from ? join ? on ? = ? join ? on ? = ? where ? = ? except select count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where count(distinct ?) < ?",
        "1282": "select count(?) from ? where ? = ? group by ?",
        "1283": "select ? from ? intersect select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "1284": "select distinct ?, count(?) from ?",
        "1285": "select ?, count(distinct ?), count(?) from ? join ? on ? = ?",
        "1286": "select ? from ? except select count(?) from ?",
        "1287": "select count(?) from ? join ? on ? = ? where ? = ? and count(?) = ?",
        "1288": "select count(?), count(?) from ? intersect select ?, ? from ?",
        "1289": "select ? from ? join ? on ? = ? join ? on ? = ? where ? = ? and ? < ?",
        "1290": "select count(?), ? from ? join ? on ? = ? join ? on ? = ? where count(?) = ?",
        "1291": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ?",
        "1292": "select count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ?",
        "1293": "select count(?), ?, ? from ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ?",
        "1294": "select distinct ?, ? from ? where ? = ?",
        "1295": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ?, ?",
        "1296": "select ?, ?, ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ?",
        "1297": "select ?, ?, ?, count(?) from ? join ? on ? = ? join ? on ? = ?",
        "1298": "select count(?) from ? join ? on ? = ? join ? on ? = ? and ? = ? join ? on ? = ? where ? = ? and ? = ? or ? = ? or ? = ?",
        "1299": "select count(?) from ? where ? = ? and ? = ? or count(?) = ?",
        "1300": "select ?, ? from ? join ? on ? = ? where count(?) = ? group by ?",
        "1301": "select ? from ? where ? = ? intersect select ? from ? except select ? from ?",
        "1302": "select count(?), ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where count(?) = ?",
        "1303": "select ? from ? where ? = ? and ? = ? or count(?) = ? and ? = ?",
        "1304": "select ?, ?, count(distinct ?), ? from ? join ? on ? = ? join ? on ? = ? except select ? from ?",
        "1305": "select ?, count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and count(?) = ? or ? = ? and ? = ? group by ?",
        "1306": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? group by ? order by ? desc limit ?",
        "1307": "select ?, count(?), ? from ? join ? on ? = ? join ? on ? = ?",
        "1308": "select count(?) from ? except select ?, ? from ? join ? on ? = ? join ? on ? = ?",
        "1309": "select distinct ?, ?, count(?), ? from ? join ? on ? = ?",
        "1310": "select ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? group by ?",
        "1311": "select count(?), ? from ? except select count(?) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? and count(?) < ?",
        "1312": "select ? from ? group by ? having ? = ? except select count(count(?)) from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? order by ? desc limit ?",
        "1313": "select ?, ? from ? join ? on ? = ? join ? on ? = ? where count(distinct ?) = ? or count(?) = ?",
        "1314": "select ? from ? except select ?, ?, count(distinct ?) from ? join ? on ? = ? join ? on ? = ? intersect select ?, ? from ? join ? on ? = ? join ? on ? = ?",
        "1315": "select count(?) from ? group by count(?)",
        "1316": "select ?, ? from ? join ? on ? = ? join ? on ? = ? join ? on ? = ? join ? on ? = ? where ? = ? group by ?",
        "1317": "select count(?), ? from ? join ? on ? = ? join ? on ? = ? group by ?"
    }
}