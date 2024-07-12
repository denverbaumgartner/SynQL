# system packages 
import os
import json
from functools import cache
from typing import Optional, Dict, List

# internal packages
from .loader import Loader

# external packages
import pandas as pd
from transformers.models.t5.tokenization_t5_fast import T5TokenizerFast

class Transform():
    """A supporting class for the Loader class, intended for manipulating dataframes.
    """

    def __init__(
            self, 
            loader: Loader, 
            tokenizer: Optional[str] = "tscholak/cxmefzzi",
            load_tokenizer: Optional[bool] = True,
        ):
        self.loader = loader
        self.tokenizer = T5TokenizerFast.from_pretrained(tokenizer) if load_tokenizer else None
    
    @cache     
    def create_contexts(
            self, 
            schema_serialization_type: Optional[str] = "peteshaw",
        ): 
        """Take the loaded Spider dataset and create contexts for each question.
        """
        if self.loader.spider is None:
            raise ValueError("Spider data not loaded.")
        if schema_serialization_type != "peteshaw":
            raise ValueError("Only peteshaw schema serialization is supported at this time.")
        for d in self.loader.spider['dev']:
            if d.get('formatted_schema') is None:
                raise ValueError("Formatted schema not found.")
            d['context'] = d['question'] + d['formatted_schema']
        for t in self.loader.spider['train']:
            if t.get('formatted_schema') is None:
                raise ValueError("Formatted schema not found.")
            t['context'] = t['question'] + t['formatted_schema']
        return self.loader.spider
    
    @cache
    def tokenize_value(
            self,
            to_tokenize: Optional[str] = "context",
        ):
        """Tokenize the contexts of the Spider dataset.
        """
        if self.loader.spider is None:
            raise ValueError("Spider data not loaded.")
        if self.tokenizer is None:
            raise ValueError("Tokenizer not loaded.")
        for d in self.loader.spider['dev']:
            if d.get(to_tokenize) is None:
                raise ValueError("Context not found.")
            d[f'tokenized_{to_tokenize}'] = self.tokenizer(d[to_tokenize])
        for t in self.loader.spider['train']:
            if t.get('context') is None:
                raise ValueError("Context not found.")
            t[f'tokenized_{to_tokenize}'] = self.tokenizer(t[to_tokenize])
        return self.loader.spider
    
    def tokenize_values(
        self,
        values: List[str],
    ):
        """A function for tokenizing multiple values.
        """
        for v in values:
            self.tokenize_value(v)
