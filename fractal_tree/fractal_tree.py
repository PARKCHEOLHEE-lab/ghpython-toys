import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


BASE_ANGLE = 0
BRANCH_ANGLE = 0.12
TREE_LENGTH = 15

x1, y1 = 0, 0
x2 = x1 + math.cos(math.radians(BASE_ANGLE)) * TREE_LENGTH
y2 = y1 + math.sin(math.radians(BASE_ANGLE)) * TREE_LENGTH

p1 = rg.Point3d(y1, 0, x1)
p2 = rg.Point3d(y2, 0, x2)