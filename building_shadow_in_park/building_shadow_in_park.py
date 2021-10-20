import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


class Vector:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2
        
    def generate_vector(self):
        x1, y1, z1 = self.point_1
        x2, y2, z2 = self.point_2
        return rg.Point3d(x2, y2, z2) - rg.Point3d(x1, y1, z1)


class Rectangle:
    def __init__(self, origin, size):
        self.origin = origin
        self.size = size
        self.rectangle = self.generate_rectangle()
        
    def generate_rectangle(self):
        return rs.AddRectangle(self.origin, self.size, self.size)
        
    def extrude_rectangle(self, height):
        direction = rs.AddLine(rs.AddPoint(0,0,0), rs.AddPoint(0,0,height))
        mass = rs.ExtrudeCurve(self.rectangle, direction); rs.CapPlanarHoles(mass)
        return mass
        
    def generate_planarsrf(self):
        return rs.AddPlanarSrf(self.rectangle)


class Region:
    def __init__(self, curves):
        self.plane = rg.Plane.WorldXY
        if len(curves) == 1:
            self.curves = curves
        else:
            self.curves = self.evaluate_type(curves)
            self.union = self.generate_union()
            self.intsc = self.generate_intersection()
        
    def evaluate_type(self, curves):        
        converted_curves = []
        for curve in curves:
            if type(curve) == type(rs.AddPoint(0,0,0)):
                converted_curves.append(rs.coercecurve(curve))
            else:
                converted_curves.append(curve)
        return converted_curves
        
    def generate_union(self):
        return gh.RegionUnion(self.curves, self.plane)
        
    def generate_intersection(self):
        return gh.RegionIntersection(self.curves[0], self.curves[1], self.plane)
        
    def area_region(self):
        return round(gh.Area(self.curves)[0], 0)
        
    def area_intersection(self):
        try: 
            intsc_area = gh.Area(self.intsc)[0]
            if type(intsc_area) == list:
                intsc_area = sum(intsc_area)
            return round(intsc_area, 0)
        except:
            return 0


class Sphere:
    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius
        
    def generate_sphere(self):
        return rs.AddSphere(self.origin, self.radius)


class Sun(Sphere):
    def __init__(self, origin, radius, position):
        Sphere.__init__(self, origin, radius)
        self.SUN_RADIUS = 50
        self.position = position
        self.sphere = self.generate_sphere()
        self.split_sphere = self.split_sphere()
        
    def split_sphere(self):
        cutter_size = rg.Interval(-1000, 1000)
        cutter = Rectangle(self.origin, cutter_size).generate_planarsrf()
        return rs.SplitBrep(self.sphere, cutter)[0]
        
    def generate_path(self):
        if type(self.split_sphere) == type(rs.AddPoint(0,0,0)):
            self.split_sphere = rs.coercebrep(self.split_sphere)
        uv = rs.SurfaceParameter(self.split_sphere, [self.position[0], self.position[1], 0])
        path = gh.IsoCurve(self.split_sphere, gh.ConstructPoint(uv[0], uv[1], 0))
        return path
        
    def generate_sun(self):
        sun_base = rs.SurfaceParameter(self.split_sphere, self.position)
        sun_origin = rs.EvaluateSurface(self.split_sphere, sun_base[0], sun_base[1])
        sun = Sphere(sun_origin, self.SUN_RADIUS).generate_sphere()
        return sun, sun_origin


class Tower(Rectangle):
    def __init__(self, origin, size, count, heights):
        Rectangle.__init__(self, origin, size)
        self.FLOOR_HEIGHT = 4.5
        self.count = count
        self.heights = heights
        self.rectangle = self.generate_rectangle()
        self.grid = self.generate_grid()
        self.tower = self.extrude_grid()
        
    def generate_grid(self):
        grid = []
        for i in range(self.count):
            for j in range(self.count):
                grid.append(rs.CopyObject(self.rectangle, [i*self.size, j*self.size, 0]))
        return grid
        
    def extrude_grid(self):
        tower = []
        for i in range(len(self.grid)):
            if i == 4:
                self.heights[i] = max(self.heights)
            direction = rs.AddLine(rs.AddPoint(0,0,0), rs.AddPoint(0,0,self.heights[i]*self.FLOOR_HEIGHT))
            tower.append(rs.ExtrudeCurve(self.grid[i], direction)); rs.CapPlanarHoles(tower[i])
        return tower
        
    def generate_shadow(self, vector):
        mesh_setting = rg.MeshingParameters()
        tower_shadow = []
        for tower in self.tower:
            mesh_tower = rg.Mesh.CreateFromBrep(rs.coercebrep(tower), mesh_setting)
            tower_shadow.extend(gh.MeshShadow(mesh_tower, vector, rg.Plane.WorldXY))
        shadow = Region(tower_shadow).generate_union()
        return shadow
        
    def area_shadow(self, shadow):
        return gh.Area(shadow)[0]
        
    def calculate_gfa(self):
        return self.size * self.size * sum(self.heights)



if __name__ == "__main__":
    TOWER_ORIGIN = [200, 0, 0]
    TOWER_SIZE = 23
    TOWER_COUNT = 3
    PARK_ORIGIN = [200,100,0]
    PARK_SIZE = 165
    MASS_ORIGIN = [300,0,0]
    MASS_SIZE = 69
    MASS_HEIGHT = 50
    SPHERE_RADIUS = 700
    SUN_POSITION = [sun_position_x, sun_position_y]
    
    tower_obj = Tower(TOWER_ORIGIN, TOWER_SIZE, TOWER_COUNT, floor_count)
    park_obj = Rectangle(PARK_ORIGIN, PARK_SIZE)
    mass_obj = Rectangle(MASS_ORIGIN, MASS_SIZE)
    sun_obj = Sun(TOWER_ORIGIN, SPHERE_RADIUS, SUN_POSITION)
    
    tower = tower_obj.extrude_grid()
    park = park_obj.generate_rectangle()
    mass = mass_obj.extrude_rectangle(MASS_HEIGHT)
    mass_crv = mass_obj.generate_rectangle()
    
    sun = sun_obj.generate_sun()[0]
    sun_origin = sun_obj.generate_sun()[1]
    sun_path = sun_obj.generate_path()
    sun_vector = Vector(sun_origin, TOWER_ORIGIN).generate_vector()
    shadow = tower_obj.generate_shadow(sun_vector)
    
    shadow_area = Region([shadow]).area_region()
    shadow_park_intsc_area = Region([shadow, park]).area_intersection()
    shadow_mass_intsc_area = Region([shadow, mass_crv]).area_intersection()
    gross_floor_area = tower_obj.calculate_gfa()