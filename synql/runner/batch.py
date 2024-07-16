"""
Batch Generation Script

This script is an example of using SynQL to generate a QQPs batch request file from databases, topics, and query templates. It requires a configuration file, as shown in `configs/batch_example.json`. Additionally, the script expects a `.env` file in the root of the directory. 

python topic.py \ 
    --config configs/batch_example.json
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

import synql.synql
load_dotenv("../.env")

if __name__ == "__main__": 

    print("running batch.py: generating a QQP batch request from databases, topics, and query templates")

    # Parse the configuration file
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, help="Path to the configuration file.")
    
    args = parser.parse_args()
    with open(args.config, "r") as f: 
        config = json.load(f)

    # Set configuration variables
    topics_path = config["topics_path"]
    query_templates_path = config["query_templates_path"]
    create_statement_path = config["create_statement_path"]
    db_ids = config["db_ids"]

    model = config["model"]
    temperature = config["temperature"]
    qqp_joint_user_prompt_version = config["qqp_joint_user_prompt_version"]
    qqp_joint_system_prompt_version = config["qqp_joint_system_prompt_version"]
    sample_count = config["sample_count"]

    save_local = config["save_local"]
    save_prompt_path = config["save_prompt_path"]
    param_file_path = save_prompt_path + "_params.jsonl"
    desired_sample_params_save_path = save_prompt_path + "_distribution_params.jsonl" 
    desired_sample_save_path = save_prompt_path + "_distribution.jsonl"
    batch_requests_path = config["batch_requests_path"]

    # Load Contextual Information (Topics, Query Templates, and Databases)
    with open(topics_path, "r") as f:
        topics = json.load(f)
    with open(query_templates_path, "r") as f:
        templates = json.load(f) 
    with open(create_statement_path, 'r') as f: 
        create_statements = json.load(f)
    
    # Initialize SynQL
    syn = synql.SynQL()
    syn.joint_generator.load_local_prompts(syn.prompt_path)

    # Subset the seed data based on desired db_ids
    topics = {k: v for k, v in topics.items() if k in db_ids} 
    create_statements = {k: v for k, v in create_statements.items() if k in db_ids} 

    # Set the prompts
    prompts = {
        "qqp_user_prompt": syn.joint_generator.prompts.qqp.joint.user,
        "qqp_system_prompt": syn.joint_generator.prompts.qqp.joint.system,
    }

    # Set the arguments
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

    # Format the requests
    syn.joint_generator.format_qqp_data_request(
        prompts=prompts,
        args=args
    )

    # Load the formatted requests 
    with open(param_file_path, "r") as f:
        data = [json.loads(l) for l in f]

    # Get the arguments for the desired distribution
    desired_sample_args = {
        "count": sample_count,
        "strategy": "uniform",
        "params": [
            "db_id",
            "query",
        ]
    }

    # Subset the desired to the desired distribution 
    desired_distribution = syn.joint_generator.get_desired_qqp_distribution(
        data=data, 
        args=desired_sample_args
    )

    # Save the desired distribution
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

    # Format the batch requests
    prepare_batch_request_file(
        input_file_path=desired_sample_save_path,
        output_file_path=batch_requests_path,
    )