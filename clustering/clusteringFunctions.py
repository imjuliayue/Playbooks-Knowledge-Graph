from sklearn.metrics.pairwise import cosine_similarity

# IMPORTS --------------------------------
from dotenv import load_dotenv
import os
from openai import OpenAI

import numpy as np

import pandas as pd

import csv

import pickle as pkl

import ast

from tenacity import retry, wait_random_exponential, stop_after_attempt

# -----------------------------------------

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
  emb = openai_client().embeddings.create(input = [text], model="text-embedding-ada-002")
  return emb.data[0].embedding

# ---

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def getEmbeds(values):
  embeds = []
  i = 0
  for item in values:
    embed = get_embed(item)
    if(i % 500 == 0):
        print(i)
    i+=1
    embeds.append(embed)
  return np.array(embeds)

# ---

# ---

def saveData(path, data, name):
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

def cleanForCluster():
   # NOTE: function adds another column to processed csv --> removes variables from predicate descriptions.
   pass