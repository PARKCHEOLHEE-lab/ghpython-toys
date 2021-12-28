import math
import Rhino.Geometry as rg

class FractalTree:
    def __init__(self, origin_x, origin_y, branch_angle, tree_length, base_angle, scale, depth):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.branch_angle = branch_angle
        self.tree_length = tree_length
        self.base_angle = base_angle
        self.scale = scale
        self.depth = depth
        
        self.branch = []
        
    def to_radians(self, angle):
        return math.pi * angle
        
    def draw_tree(self):
        return
    
#def draw_tree(x1, y1, branch_angle, tree_length, base_angle, scale, depth):
#    if depth >= 0:
#        rad = to_radians(base_angle)
#        x2 = x1 + math.cos(rad) * tree_length
#        y2 = y1 + math.sin(rad) * tree_length
#        
#        p1 = rg.Point3d(y1, 0, x1)
#        p2 = rg.Point3d(y2, 0, x2)
#        
#    return p1, p2

if __name__ == "__main__":
    branch_angle = 0.12
    tree_length = 15
    base_angle = 0
    scale = 0.7
    depth = 7
    
    origin_x, origin_y = 0, 0
    fractal_tree = FractalTree(origin_x,origin_y,branch_angle, tree_length, base_angle, scale, depth)
    
