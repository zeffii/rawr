# import bpy

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
        - patch declaration
        - patch data

    first sate starts with characters
    second state starts with spaces
    third state starts with characters again
        - it is easy to split them on this idea alone.
    """
    print(makeDiv('yay'))


def main():

    result = get_raw_data(filename)
    if result == None:
        print('file doesn\'t appear to be at given location')
        return
    else:
        split_into_fields(result)
        return

main()
