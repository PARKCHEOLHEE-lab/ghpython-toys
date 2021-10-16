import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh

def size_scaling(x):
    return x*10
    
if __name__ == "__main__":
    crane_radius_1 = size_scaling(size[0])
    crane_radius_2 = size_scaling(size[1])