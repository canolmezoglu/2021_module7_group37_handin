from our_lib import factorial


def find_center(graph):
    """
    Returns the middle vertex(s) of the longest path of a given tree
    Inspired by: https://towardsdatascience.com/graph-theory-center-of-a-tree-a64b63f9415d
    "Jose, Kelvin. “Graph Theory: Center of a Tree.” Medium, Towards Data Science, 18 June 2020,
    towardsdatascience.com/graph-theory-center-of-a-tree-a64b63f9415d."
    Disclaimer: I created my implementation with influence from this source, I did not copy it.
    :param graph: The given graph graph
    """
    n = len(graph.vertices)
    degree = [0] * n
    leaves = []
    visited = [0] * n
    # for each vertex of the graph, determine if it is a loner or a leaf and add loners and leaves to a list.
    for vertex in graph.vertices:
        vertex_degree = len(vertex.neighbours)
        degree[vertex.label] = vertex_degree
        if vertex_degree == 0 or vertex_degree == 1:
            leaves.append(vertex)
            degree[vertex.label] = 0

    count = len(leaves)
    # iterate over each vertex, decrementing it's degree for each leaf neighbour it has
    # the finally left vertex with degree 0 should be the center
    while count < n:
        new_leaves = []
        for vertex in leaves:
            visited[vertex.label] = 1
            for neighbor in vertex.neighbours:
                degree[neighbor.label] = degree[neighbor.label] - 1
                if degree[neighbor.label] == 1:
                    new_leaves.append(neighbor)
        count += len(new_leaves)
        leaves = new_leaves
    temp = []
    for i in range(0, len(visited)):
        if visited[i] == 0:
            temp.append(i)
    # check if the tree has only one center
    if len(temp) == 1:
        return temp[0]
    maximum = 0
    temp2 = 0
    # if the tree is bi-centered, return the center with the max value
    for i in temp:
        vertex = graph.vertices[i]
        if vertex.degree > maximum:
            maximum = vertex.degree
            temp2 = vertex.label
    return temp2


class Treenode:
    """
    A tree structure.
    Inspired by: https://towardsdatascience.com/graph-theory-rooting-a-tree-fb2287b09779
    "Jose, Kelvin. “Graph Theory: Rooting a Tree.” Medium, Towards Data Science, 8 June 2020,
    towardsdatascience.com/graph-theory-rooting-a-tree-fb2287b09779."
    Disclaimer: I created my implementation with influence from this source, I did not copy it, as
    seen from additions.
    """

    def __init__(self, id, parent, child):
        # left child
        self.parent = parent
        # right child
        self.children = child
        # node's value
        self.id = id
        self.AHU = None


def root_tree(g, root_id=0):
    """
    A function to create the root of a tree.
    Inspired by: https://towardsdatascience.com/graph-theory-rooting-a-tree-fb2287b09779
    "Jose, Kelvin. “Graph Theory: Rooting a Tree.” Medium, Towards Data Science, 8 June 2020,
    towardsdatascience.com/graph-theory-rooting-a-tree-fb2287b09779."
    Disclaimer: I created my implementation with influence from this source, I did not copy it, as
    seen from additions.
    :param g: The graph for which the tree object is created for
    :param root_id: the id of the root
    """
    root = Treenode(root_id, None, [])
    return build_tree(g, root)


def build_tree(g, node, parent = None):
    """
    A function to create children of a tree.
    Inspired by: https://towardsdatascience.com/graph-theory-rooting-a-tree-fb2287b09779
    "Jose, Kelvin. “Graph Theory: Rooting a Tree.” Medium, Towards Data Science, 8 June 2020,
    towardsdatascience.com/graph-theory-rooting-a-tree-fb2287b09779."
    Disclaimer: I created my implementation with influence from this source, I did not copy it, as
    seen from additions.
    :param g: The graph for which the tree object is created for
    :param node: the node for which the children is created for
    :param parent: the parents of that node
    """
    vertex = g.vertices[node.id]
    for child in vertex.neighbours:
        if parent is not None and child.label == parent.id:
            continue
        child = Treenode(child.label, node, [])
        node.children.append(child)
        build_tree(g, child, node)
    return node


def ahu(node):
    """
    A function inspired by Aho, Hopcroft , Ullman algorithm to check for tree isomorphisms.
    :param node: The node for which the AHU tuple is obtained for
    :returns ahu_of_node: a canonical tuple that describes the three
    :returns node: the root of the tree with children that has AHU values
    """
    # if the node is not a leaf, get the AHU of it's children first
    if len(node.children) > 0:
        ahu_of_children = []
        for children in node.children:
            ahu_of_child, node_of_child = ahu(children)
            ahu_of_children.append(ahu_of_child)
        # sort the ahu so that it is canonical between trees
        ahu_of_children = sorted(ahu_of_children)
        ahu_of_node = ""
        for i in ahu_of_children:
            ahu_of_node += i
        # create the ahu of node
        ahu_of_node = "(" + ahu_of_node + ")"
        node.AHU = ahu_of_node
        # return root of the tree (node) to use in #aut counting
        return ahu_of_node, node
    # if the node is a leaf return the basic value
    else:
        return "()"


def aut_counter(node):
    """
    A function to calculate the #aut for trees.
    :param node: The node for which the AHU tuple is obtained for
    """
    # if the node is not a leaf, calculate the #aut of children
    if len(node.children) > 0:
        number = 1
        children_ahus = dict()
        for child in node.children:
            if child.AHU not in children_ahus:
                children_ahus[child.AHU] = []
            children_ahus[child.AHU].append(child.id)
            number = number * aut_counter(child)

        for children_ahu in children_ahus:
            if len(children_ahus[children_ahu]) > 0:
                # if there are isomorphic subtrees then the factorial of them is the #aut for parent
                number = number * factorial(len(children_ahus[children_ahu]))
        return number
    # if it is a leaf, it has #aut 1
    else:
        return 1


def check_isomorphism(g, g1):
    """
    A  function to check for isomorphisms between two trees
    :param g: the graph of the first tree
    :param g1: the graph of the second tree
    """
    ahu_g = root_tree(g, find_center(g))
    ahu_g1 = root_tree(g1, find_center(g1))

    return ahu(ahu_g) == ahu(ahu_g1), ahu_g


def equivalence_classes(graphs):
    """
    A  function to get the isomorphic graphs in a given list of graphs
    :param graphs: the list of graphs
    :returns equivalent_graphs_list: a list of equivalent graphs
    :returns trees: a list of tree versions of graphs with ahu's put
    """
    equivalence_classes = dict()
    trees = [0] * len(graphs)

    for i in range(0, len(graphs)):
        trees[i] = root_tree(graphs[i], find_center(graphs[i]))
        ahu_of_tree, trees[i] = ahu(trees[i])
        if ahu_of_tree not in equivalence_classes:
            equivalence_classes[ahu_of_tree] = []
        equivalence_classes[ahu_of_tree].append(i)
    equivalent_graphs_list = list()
    for equivalences in equivalence_classes.values():
        equivalent_graphs_list.append(equivalences)
    return equivalent_graphs_list, trees


def aut_for_trees(equivalence_classes, trees):
    """
    A  function to count #aut for a given equivalence class and trees
    :param equivalence_classes: given equivalance class
    :param trees: the given trees
    :returns auts: a dict with [equivalence classes as tuples] --> #aut for that equivalence class
    """
    auts = dict()
    for clas in equivalence_classes:
        aut = aut_counter(trees[clas[0]])
        auts[tuple(clas)] = aut
    return auts


def tree_aut_counter(graphs, just_isomorphism=False):
    """
    A that gets a list of tree graphs and returns the equivalence classes and their #aut
    :param graphs: the graphs you want to count automorphisms for
    :param just_isomorphism: a boolean to indicate whether #aut is wanted or not
    :returns trees_and_aut: a dict with [equivalence classes as tuples] --> #aut for that equivalence class
    """
    classes, trees = equivalence_classes(graphs)
    if just_isomorphism:
        return classes
    trees_and_aut = aut_for_trees(classes, trees)
    return trees_and_aut
