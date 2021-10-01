import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


def bounding_box_site(curve):
    base_points = rs.BoundingBox(curve)
    bounding_box = rs.AddCurve(base_points, 1)
    return base_points, bounding_box

def bounding_box_size(base_points):
    bbox_width = rs.Distance(base_points[0], base_points[1])
    bbox_height = rs.Distance(base_points[1], base_points[2])
    return bbox_width, bbox_height

def generate_unit(origin, unit_width, unit_height):
    rectangle = rs.AddRectangle(origin, unit_width, unit_height)
    return rectangle

def generate_grid(origin_x, origin_y, grid_count, unit_width, unit_height):
    grid = []
    for i in range(grid_count):
        for j in range(1, grid_count+1):
            x = origin_x + unit_width*i
            y = origin_y - unit_height*j
            z = 0
            unit = generate_unit([x,y,z], unit_width, unit_height)
            grid.append(unit)
    return grid

def get_guid(object):
    translate = [0,0,0]
    return rs.MoveObject(object, translate)

def area_grid(unit):
    area = rs.Area(unit)
    return area

def centroid_grid(grid):
    centroid = []
    for unit in grid:
        centroid.append(rs.CurveAreaCentroid(unit)[0])
    return centroid

def inside_grid(grid, site):
    inside_grid = gh.RegionIntersection(grid, site)
    return inside_grid

#def evaluate_grid(grid, inside_grid):
#    n = int(len(grid)**0.5)
#    inside_units = []
#    inside_bools = [[0]*n for _ in range(n)]
#    for inside_polygon in inside_grid:
#        inside_polygon_area = area_grid(get_guid(inside_polygon))
#        if round(inside_polygon_area, 5) == round(area, 5):
#            inside_units.append(inside_polygon)
#    return inside_units, inside_bools

def evaluate_grid(grid, inside_grid):
    n = int(len(grid)**0.5)
    inside_units = []
#    inside_bools = [[0]*n for _ in range(n)]
    inside_bools = []
    for inside_polygon in inside_grid:
        inside_polygon_area = area_grid(get_guid(inside_polygon))
        if round(inside_polygon_area, 5) == round(area, 5):
            inside_units.append(inside_polygon)
            
    grid_centroid = centroid_grid(grid)
    units_centroid = centroid_grid(inside_units)
    
    for i, gp in enumerate(grid_centroid):
        row = []
        gp_x, gp_y = gp[0], gp[1]
        for up in units_centroid:
            up_x, up_y = up[0], up[1]
            if round(gp_x, 5) == round(up_x, 5) and round(gp_y, 5) == round(up_y, 5):
                print(True)
            
            
    return inside_units, inside_bools
            

if __name__ == "__main__":
    base_points, bounding_box = bounding_box_site(site)
    bbox_width, bbox_height = bounding_box_size(base_points)
    
    origin_x, origin_y = base_points[3][0], base_points[3][1]
    unit_width = bbox_width / grid_count
    unit_height = bbox_height / grid_count    
    grid = generate_grid(origin_x, origin_y, grid_count, unit_width, unit_height)
    area = area_grid(grid[0])
    convert_grid = [rs.coercecurve(u) for u in grid]
    inside_grid = inside_grid(convert_grid, site)
#    inside_units, inside_bools = evaluate_grid(grid, inside_grid)
#    grid_centroid = centroid_grid(grid)
#    units_centroid = centroid_grid(inside_units)
    
    a = evaluate_grid(grid, inside_grid)
