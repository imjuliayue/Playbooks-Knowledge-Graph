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
# openai_client = OpenAI(api_key = )