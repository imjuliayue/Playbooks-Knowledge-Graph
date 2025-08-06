from clusteringFunctions import *

def modified_loadPkl(FOLDERNAME, FILENAME):
    # PATHWAY IS W.R.T. WHERE RUNNING SCRIPT
    with open(f"../data/{FOLDERNAME}/{FILENAME}.pkl", 'rb') as f:
        return pkl.load(f)

test = modified_loadPkl('DI-R50_Data/Clustering', 'DI-R50_CLUSTER_READY_ALL')

names, descr, variables, sim_matrix = get_pred_list(test)

# print(variables)
# print(names[194])
# print(descr[194])

# print(names[195])
# print(descr[195])

# print(names[196])
# print(descr[196])
# print(len(sim_matrix))
# print(len(sim_matrix[0]))

# sim_matrix = normalize_sim_matrix(sim_matrix)
# clusters = clustering_clique_method(sim_matrix, names, variables, 0.825)
# output_as_csv(clusters, names, descr, variables, 0.825)

#prompt used:
# You will be given a csv file that contains the following headers: cluster_number,predicate,predicate_description,vars,cluster_size

# For each cluster, add only two new columns that contain a predicate name and description that accurately represents the cluster as a whole. export the result as a csv.

path = "clustering_results"
name = "clustering_after_chatGPT_naming"
test_dict = create_cluster_dictionary(path, name)
print(test_dict['PartOf61'])
