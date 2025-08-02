# IMPORTS --------------------------------
from dotenv import load_dotenv
import os
from openai import OpenAI

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import pandas as pd
import csv

import pickle as pkl
# from google.colab import drive

import random

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

def extraction(condition, context):
  client = openai_client()
  response = client.chat.completions.create(
  model="gpt-4.1",
  messages=
    [
      {
          "role": "system",
          "content": f'''
                        We plan on creating a knowledge graph of cyber defense actions from (MITRE D3FEND Detect and Isolate) which maps logical actions from postconditions to preconditions. The first step is creating an ontoloy, which will be done through logical predicates. There will be a signature called everything; all objects are type everything.
                        Given a condition. And its context, ONLY for clarifying ambiguities.
                        Represent the condition with predicates.
                        Notice "distributive property" (e.g. "hardware or software components" is actually "hardware components or software components")
                        If unclear, use context to help understanding. (e.g. "image" used in context of disks => disk image instead of container image.)
                        If says something "may" or "could" happen, assume it will happen
                        (e.g. `...the process may be terminated` becomes `...the process will be terminated".
                        Always use quantifiers: "all" is for all, "some" is exists, "no" is none exist, "one" is exactly one exists (use only if it's really the only one), "lone" is 0 or 1.
                        Write logical expression in alloy formal logic modelling syntax. NO facts or signatures, ONLY predicates! Keep names and descriptions generic (have them work for wide range of objects). E.g. if x is an operational firewall, do Operational(x) and Firewall(x), NOT OperationalFirewall(x)
                        Return list containing: 1. logical expression, 2. list of singular predicate names, 3. list of corresponding variable input letters, 4. list of corresponding predicate descriptions (without predicate name), SIMPLE as possible.
                        EXPLAIN YOUR REASONING THROUGHOUT. On new line, output final answer alone, no explanation/extra text. Example: 
                        (config) The system denies access for the subject to the network.
                        You respond: 
                        FINAL ANSWER:
                        ["some x : everything, y : everything, z : everything | System[x] && Subject[y] && Network[z] && DeniesAccessTo[x,y,z]",
                          ["System", "Subject", "Network"; "DeniesAccess"],
                          ["x", "y", "z", "x,y,z"],
                          [" x is a system", " y is a subject", " x denies access for y to z "]
                        ]
                        NO nested predicates! E.g. something like Exists(Tool(x)) is NOT allowed.
                        About quantifiers: if statement applies to one object or has "the", it would be "some". and if statement applies to all objects then it's 'all')
                        do not use variables other than w, x, y, and z. Make sure they correspond to correct objects. Also try to surround variables with spaces in DESCRIPTIONS (" x ")
                        use reasoning, and be very careful with implies and quantifiers.
                        Condition may have unnecessary information. Remove it. (E.g. "If a match is found, a detection log is generated for auditing or alerting purposes", remove "for auditing or alerting purposes"; only care that it's generated.)
                        Condition may have examples. Remove it. (E.g. "A predefined response is triggered if verification fails, such as disabling devices or blocking operations", remove "such as disabling...")
                        If anything else is unnecessary, remove it or simplify it.
                        Do not change meaning of condition.
                        '''
      },
      {
          "role": "user",
          "content": "condition: " + condition + "\ncontext: " + context
      }
    ]
  )

  return  response.choices[0].message.content

# ---

def extractionFinalResult(output):
    x = output.split("ANSWER:\n")
    return x[1]

# ---

def fixExtraction(condition, context, extraction):
  client = openai_client()
  response = client.chat.completions.create(
  model="gpt-4.1",
  messages=
    [
      {
          "role": "system",
          "content": f'''
                        We plan on creating a knowledge graph of cyber defense actions from (MITRE D3FEND Detect and Isolate) which maps logical actions from postconditions to preconditions. There will be a signature called everything; all objects are type everything.
                        Given a condition. And its context, ONLY for clarifying ambiguities. And an extraction attempt.
                        Determine whether the extraction is valid or not given the prompt:
                        ---
                        Represent the condition with predicates.
                        Notice "distributive property" (e.g. "hardware or software components" is actually "hardware components or software components")
                        If unclear, use context to help understanding. (e.g. "image" used in context of disks => disk image instead of container image.)
                        If says something "may" or "could" happen, assume it will happen
                        (e.g. `...the process may be terminated` becomes `...the process will be terminated".
                        Always use quantifiers: "all" is for all, "some" is exists, "no" is none exist, "one" is exactly one exists (use only if it's really the only one), "lone" is 0 or 1.
                        Write logical expression in alloy formal logic modelling syntax. NO facts or signatures, ONLY predicates! Keep names and descriptions GENERIC and SIMPLE (have them work for wide range of objects). E.g. if x is an operational firewall, do Operational(x) and Firewall(x), NOT OperationalFirewall(x)
                        Return list containing: 1. logical expression, 2. list of singular predicate names, 3. list of corresponding variable input letters, 4. list of corresponding predicate descriptions (without predicate name), SIMPLE as possible.
                        EXPLAIN YOUR REASONING THROUGHOUT. On new line, output final answer alone, no explanation/extra text. Example: 
                        (config) The system denies access for the subject to the network.
                        You respond: 
                        FINAL ANSWER:
                        ["some x : everything, y : everything, z : everything | System[x] && Subject[y] && Network[z] && DeniesAccessTo[x,y,z]",
                          ["System", "Subject", "Network"; "DeniesAccess"],
                          ["x", "y", "z", "x,y,z"],
                          [" x is a system", " y is a subject", " x denies access for y to z "]
                        ]
                        Within the variables sublist, separate each element with semicolons!!!
                        NO nested predicates! E.g. something like Exists(Tool(x)) is NOT allowed.
                        About quantifiers: if statement applies to one object or has "the", it would be "some". and if statement applies to all objects then it's 'all')
                        About implications: if statement applies to only one TYPE of object, use implies (all x : everything | Baby[x] implies DrinksMilk[x], NOT all x : everything | Baby[x] && DrinksMilk[x])
                        do not use variables other than w, x, y, and z. Make sure they correspond to correct objects. Also try to surround variables with spaces in DESCRIPTIONS (" x ")
                        use reasoning, and be very careful with implies and quantifiers.
                        ---
                        Condition may have unnecessary information. Remove it. (E.g. "If a match is found, a detection log is generated for auditing or alerting purposes", remove "for auditing or alerting purposes"; only care that it's generated.)
                        Condition may have examples. Remove it. (E.g. "A predefined response is triggered if verification fails, such as disabling devices or blocking operations", remove "such as disabling...")
                        If anything else is unnecessary, remove it or simplify it.
                        Do not change meaning of condition.
                        KEEP PREDICATES AND DESCRIPTIONS GENERIC AND SIMPLE
                        provide reasoning and in a new line output your own extraction. Pay special attention to QUANTIFIERS, IMPLICATIONS, and variables or variable order.
                        <reasoning>
                        FINAL ANSWER:
                        <extraction>
                        '''
      },
      {
          "role": "user",
          "content": "condition: " + condition + "\ncontext: " + context + "\nprevious attempt: " + extraction
      }
    ]
  )

  return  response.choices[0].message.content

# ---

def batchExtraction(conditions):
  # conditions is a list of conditions, each condition is a list of [condition_name, condition_desc, condition_context]
  result = []
  i = 0
  for condition in conditions:
    #postcondition[2] contains desc

    # initial extraction of condition (WITH reasoning)
    res = extraction(condition[1], condition[2])

    # remove reasoning, get only extraction
    extractionResult = extractionFinalResult(res)

    # fix extraction
    res = fixExtraction(condition[1], condition[2], extractionResult)
    
    # remove reasoning, get only extraction
    res = extractionFinalResult(res)

    result.append(res)

    print("done " + str(i))
    i+=1
  return result

# ---

def saveData(path, data, name):
  # path is the path to save the data to (can include '../'), W.R.T. WHERE RUNNING SCRIPT
  # data is in the form of [[name, descr1, descr2, ...], [name2, descr1, descr2, ...], ...]
  # saves as CSV file with name as the first column and descriptions as the rest
  with open(f'{path}/{name}.csv', 'w', newline='') as f:
      writer = csv.writer(f)
      writer.writerows(data)

# ---

def string_to_list(extraction):
  # extraction is the string: [logical expression, [pred1; pred2; ...], [var1; var2; ...], [descr1; descr2; ...]]
  # returns list of the form [logical expression, [pred1, pred2, ...], [var1, var2, ...], [descr1, descr2, ...]]
  lst= ast.literal_eval(extraction)
  if(len(lst) != 4):
    print("Error: extraction string does not have 4 elements!")
    return None
  return lst

# ---

def processing_to_list(extraction_array,conditions):
  # extraction_array is a list of extraction strings
  #   NOT listified!
  # conditions is a list of conditions corresponding to the extractions

  # RETURNS:
  # - `result`
  result = []
  retry = []
  retryInds = []
  count=0
  for extraction in extraction_array:

    # turns extraction string into list
    res = string_to_list(extraction)

    # append everything to result (even if None, aka failed parse)
    result.append(res)
    if(res is None):
        # if parsing failed, append to retry and index to conditions
        retry.append(conditions[count])
        retryInds.append(count)
    count+=1

  # remove empty strings from result
  for i in result:
    # if i is None, skip
    if(i is None):
      continue
    i[1] = [j for j in i[1] if j != ""]
    i[2] = [j for j in i[2] if j != ""]
  
  return result, retry, retryInds

# ---

# BULK turns string to list
def processStringtoList(conditions, result):
  # conditions is an NP ARRAY of actual conditions ([condition_name, condition_desc, condition_context])
  # result is a list of extraction strings ([logical expression, [pred1; pred2; ...], [var1; var2; ...], [descr1; descr2; ...]])
  #   NOT listified!
  indices = np.array(range(len(conditions)))
  processed, retry, retryInds = processing_to_list(result, conditions[indices])
  print(len(retry))

  while(len(retry) != 0):
    again = batchExtraction(retry)

    # indices STILL correspond to the original conditions
    indices = indices[retryInds]

    reProcessed, retry, retryInds = processing_to_list(again, conditions[indices])
    print(len(retry))

    for idx, res in zip(indices, reProcessed):
      processed[idx] = res
    

  return processed


