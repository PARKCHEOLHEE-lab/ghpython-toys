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
        
    def rotate_rectangle(self):
        return
    

class Tower(Rectangle):
    def __init__(self, origin, width, height, vertical_heights):
        self.recs = []
        self.floor_height = 4
        self.vertical_heights = vertical_heights
        Rectangle.__init__(self, origin, width, height)
        
    def get_recs(self):
        return self.recs
        
    def get_vertical_heights(self):
        return self.vertical_heights
        
    def get_floor_height(self):
        return self.floor_height
        
    def heights_length(self):
        return len(vertical_heights)
        
    def generate_frame(self):
        for i in range(self.heights_length()):
            z = self.get_vertical_heights()[i]
            copied_rectangle = self.copy_rectangle([0, 0, z*self.get_floor_height()])
            self.recs.append(copied_rectangle)
        return self.get_recs()

if __name__ == "__main__":
    ORIGIN = [200, 0, 0]
    SIZE = 32
    
    tower_obj = Tower(ORIGIN, SIZE, SIZE, vertical_heights)
    tower = tower_obj.generate_frame()
    
        
