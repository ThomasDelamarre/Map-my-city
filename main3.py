from visualisation_tools import visualise_circuit_with_plt
from external_files_handler import readSolutionFromCsv, createGpxFromCircuit
from classes.circuit import Circuit
from prepare_data_for_postman_problem import getAllEdges

"""
filename = ?
number of graphs = ?
"""
number_graphs=12
filename = "Vaucresson_bike"

all_edges = getAllEdges(filename=filename)
print(all_edges)

#ITERATE SUR TOUS LES GRAPHS
#for i in range (number_graphs):

all_circuits = []

for i in range (number_graphs):
    solution = readSolutionFromCsv(filename + "_graph" + str(i))
    circuit = Circuit(solution, all_edges)
    all_circuits += [circuit]
    print(i, circuit)
    createGpxFromCircuit(circuit, filename + "_graph" + str(i))
    #visualise_circuit_with_plt(circuit, legend=False, time_between_frames=0.0000001)

createGpxFromCircuit(all_circuits, filename)
