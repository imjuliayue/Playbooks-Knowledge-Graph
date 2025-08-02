from predicateExtractionFunctions import *

import pandas as pd

import json

import re

# FUNCTIONS --------------

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
    
def uniquifyNames(processed, i, d):
    # processed is a python list of [[logical expression, [pred1, pred2, ...], [var1, var2, ...], [descr1, descr2, ...]],...]
    # i is the starting index for nonunique names
    # d is the dictionary of all unique names
    # processed is modified in place
    # - turns all of the names in the list to a unique one.
    # returns next index for nonunique names
    for x in processed:
        for j in range(len(x[1])):
            predOG = x[1][j]
            pred = predOG.strip().rstrip(",.!?")
            if(d.get(pred) == None):
                d[pred] = 1
            else:
                pred = pred + str(i)
                i+=1
                d[pred] = 1
            x[1][j] = pred
            print(pred)
            escaped_predOG = re.escape(predOG)
            newexpr = re.sub(rf"(?<![a-zA-Z])({escaped_predOG})(\()", pred + "(", x[0])
            x[0] = newexpr
    return i
    
    
# ------------------------

# DATA ORGANIZATION --------------
# indices of D50 in full arrays.
Preinds = np.array([496, 189, 462, 346, 426, 353, 406, 484, 399, 407, 284, 372, 387, 480, 255, 190, 425, 350, 398, 432, 471, 376, 302, 201, 458, 345, 305, 183, 279, 457, 388, 269, 300, 420, 224, 355, 296, 447, 499, 465, 205, 414, 321, 297, 476, 437, 368, 498, 210, 287])
Postinds = np.array([123, 145, 287, 144, 124, 248, 247, 298, 317, 207, 242, 217, 319, 201, 288, 196, 150, 220, 153, 164, 294, 154, 336, 262, 184, 301, 191, 245, 161, 379, 252, 321, 358, 290, 141, 147, 194, 324, 125, 188, 282, 186, 344, 228, 223, 179, 255, 235, 175, 185])

valuesPostcondition = pd.read_csv('data/PostconditionsWTechDescr.csv', header=None).to_numpy()
valuesPrecondition = pd.read_csv('data/PreconditionsWTechDescr.csv', header=None).to_numpy()

# Randomly selected 50 postconditions and 50 preconditions
PostDI = valuesPostcondition[Postinds]
PreDI = valuesPrecondition[Preinds]

# -------------------------------



# EXTRACT DATA --------------

# Extract to string lists (not processed) and save them
FOLDERNAME = "DI-R50_Data"

# resultPosts = np.array(batchExtraction(PostDI))
# saveTxt(FOLDERNAME, "DI-R50_Post_StringExtract", resultPosts.tolist())
# resultPres = np.array(batchExtraction(PreDI))
# saveTxt(FOLDERNAME, "DI-R50_Pre_StringExtract", resultPres.tolist())

# ---------------------------


# PROCESS DATA --------------

LOADEXTRACTEDFLAG = True

if LOADEXTRACTEDFLAG:
    resultPres = loadTxt(FOLDERNAME, "DI-R50_Pre_StringExtract")
    resultPosts = loadTxt(FOLDERNAME, "DI-R50_Post_StringExtract")

# Process the extracted strings to lists
# Save processed data
# NOTE: writes files w.r.t WHERE RUNNING SCRIPT
assert len(resultPosts) == len(PostDI), "Postcondition extraction length mismatch"
assert len(resultPres) == len(PreDI), "Precondition extraction length mismatch"

# print(resultPres[0])
# lst= ast.literal_eval(resultPres[0])


processedPosts = processStringtoList(PostDI, resultPosts)
saveData("data/DI-R50_Data",processedPosts, 'DI-R50_Pre_Processed')

processedPres = processStringtoList(PreDI, resultPres)
saveData("data/DI-R50_Data",processedPres, 'DI-R50_Post_Processed')

# ---------------------------



# # UNIQUIFY NAMES --------------
# # TODO: add function to the functions file.

