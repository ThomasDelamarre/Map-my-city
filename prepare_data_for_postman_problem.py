from classes.node import Node, Nodes
from classes.edge import Edge, Edges
import webbrowser


def getAllEdgesFromOsm(filename):
    # Open .graphml files
    file = open("raw_data_from_OSM/" + filename + ".graphml", 'r', encoding="utf-8")
    file_lines = file.readlines()

    file_extended = open("raw_data_from_OSM/" + filename + "_extended.graphml", 'r', encoding="utf-8")
    file_extended_lines = file_extended.readlines()

    # Extract data from .graphml files
    keys = findKeys(file_lines)
    nodes = findNodes(file_lines, keys)
    edges = findEdges(file_lines, nodes, keys, required=1)

    """keys_extended = findKeys(file_extended_lines)
    nodes_extended = findNodes(file_extended_lines, keys_extended)
    edges_extended = findEdges(file_extended_lines, nodes_extended, keys_extended, required=0)

    edges_output = mergeEdgesLists(edges, edges_extended)"""

    edges_output = edges

    # Clean edges list
    edges_output = removeMotorways(edges_output)
    edges_output = removeStairs(edges_output)
    edges_output = removePaths(edges_output)
    edges_output = removeParkings(edges_output)
    edges_output = removeTunnels(edges_output)

    edges_output = markDoubleOneWaysAsDoubleWays(edges_output)
    edges_output = mergeEdgesThatCouldBeOne(edges_output)

    return edges_output


def mergeEdgesLists(edges1, edges2):
    output = edges1
    for edge in edges2.edges:
        if not output.includes(edge):
            output.addEdge(edge)
    return output


def isolateUnlinkedGraphs(edges):
    graphs = __findSubGraphs(edges)
    for i in range(len(graphs)):
        graphs[i] = Edges(graphs[i])
    return graphs


def findKeys(lines):
    keys = {}
    for line in lines:
        line.strip()
        # Weird as it seems, lat longs are called x and y if the graph is unprojected
        if "\"x\"" in line:
            keys["lat"] = __getIdFromLine(line)
        if "\"y\"" in line:
            keys["lon"] = __getIdFromLine(line)
        if "\"geometry\"" in line:
            keys["path"] = __getIdFromLine(line)
        if "\"osmid\"" in line and "\"node\"" in line:
            keys["osmid_node"] = __getIdFromLine(line)
        if "\"osmid\"" in line and "\"edge\"" in line:
            keys["osmid_edge"] = __getIdFromLine(line)
        if "\"name\"" in line and "\"edge\"" in line:
            keys["name"] = __getIdFromLine(line)
        if "\"length\"" in line and "\"edge\"" in line:
            keys["length"] = __getIdFromLine(line)
        if "\"oneway\"" in line and "\"edge\"" in line:
            keys["oneway"] = __getIdFromLine(line)
        if "\"highway\"" in line and "\"edge\"" in line:
            keys["highway"] = __getIdFromLine(line)
        if "\"service\"" in line and "\"edge\"" in line:
            keys["service"] = __getIdFromLine(line)
        if "\"tunnel\"" in line and "\"edge\"" in line:
            keys["tunnel"] = __getIdFromLine(line)
        if "\"access\"" in line and "\"edge\"" in line:
            keys["access"] = __getIdFromLine(line)
    return keys


def findNodes(lines, keys):
    nodes = Nodes()
    i = 0
    while i < (len(lines)):
        line = lines[i].strip()
        if "<node" in line:
            lat, lon, id = 0, 0, 0
            id = __getNodeIdFromLine(line)
            while "</node" not in line:
                i += 1
                line = lines[i].strip()
                if keys["lat"] in line:
                    lat = __getFloatFromLine(line)
                if keys["lon"] in line:
                    lon = __getFloatFromLine(line)
            nodes.addNode(Node(id, lat, lon))
        i += 1
    return (nodes)


def findEdges(lines, nodes, keys, required):
    edges = Edges()
    i = 0
    while i < (len(lines)):
        line = lines[i].strip()
        if "<edge" in line:
            length, osmids, oneway, name, path, highway, service, tunnel, access = 0, 0, False, "", "", "", "", "", ""
            node1, node2 = __getNodesFromLine(line, nodes)

            while "</edge" not in line:
                i += 1
                line = lines[i].strip()
                if keys["length"] in line:
                    length = round(float(line[16:-7]), 3)
                if keys["oneway"] in line:
                    oneway = __str2bool(line[16:-7])
                if keys["osmid_edge"] in line:
                    osmids = __getEdgesIdsFromLine(line)
                if keys["name"] in line:
                    name = line[15:-7]
                if keys["path"] in line:
                    path = line[16:-7]
                if keys["highway"] in line:
                    highway = line[16:-7]
                if keys["service"] in line:
                    service = line[16:-7]
                if keys["tunnel"] in line:
                    tunnel = line[16:-7]
                if keys["access"] in line:
                    access = line[16:-7]
            edges.addEdge(
                Edge(node1, node2, osmids, length, oneway, name, path, highway, service, tunnel, access, required))
        i += 1
    return (edges)


def __str2bool(v):
    return v == "True"


def __getNodesFromLine(line, nodes):
    keys = ["source=\"", "target=\""]
    ids = __getNumberForKeys(line, keys)
    return nodes.getNodeById(ids[0]), nodes.getNodeById(ids[1])


def __getNodeIdFromLine(line):
    keys = ["id=\""]
    id = __getNumberForKeys(line, keys)
    return id[0]


def __getEdgesIdsFromLine(line):
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    id = ""
    ids = []
    i = 0
    while i < (len(line)):
        while line[i] in numbers:
            id += line[i]
            i += 1
        if id != "" and len(id) != 1:  # len(id) = 1 if d9
            ids.append(int(id))
        id = ""
        i += 1
    return ids


def __getNumberForKeys(line, keys):
    ids = list()
    for key in keys:
        id = ""
        index = line.find(key) + len(key)
        while line[index].isdigit():
            id += line[index]
            index += 1
        ids += [int(id)]
    return (ids)


def __getFloatFromLine(line):
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"]
    nb = ""
    floats = []
    i = 0
    while i < (len(line)):
        while line[i] in numbers:
            nb += line[i]
            i += 1
        if nb != "":
            floats.append(nb)
        nb = ""
        i += 1
    return float(floats[1])


def __getIdFromLine(line):
    for i in range(30):
        key = "\"d" + str(i) + "\""
        if key in line:
            return key
    raise ValueError("No key found")


def markDoubleOneWaysAsDoubleWays(edges):
    seen = {}
    for edge in edges.edges:
        if edge.length not in seen.keys():
            seen[edge.length] = edge
        else:
            if seen[edge.length].node1 == edge.node2 and seen[edge.length].node2 == edge.node1:
                seen[edge.length].oneway = False

    keys = list(seen)
    reduced_edges = Edges()
    for key in keys:
        reduced_edges.addEdge(seen[key])

    return reduced_edges


def getNodesLinkedToNEdges(edges, n):
    nodes = {}
    for edge in edges.edges:
        if edge.node1.id in nodes.keys():
            nodes[edge.node1.id] += 1
        else:
            nodes[edge.node1.id] = 1

        if edge.node2.id in nodes.keys():
            nodes[edge.node2.id] += 1
        else:
            nodes[edge.node2.id] = 1

    keys_to_pop = []
    for node in nodes.keys():
        if nodes[node] != n:
            keys_to_pop.append(node)

    for key in keys_to_pop:
        nodes.pop(key)

    return nodes.keys()


def checkNodesInBrowser(nodes_to_check):
    nodes_id = list(nodes_to_check)
    if len(nodes_id) < 15:
        for id in nodes_id:
            webbrowser.open('https://www.openstreetmap.org/node/' + str(id), new=2)
    else:
        ("Too many possible false nodes: ", str(len(nodes_id)))


def doubleDeadEnds(edges):
    nodes = getNodesLinkedToNEdges(edges, n=1)
    for edge in edges.edges:
        if edge.node1.id in nodes or edge.node2.id in nodes:
            edge.oneway = False
    return edges


def __findGraphId(id, graphs):
    for i, graph in enumerate(graphs):
        for edge in graph:
            if id == edge.node1.id or id == edge.node2.id:
                return (i)
    return ("Error")


def __findSubGraphs(edges):
    graph_nodes = set()
    graphs = [[]]
    for edge in edges.edges:
        if edge.node1.id in graph_nodes and edge.node2.id in graph_nodes:
            id1 = __findGraphId(edge.node1.id, graphs)
            id2 = __findGraphId(edge.node2.id, graphs)
            if (id1 != id2):
                graphs[id1] += graphs[id2]
                graphs[id2] = []
            graphs[id1].append(edge)

        elif edge.node1.id in graph_nodes and edge.node2.id not in graph_nodes:
            graph_nodes.add(edge.node2.id)
            id1 = __findGraphId(edge.node1.id, graphs)
            graphs[id1].append(edge)

        elif edge.node1.id not in graph_nodes and edge.node2.id in graph_nodes:
            graph_nodes.add(edge.node1.id)
            id2 = __findGraphId(edge.node2.id, graphs)
            graphs[id2].append(edge)

        elif edge.node1.id not in graph_nodes and edge.node2.id not in graph_nodes:
            graph_nodes.add(edge.node1.id)
            graph_nodes.add(edge.node2.id)
            graphs += [[edge]]

    while [] in graphs:
        graphs.remove([])

    return (graphs)


def mergeEdgesThatCouldBeOne(edges):
    nodes_ids = getNodesLinkedToNEdges(edges, n=2)
    error_factor = 0
    while len(nodes_ids) - error_factor > 0:
        id = list(nodes_ids)[0]
        edges_to_merge = edges.findEdgesByNodeId(id)
        if len(edges_to_merge) == 1:
            error_factor += 1
        if len(edges_to_merge) == 2:  # To avoid errors when edges are roundabouts and node1 = node2
            edges.mergeEdges(edges_to_merge, id)
        nodes_ids = getNodesLinkedToNEdges(edges, n=2)
    return edges


def removeMotorways(edges):
    to_remove = []
    for edge in edges.edges:
        if "motorway" in edge.highway:
            to_remove.append(edge)
    edges.removeEdges(to_remove)
    return edges


def removePaths(edges):
    to_remove = []
    for edge in edges.edges:
        if "path" in edge.highway:
            to_remove.append(edge)
    edges.removeEdges(to_remove)
    return edges


def removeStairs(edges):
    to_remove = []
    for edge in edges.edges:
        if "steps" in edge.highway:
            to_remove.append(edge)
    edges.removeEdges(to_remove)
    return edges


def removeParkings(edges):
    to_remove = []
    for edge in edges.edges:
        if "parking" in edge.service:
            to_remove.append(edge)
    edges.removeEdges(to_remove)
    return edges


def removeTunnels(edges):
    to_remove = []
    for edge in edges.edges:
        if "yes" in edge.tunnel:
            to_remove.append(edge)
    edges.removeEdges(to_remove)
    return edges


def removePrivateService(edges):
    to_remove = []
    for edge in edges.edges:
        if "private" in edge.access and "service" in edge.highway:
            to_remove.append(edge)
    edges.removeEdges(to_remove)
    return edges
