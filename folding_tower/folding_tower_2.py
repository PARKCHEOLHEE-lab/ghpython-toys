import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh

contours = gh.BoundarySurfaces(contours)
rs.MoveObject(contours, [200,0,0])

collision = gh.CollisionOneXMany(contours, core).collision

contours = [c for i, c in enumerate(contours) if collision[i] == True]
