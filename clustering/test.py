from clusteringFunctions import *

test = loadPkl('DI-R50_Data/Clustering', 'DI-R50_CLUSTER_READY_ALL')

names, descr, sim_matrix = get_pred_list(test)

print(names[194])
print(descr[194])

print(names[195])
print(descr[195])

print(names[196])
print(descr[196])
# print(len(sim_matrix))
# print(len(sim_matrix[0]))

# clusters = clustering_clique_method(sim_matrix, names, 0.95)
# output_as_csv(clusters, names, descr, sim_matrix)