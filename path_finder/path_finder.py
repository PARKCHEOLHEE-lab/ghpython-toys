import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


class Utils:
    def generate_line(self, pt_1, pt_2):
        return rs.AddLine(pt_1, pt_2)
        
#    def generate_pipe(curve):
#        rs.AddPipe(
        
    
    def divide_curve(self, curve, seg_count):
        return rs.DivideCurve(curve, seg_count)
            
    def move_object(self, object, translation):
        return rs.MoveObject(object, translation)
        
    def interpolate_curve(self, points):
        return rs.AddInterpCurve(points, degree=3, knotstyle=1)


class PathFinder:
    def __init__(self, mountain, start_point, end_point, gene):
        self.mountain = mountain
        self.start_point = start_point
        self.end_point = end_point
        self.gene = gene
        
    def get_start_point(self):
        return self.start_point
        
    def get_end_point(self):
        return self.end_point
        
    def get_gene(self):
        return self.gene
        
        
    def main(self):
        utils = Utils()
        
        SEG_COUNT = 11
        
        straight = utils.generate_line(self.start_point, self.end_point)
        divide_straight = utils.divide_curve(straight, SEG_COUNT)
        
        for i, point in enumerate(divide_straight[1:-1]):
            gene = self.get_gene()[i]
            translation = [gene, 0, 0]
            utils.move_object(point, translation)
            
        return divide_straight
        
if __name__ == "__main__":
    pf = PathFinder(mountain, start_point, end_point, gene)
    
    a = pf.main()