from implicationFunctions import *
from sklearn.metrics.pairwise import cosine_similarity

FOLDERNAME = "DI-R50_Data/Implications"
EMBEDFLAG = True

# indices of D50 in full arrays.
Preinds = np.array([496, 189, 462, 346, 426, 353, 406, 484, 399, 407, 284, 372, 387, 480, 255, 190, 425, 350, 398, 432, 471, 376, 302, 201, 458, 345, 305, 183, 279, 457, 388, 269, 300, 420, 224, 355, 296, 447, 499, 465, 205, 414, 321, 297, 476, 437, 368, 498, 210, 287])
Postinds = np.array([123, 145, 287, 144, 124, 248, 247, 298, 317, 207, 242, 217, 319, 201, 288, 196, 150, 220, 153, 164, 294, 154, 336, 262, 184, 301, 191, 245, 161, 379, 252, 321, 358, 290, 141, 147, 194, 324, 125, 188, 282, 186, 344, 228, 223, 179, 255, 235, 175, 185])

valuesPostcondition = pd.read_csv('data/PostconditionsWTechDescr.csv', header=None).to_numpy()
valuesPrecondition = pd.read_csv('data/PreconditionsWTechDescr.csv', header=None).to_numpy()

# Randomly selected 50 postconditions and 50 preconditions
PostDI = valuesPostcondition[Postinds]
PreDI = valuesPrecondition[Preinds]

# Embed the postconditions and preconditions

if EMBEDFLAG: 
    embPost, costPost = getEmbeds(PostDI[:,1])
    embPre, costPre = getEmbeds(PreDI[:,1])

    print(f"Cost: {(costPost + costPre) / 130000}")

    np.savetxt(f"data/{FOLDERNAME}/R50PostCondEmbs.txt", embPost)
    np.savetxt(f"data/{FOLDERNAME}/R50PreCondEmbs.txt", embPre)
else:
    embPre = np.loadtxt(f"data/{FOLDERNAME}/R50PreCondEmbs.txt")
    embPost = np.loadtxt(f"data/{FOLDERNAME}/R50PostCondEmbs.txt")

# create cos matrix
CosMatrix = cosine_similarity(embPost,embPre) #rows = post, cols = pre
print(np.min(CosMatrix))
print(np.max(CosMatrix))


# no normalizing!

# threshold
thresh = 0.272
CosMatrix[CosMatrix < thresh] = 0

# Save CSV
labelsRow = PostDI[:,1]
labelsCol = PreDI[:,1]


df = pd.DataFrame(CosMatrix, index=labelsRow, columns=labelsCol)

df.to_csv(f"CosSim{thresh}.csv")

