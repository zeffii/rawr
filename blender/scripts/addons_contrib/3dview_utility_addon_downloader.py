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
[ ] Add download buttons, based on list
[ ] Color Picker
[ ] Extra templates

- 3d view tools
- console
- external
"""


import bpy
from bpy.props import BoolProperty
from bpy.types import Operator

import os
import shutil
import json
from urllib.request import urlopen
import base64


github = "https://api.github.com/repos/"
zeffii = github + "zeffii/rawr/contents/blender/scripts/addons_contrib"
mrdoob = github + "mrdoob/three.js/contents/utils/exporters/blender/2.63/scripts/addons"

powertools_constants = lambda: None
powertools_constants.prefixes = {
    'v3d': "3d View tools",
    'text': "Text Editor",
    'term': "Console",
    'xt': "External Utils"

}

powertools_constants.dl_mapping = {
    'v3d_dl_add_keymaps': zeffii + '/interface_add_keymaps',
    'v3d_dl_add_vert': zeffii + '/add_mesh_vertex_object',
    'v3d_dl_add_empty': zeffii + '/mesh_place_empty',
    'v3d_dl_add_sum': zeffii + '/mesh_edge_sum',
    'text_dl_add_searchutils': zeffii + '/text_editor_extras',
    'text_dl_gist_tools': zeffii + '/text_editor_gists',
    'text_dl_ba_leech': zeffii + '/text_editor_ba_leech',
    'text_dl_syntax_from_text': zeffii + '/text_editor_syntax_pygments',
    'term_dl_console_history_clean': zeffii + '/console_to_script_clean',
    'xt_dl_add_threejs': mrdoob + '/io_mesh_threejs'
}


def nice_format(input_string):
    return input_string.replace('_', ' ').title()


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

        # this enables directly after download.
        bpy.ops.wm.addon_enable(module=main_url.split('/')[-1])

    wjson = get_json_from_url(main_url)
    directory = get_dir_name()
    urls = get_file_tree()
    write_directory()
    print(' : done!')


def short_name(url):
    return '/'.join(url.rsplit('/',2)[-2:])


def directory_exists(dir_to_check):
    scripts_path = bpy.utils.script_paths()[0]
    dir_path_to_check = os.path.join(scripts_path, "addons_contrib", dir_to_check)
    return True if os.path.exists(dir_path_to_check) else False


def main(context, **kw):

    # if boolean switch is true, download from that url
    for k, v in kw.items():
        if v:
            main_url = powertools_constants.dl_mapping[k]
            print(short_name(main_url), end=' ')
            dl_main(main_url)

    print('\nFinished')


class PowerTools(Operator):
    bl_idname = "scene.add_power_tools"
    bl_label = "Power Tools Download Bay"


    for k, v in powertools_constants.dl_mapping.items():
        exec("""{} = BoolProperty(
        name="",
        default=False,
    )\n\n""".format(k))

    def execute(self, context):
        keywords = self.as_keywords()
        main(context, **keywords)
        return {'FINISHED'}


    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=250, height=600)


    def draw(self, context):
        layout = self.layout

        for k, v in powertools_constants.prefixes.items():
            box = layout.box()
            col = box.column()
            col.label(v)

            plugs_found = [i for i in powertools_constants.dl_mapping.keys() \
                                if i.startswith(k)]

            for option in plugs_found:

                row = col.row()
                split = row.split(percentage=0.25)
                col_int = split.column()

                plugin_uri = powertools_constants.dl_mapping[option]
                plugin_uri = plugin_uri.split('/')[-1]

                DIR_EXISTS = directory_exists(plugin_uri)
                if plugin_uri in bpy.context.user_preferences.addons.keys():
                    if DIR_EXISTS:
                        col_int.prop(self, option, icon='FILE_TICK', text="")
                    else:
                        col_int.prop(self, option, icon='X_VEC', text="")
                elif DIR_EXISTS:
                    col_int.prop(self, option, icon='FILE_FOLDER', text="")
                else:
                    col_int.prop(self, option, icon='URL', text="")

                split = split.split()
                col_int = split.column()
                col_int.label(nice_format(plugin_uri))


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