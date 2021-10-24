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
        
    def add_node(self, other_node):
        self.connection.extend(other_node)


if __name__ == "__main__":
    space_syntax = Data(datas).preprocessing()
    
    nodes = []
    for i, conn in enumerate(space_syntax):
        curr_node = Node(i)
        curr_node.add_node(conn)
        nodes.append(curr_node)