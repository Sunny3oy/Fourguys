# Regular expressions, for validation.
import re
# Random number generation.
import secrets 

# TODO:
# - Create package for delivery.
#   - Figure out interface to all of the things in here.
# - Do some more validation. Don't allow vertices that aren't
#   technically in the graph, like vertices with a y larger than the
#   height or an x wider than the width.
# - Maybe make some sort of dispatcher that makes sure that functions
#   get data in the form that they expect it without the user having to
#   concern themselves with that.
# - Make the shortest path algorithm faster.

# Address to Vertex Conversion:
# - We can use the validator to check if an address is a valid sky
#   island address.
# - If it is a valid address, then we can also extract the street number
#   and avenue number, which translate into a vertex.
# - The address form is: "Sky Street" Number "Sky Avenue" Number, where
#   the two numbers represent your avenue and street respectively.
#   - The street number increases as you go north (up), so they denote
#     rows.
#   - The avenue number increases as you go east (right), so they denote
#     columns.
#   - Each one starts from 1, to the bottom left corner of the island is
#     the address Sky Street 1 Sky Avenue 1.

# Generates a number in [low, high) with uniform probability.
def uniformRandom(low, high):
    return low + secrets.randbelow(high - low)
# Generates a 1 with 40% probability, 2 with 30% probability, ... so on.
def lightdayRandom():
    return secrets.choice( [ *[1]*40, *[2]*30, *[3]*15, *[4]*10, *[5]*5 ] )
# Heavy numbers are more probable here.
def heavydayRandom():
    return secrets.choice( [ *[1]*20, *[2]*30, *[3]*25, *[4]*15, *[5]*10 ] )
# Create a table of random things that could happen to an existing map,
# and pair them with transformations on the map.
def somethingHappens():
    {
        "parade" : "increase one strip of vertices by x",
        "block party": "increase one vertex and it's neighborhood by x",
        "shootout" : "set some edges to 5",
    }

# Map representation:
# - For now, just a dictionary. It'll be large, memory-wise, but there
#   will only be one of them. There's no duplicating this graph, so it
#   shouldn't be that bad.
# - We don't really need to do an adjacency list because adjacency is
#   fairly obvious. I can make a function to generate the neighborhood
#   of a vertex based solely on the vertex. 
# - I'll make a class that'll hold the basic characteristics of how the
#   graph should look like, then generate graphs based on that with
#   random weights. The randomness function will be customizable.
class WorldMap:

    # - width, height: integers representing number of blocks.
    # - maxWeight: integer representing the maximum weight on the graph.
    # - randFunc: a function which should return a random integer when
    #   called. There's little point to using both this and maxWeight at
    #   the same time.
    def __init__(self, width, height, 
            minWeight=1, maxWeight=5, randFunc=None,
            restaurantLocation=None):
        self.width = width
        self.height = height
        if randFunc == None:
            self.randFunc = lambda: uniformRandom(minWeight,maxWeight+1)
        else:
            self.randFunc = randFunc
        if restaurantLocation == None:
            self.restaurantLocation = (self.width // 2, self.height // 2)
        else:
            self.restaurantLocation = restaurantLocation

    address_validator =\
        re.compile(r"Sky Street (\d+) Sky Avenue (\d+)",
                flags=re.IGNORECASE)
    def validate_address(self, address):
        match = self.address_validator.fullmatch(address)
        if not match:
            return False
        x, y = int(match.group(1)) - 1, int(match.group(0)) - 1
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return True

    def is_position(self, v):
        return type(v) == type(0)
    def is_vertex(self, v):
        return type(v) == type(())
    def is_address(self, v):
        return type(v) == type("") and validate_address(v)

    # vertex: A tuple of integers representing the block you're on.
    # Returns: A list of the vertices which are neighbors of vertex.
    def neighborhood_of(self, vertex):
        x, y = self.to_vertex(vertex)
        # Every block is adjacent to blocks in cardinal directons
        potentialNeighbors = [ 
            (x+1, y),
            (x, y+1),
            (x-1, y),
            (x, y-1),
        ]
        neighbors = [x for x in potentialNeighbors if 
                x[0] >= 0 and
                x[1] >= 0 and
                x[0] < self.width and
                x[1] < self.height]
        if self.is_position(vertex):
            return [self.to_position(x) for x in neighbors]
        elif self.is_vertex(vertex):
            return neighbors
        elif self.is_address(vertex):
            return [self.to_address(x) for x in neightbors]

    def neighborhood_of_positions(self, vertex):
        return self.neighborhood_of(self.to_position(vertex))
    def neighborhood_of_vertices(self, vertex):
        return self.neighborhood_of(self.to_vertex(vertex))

    # v1, v2: Vertices, which are tuples of integers.
    def adjacent_to(self, v1, v2):
        v1, v2 = self.normalize_vertices([v1, v2])
        return v1 in self.neighborhood_of(v2)

    # The data types that Map will work with:
    # - vertex: A tuple of integers which refer to a block on the map.
    #   They're of the form (avenue, street).
    # - position: An integer representing a vertex in the Map. They're
    #   necessary for accessing positions on the graph when the graph
    #   is a list. For any vertex (x, y) the corresponding position is
    #   x * height + y.
    # - address: Street addresses representing vertices on the map.
    #   They're of the form "Sky Street <street-num> Sky Avenue
    #   <ave-num>. The corresponding vertex is (<ave-num>,
    #   <street-num>).
    def vertex_to_position(self, v):
        return v[0]*self.height + v[1]
    def position_to_vertex(self, position):
        return (position//self.height, position % self.height)
    def vertex_to_address(self, vertex):
        return "Sky Street {} Sky Avenue {}".format(
                *[x+1 for x in vertex[::-1]])
    def address_to_vertex(self, address):
        match = self.address_validator.fullmatch(address)
        if match:
            return (int(match.group(2)) - 1, int(match.group(1)) - 1)
    def address_to_position(self, address):
        return self.convert_to(address, 'position')
    def convert_to(self, vertex, new_type):
        """Convert the vertex from it's current type to the type specified in the third argument, new_type. new_type may be one of:
    - 'vertex'
    - 'position'
    - 'address'"""
        identity_function = lambda x: x

        if self.is_vertex(vertex) and new_type == 'vertex' or\
           self.is_position(vertex)and new_type == 'position' or\
           self.is_address(vertex) and new_type == 'address':
            return vertex

        if self.is_vertex(vertex):
            fromFunc = identity_function
        elif self.is_address(vertex):
            fromFunc = self.address_to_vertex
        elif self.is_position(vertex):
            fromFunc = self.position_to_vertex

        if new_type == 'vertex':
            toFunc = identity_function
        elif new_type == 'position':
            toFunc = self.vertex_to_position
        elif new_type == 'address':
            toFunc = self.vertex_to_address

        return toFunc(fromFunc(vertex))

    # These are here until I get rid of references to them.
    def to_position(self, v):
        return self.convert_to(v, 'position')
    def to_vertex(self, v):
        return self.convert_to(v, 'vertex')
    def normalize_vertices(self, vertexList):
        return [self.to_vertex(x) for x in vertexList]
        

    # Preconditions:
    # - None
    # Returns:
    # - Creates an actual graph as an adjacency matrix. If matrix is the
    #   return value of this function, and v1 and v2 are two vertices in
    #   the graph, then the weight of the edge between v1 and v2 is
    #   matrix[v1][v2], or matrix[v2][v1] (it's the same either way).
    def generate_graph(self):
        num_vertices = self.width * self.height
        # num_vertices columns, num_vertices rows.
        adjacency_matrix = [[None]*num_vertices]*num_vertices
        # Loop over all the pairs of vertices and their neighbors.
        for i in range(0, num_vertices):
            #neighbors = self.neighborhood_of(self.position_to_vertex(i))
            #neighboring_positions =\
                #[self.vertex_to_position(x) for x in neighbors]
            neighboring_positions = self.neighborhood_of(i)

            for neighbor in neighboring_positions:
                if adjacency_matrix[i][neighbor] == None:
                    weight = self.randFunc()
                    adjacency_matrix[i][neighbor] = weight
                    adjacency_matrix[neighbor][i] = weight
        self.graph = adjacency_matrix
    def vertex_set(self):
        return [(x,y) for x in range(0,self.width) 
                        for y in range(0,self.height)]
    def position_set(self):
        return [self.to_position(x) for x in self.vertex_set()]

    # Get an edge weight.
    def edge(self, v1, v2):
        return self.graph[v1][v2]

    # Set an edge weight.
    def set_edge(self, v1, v2, weight):
        if weight < self.minWeight:
            self.graph[v1][v2] = self.minWeight
        elif weight > self.maxWeight:
            self.graph[v1][v2] = self.maxWeight
        else:
            self.graph[v1][v2] = weight

    def shortest_delivery_route(self, destination):
        # If we haven't generated a graph yet:
        if 'graph' not in dir(self):
            self.generate_graph()
        result = shortest_path(
                    self,
                    self.to_position(self.restaurantLocation),
                    self.to_position(destination))
        # Cut out the terminal vertex from the result, keeping only
        # the path and the total weight.
        return [self.normalize_vertices(result[1]), result[2]]

# Preconditions:
# - graph: An instance of the WorldMap class. It is assumed that the
#   graph here is a simple graph.
# - source, destination: These are vertices in the graph, and since the
#   graph is a list of lists, the vertices are numbers-- indexes of the
#   matrix.
# Returns:
# - If destination is None, then it returns paths from the source to
#   every possible destination.
# - If destination is a vertex in the graph, then it returns one path
#   from the source to the destination.
def shortest_path(graph, source, destination=None):
    # Each entry of explored is of the form [vertex, path, weight],
    # where:
    # - vertex is the terminal vertex in the path.
    # - path is a list of vertices that specify a path through the
    #   graph, starting from source and ending in vertex.
    # - weight is the weight of the path (the sum of the weights of the
    #   edges in the path).
    explored_paths = [[source, [source], 0]]
    explored_vertices = {source}

    # The set of unexplored vertices in the neighborhood of explored
    # vertices.
    frontier = set(graph.neighborhood_of(source))

    while len(frontier) != 0:
        #print("Explored Vertices:", explored_vertices)
        #print("Explored Paths:", explored_paths)
        #print("Frontier:", frontier)

        next_paths = []
        for vertex in frontier:
            explored_neighbors = [x for x in explored_paths
                    if x[0] in graph.neighborhood_of(vertex)]
            #print("Explored Neighbors:", explored_neighbors)
            # Get best path to this particular frontier vertex.
            best_path = min([\
                [vertex,
                [ *x[1], vertex ],
                x[2] + graph.edge(x[0], vertex)]
                for x in explored_neighbors],
                key=lambda x: x[2])
            next_paths.append(best_path)

        # Choose the best path out of the best paths to frontier
        # vertices.
        chosen_path = min(next_paths, key=lambda x: x[2])
        if chosen_path[0] == destination:
            return chosen_path
        explored_paths.append(chosen_path)
        explored_vertices.add(chosen_path[0])
        frontier.remove(chosen_path[0])
        for vertex in graph.neighborhood_of(chosen_path[0]):
            if vertex not in explored_vertices:
                frontier.add(vertex)

    return explored_paths

# Making this algorithm faster:
# - Maybe I can put all the possibilities on a priority queue?
# - The old possibilities don't really go away, and I keep regenerating
#   them with each iteration.
# - I also know that I'm exploring paths in nondecreasing order, so if I
#   ever see a frontier vertex in the neighborhood of another vertex
#   just discovered, there's no way the path from that vertex to the
#   frontier vertex is better than the path that I already found
#   (assuming that this path was found on a previous iteration.
# - Even further, we only put one vertex at a time in the explored set,
#   and this graph is assumed to be a simple graph. So vertices
#   shouldn't pop up more than once in a vertex's neighborhood.
#   Therefore there's no way that I'll encounter two different ways to
#   reach the same vertex on the frontier update from a single
#   generation.


# Tests: {{{ ###############################################

def validate_address_test():
    # ( Case, value it should have).
    cases = [
        ( "Sky Street Sky Avenue", False ),
        ( "Sky Street 0 Sky Avenue", False ),
        ( "Sky Street 0 Sky Avenue 0", True ),
        ( "Sky Street 00 Sky Avenue 0", True ),
        ( "Sky Street 123 Sky Avenue 456", True ),
    ]

    passed = [x for (x,y) in cases if validate_address(x) == y]
    failed = [x for (x,y) in cases if validate_address(x) != y]

    if len(failed) == 0:
        return True
    else:
        return failed

# }}} ######################################################
