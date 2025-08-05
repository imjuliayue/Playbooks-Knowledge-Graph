from sklearn.metrics.pairwise import cosine_similarity

# IMPORTS --------------------------------
from dotenv import load_dotenv
import os
from openai import OpenAI

import numpy as np

import pandas as pd

import csv

import pickle as pkl

import json

from tenacity import retry, wait_random_exponential, stop_after_attempt

import re

from sklearn.metrics.pairwise import cosine_similarity

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
    with open(f"../data/{FOLDERNAME}/{FILENAME}.pkl", 'rb') as f:
        return pkl.load(f)
    
# ---

def cleanForCluster(condDI):
  # condDI is a list of lists, each list is [cond, descr, techDescr], log, [preds], [vars], [descr w vars]
  # returns nothing; edits in place
  # NOTE: function adds another column to processed csv --> removes variables from predicate descriptions.
  for cond in condDI:
      descrs = cond[4]
      vars = cond[3]
      cleanedDescr = []
      for descr,var in zip(descrs,vars):
        descr = " " + descr + " "
        descr = re.sub(r":", " is", descr)
        descr = re.sub(r",", "", descr)
        descr = re.sub(r"\b(x|y|z|w)(?:'s)?\b", " ", descr)
        descr = ' '.join(descr.strip().split())
        cleanedDescr.append(descr)
        # cleanedDescr.append(descr + f" {len(var)} VARIABLES")
      cond.append(cleanedDescr)

# ---

def get_pred_list(pkl):
    names = []
    descr = []
    embeds = []

    for i in range(len(pkl)):
        # index 0 contains predicate name
        names.append(pkl[i][0])
        # index 1 contains predicate descr (with vars)
        # index 2 contains predicate descr (withOUT vars)
        descr.append(pkl[i][1])
        # index 3 contains embedding
        embeds.append(pkl[i][3])
    cosine_sim_matrix = cosine_similarity(np.array(embeds))
    return (np.array(names), np.array(descr), cosine_sim_matrix)

# ---



# ---
      
def clustering_clique_method(similarity_matrix, predicate_list, threshold=0.9):
    n = len(predicate_list)
    clustered = [False] * n
    clusters = []

    while not all(clustered):
        # create clusters
        candidate_clusters = []
        for i in range(n):
          if clustered[i]:
              continue
          # new cluster
          current_cluster = [i]
          while True:
              best_candidate = -1
              best_min_similarity = -1
              for j in range(n):
                  if clustered[j] or j in current_cluster:
                      continue
                  similarities = [similarity_matrix[j][member] for member in current_cluster]
                  min_similarity = min(similarities)
                  if min_similarity >= threshold and min_similarity > best_min_similarity:
                      valid_clique = True
                      # check clique is valid
                      for member1 in current_cluster:
                        for member2 in current_cluster:
                            if similarity_matrix[member1][member2] < threshold:
                                valid_clique = False
                                break
                        if not valid_clique:
                            break
                      # check sim with rest of cluster
                      if valid_clique:
                          for member in current_cluster:
                              if similarity_matrix[j][member] < threshold:
                                  valid_clique = False
                                  break
                      if valid_clique:
                          best_min_similarity = min_similarity
                          best_candidate = j
              if best_candidate != -1:
                  current_cluster.append(best_candidate)
              else:
                  break
          candidate_clusters.append(current_cluster)

        # get largest clique
        if candidate_clusters:
            largest_clique = max(candidate_clusters, key=len)
            # remove predicates in largest clique from pool
            for member in largest_clique:
                clustered[member] = True

            clusters.append(largest_clique)
        else:
            # if no clusters, append as single clusters
            for i in range(n):
                if not clustered[i]:
                    clusters.append([i])
                    clustered[i] = True

    return clusters