# gimp 2.8 rc1 only.
# import everything, this feels wrong.
from gimpfu import *
import re

# user must first preload all images as layers.

def get_dimensions_from_imagename(input_name):
    # matches last 2 digit clusters of a filename
    print(input_name)
    match = re.search('_(\d+_\d+)\.', input_name)

    if match != None:
        match_str = match.group(1)
        col_row = tuple(match_str.split("_"))
        return [int(dim) for dim in col_row]
    else:
        return
        

def main_process(final_string_name):
    # be sure to have only 1 instance of GIMP open with one image
    if len(gimp.image_list()) > 1: 
        return

    gimg = gimp.image_list()[0]
    num_layers = len(gimg.layers)
    print('number of images to stitch: %d' % num_layers)
    
    # only need details of last image
    last_layer = gimg.layers[-1]
    response = get_dimensions_from_imagename(last_layer.name)

    if response != None:
        cols, rows = response
    else:
        print('didn\'t find suitable filenames')
        return

    # composite dimensions
    w = cols * last_layer.image.width
    h = rows * last_layer.image.height
    
    print('cols: %d \trows: %d' % (cols, rows))
    print(w, h)
    gimg.resize(w, h, 0, 0)
    
    for idx in range(num_layers):
        layer_info = gimg.layers[idx].name
                
        c, r = get_dimensions_from_imagename(layer_info)
        c, r = c-1, r-1
        x_trans = c * last_layer.width
        y_trans = r * last_layer.height
        
        print('translate:', layer_info, 'x=',x_trans, ' y=',y_trans)
        gimg.layers[idx].translate(x_trans, y_trans)

    gimg.flatten()


register(
    "python_fu_stitcher",
    "image stitcher",
    "image stitcher",
    "Author", 
    "Author Again", 
    "2012",
    "Image Composite",
    "",

    [
    (PF_STRING, "string", "String", "output_name")],
    [],
    main_process, menu="<Image>/File/Create" )


main()