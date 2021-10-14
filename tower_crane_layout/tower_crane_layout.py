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

    crane_origin_1 = site_object.evaluate_surface(crane_position_1)
    crane_origin_2 = site_object.evaluate_surface(crane_position_2)
    
    crane_tower_1 = Circle(crane_origin_1, crane_size_1).generate_circle()
    crane_tower_2 = Circle(crane_origin_2, crane_size_2).generate_circle()