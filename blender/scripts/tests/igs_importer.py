# early prototype of igs / iges importer
# import bpy

"""
supported entities 

B-Splines (Entity type 126) 

NOT # Parametric Splines (Entity type 112) 

"""

filename = 'siggraphSpacecraft70.igs'

def makeDiv(input):
    return input.center(80, '-')


def get_raw_data(filename):
    try:
        file_in_mem = open(filename)
    except:
        return

    # strips newlines while appending to lines list.
    lines = []
    for line in file_in_mem:
        lines.append(line[:-1])

    return lines


def split_into_fields(lines):
    """
    incoming data is the igs file as a list with newlines removed.

    there are three distinct states for this file
        - header
        - patch declarations
        - patch data

    first sate starts with characters
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
            patch_data.append(line)            

    return h, pdc, pd



def main():

    result = get_raw_data(filename)
    if result == None:
        print('file doesn\'t appear to be at given location')
        return
    else:
        h, pdc, pd = split_into_fields(result)
        for i in pd[-18:]:
            print(i)
        return

main()
