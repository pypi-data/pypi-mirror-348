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
#   * The script is used in apply query for recognizing pii
#     using 'deberta_finetuned_pii' hugging face model.
# ##################################################################
# -*- coding: utf-8 -*-
import sys
import warnings
import json

warnings.simplefilter('ignore')
input_str = sys.stdin.read()

DELIMITER = '#'
if len(input_str) > 0:
    # Load model directly
    from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

    model_path = "./models/deberta_finetuned_pii"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForTokenClassification.from_pretrained(model_path)
    pipe = pipeline("token-classification", model=model, tokenizer=tokenizer,
                    device='cuda', aggregation_strategy='first')

    l_s = []
    for line in input_str.splitlines():
        l_s = []
        prediction = pipe(line)
        for p in prediction:
            l_s.append(p['word'])
        print('{}{}{}'.format(line, DELIMITER, ','.join(l_s)))
