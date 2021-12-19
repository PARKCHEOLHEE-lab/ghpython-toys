﻿import Rhino.Geometry as rg
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
        
    def get_points(self, frame):
        return rs.CurvePoints(frame)
        
    def generate_rectangle(self):
        return rs.AddRectangle(self.get_origin(), self.get_width(), self.get_height())
        
    def copy_rectangle(self, translation):
        original_rectangle = self.generate_rectangle()
        return rs.CopyObject(original_rectangle, translation)
        
    def rotate_rectangle(self, object, frame_angle):
        origin = rs.CurveAreaCentroid(object)[0]
#        origin = self.get_points(object)[0]
        return rs.RotateObject(object, origin, frame_angle)


class Tower(Rectangle):
    def __init__(self, origin, width, height, vertical_heights, frame_angle):
        self.floor_height = 4
        self.vertical_heights = vertical_heights
        self.frame_angle = frame_angle
        Rectangle.__init__(self, origin, width, height)
        
    def get_vertical_heights(self):
        return self.vertical_heights
        
    def get_floor_height(self):
        return self.floor_height
        
    def get_frame_angle(self):
        return self.frame_angle
        
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
        frame_angle = self.get_frame_angle()
        
        for i in range(self.frame_count()):
            self.rotate_rectangle(frame[i], frame_angle[i])
            
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
        
    def generate_core(self):
        core_size = -10
        base_curve = self.rotate_frame()[0]
        core_curve = rs.OffsetCurve(base_curve, [0,0,0], core_size)
        
        core_z = 160
        core_path = rs.AddLine(rs.AddPoint(0,0,0), rs.AddPoint(0,0,core_z))
        core = rs.ExtrudeCurve(core_curve, core_path)
        return core
        
    def generate_main_structure(self):
        main_structure = []
        frame = self.rotate_frame()
        for i in range(len(frame)-1):
            curr_points = self.get_points(frame[i])[:-1]
            next_points = self.get_points(frame[i+1])[:-1]
            
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
                    
                    main_structure.extend([polyline_1, polyline_2])
                    
                else:
                    points_1 = [curr_points[idx_1], next_points[idx_1], curr_points[idx_2]]
                    points_2 = [curr_points[idx_2], next_points[idx_1], next_points[idx_2]]
                    
                    polyline_1 = gh.PolyLine(points_1, True)
                    polyline_2 = gh.PolyLine(points_2, True)
                    
                    main_structure.extend([polyline_1, polyline_2])
                    
        return main_structure
        
    def generate_sub_structure(self):
        tower_frame = self.rotate_frame()
        diagonal_columns = []
        
        for i in range(len(tower_frame)-1):
            curr_points = self.get_points(tower_frame[i])[:-1]
            next_points = self.get_points(tower_frame[i+1])[:-1]
            
            for j in range(len(curr_points)):
                idx_1 = j
                idx_2 = j+1
                if idx_2 == 4:
                    idx_2 = 0
                
                if i % 2 == 0:
                    start_point = curr_points[idx_1]
                    end_point = next_points[idx_2]
                    diagonal = rs.AddLine(start_point, end_point)
                    diagonal_columns.append(diagonal)
                    
                else:
                    start_point = next_points[idx_1]
                    end_point = curr_points[idx_2]
                    diagonal = rs.AddLine(start_point, end_point)
                    diagonal_columns.append(diagonal)
                    
        segment = 5
        frame_points = []
        for frame in tower_frame:
            temp_list = []
            exploded_frame = rs.ExplodeCurves(frame)
            
            for curve in exploded_frame:
                divide_points = rs.DivideCurve(curve, segment)
                temp_list.append(divide_points)
                
            frame_points.append(temp_list)
            
        preprocess = []
        for column in diagonal_columns:
            divide_points = rs.DivideCurve(column, segment)
            preprocess.append(divide_points)
        
        side_count = 4
        column_points = []
        for i in range(0, len(preprocess), side_count):
            column_points.append(preprocess[i:i+side_count])
            
        sub_structure = []
        for i in range(4):
            for j in range(1,5):
                temp = []
                for k in range(len(tower_frame)):
                    if k == 4:
                        last_point = frame_points[k][i][j]
                        temp.append(last_point)
                    else:
                        point_1 = frame_points[k][i][j]
                        point_2 = column_points[k][i][j]
                    
                        temp.extend([point_1, point_2])
                
                curve = rs.AddCurve(temp, 1)
                sub_structure.append(curve)
            
                    
        return sub_structure
        
    def generate_facade(self):
        srfs = []
        main_structure = self.generate_main_structure()
        for polyline in main_structure:
            srf = gh.BoundarySurfaces(polyline)
            srfs.append(srf)
        
#        facade = 
        
        return gh.BrepJoin(srfs)[0]


if __name__ == "__main__":
    VERTICAL_HEIGHTS = [0, 5, 16, 30, 40]
    ORIGIN = [200, 0, 0]
    SIZE = 32
    
    tower_obj = Tower(ORIGIN, SIZE, SIZE, VERTICAL_HEIGHTS, frame_angle)
    
    tower_facade = tower_obj.generate_facade()
    main_structure = tower_obj.generate_main_structure()
    sub_structure = tower_obj.generate_sub_structure()
    
    
    a = tower_obj.generate_core()