import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh

def extrude_curve(crv, height):
    direction = rs.AddLine(rs.AddPoint(0,0,0), rs.AddPoint(0,0,height))
    mass = rs.ExtrudeCurve(crv, direction); rs.CapPlanarHoles(mass)
    return mass
    
def generate_mass(crvs, heights):
    masses = []
    for crv in crvs:
        if type(heights) != list:
            random_height = heights
        else:
            random_height = random.choice(heights)
        mass = extrude_curve(crv, random_height)
        masses.append(mass)
    return masses

if __name__ == "__main__":
    random.seed(0)
    
    low_heights = [3, 6, 9]
    middle_height = 15
    high_height = 70
    ground = extrude_curve(boundary[76], -20)
    low_masses = generate_mass(low_mass, low_heights)
    middle_masses = generate_mass(middle_mass, middle_height)
    high_masses = generate_mass(high_mass, high_height)