from refinement_classes import Color, Partition
from refinement import hopcroft_refinement
from basic_permutation_group import OrderGenerators
from permv2 import Permutation
from graph import Graph, Vertex, Edge


def main(partitions: "list[Partition]", classes: "set[int]") -> "list[set[int]]" and "list[int]":
    """
        Calculates the amount of automorphisms for each equivalence class using pruning and ideas from Lecture 4.
        :param partitions: the partitions
        :param classes: the equivelance classes of the partitions
    """

    # the equivalence classes and automorphism count classes
    equivalence_classes = list(classes)
    auto_classes = []

    # for each equivelance class, go through the trivial branch and then for each trivial node on the trivial branch
    # go down a non trivial branch to find an isomorphisms and get the permutation done to achieve that branch and add
    # it if it is not in the span of the generating set
    for current_class in equivalence_classes:

        # get 1 partition to calculate the #auto from
        partition = partitions[next(iter(current_class))]

        # the trivial branch that will store the trivial nodes
        trivial_branch = list()

        # create a copy of the partition
        copy = partition.copy()
        n = [0]
        # branch with the copied partition and a copy of the copied partition on another graph, this is important
        # because otherwise it will try to refine 2 partitions that are on the same graph
        generate_trivial_branch(copy, copy_partition_to_copy_graph(copy), trivial_branch, n)

        # the generating set that should span the automorphisms
        generating_set = []

        # for each trivial node pair (the 2 copy partitions), go down a non trivial branch and find a non trivial
        # permutation that leads to a non trivial isomorphism
        for pair in trivial_branch:
            generate_non_trivial_branch(pair[0], pair[1], list(), generating_set, False, False)

        # if the generating set contains permutations, calculate its order, else it has #auto = 1
        if len(generating_set) > 0:
            auto_classes.append(
                "iteration count: " + str(n[0]) + " , " + " generating set size " + str(len(generating_set)) + " , " +
                " #aut " + str(OrderGenerators(generating_set)))
        else:
            auto_classes.append(1)

    # return the equivalence classes and its corresponding automorphisms counts
    return classes, auto_classes


def main_automorphisms(equivalence_class) -> None:
    """
        Calculates the amount of automorphisms for each equivalence class using pruning and ideas from Lecture 4.
        :param equivalence_class: the equivalence classes of the partitions
    """

    # get 1 partition to calculate the #auto from
    partition = equivalence_class.partitions[0]

    # the trivial branch that will store the trivial nodes
    trivial_branch = list()

    # create a copy of the partition
    copy = partition.copy()
    n = [0]

    # branch with the copied partition and a copy of the copied partition on another graph, this is important
    # because otherwise it will try to refine 2 partitions that are on the same graph
    generate_trivial_branch(copy, copy_partition_to_copy_graph(copy), trivial_branch, n)

    # the generating set that should span the automorphisms
    generating_set = []


    # for each trivial node pair (the 2 copy partitions), go down a non trivial branch and find a non trivial
    # permutation that leads to a non trivial isomorphism
    for pair in trivial_branch:
        generate_non_trivial_branch(pair[0], pair[1], list(), generating_set, False, False)

    # if the generating set contains permutations, calculate its order, else it has #auto = 1
    if len(generating_set) > 0:
        equivalence_class.automorphisms = OrderGenerators(generating_set) * partition.graph.factor
    else:
        equivalence_class.automorphisms = 1

    return


def generate_trivial_branch(partition_a: "Partition", partition_b: "Partition",
                            trivial_branch: "list[[Partition, Partition]]", n):
    """
        Goes down a trivial branch, storing for each trivial permutation, the permutation and the partitions
        :param partition_a: the first partition
        :param partition_b: the second partition
        :param trivial_branch: the trivial branch list given to store the trivial nodes in
        :returns: True if it found an isomorphism node, False if there is no isomorphism node on this branch and adds
        a copy of the 2 partitions as a pair to the trivial branch given
    """

    n[0] += 1
    # update the partitions
    hopcroft_refinement([partition_a, partition_b], [partition_a.length() - 1])

    # if it is not balanced, there is no bijection, so go up the branch
    if not check_if_balanced(partition_a, partition_b):
        return False

    # if there is 1 bijection, go up the branch and store the previous trivial nodes
    if check_if_bijection(partition_a):
        return True

    # for each color in the partition, check if it has multiple vertices and if so, try to branch on it
    for color_a in partition_a.colors:

        # if the color has multiple vertices
        if color_a.length() > 1:

            # for each vertex in the color
            for vertex_a in color_a.vertices:

                # create a copy of the first partition, and separate 'the color' into 2, with new color having 1 vertex
                copy_a = partition_a.copy()
                copy_a.colors[color_a.colornum].vertices.remove(vertex_a)
                newcolor_a = Color({vertex_a}, copy_a)
                copy_a.add_color(newcolor_a)

                # get the corresponding vertex from the other partition
                vertex_b = partition_b.graph.vertices[vertex_a.label]

                # check if it is the right vertex
                if vertex_b.label == vertex_a.label:

                    # create a copy of the second partition, and separate 'the color' into 2, with new color having
                    # 1 vertex, the one corresponding to the vertex selected in partition a for its new color
                    copy_b = partition_b.copy()
                    copy_b.colors[color_a.colornum].vertices.remove(vertex_b)
                    newcolor_b = Color({vertex_b}, copy_b)
                    copy_b.add_color(newcolor_b)

                    # try to branch
                    if generate_trivial_branch(copy_a, copy_b, trivial_branch, n):
                        trivial_branch.append([partition_a.copy(), partition_b.copy()])
                        return True

                # safeguard, in case the vertices in the graph are not stored sequentually, but that should never happen
                else:
                    print("vertices not stored sequentially in the graph")
                    for vertex_b in partition_b.colors[color_a.colornum].vertices:
                        if vertex_b.label == vertex_a.label:
                            copy_b = partition_b.copy()
                            copy_b.colors[color_a.colornum].vertices.remove(vertex_b)
                            newcolor_b = Color({vertex_b}, copy_b)
                            copy_b.add_color(newcolor_b)
                            if generate_trivial_branch(copy_a, copy_b, trivial_branch, n):
                                trivial_branch.append([partition_a.copy(), partition_b.copy()])
                                return True


def basic_branch(partitions: "list[Partition]", classes: "set[int]") -> "list[set[int]]" and "list[int]":
    """
         Calculates the amount of automorphisms for each equivalence class using ideas from Lecture 2.
         :param partitions: the partitions
         :param classes: the equivelance classes of the partitions
     """
    equivalence_classes = list(classes)
    auto_classes = []

    # go over each equivalence class
    for clas in equivalence_classes:
        # get 1 partition to calculate the #auto from
        partition = partitions[next(iter(clas))]

        # create a copy of the partition
        copy = partition.copy()
        # create a list to count the iteration count
        n = [0]

        num = basic_branching(copy, copy_partition_to_copy_graph(copy), n)

        auto_classes.append("iteration count: " + str(n[0]) +
                            " #aut " + str(num))

    # return the equivalence classes and its corresponding automorphisms counts
    return classes, auto_classes


def basic_branching(partition_a: "Partition", partition_b: "Partition", n):
    """
         Uses basic branching and ideas from Lectures 2 to count automorphisms
         between 2 partitions
         :param partition_a: the first partition
         :param partition_b: the second partition
         :param n: a list to count the amount of iterations for performance concerns
     """
    # increment the iteration counter
    n[0] += 1
    # update the partitions
    hopcroft_refinement([partition_a, partition_b], [partition_a.length() - 1])

    # if it is not balanced, there is no bijection, so go up the branch
    if not check_if_balanced(partition_a, partition_b):
        return 0

    # if there is 1 bijection, go up the branch and store the previous trivial nodes
    if check_if_bijection(partition_a):
        return 1
    # pick an arbitrary vertex from the first partition to start coloring
    color_a = get_arbitrary_vertex(partition_a)
    vertex_a = next(iter(color_a.vertices))
    # set the initial amount of automorphims to 0
    num = 0
    for vertex_b in partition_b.colors[color_a.colornum].vertices:
        # create a copy of the first partition, and separate 'the color' into 2, with new color having 1 vertex
        copy_a = partition_a.copy()
        copy_a.colors[color_a.colornum].vertices.remove(vertex_a)
        # copy_a.colors[color_a.colornum]._length -= 1 (THINK THIS WORSENS IT)
        newcolor_a = Color({vertex_a}, copy_a)
        copy_a.add_color(newcolor_a)
        # create copy of the second partition, seperate 'the color' into 2, with new color having 1 vertex
        copy_b = partition_b.copy()
        copy_b.colors[color_a.colornum].vertices.remove(vertex_b)
        # copy_b.colors[color_a.colornum]._length -= 1 (THINK THIS WORSENS IT)
        newcolor_b = Color({vertex_b}, copy_b)
        copy_b.add_color(newcolor_b)

        num = num + basic_branching(copy_a, copy_b, n)

    return num


def get_arbitrary_vertex(partition_a):
    """
         Picks an arbitrary vertex with degree(vertex)>1 for branching
         :param partition_a: the partition where the vertex is picked from
         :returns: the color with the chosen two vertices
        """
    # for each color in the partition, check if it has multiple vertices and if so, try to branch on it
    for color_a in partition_a.colors:

        # if the color has multiple vertices
        if color_a.length() > 1:
            return color_a


def generate_non_trivial_branch(partition_a: "Partition", partition_b: "Partition", cycles: "list[[int, int]]",
                                generating_set: "list[Permutation]", non_trivial: "bool", non_trivial_2):
    """
        First deviates from trivial branch then just goes down random branch till finds an isomorphism
        :param partition_a: the first partition
        :param partition_b: the second partition
        :param cycles: the cycles it has gone through so far
        :param generating_set: the generating set for the automorphisms of the graph
        :param non_trivial: whether it has gone through a non trivial cycle
        :param non_trivial_2:
        :returns: False if there is no bijection, True if there is 1 bijection, Else None, but it passes the permutation
        it used to get to the non trivial branch to the generating set
    """
    # update the partitions
    hopcroft_refinement([partition_a, partition_b], [partition_a.length() - 1])

    # if it is not balanced, there is no bijection, so go up the branch
    if not check_if_balanced(partition_a, partition_b):
        return False

    # if there is 1 bijection, pass the permutation it used to get to this leave to the generating set
    if check_if_bijection(partition_a):

        # not sure why, but if it is not here it changes #auto = 1 to # auto = 0
        if len(cycles) > 0:

            # the amount of vertices in the graph
            n = len(partition_a.graph)

            # the permutation it used to get to this leave
            perm = Permutation(n,
                               # mapping = CyclesToMapping(cycles, n))
                               # print("perm by cycles" + str(perm))
                               # perm2 = permutation(n,
                               mapping=color_to_mapping(partition_a, partition_b))
            # print("perm by coloring" + str(perm2))

            # if the permutation is not yet in the generating set, add it
            # TODO: do membership testing here (currently broken, so not yet)
            if True:
                generating_set += [perm]

        return True

    # for each color in the partition, check if it has multiple vertices and if so, try to branch on it
    for color_a in partition_a.colors:

        # if there are multiple vertices in the color
        if color_a.length() > 1:

            # for each vertex in the color
            for vertex_a in color_a.vertices:

                # Assumption: from the trivial node you can immediately go into a nontrivial node that leads to a
                # isomorphism
                go_to_parent = False
                for vertex_b in partition_b.colors[color_a.colornum].vertices:

                    # if it leads to a non trivial node, try another vertex
                    if not non_trivial_2 and vertex_a.label == vertex_b.label:
                        continue
                    copy_a = partition_a.copy()
                    copy_a.colors[color_a.colornum].vertices.remove(vertex_a)
                    # copy_a.colors[color_a.colornum]._length -= 1 (THINK THIS WORSENS IT)
                    newcolor_a = Color({vertex_a}, copy_a)
                    copy_a.add_color(newcolor_a)

                    # create copy of the second partition, seperate 'the color' into 2, with new color having 1 vertex
                    copy_b = partition_b.copy()
                    copy_b.colors[color_a.colornum].vertices.remove(vertex_b)
                    # copy_b.colors[color_a.colornum]._length -= 1 (THINK THIS WORSENS IT)
                    newcolor_b = Color({vertex_b}, copy_b)
                    copy_b.add_color(newcolor_b)

                    # create a copy of the nontrivial cycles done so far to reach this node on the branch and add the
                    # cycle done now iff it is non trivial
                    new_cycles = copy_list(cycles)
                    if vertex_a.label != vertex_b.label:
                        new_cycles.append([vertex_a.label, vertex_b.label])
                        go_to_parent = generate_non_trivial_branch(copy_a, copy_b, new_cycles, generating_set, True, True)
                    # if this branch has reached an isomorphism leave, return
                    else:
                        go_to_parent = generate_non_trivial_branch(copy_a, copy_b, new_cycles, generating_set, False, True)
                    if go_to_parent and non_trivial:
                        break
                return go_to_parent


def copy_list(input_list):
    """
         Copies a given list since the normal copy() does shallow copying
         :param input_list: the given list
         :returns: A new list with the same elements as the given list
        """
    new = []
    for i in input_list:
        new.append(i)
    return new


def cycles_to_mapping(cycles: "list[[int, int]]", n: "int") -> "list[int]":
    """
        Converts the cycles which contains duplicates and not yet combined to 1 mapping that is accepted by the
        permutation class
        :param cycles: a bunch of 2 length cycles, with possible duplicates
        :param n: the amount of vertices in the graph
        :returns: A valid mapping to create a permutation with
    """

    # creates trivial mapping
    mapping = []
    for i in range(n):
        mapping.append(i)

    # keep track of which cycles are already done
    done = set()

    # for each cycle, check if it has already been done, if not,
    # switch the elements with indicides being the pair elements
    for cycle in cycles:  # cycle in form (i, j)

        # if cycle not yet done
        cycle_hash = max(cycle[0], cycle[1]) * n + min(cycle[0], cycle[1])
        if cycle_hash not in done:
            # switch element i, j
            mapping[cycle[0]], mapping[cycle[1]] = mapping[cycle[1]], mapping[cycle[0]]

            # cycle now done
            done.add(cycle_hash)

    # return valid mapping
    return mapping


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


def color_to_mapping(partition_a, partition_b):
    """
        Maps color partitions to one another to make a permutation
        :param partition_a: color partition a
        :param partition_b: color partition b
        :returns: a mapping of the colors
    """
    # TODO optimize this
    mapping = []

    n = len(partition_b.graph)

    for i in range(n):
        mapping.append(i)

    for color in partition_a.colors:
        # if the color does not have any vertices, do not add it
        if len(color.vertices) != 1:
            continue
        vertex_1 = next(iter(color.vertices))

        vertex_2 = next(iter(partition_b.colors[color.colornum].vertices))
        # map vertex_1 to vertex_2
        mapping[vertex_1.label] = vertex_2.label
    return mapping


def copy_partition_to_copy_graph(partition: "Partition") -> "Partition":
    """
        Gives a copy of the partition in the copy of the graph of the partition
        :param: partition to copy in another identical graph
        :returns: the copied partition
    """

    # the original graph
    original_graph = partition.graph

    # the new graph that is a copy of the original graph
    new_graph = Graph(original_graph.directed)

    # mapping between vertices of original graph and new graph
    mapping = dict()

    # copy the vertices in the new graph
    for vertex in original_graph.vertices:
        new_vertex = Vertex(new_graph, vertex.label)
        new_graph.add_vertex(new_vertex)
        mapping[vertex] = new_vertex

    # copy the edges in the new graph
    for edge in original_graph.edges:
        new_edge = Edge(mapping[edge.tail], mapping[edge.head], edge.weight)
        new_graph.add_edge(new_edge)

    # the copy of the partition in the new graph
    new_partition = Partition(new_graph)

    # for each color in the partition (in order), copy it to the new partition with vertices in the new graph
    for colorIndex in range(partition.length()):

        # old color
        old_color = partition.colors[colorIndex]

        # vertices in the old color, but their copy in the new graph
        new_vertices = set()

        # copy the old vertices of the old color to the new color by their corresponding vertices in the new graph
        for vertex in old_color.vertices:
            if vertex in mapping:
                new_vertices.add(mapping[vertex])

        # new color, with the vertices in the new graph corresponding to the vertices of the old color
        new_color = Color(new_vertices, new_partition)
        new_partition.add_color(new_color)

    # return the copy partition
    return new_partition
