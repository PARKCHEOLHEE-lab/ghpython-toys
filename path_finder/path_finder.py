import math
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


class Utils:
    def generate_line(self, pt_1, pt_2):
        return rs.AddLine(pt_1, pt_2)
        
    def divide_curve(self, curve, seg_count):
        return rs.DivideCurve(curve, seg_count)
        
    def length_curve(self, curve):
        return rs.CurveLength(curve)
        
    def interpolate_curve(self, points):
        return rs.AddInterpCurve(points, degree=3, knotstyle=1)
        
    def projection_curve(self, curve, surface):
        return rs.ProjectCurveToSurface(curve, surface, [0,0,1])
        
    def surface_points(self, surface):
        return rs.SurfacePoints(surface)
        
    def move_object(self, object, translation):
        return rs.MoveObject(object, translation)
        

class PathFinder:
    def __init__(self, mountain, start_point, end_point, gene):
        self.mountain = mountain
        self.start_point = start_point
        self.end_point = end_point
        self.gene = gene
        
        self.utils = Utils()
        
    def get_mountain(self):
        return self.mountain
        
    def get_start_point(self):
        return self.start_point
        
    def get_end_point(self):
        return self.end_point
        
    def get_gene(self):
        return self.gene
        
    def calculate_slope(self, pt_1, pt_2):
        x1, y1, z1 = pt_1
        x2, y2, z2 = pt_2
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        slope_degree = (z2-z1)/distance * 100
        return slope_degree
        
    def calculate_average(self, degree_of_slope):
        return sum(degree_of_slope) / len(degree_of_slope)
        
    def limit_point(self):
        mountain_points = self.utils.surface_points(self.mountain)
        x_coordinates = []
        
        for point in mountain_points:
            x = point[0]
            if x not in x_coordinates:
                x_coordinates.append(x)
                
        min_x = min(x_coordinates)
        max_x = max(x_coordinates)
        return min_x, max_x
        
    def evaluate_fitness(self, degree_of_slope, length_of_path):
        average_degree = self.calculate_average(degree_of_slope)
        return average_degree * length_of_path
        
    def main(self):
        STRAIGHT_SEG_COUNT = 11
        PROJECTION_SEG_COUNT = 60
        MARGIN = 15
        
        min_x, max_x = self.limit_point()
        
        straight = self.utils.generate_line(self.start_point, self.end_point)
        divide_straight = self.utils.divide_curve(straight, STRAIGHT_SEG_COUNT)
        for i, point in enumerate(divide_straight[1:-1]):
            gene = self.get_gene()[i]
                
            translation = [gene, 0, 0]
            self.utils.move_object(point, translation)
            
            if point[0]-MARGIN < min_x:
                point[0] = min_x+MARGIN
            elif point[0]+MARGIN > max_x:
                point[0] = max_x-MARGIN
                
        interpolate_curve = self.utils.interpolate_curve(divide_straight)
        projection_curve = self.utils.projection_curve(interpolate_curve, self.get_mountain())
        
        divide_projection = self.utils.divide_curve(projection_curve, PROJECTION_SEG_COUNT)
        divide_projection_lines = []
        degree_of_slope = []
        length_of_path = 0
        for i in range(1, len(divide_projection)):
            pt_1 = divide_projection[i-1]
            pt_2 = divide_projection[i]
            
            line = self.utils.generate_line(pt_1, pt_2)
            divide_projection_lines.append(line)
            
            line_length = self.utils.length_curve(line)
            length_of_path += line_length
            
            degree = abs(self.calculate_slope(pt_1, pt_2))
            degree_of_slope.append(degree)
            
        fitness = self.evaluate_fitness(degree_of_slope, length_of_path)
        average_degree = self.calculate_average(degree_of_slope)
        return divide_projection_lines, fitness, average_degree, length_of_path
        
if __name__ == "__main__":
    utils = Utils()
    
    translation = [0,0,0]                                        # convert surface to guid
    mountain = utils.move_object(mountain, translation)          # convert surface to guid
    pf = PathFinder(mountain, start_point, end_point, gene)
    
    path, fitness, average_degree, length_of_path = pf.main()
