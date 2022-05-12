from old_branching import countIsomorphisms2, countIsomorphisms3
from graph import Graph, Vertex, Edge
from graph_io import *
def iterative_depth_first_search(graph, vertex=None):
    """
        A dynamic programming function that does depth first search
        :param graph: the graph that the depth first search is done on
        :param vertex: the vertex to start the depth first search on
    """
    s = []
    visited = set()
    if vertex is None:
        vertex = graph.vertices[0]
    s.append(vertex)
    while len(s) > 0:
        v = s.pop()
        if v not in visited:
            visited.add(v)
            for neighbor in v.neighbours:
                s.append(neighbor)
    return visited


def get_components(graph):
    """
        A function that returns the lengths of the components of a graph
        and whether it is disconnected
        :param graph: the graph that the depth first search is done on
    """
    # visited = depth_first_search_main(graph)
    visited = iterative_depth_first_search(graph)
    components = list()
    graph_vertices = set(graph.vertices)
    components.append(len(visited))
    disconnected = False
    if len(visited) == len(graph_vertices):
        return tuple(components), disconnected, None
    actual_components = list()
    actual_components.append(visited)
    while len(visited) != len(graph_vertices):
        new_visits = set()
        temp = graph_vertices.difference(visited)
        new_search_vertex = next(iter(temp))
        # depth_first_search_recursion(graph, new_visits, new_search_vertex)
        new_visits = iterative_depth_first_search(graph, new_search_vertex)
        components.append(len(new_visits))
        visited = visited.union(new_visits)
        actual_components.append(new_visits)
    components = sorted(components)
    disconnected = True

    return tuple(components), disconnected, actual_components


def construct_graph_from_components(components):

    result_graphs = list()
    for component in components:
        subgraph = Graph(False)
        i = 0
        convert = dict()
        for vertex in component:
            convert[vertex.label] = i
            temp = Vertex(subgraph, i)
            subgraph.add_vertex(temp)
            i = i+1
        for vertex in component:
            for edge in vertex.incidence:
                tail = subgraph.vertices[convert[edge.tail.label]]
                head = subgraph.vertices[convert[edge.head.label]]
                temp = Edge(tail, head)
                if temp not in subgraph.edges:
                    subgraph.add_edge(temp)
        result_graphs.append(subgraph)
    return result_graphs




def iso_between_disconnected(components1, components2):
    seen = set()
    num = 0
    if len(components1) != len(components2):
        return False
    for component in components1:
        for component2 in components2:
            if component2 in seen:
                continue
            if countIsomorphisms2(component, component2):
                num = num+1
                seen.add(component2)
                break
    return num == len(components1)

def copy_graph(graph):

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
def copyComponents(components):
    pff=list()
    for component in components:
        pff.append(copy_graph(component))
    return pff
def disconnected_equivalence_classes(graphs):
    graph_components = [0]*len(graphs)
    for i in range(0, len(graphs)):
        _, _, compos1 = get_components(graphs[i])
        compos = construct_graph_from_components(compos1)
        graph_components[i] = compos
    matches = dict()
    visited = set()
    for i in range(0, len(graphs)):
        visited.add(i)
        if i not in matches:
            matches[i] = set()
            matches[i].add(i)
        for v in range(0, len(graphs)):
            if v not in matches:
                matches[v] = set()
                matches[v].add(v)
            if v in visited:
                continue
            if iso_between_disconnected(graph_components[i], graph_components[v]):
                matches[v].add(i)
                matches[i].add(v)
                if matches[i] != matches[v]:
                    temp = matches[i].union(matches[v])
                    matches[i] = temp
                    matches[v] = temp
    equivalences = list()
    visited2 = set()
    automorphism_params = dict()
    for i in matches:
        if len(matches[i]) > 0:
            if i not in visited2:
                s = tuple(matches[i])
                copy_compos=copyComponents(graph_components[s[0]])
                automorphism_params[s] = [graph_components[s[0]], copy_compos]
                equivalences.append(s)
                visited2 = visited2.union(matches[i])
    return equivalences, automorphism_params


def aut_disconnected(components1, components2):
    seen = set()
    num2 = 1
    if len(components1) != len(components2):
        return False
    for component in components1:
        for component2 in components2:
            if component2 in seen:
                continue
            if countIsomorphisms2(component, component2):
                num2 = num2*(countIsomorphisms3(component, component2))
                seen.add(component2)
                break
    return num2


def aut_for_cographs(equivalences, components):
    automorphisms = dict()
    for current_class in equivalences:
        tmp = components[current_class]
        aut = aut_disconnected(tmp[0], tmp[1])
        automorphisms[current_class] = aut
    return automorphisms


def cograph_all(graphs):
    eq, cmp = disconnected_equivalence_classes(graphs)
    return aut_for_cographs(eq, cmp)


if __name__ == "__main__":
    with open('graphs/bonusAut4.grl') as f:
        G = load_graph(f, read_list=True)
    graphs = G[0]
    print((cograph_all(graphs)))
