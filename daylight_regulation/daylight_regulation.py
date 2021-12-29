import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


if __name__ == "__main__":
    
    ceiling_polylines = []
    criterion = 9
    for i in range(1, floor_count+1):
        ceiling_height = i*floor_height
        distance = 1.5
        
        if ceiling_height > criterion:
            distance = ceiling_height / 2
        
        s_vector = gh.ConstructPoint(0, -distance, 0)
        moved_polyline = gh.Move(site_polyline, s_vector)[0]
        
        ceiling_polyline = gh.RegionIntersection(moved_polyline, site_polyline)
        z_vector = gh.ConstructPoint(0, 0, ceiling_height)
        
        ceiling_polyline = gh.Move(ceiling_polyline, z_vector)[0]
        ceiling_polylines.append(ceiling_polyline)
    
    if cutting_type == True:
        z_vector = gh.ConstructPoint(0, 0, -floor_height)
        first_floor = gh.Move(ceiling_polylines[0], z_vector)[0]
        
        ceiling_polylines.insert(0, first_floor)
        mass = []
        for i in range(len(ceiling_polylines)-1):
            loft_polyline = [ceiling_polylines[i], ceiling_polylines[i+1]]
            wall = rs.AddLoftSrf(loft_polyline)
            
            converted_wall = rs.coercebrep(wall)
            floor = gh.CapHoles(converted_wall)
            mass.append(floor)
        
        
    else:
        mass = []
        for ceiling in ceiling_polylines:
            z_vector = gh.ConstructPoint(0, 0, -floor_height)
            
            wall = gh.Extrude(ceiling, z_vector)
            floor = gh.CapHoles(wall)
            mass.append(floor)
