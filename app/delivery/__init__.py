from .delivery import WorldMap
from .delivery import lightdayRandom as _normalWeight

Map = WorldMap(5,5, randFunc=_normalWeight)

# Returns:
# - A list containing the path to be travelled and the total weight of
#   that path.
def shortest_route(destination):
    # Change up the state of the streets.
    Map.generate_graph()
    return Map.shortest_delivery_route(destination)

