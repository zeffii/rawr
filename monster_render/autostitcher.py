#/bin/env python
""" 
commandline stitcher 
run using py 2.6/2.7 and PIL

minor modifcations are required for py3k.

"""

import os
import sys
import re
import PIL
from PIL import Image

# -- helper functions

def red(input):
    return "\033[31m%s\033[0m" % input

def green(input):
    return("\033[36m%s\033[0m" % input)


def get_stitch_list(path, filelist):
    """ 
    stitchlist items are ((column,row), (x, y), '/path/name_with_extension')
    """

    stitchlist = []
    for i in filelist:
        strname = str(i[:])
        filepath = path + strname
        
        # disect filename, get dimensions
        db = Image.open(filepath)
        match = re.search('\_(\d+\_\d+)\.', filepath)
        
        if match.group() != None:
            match_str = match.group(1)
        else:
            print("your filenames should be formatted like:")
            print("yourfilename_col_row.extention")
            print("if still issues, check/remove uncommon characters from path")
            return

        col_row = tuple(match_str.split("_"))
        col_row = [int(dimension) for dimension in col_row]
        stitch_up = (tuple(col_row), db.size, filepath)
        stitchlist.append(stitch_up)
    return stitchlist


def makematrix(rows, columns, stitchlist):
    main_matrix = []
    for i in range(rows):
        minor_matrix = []
        for m in range(columns):
            minor_matrix.append([])
        main_matrix.append(minor_matrix)

    # temporary
    for entry in stitchlist:
        main_matrix[entry[0][0]-1][entry[0][1]-1] = entry[1]

    px_wide = sum([i[0][0] for i in main_matrix])
    px_high = sum([i[1] for i in main_matrix[0]])

    # permanent
    for entry in stitchlist: 
        main_matrix[entry[0][0]-1][entry[0][1]-1] = entry

    print(green("px_wide %(px_wide)s, px_high %(px_high)s" % vars()))
    return main_matrix, px_wide, px_high


# -- master functions

def stitch(path):
    if not path.endswith('/'):
        path += '/'

    input_format = '.' + 'png'
    output_format = 'PNG'
    os.chdir(path) # set this folder active

    mycurdir = os.getcwdu()
    filelist = os.listdir(mycurdir) 
    filelist = sorted(filelist)
    filelist = [file for file in filelist if file.endswith(input_format)]

    if len(filelist) == 0:
        print(red('no files found - come on luke!'))
        return
    
    stitchlist = get_stitch_list(path, filelist)
    if stitchlist == None:
        return

    print('everything seems ok! attempting stitch')
    
    rows = stitchlist[-1][0][0]
    columns = stitchlist[-1][0][1]
    main_matrix, px_wide, px_high = makematrix(rows, columns, stitchlist)

    comp_image = Image.new('RGB', (px_wide, px_high))

    ypos = 0
    xpos = 0
    current_height = 0
    current_width = 0
    for col in main_matrix:
        ypos = 0
        #do top to bottom
        for row in col:
            ymp = Image.open(row[2])
            current_width = row[1][0]
            current_height = row[1][1]
            ymp = ymp.crop((0,0,current_width, current_height))
            comp_image.paste(ymp, (xpos,ypos))
            ypos += current_height
        xpos += current_width

    comp_image.show()
    comp_image.save(path+"composited.png", format=output_format)



def help_string():

    lazy_usage = red('python autostitcher.py -d')

    hasl_usage = red('python autostitcher.py filepath')

    full_help = """\
    \n\n
    Two ways to use this beast:

    %(lazy_usage)s
    - attempts to stitch the content of the folder that contains this script.
    
    %(hasl_usage)s
    example: python autostitcher.py /home/username/somefolder/
    - attempts to stitch the content of the supplied path 
    \n\n        
    """ % vars()

    return full_help



def main(args):

    if len(args) >= 1:
        argument = ' '.join(args[1:])
                
        if argument == '-d':
            print('will attempt stitching image content of current directory')
            stitch(os.getcwd())
            return
        
        if os.path.isdir(argument):
            print('destination directory seems valid, will attempt stitch')
            stitch(argument)
            return
        else:
            print(red(argument + ' is not a valid directory or argument'))

    print(help_string())
    return


if __name__ == '__main__':
    main(sys.argv)
    

    
    