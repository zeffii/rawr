import bpy
import re
"""
possible entities:
http://help.solidworks.com/2011/English/SolidWorks/
sldworks/LegacyHelp/Sldworks/ImpExp/IGES_Entity_Types.htm

supported entities 
B-Splines (Entity type 126) 

early prototype of igs / iges importer
"""
# tested on 
# filename = 'siggraphSpacecraft70.igs'

filename = 'siggraphSpacecraft22.igs'
filename = '/home/zeffii/Downloads/igs_siggraph/' + filename

def makeDiv(input):
    return input.center(80, '-')


def get_raw_data(filename):
    try:
        file_in_mem = open(filename)
    except:
        return

    lines = []
    for line in file_in_mem:
        lines.append(line)

    # be explicit
    file_in_mem.close()
    return lines


def split_into_fields(lines):
    """
    there are three distinct states for this file
        - header
        - patch declarations
        - patch data

    first state starts with characters
    second state starts with spaces
    third state starts with characters again
        - it is easy to split them on this idea alone.

    """
    print(makeDiv('content'))

    # alias to keep the return statement readable
    h = header = []
    pdc = patch_declarations = []
    pd = patch_data = []
    
    STATE = 1
    for line in lines:
        if STATE == 1:
            if not line[0] == ' ':
                header.append(line)
            else: 
                STATE = 2

        if STATE == 2:
            if line[0] == ' ':
                patch_declarations.append(line)
            else:
                STATE = 3

        if STATE == 3:
            # slightly verbose, for readability.
            if ';' in line:
                line_separated = line.split(';')
                line = line_separated[0] + ';'

            if ', ' in line:
                line_separated = line.split(', ')
                line = line_separated[0] + '\n'
            
            patch_data.append(line)

    return h, pdc, pd

def split_into_individual_paths(pd):
    # strip off the last line
    pd = pd[:-1]

    # join file-lines that represent one path, split on semicolon
    joined_list = ''.join(pd)
    joined_list = re.sub(' {2,}', ' ', joined_list)
    joined_list = joined_list.replace('\n', ',')

    properly_split = joined_list.split(';')
    
    num_paths_found = str(len(properly_split))
    print(makeDiv(num_paths_found + ' paths found'))

    further_split = []
    for entity in properly_split:
        if ',' in entity:
            further_split.append(entity.split(','))

    return further_split


def generate_paths_from_list(path_list):
    """
    my understanding from the siggraph test files is now:
    - the first integer is the entity type
    - followed by six integers (the first of which can be either 5 or 3)
    - followed by 8 float (4 times 2 different values)
    - followed by 4 or 6 weighted floats 
        - if element 2 is a 3 then 4 weighted floats
        - if element 2 is a 5 then 6 weighted floats

    """
    valid_path_types = ('126')

    BSplines = []

    def get_bspline(path, _from, _to):
        current_path = path[_from: _to]
        cp = [float(i) for i in current_path]
        iteration_list = list(range(0, len(cp), 3))
        cp = [tuple(cp[i:i+3]) for i in iteration_list]
        return cp


    for path in path_list:
        if path[0] not in valid_path_types:
            print(path[0], 'has not been implemented yet')
            continue
        else:
            if path[0] == '126':
                
                # looks like a pattern has developed! 
                # 126, n, 3
                # 126, 1, 1
                #
                
                bspline_type = path[1]
                if bspline_type == '1':
                    cp = get_bspline(path, 13, -5)

                elif bspline_type == '3':
                    cp = get_bspline(path, 19, -5)

                elif bspline_type == '5':
                    cp = get_bspline(path, 23, -5)

                elif bspline_type == '7':
                    cp = get_bspline(path, 27, -5)
                
                elif bspline_type == '9':
                    cp = get_bspline(path, 31, -5)

                elif bspline_type == '11':                                       
                    cp = get_bspline(path, 35, -5)

                elif bspline_type == '12':                                       
                    cp = get_bspline(path, 37, -5)

                else:
                    print('BSpline with unhandled content: ' + bspline_type)
                    print(path)
                    print('---------')
                    continue
                
                BSplines.append(cp)                



    return BSplines


w = 1 # weight

def MakePolyLine(objname, curvename, cList):    
    curvedata = bpy.data.curves.new(name=curvename, type='CURVE')    
    curvedata.dimensions = '3D'    
    
    objectdata = bpy.data.objects.new(objname, curvedata)    
    objectdata.location = (0,0,0) #object origin    
    bpy.context.scene.objects.link(objectdata)    
    
    polyline = curvedata.splines.new('NURBS')    
    polyline.points.add(len(cList)-1)    
    for num in range(len(cList)):    
        x, y, z = cList[num]
        x, y, z = x/1000.,y/1000.,z/1000.
        polyline.points[num].co = (x, y, z, w)    
    
    polyline.order_u = len(polyline.points)-1  
    polyline.use_endpoint_u = True  
      



def main():

    result = get_raw_data(filename)
    if result == None:
        print('file doesn\'t appear to be at given location')
        return
    else:
        h, pdc, pd = split_into_fields(result)
        path_list = split_into_individual_paths(pd)
        BSplines = generate_paths_from_list(path_list)
        
        for idx, spline in enumerate(BSplines):
            id_num = str(idx).zfill(4)
            object_name = 'Obj_named_' + id_num
            curve_name = 'Curve_named_' + id_num
            MakePolyLine(object_name, curve_name, spline) 
    return


main()


    
