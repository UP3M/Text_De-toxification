# -*- coding: utf-8 -*-
"""t5_predict.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rggL6ZrBHObliUnTKM2UFjVTEzf3QuLn
"""

!wget https://github.com/s-nlp/detox/blob/main/emnlp2021/data/test/test_10k_toxic

import pandas as pd
from transformers import T5ForConditionalGeneration, AutoTokenizer
import torch
from tqdm.auto import tqdm, trange
import gc

import torch

if torch.cuda.is_available():
  device = torch.device("cuda")
else:
  device = torch.device("cpu")

def cleanup():
    """
    A helpful function to clean all cached batches.
    """
    gc.collect()
    torch.cuda.empty_cache()
#Reading the inputs

# reference for test dataset https://github.com/s-nlp/detox/blob/main/emnlp2021/data/test/test_10k_toxic
file_path = '/content/test_10k_toxic.txt'

# Read the text file and split it into a list of sentences
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Split the content into a list of sentences, assuming each sentence is on a separate line
sentences = content.split('\n')

# Remove any empty or blank lines from the list of sentences
sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

# Print the list of sentences
print(sentences)

toxic_inputs = sentences
#Loading the model. For the baseline we used t5_model

base_model_name = 't5-small'
model_name = '/content/drive/MyDrive/t5_base_train_10000'
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
model.to(device);
# Paraphrasing preparation with small example

def paraphrase(text, model, n=None, max_length='auto', temperature=0.0, beams=3):
    texts = [text] if isinstance(text, str) else text
    inputs = tokenizer(texts, return_tensors='pt', padding=True)['input_ids'].to(model.device)
    if max_length == 'auto':
        max_length = int(inputs.shape[1] * 1.2) + 10
    result = model.generate(
        inputs,
        num_return_sequences=n or 1,
        do_sample=False,
        temperature=temperature,
        repetition_penalty=3.0,
        max_length=max_length,
        bad_words_ids=[[2]],  # unk
        num_beams=beams,
    )
    texts = [tokenizer.decode(r, skip_special_tokens=True) for r in result]
    if not n and isinstance(text, str):
        return texts[0]
    return texts
print(paraphrase(['you are idiot'], model, temperature=50.0, beams=10))

# The inference
para_results = []
problematic_batch = [] #if something goes wrong you can track such bathces
batch_size = 8

for i in tqdm(range(0, len(toxic_inputs), batch_size)):
    batch = [sentence for sentence in toxic_inputs[i:i + batch_size]]
    try:
        para_results.extend(paraphrase(batch, model, temperature=0.0))
    except Exception as e:
        print(i)
        para_results.append(toxic_inputs[i:i + batch_size])
# Saving the results

with open('t5_result.txt', 'w') as file:
    file.writelines([sentence+'\n' for sentence in para_results])