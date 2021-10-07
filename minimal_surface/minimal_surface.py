import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


def subtraction(a, b):
    return a-b

def multiplication(a, b):
    return a*b

def division(a, b):
    return a/b

def square_root(x):
    return math.sqrt(x)

def base_boundary(origin, size):
    x, y, z = origin[0], origin[1], origin[2]
    origin_point = gh.ConstructPoint(x, y, z)
    boundary_box = gh.DomainBox(origin_point, size, size, size)
    return boundary_box

def brep_elements(brep):
    _, edges, vertices = gh.DeconstructBrep(brep)
    return edges, vertices

def brep_centroid(brep):
    _, centroid = gh.Volume(brep)
    return centroid

def line_generate(pt1, pt2):
    return gh.Line(pt1, pt2)

def line_evaluate(line, place):
    return gh.EvaluateLength(line, place, True)[0]

def twopoint_midpoint(pt1, pt2):
    x = (pt1[0]+pt2[0]) * 0.5
    y = (pt1[1]+pt2[1]) * 0.5
    z = (pt1[2]+pt2[2]) * 0.5
    midpoint = gh.ConstructPoint(x,y,z)
    return midpoint

def plane_generate(pt1, pt2, pt3):
    return gh.Plane3Pt(pt1, pt2, pt3)

def plane_origin(plane, origin):
    return gh.PlaneOrigin(plane, origin)

def vector_twopoint(pt1, pt2):
    return pt2 - pt1

def arc_generate(pt1, pt2, vector):
    return gh.ArcSED(pt1, pt2, vector)[0]

def surface_generate(edge_1, edge_2, edge_3, edge_4):
    return gh.EdgeSurface(edge_1, edge_2, edge_3, edge_4)

def surface_mirror(surface, plane):
    return gh.Mirror(surface, plane)[0]


if __name__ == "__main__":
    # 1.  set parameter
    root_2 = square_root(2)
    root_3 = square_root(3)
    temp_1 = subtraction(1, slider)
    temp_2 = division(2, root_3)
    
    parameter_a = 0.5
    parameter_b = multiplication(root_2, temp_1)
    parameter_c = multiplication(slider, temp_2)
    parameter_d = subtraction(1, parameter_c)
    parameter_d = multiplication(parameter_d, root_3)
    parameter_d = subtraction(1, parameter_d)
    
    
    # 2. minimal surface base boundary
    base = base_boundary([-100,0,0], 50)
    
    
    # 3. base point & line for minimal surface generate
    base_edges, base_vertices = brep_elements(base)
    point_a = base_vertices[4]
    point_b = base_vertices[5]
    point_mid = twopoint_midpoint(base_vertices[1], base_vertices[4])
    point_inside = brep_centroid(base)
    
    line_1 = line_generate(point_a, point_mid)
    line_2 = line_generate(point_mid, point_inside)
    line_3 = line_generate(point_b, point_inside)
    line_4 = base_edges[4]
    print(line_1)
    lines = [line_1, line_2, line_3, line_4]
    params = [parameter_b, parameter_d, parameter_b, parameter_a]
    line_pts = []
    for i, param in enumerate(params):
        line_pt = line_evaluate(lines[i], param)
        line_pts.append(line_pt)
    
    line_1_pt, line_2_pt, line_3_pt, line_4_pt = line_pts
    
    
    # 4. minimal surface edges generate
    edge_1_vector = vector_twopoint(line_4_pt, point_mid)
    edge_2_vector = vector_twopoint(line_4_pt, point_inside)
    edge_3_vector = vector_twopoint(point_mid, point_b)
    edge_4_vector = vector_twopoint(point_mid, point_a)
    edge_1 = arc_generate(line_4_pt, line_1_pt, edge_1_vector)
    edge_2 = arc_generate(line_4_pt, line_3_pt, edge_2_vector)
    edge_3 = arc_generate(line_2_pt, line_3_pt, edge_3_vector)
    edge_4 = arc_generate(line_2_pt, line_1_pt, edge_4_vector)
    
    minimal_surface = surface_generate(edge_1, edge_2, edge_3, edge_4)