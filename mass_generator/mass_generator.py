import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
from collections import Counter
import json


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
        
    def preprocess_information(self, keyword):
        postprocess = []
        for data in self.read_information():
            target_data = data[keyword]
            if target_data is not None:
                postprocess.append(int(target_data))
            else:
                postprocess.append(0)
        return postprocess


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
        
    def generate_centroids(self):
        polylines = self.generate_polylines()
        centroids = []
        for polyline in polylines:
            centroid = rs.CurveAreaCentroid(polyline)[0]
            centroids.append(centroid)
        return centroids
        
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
    buildings = data_object.extrude_polylines()
    centroids = data_object.generate_centroids()
    
    heights = data_object.calculate_height()
    min_height = min(heights)
    max_height = max(heights)
    
    regist_keyword = 'REGIST_DAY'
    regist_codes = data_object.preprocess_information(regist_keyword)
    min_regist_code = min(regist_codes)
    max_regist_code = max(regist_codes)
    
    structure_keyword = 'STRCT_CD'
    structure_codes = data_object.preprocess_information(structure_keyword)
    min_structure = min(structure_codes)
    max_structure = max(structure_codes)

    usability_keyword = 'USABILITY'
    usability_codes = data_object.preprocess_information(usability_keyword)
    min_usability = min(usability_codes)
    max_usability = max(usability_codes)
    
    scaled_usability = list(map(lambda x: int(100 * ((x-min_usability) / max_usability - min_usability)), usability_codes))
    min_scaled_usability = min(scaled_usability)
    max_scaled_usability = max(scaled_usability)
    
    heights_text = heights
    regist_text = regist_codes
    structure_text = structure_codes
    usability_text = usability_codes