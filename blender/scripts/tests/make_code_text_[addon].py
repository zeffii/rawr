try:
    import pygments
except:
    import sys
    sys.path.append('/usr/local/lib/python3.2/site-packages/')

import bpy
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import RawTokenFormatter
import re

# License MIT, (c) Dealga McArdle 2012 
# blenderscripting.blogspot

# ----------------- helpers

line_height = 0.9

source_path = "/home/zeffii/Desktop/typeFACE/"
source_dir = source_path + "SourceCodePro_FontsOnly-1.009/"

font_family = {
    'bold': "SourceCodePro-Bold",
    'regular': "SourceCodePro-Regular"}

ext = '.ttf'

material_library = {'Name.Namespace': (0.4, 0.4, 0.9, 1.0),
                    'Comment': (0.6, 0.6, 0.6, 1.0),
                    'Name': (0.2, 0.2, 0.2, 1.0),
                    'Keyword': (0.2, 0.8, 0.5, 1.0),
                    'Text': (0.0, 0.0, 0.0, 1.0),
                    'Punctuation': (0.8, 0.8, 0.8, 1.0),
                    'Literal.Number.Integer': (0.9, 0.5, 0.5, 1.0),
                    'Literal.String.Escape': (0.9, 0.2, 0.7, 1.0),
                    'Literal.Number.Float': (0.9, 0.4, 0.6, 1.0),
                    'Operator.Word': (0.9, 0.3, 0.8, 1.0),
                    'Operator': (0.4, 0.8, 0.0, 1.0),
                    'Literal.String': (0.8, 0.4, 0.6, 1.0),
                    'Name.Builtin': (0.2, 0.9, 0.94, 1.0),
                    'Keyword.Namespace': (0.4, 0.6, 0.97, 1.0)}


def print_time_stamp():
    from time import asctime
    print(asctime().center(60, '-'))


def get_unique_sequential_name():
    # if you need more, increase this value it is arbitrary at the moment
    for i in range(10000):
        yield(str(i).zfill(6))


# ----------------- setup fonts and get spacing values


def add_fonts():
    for font_name in font_family.values():
        rel_path = bpy.path.relpath(source_dir + font_name + ext)
        bpy.data.fonts.load(rel_path)


def create_syntax_block(caret, syntax_object):
    # the material happens also to be the name of the syntax element,
    material, content = syntax_object

    bpy.ops.object.text_add(location=(caret.x, caret.y, 0.0))
    f_obj = bpy.context.active_object
    f_obj.name = next(seq_yielder)
    
    if material in ['Literal.String']:
        font_choice = font_family['regular']
    else:
        font_choice = font_family['bold']
    
    f_obj.data.font = bpy.data.fonts[font_choice]
    f_obj.data.body = content
    f_obj.data.materials.append(bpy.data.materials[material])

    # i can't get real information about the length including whitespace
    object_width = .471 * len(content)
    return object_width


# ----------------- materials set up


def make_material(syntax_name, float3):
    col = pymat.new(syntax_name)
    col.use_nodes = True
    Diffuse_BSDF = col.node_tree.nodes['Diffuse BSDF']
    Diffuse_BSDF.inputs[0].default_value = float3


def make_materials(material_library):
    for k, v in material_library.items():
        make_material(k, v)


# ----------------- main worker function


def write_lines(post_split_lines):

    caret = lambda: None
    caret.x = 0.0
    caret.y = 0.0

    TOKEN_RE = """(Token\.(.*?)\t(\'(.*?)\')|Token\.(.*?)\t(\"(.*?)\"))"""

    for i in post_split_lines:
        if '\t' in i:

            pattern = re.compile(TOKEN_RE)
            results = pattern.findall(i)

            for udix in results:
                udix = [i for i in udix if len(i) > 0]
                syntax_name = udix[1]
                syntax_value = udix[2][1:-1]

                print('Token: {}: |{}|'.format(syntax_name, syntax_value))

                # add material if not present
                if not syntax_name in material_library:
                    from random import random
                    random_rgb_float = (0.0, 0.0, round(random(), 4), 1.0)
                    material_library[syntax_name] = random_rgb_float
                    make_material(syntax_name, random_rgb_float)

                syntax_object = syntax_name, syntax_value
                syntax_width = create_syntax_block(caret, syntax_object)
                caret.x += syntax_width

        caret.x = 0.0

        print('----newline')
        caret.y -= line_height


# ----------------- main loop

print_time_stamp()
pymat = bpy.data.materials
make_materials(material_library)
add_fonts()

seq_yielder = get_unique_sequential_name()

# ----------------- make raw data

code = bpy.context.edit_text.as_string()
code_as_raw = highlight(code, Python3Lexer(), RawTokenFormatter())

# ----------------- process data

pre_split_lines = code_as_raw.decode('utf-8')
post_split_lines = pre_split_lines.split(r"""Token.Text '\n'""")

# ----------------- write data

write_lines(post_split_lines)