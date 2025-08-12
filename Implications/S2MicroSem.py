from implicationFunctions import *
from sklearn.metrics.pairwise import cosine_similarity

Preinds = np.array([496, 189, 462, 346, 426, 353, 406, 484, 399, 407, 284, 372, 387, 480, 255, 190, 425, 350, 398, 432, 471, 376, 302, 201, 458, 345, 305, 183, 279, 457, 388, 269, 300, 420, 224, 355, 296, 447, 499, 465, 205, 414, 321, 297, 476, 437, 368, 498, 210, 287])
Postinds = np.array([123, 145, 287, 144, 124, 248, 247, 298, 317, 207, 242, 217, 319, 201, 288, 196, 150, 220, 153, 164, 294, 154, 336, 262, 184, 301, 191, 245, 161, 379, 252, 321, 358, 290, 141, 147, 194, 324, 125, 188, 282, 186, 344, 228, 223, 179, 255, 235, 175, 185])

valuesPostcondition = pd.read_csv('data/PostconditionsWTechDescr.csv', header=None).to_numpy()
valuesPrecondition = pd.read_csv('data/PreconditionsWTechDescr.csv', header=None).to_numpy()

# Randomly selected 50 postconditions and 50 preconditions
PostDI = valuesPostcondition[Postinds]
PreDI = valuesPrecondition[Preinds]

# READ THE UNIFIED FILES
PostUnified = loadPkl('replacement_test', "DI-R50_Post_Unified")
PreUnified = loadPkl('replacement_test', "DI-R50_Pre_Unified")

cleanForCluster(PostUnified)
cleanForCluster(PreUnified)

# LOAD COSINE SIMILARITY MATRIX (ROW = PRECONDITION)
cosSim = pd.read_csv('CosSim0.27.csv', skiprows=0, index_col=0).to_numpy().T

totalEmbedTok = 0

# FINDS POSTCONDITION PREDICATES IMPLYING PRECONDITION PREDICATES
def cosSimPrecon(i,cosSim):
    # i = index of PostDI of precondition
    # cosSim = the np cosine similarity vector for that precondition

    # Set up (find similar postcondition inds)
    SimPostInds = np.where(cosSim > 0)[0]
    print(f"# similar postconditions: {len(SimPostInds)}")

    # Collect all of the predicate names, variables, descriptions, and cleaned descriptions
    prePreds = PreUnified[i][2:6]
    print(prePreds)

    postPreds = [[x for j in SimPostInds for x in PostUnified[j][2]], [x for j in SimPostInds for x in PostUnified[j][3]], [x for j in SimPostInds for x in PostUnified[j][4]],[x for j in SimPostInds for x in PostUnified[j][5]]]
    print(f"# postcondition predicates: {len(postPreds[0])}")

    # Embed the cleaned descriptions
    embPost, costPost = getEmbeds(postPreds[3])
    embPre, costPre = getEmbeds(prePreds[3])

    # Create the cosine similarity matrix
    CosMatrix = cosine_similarity(embPre,embPost) #rows = post, cols = pre
    print(np.min(CosMatrix))

    # Set a low threshold of 0.13
    CosMatrix[(CosMatrix <= 0.13)] = 0

    df = pd.DataFrame(CosMatrix, index=prePreds[3], columns=postPreds[3])
    df.to_csv(f"zcosSimMsPred/CosSimTest{i}.(S3).csv")

    return np.sum(CosMatrix == 0)/CosMatrix.size, len(CosMatrix[0]), costPost + costPre



    # S3 -- IMPLICATIONS

    

# nonRetention, postP, tokens = 0,0,0
# for i in range(50):
#     ret, p, t = cosSimPrecon(i, cosSim[i])
#     nonRetention += ret
#     postP += p
#     tokens += t

# print(f"nonRet Avg: {nonRetention/50}")
# print(f"postP Avg: {postP/50}")
# print(f"total Toks: {tokens}")
# print(f"avg Toks: {tokens/50}")
# print(f"total cost: {tokens / 130000}")


