import math
import random
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
        
#    def point_in_region(self, point):
#        return gh.PointInCurve(point
        
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
    
    crane_positions = [crane_position_1, crane_position_2]
    crane_radius = [crane_radius_1, crane_radius_2]
    crane_spec = {30:25, 40:30, 50:40, 60:60, 70:65}
    
    crane_origins = []
    crane_towers = []
    crane_site_intscs = []
    visualization_elements = []
    for i, position in enumerate(crane_positions):
        crane_height = crane_spec[crane_radius[i]]
        crane_origin = site_object.evaluate_surface(position)
        crane_tower = Circle(crane_origin, crane_radius[i]).generate_circle()
        crane_site_intsc = Region([crane_tower, site]).intersection_region()
        
        crane_origin_vis = rs.CopyObject(crane_origin, [0,0,crane_height])
        crane_tower_vis = rs.CopyObject(crane_tower, [0,0,crane_height])
        
        crane_origins.append(crane_origin)
        crane_towers.append(crane_tower)
        crane_site_intscs.append(crane_site_intsc)
        visualization_elements.extend([crane_origin_vis, crane_tower_vis])
    
    crane_site_union = Region(crane_site_intscs).union
    crane_site_union_area = Region(crane_site_intscs).union_area
    empty_site_area = site_area - crane_site_union_area
    
    evaluate_score = []
    for crane in crane_towers:
        housing_area_intsc_crane = Region([crane, housing_area]).intsc_area
#        green_area_intsc_crane = -Region([crane, green_area]).intsc_area
        diff_area_site_crane = Region([crane_towers[0], site]).diff_area
        
#        evaluate_score.extend([housing_area_intsc_crane, green_area_intsc_crane, diff_area_site_crane])
        evaluate_score.extend([housing_area_intsc_crane, diff_area_site_crane])
        
    evaluate_score = sum(evaluate_score)
    
    print(gh.PointInCurve(crane_origins[0], site)[0])