import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


class Data:
    def __init__(self, datas):
        self.datas = datas
        
    def preprocessing(self):
        prep_data = []
        for data in self.datas:
            split_data = data.split(',')
            convert_data = list(map(int, split_data))
            prep_data.append(convert_data)
        return prep_data


class Node:
    def __init__(self, node):
        self.node = node
        self.connection = []
        
    def connect_node(self, other_node):
        self.connection.extend(other_node)


class Graph:
    def __init__(self, nodes, origin):
        self.nodes = nodes
        self.origin = origin
        
    def generate_polygon(self):
        size = 10
        segments = len(self.nodes)
        fillet = 0
        return gh.Polygon(rs.coerce3dpoint(self.origin), size, segments, fillet)[0]
        
    def generate_node_points(self):
        return gh.DeconstructBrep(self.generate_polygon())[2]
        
    def visualization(self):
        pass



if __name__ == "__main__":
    convert_data = Data(datas).preprocessing()
    
    nodes = []
    for i, conn in enumerate(convert_data):
        curr_node = Node(i)
        curr_node.connect_node(conn)
        nodes.append(curr_node)
        
    points = Graph(nodes, origin).generate_node_points()
    lines = []
    for i, node in enumerate(nodes):
        for c in node.connection:
            line = rs.AddLine(points[i], points[c])
            lines.append(line)