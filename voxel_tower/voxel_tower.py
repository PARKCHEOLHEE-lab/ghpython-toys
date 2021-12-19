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
        
    def get_coord(self):
        return self.x, self.y, self.z
        
    def generate_point(self):
        return rg.Point3d(*self.get_coord())
        
        
        
class Rectangle:
    def __init__(self, plane, size):
        self.palne = plane
        self.size = size
        
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
