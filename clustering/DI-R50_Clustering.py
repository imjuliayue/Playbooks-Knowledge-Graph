from clusteringFunctions import *

FOLDERNAME = "DI-R50_Data"

postDI = loadPkl(FOLDERNAME, "DI-R50_Post_Unique")

preDI = loadPkl(FOLDERNAME, "DI-R50_Pre_Unique")

cleanForCluster(postDI)
cleanForCluster(preDI)
# Now each of them have 5th is cleaned description


embedsPost = getEmbeds([item for cond in postDI for item in cond[5]])
embedsPre = getEmbeds([item for cond in preDI for item in cond[5]])

np.savetxt('PostDI-R50_embeddings.txt', embedsPost)
np.savetxt('PreDI-R50_embeddings.txt', embedsPre)

# Change everything to normal floats
testPost = embedsPost.tolist()
testPre = embedsPre.tolist()

testPost = [[float(x) for x in arr] for arr in testPost]
testPre = [[float(x) for x in arr] for arr in testPre]

for cond, emb in zip(postDI + preDI, testPost + testPre):
    cond.append(emb)

savePkl(FOLDERNAME, "DI-R50_CLUSTER_READY_ALL", postDI + preDI)


