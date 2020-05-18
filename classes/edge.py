from classes.path import Path


class Edge:
    __id = 0

    def __init__(self, node1, node2, osmid, length, oneway, name, path = "", highway = "", service = "", tunnel="", access="", required = 0):
        self.id = self.__id
        self.__class__.__id += 1
        self.node1 = node1
        self.node2 = node2
        self.osmid = osmid
        self.length = length
        self.oneway = oneway
        if name == "":
            self.name = str(osmid)
        else:
            self.name = name
        if isinstance(path, Path):
            self.path = path
        elif isinstance(path, str):
            self.path = Path(path, node1=node1, node2=node2)
        else:
            raise(TypeError("Expected path to be a Path or a String"))
        self.highway = highway
        self.service = service
        self.tunnel = tunnel
        self.access = access
        self.required = required

    def __repr__(self):
        return "Edge: " + str(self.name) + " // " + str(self.node1.id) + " // " + str(self.node2.id) + " // " + str(self.length) + " // " + str(self.path) + " // " + self.highway + "\n"

    def reverse(self):
        rev_path, lats, longs = self.path.reverse()
        reversed_path = Path(path=rev_path, lat=lats, long=longs)
        return Edge(self.node2, self.node1, self.osmid, self.length, self.oneway, self.name, reversed_path, self.highway, self.service, self.tunnel, self.access, self.required)


class Edges:
    def __init__(self, edges=None):
        if edges is None:
            edges = []
        self.edges = edges

    def __repr__(self):
        ret = str(len(self.edges)) + " Edges\n"
        for edge in self.edges:
            ret += str(edge)
        return ret

    def includes(self, edge):
        for e in self.edges:
            if e.node1 == edge.node1 and e.node2 == edge.node2 and e.length == edge.length and e.name == edge.length:
                return True
        return False

    def checkIfDuplicate(self, edge): #TODO Not the correct name for this function, should be smth like keeponly the longest
        for e in self.edges:
            if edge.name == e.name and edge.node2 == e.node2 and edge.node1 == e.node1:
                if edge.path.len > e.path.len:
                    self.removeEdge(e)
                    return edge
                else:
                    return None

            elif edge.osmid == e.osmid and edge.node2 == e.node2 and edge.node1 == e.node1:
                if edge.path.len > e.path.len:
                    self.removeEdge(e)
                    return edge
                else:
                    return None
        return edge

    def addEdge(self, edge):
        self.edges.append(edge)
        """ 
        else:
            raise ValueError("Edge already in the Edges()")
            SHOULD ADD SMTH TO CHECK IF EDGE ALREADY IN"""

    def removeEdges(self, edges):
        for edge in edges:
            self.removeEdge(edge)

    def removeEdge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)


    def findEdgeByOSMId(self, osmid):
        for edge in self.edges:
            if edge.osmid == osmid:
                return edge
        raise ValueError("No edge with this OSM id")

    def findEdgeByNodeIdsAndDistance(self, id1, id2, dist, create_reverse_edge_even_if_not_doubleway=False):
        for edge in self.edges:
            if edge.node1.id == id1 and edge.node2.id == id2 and round(edge.length, 3) == round(dist, 3):
                return edge
            elif (create_reverse_edge_even_if_not_doubleway or not edge.oneway) and (edge.node1.id == id2) and (edge.node2.id == id1) and (round(edge.length, 3) == round(dist, 3)):
                rev_edge = edge.reverse()
                self.addEdge(rev_edge)
                return rev_edge
        raise ValueError("Edge couldn't be find for the given length and node ids ", dist, id1, id2, self)

    def findEdgesByNodeId(self, id):
        to_ret = []
        for edge in self.edges:
            if edge.node1.id == id or edge.node2.id == id:
                to_ret.append(edge)
        return(to_ret)

    def mergeEdges(self, edges, middle_node):
        if edges[0].node2.id == middle_node and edges[1].node1.id == middle_node:
            left_edge = edges[0]
            right_edge = edges[1]
        elif edges[1].node2.id == middle_node and edges[0].node1.id == middle_node:
            left_edge = edges[1]
            right_edge = edges[0]
        elif edges[0].node1.id == middle_node and edges[1].node1.id == middle_node:
            left_edge = edges[0].reverse()
            right_edge = edges[1]
        elif edges[0].node2.id == middle_node and edges[1].node2.id == middle_node:
            left_edge = edges[0]
            right_edge = edges[1].reverse()

        self.removeEdge(right_edge)
        self.removeEdge(left_edge)

        new_path = Path("Preparation for merge")
        new_path.merge(left_edge.path, right_edge.path)
        self.addEdge(Edge(left_edge.node1, right_edge.node2, "Merge of " + str(left_edge.osmid) + str(right_edge.osmid), left_edge.length + right_edge.length, bool(left_edge.oneway * right_edge.oneway), "Merge of " + str(left_edge.name) + str(right_edge.name), new_path, left_edge.highway + "/" + right_edge.highway, left_edge.service + "/" + right_edge.service, left_edge.tunnel + "/" + right_edge.tunnel, left_edge.access + "/" + right_edge.access, left_edge.required*right_edge.required))





