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
#   * The script is used in apply query for performing sentiment analysis
#     using 'distilbert-base-uncased-emotion' hugging face model.
# ##################################################################
# -*- coding: utf-8 -*-
import sys
import warnings

import torch
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          pipeline)

warnings.simplefilter('ignore')
input_str = sys.stdin.read()

DELIMITER = '#'
if len(input_str) > 0:
    torch_device = 'cuda'
    model_path = './models/distilbert-base-uncased-emotion'
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    translator = pipeline("text-classification", model=model,
                          tokenizer=tokenizer, top_k=None, device=torch_device)

for line in input_str.splitlines():
    print('{}{}{}'.format(line, DELIMITER, translator(line)[0][0]['label']))