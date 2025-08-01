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
# -----------------------------------------

# OPEN AI CLIENT
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key = key)


# FUNCTIONS --------------------------------

def simplifyCondition(condition : str, context : str):
  # condition - string
  # context - string
  response = openai_client.chat.completions.create(
  model="gpt-4.1",
  messages=
    [
      {
          "role": "system",
          "content": f'''
                        You are given a condition. Context is provided, ONLY for resolving ambiguities. Simplify condition.
                        Simplifications are then turned to logical expressions, want it to be easy to do.
                        Condition may have unnecessary information. Remove it. (E.g. "If a match is found, a detection log is generated for auditing or alerting purposes", remove "for auditing or alerting purposes"; only care that it's generated.)
                        Condition may have examples. Remove it. (E.g. "A predefined response is triggered if verification fails, such as disabling devices or blocking operations", remove "such as disabling...")
                        If anything else is unnecessary, remove it or simplify it.
                        Do not change meaning of condition.
                        Only removals are substitutions allowed; no adding words.
                        Use reasoning, and on a new line write the final answer. For example, you would return:
                        <Reasoning>
                        FINAL ANSWER:
                        <simplified condition>.
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

