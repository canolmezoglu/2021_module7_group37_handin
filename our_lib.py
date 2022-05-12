from graph import Graph, Vertex, Edge
# this script is meant as to make our code not dependent on external libraries, this is a basic factorial implementation

def factorial(n: int) -> int:
    """
        A non recursive function for calculating factorials, inputs needs to be a positive integer
        :param n: The given positive integer to factorialize
        :returns result: The factorialization of n (mathematical notation n!)
    """

    result = 1
    for i in range(n):
        result *= (i+1)
    return result

def copy_graph(graph):
    """
        A way to deep_copy a Graph without using the copy.deepcopy() library
        :param graph: The given graph you want to copy
        :returns new_graph: An exact copy of the given graph
    """

    # the new graph that is a copy of the original graph
    new_graph = Graph(graph.directed)

    # mapping between vertices of original graph and new graph
    mapping = dict()

    # copy the vertices in the new graph
    for vertex in graph.vertices:
        new_vertex = Vertex(new_graph, vertex.label)
        new_graph.add_vertex(new_vertex)
        mapping[vertex] = new_vertex

    # copy the edges in the new graph
    for edge in graph.edges:
        new_edge = Edge(mapping[edge.tail], mapping[edge.head], edge.weight)
        new_graph.add_edge(new_edge)

    return new_graph