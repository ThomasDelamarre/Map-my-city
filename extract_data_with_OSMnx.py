import osmnx as ox


def extractCityFromOsm(cityname, network_type, plot=True):
    G = ox.graph_from_place(cityname +", France", retain_all=True, simplify=True, network_type=network_type)
    #G = ox.project_graph(G)
    if plot:
        ox.plot_graph(G)

    ox.save_graphml(G, filename=cityname+"_"+network_type+".graphml", folder="raw_data_from_OSM")


