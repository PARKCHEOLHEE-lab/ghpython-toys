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
    def __init__(self, origin, width, height, frame_heights, frame_angle):
        self.floor_height = 4
        self.frame_heights = [0] + frame_heights
        self.frame_angle = frame_angle
        Rectangle.__init__(self, origin, width, height)
        
    def get_frame_heights(self):
        return self.frame_heights
        
    def get_floor_height(self):
        return self.floor_height
        
    def get_frame_angle(self):
        return self.frame_angle
        
    def frame_count(self):
        return len(self.frame_heights)
        
    def generate_frame(self):
        recs = []
        floor_height = self.get_floor_height()
        for i in range(self.frame_count()):
            z = self.get_frame_heights()[i]
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
        
    def get_frist_floor_length(self):
        first_floor_curve = self.rotate_frame()[0]
        first_floor_length = rs.CurveLength(first_floor_curve)
        
        return first_floor_length
        
    def lean_roof(self, frame):
        frame_points = rs.CurvePoints(frame[-1])
        
        target_points = [frame_points[0], frame_points[3], frame_points[4]]
        translation = [0,0,15]
        rs.MoveObjects(target_points, translation)
        roof_frame = rs.AddCurve(frame_points, degree=1)
        return roof_frame
        
    def generate_closed_facade(self):
        merged_facade = self.generate_facade()
        closed_facade = gh.CapHoles(merged_facade)
        
        return closed_facade
        
    def generate_bbox(self):
        closed_facade = self.generate_closed_facade()
        
        tower_bbox = gh.BoundingBox(closed_facade, rg.Plane.WorldXY).box
        tower_bbox_centroid = gh.Volume(tower_bbox).centroid
        
        return tower_bbox, tower_bbox_centroid
        
    def generate_core(self):
        before_rotate_frame = self.generate_frame()
        first_floor_frame = before_rotate_frame[0]
        
        coefficient = 0.3
        core_origin = gh.Area(rs.coercecurve(first_floor_frame)).centroid
        core_base = rs.AddLoftSrf(before_rotate_frame)
        
        core = gh.ScaleNU(rs.coercebrep(core_base), core_origin, coefficient, coefficient, 1.02).geometry
        core = gh.CapHoles(core)
        
        rs.MoveObject(core, [200, 0, 0])
        
        return core
        
    def generate_main_structure(self):
        main_structure_for_facade = []
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
                    
                    main_structure_for_facade.extend([polyline_1, polyline_2])
                    
                else:
                    points_1 = [curr_points[idx_1], next_points[idx_1], curr_points[idx_2]]
                    points_2 = [curr_points[idx_2], next_points[idx_1], next_points[idx_2]]
                    
                    polyline_1 = gh.PolyLine(points_1, True)
                    polyline_2 = gh.PolyLine(points_2, True)
                    
                    main_structure_for_facade.extend([polyline_1, polyline_2])
                    
        exploded_main_structure_for_facade = gh.Explode(main_structure_for_facade, True).segments
        main_structure = gh.Pipe(exploded_main_structure_for_facade, 0.25, 2)
        
        rs.MoveObjects(main_structure, [105, 0, 0])
                    
        return main_structure_for_facade, main_structure
        
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
            
        sub_structures = []
        structure_size = rg.Interval(-0.15, 0.15)
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
                curve_geom = rs.coercecurve(curve)
                
                sub_structure_start_pt = gh.EndPoints(curve_geom).start
                sub_structure_rec = gh.Rectangle(sub_structure_start_pt, structure_size, structure_size, 0).rectangle
                
                sub_structure = gh.Sweep1(curve_geom, sub_structure_rec, 1)
                sub_structure = gh.Move(sub_structure, rg.Point3d(105, 0, 0)).geometry
                
                if isinstance(sub_structure, list):
                    sub_structures.append(sub_structure[0])
                    sub_structures.append(sub_structure[1])
                
                sub_structures.append(sub_structure)
        
        return sub_structures
        
    def generate_facade(self):
        main_structure_for_facade, _ = self.generate_main_structure()
        
        facade = []
        for polyline in main_structure_for_facade:
            srf = gh.BoundarySurfaces(polyline)
            facade.append(srf)
            
        merged_facade = gh.BrepJoin(facade).breps
            
        return merged_facade
        
    def generate_double_skin(self):
        merged_facade = self.generate_facade()
        
        tower_bbox, tower_bbox_centroid = self.generate_bbox()
        first_floor_length = self.get_frist_floor_length()
        
        offset_dis = 2
        coefficient = (first_floor_length/4 + offset_dis) / (first_floor_length/4)
        
        double_skin = gh.ScaleNU(merged_facade, tower_bbox_centroid, coefficient, coefficient, 1.02).geometry
        
        return double_skin
        
    def generate_tower_cap(self):
        double_skin = self.generate_double_skin()
        closed_facade = gh.CapHoles(double_skin)
        bottom_cap = gh.DeconstructBrep(closed_facade).faces[0]
        upper_cap = gh.DeconstructBrep(closed_facade).faces[1]
        
        return bottom_cap, upper_cap


if __name__ == "__main__":
    ORIGIN = [200, 0, 0]
    SIZE = 32
    
    tower = Tower(ORIGIN, SIZE, SIZE, frame_heights, frame_angle)
    
    tower_facade = tower.generate_facade()
    tower_double_skin = tower.generate_double_skin()
    tower_cap = tower.generate_tower_cap()
    tower_core = tower.generate_core()
    
    _, main_structure = tower.generate_main_structure()
    sub_structure = tower.generate_sub_structure()

