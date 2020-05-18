class Node:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.long = lon

    def __repr__(self):
        return "Node id:" + str(self.id) + " lat:" + str(self.lat) + " lon:" + str(self.long)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id


class Nodes:

    def __init__(self):
        self.nodes = []

    def __repr__(self):
        ret = str(len(self.nodes)) + " Nodes : "
        for node in self.nodes:
            ret += str(node)
        return ret

    def getNodeById(self, id):
        for node in self.nodes:
            if node.id == id:
                return node

    def addNode(self, node):
        self.nodes.append(node)
