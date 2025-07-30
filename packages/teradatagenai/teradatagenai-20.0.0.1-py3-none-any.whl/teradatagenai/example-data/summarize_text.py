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
#   * The script is used in apply query for summarizing
#     text using 'bart-large-cnn' hugging face model.
# ##################################################################
# -*- coding: utf-8 -*-
import sys
import warnings

import torch

warnings.simplefilter('ignore')
input_str = sys.stdin.read()

DELIMITER = '#'
if len(input_str) > 0:    
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
    torch_device = 'cuda'
    model_ckpt = "./models/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_ckpt)

    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, device=torch_device)

    for line in input_str.splitlines():
        print('{}{}{}'.format(line, DELIMITER, summarizer(line)[0]['summary_text']))