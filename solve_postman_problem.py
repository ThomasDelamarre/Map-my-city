from postman_problems.solver import cpp
from postman_problems.stats import calculate_postman_solution_stats
from external_files_handler import createCsvFromCircuit


def solvePostmanProblem(name, write=True, write_minimal=True):
    filename = "graphs_in_csv/" + name + ".csv"
    # find CPP solution
    circuit, graph = cpp(edgelist_filename=filename)
    if write:
        print(circuit)
    if write_minimal:
        print("\tNumber of edges walked: " + str(len(circuit)))

    """
    # print solution route
    for e in circuit:
        print(e)
    """

    if write:
        # print solution summary stats
        for k, v in calculate_postman_solution_stats(circuit).items():
            print(k, v)

    createCsvFromCircuit(circuit, name)
