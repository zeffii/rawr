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
    
    num_paths_found = len(properly_split)

    # i'm not to sure about what the first portion does, but 
    # the part after 1.0, 1.0, 1.0 seems to be coordinates. up to 0.0, 1.0

    print('%(num_paths_found)s paths found' % vars())





    return properly_split



def main():

    result = get_raw_data(filename)
    if result == None:
        print('file doesn\'t appear to be at given location')
        return
    else:
        h, pdc, pd = split_into_fields(result)
        path_list = split_into_individual_paths(pd)
        # generate_paths_from_list(path_list)
        for i in path_list[:20]:
            print(i)
            print('---------')

        return

main()
