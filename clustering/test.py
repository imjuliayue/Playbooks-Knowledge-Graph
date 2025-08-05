from clusteringFunctions import *

test = loadPkl('DI-R50_Data/Clustering', 'DI-R50_CLUSTER_READY_ALL')

names, descr, sim_matrix = get_pred_list(test)

print(len(test))
print(len(sim_matrix))
print(len(sim_matrix[0]))

