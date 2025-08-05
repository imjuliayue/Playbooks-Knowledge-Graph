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
    # if(i % 500 == 0):
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
    with open(f"data/{FOLDERNAME}/{FILENAME}.pkl", 'rb') as f:
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

def output_as_csv(clusters, names, descr, sim_matrix):
  csv_data = []
  for i, cluster in enumerate(clusters):
    first = cluster[0]
    cluster_size = len(cluster)
    for node_idx in cluster:
        predicate = names[node_idx]
        predicate_desc = descr[node_idx]
        similarity_score = sim_matrix[node_idx][first]
        csv_data.append([i+1, predicate, predicate_desc, cluster_size, similarity_score])

  output_df = pd.DataFrame(csv_data, columns=['cluster_number', 'predicate', 'predicate_description', 'cluster_size', 'similarity_score'])
  output_df.to_csv('clustering_results_0.92.csv', index=False)
  return

# ---

def find_max_sim_pred_index(sim_matrix, baseline_index, clustered, threshold):
  max_score = 0
  max_index = -1
  for i in range(len(sim_matrix[baseline_index])):
    if (i != baseline_index) and (not clustered[i]) and (sim_matrix[baseline_index][i] > max_score) and (sim_matrix[baseline_index][i] > threshold):
      max_index = i
      max_score = sim_matrix[baseline_index][i]
  return max_index

# ---

def find_most_sim_to_cluster(sim_matrix, current_cluster, clustered, threshold):
  max_score = 0
  max_index = -1
  for i in range(len(sim_matrix)):
    temp_score = 0
    for pred_index in current_cluster:
      if (i not in current_cluster) and (not clustered[i]) and (sim_matrix[i][pred_index] > max_score) and (sim_matrix[i][pred_index] > threshold):
        temp_score += sim_matrix[i][pred_index]
    if temp_score / len(current_cluster) > max_score:
      max_score = temp_score / len(current_cluster)
      max_index = i
  return max_index

# ---

def sim_to_all_pred_in_cluster(sim_matrix, baseline_index, current_cluster, threshold):
  for pred_index in current_cluster:
    if sim_matrix[pred_index][baseline_index] < threshold:
      return False
  return True

# ---
      
def clustering_clique_method(sim_matrix, predicate_list, threshold=0.92):
    n = len(predicate_list)
    clustered = [False] * n
    temp_clustered = clustered.copy()
    final_clusters = []

    while not all(clustered):
      candidate_clusters = []
      for i in range(n):
        if not temp_clustered[i]:
          # create new cluster
          current_cluster = [i]
          temp_clustered[i] = True
          # add most similar not yet clustered predicate
          most_sim_pred_index = find_max_sim_pred_index(sim_matrix, i, temp_clustered, threshold)
          while most_sim_pred_index != -1:
            temp_clustered[most_sim_pred_index] = True
            current_cluster.append(most_sim_pred_index)

            most_sim_pred_index = find_most_sim_to_cluster(sim_matrix, current_cluster, temp_clustered, threshold)
            # for j in range(n):
            #   if not temp_clustered[j] and sim_to_all_pred_in_cluster(sim_matrix, j, current_cluster, threshold):
            #     temp_clustered[j] = True
            #     current_cluster.append(j)
          candidate_clusters.append(current_cluster)
      
      largest_cluster = max(candidate_clusters, key=len)
      for i in largest_cluster:
        clustered[i] = True
      final_clusters.append(largest_cluster)
      temp_clustered = clustered.copy()
      
    
    return final_clusters