import Rhino.Geometry as rg

with open(tree_coord, "r") as coords:
    tree = []
    for coord in coords.readlines()[1:]:
        c = coord.split(',')
        c[3] = c[3].replace('\n', '')
        
        id, x, y, z = list(map(float, c))
        tree_point = rg.Point3d(x, y, z)
        tree.append(tree_point)
