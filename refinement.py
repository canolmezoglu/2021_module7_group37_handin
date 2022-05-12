from graph import *
from graph_io import *
from refinement_classes import Partition, Color
from time import time


def uniform_partitions(graphs: "list[Graph]"):
    """
        Arguments: <graphs> is the list of graphs to create partitions for
        Returns: a list with 1 partition per graph given
    """
    # partitions and stack to return
    partitions = list()
    stack = list()

    # for each graph, create a partition with all vertices in the same color
    for graph in graphs:
        partition = Partition(graph)
        color = Color(set(graph.vertices), partition)

        # for each vertex color it the uniform
        for vertex in color.vertices:
            vertex.colornum = 0
        partition.add_color(color)
        partitions.append(partition)

    # adding the new uniform color to the stack
    stack.append(0)

    # return the partitions and the stack
    return partitions, stack


def hopcroft_refinement(partitions: "list[Partitions]", stack):
    # keep track of which colors are currently in the stack
    inStack = list()

    # set all colors to not be in the stack
    for i in range(partitions[0].length()):
        inStack.append(False)

    # set the colors in the stack to being currently in the stack
    for i in stack:
        inStack[i] = True

    # color each vertex by their colornum according to the partitions.
    for partition in partitions:
        for color in partition.colors:
            colornum = color.colornum
            for vertex in color.vertices:
                vertex.colornum = colornum

    # while the stack is nonempty, get a color from the stack and perform one degree on the coloring
    while stack:
        colornum = stack.pop()
        inStack[colornum] = False
        hopcroft_refinement_helper(partitions, stack, colornum, inStack)


def hopcroft_refinement_helper(partitions, stack, colornum, inStack):

    groups = dict()
    encountered = set() # use other data structure?
    mainColors = []


    for i in range(len(partitions)):
        partitions[i].graph.index = i
        mainColors.append(partitions[i].colors[colornum])

    # For each color with the colornum in the partitions, go over the neighbours of all the vertices in those colors
    # and seperate those neighbours based on indegree in to the color and their color
    for color in mainColors:
        if color.vertices:
            for vertex in color.vertices:
                for neighbour in vertex.neighbours:
                    if neighbour not in encountered:
                        indegree = 0
                        for neighbour2 in neighbour.neighbours:
                            if neighbour2.colornum == colornum:
                                indegree += 1
                        key = tuple([neighbour.colornum, indegree])
                        if key in groups:
                            groups[key].add(neighbour)
                        else:
                            groups[key] = {neighbour}
                        encountered.add(neighbour)

    # for each group,
    # TODO: replace lamba function
    # TODO: optimize not adding the largest color to the stack? Perhaps by switching the vertices between old color and
    # TODO: new color when old color is not in the stack and |old color| < |new color|
    #for key in sorted(reversed(sorted(groups.keys())), key = lambda k: k[0]):
    for key in sorted(groups.keys(), reverse=True):
    # or do groups.keys().sort(reverse=True)
    #for key in sorted(groups.keys(), key=lambda k: k[0]):
        colorIndex = key[0]
        colorGroups = []
        newColors = []

        for index in range(len(partitions)):
            colorGroups.append(set())
            newColors.append([])

        # is there a new color
        new = False

        # seperate the group into subgroups by their graph
        for vertex in groups[key]:
            colorGroups[vertex.graph.index].add(vertex)

        # for each subgroup, test if there will be a new color
        for index in range(len(partitions)):
            group = colorGroups[index]
            color = partitions[index].colors[colorIndex]

            # there is a new color, since intersection and difference are both non-empty
            if len(group) > 0 and len(group) != len(color.vertices):
                new = True
                difference = color.vertices.difference(group)
                newColor = Color(group, partitions[index])
                newColors[index] = newColor
                color.vertices = difference

            # create an empty color, which will not be added if there is no new color created
            else:
                newColors[index] = Color({}, partitions[index])

        # new color created, hence add all colors to their respective partitions.
        if new:
            inStack.append(False)

            # calculate the maximum lenth for both colors, to determine which color to add to the stack
            maxLength = 0
            maxLengthOld = 0

            # for each partition, add the new color to the partition and update the maximum of the color if it contains
            # a longer color
            for index in range(len(partitions)):
                partitions[index].add_color(newColors[index])
                maxLengthOld = max(maxLengthOld, len(partitions[index].colors[colorIndex].vertices))
                if newColors[index]:
                    maxLength = max(maxLength, len(newColors[index].vertices))
                    for vertex in newColors[index].vertices:
                        vertex.colornum = newColors[index].colornum

            # if the original color is already in the stack, add the new color to the stack
            if inStack[colorIndex]:
                stack.append(newColors[0].colornum)

            # if the original color is not in the stack currently, add the shortest of the old
            # and new color to the stack
            else:
                if maxLength > maxLengthOld:
                    stack.append(colorIndex)
                    inStack[colorIndex] = True
                else:
                    stack.append(newColors[0].colornum)
                    inStack[newColors[0].colornum] = True


def refine_partitions_by_color_group_size(partitions: "list[partition]"):
    """
        Refine colors by dividing vertices into connected groups (all with same color) and coloring them based on
        group size, should only need to be done once
    """
    for partitionIndex in range(len(partitions)):
        for vertex in partitions[partitionIndex].graph.vertices:
            vertex.index = partitionIndex

    for colorIndex in range(partitions[0].length()):

        groups = dict()

        for partitionIndex in range(len(partitions)):
            color = partitions[partitionIndex].colors[colorIndex]
            if color.length() < 2:
                continue
            colornum = color.colornum
            stack = color.vertices.copy()

            while stack:
                group = {stack.pop()}
                cur = group.copy()
                while cur:
                    x = cur.pop()
                    for neighbour in x.neighbours:
                        if neighbour.colornum == colornum and neighbour not in group:
                            group.add(neighbour)
                            cur.add(neighbour)
                length = len(group)
                if length in groups:
                    for vertex in group:
                        groups[length].add(vertex)
                else:
                    groups[length] = group

        for group in groups.values():
            curGroups = []
            newColors = []

            for partitionIndex in range(len(partitions)):
                curGroups.append(set())
                newColors.append([])

            for vertex in group:
                curGroups[vertex.index].add(vertex)

            # is there a new color
            new = False

            for partitionIndex in range(len(partitions)):
                group = curGroups[partitionIndex]
                color = partitions[partitionIndex].colors[colorIndex]

                # there is a new color, since intersection and difference are both non-empty
                if len(group) > 0 and len(group) != len(color.vertices):
                    new = True
                    difference = color.vertices.difference(group)
                    newColor = Color(group, partitions[partitionIndex])
                    newColors[partitionIndex] = newColor
                    color.vertices = difference

                # create an empty color, which will not be added if there is no new color created
                else:
                    newColors[partitionIndex] = Color({}, partitions[partitionIndex])

            if new:
                for partitionIndex in range(len(partitions)):
                    partitions[partitionIndex].colors[colorIndex].update_vertices(partitions[partitionIndex].colors[colorIndex].vertices)
                    partitions[partitionIndex].add_color(newColors[partitionIndex])
                    for vertex in newColors[partitionIndex].vertices:
                        vertex.colornum = newColors[partitionIndex].colornum


def combine_graphs(graphs: "list[Graph]") -> "Graph":
    # create a new graph
    result = Graph(graphs[0].directed)
    # create a dictionary to map vertices of graph in graphs to vertices in new graph
    mapping = dict()

    # for each graph
    for graph in graphs:

        # for each vertex in the graph create a new vertex in the new graph and map it
        for vertex in graph.vertices:
            newVertex = Vertex(result)
            newVertex.colornum = vertex.colornum
            mapping[vertex] = newVertex

        # for each edge in the graph add a new edge to the new graph using the dictionary
        for edge in graph.edges:
            newEdge = Edge(mapping[edge.tail], mapping[edge.head], edge.weight)
            result.add_edge(newEdge)

    # return new graph
    return result



if __name__ == "__main__":

    with open('graphs/colorref_largeexample_4_1026.grl') as f:
        G = load_graph(f, read_list=True)
    startt = time()
    graphs = G[0]
    partitions, stack = uniform_partitions(G[0])
    hopcroft_refinement(partitions, stack)
    for partition in partitions:
        temp = []
        for color in partition.colors:
            temp.append(len(color.vertices))
        print(len(temp))
    endt = time()
    print("time elapsed in seconds: ", endt - startt)
    with open('testGraph.dot', 'w') as f:
        write_dot(combine_graphs(graphs), f)
    # with open('testGraph2.dot', 'w') as f:
    #     write_dot(graphs[1], f)
