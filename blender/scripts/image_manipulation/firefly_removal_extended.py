import bpy
import time

"""
pep8 > relating to one-line if-statements is ignored for short lines.
zen  > flat rather than nested, no serious logic is deeply nested.
zen  > pretty complex but not very complicated

some conventions:
    rc  = coordinate
    co  = coordinate
    rcs = coordinates
    idx = index (refers only to the converted dm from img.pixels)
"""

high_firefly_count_text = """\
\t: anything over 200 pixels is probably an indication of a lightsource pointing
\t: at the camera directly or via mirrors."""


DEBUG = False
INTERACTIVE = True
ERROR = True
STRICT = True


# matrix representation, everything pivots around e
a, b, c = [+1,-1], [+1, 0], [+1,+1] 
d, e, f = [0, -1], [0,  0], [0, +1] 
g, h, i = [-1,-1], [-1, 0], [-1,+1]  

# all sides surrounded by sample-able pixels
rest_list =     [a, b, c, f, i, h, g, d]

# from the indication of which of the 4 sides the pixel
# is on, this will return the list of pixels to sample    
sides = {
    'top':      [f, i, h, g, d],
    'bottom':   [d, a, b, c, f],
    'left':     [b, c, f, i, h],
    'right':    [h, g, d, a, b]
}


# ------helpers-----------------------------------------------------------------


def side(r, c, w, h):
    """ helps find side, else returns None by default """
    if r == 0: return 'bottom'
    if r == h-1: return 'top'
    if c == 0: return 'left'
    if c == w-1: return 'right'



def is_bright(rgba):
    sum_to_true = [True for i in rgba if i >= .97]        
    if len(sum_to_true) == 4:
        return True



def idx_to_co(idx, width):
    """ helps translate index of pixel into 2d coordinate """
    r = int(idx / width)
    c = idx % width
    return r, c



def co_to_idx(r, c, width):
    return r*width+c



def rgba_from_index(idx, dm):
    """
    idx:    a pixel, idx*4 is its index in the flat dm list
    dm:     a flat sequence of ungrouped floats, every 4 floats is one rgba
    """
    start_raw_index = idx * 4
    return dm[start_raw_index:start_raw_index+4]



def mix_rgba_from_list(colors_pre_mix):
    col_avg = []
    num_colors = len(colors_pre_mix) 
    for component in range(len(colors_pre_mix[0])):
        component_summed = 0
        for i in range(num_colors):
            component_summed += (colors_pre_mix[i][component])
        col_avg.append(float(component_summed / num_colors))
        
    return col_avg



def return_coordinates(r, c, surrounder_list):
    """ takes surrounder_list from the sides dictionary or the rest_list """
    return [(r+i[0],c+i[1]) for i in surrounder_list]



def coordinates_in_corner(r, c, w, h):
    corner_dict = {
        (0,0):     [(+1,  0), (+1,  +1), (0,  +1)],
        (0,w-1):   [(0, w-2), (+1, w-2), (+1,w-1)],
        (h-1,0):   [(h-1, 1), (h-2,  1), (h-2, 0)],
        (h-1,w-1): [(h-2,w-1),(h-2,w-2),(h-1,w-1)]
    }    

    if (r,c) in corner_dict:
        return True, corner_dict[(r, c)]
    else:
        return None, None



def get_surrounding_rc_from_index(r, c, w, h):
    """ surrounding row column coordinates given the current coordinate """
        
    in_corner, corner_list = coordinates_in_corner(r, c, w, h)
    
    if in_corner:
        color_coordinates = corner_list

    elif side(r ,c ,w, h) in sides:
        found_side = side(r ,c ,w, h)
        surround_list = sides[found_side]
        color_coordinates = return_coordinates(r, c, surround_list)

    else:
        color_coordinates = return_coordinates(r, c, rest_list)
    
    return color_coordinates


# --------main------------------------------------------------------------------


def remove_fireflies(nested2D, idx_list, img):
    """ all sampling is clockwise """

    def get_color_list_from_coordinates(r, c, color_coordinates):
        """ first get colors, except white """            
        
        if DEBUG: print(color_coordinates)

        colors = [nested2D[co[0]][co[1]] for co in color_coordinates]
        colors_pre_mix = [rgba for rgba in colors if not is_bright(rgba)]

        if len(colors_pre_mix) == 0:
            # this coordinate seems to have all bright surrounding.
            # return pixel colour unchanged
            return nested2D[r][c]
        else:
            return colors_pre_mix

    
    w = width = img.size[0]
    h = height = img.size[1]

    """ for every pixel in idx_list check the neighbours """
    for idx in idx_list:
        r,c = idx_to_co(idx, w)
        color_rcs = get_surrounding_rc_from_index(r, c, w, h)
        color_list_pre_mix = get_color_list_from_coordinates(r, c, color_rcs)        

        # could take dominant colour direction into account..but doesn't
        color_average = mix_rgba_from_list(color_list_pre_mix)
        nested2D[r][c] = color_average

    return nested2D



def is_firefly(idx, img, dm):
    """ this checks the bounding pixels and returns 
    true if they are not all bright"""
    w = width = img.size[0]
    h = height = img.size[1]
    
    # where is this pixel?
    r, c = idx_to_co(idx, width)
    
    # what are its surrounding coordinates?    
    co_list = get_surrounding_rc_from_index(r, c, w, h)
    
    # what are surrounding colors?
    colors_pre_mix = []
    for _r, _c in co_list:
        _idx = co_to_idx(_r,_c, w)
        rgba = rgba_from_index(_idx, dm)
        colors_pre_mix.append(rgba)
    
    # enforces to be considered a firefly the
    # pixel must be touching no other pixels
    if STRICT:
        for found_rgba in colors_pre_mix:
            if is_bright(found_rgba):
                return False
        
    
    # when the compounded colours are all bright, then this is not a firefly.
    avg_rgba = mix_rgba_from_list(colors_pre_mix)
    return not is_bright(avg_rgba)
    


def make_firefly_list(dm, img):
    """ find and index non engulfed bright pixels """
    if INTERACTIVE: print('> analyzing image ', end='')
        
    firefly_count = 0
   
    idx_list = []
    for idx, pos in enumerate(range(0,len(dm),4)):
        rgba = dm[pos:pos+4]
        if is_bright(rgba) and is_firefly(idx, img, dm):
            firefly_count += 1
            idx_list.append(idx)
   
    if len(idx_list) == 0: return []
    
    if INTERACTIVE: 
        print("> found %d possible fireflies" % firefly_count)
        if firefly_count > 200: 
            print(high_firefly_count_text)
        
    return idx_list



def fix_fireflies(img, idx_list, dm):
    """ make 1D and then 2d list for convenience, returns a dm """
    w = width = img.size[0]
    
    # turn into 2d grid
    nested1D = [dm[i:i+4] for i in range(0, len(dm), 4)]
    nested2D = [nested1D[i:i+width] for i in range(0, len(nested1D), w)]
    
    # return modified grid
    nested2D = remove_fireflies(nested2D, idx_list, img)
    
    # return flattened sequence
    nested1D = [col for row in nested2D for col in row]
    return [comp for px in nested1D for comp in px]


# -------user interaction ------------------------------------------------------


def image_doctor(image_name):
    D = bpy.data
    
    if INTERACTIVE:
        tm = time.localtime()
        current_time =  ' %d:%d:%d ' % (tm.tm_hour, tm.tm_min, tm.tm_sec)
        time_bar = '{:-^80}'.format(current_time)
        print(time_bar)
        print('> strict mode on')
        
    if image_name in D.images:

        if INTERACTIVE: 
            print('\n> found file ',end='')
        
        img = image_object = D.images[image_name]
        dm = [i for i in img.pixels]
        
        """ find and index all near white """
        idx_list = make_firefly_list(dm, img)
        num_flies = len(idx_list)
        if not num_flies == 0:

            if INTERACTIVE and num_flies > 200:
                print('\n\t: Can take 20 seconds on a 2core 2.4ghz')
                print('\t: overexposed images will be slower')
                print('\n> processing.')

            img.pixels = fix_fireflies(img, idx_list, dm)
            
            if not INTERACTIVE:
                img.save()
            else:
                print('> done.')
                print('\nClick in the Image Editor to preview.', end='')
                print(' Save if satisfied')
    
        else:
            if INTERACTIVE: print('no updates')
            return
    
    else:
        
        if not INTERACTIVE: return 
        
        print('couldn\'t find: ' + image_name)
        images = D.images[:]
        num_images = len(images)

        if num_images > 0:
            print('try: \t')
            for idx, tp in enumerate(images):
                jumble = '\t' + str(idx) + ' > ' + tp.name
                print(jumble)

            q = '\nPress any number to load, or anything else to cancel > '
            a = input(q)

            if a.isnumeric():
                a = int(a)
                if a in range(num_images):
                    image_doctor(images[a].name) 
    
        print('> script terminated')    
        
image_doctor('your_image.ext')
# image_doctor('firefly_test_pattern2.tga')