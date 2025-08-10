import pandas as pd
import numpy as np
from implicationFunctions import *

testAx = ["isSoftware","x is a software component", 1]

testT = ["isSystem", "y is a system component", 1]

print(predImplication(testAx, testT))

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

