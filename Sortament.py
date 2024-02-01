import fileinput
import json
from decimal import Decimal, localcontext
from typing import List
import numpy as np


class Type:
    def __init__(self, _c1, _c2, _c3, _r1, _r2, _r3):
        self.c1 = _c1
        self.c2 = _c2
        self.c3 = _c3
        self.r1 = _r1
        self.r2 = _r2
        self.r3 = _r3

    J = None
    S = None

def Y_CT_Z (c1,c2,c3,r1,r2,r3):
    return (c1*r1*r1/2 + (c2-r1-r3)*r2*(r1 + (c2 - r1 - r2)/2) + c3*r3*(c2-r3/2))/(c1*r1+(c2-r1-r3)*r2 + c3*r3)

def JzZetik(c1,c2,c3,r1,r2,r3) :
    Ji1 = c1*r1**3/12
    Ji2 = r2*(c2-r1-r3)**3/12
    Ji3 = c3*r3**3/12
    Y_ct_z = Y_CT_Z (c1,c2,c3,r1,r2,r3)
    return Ji1 + c1*r1*(Y_ct_z-r1/2)**2 + Ji2+ r2*(c2-r1-r3)*(Y_ct_z-(r1 + (c2 - r1 - r2)/2))**2 + Ji3 + c3*r3*(Y_ct_z-(c2 - r3/2))**2

def S_str( _c1, _c2,_c3,_r1, _r2,_r3) :
    return (_c1*_r1 + (_c2 - _r1 - _r3)*_r2 + _c3*_r3)

sortament : List[Type]= []
with open(r"c:\Production\Sortament\Sortament_L_raw.txt", "r") as input_file:
    counter = 1
    for line in input_file:
        if (counter < 12):
            if (counter == 2):
                line = line.strip()
                value = float(line)
                c2 = value
            if (counter ==3):
                line = line.strip()
                value = float(line)
                c1 = value
            if (counter == 4):
                line = line.strip()
                value = float(line) 
                r2 = value
            if (counter == 5) :
                line = line.strip()
                value = float(line)
                r1 = value
            counter = counter+1
        else:
            if ( 10 <= c1 <= 60 and 10 <= c2 <= 200 and 1 <= r1 <= 10 and 1 <= r2 <= 10):
                sortament.append(Type(c1, c2,0, r1, r2,0))
            counter = 1

with open(r"c:\Production\Sortament\Sortament_Z_raw.txt", "r") as input_file:

    counter = 1
    for line in input_file:
        if (counter < 12):
            if (counter == 2):
                line = line.strip()
                value = float(line)
                c2 = value
            if (counter ==3):
                line = line.strip()
                value = float(line)
                c1 = value
                c3 = value
            if (counter == 4):
                line = line.strip()
                value = float(line) 
                r2 = value
            if (counter == 5) :
                line = line.strip()
                value = float(line)
                r1 = value
            if (counter == 6) :
                line = line.strip()
                if (line != '-'):
                    value = float(line)
                    r3 = value
                else:
                    r3 = 0
            counter = counter+1
        else:
            sortament.append(Type(c1, c2, c3, r1, r2, r3))
            counter = 1


with localcontext() as ctx:   
    ctx.prec = 4    
    for type in sortament:
            type.S = round(S_str(type.c1,type.c2, type.c3, type.r1, type.r2, type.r3 ), 2)
            type.J = round(JzZetik(type.c1,type.c2, type.c3, type.r1, type.r2, type.r3 ) + \
                  S_str(type.c1,type.c2, type.c3, type.r1, type.r2, type.r3 )
                  *(Y_CT_Z(type.c1,type.c2, type.c3, type.r1, type.r2, type.r3 )**2), 2 )      
js_str = ""
js_str = json.dumps([ob.__dict__ for ob in sortament])
js_str = js_str.replace("}, {", "},\n {")
js_str = js_str.replace(" 0,", " 0.0,")

with open(r"c:\Production\Sortament\Sortament_L_and_Z.json", 'w', encoding='utf-8') as file:
    file.write(js_str)


sortament_filtered_stringers : List[Type]= []
for item in sortament:
    if item.c1 >= 10 and item.c2 >= 10 and  item.c1 <= 60 and item.c2 <= 60 and item.r1 >= 1 and item.r2 >= 1 and item.r3 <= 10:
        sortament_filtered_stringers.append(item)

sortament_filtered_frames : List[Type]= []
for item in sortament:
    if item.c1 >= 20 and item.c2 >= 50 and item.c1 <= 60 and item.c2 <= 200 and item.r1 >= 1 and item.r2 >= 1 and item.r3 <= 10:
        sortament_filtered_frames.append(item)

sortament_filtered_stringers.sort(key= lambda x : x.S)
sortament_filtered_frames.sort(key= lambda x : x.S)


i=1
while i < len(sortament_filtered_stringers):
    current = sortament_filtered_stringers[i]
    previous = sortament_filtered_stringers[i - 1]
    if current.J < previous.J:
        sortament_filtered_stringers.pop(i)
    else:   
        i+=1

i=1
while i < len(sortament_filtered_frames):
    current = sortament_filtered_frames[i]
    previous = sortament_filtered_frames[i - 1]
    if current.J < previous.J:
        sortament_filtered_frames.pop(i)
    else:   
        i+=1      

js_str = ""
js_str = json.dumps([ob.__dict__ for ob in sortament_filtered_stringers])
js_str = js_str.replace("}, {", "},\n {")
js_str = js_str.replace(" 0,", " 0.0,")

with open(r"c:\Production\Sortament\Sortament_L_and_Z_stringers.json", 'w', encoding='utf-8') as file:
    file.write(js_str)

js_str = ""
js_str = json.dumps([ob.__dict__ for ob in sortament_filtered_frames])
js_str = js_str.replace("}, {", "},\n {")
js_str = js_str.replace(" 0,", " 0.0,")

with open(r"c:\Production\Sortament\Sortament_L_and_Z_frames.json", 'w', encoding='utf-8') as file:
    file.write(js_str)

c1_range = np.arange(20, 60, 1).tolist()
c2_range = np.arange(20, 50, 1).tolist()
r_range = np.arange(1, 10, 0.2).tolist()
frame_sortament_v2 : List[type] = []
for c1 in c1_range:
    for c2 in c2_range:
        for r in r_range:
            type = Type(round(float(c1), 2), round(float(c2), 2), round(float(c1), 2),
                         round(float(r), 2), round(float(r), 2), round(float(r), 2))
            type.S = round(S_str(type.c1,type.c2, type.c3, type.r1, type.r2, type.r3 ), 2)
            type.J = round(JzZetik(type.c1,type.c2, type.c3, type.r1, type.r2, type.r3 ) + \
                  S_str(type.c1,type.c2, type.c3, type.r1, type.r2, type.r3 )
                  *(Y_CT_Z(type.c1,type.c2, type.c3, type.r1, type.r2, type.r3 )**2), 2 )      
            frame_sortament_v2.append(type)

# for i in range 
frame_sortament_v2.sort(key=lambda x: x.S)
i=1
while i < len(frame_sortament_v2):
    current = frame_sortament_v2[i]
    previous = frame_sortament_v2[i - 1]
    if current.J < previous.J:
        frame_sortament_v2.pop(i)
    else:   
        i+=1

js_str = ""
js_str = json.dumps([ob.__dict__ for ob in frame_sortament_v2])
js_str = js_str.replace("}, {", "},\n {")
js_str = js_str.replace(" 0,", " 0.0,")

with open(r"c:\Production\Sortament\frame_sortament_v2.json", 'w', encoding='utf-8') as file:
    file.write(js_str)
print('done')

    # for line in input_file:
    #     line = line.strip()
    #     if line:
    #         output_file.write(line + "\n")