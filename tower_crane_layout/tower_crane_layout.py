﻿import math
import random
from itertools import combinations
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh

class Point:
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.coord = self.coordinate_point()
        self.point = self.generate_point()
        
    def coordinate_point(self):
        return self.x, self.y, self.z
        
    def generate_point(self):
        return rs.AddPoint(self.coord[0], self.coord[1], self.coord[2])


class Circle(Point):
    def __init__(self, position, radius):
        Point.__init__(self, position)
        self.radius = radius
        
    def generate_circle(self):
        return rs.AddCircle(self.point, self.radius)


class Region:
    def __init__(self, crvs):
        self.plane = rg.Plane.WorldXY
        self.curves = self.evaluate_type(crvs)
        self.union = self.union_region()
        self.intsc = self.intersection_region()
        self.diff = self.difference_region()
        self.union_area = self.area_region(self.union)
        self.intsc_area = self.area_region(self.intsc)
        self.diff_area = self.area_region(self.diff)
        
    def evaluate_type(self, crvs):
        curves = []
        for crv in crvs:
            if type(crv) == type(rs.AddPoint(0,0,0)):
                curves.append(rs.coercecurve(crv))
            else:
                curves.append(crv)
        return curves
        
    def union_region(self):
        return gh.RegionUnion(self.curves)
        
    def intersection_region(self):
        return gh.RegionIntersection(self.curves[0], self.curves[1])
        
    def difference_region(self):
        return gh.RegionDifference(self.curves[0], self.curves[1])
        
    def origin_in_region(self):
        origin = rs.CurveAreaCentroid(self.curves[0])[0]
        return gh.PointInCurve(origin, self.curves[1])[0]
        
    def area_region(self, region):
        area = gh.Area(region)[0]
        if type(area) == list:
            if area.count(None) == 2:
                return 0
            elif area.count(None) == 1:
                area[area.index(None)] = 0
                return sum(area)
            else:
                return sum(area)
        else:
            if area == None:
                return 0
            return area


class Surface:
    def __init__(self, polyline):
        self.polyline = self.evaluate_type(polyline)
        self.surface = self.generate_surface()
            
    def generate_surface(self):
        return rs.AddPlanarSrf(self.polyline)[0]
        
    def evaluate_surface(self, position):
        srf_parameter = rs.SurfaceParameter(self.surface, position)
        crane_origin = rs.EvaluateSurface(self.surface, srf_parameter[0], srf_parameter[1])
        return crane_origin
        
    def evaluate_type(self, surface):
        if type(surface) != type(rs.AddPoint(0,0,0)):
            return rs.MoveObject(surface, [0,0,0])
        else:
            return surface        
            
    def area_surface(self):
        return rs.SurfaceArea(self.surface)[0]



if __name__ == "__main__":
    site_object = Surface(site)
    site_surface = site_object.generate_surface()
    site_area = site_object.area_surface()
    
    crane_positions = [crane_position_1, crane_position_2, crane_position_3]
    crane_radius = [crane_radius_1, crane_radius_2, crane_radius_3]
    
    crane_origins = []
    crane_towers = []
    crane_site_intscs = []
    for i, position in enumerate(crane_positions):
        crane_origin = site_object.evaluate_surface(position)
        crane_tower = Circle(crane_origin, crane_radius[i]).generate_circle()
        crane_site_intsc = Region([crane_tower, site]).intersection_region()
        
        crane_origins.append(crane_origin)
        crane_towers.append(crane_tower)
        crane_site_intscs.append(crane_site_intsc)
    
    crane_site_union = Region(crane_site_intscs).union
    crane_site_union_area = Region(crane_site_intscs).union_area
    empty_site_area = site_area - crane_site_union_area
    
    exception_score = 500000
    crane_housing_intsc_area =  Region([Region(crane_towers).union, housing_area]).intsc_area
    threshold = 200
    if crane_housing_intsc_area >= threshold:
        empty_site_area = exception_score
        
    for crane in crane_towers:
        origin_check = Region([crane, site]).origin_in_region()
        if origin_check == 0 or origin_check == 1:
            empty_site_area = exception_score
    
    total_crane_crane_intsc_area = 0
    for crane_combi in combinations(crane_towers, 2):
        crane_crane_intsc_area = Region(crane_combi).intsc_area
        total_crane_crane_intsc_area = total_crane_crane_intsc_area + crane_crane_intsc_area
    if total_crane_crane_intsc_area >= 1000:
        empty_site_area = exception_score
            
    
    current_condition = "Current Condition ▼\nSite Area: {}\nSite Empty Area: {}\nHousing Intersection Area: {}\nCrane Intersection Area: {}"\
                        .format(site_area, empty_site_area, crane_housing_intsc_area, total_crane_crane_intsc_area)