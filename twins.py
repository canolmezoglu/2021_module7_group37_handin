from old_branching import *
from our_lib import factorial

def get_twins(G):
    sames = set()
    not_connected = set()
    for v in G.vertices:
        if v.degree>0:
            for v2 in v.neighbours:
                if check_twins(v,v2):
                    if (v,v2) not in sames and (v2,v) not in sames:
                        sames.add((v,v2))
        else:
            not_connected.add(v)
    twins_dict = dict()
    for p in sames:
        if p[0] not in twins_dict:
            twins_dict[p[0]] = set()
            twins_dict[p[0]].add(p[0])
        if p[1] not in twins_dict:
            twins_dict[p[1]] = set()
            twins_dict[p[1]].add(p[1])
        twins_dict[p[0]].add(p[1])
        twins_dict[p[1]].add(p[0])
    visited = set()
    newdict = dict()
    for equivalences in twins_dict:
        if equivalences not in visited:
            if equivalences not in newdict:
                newdict[equivalences] = twins_dict[equivalences]
                visited = visited.union(newdict[equivalences])
    factor = 1
    listoftwins=[]
    if len(not_connected) > 0:
        factor = factor * factorial(len(not_connected))
        for vertex in not_connected:
            if vertex in G.vertices:
                G.remove_vertex(vertex)
    false_twins=list()
    true_twins=list(get_true_twins(G))
    # true_twins=[]


    for twins in true_twins:
        leng = len(twins)
        listoftwins.append(leng)
        n = twins.pop()
        factor = factor * factorial(leng)
        for v in twins:
               if v in G.vertices:
                  G.remove_vertex(v)
    # if len(not_connected) > 0:
    #     factor = factor * factorial(len(not_connected))
    #     for vertex in not_connected:
    #         if vertex in G.vertices:
    #             G.remove_vertex(vertex)

    for twins in newdict.values():
        leng=len(twins)
        listoftwins.append(leng)
        n=twins.pop()
        factor = factor * factorial(leng)
        for v in twins:
            if v in G.vertices:
                G.remove_vertex(v)
    G.update_labels()
    return G, factor,false_twins


def check_twins(v, u):
    set1 = v.set_of_neighbours
    if u in set1:
        set1.remove(u)
    else:
        return False
    set2 = u.set_of_neighbours
    if v in set2:
        set2.remove(v)
    else:
      return False
    return set1 == set2

def get_true_twins(g):
    neighb=dict()
    for v in g.vertices:
        neigbb=frozenset(v.set_of_neighbours)
        if neigbb not in neighb:
            neighb[neigbb]=set()
        neighb[neigbb].add(v)
    temp=list()
    for ne in neighb:
        if len(neighb[ne])>1:
            temp.append(neighb[ne])
    return temp

if __name__ == "__main__":
    startt = time()
    with open('graphs/wheelstar15.grl') as f:
        G = load_graph(f, read_list=True)
    graphs = G[0]
    # print(countIsomorphisms3(graphs[1],graphs[2]))
    # s,yy=twins(graphs[1])
    # gw,yyr=twins(graphs[2])
    # print(yyr)
    # print(countIsomorphisms3(gw,s))
    for i in range(0,len(graphs)):
        get_twins(graphs[i])
    finish = time() - startt
    print(finish)
