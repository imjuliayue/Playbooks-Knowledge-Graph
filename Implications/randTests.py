import pandas as pd
import numpy as np
from S2MicroSem import * # NOTE: IF MICROSEM HAS SCRIPS, THOSE WILL RUN FIRST
from sklearn.metrics.pairwise import cosine_similarity

from implicationFunctions import *

# testAx = [["isSoftwareFor","x,y","x is a software component for y", "is a software component for"],["isSoftware","x","x is a software component", "is a software component"], ["isSoftware", "x", "x is a software component"]]

# testT = ["isSystem", "y", "y is a system component", "is a system component"]


Postcondition1 = ["all computers have been recorded", "all x : everything | computer[x] implies recorded[x]", ["computer", "recorded"],["x","y"], ["x is a computer", "y is recorded"], ["is a computer", "is recorded"]]   # all x : everything | computer[x] implies recorded[x]

Postcondition2 = ["if something is stored, then it is online", "all x : everything | stored[x] implies online[x]", ["stored", "online"], ["z","x"], ["z is stored", "x is online"], ["is stored","is online"]] # all x : everything | stored[x] implies online[x]

Postcondition3 = ["there is a computer", "some x : everything | computer[x]", ["computer"], ["x"], ["x is a computer"], ["is a computer"]]               # some x : everything | computer[x]

Precondition = ["a system component is online", "some x : systemComp[x] && online[x]", ["systemComp", "online"], ["z","x"], ["z is a system component", "x is online"], ["is a system component", "is online"]]               # some x : systemComp[x] && online[x]

embsPost,_ = getEmbeds([Postcondition1[0], Postcondition2[0], Postcondition3[0]])
embsPre,_ = getEmbeds([Precondition[0]])
conditionCM = cosine_similarity(embsPre,embsPost)

savePkl("Implications", "smallExCM", conditionCM)

allAsserts, totalInToks, totalOutToks, dictNoRepeats = cosSimPrecon(0,conditionCM[0],{},[Postcondition1,Postcondition2,Postcondition3],[Precondition])

# postPreds = [["computer", "x", "x is a computer", "is a computer"], ["recorded", "y", "y is recorded", "is recorded"], ["stored", "z", "z is stored", "is stored"], ["computer", "x", "x is a computer", "is a computer"]]

# prePreds = [["systemComp", "z", "z is a system component"], ["online", "x", "x is online", "is online"]]

# dictNoRepeats = {}

# allAsserts = []         # All Alloy assertions
# totalInToks = 0
# totalOutToks = 0


# # between precondition predicates and postcondition predicates
# for pred in prePreds:
#     asserts, intoks, outtoks = findAssertions(pred, postPreds, dictNoRepeats)
#     allAsserts.extend(asserts)
#     totalInToks += intoks
#     totalOutToks += outtoks

# print(f"test: {postPreds[0][3]}")

# postEmbs, _ = getEmbeds([postPreds[i][3] for i in range(len(postPreds))])
# matrix = cosine_similarity(postEmbs,postEmbs)
# matrix[matrix < 0.35] = 0

# for i,pred in enumerate(postPreds,0):
#     indices = np.where(matrix[i] != 0)[0]
#     print(indices)
#     simPostPreds = [postPreds[i] for i in indices]
#     asserts, intoks, outtoks = findAssertions(pred, simPostPreds, dictNoRepeats)
#     allAsserts.extend(asserts)
#     totalInToks += intoks
#     totalOutToks += outtoks

print(allAsserts)
print(totalInToks)
print(totalOutToks)

# savePkl("Implications", "SmallEXallasserts", allAsserts)

# arr = loadPkl ("Implications", "test1")


# with open("data/Implications/test1.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     for item in arr:
#         writer.writerow([item])

# CM = pd.read_csv("CosSimTest(S3).csv",header=None).to_numpy()

# sh = CM.shape

# labelsRow = CM[1:sh[0],0]
# labelsCol = CM[0,1:sh[1]]

# CM = CM[1:sh[0],1:sh[1]].astype(float)

# print(CM.shape)
# print(np.min(CM))
# print(np.max(CM))

# print(labelsRow)

# thresh = 0.13

# CM[(CM <= thresh)] = 0

# print(np.sum(CM == 0))



# df = pd.DataFrame(CM, index=labelsRow, columns=labelsCol)

# df.to_csv(f"CosSim{10}.{thresh}.csv")

