from clusteringFunctions import *

test = modified_loadPkl('../data/DI-R50_Data/Clustering', 'DI-R50_CLUSTER_READY_ALL')

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

# path = "clustering_results"
# name = "clustering_after_chatGPT_naming"
# test_dict = create_cluster_dictionary(path, name)
# path_to_unique = "../data/DI-R50_Data/Extraction"
# save_file_path = "../data/replacement_test"
# replace_pred_with_cluster_names(path_to_unique, "DI-R50_Post_Unique", test_dict, save_file_path, "DI-R50_Post")
# replace_pred_with_cluster_names(path_to_unique, "DI-R50_Pre_Unique", test_dict, save_file_path, "DI-R50_Pre")

cluster_dict, cluster_names_list, cluster_descr_list = get_unique_clusters("../clustering/clustering_results", "clustering_after_chatGPT_naming")
# print(cluster_names_list)
output_unique_clusters_to_csv(cluster_names_list, cluster_descr_list, "unique_cluster_name_and_descr")
