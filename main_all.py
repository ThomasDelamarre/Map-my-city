from extract_data_with_OSMnx import extractCityFromOsm
from prepare_data_for_postman_problem import getAllEdges, isolateUnlinkedGraphs
from visualisation_tools import visualise_graph, visualise_circuit_with_plt
from solve_postman_problem import solvePostmanProblem
from external_files_handler import createCsvFromEdges, readSolutionFromCsv, createGpxFromCircuit
from classes.circuit import Circuit
import timeit
import os.path
import datetime.datetime


def main(create_pdf=False, visualise_solutions=False):
    city = "Vaucresson"
    network_type = "drive"
    #TODO NETWORK TYPE CHECK TO AVIOD PUBLIC PARCS + MOTORWAYS
    filename = city + "_" + network_type

    start_total = timeit.default_timer()
    now = datetime.datetime.now()
    print("Started at: " + str(now.hour) + "h" + str(now.minute) + "m" + str(now.second) + "s")
    start_step = timeit.default_timer()
    print("Step 1 - Extract data from OSM")

    if os.path.exists("raw_data_from_OSM/" + filename + ".graphml"):
        print("\tFile already downloaded")
    else:
        extractCityFromOsm(city, network_type, plot=visualise_solutions)
    stop_step = timeit.default_timer()
    print("Elapsed time: " + str(round(stop_step - start_step, 1)) + "s")

    print("Step 2 - Prepare OSM data for solve")
    start_step = timeit.default_timer()

    all_edges = getAllEdges(filename=filename)
    graphs = isolateUnlinkedGraphs(all_edges)

    stop_step = timeit.default_timer()
    print("\tNumber of graphs: " + str(len(graphs)))
    print("Elapsed time: " + str(round(stop_step - start_step, 1)) + "s")

    print("Step 3 - Solve postman problem for each graph")
    start_step = timeit.default_timer()

    for i, graph in enumerate(graphs):
        start = timeit.default_timer()

        print("\tGraph " + str(i) + "/" + str(len(graphs)) + ":")
        print("\t\tNumber of edges: " + str(len(graph.edges)))

        name = filename + "_graph" + str(i)

        # Save graph in pdfs
        if create_pdf:
            visualise_graph(graph, name)

        # Create csv files for each graph
        createCsvFromEdges(graph, name + ".csv")

        # Solve postman problems for all graphs
        # TODO ATTENTION FONCTIONNE AVEC DES EDGES NON DIRECTIONNELS
        solvePostmanProblem(name, write=False, write_minimal=True)

        stop = timeit.default_timer()
        print("\tDone -- " + str(round(stop - start, 1)) + "s")

    stop_step = timeit.default_timer()
    print("Elapsed time: " + str(round(stop_step - start_step, 1)) + "s")

    print("Step 4 - Convert solutions to .gpx")
    start_step = timeit.default_timer()

    all_circuits = []

    for i in range(len(graphs)):
        solution = readSolutionFromCsv(filename + "_graph" + str(i))
        circuit = Circuit(solution, all_edges)
        all_circuits += [circuit]
        createGpxFromCircuit(circuit, filename + "_graph" + str(i))
        if visualise_solutions:
            visualise_circuit_with_plt(circuit, legend=False, time_between_frames=0.0000001)

    createGpxFromCircuit(all_circuits, filename)

    stop_step = timeit.default_timer()
    print("Elapsed time: " + str(round(stop_step - start_step, 1)) + "s")

    stop_total = timeit.default_timer()
    print("Process finished in: " + str(round(stop_total - start_total, 1)) + "s")


if __name__ == "__main__":
    main()
