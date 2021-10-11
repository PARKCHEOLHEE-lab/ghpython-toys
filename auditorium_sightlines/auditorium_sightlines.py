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
        self.START_X = 110
        self.END_X = 270
        self.STEP_COUNT = 10
        self.STEP_X = 160
        self.STEP_Y = 0
        self.CHAIR_Y = 5
        self.CEIL_Z = 65
        self.CHAIRS = 11
        self.SECTION_M = [230, 0, 0]
        self.DIRECTION_A = self.auditorium_direction()
        self.DIRECTION_C = self.chair_direction()
        
        self.step_width = step_width
        self.step_height = step_height
        self.cutter_pts = cutter_pts
        self.chairs = []
        self.base_pts = self.base_points()
        self.base_crvs = self.base_curves()
        self.auditorium = self.generate_auditorium()
        
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
        
    def calculate_height(self):
        return rs.Distance(self.base_pts[-3], self.base_pts[-4])
        
    def calcuate_cvalue(self):
        section_lines = self.generate_section()[-1]
        base_line = self.elements_auditorium(section_lines)[1][25]
        focus = rs.CurveMidPoint(base_line)
        return focus


if __name__ == "__main__":
    auditorium = Auditorium(step_height, step_width, cutter_pts)
    
    auditorium_height = auditorium.calculate_height()
    auditorium_brep = auditorium.generate_auditorium()
    auditorium_chairs = auditorium.generate_chairs(chair_pts)
    auditorium_section = auditorium.generate_section()
    auditorium_focus = auditorium.calcuate_cvalue()