import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh
import Rhino

class Space:
    def __init__(self, curves, resolution):
        self.curves = curves
        self.resolution = resolution
        self.coordinate = self.get_coordinate()
        self.grid = self.generate_grid()
        
    def get_coordinate(self):
        points = []
        for curve in self.curves:
            points.extend(rs.CurvePoints(curve))
        
        min_coords = []
        max_coords = []
        for i in range(2):
            min_coord = min([coord[i] for coord in list(set(points))])
            max_coord = max([coord[i] for coord in list(set(points))])
            min_coords.append(min_coord)
            max_coords.append(max_coord)
        
        min_x, min_y = min_coords
        max_x, max_y = max_coords
        coordinates = [rg.Point3d(min_x, min_y, 0),
                       rg.Point3d(max_x, min_y, 0),
                       rg.Point3d(min_x, max_y, 0),
                       rg.Point3d(max_x, max_y, 0)]
        return coordinates
        
    def generate_brep(self):
        path = rs.AddLine(rs.AddPoint(0,0,0), rs.AddPoint(0,0,-0.1))
        surface = rs.AddPlanarSrf(self.curves)
        brep = rs.ExtrudeSurface(surface, path)
        return rs.coercebrep(brep)
        
    def generate_boundingbox(self):
        plane = rg.Plane.WorldXY
        return rg.Rectangle3d(plane, self.coordinate[0], self.coordinate[3])
        
    def generate_grid(self):
        bbox_width = self.coordinate[0].DistanceTo(self.coordinate[1])
        bbox_height = self.coordinate[0].DistanceTo(self.coordinate[2])
        unit_width = bbox_width / self.resolution
        unit_height= bbox_height / self.resolution
        start_point = self.coordinate[0]
        
        grid = []
        for i in range(resolution):
            for j in range(resolution):
                origin = [start_point[0] + i*unit_width, start_point[1] + j*unit_height, start_point[2]]
                unit = rs.AddRectangle(origin, unit_width, unit_height)
                grid.append(unit)
        return grid
        
    def generate_centroid(self):
        grid = self.generate_grid()
        centroids = [rs.CurveAreaCentroid(unit)[0] for unit in grid]
        return centroids
        
    def generate_ray(self):
        centroids = self.generate_centroid()
        rays = []
        for centroid in centroids:
            ray_len = rg.Point3d(100,0,0)
            ray = rs.AddLine(centroid, centroid + ray_len)
            rays.append(ray)
        return rays
        
    def generate_inside_grid(self):
        brep = self.generate_brep()
        centroids = self.generate_centroid()
        inside_check = gh.PointInBrep(brep, centroids, False)
        inside_grid = []
        inside_centroid = []
        for i, check in enumerate(inside_check):
            if check == True:
                inside_grid.append(self.grid[i])
                inside_centroid.append(centroids[i])
        return inside_grid, inside_centroid
        
    def generate_grid_surface(self):
        inside_grid = [rs.coercecurve(unit) for unit in self.generate_inside_grid()[0]]
        return gh.BoundarySurfaces(inside_grid)
        
#    def generate_inside_grid(self):
#        rays = self.generate_ray()
#        inside_grid = []
#        for i, ray in enumerate(rays):
#            intersect = gh.CurveXCurve(rs.coercecurve(rays[i]), self.curves)[0]
#            if type(intersect) != type(None):
#                if len(intersect) % 2 != 0:
#                    inside_grid.append(self.grid[i])
#        return inside_grid
        
    def generate_vispolygon(self):
        inside_centroid = self.generate_inside_grid()[1]
        point_count = 100
        radius = 100
        vispolygons = []
        for centroid in inside_centroid:
            isovist = gh.IsoVist(centroid, point_count, radius, self.curves)[0]
            vispolygons.append(gh.PolyLine(isovist, True))
        return vispolygons
        
    def perimeter_vispolygon(self):
        vispolygons = self.generate_vispolygon()
        perimeters = []
        for vispolygon in vispolygons:
            perimeters.append(rs.CurveLength(vispolygon))
        return perimeters
        
        


if __name__ == "__main__":
    space_obj = Space(space, resolution)
    
    all_perimeter = space_obj.perimeter_vispolygon()
    min_perimeter = min(space_obj.perimeter_vispolygon())
    max_perimeter = max(space_obj.perimeter_vispolygon())
    grid_surface = space_obj.generate_grid_surface()