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
        
    def point_in_polygon(self, boundary):
        if boundary[0].get_coord() != boundary[-1].get_coord():
            boundary.append(boundary[0])
        
        x, y, z = self.get_coord()
        
        pt = Point(x, y, z)
        ept = Point(10000, pt[1], z)
        ray = Line(pt, ept)
        
        count = 0
        for i in range(len(boundary)-1):
                p1 = boundary[i]
                p2 = boundary[i+1]
                boundary_line = Line(p1, p2)
                
                ray_intsc_pt = ray.intersect_point(boundary_line) 
                if ray_intsc_pt is not None:
                    count += 1
                    
        if count % 2 == 0:
            return False

        return True
        
    def generate_point(self):
        x, y, z = self.get_coord()
        return rg.Point3d(x, y, z)


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    def generate_line(self):
        return rg.Line(self.p1, self.p2)
        
    def get_p1_coord(self):
        return self.p1[0], self.p1[1]
        
    def get_p2_coord(self):
        return self.p2[0], self.p2[1]
        
    def intersect_point(self, line2):
        # 두 선분의 교점을 찾는 함수
        p1 = self.get_p1_coord()
        p2 = self.get_p2_coord()
        p3 = line2.get_p1_coord()
        p4 = line2.get_p2_coord()
        
        # 선분1 => (x1,y1) to (x2, y2); 선분2 => (x3,y3) to (x4, y4)
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        z = 0
        
        # 완전히 교차하는 경우에만 점을 생성 
        # ex) 선분AB의 정점이 선분CD의 사이에 있으면 교차하지 않는 것으로 판단
        denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
        
        # 선분이 평행하지 않은 경우
        if denom != 0:
            ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
            ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
            if (0 < ua < 1) and (0 < ub < 1): # 교차여부 확인
                ix = x1 + ua * (x2-x1)
                iy = y1 + ua * (y2-y1)
                
                intersect_point = Point(ix, iy, z)
                return intersect_point
                
        # 선분이 평행한 경우
        elif denom == 0:
            ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3))
            ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3))
            if (0 < ua < 1) and (0 < ub < 1): # 교차여부 확인
                ix = x1 + ua * (x2-x1)
                iy = y1 + ua * (y2-y1)
                
                intersect_point = Point(ix, iy, z)
                return intersect_point

class Polyline:
    def __init__(self, pts):
        self.pts = pts
        
    def __len__(self):
        polyline_pts = self.get_polyline_pts()
        return len(polyline_pts)
        
    def __getitem__(self, i):
        polyline_pts = self.get_polyline_pts()
        return polyline_pts[i]
        
    def __repr__(self):
        return "{}".format(self.get_polyline_pts())
        
    def get_polyline_pts(self):
        return self.pts
        
    def generate_polyline(self):
        polyline_pts = self.get_polyline_pts()
        converted_pts = [pt.generate_point() for pt in polyline_pts]
        
        return rg.PolylineCurve(converted_pts)


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
        
    def rotate_rectangle(self, origin):
        rectangle_pts = self.get_rectangle_pts()
        
        degree = 45
        sin45 = math.sin(math.radians(degree))
        cos45 = math.cos(math.radians(degree))
        
        rotated_rectangle_pts = []
        for pt in rectangle_pts:
            x, y, z = pt.get_coord()
            
            origin_x, origin_y, _ = origin.get_coord()

            rx = origin_x + (cos45*(x-origin_x) - sin45*(y-origin_y))
            ry = origin_y + (sin45*(x-origin_x) + cos45*(y-origin_y))
            
            rp = Point(rx, ry, z)
            rotated_rectangle_pts.append(rp)
            
        return Polyline(rotated_rectangle_pts)
        
    def generate_rectangle(self, rectangle):
        rectangle_pts = rectangle.get_rectangle_pts()
        converted_pts = [pt.generate_point() for pt in rectangle_pts]
        
        return Polyline(converted_pts).generate_polyline()


class Pattern(Rectangle):
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
        
    def get_scaled_bbox_cpt(self):
        _, height = self.get_scaled_bbox_size()
        scaled_bbox = self.get_scaled_bbox()
        
        O = 0
        anchor = scaled_bbox[0]*0.5 + scaled_bbox[3]*0.5
        vector = Point(O, height/2, O)
        
        center_point = anchor + vector
        x, y, z = center_point
        return Point(x, y, z)
        
    def generate_pattern(self):
        origin = self.get_pattern_origin()
        
        size = self.get_size()
        width, height = self.get_scaled_bbox_size()
        
        height_count = int(height / size) * 2
        width_count = int(width / size)
        O = 0
        
        base_pattern = []
        all_patterns = []
        
        for i in range(height_count):
            curr_origin = origin
            
            if i == 0:
                copied_rec = Rectangle(curr_origin, size)
                base_pattern.append(copied_rec)
                
                all_patterns.append(copied_rec)
                origin = base_pattern[-1][2]*0.5 + base_pattern[-1][3]*0.5
            
            elif i % 2 != 0:
                copied_rec = Rectangle(curr_origin, size)
                base_pattern.append(copied_rec)
                
                all_patterns.append(copied_rec)
                origin = base_pattern[-2][1]
                
            else:
                copied_rec = Rectangle(curr_origin, size)
                base_pattern.append(copied_rec)
                
                all_patterns.append(copied_rec)
                origin = base_pattern[-1][2]*0.5 + base_pattern[-1][3]*0.5
                
            for j in range(2, width_count, 2):
                vector = Point(size*j, O, O)
                copied_pattern = copied_rec + vector
                
                all_patterns.append(copied_pattern)
                
        return all_patterns
        
    def rotate_pattern(self):
        rotate_origin = self.get_scaled_bbox_cpt()
        all_patterns = self.generate_pattern()
        
        rotate_patterns = []
        for pattern in all_patterns:
            rotate_pattern_pts = pattern.rotate_rectangle(rotate_origin)
            rotate_pattern_polyline = Polyline(rotate_pattern_pts)
            
            rotate_patterns.append(rotate_pattern_polyline)
        
        return rotate_patterns
        
    def cull_pattern(self):
        rotate_patterns = self.rotate_pattern()
        boundary = self.get_boundary_pts()
        
        inside_pattern = []
        for pattern in rotate_patterns:
            count = 0
            
            for pt in pattern[:-1]:
                check = pt.point_in_polygon(boundary)
                
                if check == False:
                    count += 1
                if count > 1:
                    break
            
            if count < 2:
                inside_pattern.append(pattern.generate_polyline())
        
        return inside_pattern


if __name__ == "__main__":
    pass
#    pattern_size = 3
#    base_rec_pts = Pattern(boundary_points, pattern_size)  
#    pattern = base_rec_pts.cull_pattern()