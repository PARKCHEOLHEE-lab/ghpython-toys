import math
import random
import Rhino.Geometry as rg
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
        
        
class Test:
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
        
        
class Rectangle:
    def __init__(self, origin, size):
        self.origin = origin
        self.size = size
        
    def get_origin(self):
        return self.origin
        
    def get_size(self):
        return self.size
        
    def get_rectangle_pts(self):
        origin = self.get_origin()
        size = self.get_size()
        O = 0
        
        p0 = origin
        p1 = origin + Point(O, size, O)
        p2 = origin + Point(size, size, O)
        p3 = origin + Point(size, O, O)
        p4 = p0
        
        return [p0, p1, p2, p3, p4]
        
    def generate_rectangle(self):
        rectangle_pts = self.get_rectangle_pts()
        converted_pts = [pt.generate_point() for pt in rectangle_pts]
        
        return rg.PolylineCurve(converted_pts)


class Zigzag(Rectangle):
    def __init__(self, bbox, size):
        self.bbox = bbox
#        self.origin = 
        Rectangle.__init__(self, bbox[0], size)
        
    def pattern_start_origin(self):
        return
        
    def generate_pattern(self):
        rectangle_pts = self.get_rectangle_pts()
        
        count = 0
        while count < 10:
            
            curr_pts = rectangle_pts
            temp_pts = []
            for i in range(len(rectangle_pts)-1):
                anchor = rectangle_pts[1]
                vector = rectangle_pts[i] - rectangle_pts[0]
                
                copied_pt = anchor + vector
                temp_pts.append(copied_pt)
            
            count += 1
        
        
        return


if __name__ == "__main__":
#    p0 = Point(0,0,0)
#    p1 = Point(5,0,0)
#    p2 = Point(5,5,0)
#    p3 = Point(0,5,0)
#    p4 = p0
#    
#    rectangle_pts = [p0, p1, p2, p3, p4]
#    rectangle = Rectangle(rectangle_pts)
#    
#    rotated_rec = rectangle.generate_rectangle()
#    rotated_pts = rectangle.generate_rotate_pts()
#    
#    zgzg_rec_pts = []
#    for i in range(len(rotated_pts)-1):
#        anchor = rotated_pts[2]*0.5 + rotated_pts[1]*0.5
#        vector = rotated_pts[i] - rotated_pts[0]
#        
#        zgzg_rec_pt = vector + anchor
#        zgzg_rec_pts.append(zgzg_rec_pt)
#    
#    rotated_pts = [pt.generate_point() for pt in rotated_pts]
#    test = [rotated_rec]
#    
#    
#    count = 0
#    all_pts = [rotated_pts]
#    while count < 10:
#        curr_pts = rotated_pts
#        temp_pts = []
#        for i in range(len(curr_pts)-1):
#            anchor = rotated_pts[2]*0.5 + rotated_pts[1]*0.5
#            vector = rotated_pts[i] - rotated_pts[0]
#        
#            zgzg_rec_pt = vector + anchor
#            temp_pts.append(zgzg_rec_pt)
#            
#        temp_pts.append(temp_pts[0])
#        zgzg_rec_polyline = rg.PolylineCurve(temp_pts)
#        test.append(zgzg_rec_polyline)
#        all_pts.append(temp_pts)
#        
#        rotated_pts = temp_pts
#        
#        count += 1
    
    
    ############## Scaled Bounding Box ##############
    if boundary_points[0] != boundary_points[-1]:
        boundary_points.append(boundary_points[0])
        
    converted_boundary_points = []
    for bp in boundary_points:
        x, y, z = bp
        converted_bp = Point(x, y, z)
        converted_boundary_points.append(converted_bp)
        
    zip_bpts = zip(*converted_boundary_points)
    
    min_x, min_y = min(zip_bpts[0]), min(zip_bpts[1])
    max_x, max_y = max(zip_bpts[0]), max(zip_bpts[1])
    z = 0
    
    s = 30
    
    p0 = Point(min_x, min_y, z) + Point(-s, -s, z)
    p1 = Point(min_x, max_y, z) + Point(-s, +s, z)
    p2 = Point(max_x, max_y, z) + Point(+s, +s, z)
    p3 = Point(max_x, min_y, z) + Point(+s, -s, z)
    p4 = p0
    
    d = [p0, p1, p2, p3, p4]
    
    
    ############## Generate Pattern ##############
    base_rec = Zigzag(d, 3)
    
    base_rec.generate_pattern()
    
    
    
