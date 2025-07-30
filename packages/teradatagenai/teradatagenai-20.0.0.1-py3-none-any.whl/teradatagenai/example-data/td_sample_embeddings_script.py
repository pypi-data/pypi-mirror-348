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
#   * The script is used in apply query for generating embeddings and
#     sentence_similarity using 'all-MiniLM-L6-v2', 'distilbert-base-uncased',
#     'albert-base-v2' and 'xlnet-base-cased' hugging face model.
#   * It performs mean_pooling to correct averaging.
#   * It also uses torch.nn.functional.normalize to normalize embeddings.
# ##################################################################

import importlib
import json
import re
import sys
import warnings

import torch
import torch.nn.functional as F
from sentence_transformers import util
from transformers import AutoTokenizer, pipeline

warnings.simplefilter('ignore')
input_str = sys.stdin.read()

model_name = sys.argv[1]
transformer_class = sys.argv[2]
task = sys.argv[3]

extra_kwargs = json.loads(sys.argv[4])
DELIMITER = extra_kwargs['delimiter']
api_type = extra_kwargs['func_name']

def extract_numbers(string):
   numbers = re.findall(r'\b\d+\.\d+|\b\d+', string)
   # Join numbers with a space or another desired separator.
   return ' '.join(numbers)

# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

if len(input_str) > 0:
    torch_device = 'cuda'
    model_path = f"./models/{model_name}"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = getattr(getattr(importlib.import_module("transformers"),
                            transformer_class), "from_pretrained")(model_path)

    for line in input_str.splitlines():
        sentences = line.strip()

        if api_type.lower() == 'sentence_similarity':
            sentences = line.strip().split('#')

        # Tokenize sentences
        encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = model(**encoded_input)

        # Perform pooling
        sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

        # Normalize embeddings
        model_output = F.normalize(sentence_embeddings, p=2, dim=1)

        if api_type.lower() == 'sentence_similarity':
            # Compute cosine-similarities for each sentence with each other sentence.
            cosine_scores = util.cos_sim(model_output[0], model_output[1])
            cosine_scores = extract_numbers(str(cosine_scores))
            print('{}{}{}{}{}'.format(sentences[0], DELIMITER, sentences[1], DELIMITER, cosine_scores))
        else:
            emb = DELIMITER.join([str(round(x, 6)) for x in model_output.tolist()[0]])
            out_txt = DELIMITER.join([line, emb])
            print(out_txt)