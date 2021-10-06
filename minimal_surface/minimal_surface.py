import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


def square_root(x):
    return math.sqrt(x)

def subtraction(a, b):
    return a-b

def multiplication(a, b):
    return a*b

def division(a, b):
    return a/b

def base_boundary(origin, size):
    x_pt = origin[0]
    y_pt = origin[1]
    z_pt = origin[2]
    origin_point = gh.ConstructPoint(x_pt, y_pt, z_pt)
    boundary_box = gh.DomainBox(origin_point, size, size, size)
    return boundary_box

def brep_elements(brep):
    faces, edges, vertices = gh.DeconstructBrep(brep)
    return edges, vertices

def brep_centroid(brep):
    volume, centroid = gh.Volume(brep)
    return centroid

def line_generate(pt1, pt2):
    return gh.Line(pt1, pt2)

def line_evaluate(line, place):
    return gh.EvaluateLength(line, place, True)

def twopoint_midpoint(pt1, pt2):
    x = (pt1[0]+pt2[0]) * 0.5
    y = (pt1[1]+pt2[1]) * 0.5
    z = (pt1[2]+pt2[2]) * 0.5
    midpoint = gh.ConstructPoint(x,y,z)
    return midpoint

def plane_generate(pt1, pt2, pt3):
    return gh.Plane3Pt(pt1, pt2, pt3)



if __name__ == "__main__":
    
    # 1.  set parameter
    root_2 = square_root(2)
    root_3 = square_root(3)
    temp_1 = subtraction(1, slider)
    temp_2 = division(2, root_3)
    
    parameter_a = slider
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
    line_1_pt = line_evaluate(line_1, parameter_b)
    line_2_pt = line_evaluate(line_2, parameter_d)
    line_3_pt = line_evaluate(line_3, parameter_b)
    line_4_pt = line_evaluate(line_4, parameter_a)
    
    # 4. minimal surface edges generate
    
    print(parameter_a, parameter_b, parameter_c, parameter_d)
