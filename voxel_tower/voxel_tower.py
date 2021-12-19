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
        
    def __getitem__(self, i):
        return self.get_coord()[i]
        
    def __repr__(self):
        return "{}".format(self.get_coord())
        
    def __add__(self, other_pt):
        x, y, z = self.get_coord()
        ox, oy, oz = other_pt.get_coord()
        return Point(x+ox, y+oy, z+oz)
        
    def __sub__(self, other_pt):
        x, y, z = self.get_coord()
        ox, oy, oz = other_pt.get_coord()
        return Point(x-ox, y-oy, z-oz)
        
    def __mul__(self, n):
        x,y,z = self.get_coord()
        return Point(x*n, y*n, z*n)
        
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
        
    def get_center_point(self):
        rec_pts = self.get_pts()
        zip_pts = zip(*rec_pts)
        
        min_x, min_y = min(zip_pts[0]), min(zip_pts[1])
        max_x, max_y = max(zip_pts[0]), max(zip_pts[1])
       
        x = max_x*0.5 + min_x*0.5
        y = max_y*0.5 + min_y*0.5
        z = 0
        
        return Point(x,y,z)
        
    def generate_rotate_pts(self):
        rec_pts = self.get_pts()
        degree = 45
        
        rotated_rec_pts = []
        for pt in rec_pts:
            x, y, z = pt.get_coord()
            
            sin45 = math.sin(math.radians(degree))
            cos45 = math.cos(math.radians(degree))
            
            cx, cy, _ = self.get_center_point()
            
            rx = cx + (cos45*(x-cx) - sin45*(y-cy))
            ry = cy + (sin45*(x-cx) + cos45*(y-cy))
            
            rp = Point(rx, ry, z)
            rotated_rec_pts.append(rp)
        
        return rotated_rec_pts
        
    def generate_rectangle(self):
        rotated_rec_pts = self.generate_rotate_pts()
        converted_rec_pts = [pt.generate_point() for pt in rotated_rec_pts]
        
        return rg.PolylineCurve(converted_rec_pts)
        
if __name__ == "__main__":
    p0 = Point(0,0,0)
    p1 = Point(5,0,0)
    p2 = Point(5,5,0)
    p3 = Point(0,5,0)
    p4 = p0
    
    rectangle_pts = [p0, p1, p2, p3, p4]
    rectangle = Rectangle(rectangle_pts)
    
    rotated_rec = rectangle.generate_rectangle()
    a = rectangle.generate_rotate_pts()
