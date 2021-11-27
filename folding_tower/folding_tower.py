import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


class Rectangle:
    def __init__(self, origin, width, height):
        self.origin = origin
        self.width = width
        self.height = height
        
    def get_origin(self):
        return self.origin
        
    def get_width(self):
        return self.width
        
    def get_height(self):
        return self.height
        
    def generate_rectangle(self):
        return rs.AddRectangle(self.get_origin(), self.get_width(), self.get_height())
        
    def copy_rectangle(self, translation):
        original_rectangle = self.generate_rectangle()
        return rs.CopyObject(original_rectangle, translation)
        
    def rotate_rectangle(self, object, rotation_angle):
        centroid = rs.CurveAreaCentroid(object)[0]
        return rs.RotateObject(object, centroid, rotation_angle)


class Tower(Rectangle):
    def __init__(self, origin, width, height, vertical_heights, rotation_angle):
        self.floor_height = 4
        self.vertical_heights = vertical_heights
        self.rotation_angle = rotation_angle
        Rectangle.__init__(self, origin, width, height)
        
    def get_vertical_heights(self):
        return self.vertical_heights
        
    def get_floor_height(self):
        return self.floor_height
        
    def get_rotation_angle(self):
        return self.rotation_angle
        
    def frame_count(self):
        return len(self.vertical_heights)
        
    def generate_frame(self):
        recs = []
        floor_height = self.get_floor_height()
        for i in range(self.frame_count()):
            z = self.get_vertical_heights()[i]
            copied_rectangle = self.copy_rectangle([0, 0, z*floor_height])
            recs.append(copied_rectangle)
        return recs
        
    def rotate_frame(self):
        frame = self.generate_frame()
        rotation_angle = self.get_rotation_angle()
        
        for i in range(self.frame_count()):
            self.rotate_rectangle(frame[i], rotation_angle[i])
            
        roof_frame = self.lean_roof(frame)
        frame[-1] = roof_frame
        return frame
        
    def lean_roof(self, frame):
        frame_points = rs.CurvePoints(frame[-1])
        
        target_points = [frame_points[0], frame_points[3], frame_points[4]]
        translation = [0,0,15]
        rs.MoveObjects(target_points, translation)
        roof_frame = rs.AddCurve(frame_points, degree=1)
        return roof_frame
        
    def generate_surface(self):
        srfs = []
        
        return srfs


if __name__ == "__main__":
    VERTICAL_HEIGHTS = [0, 5, 16, 30, 40]
    ORIGIN = [200, 0, 0]
    SIZE = 32
    
    tower_obj = Tower(ORIGIN, SIZE, SIZE, VERTICAL_HEIGHTS, rotation_angle)
    tower = tower_obj.rotate_frame()
    
    a = []
    for i in range(len(tower)-1):
        curr_points = rs.CurvePoints(tower[i])[:-1]
        next_points = rs.CurvePoints(tower[i+1])[:-1]
        
        for j in range(len(curr_points)):
            idx_1 = j
            idx_2 = j+1
            if idx_2 == 4:
                idx_2 = 0
                
            if i % 2 == 0:
                points_1 = [curr_points[idx_1], next_points[idx_1], next_points[idx_2]]
                points_2 = [curr_points[idx_1], next_points[idx_2], curr_points[idx_2]]
                
                polyline_1 = gh.PolyLine(points_1, True)
                polyline_2 = gh.PolyLine(points_2, True)
                
                surface_1 = gh.BoundarySurfaces(polyline_1)
                surface_2 = gh.BoundarySurfaces(polyline_2)
                
                a.extend([surface_1, surface_2])
                
            else:
                points_1 = [curr_points[idx_1], next_points[idx_1], curr_points[idx_2]]
                points_2 = [curr_points[idx_2], next_points[idx_1], next_points[idx_2]]
                
                polyline_1 = gh.PolyLine(points_1, True)
                polyline_2 = gh.PolyLine(points_2, True)

                surface_1 = gh.BoundarySurfaces(polyline_1)
                surface_2 = gh.BoundarySurfaces(polyline_2)
                a.extend([surface_1, surface_2])
