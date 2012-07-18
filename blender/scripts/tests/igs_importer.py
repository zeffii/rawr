# early prototype of igs / iges importer
# import bpy
import re
"""
possible entities:
http://help.solidworks.com/2011/English/SolidWorks/
sldworks/LegacyHelp/Sldworks/ImpExp/IGES_Entity_Types.htm

supported entities 
B-Splines (Entity type 126) 


"""

filename = 'siggraphSpacecraft70.igs'

def makeDiv(input):
    return input.center(80, '-')


def get_raw_data(filename):
    try:
        # file_in_mem = open(filename)
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
            if line[0] is not ' ':
                header.append(line)
            else: 
                STATE = 2

        if STATE == 2:
            if line[0] is ' ':
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

    for path in path_list:
        if path[0] not in valid_path_types:
            print(path[0], 'has not been implemented yet')
            continue
        else:
            if path[0] == '126':
                bspline_type = path[1]
                if bspline_type == '3':
                    current_path = path[19:-5]
                    cp = [float(i) for i in current_path]
                    cp = [tuple(cp[i:i+3]) for i in range(0, len(cp), 3)]
                    BSplines.append(cp)
                    print('3')
                    print(cp)
                    print(len(cp))
                elif bspline_type == '5':
                    print('bspline v5 not handled yet')
                    continue
                    # current_path = path[22:-5]
                    # BSplines.append(current_path)
                    # print('5')
                    # print(current_path)
                else:
                    print('BSpline with unhandled content: ' + bspline_type)

            print('---------')

    return BSplines


def main():

    result = get_raw_data(filename)
    if result == None:
        print('file doesn\'t appear to be at given location')
        return
    else:
        h, pdc, pd = split_into_fields(result)
        path_list = split_into_individual_paths(pd)
        generate_paths_from_list(path_list)
    return


main()
