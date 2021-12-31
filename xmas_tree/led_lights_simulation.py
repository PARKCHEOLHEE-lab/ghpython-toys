import Rhino.Geometry as rg
from System.Drawing import Color

csv = open(CSV, 'r')
simulation_limit = len(list(csv)) - 2
csv.close()

with open(CSV, 'r') as csv:
    if RUN == True:
        current_frame += 1
        if current_frame > simulation_limit:
            current_frame = 0
            
    else:
        current_frame = 0
    
    
    current_csv = csv.readlines()[current_frame+1].split(',')
    led_count = ( len(current_csv)-1 ) // 3
    
    colors = []
    transparencies = []
    for i in range(led_count):
        r = int( current_csv[i*3 + 1] )
        g = int( current_csv[i*3 + 2] )
        b = int( current_csv[i*3 + 3].replace('\n', '') )
        a = ( r + g + b ) / 3
        
        if a < min_alpha:
            a = min_alpha
            
        t = 1 - ( a / 255 )
        transparencies.append(t)
        
        color = Color.FromArgb(a, r, g, b)
        colors.append(color)