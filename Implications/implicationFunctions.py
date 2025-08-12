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

# PREDICATE IMPLICATION DETERMINATION (STEP 3) --------------------------------

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
                        You are given:
                        1) A SINGLE axiom predicate, each with: Predicate name (string), Natural-language description of its meaning, Number of variables it takes (arity)
                        2) A theorem predicate with: Predicate name, Natural-language description, Number of variables it takes (arity)

                        Your task:
                        Determine whether the axiom predicate implies the theorem predicate. Variables in axiom do not correspond to variables in theorem predicate whatsoever.
                        Assume the natural-language descriptions reflect real-world meanings.
                        Use common-sense reasoning to connect axioms to the theorem whenever plausible, even if the connection is not explicitly stated.
                        Only output "False." if there is truly no reasonable conceptual bridge from the axioms to the theorem.

                        Formalization rules:
                        All final expressions must be valid Alloy syntax.
                        You must respect the exact predicate names and their arity (number of variables) as given, assume the order of variable inputs to predicates matches the order of first appearance in description.
                        All variables used must be declared in a quantifier (all, some, one, no, etc.) before they appear in a predicate.
                        Alloy function application must use square brackets: PredicateName[var1, var2, ...].
                        Quantifiers must specify the type `everything`. Example: all x: everything | ....
                        You may combine predicates with logical operators: && (and), || (or), ! (not).
                        Parentheses must ensure correct grouping.

                        Output format:
                        A short reasoning section describing the hypothesized link between axioms and theorem.
                        FINAL ANSWER: followed by either "True." or "False."
                        If "True.", then immediately after, output:
                        EXPRESSIONS: a JSON array of one or more valid Alloy expressions that represent one or more logical implication from axioms to theorem.

                        Example output for a True case:
                        FINAL ANSWER:
                        True.
                        EXPRESSIONS:
                        ["all x: everything, y: everything | isSoftwareComponentFor[x,y] implies isSystemComponent[y]", "all x: everything | (some y: everything | isSoftwareComponentFor[x,y] implies isSystemComponent[x])"]

                        Example output for a False case:
                        FINAL ANSWER:
                        False.
                        Important:

                        Prefer "True." whenever a reasonable real-world interpretation makes the theorem follow from the axioms.
                        "False." should only be used if no logical path exists even with generous interpretation of the descriptions.
                        Alloy expressions must be syntactically valid and executable in Alloy Analyzer without modification
                        There may be more than one expression that can represent an implication! Depending on how you represent the variables and quantifers.
                        '''
      },
      {
          "role": "user",
          "content": "axioms: " + str(axiom) + "\ntheorem: " + str(pred)
      }
    ]
  )

  return  response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens

def predImplicationConjunction(axiom, pred):
  client = openai_client()
  response = client.chat.completions.create(
  model="gpt-4.1",
  messages=
    [
      {
          "role": "system",
          "content": f'''
                        You are given:
                        1) An axiom predicate with: Predicate name (string), Natural-language description of its meaning, Number of variables it takes (arity)
                        2) A theorem predicate with: Predicate name, Natural-language description, Number of variables it takes (arity)

                        Your task:
                        Assume the natural-language descriptions reflect real-world meanings in context of systems and security.
                        Determine whether the axiom predicate natural-language description implies the description of the theorem predicate.
                          Note: NOT necessary using the same variables in descriptions.
                        Use common-sense reasoning to connect axioms to the theorem whenever plausible, even if the connection is not explicitly stated.

                        Formalization rules:
                        All final expressions must be valid Alloy syntax.
                        You must respect the exact predicate names and their arity (number of variables) as given.
                        All variables used must be declared in a quantifier (all, some, one, no, etc.) before they appear in a predicate.
                        Alloy function application must use square brackets: PredicateName[var1, var2, ...].
                        Quantifiers must specify the type `everything`. Example: all x: everything | ....
                        You may combine predicates with logical operators: && (and), || (or), ! (not).
                        Parentheses must ensure correct grouping.

                        Output format:
                        A short reasoning section describing the hypothesized link between axioms and theorem.
                        FINAL ANSWER: followed by either "True." or "False."
                        If "True.", then immediately after, output:
                        EXPRESSION: the Alloy expression that represents the logical implication from axiom to theorem.
                        If "False.", then do not follow it with anything else.

                        Example output for a True case:
                        FINAL ANSWER:
                        True.
                        EXPRESSION:
                        all x : everything | isHardwareComp[x] => isSystemComp[x]

                        Example output for a False case:
                        FINAL ANSWER:
                        False.

                        Important:
                        Prefer "True." whenever a reasonable real-world interpretation makes the theorem follow from the axioms.
                        "False." should only be used if no logical path exists even with generous interpretation of the descriptions.
                        Alloy expressions must be syntactically valid and executable in Alloy Analyzer without modification.
                        '''
      },
      {
          "role": "user",
          "content": "axioms: " + str(axiom) + "\ntheorem: " + str(pred)
      }
    ]
  )

  return  response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens


def extractionFinalResult(output):
    # Returns None if the extraction does not contain "ANSWER:"
    x = output.split("ANSWER:")
    if(len(x) < 2):
       print("retry (no 'ANSWER:')")
       return None
    if("True" in x[-1]):
        x = x[-1].split("EXPRESSIONS:")
        if(len(x) < 2):
            print("true but (no 'EXPRESSION:')")
            return None
        return x[1].strip("\n")
    return "False"

def findAssertions(predicate, axioms, dictionary):
    # NOTE: HOW TO KEEP TRACK? 

    totalIn, totalOut = 0,0
    asserts = []
    # Get independent implications one by one.
    for x in axioms:
        if(x[0] == predicate[0]):
           print(f"{x[0]} and {predicate[0]} are the same predicate. Skipping...")
           continue
        res = None
        if(dictionary.get(x[0]) == None or predicate[0] not in dictionary.get(x[0])):
            print(f"{predicate[0]} not in dictionary for {x[0]}")
            if(dictionary.get(x[0]) == None):
               dictionary[x[0]] = []
            dictionary[x[0]].append(predicate[0])
            numVarsPred = len(predicate[1].split(","))
            numVarsX = len(x[1].split(","))
            print(f"numPred: {numVarsPred}, numX: {numVarsX}")
            # res is the resulting parsed raw output from ChatGPT. Any error will result in "None" being outputted.
            while(res == None):
                rawOut, inTok, outTok = predImplication([x[0],x[2],numVarsX], [predicate[0],predicate[2],numVarsPred])
                print(rawOut)
                res = extractionFinalResult(rawOut)
                if(res != "False"):
                    try:
                      lst= ast.literal_eval(res)
                      asserts.extend(lst)
                    except (SyntaxError, ValueError):
                      print("didn't work...")
                      res = None
                # Keep track of token count
                totalIn += inTok
                totalOut += outTok
        else:
          print(f"{predicate[0]} already in dictionary for {x[0]}")
    return asserts, totalIn, totalOut

# EMBEDDINGS (STEP 1-2) --------------------------------

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

# FILE SAVING -------------------------------------------------------

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
    
import re
    
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