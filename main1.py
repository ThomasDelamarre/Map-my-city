from extract_data_with_OSMnx import *


#city = input("City Name? ")
#network_type = input("Network_type? (walk, bike, all, all_private) ")


city = "Vaucresson"
network_type = "bike"

extractCityFromOsm(city, network_type, plot=True)