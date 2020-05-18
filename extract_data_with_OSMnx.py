import osmnx as ox

def extractCityFromOsm(cityname, network_type, plot=True):
    G = ox.graph_from_place(cityname +", France", retain_all=True, simplify=True, network_type=network_type)
    G2 = ox.graph_from_place(cityname +", France", retain_all=True, simplify=True, network_type=network_type, truncate_by_edge=True, buffer_dist=100)
    if plot:
        ox.plot_graph(G)

    ox.save_graphml(G, filename=cityname+"_"+network_type+".graphml", folder="raw_data_from_OSM")
    ox.save_graphml(G2, filename=cityname+"_"+network_type+"_extended.graphml", folder="raw_data_from_OSM")



