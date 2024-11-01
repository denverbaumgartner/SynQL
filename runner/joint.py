"""
Joint Generation Script

This script is an example of using SynQL to generate QQPs from databases, topics, and query templates. It requires a configuration file, as shown in `configs/joint_example.json`. Additionally, the script expects a `.env` file in the root of the directory. 

python joint.py --config configs/joint_example.json
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

# import synql.synql
load_dotenv("../.env")

if __name__ == "__main__": 

    print("running joint.py: generating QQPs from databases, topics, and query templates")

    # Parse the configuration file
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, help="Path to the configuration file.")
    
    args = parser.parse_args()
    with open(args.config, "r") as f: 
        config = json.load(f)

    # Set configuration variables
    topics_path = config["topics_path"]
    query_templates_path = config["query_templates_path"]

    data_path = config["data_path"]
    database_path = config["database_path"]
    create_statement_path = config["create_statement_path"]
    db_ids = config["db_ids"]

    model = config["model"]
    temperature = config["temperature"]
    request_url = config["request_url"]
    sample_count = config["sample_count"]
    safety_scalar = config["safety_scalar"]
    max_requests_per_minute = config["max_requests_per_minute"] * safety_scalar
    max_tokens_per_minute = config["max_tokens_per_minute"] * safety_scalar
    token_encoding_name = config["token_encoding_name"]
    max_attempts = config["max_attempts"]
    open_ai_api_key = os.getenv("OPENAI_API_KEY")

    qqp_joint_user_prompt_version = config["qqp_joint_user_prompt_version"]
    qqp_joint_system_prompt_version = config["qqp_joint_system_prompt_version"]

    save_local = config["save_local"]
    save_prompt_path = config["save_prompt_path"]
    param_file_path = save_prompt_path + "_params.jsonl"
    desired_sample_params_save_path = save_prompt_path + "_distribution_params.jsonl" 
    desired_sample_save_path = save_prompt_path + "_distribution.jsonl"
    save_qqp_path = config["save_qqp_path"]

    # Load Contextual Information (Topics, Query Templates, and Databases)
    with open(topics_path, "r") as f:
        topics = json.load(f)
    with open(query_templates_path, "r") as f:
        templates = json.load(f) 
    with open(create_statement_path, 'r') as f: 
        create_statements = json.load(f)

    syn = synql.SynQL()
    syn.loader.load_spider(data_path)
    syn.inspector.set_db_folder(database_path)
    syn.joint_generator.load_local_prompts(syn.prompt_path)

    # Subset based upon the provided db_ids
    topics = {k: v for k, v in topics.items() if k in db_ids} 
    create_statements = {k: v for k, v in create_statements.items() if k in db_ids} 

    # Set prompts
    prompts = {
        "qqp_user_prompt": syn.joint_generator.prompts.qqp.joint.user,
        "qqp_system_prompt": syn.joint_generator.prompts.qqp.joint.system,
    }

    # Set the system arguments
    args = {
        "model": model,
        "temperature": temperature,
        "qqp_joint_user_prompt_version": qqp_joint_user_prompt_version,
        "qqp_joint_system_prompt_version": qqp_joint_system_prompt_version,
        "save_local": save_local,
        "save_local_path": save_prompt_path,  
        "schemas": create_statements,
        "topics": topics,
        "queries": templates,
    }

    print(args["queries"])

    # Generate the requests (prompts)
    syn.joint_generator.format_qqp_data_request(
        prompts=prompts,
        args=args
    )

    # Load the generated prompts and downsample based on the desired distribution
    with open(param_file_path, "r") as f:
        data = [json.loads(l) for l in f]

    desired_sample_args = {
        "count": sample_count, 
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

    # Save the downsampled prompts
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

    # Generate the QQPs
    if config['run_generation']:
        asyncio.run(
            process_api_requests_from_file(
                requests_filepath=desired_sample_save_path, 
                save_filepath=save_qqp_path,
                request_url=request_url,
                api_key=open_ai_api_key,
                max_requests_per_minute=float(max_requests_per_minute),
                max_tokens_per_minute=float(max_tokens_per_minute),
                token_encoding_name=token_encoding_name,
                max_attempts=max_attempts,
                logging_level=20,
            )
        )