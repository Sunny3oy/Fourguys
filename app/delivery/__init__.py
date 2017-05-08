from .delivery import WorldMap
from .delivery import lightdayRandom as _normalWeight

Map = WorldMap(5,5, randFunc=_normalWeight)

# Returns:
# - A list containing the path to be travelled and the total weight of
#   that path.
def shortest_route(destination_address):
    """Gives the shortest path from the restaurant to the given address.
    Returns a list whose first memeber is a list of vertices which
    starts at the block of the restaurant and end at the destination
    address, and whose second member is the weight of the path. Also
    changes up the weights in the Map to reflect changing conditions."""
    # Change up the state of the streets.
    Map.generate_graph()
    vertex = Map.convert_to(destination_address, 'position')
    return Map.shortest_delivery_route(vertex)

def regnerate_weights()
    """Changes up the weights on the Map."""
    Map.generate_graph()

__all__ = ['Map', 'shortest_route', 'regnerate_weights']
