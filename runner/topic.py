"""
Topic Generation Script

This script is an example of using SynQL to generate topics given a database. It requires a configuration file, as shown in `configs/topic_example.json`. Additionally, the script expects a `.env` file in the root of the directory. 

python topic.py --config configs/topic_example.json
"""

# system packages 
import os
import sys
import json
import time
import argparse
import logging
import asyncio
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# internal packages
import synql
from synql import process_api_requests_from_file, prepare_batch_request_file

# external packages
from dotenv import load_dotenv
load_dotenv("../.env")

if __name__ == "__main__": 

    print("running topic.py: generating topics for downstream contextual information")

    # Parse the configuration file
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, help="Path to the configuration file.")
    
    args = parser.parse_args()
    with open(args.config, "r") as f: 
        config = json.load(f)

    # Set configuration variables
    run_generation = config["run_generation"]

    data_path = config["data_path"]
    database_path = config["database_path"]
    create_statement_path = config["create_statement_path"]
    
    model = config["model"]
    temperature = config["temperature"]
    request_url = config["request_url"]
    safety_scalar = config["safety_scalar"]
    max_requests_per_minute = config["max_requests_per_minute"] * safety_scalar
    max_tokens_per_minute = config["max_tokens_per_minute"] * safety_scalar
    token_encoding_name = config["token_encoding_name"]
    max_attempts = config["max_attempts"]
    open_ai_api_key = os.getenv("OPENAI_API_KEY")
    
    topic_user_prompt_version = config["topic_user_prompt_version"]
    topic_system_prompt_version = config["topic_system_prompt_version"]

    save_local = config["save_local"]
    save_prompt_path = config["save_prompt_path"]
    save_results_path = config["save_results_path"]

    # Initialize SynQL
    print("running generation_seed_spider_topics")
    syn = synql.SynQL()
    
    # Load the data (assumes a Spider style data structure, see: https://github.com/taoyds/spider?tab=readme-ov-file#data-content-and-format)
    syn.loader.load_spider(data_path)
    syn.inspector.set_db_folder(database_path)
    syn.joint_generator.load_local_prompts(syn.prompt_path)

    with open(create_statement_path, 'r') as f: 
        create_statements = json.load(f)

    # Set the prompts
    prompts = {
        "seed_topic_user_prompt": syn.joint_generator.prompts.seed.topic.user,
        "seed_topic_system_prompt": syn.joint_generator.prompts.seed.topic.system,
    }

    # Set the arguments
    args = {
        "model": model,
        "temperature": temperature,
        "seed_topic_user_prompt_version": topic_user_prompt_version,
        "seed_topic_system_prompt_version": topic_system_prompt_version,
        "schemas": create_statements,
        "save_local": save_local,
        "save_local_path": save_prompt_path,  
    }

    # Format the data requests (prompts)
    syn.joint_generator.format_seed_data_request(
        prompts=prompts,
        args=args
    )

    # check three times to see if save_prompt_path.jsonl exists. wait 2 seconds between each check
    final_save_prompt_path = save_prompt_path + ".jsonl"
    for i in range(3):
        if os.path.exists(final_save_prompt_path):
            break
        else:
            print(f"waiting for {final_save_prompt_path} to exist")
            time.sleep(2)

    if run_generation:
        asyncio.run(
            process_api_requests_from_file(
                requests_filepath=final_save_prompt_path,
                save_filepath=save_results_path,
                request_url=request_url,
                api_key=open_ai_api_key,
                max_requests_per_minute=float(max_requests_per_minute),
                max_tokens_per_minute=float(max_tokens_per_minute),
                token_encoding_name=token_encoding_name,
                max_attempts=max_attempts,
                logging_level=20, 
            )
        )