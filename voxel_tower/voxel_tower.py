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
        
    def __sub__(self, other_pt):
        x, y, z = self.get_coord()
        return
        
    def get_self_point(self):
        x, y, z = self.get_coord()
        self_pt = Point(x, y, z)
        return self_pt
        
    def get_coord(self):
        return self.x, self.y, self.z
        
    def get_vector(self, other_pt):
        self_pt = self.get_self_point()
        return other_pt - self_pt
        
    def generate_point(self):
        x, y, z = self.get_coord()
        return rg.Point3d(x, y, z)
        
        
class Rectangle:
    def __init__(self, pts):
        self.pts = pts
        
    def get_pts(self):
        return self.pts
        
    def generate_rectangle(self):
        return
        
if __name__ == "__main__":
    p0 = Point(0,0,0)
    p1 = Point(5,0,0)
    p2 = Point(5,5,0)
    p3 = Point(0,5,0)
    p4 = p0
    
    rec_pts = [p0, p1, p2, p3, p4]
    rec = []
    for pt in rec_pts:
        rec.append(pt.generate_point())
