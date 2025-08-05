from clusteringFunctions import *

# FLAGS AND INITIAL VALUES -----------------
FOLDEREXTRACT = "DI-R50_Data/Extraction"
FOLDERNAME = "DI-R50_Data/Clustering"
EMBED_FLAG = False

# LOAD PICKLES ----------------------------
# [condID, condDescr, techDescr], log expr, [preds], [vars], [predDescrs]
postDI = loadPkl(FOLDEREXTRACT, "DI-R50_Post_Unique")

preDI = loadPkl(FOLDEREXTRACT, "DI-R50_Pre_Unique")

# CLEAN PREDICATE DESCRIPTIONS -----------
cleanForCluster(postDI)
cleanForCluster(preDI)
# Now each of them have 5th is cleaned description

# EMBED ----------------------------------
# predicate names
postPredNames = [item for cond in postDI for item in cond[2]]
prePredNames = [item for cond in preDI for item in cond[2]]

print(postPredNames[0:5])

# predicate clean descriptions
postPredCDescrs = [item for cond in postDI for item in cond[5]]
prePredCDescrs = [item for cond in preDI for item in cond[5]]

print(postPredCDescrs[0:5])

# predicate uncleaned descriptions
postPredDescrs = [item for cond in postDI for item in cond[4]]
prePredDescrs = [item for cond in preDI for item in cond[4]]

# predicate variables
postPredVars = [item for cond in postDI for item in cond[3]]
prePredVars = [item for cond in preDI for item in cond[3]]

print(postPredDescrs[0:5])

print(len(postPredCDescrs),len(postPredDescrs),len(postPredNames))
print(len(prePredCDescrs),len(prePredDescrs),len(prePredNames))



if EMBED_FLAG:
    embedsPost = getEmbeds([item for cond in postDI for item in cond[5]])
    embedsPre = getEmbeds([item for cond in preDI for item in cond[5]])
    np.savetxt(f'data/{FOLDERNAME}/PostDI-R50_embeddings.txt', embedsPost)
    np.savetxt(f'data/{FOLDERNAME}/PreDI-R50_embeddings.txt', embedsPre)
else:
    embedsPost = np.loadtxt(f"data/{FOLDERNAME}/PostDI-R50_embeddings.txt")
    embedsPre = np.loadtxt(f"data/{FOLDERNAME}/PreDI-R50_embeddings.txt")

# Change everything to normal floats
testPost = embedsPost.tolist()
testPre = embedsPre.tolist()

testPost = [[float(x) for x in arr] for arr in testPost]
testPre = [[float(x) for x in arr] for arr in testPre]

all = []

for x in zip(postPredNames + prePredNames, postPredDescrs + prePredDescrs, postPredCDescrs + prePredCDescrs, postPredVars + prePredVars, testPost + testPre):
    all.append(list(x))

savePkl(FOLDERNAME, "DI-R50_CLUSTER_READY_ALL", all)


