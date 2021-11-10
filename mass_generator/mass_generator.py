import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import json
import time


class Data:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_features = self.read_data()['features']
        
    def read_data(self):
        with open(self.file_path, 'r') as data:
            convert_data = json.load(data)
        return convert_data
        
    def read_columns(self):
        return self.read_data().keys()
        
    def read_geometry(self):
        geometry_data = []
        for data in self.data_features:
            geometries = data['geometry']['coordinates'][0][0]
            geometry_data.append(geometries)
        return geometry_data
        
    def read_information(self):
        information_data = []
        for data in self.data_features:
            properties = data['properties']
            information_data.append(properties)
        return information_data
        
    def calculate_height(self):
        building_information = self.read_information()
        building_heights = []
        floor_height = 4
        for information in building_information:
            height_information = information['HEIGHT']
            floor_information = information['GRND_FLR']
            
            building_height = max(height_information, floor_information * floor_height)
            building_heights.append(building_height)
        return building_heights


class Generator(Data):
    def __init__(self, path):
        Data.__init__(self, path)
        
    def generate_polylines(self):
        polylines = []
        coordinates = self.read_geometry()
        for coords in coordinates:
            points = []
            
            for c in coords:
                x, y, z = c[0], c[1], 0
                point = rs.AddPoint(x, y, z)
                points.append(point)
            
            polyline = rs.AddPolyline(points)
            polylines.append(polyline)
        return polylines
        
    def extrude_polylines(self):
        building_polylines = self.generate_polylines()
        building_heights = self.calculate_height()
        
        buildings = []
        for i, polyline in enumerate(building_polylines):
            z = building_heights[i]
            path = rs.AddLine(rs.AddPoint(0,0,0), rs.AddPoint(0,0,z))
            building = rs.ExtrudeCurve(polyline, path)
            
            if building is not None:
                rs.CapPlanarHoles(building)
            
            buildings.append(building)
        return buildings



if __name__ == "__main__":
    data_object = Generator(file_path)
    print(data_object.read_information()[0])
    print(data_object.read_information()[1])
    
    buildings = data_object.extrude_polylines()
    
    heights = data_object.calculate_height()
    min_height = min(heights)
    max_height = max(heights)
    
#    structure_code = []
#    for data in data_object.read_information():
#        strct_cd = data['STRCT_CD']
#        if strct_cd is not None:
#            structure_code.append(data['STRCT_CD'])
#    
#    print(sorted(list(set(structure_code))))
#    print(set(structure_code))