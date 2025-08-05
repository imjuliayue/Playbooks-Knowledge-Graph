# IMPORTS --------------------------------
from dotenv import load_dotenv
import os
from openai import OpenAI

import numpy as np

import csv

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