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
    #return "\033[31m%s\033[0m" % input
    return input

def green(input):
    #return "\033[36m%s\033[0m" % input
    return input


def get_stitch_list(path, filelist):
    """ 
    stitchlist items are ((column,row), (x, y), '/path/name_with_extension')

    returns None if something is wrong
    returns stitchlist if everything made sense.
    """

    stitchlist = []
    for i in filelist:
        strname = str(i[:])
        filepath = path + strname
        
        # disect filename, get dimensions
        match = re.search('\_(\d+\_\d+)\.', filepath)

        try:
            match.group()
        except:
            print('found malformed filename [%s] in folder!' % red(strname))
            print("your filenames should be formatted like:")
            print("yourfilename_col_row.extention")
            print("if still issues, check/remove uncommon characters from path")
            return
        
        match_str = match.group(1)
        db = Image.open(filepath)

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


def get_filelist(path, input_format):
    os.chdir(path) # set this folder active

    mycurdir = os.getcwdu()
    filelist = os.listdir(mycurdir) 
    filelist = sorted(filelist)
    filelist = [file for file in filelist if file.endswith(input_format)]

    if len(filelist) == 0:
        print(red('no files found - come on luke!'))
        return

    return filelist


def correct_path(path):
    if not path.endswith('/'):
        path += '/'
    return path


def unsupported(inputMIME, outputMIME):
    supported_types = ["TIFF", "PNG", "JPEG", "GIF", "BMP"]
    if not (inputMIME and outputMIME in supported_types):
        return True

    return False



# -- master functions

def stitch(path, filetypes):
    inputMIME, outputMIME = filetypes.split(' ')
    
    # extra check before bothering.
    if unsupported(inputMIME.upper(), outputMIME.upper()):
        return

    input_format = '.' + inputMIME.lower()
    output_format = outputMIME.upper()
    path = correct_path(path)
    
    filelist = get_filelist(path, input_format)
    if filelist == None:
        return
    
    stitchlist = get_stitch_list(path, filelist)
    if stitchlist == None:
        return

    # starts stitching process here.

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

    output_filename = 'composite' + '.' + output_format.lower()
    comp_image.save(path + output_filename, format=output_format)



def help_string():

    lazy_usage = red('python autostitcher.py -d -c PNG PNG')

    hasl_usage = red('python autostitcher.py /filepath/ -c PNG PNG')

    full_help = """\
    \n\n
    Two ways to use this beast:

    %(lazy_usage)s
    - attempts to stitch the content of the folder that contains this script.
    
    %(hasl_usage)s
    example: python autostitcher.py /home/username/somefolder/ -c PNG PNG
    - attempts to stitch the content of the supplied path 
    \n\n
    At present the script only supports TIFF/PNG/JPEG/GIF/BMP.

    In addition, you can modifiy the script to output RGBA but only for PNG out.
    http://infohost.nmt.edu/tcc/help/pubs/pil/formats.html        

    You must have no stray (or already composited) files in the directory
    """ % vars()

    return full_help



def main(args):

    if len(args) > 1:
        argument = ' '.join(args[1:])
        argument, filetypes = argument.split(' -c ')
                
        if argument == '-d':
            print('will attempt stitching image content of current directory')
            stitch(os.getcwd(), filetypes)
            return
        
        if os.path.isdir(argument):
            print('destination directory seems valid, will attempt stitch')
            stitch(argument, filetypes)
            return
        else:
            print(red(argument + ' is not a valid directory or argument'))

    print(help_string())
    return


if __name__ == '__main__':
    main(sys.argv)
    

    
    