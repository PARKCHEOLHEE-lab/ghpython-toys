import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.coordinate = self.get_coordinate()
        
    def get_coordinate(self):
        return [self.x, self.y, self.z]
        
    def generate_point(self):
        x, y, z = self.coordinate
        return rs.AddPoint(x,y,z)
        
        
class Curve:
    def __init__(self, points):
        self.points = points
        self.DEGREE = 1
        
    def generate_curve(self):
        return rs.AddCurve(self.points, self.DEGREE)
        
        
class Auditorium:
    def __init__(self):
        self.pts = []
        
    def base_points(self):
        pt1 = Point(100,0,0).generate_point()
        return pt1
    
if __name__ == "__main__":
    a = Auditorium().base_points()
    print(a)