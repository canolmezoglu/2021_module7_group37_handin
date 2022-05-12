from graph import Graph, Vertex


class Partition(object):
    """
        A partition which represents a refinement for a graph
        :param graph:
        :param colors:
        :param length:
    """

    def __init__(self, graph: "Graph"):
        """
            Creates a partition
            :param graph: the graph it is a partition for
        """
        self.graph = graph
        self.colors = list()
        self.factor = 1
        self._length = 0

    def copy(self):
        """"
            :returns: a copy of the partition
        """
        copy = Partition(self.graph)
        for i in range(self._length):
            copy.add_color(Color(self.colors[i].vertices.copy(), copy))
        return copy

    def add_color(self, color: "Color"):
        """
            Adds the given color to the partition and gives it a colornum
            :param color: the color to add to the partition
        """
        color.colornum = self._length
        self.colors.append(color)
        self._length += 1

    def length(self):
        """
            :returns: the length of the partition
        """
        return self._length


class Color(object):
    """
        A color object that is in a partition with some colornum assigned by the partition with given vertices
        :param vertices: the vertices it has
        :param colornum: the color it is
        :param length: the length of the color (# vertices)
    """

    def __init__(self, vertices: "set[Vertex]", partition: "Partition"):
        """
            Creates a color
            :param vertices: the vertices that belong to this color
            :param partition: the partition it is in
        """
        self.vertices = vertices
        self.colornum = -1
        self.partition = partition
        self._length = len(self.vertices)

    def update_vertices(self, vertices):
        """
            Updates the vertices
            :param vertices: the new vertices
        """
        self.vertices = vertices
        self._length = len(self.vertices)

    def length(self):
        """
            Returns the length of the color
        """
        return self._length
