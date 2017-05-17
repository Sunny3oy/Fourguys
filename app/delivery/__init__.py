from .delivery import WorldMap
from .delivery import lightdayRandom as _normalWeight
from .delivery import shortest_path as _dijkstra

Map = WorldMap(5,5, randFunc=_normalWeight)
Map.generate_graph()

# Returns:
# - A list containing the path to be travelled and the total weight of
#   that path.
def get_delivery_route(destination_address):
    """Gives the shortest path from the restaurant to the given address.
    Based on the current state of the world. The current state of the
    world is simulated by reassigning weights to all the edges in the
    graph that represents the map.  Returns a list whose first memeber
    is a list of vertices which starts at the block of the restaurant
    and end at the destination address, and whose second member is the
    weight of the path."""
    Map.generate_graph()
    position = Map.convert_to(destination_address, 'position')
    return Map.shortest_delivery_route(position)

# Returns:
# - A list containing the path to be travelled and the total weight of
#   that path.
def shortest_route(destination_address):
    """Gives the shortest path from the restaurante to the given address
    using the current map conditions."""
    position = Map.convert_to(destination_address, 'position')
    return Map.shortest_delivery_route(position)


def regnerate_weights():
    """Changes up the weights on the Map."""
    Map.generate_graph()

__all__ = ['Map', 'shortest_route', 'regnerate_weights']
#__all__.append('_dijkstra') # DEBUG
