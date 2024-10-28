# system packages 
import os
import json
import random
import logging
from types import SimpleNamespace
from typing import Optional, Dict, List
from collections import defaultdict
from abc import ABC, abstractmethod

# internal packages
from .prompts import *
from .helper import validate_system_path, dict_to_sns
from .requestor import process_api_requests_from_file

# external packages
import pandas as pd
import datasets as ds

# TODO: it probably makes a lof of sense to move this to a separate directory and have a separate file for each implementation of the base class
class Synth(ABC):

    @abstractmethod
    def __init__(
        self, 
        dbs: Optional[List] = None,
        prompts: Dict = None,
        seed_data: ds.Dataset = None, # lets use datasets for now
        qqp_data: ds.Dataset = None, # lets use datasets for now
        prompt_local_load_path: str = None,
        seed_data_local_load_path: str = None,
        seed_data_local_save_path: str = None,
        qqp_data_local_load_path: str = None,
        qqp_data_local_save_path: str = None,
    ) -> None:
        self.dbs = dbs
        self.prompts = prompts
        self.seed_data = seed_data
        self.qqp_data = qqp_data
        self.prompt_local_load_path = prompt_local_load_path
        self.seed_data_local_load_path = seed_data_local_load_path
        self.seed_data_local_save_path = seed_data_local_save_path
        self.qqp_data_local_load_path = qqp_data_local_load_path
        self.qqp_data_local_save_path = qqp_data_local_save_path

    ##########################
    # Load Methods           #
    ##########################
    def load_local_prompts(
        self,
        path: Optional[str]
    ):
        """Loads prompts from a given path. Attempts to load from local path if no path is provided.
        
        :param path: The path to the prompts. 
        :type path: Optional[str]
        """
        if path is not None:
            validate_system_path(path)
            self.prompts = dict_to_sns(json.load(open(path)))
        elif self.prompt_local_load_path is not None:
            validate_system_path(self.prompt_local_load_path)
            self.prompts = dict_to_sns(json.load(open(self.prompt_local_load_path)))
        else:
            raise ValueError("No path provided for loading prompts")

    def load_local_seed_data(
        self, 
        path: Optional[str]
    ):
        """Loads seed data from a given path. Attempts to load from local path if no path is provided.
        
        :param path: The path to the seed data. 
        :type path: Optional[str]
        """
        if path is not None:
            validate_system_path(path)
            self.seed_data = ds.load_dataset(path)
        elif self.seed_data_local_load_path is not None:
            validate_system_path(self.seed_data_local_load_path)
            self.seed_data = ds.load_dataset(self.seed_data_local_load_path)
        else:
            raise ValueError("No path provided for loading seed data")
        
    def load_local_qqp_data(
        self, 
        path: Optional[str]
    ):
        """Loads qqp data from a given path. Attempts to load from local path if no path is provided.
        
        :param path: The path to the qqp data. 
        :type path: Optional[str]
        """
        if path is not None:
            validate_system_path(path)
            self.qqp_data = ds.load_dataset(path)
        elif self.qqp_data_local_load_path is not None:
            validate_system_path(self.qqp_data_local_load_path)
            self.qqp_data = ds.load_dataset(self.qqp_data_local_load_path)
        else:
            raise ValueError("No path provided for loading qqp data")
    
    ##########################
    # Distribution Methods   #
    ##########################
    @abstractmethod
    def get_desired_qqp_distribution(self, data: List[Dict], args: Dict) -> Dict:
        """Gets the desired distribution of qqp data for a given prompt and args

        Today, we expect the data to be in a dictionary format loaded from a json file.
        """
        pass

    ##########################
    # Generation Methods     #
    ##########################
    @abstractmethod
    def format_seed_data_request(self, prompts: Dict, args: Dict) -> Dict:
        pass

    @abstractmethod
    def format_qqp_data_request(self, prompts: Dict, args: Dict) -> Dict:
        pass

    ##########################
    # Save Methods           #
    ##########################
    @abstractmethod
    def save_seed_data_local(self, path: str, data: Dict) -> None:
        pass # TODO: we need to align behind a common data format (lets go with datasets or polars)

    @abstractmethod
    def save_qqp_data_local(self, path: str, data: Dict) -> None:
        pass # TODO: we need to align behind a common data format (lets go with datasets or polars)

class JointGenerationSynth(Synth):

    def __init__(
        self, 
        dbs: Optional[List] = None,
        prompts: Dict = None,
        seed_data: ds.Dataset = None, # lets use datasets for now
        qqp_data: ds.Dataset = None, # lets use datasets for now
        prompt_local_load_path: str = None,
        seed_data_local_load_path: str = None,
        seed_data_local_save_path: str = None,
        qqp_data_local_load_path: str = None,
        qqp_data_local_save_path: str = None,
    ) -> None:
        self.dbs = dbs
        self.prompts = prompts
        self.seed_data = seed_data
        self.qqp_data = qqp_data
        self.prompt_local_load_path = prompt_local_load_path
        self.seed_data_local_load_path = seed_data_local_load_path
        self.seed_data_local_save_path = seed_data_local_save_path
        self.qqp_data_local_load_path = qqp_data_local_load_path
        self.qqp_data_local_save_path = qqp_data_local_save_path

    def print_hello(self):
        print("hello, world!")
    
    ##########################
    # Distribution Methods   #
    ##########################    
    def get_desired_qqp_distribution(self, data: List[Dict], args: Dict) -> Dict:
        """Gets the desired distribution of qqp data for a given prompt and args. Returns a subset of the initial data based upon the desired distribution.

        Today, we expect the data to be in a dictionary format loaded from a json file.

        data = [
                    {
                        "model": "gpt-4",
                        "temperature": 0.7,
                        "db_id": "db_id",
                        "topic": "1",
                        "query": "1",
                        "messages": [
                            ...
                        ],
                    },
                    {
                        ...
                    },
                    ...
                ]
        
        args = {
            "count": int, # desired number of requests
            "strategy": "uniform", # desired distribution strategy
            "params": [ # desired distribution parameters
                "db_id",
                "query",
            ]
        }
        """
        # TODO: this should all be reworked...

        # for today, we are just going to make this work under a strict hard-coded implementation
        # we can now thing about this as groups of db_id-query pairs
        # partition the data into groups of db_id-query pairs where there are no duplicates per each group
        # then we take each group and add it to our aggregate
        # when subset + new group > count, we sample count - subset from the new group
        # we then add the subset to our aggregate and return the aggregate
        if args["strategy"] != "uniform":
            raise ValueError("Strategy not found")
        if args["params"] != ["db_id", "query"]:
            raise ValueError("Currently, we only support db_id and query as parameters")
        
        grouped_data = defaultdict(list)
        for item in data: 
            key = (item["db_id"], item["query"])
            grouped_data[key].append(item)

        total = len(data)
        count = args["count"]
        num_groups = len(grouped_data)
        samples_per_group = max(1, count // num_groups)
        
        sampled_data = []
        remaining_count = count
        
        for group, items in grouped_data.items():
            if remaining_count <= 0:
                break
            available_samples = min(len(items), samples_per_group)
            random.shuffle(items)
            for _ in range(available_samples):
                if items:  
                    sampled_data.append(items.pop())
                    remaining_count -= 1
                    if remaining_count <= 0:
                        break

        while remaining_count > 0:
            data_count = 0 
            for group, items in grouped_data.items():
                data_count += len(items)
            if data_count == 0:
                break


            for group, items in grouped_data.items():
                if remaining_count <= 0:
                    break
                if items:
                    sampled_data.append(items.pop())
                    remaining_count -= 1
                    if remaining_count <= 0:
                        break
        return sampled_data

    ##########################
    # Generation Methods     #
    ##########################
    def format_seed_topic_user_context_prompt(
            self,
            prompt: str,
            args: Dict 
    ): 
        """
        args = {
            "version: "1.0.0",
            "db_id": "db_id",
            "schema": "CREATE TABLE ... ;",
        }
        """
        if args["version"] == "1.0.0":
            return prompt.format(
                schema=args["schema"],
            )
        if args["version"] == "1.1.0":
            return prompt.format(
                schema=args["schema"],
            )
        if args["version"] == "1.2.0":
            return prompt.format(
                db_id=args["db_id"],    
                schema=args["schema"],
            )
        
    def format_qqp_joint_user_context_prompt(
            self, 
            prompt: str,
            args: Dict
        ) -> str:
        """args = {
            "version": "1.3.1",
            "schema": "CREATE TABLE ... ;",
            "topic": "Questions about ...",
            "query": "SELECT ? FROM ?;",
            "list_of_questions": ["...", "...", "..."],
            "list_of_queries": ["...", "...", "..."],
        }
        """
        if args["version"] == "1.3.1":
            return prompt.format(
                question_subject=args["topic"],
                query_structure=args["query"],
                schema=args["schema"],
                list_of_questions=args["list_of_questions"],
                list_of_queries=args["list_of_queries"]
            )
        elif args["version"] == "1.4.0":
            return prompt.format(
                schema=args["schema"],
                question_subject=args["topic"],
                query_structure=args["query"],
                list_of_questions=args["list_of_questions"],
                list_of_queries=args["list_of_queries"]
            )
        elif args["version"] == "1.5.0":
            return prompt.format(
                schema=args["schema"],
                question_subject=args["topic"],
                query_structure=args["query"],
            )
        elif args["version"] == "1.5.1":
            return prompt.format(
                schema=args["schema"],
                question_subject=args["topic"],
                query_structure=args["query"],
            )
        elif args["version"] == "1.5.2":
            return prompt.format(
                schema=args["schema"],
                question_subject=args["topic"],
                query_structure=args["query"],
            )
        else:
            raise ValueError("Version not found")

    def format_seed_data_request(
            self, 
            prompts: Dict[str, SimpleNamespace], 
            args: Dict
        ) -> Dict:
        """This function returns a json object that contains the formatted prompts for generating the topic seed data for the joint generation approach.
        
        :param prompts: The prompts for the seed data generation.
        :type prompts: Dict containing the prompts for the seed data generation.
        :param args: The arguments for the seed data generation.
        :type args: Dict containing the arguments for the seed data generation.

        prompts = {
            "seed_topic_user_prompt": prompts.seed.topic.user,
            "seed_topic_system_prompt": prompts.seed.topic.system,
        }

        args = {
            "model": "gpt-4",
            "temperature": 0.7,
            "seed_topic_user_prompt_version": "1.0.0",
            "seed_topic_system_prompt_version": "1.0.0",
            "schemas": {
                "db_id": "CREATE TABLE ... ;",
            }
            "save_local": True,
            "save_local_path": "path/to/save",
        }

        return {
            db_id: {
                "model": "gpt-4",
                "messages": [
                    {
                        "role": "system", 
                        "content": "...",
                    }, {
                        "role": "user", 
                        "content": "...",
                    }
                ], 
                "temperature": 0.7,
            },
            ...
        }
        """
        user_context_prompt = "".join([prompt for prompt in prompts["seed_topic_user_prompt"] if prompt.version == args["seed_topic_user_prompt_version"]][0].prompt)
        system_context_prompt = "".join([prompt for prompt in prompts["seed_topic_system_prompt"] if prompt.version == args["seed_topic_system_prompt_version"]][0].prompt)

        seed_data_requests = {}
        for db_id, create_statement in args["schemas"].items():

            seed_data_requests[db_id] = {
                "model": args["model"],
                "messages": [
                    {
                        "role": "system", 
                        "content": system_context_prompt,
                    },
                    {
                        "role": "user",
                        "content": self.format_seed_topic_user_context_prompt(
                            prompt=user_context_prompt,
                            args={
                                "version": args["seed_topic_user_prompt_version"],
                                "db_id": db_id,
                                "schema": create_statement,
                            }
                        )
                    }
                ],
                "temperature": args["temperature"],
            }
        if args["save_local"]:
            self.save_seed_data_local(
                path=args["save_local_path"],
                data={
                    "args": args, 
                    "data": seed_data_requests
                },
            )
        return seed_data_requests
    
    def format_qqp_data_request(self, prompts: Dict, args: Dict) -> Dict:
        """This function returns a json object that contains the formatted prompts for generating the qqp data for the joint generation approach.
        
        :param prompts: The prompts for the qqp data generation.
        :type prompts: Dict containing the prompts for the qqp data generation.
        :param args: The arguments for the qqp data generation.
        :type args: Dict containing the arguments for the qqp data generation.

        prompts = {
            "qqp_user_prompt": prompts.qqp.joint.user,
            "qqp_system_prompt": prompts.qqp.joint.system,
        }

        args = {
            "model": "gpt-4",
            "temperature": 0.7,
            "qqp_joint_user_prompt_version": "1.3.1",
            "qqp_joint_system_prompt_version": "1.3.1",
            "save_local": True,
            "save_local_path": "path/to/save",
            "schemas": {
                "db_id": "CREATE TABLE ... ;",
            }
            "topics": {
                "db_id": {
                    "1": "...",
                    ...
                }
            }
            queries: {
                "1": "SELECT ? FROM ?;",
                ...
            }
        }

        return {
            db_id: {
                "model": "gpt-4",
                "temperature": 0.7,
                "db_id": "db_id",   
                "topic": "1",
                "query": "1",
                "messages": [
                    {
                        "role": "system", 
                        "content": "...",
                    }, {
                        "role": "user", 
                        "content": "...",
                    }
                ], 
            },
            ...
        }
        """
        user_context_prompt = "".join([prompt for prompt in prompts["qqp_user_prompt"] if prompt.version == args["qqp_joint_user_prompt_version"]][0].prompt)
        system_context_prompt = "".join([prompt for prompt in prompts["qqp_system_prompt"] if prompt.version == args["qqp_joint_system_prompt_version"]][0].prompt)

        qqp_data_requests = {}
        for db_id, create_statement in args["schemas"].items():
            if db_id not in qqp_data_requests: # TODO: we should dynamically handle assignment using defaultdict or similar
                qqp_data_requests[db_id] = {}
            for topic_id, topic in args["topics"][db_id].items():
                if topic_id not in qqp_data_requests[db_id]:
                    qqp_data_requests[db_id][topic_id] = {}
                for query_id, query in args["queries"].items():
                    if query_id not in qqp_data_requests[db_id][topic_id]:
                        qqp_data_requests[db_id][topic_id][query_id] = {}
                    qqp_data_requests[db_id][topic_id][query_id] = { # TODO: this is not dynamic for handling multiple requests
                        "model": args["model"],
                        "temperature": args["temperature"],
                        "db_id": db_id,
                        "topic": topic_id,
                        "query": query_id,
                        "messages": [
                            {
                                "role": "system", 
                                "content": system_context_prompt,
                            }, {
                                "role": "user", 
                                "content": self.format_qqp_joint_user_context_prompt(
                                    prompt=user_context_prompt,
                                    args={
                                        "version": args["qqp_joint_user_prompt_version"],
                                        "schema": create_statement,
                                        "topic": topic,
                                        "query": query,
                                        "list_of_questions": [], # TODO: currently, we are only set up to handle a single request
                                        "list_of_queries": [], # TODO: currently, we are only set up to handle a single request
                                    }
                                ),
                            }
                        ],
                    }
        if args["save_local"]:
            self.save_qqp_data_local(
                path=args["save_local_path"],
                data={
                    "args": args, 
                    "data": qqp_data_requests
                },
            )
        return qqp_data_requests

    ##########################
    # Save Methods           #
    ##########################
    def save_seed_data_local(self, path: str, data: Dict) -> None:
        """Saves the seed data and configuration details to a local path.
        
        :param path: The path to save the seed data.
        :type path: str, do not pass file extension.
        :param data: The seed data to save.
        :type data: Dict

        data = {
            args: {format_seed_data_request(args)},
            data: {format_seed_data_request},
        }
        """
        print("here is the path:")
        print(path)
        with open(path + "_map" + ".jsonl", 'w') as f: 
            json.dump(data['data'], f)
        with open(path + "_config" + ".jsonl", 'w') as f: 
            json.dump(data["args"], f)
        
        with open(path + ".jsonl", 'w') as f: 
            for key, prompt in data['data'].items():
                json.dump(prompt, f)
                f.write('\n')

    def save_qqp_data_local(self, path: str, data: Dict) -> None:
        """Saves the qqp data and configuration details to a local path.
        
        :param path: The path to save the qqp data.
        :type path: str, do not pass file extension.
        :param data: The qqp data to save.
        :type data: Dict

        data = {
            args: {format_qqp_data_request(args)},
            data: {format_qqp_data_request},
        }
        """
        with open(path + "_map" + ".json", 'w') as f: 
            json.dump(data['data'], f)
        with open(path + "_config" + ".json", 'w') as f:
            json.dump(data["args"], f)
        
        with open(path + '_params' + ".jsonl", 'w') as f:
            for db_id, level_one in data['data'].items():
                for topic_id, level_two in level_one.items():
                    for query_id, prompt in level_two.items():
                        json.dump(prompt, f)
                        f.write('\n')

        with open(path + ".jsonl", 'w') as f:
            for db_id, level_one in data['data'].items():
                for topic_id, level_two in level_one.items():
                    for query_id, prompt in level_two.items():
                        request_values = {
                            "model": prompt["model"],
                            "messages": prompt["messages"],
                            "temperature": prompt["temperature"],
                        }
                        json.dump(request_values, f)
                        f.write('\n')