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
        
        
class Generator:
    pass
        




if __name__ == "__main__":
    data_obj = Data(file)
    data = data_obj.read_data()['features']
    
    test = data_obj.read_geometry()
    pts = []
    count = 0
    for coordinates in test:
        print(coordinates)
        for c in coordinates:
            print(c)
        
        if count > 1:
            break
        
        count += 1
#        pt = rs.AddPoint(t[0], t[1], 0)
#        pts.append(pt)
#    
#    
#    
#    a = rs.AddPolyline(pts)