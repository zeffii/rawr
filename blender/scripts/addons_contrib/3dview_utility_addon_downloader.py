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
import re
import shutil
from urllib.request import urlopen
from urllib.request import urlretrieve

def dl_main(main_url):

    def make_raw(i):
        removed = i.split('/')[5:]
        chunks = ["https://raw.github.com", user_name, project, branch] 
        raw_url = '/'.join(chunks + [i for i in removed])
        return raw_url

    def get_details(main_url):
        user_name, project, _, branch = main_url.split('/')[3:7]
        directory = main_url.split('/')[-1]
        return user_name, project, branch, directory

    def get_valid_urls(results):
        urls = [make_raw(i) for i in results if user_name in i]
        return [i for i in urls if not i.endswith(branch)]

    def write_directory(directory, urls):
        system_cwd = os.getcwd()
        
        #basic assumption here, that the first path found is sufficient
        working_dir = os.path.join(bpy.utils.script_paths()[0], "addons_contrib")
        os.chdir(working_dir)
        print('current working directory: {}'.format(os.getcwd()))

        if os.path.exists(directory):
            shutil.rmtree(directory)

        os.mkdir(directory)
        os.chdir(directory)
        print('current working directory: {}'.format(os.getcwd()))

        for url in urls:
            file_name = url.split('/')[-1]
            urlretrieve(url, file_name)            

        # restore, might not be needed.
        os.chdir(system_cwd)


    user_name, project, branch, directory = get_details(main_url)

    print('getting {}'.format(main_url))

    p = urlopen(main_url)
    x = p.read().decode('utf-8')

    pattern = re.compile(r'<a href="(.*?\.[a-z]{2,3})"')
    results = pattern.findall(x)
    valid_urls = get_valid_urls(results)

    for i in valid_urls:
        print('downloading: ....', i[-40:])

    write_directory(directory, valid_urls)
    print('done!\n#####')



def main(context, **kw):

    github = "https://github.com/"
    zeffii = github + "zeffii/rawr/tree/master/blender/scripts/addons_contrib"
    mrdoob = github + "mrdoob/three.js/tree/master/utils/exporters/blender/2.63/scripts/addons"

    dl_mapping = {
        'dl_add_keymaps': zeffii + "/interface_add_keymaps",
        'dl_add_vert': zeffii + "/add_mesh_vertex_object",
        'dl_add_empty': zeffii + "/mesh_place_empty",
        'dl_add_sum': zeffii + "/mesh_add_sum",
        'dl_add_searchutils': zeffii + '/text_editor_extras',
        'dl_gist_tools': zeffii + '/text_editor_gists',
        'dl_ba_leech': zeffii + '/text_editor_ba_leech',
        #'dl_extra_templates': zeffii + ,
        'dl_syntax_from_text': zeffii + "/text_editor_syntax_pygments",
        'dl_console_history_clean': zeffii + "/console_to_script_clean",
        'dl_add_threejs': mrdoob + '/io_mesh_threejs'
    }

    # if boolean switch is true, download from that url
    for k, v in kw.items():
        if v:
            main_url = dl_mapping[k]
            dl_main(main_url)

    print('Finished')


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
        name="Add pygments plugin",
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
