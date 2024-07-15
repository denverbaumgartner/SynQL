"""
SYNTHESIZER RUNNER

This script is the main entry point for the synthesizer. It takes a configuration file as input and runs the synthesizer.

python runner.py \
    --config configs/generation_qqp_join_spider_all_queries_batch.json
"""
#    --config configs/generation_qqp_joint_kaggle_all_queries.json
#    --config configs/generation_seed_kaggle_topics.json

# system packages 
import os
import json
import argparse
import logging
import asyncio

# internal packages
import synsql
from synsql import process_api_requests_from_file, prepare_batch_request_file

# external packages
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    print('hello, world!')

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, help="Path to the configuration file.")

    args = parser.parse_args()

    with open(args.config, "r") as f: 
        config = json.load(f)

    ##############################################################
    # generation_seed_spider_topics                              #
    ##############################################################
    if config['run_type'] == "generation_seed_spider_topics" or config['run_type'] == "generation_seed_kaggle_topics":
        print('running generation_seed_spider_topics')

        syn = synsql.SynSql()
        spider_path = config['spider_local_path']
        db_path = config['spider_local_path'] + "database/"
        syn.inspector.set_db_folder(db_path)
        syn.loader.load_spider(spider_path)

        syn.joint_generator.load_local_prompts(syn.prompt_path)
        with open(config["spider_create_statements_path"], 'r') as f: 
            create_statements = json.load(f)

        prompts = {
            "seed_topic_user_prompt": syn.joint_generator.prompts.seed.topic.user,
            "seed_topic_system_prompt": syn.joint_generator.prompts.seed.topic.system,
        }

        args = {
            "model": config['model'],
            "temperature": config['temperature'],
            "seed_topic_user_prompt_version": config["seed_topic_user_prompt_version"],
            "seed_topic_system_prompt_version": config["seed_topic_system_prompt_version"],
            "schemas": create_statements,
            "save_local": config["seed_save_local"],
            "save_local_path": config["seed_save_local_path"],  
        }

        if not config["load_local_seeds"]:
            syn.joint_generator.format_seed_data_request(
                prompts=prompts,
                args=args
            )
        
        save_filepath = config["local_seeds_path"].rstrip(".jsonl") + "_results.jsonl"
        max_requests_per_minute = config["max_requests_per_minute"] * 0.5
        max_tokens_per_minute = config["max_tokens_per_minute"] * 0.5

        if config['run_generation']:
            asyncio.run(
                process_api_requests_from_file(
                    requests_filepath=config['local_seeds_path'],
                    save_filepath=save_filepath,
                    request_url=config['request_url'],
                    api_key=os.getenv("OPENAI_API_KEY"),
                    max_requests_per_minute=float(max_requests_per_minute),
                    max_tokens_per_minute=float(max_tokens_per_minute),
                    token_encoding_name=config['token_encoding_name'],
                    max_attempts=config['max_attempts'],
                    logging_level=20, # logging.INFO
                )
            )
    ##############################################################
    # generation_qqp_joint_spider                                #
    ##############################################################
    if config['run_type'] == "generation_qqp_joint": 
        print('running generation_qqp_joint_spider')
        with open(config["spider_topics_path"], "r") as f:
            topics = json.load(f)
        with open(config["spider_templates_path"], "r") as f:
            all_templates = json.load(f) # 912

        syn = synsql.SynSql()
        spider_path = config['spider_local_path']
        db_path = config['spider_local_path'] + "database/"
        syn.inspector.set_db_folder(db_path)
        syn.loader.load_spider(spider_path)

        syn.joint_generator.load_local_prompts(syn.prompt_path)
        with open(config["spider_create_statements_path"], 'r') as f: 
            create_statements = json.load(f)

        # subset based on db_ids
        topics = {k: v for k, v in topics.items() if k in config['db_ids']} 
        create_statements = {k: v for k, v in create_statements.items() if k in config['db_ids']} 

        prompts = {
            "qqp_user_prompt": syn.joint_generator.prompts.qqp.joint.user,
            "qqp_system_prompt": syn.joint_generator.prompts.qqp.joint.system,
        }

        args = {
            "model": config['model'],
            "temperature": config['temperature'],
            "qqp_joint_user_prompt_version": config["qqp_joint_user_prompt_version"],
            "qqp_joint_system_prompt_version": config["qqp_joint_system_prompt_version"],
            "save_local": config["qqp_save_local"],
            "save_local_path": config["qqp_save_local_path"],  
            "schemas": create_statements,
            "topics": topics,
            "queries": all_templates,
        }

        if not config["load_local_qqp"]:
            syn.joint_generator.format_qqp_data_request(
                prompts=prompts,
                args=args
            )

        # load the generated data and downsample based on the desired distribution
        param_file_path = config["local_qqp_path"].replace(".jsonl", "") + "_params.jsonl"
        with open(param_file_path, "r") as f:
            data = [json.loads(l) for l in f]

        desired_sample_args = {
            "count": config["sample_count"], # 12000
            "strategy": "uniform",
            "params": [
                "db_id",
                "query",
            ]
        }
        desired_distribution = syn.joint_generator.get_desired_qqp_distribution(
            data=data, 
            args=desired_sample_args
        )
        desired_sample_params_save_path = config["local_qqp_path"].replace(".jsonl", "") + "_distribution_params.jsonl" 
        desired_sample_save_path = config["local_qqp_path"].replace(".jsonl", "") + "_distribution.jsonl"
        with open(desired_sample_params_save_path, "w") as f:
            for d in desired_distribution:
                f.write(json.dumps(d) + "\n")
        with open(desired_sample_save_path, "w") as f:
            for d in desired_distribution:
                req = {
                    "model": d["model"],
                    "messages": d["messages"],
                    "temperature": d["temperature"],
                }
                f.write(json.dumps(req) + "\n")


        save_filepath = config["local_qqp_path"].replace(".jsonl", "") + "_results.jsonl"
        print(save_filepath)
        max_requests_per_minute = config["max_requests_per_minute"] * 0.5
        max_tokens_per_minute = config["max_tokens_per_minute"] * 0.5
        print(desired_sample_save_path)

        if config['run_generation']:
            asyncio.run(
                process_api_requests_from_file(
                    requests_filepath=desired_sample_save_path, 
                    save_filepath=save_filepath,
                    request_url=config['request_url'],
                    api_key=os.getenv("OPENAI_API_KEY"),
                    max_requests_per_minute=float(max_requests_per_minute),
                    max_tokens_per_minute=float(max_tokens_per_minute),
                    token_encoding_name=config['token_encoding_name'],
                    max_attempts=config['max_attempts'],
                    logging_level=20, # logging.INFO
                )
            )
    ##############################################################
    # generation_qqp_joint_batch_requests                        #
    ##############################################################
    if config["run_type"] == "generation_qqp_joint_batch_requests":
        print("running generation_qqp_joint_batch_requests")

        # load the prompts
        syn = synsql.SynSql()
        syn.joint_generator.load_local_prompts(syn.prompt_path)

        # load the seed data
        with open(config["spider_topics_path"], "r") as f:
            topics = json.load(f)
        with open(config["spider_templates_path"], "r") as f:
            templates = json.load(f) # 912
        with open(config["spider_create_statements_path"], 'r') as f: 
            create_statements = json.load(f)

        # subset the seed data based on desired db_ids
        topics = {k: v for k, v in topics.items() if k in config['db_ids']} 
        create_statements = {k: v for k, v in create_statements.items() if k in config['db_ids']} 

        topic_count = 0
        for k, v in topics.items():
            for k2, v2 in v.items():
                topic_count += len(v2) # TODO: fix count 

        print(f"Number of databases: {len(create_statements)}")
        print(f"Number of topics:    {topic_count}")
        print(f"Number of templates: {len(templates)}")

        # set the prompts and arguments
        prompts = {
            "qqp_user_prompt": syn.joint_generator.prompts.qqp.joint.user,
            "qqp_system_prompt": syn.joint_generator.prompts.qqp.joint.system,
        }

        args = {
            "model": config['model'],
            "temperature": config['temperature'],
            "qqp_joint_user_prompt_version": config["qqp_joint_user_prompt_version"],
            "qqp_joint_system_prompt_version": config["qqp_joint_system_prompt_version"],
            "save_local": config["qqp_save_local"],
            "save_local_path": config["qqp_save_local_path"],  
            "schemas": create_statements,
            "topics": topics,
            "queries": templates,
        }

        # format the requests
        syn.joint_generator.format_qqp_data_request(
            prompts=prompts,
            args=args
        )

        # set the path to all the formatted requests
        param_file_path = config["qqp_save_local_path"] + "_params.jsonl"

        # load the formatted requests 
        with open(param_file_path, "r") as f:
            data = [json.loads(l) for l in f]

        # get the arguments for the desired distribution
        desired_sample_args = {
            "count": config["sample_count"], # 12000
            "strategy": "uniform",
            "params": [
                "db_id",
                "query",
            ]
        }

        # subset the desired to the desired distribution 
        desired_distribution = syn.joint_generator.get_desired_qqp_distribution(
            data=data, 
            args=desired_sample_args
        )

        # set the paths to save the desired distributions
        desired_sample_params_save_path = config["qqp_save_local_path"] + "_distribution_params.jsonl" 
        desired_sample_save_path = config["qqp_save_local_path"] + "_distribution.jsonl"

        # save the desired distribution
        with open(desired_sample_params_save_path, "w") as f:
            for d in desired_distribution:
                f.write(json.dumps(d) + "\n")
        with open(desired_sample_save_path, "w") as f:
            for d in desired_distribution:
                req = {
                    "model": d["model"],
                    "messages": d["messages"],
                    "temperature": d["temperature"],
                }
                f.write(json.dumps(req) + "\n")

        # format the batch requests
        prepare_batch_request_file(
            input_file_path=desired_sample_save_path,
            output_file_path=config["batch_requests_path"]
        )