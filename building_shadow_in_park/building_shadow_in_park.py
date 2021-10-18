import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


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

class Sphere:
    pass


class Sun(Sphere):
    pass


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
    
    tower_obj = Tower(TOWER_ORIGIN, TOWER_SIZE, TOWER_COUNT, floor)
    park_obj = Rectangle(PARK_ORIGIN, PARK_SIZE)
    mass_obj = Rectangle(MASS_ORIGIN, MASS_SIZE)
    
    tower = tower_obj.extrude_grid()
    park = park_obj.generate_rectangle()
    mass = mass_obj.extrude_rectangle(MASS_HEIGHT)
    
    print(tower_obj.calculate_gfa())