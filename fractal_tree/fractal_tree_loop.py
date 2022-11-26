import Rhino.Geometry as rg
import ghpythonlib.components as gh
import math

class FractalTree2D:
    def __init__(self, depth):
        self.depth = depth
        self.fractal_tree_branches = []
        
        self._generate()
        
    def _generate(self):
        for depth in range(self.depth):
            
            # _generate first branch
            if depth == 0:
                base_branch = rg.Line(ORIGIN, ORIGIN + VECTOR_Z * BRANCH_LENGTH)
                self.fractal_tree_branches.append(base_branch)
                self.fractal_tree_branches.extend(self._divide_target_branch(base_branch))
                
                if self.depth == 1:
                    break
                    
            sub_branches = self.fractal_tree_branches[-2 ** depth * 2:]
            
            for sub_branch in sub_branches:
                self.fractal_tree_branches.extend(self._divide_target_branch(sub_branch))
                
    def _divide_target_branch(self, target_branch):
                
        target_branch_last_vertex = target_branch.PointAt(1)
        
        reduced_target_branch= rg.Line(
                                      target_branch_last_vertex,
                                      target_branch.PointAt(1 - SUB_BRANCH_RATIO)
                                      )
        
        rotated_reduced_target_branch_1 = gh.Rotate(
                                                  reduced_target_branch, 
                                                  ANGLE * math.pi, 
                                                  gh.XZPlane(target_branch_last_vertex)
                                                 ).geometry
        
        rotated_reduced_target_branch_2 = gh.Rotate(
                                                  reduced_target_branch, 
                                                  (ANGLE + (1 - ANGLE) * 2) * math.pi, 
                                                  gh.XZPlane(target_branch_last_vertex)
                                                 ).geometry
        
        return rotated_reduced_target_branch_1, rotated_reduced_target_branch_2

ORIGIN = rg.Point3d(30, 0, 0)
VECTOR_Z = rg.Point3d(0, 0, 1)
SUB_BRANCH_RATIO = 0.7
BRANCH_LENGTH = 8
ANGLE = 0.88
DEPTH = 6

if __name__ == "__main__":
    # depth is iteration count
    fractal_tree_2d = FractalTree2D(depth=DEPTH)
    fractal_tree_branches = fractal_tree_2d.fractal_tree_branches