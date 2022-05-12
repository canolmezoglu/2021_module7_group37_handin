from graph import Vertex
from old_branching import *


def depth_first_search_main(graph):
    """
        A function holds the global variable for another recursive function that does a depth first search on a graph.
        :param graph: the graph that the depth first search is done on
        :returns visited: the set of nodes where depth first search has visited
    """
    visited = set()
    depth_first_search_recursion(graph, visited, graph.vertices[0])
    return visited


def depth_first_search_recursion(graph, visited, vertex):
    """
        A recursive function that does depth first search
        :param graph: the graph that the depth first search is done on
        :param visited: the shared visited set that is modified between
        :param vertex: the vertex to start the depth first search on
    """
    if vertex not in visited:
        visited.add(vertex)
    for neighbour in vertex.neighbours:
        if neighbour not in visited:
            depth_first_search_recursion(graph, visited, neighbour)
    return


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
        and whether it is is_disconnected
        :param graph: the graph that the depth first search is done on
    """
    # visited = depth_first_search_main(graph)
    visited = iterative_depth_first_search(graph)
    components = list()
    graph_vertices = set(graph.vertices)
    components.append(len(visited))
    is_disconnected = False
    if len(visited) == len(graph_vertices):
        return tuple(components), is_disconnected, None
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
    is_disconnected = True
    return tuple(components), is_disconnected, actual_components


def give_graph_tuples(graph):
    """
        A function that returns the lengths of the components of a graph
        :param graph: the graph that the depth first search is done on
    """
    components, is_disconnected, _ = get_components(graph)
    graph_tuple = list()
    tree = check_if_tree(graph, not is_disconnected, True)
    # TODO justin add cube function
    cube = True
    graph_tuple.append(components)
    graph_tuple.append(tree)
    graph_tuple.append(cube)
    graph_tuple.append(is_disconnected)
    return tuple(graph_tuple)


def preprocess(graphs):
    """
        A function that separates graphs based on their conditions
        :param graphs: the given list of graphs
        :returns equivalences: a list of lists containing equivalently preprocessed graphs
        :returns trees: a list of indices of lists containing trees in equivalences list
        :returns cubes: a list of indices of lists containing cubes in equivalences list
        :returns disconnected: a list of indices of lists containing disconnected graphs in equivalences list
    """
    temp = dict()
    equivalences = list()
    trees = list()
    cubes = list()
    disconnected = list()
    for i in range(0, len(graphs)):
        graph = graphs[i]
        tuple_g = give_graph_tuples(graph)
        if tuple_g not in temp:
            temp[tuple_g] = []
        temp[tuple_g].append(i)
    y = 0
    for tuple_graph in temp:
        equivalences.append(temp[tuple_graph])
        if tuple_graph[1]:
            trees.append(y)
        if tuple_graph[2]:
            cubes.append(y)
        if tuple_graph[3]:
            disconnected.append(y)
    return equivalences, trees, cubes, disconnected


def check_if_connected(graph, dfs_value, dfs_done=False):
    """
        A function that checks if a given graph is connected.
        :param graph: the given list of graphs
        :param dfs_value: the size of the list of visited nodes if dfs was done
        :param dfs_done: a value indicating if dfs was already done or not
    """
    if not dfs_done:
        dfs_value = len(iterative_depth_first_search(graph))
    return dfs_value == len(graph.vertices)


#
def check_if_tree(graph, connected=False, connected_checked=False):
    """
        A function that checks if a given graph is a tree
        :param graph: the given list of graphs
        :param connected: a boolean indicating the graph was already connected or not
        :param connected_checked: a boolean indicating whether the connected
    """
    if not connected_checked:
        connected = check_if_connected(graph, 0)
    if connected and len(graph.vertices) == len(graph.edges) + 1:
        return True
    return False


def trees_in_graphs(graphs):
    """
        A function that returns a list of tree graphs from a list of graphs
        :param graphs: the given list of graphs
    """
    temp = list()
    for graph in range(0, len(graphs)):
        if check_if_tree(graphs[graph]):
            temp.append(graph)
    return temp


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
            i += 1
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


def disconneted_equivalence_classes(graphs):
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
    offe = dict()
    for i in matches:
        if len(matches[i]) > 1:
            if i not in visited2:
                s = tuple(matches[i])
                offe[s] = [graph_components[s[0]], graph_components[s[1]]]
                equivalences.append(s)
                visited2 = visited2.union(matches[i])
    return equivalences, offe


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
    for equivalence_class in equivalences:
        tmp = components[equivalence_class]
        aut = aut_disconnected(tmp[0], tmp[1])
        automorphisms[equivalence_class] = aut
    return automorphisms


def cograph_all(graphs):
    eq, cmp = disconneted_equivalence_classes(graphs)
    return aut_for_cographs(eq, cmp)
