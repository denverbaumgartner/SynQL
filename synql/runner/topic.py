"""
Topic Generation Script

This script is an example of using SynQL to generate topics given a database. It requires a configuration file, as shown in `configs/topic_example.json`. Additionally, the script expects a `.env` file in the root of the directory. 

python topic.py \ 
    --config configs/topic_example.json
"""

# system packages 
import os
import json
import argparse
import logging
import asyncio

# internal packages
import synql
from synql import process_api_requests_from_file, prepare_batch_request_file

# external packages
from dotenv import load_dotenv
load_dotenv("../.env")

if __name__ == "__main__": 

    # Parse the configuration file
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, help="Path to the configuration file.")
    
    args = parser.parse_args()
    with open(args.config, "r") as f: 
        config = json.load(f)

    # Initialize SynQL

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