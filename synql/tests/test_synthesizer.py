import pytest 
from synql import SynQL

class TestJointGenerationSynth:

    def test_syn(self, syn: SynQL):
        assert syn.joint_generator is not None

    def test_prompt_path(self, syn: SynQL):
        assert syn.prompt_path is not None

    def test_load_local_prompts(self, syn: SynQL):
        syn.joint_generator.load_local_prompts(syn.prompt_path)        
        for prompt in syn.joint_generator.prompts.seed.topic.user:
            assert prompt is not None
        assert syn.joint_generator.prompts is not None

    def test_format_seed_topic_prompt(self, syn: SynQL):
        syn.joint_generator.load_local_prompts(syn.prompt_path)
        
        user_prompts = syn.joint_generator.prompts.seed.topic.user
        user_prompt = [prompt for prompt in user_prompts if prompt.version == '1.0.0'][0]
        assert user_prompt.version == '1.0.0'

    def test_format_seed_data_request(self, syn: SynQL):
        syn.joint_generator.load_local_prompts(syn.prompt_path)
        create_statements = syn.get_spider_create_statements()

        prompts = {
            "seed_topic_user_prompt": syn.joint_generator.prompts.seed.topic.user,
            "seed_topic_system_prompt": syn.joint_generator.prompts.seed.topic.system,
        }

        args = {
            "model": "gpt-4",
            "temperature": 0.7,
            "seed_topic_user_prompt_version": "1.0.0",
            "seed_topic_system_prompt_version": "1.0.0",
            "schemas": create_statements,
        }

        seed_data_requests = syn.joint_generator.format_seed_data_request(prompts, args)
        perpetrator_seed_request = {'content': "Provided here are the create statements for tables in a database. Your job is to return distinct topics of questions can be asked about the database.\n\nschema: CREATE TABLE perpetrator (perpetrator_id NUMBER, people_id NUMBER, date TEXT, YEAR NUMBER, LOCATION TEXT, country TEXT, killed NUMBER, injured NUMBER,\n                          FOREIGN KEY (people_id) REFERENCES people(people_id));\nCREATE TABLE people (people_id NUMBER, name TEXT, height NUMBER, weight NUMBER, home_town TEXT);\n\n\nExample Topics: \n    1: 'College Information (Questions specifically related to the colleges. Avoid questions related to players or tryouts)'\n    2: 'Player Information (Questions specifically related to players. Avoid questions related to colleges or tryouts)'\n    3: 'Tryout Information (Questions specifically related to tryouts. Avoid questions related to colleges or players)'\n\nOnly respond with the topic of the question, not the question itself, formatted as the Example Topics are. Return them in a numbered list, separated by commas.", 'system_context': 'Your job is to provide distinct topics that encapsulate a specific subset of questions that can be asked about a database.\n\nThe goal is to generate distinct topics for the database. The topics should not overlap. Return the topics as a numbered list, seperated by commas.'}
        assert seed_data_requests['perpetrator']['message'][1]['content'] == perpetrator_seed_request['content']