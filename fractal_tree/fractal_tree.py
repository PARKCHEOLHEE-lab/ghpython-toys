import math
import Rhino.Geometry as rg


def to_radians(angle):
    return math.pi * angle
    
def draw_tree(x1, y1, branch_angle, tree_length, base_angle, scale, depth, fractal_tree):
    if depth >= 0:
        rad = to_radians(base_angle)
        x2 = x1 + math.cos(rad) * tree_length
        y2 = y1 + math.sin(rad) * tree_length
        
        p1 = rg.Point3d(y1, 0, x1)
        p2 = rg.Point3d(y2, 0, x2)
        fractal_tree.append(rg.Line(p1, p2))
        
        draw_tree(x2, y2, branch_angle, tree_length*scale, base_angle+branch_angle, scale, depth-1, fractal_tree)
        draw_tree(x2, y2, branch_angle, tree_length*scale, base_angle-branch_angle, scale, depth-1, fractal_tree)
        
if __name__ == "__main__":
    branch_angle = 0.12
    tree_length = 15
    base_angle = 0
    scale = 0.7
    depth = 7
    
    fractal_tree = []
    origin_x, origin_y = 0, 0
    
    draw_tree(origin_x,origin_y,branch_angle, tree_length, base_angle, scale, depth, fractal_tree)