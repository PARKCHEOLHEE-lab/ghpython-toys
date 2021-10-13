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
        self.coordinate = self.get_coordinate()
        
    def get_coordinate(self):
        return [self.x, self.y, self.z]
        
    def generate_point(self):
        x, y, z = self.coordinate
        point = rs.AddPoint(x,y,z)
        return rs.PointCoordinates(point)
        
        
class Curve:
    def __init__(self, points):
        self.DEGREE = 1
        self.DISTANCE = 5
        self.DIRECTION = [0, 0, 0]
        self.points = points
        self.curve = self.generate_curve()
        
    def generate_curve(self):
        return rs.AddCurve(self.points, self.DEGREE)
        
    def offset_curve(self):
        return rs.OffsetCurve(self.curve, self.DIRECTION, self.DISTANCE)[0]
        
        
class Surface:
    def __init__(self, crvs):
        self.crvs = crvs
        self.srf = self.generate_surface()
        
    def generate_surface(self):
        return rs.AddPlanarSrf(self.crvs)
        
    def extrude_surface(self, direction):
        return rs.ExtrudeSurface(self.srf, direction)
        
        
class Auditorium:
    def __init__(self, step_height, step_width, cutter_pts):
        self.SCALE = 100
        self.START_X = 110
        self.END_X = 270
        self.STEP_COUNT = 10
        self.STEP_X = 160
        self.STEP_Y = 0
        self.CHAIR_Y = 5
        self.CEIL_Z = 65
        self.CHAIRS = 11
        self.SIGHT_LEVEL = 11.5
        self.SECTION_M = [200, 0, 0]
        self.DIRECTION_A = self.auditorium_direction()
        self.DIRECTION_C = self.chair_direction()
        
        self.step_width = step_width
        self.step_height = step_height
        self.cutter_pts = cutter_pts
        self.base_pts = self.base_points()
        self.base_crvs = self.base_curves()
        self.auditorium = self.generate_auditorium()
        self.chairs = []
        
    def base_points(self):
        base_pts = [Point(self.START_X,0,0).generate_point()]
        mul_list = []
        for i in range(self.STEP_COUNT+1):
            mul_list.extend([i, i])
            
        for i in zip(mul_list[:-1], mul_list[1:]):
            point = Point(self.STEP_X + self.step_width * i[0],
                          self.STEP_Y,
                          self.step_height * i[1])
            base_pts.append(point.generate_point())
        base_pts[-1][0] = self.END_X
        
        ceil_pt_1 = Point(self.END_X, self.STEP_Y, self.CEIL_Z)
        ceil_pt_2 = Point(self.START_X, self.STEP_Y, self.CEIL_Z)
        base_pts.extend([ceil_pt_1.generate_point(),
                         ceil_pt_2.generate_point(),
                         base_pts[0]])
        return base_pts
        
    def base_curves(self):
        crv_1 = Curve(self.base_pts).generate_curve()
        crv_2 = Curve(self.base_pts).offset_curve()
        return crv_1, crv_2
        
    def base_surface(self):
        return Surface(self.base_crvs).generate_surface()
        
    def auditorium_direction(self):
        pt1 = Point(self.STEP_Y, self.STEP_Y, self.STEP_Y).generate_point()
        pt2 = Point(self.STEP_Y ,self.CEIL_Z ,self.STEP_Y).generate_point()
        return Curve([pt1, pt2]).generate_curve()
        
    def chair_direction(self):
        pt1 = Point(self.STEP_Y, self.STEP_Y, self.STEP_Y).generate_point()
        pt2 = Point(self.STEP_Y, self.CHAIR_Y, self.STEP_Y).generate_point()
        return Curve([pt1, pt2]).generate_curve()
        
    def generate_auditorium(self):
        return Surface(self.base_crvs).extrude_surface(self.DIRECTION_A)
        
    def elements_auditorium(self, brep):
        try:
            faces, edges, vertices = gh.DeconstructBrep(rs.coercebrep(brep))
        except:
            faces, edges, vertices = gh.DeconstructBrep(brep)
        return faces, edges, vertices
        
    def generate_chairs(self, chair_pts):
        chair_crv = Curve(chair_pts).generate_curve()
        chair_ori = Surface(chair_crv).extrude_surface(self.DIRECTION_C)
        auditorium_lines = self.elements_auditorium(self.auditorium)[1]
        lines_index = [i for i in range(106, 142, 4)]
        for i in lines_index:
            base_curve = auditorium_lines[i]
            base_points = gh.DivideCurve(base_curve, self.CHAIRS, False)[0]
            base_points.pop(0); base_points.pop(-1)
            for bp in base_points:
                chair = rs.CopyObject(chair_ori, bp)
                self.chairs.append(chair)
        return self.chairs
        
    def generate_section(self):
        cutter_crv = Curve(self.cutter_pts).generate_curve()
        cutter = Surface(cutter_crv).generate_surface()
        cutting_idx = [i for i in range(5, 95, 10)]
        section_lines = []
        for i in cutting_idx:
            split_chair = rs.SplitBrep(self.chairs[i], cutter)[1];\
                          rs.CapPlanarHoles(split_chair)
            section_chair = self.elements_auditorium(split_chair)[0][0]
            section_lines.append(section_chair)
        
        split_auditorium = rs.SplitBrep(self.auditorium, cutter)[1];\
                           rs.CapPlanarHoles(split_auditorium);
        section_auditorium = self.elements_auditorium(split_auditorium)[0][0]
        section_lines.append(section_auditorium)
        rs.MoveObjects(section_lines, self.SECTION_M)
        return section_lines
        
    def generate_sight(self):
        section_lines = self.generate_section()[-1]
        sitting_lines = self.elements_auditorium(section_lines)[1]
        base_line = self.elements_auditorium(section_lines)[1][24]
        sight_points = gh.CurveMiddle([sitting_lines[37], sitting_lines[39]]);\
                       rs.MoveObjects(sight_points, [0,0,self.SIGHT_LEVEL]);
        focus_point = rs.CurvePoints(base_line)[0]
        
        sight_curve = Curve([sight_points[0], focus_point, sight_points[1]]).generate_curve()
        return [sight_curve, sight_points[0], sight_points[1]]
        
    def calculate_ceil_height(self):
        ceil_height = rs.Distance(self.base_pts[-3], self.base_pts[-4]) * self.SCALE
        limit_height = 2100
        
        if ceil_height < limit_height:
            return 0
        else:
            return ceil_height
        
    def calculate_step_margin(self):
        margin_space = (self.step_width - self.CHAIR_Y) * self.SCALE
        limit_margin = 350
        
        if margin_space < limit_margin:
            return 0
        else:
            return margin_space
        
    def calculate_cvalue(self):
        curr_ceil_height = self.calculate_ceil_height()
        curr_step_width = self.calculate_step_margin()
        
        sight_elements = self.generate_sight()
        cal_crv = sight_elements[0]
        cal_pt_1 = sight_elements[1]
        cal_vect = Point(0,0,1).generate_point()
        cal_line = gh.LineSDL(cal_pt_1, cal_vect, 30)
        cal_pt_2 = gh.CurveXLine(rs.coercecurve(cal_crv), cal_line)[0][1]
        
        if curr_ceil_height == 0 or curr_step_width == 0:
            cvalue = 0
        else:
            cvalue = rs.Distance(cal_pt_1, cal_pt_2) * self.SCALE
        return round(cvalue, 1)
        
    def visualization_circle(self):
        section_lines = self.generate_section()[-1]
        section_lines = self.elements_auditorium(section_lines)[1]
        circle_base = gh.CurveMiddle(section_lines[24]); rs.MoveObject(circle_base, [100,0,0])
        circle = gh.Circle(gh.PlaneOrigin(rg.Plane.WorldZX, circle_base), 25)
        circle_scaled = rs.coercegeometry(rs.CopyObject(circle, [130,0,0]))
        circle_origin = rs.coerce3dpoint(gh.Area(rs.coercegeometry(circle_scaled))[1])
        circle_scaled = gh.Scale(circle_scaled, circle_origin, 2)[0]
        
        circle_pts = gh.DivideCurve(circle, 4, False)[0]
        circle_scaled_pts = gh.DivideCurve(circle_scaled, 4, False)[0]
        connect_line_1 = Curve([circle_pts[0], circle_scaled_pts[0]]).generate_curve()
        connect_line_2 = Curve([circle_pts[2], circle_scaled_pts[2]]).generate_curve()
        return circle, circle_scaled, connect_line_1, connect_line_2
        
    def visualization_zoom(self):
        circle_list = self.visualization_circle()
        scaled_origin = rs.coerce3dpoint(gh.Area(rs.coercegeometry(circle_list[1]))[1])
        merge_curve = gh.Merge(gh.DeconstructBrep(self.generate_section())[1], self.generate_sight()[0])
        merge_curve[-1] = rs.coercecurve(merge_curve[-1])
        
        trimed_region = circle_list[0]
        trimed_curves = gh.TrimwithRegion(merge_curve, trimed_region, rg.Plane.WorldZX)[0];\
                        rs.MoveObjects(trimed_curves, [130,0,0])
        trimed_curves = gh.Scale(trimed_curves, scaled_origin, 2)[0]
        sight_curve = rs.coercecurve(self.generate_sight()[0]);\
                      rs.MoveObject(sight_curve, [130,0,0])
        sight_curve = gh.Scale(sight_curve, scaled_origin, 2)[0]
        sight_points = gh.EndPoints(sight_curve)
        cal_vect = Point(0,0,1).generate_point()
        cal_line = gh.LineSDL(sight_points[0], cal_vect, 30)
        cvalue_point = gh.CurveXCurve(sight_curve, cal_line)[0]
        cvalue_line = Curve([cvalue_point[0], cvalue_point[1]]).generate_curve()
        
        trimed_curves.extend([cvalue_line, cvalue_point[0], cvalue_point[1], sight_points[1]])
        
        return trimed_curves
        
    def visualization_text(self):
        text = "Current Condition ▼\nC-Value: {} \nCeiling Height: {} \nStep Height: {} \nStep Width: {} \nStep Margin: {}"\
               .format(self.calculate_cvalue(),
                       self.calculate_ceil_height(),
                       self.step_height * self.SCALE,
                       self.step_width * self.SCALE,
                       self.calculate_step_margin())
        return text
        
if __name__ == "__main__":
    auditorium = Auditorium(step_height, step_width, cutter_pts)
    auditorium_brep = auditorium.generate_auditorium()
    auditorium_chairs = auditorium.generate_chairs(chair_pts)
    auditorium_section = auditorium.generate_section()
    
    auditorium_focus = auditorium.generate_sight()
    auditorium_cvalue = auditorium.calculate_cvalue()
    section_circle = auditorium.visualization_circle()
    section_text = auditorium.visualization_text()
    section_zoom = auditorium.visualization_zoom()