from clusteringFunctions import *

# FLAGS AND INITIAL VALUES -----------------
FOLDERNAME = "DI-R50_Data/Clustering"
EMBED_FLAG = False

# LOAD PICKLES ----------------------------
# [condID, condDescr, techDescr], log expr, [preds], [vars], [predDescrs]
postDI = loadPkl(FOLDERNAME, "DI-R50_Post_Unique")

preDI = loadPkl(FOLDERNAME, "DI-R50_Pre_Unique")

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

print(postPredDescrs[0:5])

if EMBED_FLAG:
    embedsPost = getEmbeds([item for cond in postDI for item in cond[5]])
    embedsPre = getEmbeds([item for cond in preDI for item in cond[5]])
    np.savetxt('data/DI-R50_Data/PostDI-R50_embeddings.txt', embedsPost)
    np.savetxt('data/DI-R50_Data/PreDI-R50_embeddings.txt', embedsPre)
else:
    embedsPost = np.loadtxt("data/DI-R50_Data/PostDI-R50_embeddings.txt")
    embedsPre = np.loadtxt("data/DI-R50_Data/PreDI-R50_embeddings.txt")

# Change everything to normal floats
testPost = embedsPost.tolist()
testPre = embedsPre.tolist()

testPost = [[float(x) for x in arr] for arr in testPost]
testPre = [[float(x) for x in arr] for arr in testPre]

all = []

for x in zip(postPredNames + prePredNames, postPredDescrs + prePredDescrs, postPredCDescrs + prePredCDescrs, testPost + testPre):
    all.append(list(x))

savePkl(FOLDERNAME, "DI-R50_CLUSTER_READY_ALL", all)


