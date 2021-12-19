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
        
    def __repr__(self):
        return "{}".format(self.get_coord())
        
    def __sub__(self, other_pt):
        x, y, z = self.get_coord()
        ox, oy, oz = other_pt.get_coord()
        return Point(x-ox, y-oy, z-oz)
        
    def get_self_point(self):
        x, y, z = self.get_coord()
        self_pt = Point(x, y, z)
        return self_pt
        
    def get_coord(self):
        return [self.x, self.y, self.z]
        
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
    
    
    rotated = []
    for pt in rec_pts:
        x,y,z = pt.get_coord()
        
        sin45 = math.sin(45)
        cos45 = math.cos(45)
        
        rx = cos45*x - sin45*y
        ry = sin45*x + cos45*y
        
        rp = Point(rx, ry, z).generate_point()
        rotated.append(rp)
        
        
#x' = cos(45°) * x - sin(45°) * y
#y' = sin(45°) * x + cos(45°) * y