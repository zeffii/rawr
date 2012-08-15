# import everything, this feels wrong.
from gimpfu import *
import re

# User must first preload all images as layers,
# this will be slow for larger amounts of images.
# Has been tested up to 144 images / composite 9000px * 12000px png

def get_dimensions_from_imagename(input_name):

    # matches the last two digit clusters of a filename before the 
    # extension.    
    match = re.search('\_(\d+\_\d+)\.', input_name)

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
    
    # only need details of last image. -1 here is only a 
    # formality, .image all refer to the last image added to layers
    # alpabetically.
    last_layer = gimg.layers[-1].image
    response = get_dimensions_from_imagename(last_layer.name)

    if response != None:
        cols, rows = response
    else:
        return

    # composite dimensions
    w = cols * last_layer.width
    h = rows * last_layer.height
    
    print('cols: %d \trows: %d' % (cols, rows))
    print(w, h)

    # rename background image to string of last image (weird!)
    gimg.layers[-1].name = gimg.layers[-1].image.name
      
    for idx in range(num_layers):
        layer_info = gimg.layers[idx].name
                
        c, r = get_dimensions_from_imagename(layer_info)
        c, r = c-1, r-1
        x_trans = c * last_layer.width
        y_trans = r * last_layer.height
        
        print('translate:', layer_info, 'x=',x_trans, ' y=',y_trans)
        gimg.layers[idx].translate(x_trans, y_trans)

    gimg.resize(w, h, 0, 0)
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