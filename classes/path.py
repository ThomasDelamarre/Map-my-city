def extractLatLongFromNodes(node1, node2):
    lats, longs = [], []
    lats.append(node1.lat)
    lats.append(node2.lat)
    longs.append(node1.long)
    longs.append(node2.long)
    return lats, longs


class Path:

    def __init__(self, path="", lat=None, long=None, node1=None, node2=None):
        #Init from GRAPHML file; if len > 2
        if path != "" and "Reversed" not in path and "merge" not in path:
            self.raw = path
            self.lats, self.longs = self.extractDataFromLinestring()
            self.len = len(self.lats)
        #Init from GRAPHML file; if len == 2
        elif node1 is not None and node2 is not None:
            self.raw = "No linestring; only 2 nodes"
            self.lats, self.longs = extractLatLongFromNodes(node1, node2)
            self.len = len(self.lats)
        #Init from code, when we reverse an existing edge
        elif lat is not None and long is not None:
            self.raw = path
            self.lats, self.longs = lat, long
            self.len = len(self.lats)
        elif "merge" in path:
            self.raw = ""
            self.lats, self.longs = [], []
            self.len = len(self.lats)
        else:
            raise TypeError("Unexpected data provided", path, lat, long, node1, node2)

    def __repr__(self):
        return self.raw

    def reverse(self):
        return "Reversed" + self.raw, self.lats[::-1], self.longs[::-1]

    def extractDataFromLinestring(self):
        lat, long = [], []
        line = self.raw.replace("LINESTRING (", "")
        line = line.replace(")", "")
        couples = line.split(", ")
        for couple in couples:
            couple = couple.split(" ")
            lat.append(float(couple[0]))
            long.append(float(couple[1]))
        return lat, long

    def merge(self, path1, path2):
        if isinstance(path1, Path) and isinstance(path2, Path):
            self.raw = path1.raw + path2.raw
            self.lats = path1.lats + path2.lats[1:]
            self.longs = path1.longs + path2.longs[1:]
            self.len = len(self.lats)
        else:
            raise TypeError("Expected the path to merge to be of Path type")

