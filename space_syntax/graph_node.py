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
        
    def get_connection(self):
        return self.connection
        
    def get_depth(self):
        return self.depth
        
    def connect_node(self, other_node):
        self.connection.extend(other_node)
        
    def add_depth(self, depth):
        self.depth = depth

class Graph:
    def __init__(self, nodes, origin):
        self.nodes = nodes
        self.origin = origin
        
    def get_length(self):
        return len(self.nodes)
        
    def calculate_depth(self):
        start_node = 0
        graph_length = len(self.nodes)
        level = [None] * graph_length
        marked = [False] * graph_length
        
        level[start_node] = 0
        marked[start_node] = True
        queue = [start_node]
        
        while len(queue) != 0:
            curr_node = queue.pop(0)
            curr_conn = self.nodes[curr_node].get_connection()
            
            for i in range(len(curr_conn)):
                b = curr_conn[i]
                
                if marked[b] == False:
                    queue.append(b)
                    level[b] = level[curr_node] + 1
                    marked[b] = True
                    
        level_text = ""
        for i, depth in enumerate(level):
            level_text = level_text + "space: {} => depth: {}\n".format(i, depth)
            
        return level_text
        
    def generate_polygon(self):
        size = 20
        segments = self.get_length()
        if segments < 3:
            segments = 3
        fillet = 0
        return gh.Polygon(rs.coerce3dpoint(self.origin), size, segments, fillet)[0]
        
    def visualization_nodes(self):
        nodes_points = gh.DeconstructBrep(self.generate_polygon())[2]
        if self.get_length() == 2:
            nodes_points = nodes_points[:2]
        return nodes_points 
        
    def visualization_circles(self):
        radius = 2
        nodes_points = self.visualization_nodes()
        return gh.Circle(nodes_points, radius)
        
    def visualization_connections(self):
        nodes_points = self.visualization_nodes()
        
        lines = []
        for i, node in enumerate(self.nodes):
            for c in node.get_connection():
                line = rs.AddLine(nodes_points[i], nodes_points[c])
                lines.append(line)
        return lines


if __name__ == "__main__":
    convert_data = Data(datas).preprocessing()
    node_list = []
    for i, conn in enumerate(convert_data):
        curr_node = Node(i)
        curr_node.connect_node(conn)
        node_list.append(curr_node)
        
    graph = Graph(node_list, origin)
    nodes = graph.visualization_nodes()
    circles = graph.visualization_circles()
    connections = graph.visualization_connections()
    depth = graph.calculate_depth()
