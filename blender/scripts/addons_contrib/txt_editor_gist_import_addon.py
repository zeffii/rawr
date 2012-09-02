bl_info = {
    "name": "Text Editor Gist Import",
    "author": "Dealga McArdle",
    "version": (0, 1, 0),
    "blender": (2, 6, 4),
    "location": "Text Editor - Download Gist",
    "description": "Given gist id can download and insert file into current blend text.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Text Editor"}


import json
from urllib.request import urlopen

import bpy
from mathutils import Vector
from bpy.props import StringProperty


def get_raw_url_from_gist_id(gist_id):
    gist_id = str(gist_id)
    url = 'https://api.github.com/gists/' + gist_id
    
    found_json = urlopen(url).readall().decode()

    wfile = json.JSONDecoder()
    wjson = wfile.decode(found_json)

    # 'files' may contain several - this will mess up gist name.
    files_flag = 'files'
    file_names = list(wjson[files_flag].keys())
    file_name = file_names[0]
    return wjson[files_flag][file_name]['raw_url']


def get_file(gist_id):
    url = get_raw_url_from_gist_id(gist_id)
    conn = urlopen(url).readall().decode()
    return conn


class ButtonOne(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "scene.dostuff"
    bl_label = "Download given gist from id only"
 
    def execute(self, context):
        gist_id = context.scene.gist_id_property
        
        # could name this filename instead of gist_id for new .blend text.
        bpy.data.texts.new(gist_id)
        bpy.data.texts[gist_id].write(get_file(gist_id))
        print(dir(bpy.data.texts[gist_id]))
        return{'FINISHED'}  


class OperatorPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Download Gist"
    bl_idname = "OBJECT_PT_somefunction"
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_context = "object"
 

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scn = bpy.context.scene

        # display stringbox and download button
        self.layout.prop(scn, "gist_id_property")
        self.layout.operator("scene.dostuff", text='Download to .blend')



def initSceneProperties(scn):
 
    bpy.types.Scene.gist_id_property = StringProperty(
        name = "Gist ID",
        description = "Github Gist ID to download as new internal file",
        default = ""
    )  


initSceneProperties(bpy.context.scene)
classes = [OperatorPanel, ButtonOne]


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)


if __name__ == "__main__":
    register()