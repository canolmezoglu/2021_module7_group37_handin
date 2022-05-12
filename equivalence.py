from refinement_classes import Partition, Color
from preprocess import check_if_connected, check_if_tree
from refinement import hopcroft_refinement
from twins import get_twins
from tree import ahu, find_center, root_tree
from old_branching import *
from disconnected import disconnected_equivalence_classes, get_components


# TODO: give the partitions an index based on which graph they came from, probably in main function


class EquivalenceClass(object):
    """
        Equivalence class to keep track of the types
        :param partitions:
        :param connected:
        :param tree:
        :param twins:
        :param hypercube:
        :param uniform:
        :param automorphisms:
    """

    def __init__(self, partitions: "list[Partition]", connected=False, tree=False, hypercube=False, uniform=False,
                 twins=False):
        self.partitions = partitions
        self.connected = connected
        self.tree = tree
        self.twins = twins
        self.hypercube = hypercube
        self.uniform = uniform
        self.automorphisms = -1

    def copy_empty_similarly_typed(self):
        copy = EquivalenceClass([], connected=self.connected, tree=self.tree, hypercube=self.hypercube,
                                 uniform=self.uniform, twins=self.twins)
        if copy.hypercube:
            copy.hypercube_n = self.hypercube_n
        if copy.tree:
            copy.tree_ahu = self.tree_ahu
            copy.tree_tree = self.tree_tree
        if copy.twins:
            copy.twins_factor = self.twins_factor
        return copy


def equivalence_classes_main(partitions: "list[Partition]") -> "list[EquivalenceClass]":
    """
        Integrates all elements involved in equivalence testing in this file together in this method
        :param partitions: the partitions already colored based on hopcraft, were refined based on group size
        :returns: proper equivalence classes
    """


    # resulting equivalence classes, will be refined in place by sub functions
    equivalence_classes = [EquivalenceClass(partitions.copy())]

    # separate them based on connectedness
    equivalence_classes_refine_connected(equivalence_classes)

    equivalence_classes_refine_disconnected_components(equivalence_classes)

    equivalence_classes_refine_twins(equivalence_classes)
    equivalence_classes_refine_balanced(equivalence_classes)

    # separate them based on uniformity
    equivalence_classes_refine_uniform(equivalence_classes)

    # separate them based on whether or not they are a tree
    equivalence_classes_refine_trees(equivalence_classes)

    # separate trees based on AHU
    equivalence_classes_refine_trees_ahu(equivalence_classes)

    # separate them based on whether or not they are a hypercube
    equivalence_classes_refine_hypercubes(equivalence_classes)


    # separate uniform classes based on distances between each pair of vertices (sort of)
    equivalence_classes_refine_distances_vertex(equivalence_classes)

    # to be super sure, make sure they are actually isomorphic, might add some time if correct, but if incorrect
    # will give right classes (if it does not take too long)
    equivalence_classes_refine_branching(equivalence_classes)


    # for ec in equivalence_classes:
    #     print("for group containing graph: ", ec.partitions[0].graph_index)
    #     print("tree: ", ec.tree)
    #     print("hypercube: ", ec.hypercube)
    #     print("twins: ", ec.twins)
    #     print("connected: ", ec.connected)
    #     print("uniform: ", ec.uniform)

    # return the equivalence classes
    return equivalence_classes


def equivalence_classes_refine_twins(equivalence_classes: "list[Equivalence_class]") -> None:
    """
        should only have 1 equivalence class <=> should be immediately after instantiating equivalence classes
    """
    equivalence_class = equivalence_classes[0]
    if not equivalence_class.tree:
        # the groups based on whether there exist an isomorphism between partitions
        groups = dict()
        new_partitions = []

        for partition in equivalence_class.partitions:
            if check_if_tree(partition.graph, True, True):
                new_partitions.append(partition)
                continue

            for i in range(partition.length()):
                for vertex in partition.colors[i].vertices:
                    vertex.colornum = i
            graph, factor,_ = get_twins(partition.graph)
            new_partition = Partition(partition.graph)
            new_partition.graph_index = partition.graph_index
            vertices_groups = dict()
            i = 0
            for vertex in partition.graph:
                if vertex.colornum in vertices_groups:
                    vertices_groups[vertex.colornum].append(vertex)
                else:
                    vertices_groups[vertex.colornum] = [vertex]
                vertex.label = i
                i += 1

            for i in range(partition.length()):
                if i in vertices_groups:
                    new_partition.add_color(Color(set(vertices_groups[i]), new_partition))
                else:
                    new_partition.add_color(Color(set(), new_partition))
            if factor in groups:
                groups[factor].append(new_partition)
            else:
                groups[factor] = [new_partition]
            new_partitions.append(new_partition)

        equivalence_class.partitions = new_partitions

        # for each group of partitions
        for key in groups:
            group = groups[key]

            # if there are 2 different groups (so old class and new class would both be non empty)
            if len(group) != 0 and len(group) != len(equivalence_class.partitions):
                for partition in group:
                    equivalence_class.partitions.remove(partition)

                new_equivalence_class = equivalence_class.copy_empty_similarly_typed()
                new_equivalence_class.partitions = group
                new_equivalence_class.twins_factor = key
                new_equivalence_class.twins = True
                equivalence_classes.append(new_equivalence_class)
            elif len(group) != 0:
                equivalence_class.twins = True
                equivalence_class.twins_factor = key





def equivalence_classes_refine_balanced(equivalence_classes: "list[EquivalenceClass]") -> None:
    # for each equivalence class currently there, update, split or do nothing based on the hash of the graph of the
    # partitions in the equivalence class
    for i in range(len(equivalence_classes)):

        equivalence_class = equivalence_classes[i]

        # the groups based on whether there exist an isomorphism between partitions
        groups = []

        stack = set(equivalence_class.partitions.copy())

        while stack:
            partition_a = stack.pop()
            group = [partition_a]
            for partition_b in list(stack.copy()):
                if check_if_balanced(partition_a.copy(), partition_b.copy()):
                    group.append(partition_b)
                    stack.remove(partition_b)
            groups.append(group)

        # for each group of partitions
        for group in groups:

            # if there are 2 different groups (so old class and new class would both be non empty)
            if len(group) != 0 and len(group) != len(equivalence_class.partitions):
                for partition in group:
                    equivalence_class.partitions.remove(partition)

                new_equivalence_class = equivalence_class.copy_empty_similarly_typed()
                new_equivalence_class.partitions = group
                equivalence_classes.append(new_equivalence_class)

    # return nothing, since it update the equivalence classes in place
    return


def equivalence_classes_refine_uniform(equivalence_classes: "list[EquivalenceClass]") -> None:
    """
        Separates the equivalence classes based on the uniformity of the partitions, this is done in-place.
        :param equivalence_classes: the equivalenceClasses to refine in-place
    """

    # for each equivalence class currently there, update, split or do nothing based on uniformity of partitions in the
    # equivalence class
    for i in range(len(equivalence_classes)):

        # equivalence class to go over
        equivalence_class = equivalence_classes[i]

        # group for uniform partitions
        uniform = []

        # group for uniform partition
        not_uniform = []

        # for each partition in the equivalence class, put them in their respective group
        for partition in equivalence_class.partitions:
            if partition.length() == 1:
                uniform.append(partition)
            else:
                not_uniform.append(partition)

        # all are non uniform, so no need to do anything
        if len(uniform) == 0:
            pass

        # all are uniform, no need to split, only need to update tags
        elif len(not_uniform) == 0:
            equivalence_class.uniform = True

        # some are uniform, some are not, split them based on that
        else:
            equivalence_class.partitions = not_uniform

            # probably overkill on tracking of types, but in case this function is used at some random place
            new_equivalence_class = equivalence_class.copy_empty_similarly_typed()
            new_equivalence_class.uniform = True
            new_equivalence_class.partitions = uniform
            equivalence_classes.append(new_equivalence_class)

    # return nothing, since it update the equivalence classes in place
    return


def equivalence_classes_refine_connected(equivalence_classes: "list[EquivalenceClass]") -> None:
    """
        Separates the equivalence classes based on whether or not the partitions are connected, this is done in-place.
        :param equivalence_classes: the equivalenceClasses to refine in-place
    """

    # for each equivalence class currently there, update, split or do nothing based on uniformity of partitions in the
    # equivalence class
    for i in range(len(equivalence_classes)):

        # equivalence class to go over
        equivalence_class = equivalence_classes[i]

        # group for connected partitions
        connected = []

        # group for not connected partition
        not_connected = []

        # for each partition in the equivalence class, put them in their respective group
        for partition in equivalence_class.partitions:
            if check_if_connected(partition.graph, 0) == 1:
                connected.append(partition)
            else:
                not_connected.append(partition)

        # all are not connected, so no need to do anything
        if len(connected) == 0:
            pass

        # all are connected, no need to split, only need to update tags
        elif len(not_connected) == 0:
            equivalence_class.connected = True

        # some are connected, some are not, split them based on that
        else:
            equivalence_class.partitions = not_connected

            new_equivalence_class = equivalence_class.copy_empty_similarly_typed()
            new_equivalence_class.connected = True
            new_equivalence_class.partitions = connected
            equivalence_classes.append(new_equivalence_class)

    # return nothing, since it update the equivalence classes in place
    return

def equivalence_classes_refine_disconnected_components(equivalence_classes: "list[EquivalenceClass]") -> None:
    for i in range(len(equivalence_classes)):

        equivalence_class = equivalence_classes[i]

        if equivalence_class.connected:
            continue

        # the groups based on whether there exist an isomorphism between partitions
        groups = []

        stack = set(equivalence_class.partitions.copy())

        while stack:
            partition_a = stack.pop()
            _, _, component = get_components(partition_a.graph)
            if len(component) > 6:
                group = [partition_a]

                for partition_b in list(stack.copy()):
                    if len(disconnected_equivalence_classes([partition_a.graph, partition_b.graph])[0]) == 1:
                        group.append(partition_b)
                        stack.remove(partition_b)

                groups.append(group)

        # for each group of partitions
        for group in groups:

            # if there are 2 different groups (so old class and new class would both be non empty)
            if len(group) != 0 and len(group) != len(equivalence_class.partitions):
                for partition in group:
                    equivalence_class.partitions.remove(partition)

                new_equivalence_class = equivalence_class.copy_empty_similarly_typed()
                new_equivalence_class.partitions = group
                equivalence_classes.append(new_equivalence_class)

    # return nothing, since it update the equivalence classes in place
    return


def equivalence_classes_refine_trees(equivalence_classes: "list[EquivalenceClass]") -> None:
    """
        Separates equivalence classes based on whether or not the partitions are of type tree
        :param equivalence_classes: the equivalenceClasses to refine in-place
    """

    # for each equivalence class currently there, update, split or do nothing based on whether or not the graphs are
    # trees
    for i in range(len(equivalence_classes)):

        equivalence_class = equivalence_classes[i]

        # if uniform (trees cant be uniform) and if not connected, continue, since they will not be trees
        if not equivalence_class.connected or equivalence_class.uniform:
            continue

        # group for tree partitions
        tree = []

        # group for not tree partitions
        not_tree = []

        # for each partition in the equivalence class, put them in their respective group
        for partition in equivalence_class.partitions:
            if check_if_tree(partition.graph, True, True):
                tree.append(partition)
            else:
                not_tree.append(partition)

        # all are non tree, so no need to do anything
        if len(tree) == 0:
            pass

        # all are tree, no need to split, only need to update tags
        elif len(not_tree) == 0:
            equivalence_class.tree = True

            # placeholder
            equivalence_class.tree_ahu = -1

        # some are tree, some are not, split them based on that
        else:
            equivalence_class.partitions = not_tree

            new_equivalence_class = equivalence_class.copy_empty_similarly_typed()
            new_equivalence_class.tree = True

            # placeholder
            new_equivalence_class.tree_ahu = -1

            new_equivalence_class.partitions = tree
            equivalence_classes.append(new_equivalence_class)

        # return nothing, since it update the equivalence classes in place
    return


def equivalence_classes_refine_trees_ahu(equivalence_classes: "list[EquivalenceClass]") -> None:
    # for each equivalence class currently there, update, split or do nothing based on the hash of the graph of the
    # partitions in the equivalence class
    for i in range(len(equivalence_classes)):

        equivalence_class = equivalence_classes[i]

        # if not uniform, return, due to high complexity and negligible effects on non uniform colorings
        if not equivalence_class.tree:
            continue

        # the groups based on the distances between each pair of vertices
        groups = dict()
        groups_ahu_trees = dict()

        # for each partition in the equivalence class, put them in their respective group
        for partition in equivalence_class.partitions:
            ahu_of_tree, ahu_tree = ahu(root_tree(partition.graph, find_center(partition.graph)))
            if ahu_of_tree in groups:
                groups[ahu_of_tree].append(partition)
            else:
                groups[ahu_of_tree] = [partition]
                groups_ahu_trees[ahu_of_tree] = ahu_tree

        # for each group of partitions
        for key in groups:
            group = groups[key]

            # if there are 2 different groups (so old class and new class would both be non empty)
            if len(group) != 0 and len(group) != len(equivalence_class.partitions):
                for partition in group:
                    equivalence_class.partitions.remove(partition)
                    equivalence_class.tree_ahu = key
                    equivalence_class.tree_tree = groups_ahu_trees[key]

                new_equivalence_class = equivalence_class.copy_empty_similarly_typed()
                new_equivalence_class.partitions = group
                new_equivalence_class.tree_ahu = key
                new_equivalence_class.tree_tree = groups_ahu_trees[key]
                equivalence_classes.append(new_equivalence_class)
            else:
                equivalence_class.tree_ahu = groups_ahu_trees[key]
                equivalence_class.tree_tree = groups_ahu_trees[key]

    return


def equivalence_classes_refine_hypercubes(equivalence_classes: "list[EquivalenceClass]") -> None:
    """
            Separates equivalence classes based on whether or not the partitions are of type hypercube
            :param equivalence_classes: the equivalenceClasses to refine in-place
        """

    # for each equivalence class currently there, update, split or do nothing based on whether or not the graphs are
    # trees
    for i in range(len(equivalence_classes)):

        equivalence_class = equivalence_classes[i]

        found_n = -1

        # if uniform (trees cant be uniform) and if not connected, continue, since they will not be trees
        if not equivalence_class.connected or not equivalence_class.uniform:
            continue

        # group for hypercube partitions
        hypercube = []

        # group for not hypercube partitions
        not_hypercube = []

        # for each partition in the equivalence class, put them in their respective group
        for partition in equivalence_class.partitions:
            n = 0
            if found_n != -1:
                n = found_n - 1
            v = len(partition.graph.vertices)
            e = len(partition.graph.edges)
            vert_count = 0
            edge_count = 0
            while vert_count < v and edge_count < e:
                n += 1
                vert_count = 2 ** n
                edge_count = 2 ** (n - 1) * n

            if vert_count == v and edge_count == e:
                if check_if_bipartite(partition.graph):
                    hypercube.append(partition)
                    found_n = n

            if partition not in hypercube:
                not_hypercube.append(partition)

        # all are non hypercube, so no need to do anything
        if len(hypercube) == 0:
            pass

        # all are hypercube, no need to split, only need to update tags
        elif len(not_hypercube) == 0:
            equivalence_class.hypercube = True
            equivalence_class.hypercube_n = found_n

        # some are hypercube, some are not, split them based on that
        else:
            equivalence_class.partitions = not_hypercube

            new_equivalence_class = equivalence_class.copy_empty_similarly_typed()
            new_equivalence_class.hypercube = True
            new_equivalence_class.partitions = hypercube
            new_equivalence_class.hypercube_n = found_n
            equivalence_classes.append(new_equivalence_class)

    # return nothing, since it update the equivalence classes in place
    return


def check_if_bipartite(graph):
    color1 = {graph.vertices[0]}
    color2 = set()
    stack = {graph.vertices[0]}
    while stack:
        vertex = stack.pop()
        if vertex in color1:
            for neighbour in vertex.neighbours:
                if neighbour in color1:
                    return False
                if neighbour not in color2:
                    color2.add(neighbour)
                    stack.add(neighbour)
        if vertex in color2:
            for neighbour in vertex.neighbours:
                if neighbour in color2:
                    return False
                if neighbour not in color1:
                    color1.add(neighbour)
                    stack.add(neighbour)
    return True


def equivalence_classes_refine_distances_vertex(equivalence_classes: "list[EquivalenceClass]") -> None:
    """
        Separates uniform equivalence classes by a hashing algorithm for the graphs based on the distances too each
        pair of vectors
        :param equivalence_classes: the equivalenceClasses to refine in-place
    """

    # for each equivalence class currently there, update, split or do nothing based on the hash of the graph of the
    # partitions in the equivalence class
    for i in range(len(equivalence_classes)):

        equivalence_class = equivalence_classes[i]

        # if not uniform, return, due to high complexity and negligible effects on non uniform colorings
        if not equivalence_class.uniform:
            continue

        # the groups based on the distances between each pair of vertices
        groups = dict()

        # for each partition in the equivalence class, put them in their respective group
        for partition in equivalence_class.partitions:

            hashed_distances = hash_graph_distances(partition.graph)
            if hashed_distances in groups:
                groups[hashed_distances].append(partition)
            else:
                groups[hashed_distances] = [partition]

        # for each group of partitions
        for group in groups.values():

            # if there are 2 different groups (so old class and new class would both be non empty)
            if len(group) != 0 and len(group) != len(equivalence_class.partitions):
                for partition in group:
                    equivalence_class.partitions.remove(partition)

                new_equivalence_class = equivalence_class.copy_empty_similarly_typed()
                new_equivalence_class.partitions = group
                equivalence_classes.append(new_equivalence_class)

    # return nothing, since it update the equivalence classes in place
    return


def distances_to_other_vertices(vertex, graph):
    distances = []
    n = len(graph.vertices)
    seen = {vertex}
    prev = {vertex}
    depth = 0
    found = 1
    while found < n:
        depth += 1
        cur = set()
        for vertex in prev:
            for neighbour in vertex.neighbours:
                if neighbour not in seen:
                    seen.add(neighbour)
                    cur.add(neighbour)
                    distances.append(depth)
                    found += 1
        prev = cur
    distances.sort()
    return hash(tuple(distances))


def hash_graph_distances(graph):
    hashes = []
    for vertex in graph.vertices:
        hashes.append(distances_to_other_vertices(vertex, graph))
    hashes.sort()
    return hash(tuple(hashes))


def equivalence_classes_refine_branching(equivalence_classes: "list[EquivalenceClass]") -> None:
    """
        Separates the given equivalence classes based on branching till it finds isomorphisms
        :param equivalence_classes: the equivalenceClasses to refine in-place
    """

    # for each equivalence class currently there, update, split or do nothing based on the hash of the graph of the
    # partitions in the equivalence class
    for i in range(len(equivalence_classes)):

        equivalence_class = equivalence_classes[i]

        if equivalence_class.tree:
            continue

        # the groups based on whether there exist an isomorphism between partitions
        groups = []

        stack = set(equivalence_class.partitions.copy())

        while stack:
            partition_a = stack.pop()
            group = [partition_a]
            for partition_b in list(stack.copy()):
                check=False
                if len(partition_b.graph.vertices) < 60:
                    if countIsomorphisms2(partition_a.copy().graph, partition_b.copy().graph):
                        check = True
                else:
                    if found_isomorphism(partition_a.copy(), partition_b.copy()):
                        check = True
                if check:
                    group.append(partition_b)
                    stack.remove(partition_b)
            groups.append(group)

        # for each group of partitions
        for group in groups:

            # if there are 2 different groups (so old class and new class would both be non empty)
            if len(group) != 0 and len(group) != len(equivalence_class.partitions):
                for partition in group:
                    equivalence_class.partitions.remove(partition)

                new_equivalence_class = equivalence_class.copy_empty_similarly_typed()
                new_equivalence_class.partitions = group
                equivalence_classes.append(new_equivalence_class)

    # return nothing, since it update the equivalence classes in place
    return


def found_isomorphism(partition_a: "Partition", partition_b: "Partition") -> "bool":
    """
        Tries to find an isomorphism by going through all branches till it finds one
        :param partition_a: first partition
        :param partition_b: second partition
        :returns: bool which represents if it has found an isomorphism
    """

    # updates the partitions
    hopcroft_refinement([partition_a, partition_b], [partition_a.length() - 1])

    # if there is no bijection, move upward on the branch and continue
    if not check_if_balanced(partition_a, partition_b):
        return False

    # if there is 1 bijection, return
    if check_if_bijection(partition_a):
        return True

    # for each color in the first partition with multiple vertices, pick an arbitrary vertex and start branching
    # with that vertex, till an isomorphism is found or continue branching if there is none found
    color=arbitrary_vertex_picker(partition_a)
    x = next(iter(color.vertices))
    index_color = color.colornum
    for y in partition_b.colors[index_color].vertices:
        copy_a = partition_a.copy()
        copy_a.colors[index_color].vertices.remove(x)
        copy_b = partition_b.copy()
        copy_b.colors[index_color].vertices.remove(y)
        newcolor_a = Color({x}, copy_a)
        copy_a.add_color(newcolor_a)
        newcolor_b = Color({y}, copy_b)
        copy_b.add_color(newcolor_b)
        if found_isomorphism(copy_a, copy_b):
            return True
    return False


def arbitrary_vertex_picker(partition_a):
    for color in partition_a.colors:
        if color.length() > 1:
            return color

def check_if_balanced(partition_a: "Partition", partition_b: "Partition") -> "bool":
    """
        Checks if the 2 partitions are balanced
        :param partition_a: the first partition
        :param partition_b: the second partition
        :returns: a boolean that represents if the 2 partitions are balanced
    """

    # check if the 2 partitions have the same amount of colors, if the do not they are not balanced
    if partition_a.length() != partition_b.length():
        return False

    # check if each color has the same amount of vertices in both partitions, if not, they are not balanced
    for i in range(partition_a.length()):
        if partition_a.colors[i].length() != partition_b.colors[i].length():
            return False

    # the 2 partitions are balanced
    return True


def check_if_bijection(partition_a: "Partition") -> "bool":
    """
        Checks if there is an unique mapping (only 1 possible mapping) between the 2 partitions, but since they are
        balanced and they are colored at the same time, we just need to check if 1 of the 2 partitions only has
        colors of length 1 (or 0)
        :param partition_a: the first partition
        :returns: a boolean that represents if there is 1 bijection possible between the 2 partitions
    """
    # check if all colors in the first partition have at most length 1, if not there is not an unique bijection
    for color in partition_a.colors:

        # check if there is no unique bijection
        if color.length() > 1:
            return False

    # there is an unique mapping
    return True
