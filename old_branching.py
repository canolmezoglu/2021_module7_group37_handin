from old_refinement import *
from graph_io import *
from basic_permutation_group import *


def match_colors_to_degrees(graph):
    """
           Returns a graph with vertex colornums matched with the vertex degrees
           :param graph: The given graph
     """
    colordict = dict()
    for vertex in graph.vertices:
        colordict[(vertex.graph, vertex.label)] = vertex.degree
    return colordict
def countIsomorphisms3(G, H, first=True):
    """
             Returns the number of automorphisms between given graph G and H
             :param G: The given graph G
             :param H: The given graph H
             :param first : a boolean indicating if it's the first iteration of the
             :
       """
    if first:
        B = G + H
        colordict=match_colors_to_degrees(B)
    else:
        B=G
        colordict=H
    colordict=hopcroft(B,colordict)
    g1, g2 = separate_colordict(colordict,B)
    if not balanced(g1, g2):
        return 0
    if bijection(g1):
        return 1
    v = arbitrary_vertex_picker(g1)
    oldcolor = colordict[(v.graph,v.label)]
    newcolor = color_number_getter(g1)
    colordict[(v.graph,v.label)]= newcolor
    num = 0
    for g2_vertex in g2[oldcolor]:
        newdict=dict(colordict)
        newdict[(g2_vertex.graph,g2_vertex.label)]= newcolor
        num = num + countIsomorphisms3(B, newdict, False)
    return num

def cc(G,H):
    generatingSet=[]
    B = G + H
    colordict = match_colors_to_degrees(B)
    countIsomorphisms(B,colordict,generatingSet,True,False)
    return OrderGenerators(generatingSet)

def countIsomorphisms(G, H,generatingSet, first, trivial=True):
    """
             Returns the number of automorphisms between given graph G and H
             :param G: The given graph G
             :param H: The given graph H
             :param first : a boolean indicating if it's the first iteration of the
    """

    # if first:
    #     B = G + H
    #     colordict = match_colors_to_degrees(B)
    #     # if this is the first iteration, make B the union and
    #     # initialize a dict with vertex->colornum
    if True:
        B = G
        colordict = H
        # if this is not the first iteration, then B is the union of
        # both graphs and H is a dict with their colors
    colordict = hopcroft(B, colordict)
    # update the colors based on hopcroft
    g1, g2 = separate_colordict(colordict, B)
    # separate the color dictionary based on the the graph
    # the vertices inside belong by vertex.graph
    if not balanced(g1, g2):
        return 0,
    if bijection(g1):
        graph_size = len(colordict)*(0.5)
        permutation1 = (make_permutation(colordict, g1, graph_size))
        generatingSet+=permutation1
        return 1,
    v = arbitrary_vertex_picker(g1)
    oldcolor = colordict[(v.graph, v.label)]
    newcolor = color_number_getter(g1)
    colordict[(v.graph, v.label)] = newcolor
    num = 0
    for g2_vertex in g2[oldcolor]:
        newdict = dict(colordict)
        newdict[(g2_vertex.graph, g2_vertex.label)] = newcolor
        if g2_vertex.label == v.label:
            num2 = countIsomorphisms(B, newdict, False, True,generatingSet)
            if not num2: continue
            num = num + num2
        else:
            num2 = countIsomorphisms(B, newdict, False, False,generatingSet)
            if not num2: continue
            num = num + num2
        if num > 0 and not trivial:
            return num
    return num
def countIsomorphisms1(G, H, first=True):
    """
             Returns the number of automorphisms between given graph G and H
             :param G: The given graph G
             :param H: The given graph H
             :param first : a boolean indicating if it's the first iteration of the
    """

    if first:
        B = G + H
        colordict = match_colors_to_degrees(B)
        # if this is the first iteration, make B the union and
        # initialize a dict with vertex->colornum
    else:
        B = G
        colordict = H
        # if this is not the first iteration, then B is the union of
        # both graphs and H is a dict with their colors
    colordict = hopcroft(B, colordict,True)
    # update the colors based on hopcroft
    g1, g2 = separate_colordict(colordict, B)
    # separate the color dictionary based on the the graph
    # the vertices inside belong by vertex.graph
    if not balanced(g1, g2):
        return 0
    if bijection(g1):
        return 1
    v = arbitrary_vertex_picker(g1)
    oldcolor = colordict[(v.graph, v.label)]
    newcolor = color_number_getter(g1)
    colordict[(v.graph, v.label)] = newcolor
    num = 0
    for g2_vertex in g2[oldcolor]:
        newdict = dict(colordict)
        newdict[(g2_vertex.graph, g2_vertex.label)] = newcolor
        num=num+countIsomorphisms1(B, newdict, False)
    return num

def countIsomorphisms2(G, H, first=True):
    """
             Returns the number of automorphisms between given graph G and H
             :param G: The given graph G
             :param H: The given graph H
             :param first : a boolean indicating if it's the first iteration of the
    """

    if first:
        B = G + H
        colordict = match_colors_to_degrees(B)
        # if this is the first iteration, make B the union and
        # initialize a dict with vertex->colornum
    else:
        B = G
        colordict = H
        # if this is not the first iteration, then B is the union of
        # both graphs and H is a dict with their colors
    colordict = hopcroft(B, colordict,first)
    # update the colors based on hopcroft
    g1, g2 = separate_colordict(colordict, B)
    # separate the color dictionary based on the the graph
    # the vertices inside belong by vertex.graph
    if not balanced(g1, g2):
        return False
    if bijection(g1):
        return True,
    v = arbitrary_vertex_picker(g1)
    oldcolor = colordict[(v.graph, v.label)]
    newcolor = color_number_getter(g1)
    colordict[(v.graph, v.label)] = newcolor
    num = 0
    for g2_vertex in g2[oldcolor]:
        newdict = dict(colordict)
        newdict[(g2_vertex.graph, g2_vertex.label)] = newcolor
        if countIsomorphisms2(B, newdict, False):
            return True
        else:
            continue
    return False
def make_permutation(colordict, g1, g2, graph_size):
    """
                Returns a dict with mappings v1->v2
                :param colordict: a dictionary with (vertex.graph,vertex.label)=>color
                :param g1: a dictionary for g1 with color=>{vertices}
                :param g2 : a dictionary for g2 with color=>{vertices}
                :param graph_size : the amount of vertices in the graph for which a permutation should be created
          """
    permutation_list = [0]*len(g1.vertices)

    for key in colordict.keys():
        # iterate over all colors
        color = colordict[key]
        g1v = g1[color][0]
        g2v = g2[color][0]
        # get the g1 and g2 vertex representing that color

        permutation_list[g1v.label]=g2v.label

    return Permutation(graph_size, mapping=permutation_list)


def separate_colordict(colordict, B):
    """
                 Gets a dictionary with vertex-->color, returns two dictionaries
                 with color-->{set of vertices} for the two graphs added
                  :param colordict: The given dictionary with vertex-->color
                  :param B: The given union graph of two graphs
            """
    G1 = dict()
    G2 = dict()
    G = next(iter(colordict))[0]
    # get the name of one of the graphs to separate them
    for vertex in B:
        color = colordict[(vertex.graph, vertex.label)]
        # get the assigned color of the vertex
        if vertex.graph != G:
            if color not in G1:
                G1[color] = []
            G1[color].append(vertex)
        else:
            if color not in G2:
                G2[color] = []
            G2[color].append(vertex)
    return G1, G2


def balanced(g1, g2):
    """
                  Checks if given dicts G and H are balanced
                  :param g1: The given graph G
                  :param g2: The given graph H
            """
    try:
        if len(g1) != len(g2):
            return False
        for color in g1:
            if len(g1[color]) != len(g2[color]):
                return False
    except KeyError:
        return False
    return True


def bijection(g1):
    """
                    Checks if given graphs G has a bijection
                    :param g1: The given graph G
              """
    for color in g1:
        if len(g1[color]) > 1:
            return False
    return True


def arbitrary_vertex_picker(g1):
    """
                     picks a vertex to change the colornum with colornum > 1 from given graph g1
                    :param g1: The given graph g1
              """
    for color in g1:
        if len(g1[color]) > 1:
            return g1[color][1]


def color_number_getter(g1):
    """
                        returns a colornum inside given graph g1 that is unused
                        :param g1: The given graph g1
                  """
    for i in range(0, len(g1) + 1):
        if i not in g1:
            return i
def get_auto(g1,g2):
    return countIsomorphisms2(g1, g2, first=True)
def equivalenceClasses(graphs):
    visited=set()
    pff=[]
    for i in range(0,len(graphs)):
        for y in range(0, len(graphs)):
            if y==i:
                continue
            if y not in visited:
                if countIsomorphisms2(graphs[i],graphs[y]):
                       pff.append(tuple([i,y]))

        visited.add(i)
    return pff
if __name__ == "__main__":
    startt = time()
    with open('graphs/basic/basicAut2.gr') as f:
        G = load_graph(f, read_list=True)
    graphs = G[0]
    print((equivalenceClasses(graphs)))
    endt = time()
    print("time elapsed in seconds: ", endt - startt)


