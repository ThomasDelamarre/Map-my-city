from prepare_data_for_postman_problem import createChinesePostmanInputs
from visualisation_tools import visualise_graph
from solve_postman_problem import solvePostmanProblem
from external_files_handler import createCsvFromEdges



#filename = input("Filename: ?")
filename = "Vaucresson_bike"

graphs = createChinesePostmanInputs(filename)
print(graphs[0])

print("Number of graphs: " + str(len(graphs)))
for i in range(len(graphs)):
    print("\t Graph " + str(i) + ": " + str(len(graphs[i].edges)) + " edges")


for i, graph in enumerate(graphs):

    print("\n\n************************************************************************************")
    print("\t\t\t\t\t\t\t\t\tGraph" + str(i))
    print("************************************************************************************\n")

    name = filename + "_graph" + str(i)

    #Save graph in pdfs
    """visualise_graph(graph, name)"""

    #Create csv files for each graph
    createCsvFromEdges(graph, name + ".csv")

    # Solve postman problems for all graphs
    # TODO ATTENTION FONCTIONNE AVEC DES EDGES NON DIRECTIONNELS
    solvePostmanProblem(name)













