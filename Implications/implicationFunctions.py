# IMPORTS --------------------------------
from dotenv import load_dotenv
import os
from openai import OpenAI

import pandas as pd

import numpy as np

import json

import csv

from tenacity import retry, wait_random_exponential, stop_after_attempt
import pickle as pkl

import ast
# -----------------------------------------

# FUNCTIONS --------------------------------

# OPEN AI CLIENT
load_dotenv()
_openai_client = None

def openai_client():
    global _openai_client
    if(_openai_client is None):
        key = os.getenv("OPENAI_API_KEY")
        _openai_client = OpenAI(api_key = key)
    return _openai_client

# ---

def predImplication(axiom, pred):
  client = openai_client()
  response = client.chat.completions.create(
  model="gpt-4.1",
  messages=
    [
      {
          "role": "system",
          "content": f'''
                        You are given a list of axiom predicates and one theorem predicate.
                        Determine whether the axiom predicates imply the theorem predicate.
                        Include reasoning, and in the last line, write FINAL ANSWER: and include your final answer as either "True" or "False", like this:
                        FINAL ANSWER:
                        Output "True" or "False"
                        '''
      },
      {
          "role": "user",
          "content": "axioms: " + axiom + "\ntheorem: " + pred
      }
    ]
  )

  return  response.choices[0].message.content, response.usage[0], response.usage[1]

# FUNCTIONS --------------------------------

# OPEN AI CLIENT
load_dotenv()
_openai_client = None

def openai_client():
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _openai_client

# ---

def get_embed(text):
  emb = openai_client().embeddings.create(input = [text], model="text-embedding-3-large")
  return emb.data[0].embedding, emb.usage.prompt_tokens

# ---

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def getEmbeds(values):
  embeds = []
  totalToks=0
  i = 0
  for item in values:
    embed,tokens = get_embed(item)
    totalToks+=tokens
    # if(i % 500 == 0):
    print(i)
    i+=1
    embeds.append(embed)
  return np.array(embeds), totalToks

# ---

def saveData(path, name, data):
  # path is the path to save the data to (can include '../'), W.R.T. WHERE RUNNING SCRIPT
  # data is in the form of [[name, descr1, descr2, ...], [name2, descr1, descr2, ...], ...]
  # saves as CSV file with name as the first column and descriptions as the rest
  with open(f'{path}/{name}.csv', 'w', newline='') as f:
      writer = csv.writer(f)
      writer.writerows(data)

# ---

def loadData(path, name):
  # path is the path to load the data from (can include '../'), W.R.T. WHERE RUNNING SCRIPT
  # name is the name of the file to load
  # returns a list of lists, each list is [name, descr1, descr2, ...]
  with open(f'{path}/{name}.csv', 'r') as f:
      reader = csv.reader(f)
      return [row for row in reader]

# ---

# saves 1d array to txt file
def saveTxt(FOLDERNAME, FILENAME, ARRAY):
    # PATHWAY IS W.R.T. WHERE RUNNING SCRIPT
    with open(f"data/{FOLDERNAME}/{FILENAME}.json", 'w') as f:
        json.dump(ARRAY, f)
    # np.savetxt(f'data/{FOLDERNAME}/{FILENAME}', np.array(ARRAY).reshape((-1,1)),fmt="%s")

def loadTxt(FOLDERNAME, FILENAME):
    # PATHWAY IS W.R.T. WHERE RUNNING SCRIPT
    with open(f"data/{FOLDERNAME}/{FILENAME}.json", 'r') as f:
        return json.load(f)
    
def savePkl(FOLDERNAME, FILENAME, DATA):
    # PATHWAY IS W.R.T. WHERE RUNNING SCRIPT
    with open(f"data/{FOLDERNAME}/{FILENAME}.pkl", 'wb') as f:
        pkl.dump(DATA, f)

def loadPkl(FOLDERNAME, FILENAME):
    # PATHWAY IS W.R.T. WHERE RUNNING SCRIPT
    with open(f"data/{FOLDERNAME}/{FILENAME}.pkl", 'rb') as f:
        return pkl.load(f)
    
