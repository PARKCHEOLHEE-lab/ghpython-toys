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
    def __init__(self, step_height, step_width):
        # Constant
        self.START_X = 110
        self.END_X = 270
        self.STEP_COUNT = 10
        self.STEP_X = 160
        self.STEP_Y = 0
        self.CEIL_Z = 65
        self.DIRECTION = self.base_direction()
        
        # Parameter
        self.step_width = step_width
        self.step_height = step_height
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
        
    def base_direction(self):
        pt1 = Point(self.STEP_Y, self.STEP_Y, self.STEP_Y).generate_point()
        pt2 = Point(self.STEP_Y ,self.CEIL_Z ,self.STEP_Y).generate_point()
        return Curve([pt1, pt2]).generate_curve()
        
    def generate_auditorium(self):
        return Surface(self.base_crvs).extrude_surface(self.DIRECTION)
        
    def deconstruct_auditorium(self):
        return gh.DeconstructBrep(rs.coercebrep(self.auditorium))[1]
        
    def calculate_height(self):
        return rs.Distance(self.base_pts[-3], self.base_pts[-4])



if __name__ == "__main__":
    auditorium = Auditorium(step_height, step_width)
    auditorium_height = auditorium.calculate_height()
    auditorium_brep = auditorium.generate_auditorium()
    d = auditorium.deconstruct_auditorium()