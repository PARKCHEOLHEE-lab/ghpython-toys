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
        
    def distance_to(self, other_pt):
        x, y, _ = self.get_coord()
        ox, oy, _ = other_pt.get_coord()
        
        distance = ((ox-x)**2 + (oy-y)**2) ** 0.5
        
        return distance
        
    def generate_point(self):
        x, y, z = self.get_coord()
        return rg.Point3d(x, y, z)
        
        
class Rectangle:
    def __init__(self, origin, size):
        self.origin = origin
        self.size = size
        
    def __getitem__(self, i):
        rectangle_pts = self.get_rectangle_pts()
        return rectangle_pts[i]
        
    def __repr__(self):
        return "{}".format(self.get_rectangle_pts())
        
    def __add__(self, vector):
        origin = self.get_origin()
        size = self.get_size()
        
        added_rectangle = Rectangle(origin+vector, size)
        
        return added_rectangle
        
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
    def __init__(self, boundary, size):
        self.boundary = boundary
        
        origin = self.get_pattern_origin()
        Rectangle.__init__(self, origin, size)
        
    def get_boundary_pts(self):
        boundary_points = self.boundary
        
        converted_boundary_points = []
        for bp in boundary_points:
            x, y, z = bp
            converted_bp = Point(x, y, z)
            converted_boundary_points.append(converted_bp)
        
        return converted_boundary_points
        
    def get_size(self):
        return self.size
        
    def get_pattern_origin(self):
        scaled_bbox = self.get_scaled_bbox()
        origin = scaled_bbox[0]
        return origin
        
    def get_scaled_bbox(self):
        boundary_pts = self.get_boundary_pts()
        zip_boundary_pts = zip(*boundary_pts)
    
        min_x, min_y = min(zip_boundary_pts[0]), min(zip_boundary_pts[1])
        max_x, max_y = max(zip_boundary_pts[0]), max(zip_boundary_pts[1])
        z = 0
        
        s = 30
        p0 = Point(min_x, min_y, z) + Point(-s, -s, z)
        p1 = Point(min_x, max_y, z) + Point(-s, +s, z)
        p2 = Point(max_x, max_y, z) + Point(+s, +s, z)
        p3 = Point(max_x, min_y, z) + Point(+s, -s, z)
        p4 = p0
        
        scaled_bbox = [p0, p1, p2, p3, p4]
        return scaled_bbox
        
    def get_scaled_bbox_size(self):
        scaled_bbox = self.get_scaled_bbox()
        width = scaled_bbox[0].distance_to(scaled_bbox[3])
        height = scaled_bbox[0].distance_to(scaled_bbox[1])
        
        return width, height
        
    def generate_pattern(self):
        origin = self.get_pattern_origin()
        base_rec_pts = self.get_rectangle_pts()
        base_rec_polyline = self.generate_rectangle()
        
        size = self.get_size()
        width, height = self.get_scaled_bbox_size()
        
        height_count = int(height / size) * 2
        width_count = int(width / size)
        
        rec_polyline = []
        rec_pts = []
        
        for i in range(height_count):
            curr_origin = origin
            
            if i == 0:
                copied_rec = Rectangle(curr_origin, size)
                rec_polyline.append(copied_rec.generate_rectangle())
                rec_pts.append(copied_rec)
                
                origin = rec_pts[-1][2]*0.5 + rec_pts[-1][3]*0.5
            
            elif i % 2 != 0:
                copied_rec = Rectangle(curr_origin, size)
                rec_polyline.append(copied_rec.generate_rectangle())                
                rec_pts.append(copied_rec)
                
                origin = rec_pts[-2][1]
                
            else:
                copied_rec = Rectangle(curr_origin, size)
                rec_polyline.append(copied_rec.generate_rectangle())                
                rec_pts.append(copied_rec)
                
                origin = rec_pts[-1][2]*0.5 + rec_pts[-1][3]*0.5
                
            
            for j in range(2, width_count, 2):
                vector = Point(size*j, 0, 0)
                rec_polyline.append((copied_rec + vector).generate_rectangle())
            
        return rec_polyline

if __name__ == "__main__":
    
    ############## Generate Pattern ##############
    pattern_size = 3
    base_rec_pts = Zigzag(boundary_points, pattern_size)    
    
    pattern = base_rec_pts.generate_pattern()