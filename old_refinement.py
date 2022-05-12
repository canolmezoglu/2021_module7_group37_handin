def vertex_neighbours_tolist(vertex):
    """
          Returns a list neighbours[] that contains the degrees of the neighbours of a given vertex
          :param vertex: The given vertex
    """
    neighbours = []
    for neighbour in vertex:
        neighbours.append(neighbour.colornum)
    return neighbours


def canonical_color_refinement(graph):
    """
           Returns a graph colored based on sorted neighbours in a stable way
           Two graphs inputted seperately would be colored in the same way
           :param graph: The given graph
     """
    x = 0

    for vertex in graph.vertices:
        # initializing all colors based on the degree of a given vertex
        vertex.colornum = vertex.degree

    while x < len(graph.vertices) - 1:
        # the algorithm iterates n-1 times, the maximum amount of iterations needed
        neighbours_to_colors = dict({})

        for vertex in graph.vertices:

            neighbours_degrees_list = tuple(sorted(vertex_neighbours_tolist(vertex.neighbours)))
            # this is a tuple as tuples can be used as keys for dict and it is to sorted to make sure unordered lists
            # with the same elements are equal

            if neighbours_degrees_list not in neighbours_to_colors:
                value_list = []
                value_list.append(vertex.label)
                neighbours_to_colors[neighbours_degrees_list] = value_list
            else:
                temp = neighbours_to_colors[neighbours_degrees_list]
                temp.append(vertex.label)
                neighbours_to_colors[neighbours_degrees_list] = temp
        color = 0
        changes = dict({})
        for key in sorted(neighbours_to_colors):
            # sort the neighbours so that the same neighbours in different graphs
            # get different colors
            temp = neighbours_to_colors[key]
            for i in temp:
                changes[i] = color
            color = color + 1
        off = 0
        for vertex in graph.vertices:
            if vertex.colornum == changes.get(vertex.label):
                off = off + 1
            vertex.colornum = changes.get(vertex.label)
        if off == len(graph.vertices):
            break
        # assign the changes proposed by this iteration in the graph
        x = x + 1
    return graph


def basic_color_refinement(graph, first=True):
    """
           Returns a graph colored based on neighbours in a stable way
           :param graph: The given graph
     """
    x = 0
    if first:
        for vertex in graph.vertices:
            vertex.colornum = vertex.degree

    while x < len(graph.vertices) - 1:
        # the algorithm iterates n-1 times, the maximum amount of iterations needed
        neighbours_to_colors = dict({})
        # dictionary that contains the mapping of a given neighbour list to a color_number
        changes = dict({})
        # dictionary that contains the current updates for the current iteration
        color = 0
        same_color_as_before_count = 0
        # this counts the amount of colors that are the same with the previous iteration to determine when to converge
        for vertex in graph.vertices:

            neighbours_degrees_list = tuple(sorted(vertex_neighbours_tolist(vertex.neighbours)))
            # this is a tuple as tuples can be used as keys for dict and it is to sorted to make sure unordered lists
            # with the same elements are equal

            if neighbours_degrees_list not in neighbours_to_colors:

                neighbours_to_colors[neighbours_degrees_list] = color

                if vertex.colornum == color:
                    same_color_as_before_count = same_color_as_before_count + 1
                    # increment the same_color_count if the proposed color change is the same as before
                changes[(vertex.label, vertex.graph)] = color
                # save the proposed change
                color = color + 1
                # change the current color_num is this color_num is used

            else:
                # in the case if this group of neighbours is same with a previous vertex
                if vertex.colornum == neighbours_to_colors.get(neighbours_degrees_list):
                    same_color_as_before_count = same_color_as_before_count + 1
                    # increment the same_color_count if the proposed color change is the same as before

                changes[(vertex.label, vertex.graph)] = neighbours_to_colors.get(neighbours_degrees_list)
                # save the proposed change

        if same_color_as_before_count == len(graph.vertices):
            x = len(graph.vertices)
            # if the number colors same as the previous iteration is the same as amount of possible colors stop the
            # algorithm early

        for vertex in graph.vertices:
            vertex.colornum = changes.get((vertex.label, vertex.graph))
        # assign the changes proposed by this iteration in the graph
        x = x + 1
    return graph


def match_colors_to_degrees(graph):
    """
           Returns a graph with vertex colornums matched with the vertex degrees
           :param graph: The given graph
     """
    colordict = dict()
    for vertex in graph.vertices:
        colordict[(vertex.graph, vertex.label)] = vertex.degree
    return colordict


def color_to_vertices(graph, colordict):
    """
             Returns a dict with colors mapped to a list of vertices with that color
             :param graph: The given graph
       """
    vertices_by_color = dict()
    for vertex in graph.vertices:
        if colordict[(vertex.graph, vertex.label)] not in vertices_by_color:
            vertices_by_color[colordict[(vertex.graph, vertex.label)]] = set()
        vertices_by_color[colordict[(vertex.graph, vertex.label)]].add(vertex)
    return vertices_by_color


def remove_the_largest(T):
    """
             Returns a list from a given dictionary and removes the key with the largest length of value
             :param T: the given dictionary
       """
    dicta = T.copy()
    key_to_remove = max(T, key=lambda k: len(T[k]))
    del dicta[key_to_remove]
    return set(dicta.keys())
    # a set is used for more removal and contains efficiency


def hopcroft(graph, colordict, test=False):
    if test:
        colordict = match_colors_to_degrees(graph)
    # if we are testing, create a dict with vertex->colornum
    T = color_to_vertices(graph, colordict)
    # get a dict with color->{vertices of that colour}
    W = remove_the_largest(T)
    # remove the color with the largest amount of vertices
    while W:
        a = W.pop()
        dict1 = dict()
        for i, vertex in enumerate(T[a]):
            if i == 0:
                dict1 = dict.fromkeys(vertex.neighbours, 1)
            # for more efficiency, initialize the dict with each neighbour
            # of the first vertex already added
            else:
                for neighbour in vertex.neighbours:
                    if neighbour not in dict1:
                        dict1[neighbour] = 1
                    else:
                        dict1[neighbour] = dict1[neighbour] + 1
        dict2 = dict()
        for element in dict1:
            temp = (colordict[(element.graph, element.label)], dict1[element])
            if temp not in dict2:
                dict2[temp] = set()
            dict2[temp].add(element)
        for key in dict2:
            newcolor = color_number_getter(T)
            oldcolor = key[0]
            if len(dict2[key]) != 0 and len(dict2[key]) != len(T[oldcolor]):
                for vertex in dict2[key]:
                    colordict[(vertex.graph, vertex.label)] = newcolor
                T[newcolor] = dict2[key]
                T[oldcolor] = T[newcolor].difference(T[oldcolor])
                if oldcolor in W:
                    W.add(newcolor)
                else:
                    if len(T[oldcolor]) < len(T[newcolor]):
                        W.add(oldcolor)
                    else:
                        W.add(newcolor)
    if test:
        for vertex in graph.vertices:
            vertex.colornum = colordict[(vertex.graph, vertex.label)]

    # return colordict,graph
    return colordict


def color_number_getter(g1):
    """
                        returns a colornum inside given graph g1 that is unused
                        :param g1: The given graph g1
                  """
    for i in range(0, len(g1) + 1):
        if i not in g1:
            return i
