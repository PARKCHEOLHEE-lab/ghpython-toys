import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh
import json


class Data:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def read_data(self):
        with open(self.file_path, 'r') as data:
            convert_data = json.load(data)
        return convert_data
        
    def read_columns(self):
        return self.read_data().keys()
        
    def read_geometry(self):
        data_features = self.read_data()['features']
        
        data_geometries = []
        for d in data_features:
            d = d['geometry']['coordinates'][0][0]
            data_geometries.append(d)
            
        return data_geometries


class Generator(Data):
    def __init__(self, path):
        Data.__init__(self, path)
        self.coordinates = self.read_geometry()
        
    def generate_polylines(self):
        polylines = []
        for coordinates in self.coordinates:
            points = []
            
            for c in coordinates:
                x, y, z = c[0], c[1], 0
                point = rs.AddPoint(x, y, z)
                points.append(point)
            
            polyline = rs.AddPolyline(points)
            polylines.append(polyline)
            
        return polylines



if __name__ == "__main__":
    data_object = Generator(file_path)
    
    polylines = data_object.generate_polylines()
    
