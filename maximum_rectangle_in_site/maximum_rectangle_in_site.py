import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


def bounding_box_site(curve):
    return rg.BoundingBox(curve.ToArray())
    
def bounding_box_edges(b_box):
    b_box_edges = b_box.GetEdges()
    unique_edges = [b_box_edges[0], b_box_edges[1]]
    length_of_edges = (unique_edges[0].Length, unique_edges[1].Length)
    return unique_edges, length_of_edges
    
def generate_rectangle(p1, density):
    p2 = rg.Point3d(p1.X+density, p1.Y, 0)
    p3 = rg.Point3d(p2.X, p2.Y+density, 0)
    p4 = rg.Point3d(p3.X-density, p3.Y, 0)
    rect = rg.Polyline([p1, p2, p3, p4, p1])
    next_og_pt = p2
    return rect, next_og_pt



if __name__ == "__main__":
    bounding_box = bounding_box_site(site)
    unique_edges, length_of_edges = bounding_box_edges(bounding_box)
    a = generate_rectangle(rg.Point3d(5,5,0), density)
    print(a)
    b = rg.Line.PointAt(unique_edges[0], 0)
    c = unique_edges
    d = generate_rectangle(b, density)