from math import inf
from classes.edge import Edges, Edge

class Circuit:
    def __init__(self, l=None, all_edges=None):
        self.edges = []
        if isinstance(l, list) and isinstance(all_edges, Edges):
            for L in l:
                id1, id2, dist = int(L[0]), int(L[1]), float(L[2])
                edge = all_edges.findEdgeByNodeIdsAndDistance(id1, id2, dist, create_reverse_edge_even_if_not_doubleway=True)
                self.edges.append(edge)

    def __repr__(self):
        return_s = "Nodes list \n"
        for e in self.edges:
            return_s += str(e.node1.id) + " , " + str(e.node2.id) + " , " + str(e.osmid) + "\n"
        return return_s + "END \n"

    def addEdge(self, edge):
        if isinstance(edge, Edge):
            self.edges.append(edge)
        else:
            raise TypeError("Data to add should be Edge type")

    def addCircuit(self, circuit):
        if isinstance(circuit, Circuit):
            for e in circuit.edges:
                self.addEdge(e)
        else:
            raise TypeError("Data to add should be Circuit type")

    def getExtremeLatLongs(self):
        latmin, latmax, longmin, longmax = inf, -inf, inf, -inf
        for edge in self.edges:
            for x in edge.path.lats:
                if x > latmax:
                    latmax = x
                elif x < latmin:
                    latmin = x
            for y in edge.path.longs:
                if y > longmax:
                    longmax = y
                elif y < longmin:
                    longmin = y
        return latmin, latmax, longmin, longmax
