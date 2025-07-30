# ##################################################################
#
# Copyright 2024 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Aanchal Kavedia (aanchal.kavedia@teradata.com)
# Secondary Owner: Sukumar Burra (sukumar.burra@teradata.com)
#
# Notes:
#   * This code is only for internal use.
#   * The script is used in apply query for entity recognition
#     using 'roberta-large-ontonotes5' hugging face model.
# ##################################################################
# -*- coding: utf-8 -*-
import json
import sys
import warnings

from transformers import (AutoModelForTokenClassification, AutoTokenizer,
                          pipeline)

warnings.simplefilter('ignore')
input_str = sys.stdin.read()

DELIMITER = '#'
if len(input_str) > 0:
    torch_device = 'cuda'
    model_path = "./models/roberta-large-ontonotes5"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForTokenClassification.from_pretrained(model_path)
    translator = pipeline("token-classification", model=model, tokenizer=tokenizer,
                          device=torch_device, aggregation_strategy='max')

    for line in input_str.splitlines():
        results = translator(line)
        dict_val = {'ORG': [], 'PERSON': [], 'DATE': [], 'PRODUCT': [],
                    'GPE': [], 'EVENT': [], 'LOC': [], 'WORK_OF_ART': []}
        i = 0
        while i < len(results):
            if results[i]['entity_group'] in dict_val:
                dict_val[results[i]['entity_group']].append(results[i]['word'])
            i += 1
        combined_str = ""
        for key, val in dict_val.items():
            combined_str = '{}{}{}'.format(combined_str, DELIMITER, ",".join(val))

        print('{}{}'.format(line, combined_str))
