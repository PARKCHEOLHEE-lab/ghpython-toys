import Rhino.Geometry as rg
import ghpythonlib.components as gh
import ghpythonlib.treehelpers as gt
import math



class FractalChristmassTree:
    def __init__(self, depth):
        self.depth = depth                          # int
        self.fractal_christmass_tree_branches = []  # List[Rhino.Geometry.Line]
        self.fractal_christmass_tree_main_branches = []
        
        self._generate()
        
    def _generate(self):
        """generate fractal_christmass_tree"""
        
        if self.depth > 0:
            height = 0
            for i in reversed(range(TREE_ITERATION_COUNT)):
                circle_origin = ORIGIN + rg.Point3d(0, 0, height)
                
                circle_radius = CIRCLE_RADIUS * CIRCLE_RATIO * i
                circle = rg.Circle(circle_origin, circle_radius)
                
                height += HEIGHT_INTERVAL
                
                if circle.Radius != 0 and i != TREE_ITERATION_COUNT - 1:
                    
                    divided_circle_points = gh.DivideCurve(circle, CIRCLE_DIVIDE_COUNT + i, False).points
                    main_branches = gh.Line(
                                     circle_origin + rg.Point3d(0, 0, HEIGHT_INTERVAL), 
                                     divided_circle_points
                                    )
                                    
                    self.fractal_christmass_tree_branches.extend(main_branches)
                    self.fractal_christmass_tree_main_branches.extend(main_branches)
                    
                    for main_branch in main_branches:
                        # 1st depth branches per main branches
                        sub_branches = self._get_sub_branches(main_branch)
                        self.fractal_christmass_tree_branches.extend(sub_branches)
                        
                        if self.depth > 1:
                            # greater than 2nd depth branches per sub branches
                            for d in range(self.depth - 1):
                                sub_branches = self._get_depth_sub_branches(sub_branches)
                                self.fractal_christmass_tree_branches.extend(sub_branches)
        
    def _get_divided_target_branch(self, target_branch):
        """get target branch's sub branches"""
        
        target_branch_aligned_surface = gh.Extrude(target_branch, VECTOR_Z)
        target_branch_aligned_plane = gh.PlaneOrigin(
                                                     target_branch_aligned_surface,
                                                     gh.Area(target_branch_aligned_surface).centroid
                                                    )
                                                    
        target_branch_origin = target_branch.PointAt(0)
        target_branch_aligned_plane.Origin = target_branch_origin
        
        sub_brnach_1_base_segment = gh.Rotate(
                                              target_branch, 
                                              math.pi * SUB_BRANCH_ANGLE, 
                                              target_branch_aligned_plane
                                             ).geometry
                                                
        sub_brnach_1_rotated_segment = gh.Rotate(
                                                 sub_brnach_1_base_segment, 
                                                 math.pi * SUB_BRANCH_ANGLE, 
                                                 target_branch_origin,
                                                ).geometry
        sub_brnach_2_rotated_segment = gh.Rotate(
                                                 sub_brnach_1_base_segment, 
                                                 math.pi * -SUB_BRANCH_ANGLE, 
                                                 target_branch_origin,
                                                ).geometry
        
        return [sub_brnach_1_rotated_segment, sub_brnach_2_rotated_segment]

    def _get_sub_branches(self, target_branch):
        """get target branch's all sub branches"""
        
        divided_target_branch_points = gh.DivideCurve(target_branch, SUB_BRANCH_DIVIDE_COUNT, False).points
        shifted_divided_target_branch_points = divided_target_branch_points[1:] + divided_target_branch_points[:1]
        
        divided_segments = [
                            rg.Line(d, s) for d, s in zip(
                                                          divided_target_branch_points[:-1],
                                                          shifted_divided_target_branch_points[:-1]
                                                         )
                           ]
    
        sub_branch_1_segments = self._get_divided_target_branch(divided_segments[1])
        sub_branch_2_segments = self._get_divided_target_branch(divided_segments[2])
        
        return sub_branch_1_segments + sub_branch_2_segments
        
        
    def _get_depth_sub_branches(self, sub_branches):
        """get sub branches's sub branches"""
        
        all_divided_sub_branches = []
        for sub_branch in sub_branches:
            divided_sub_branches = self._get_sub_branches(sub_branch)
            all_divided_sub_branches += divided_sub_branches
            
        return all_divided_sub_branches


ORIGIN = rg.Point3d(0, 0, 0)
VECTOR_Z = rg.Point3d(0, 0, 1)

CIRCLE_RATIO = 0.2
CIRCLE_RADIUS = 10
CIRCLE_DIVIDE_COUNT = 10
TREE_ITERATION_COUNT = 8
HEIGHT_INTERVAL = 5

DEPTH = 3
SUB_BRANCH_LOCATION = 0.333
SUB_BRANCH_DIVIDE_COUNT = 3
SUB_BRANCH_ANGLE = -0.2


if __name__ == "__main__":
    fractal_christmass_tree = FractalChristmassTree(depth=DEPTH)
    trunk = rg.Line(ORIGIN, ORIGIN + rg.Point3d(0, 0, TREE_ITERATION_COUNT * HEIGHT_INTERVAL - 5))
    
    fractal_christmass_tree_branches = fractal_christmass_tree.fractal_christmass_tree_branches
    
    TEST = fractal_christmass_tree.fractal_christmass_tree_main_branches