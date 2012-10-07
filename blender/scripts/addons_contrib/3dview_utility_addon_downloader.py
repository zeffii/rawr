# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you may redistribute it, and/or
# modify it, under the terms of the GNU General Public License
# as published by the Free Software Foundation - either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, write to:
#
#   the Free Software Foundation Inc.
#   51 Franklin Street, Fifth Floor
#   Boston, MA 02110-1301, USA
#
# or go online at: http://www.gnu.org/licenses/ to view license options.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "zeffii power tools",
    "author": "zeffii",
    "version": (0, 1, 0),
    "blender": (2, 6, 4),
    "location": "3dview -> Search -> Power Tools Download bay",
    "description": "Adds a downloader utility to the search bar path",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Addon Installer"}



"""

- text editor tools -
[x] Add download buttons, based on list
[x] Search Utils 
[x] Gist Tools 
[x] Ba Leech tool 
[ ] Color Picker
[ ] Extra templates
[x] add syntax objects from text

- 3d view tools
[x] add 3dview keymap button
[x] add object vertex at cursor
[x] add empty at selected
[x] measure selected edges

- console
[x] copy cleaned history

- external
[x] threejs leecher


"""


import bpy
from bpy.props import BoolProperty
from bpy.types import Operator

import os
import shutil
import json
from urllib.request import urlopen
import base64


def dl_main(main_url):

    def get_json_from_url(url):
        """ get json from url and return in query-able form """
        found_json = urlopen(url).readall().decode()
        jfile = json.JSONDecoder()
        return jfile.decode(found_json)

    def get_dir_name():
        """ the main url ends in the directory name, this returns it """
        return main_url.rsplit('/')[-1]

    def get_file_tree():
        """ get the list of urls for the files contained in the directory """
        get_b64str = lambda x: x.get('_links').get('self')
        valid_file = lambda x: not x.get('name') == '__pycache__'
        return [get_b64str(x) for x in wjson if valid_file(x)]

    def get_file(url):
        """ get the bytes-object and file name from the url """
        wjson = get_json_from_url(url)
        file_name = wjson.get('name')
        sb64 = wjson.get('content')
        return base64.decodebytes(bytes(sb64, 'utf-8')), file_name

    def write_file_from_url(url):
        """ given a url to a base64 encoded file, writes the file to disk """
        bytes_content, file_name = get_file(url)
        with open(file_name, 'wb') as wfile:
            wfile.write(bytes_content)

    def write_directory():
        """ make dir and call write_file_from_url() for each valid url """
        system_cwd = os.getcwd()

        #basic assumption here, that the first path found is sufficient
        scripts_path = bpy.utils.script_paths()[0]
        working_dir = os.path.join(scripts_path, "addons_contrib")
        os.chdir(working_dir)

        if os.path.exists(directory):
            shutil.rmtree(directory)

        os.mkdir(directory)
        os.chdir(directory)

        for url in urls:
            write_file_from_url(url)        

        # restore, might not be needed.
        os.chdir(system_cwd)

    wjson = get_json_from_url(main_url)
    directory = get_dir_name()
    urls = get_file_tree()
    write_directory()
    print(' : done!')


def short_name(url):
    return '/'.join(url.rsplit('/',2)[-2:])


def main(context, **kw):

    github = "https://api.github.com/repos/"
    zeffii = github + "zeffii/rawr/contents/blender/scripts/addons_contrib"
    mrdoob = github + "mrdoob/three.js/contents/utils/exporters/blender/2.63/scripts/addons"


    dl_mapping = {
        'dl_add_keymaps': zeffii + '/interface_add_keymaps',
        'dl_add_vert': zeffii + '/add_mesh_vertex_object',
        'dl_add_empty': zeffii + '/mesh_place_empty',
        'dl_add_sum': zeffii + '/mesh_edge_sum',
        'dl_add_searchutils': zeffii + '/text_editor_extras',
        'dl_gist_tools': zeffii + '/text_editor_gists',
        'dl_ba_leech': zeffii + '/text_editor_ba_leech',
        #'dl_extra_templates': zeffii + ,
        'dl_syntax_from_text': zeffii + '/text_editor_syntax_pygments',
        'dl_console_history_clean': zeffii + '/console_to_script_clean',
        'dl_add_threejs': mrdoob + '/io_mesh_threejs'
    }

    # if boolean switch is true, download from that url
    for k, v in kw.items():
        if v:
            main_url = dl_mapping[k]
            print(short_name(main_url), end=' ')
            dl_main(main_url)

    print('\nFinished')


class PowerTools(Operator):
    bl_idname = "scene.add_power_tools"
    bl_label = "Power Tools Download Bay"


    dl_add_keymaps = BoolProperty(
        name="Add Keymaps",
        default=True,
        )

    dl_add_vert = BoolProperty(
        name="Add Vert",
        default=False,
        )

    dl_add_empty = BoolProperty(
        name="Add Empty",
        default=True,
        )

    dl_add_sum = BoolProperty(
        name="Add Sum",
        default=False,
        )

    dl_add_searchutils = BoolProperty(
        name="Add Searchutils",
        default=True,
        )

    dl_gist_tools = BoolProperty(
        name="Gist Tools",
        default=True,
        )

    dl_ba_leech = BoolProperty(
        name="Ba Leech",
        default=False,
        )

    # dl_extra_templates = BoolProperty(
    #     name="Extra Templates",
    #     default=True,
    #     )

    dl_syntax_from_text = BoolProperty(
        name="Syntax From Text",
        default=False,
        )

    dl_add_threejs = BoolProperty(
        name="Add Threejs",
        default=False,
        )

    dl_console_history_clean = BoolProperty(
        name="Console History (as clean script)",
        default=False,
        )

    def execute(self, context):
        keywords = self.as_keywords()
        main(context, **keywords)
        return {'FINISHED'}


    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)


    def draw(self, context):
        layout = self.layout
        
        # will do:  console_history_using_copy_as_script.py

        dl_options = {  
            "3d View tools": [  "dl_add_keymaps", 
                                "dl_add_vert", 
                                "dl_add_empty", 
                                "dl_add_sum"],

            "Text Editor": [    "dl_add_searchutils", 
                                "dl_gist_tools", 
                                "dl_ba_leech", 
                                #"dl_extra_templates", 
                                "dl_syntax_from_text"],

            "Console": ["dl_console_history_clean"],

            "External Utils": ["dl_add_threejs"]
        }

        for k, v in dl_options.items():
            box = layout.box()
            col = box.column()
            col.label(k)
            for option in v:
                row = col.row()
                row.prop(self, option)




def menu_func(self, context):
    layout = self.layout
    layout.label("power tools")
    layout.operator("scene.add_power_tools", text="Open Downloader Console")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_PT_tools_objectmode.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_PT_tools_objectmode.remove(menu_func)


if __name__ == "__main__":
    register()
