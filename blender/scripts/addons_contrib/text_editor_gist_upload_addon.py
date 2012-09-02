bl_info = {
    "name": "Text Editor Gist Upload",
    "author": "Dealga McArdle",
    "version": (0, 1, 0),
    "blender": (2, 6, 4),
    "location": "Text Editor - Upload Gist",
    "description": "Uploads current blend text as anonymous gist and gives link",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Text Editor"}


import bpy
from bpy.props import StringProperty

import json
from urllib.request import urlopen



def main_function(context, gist_filename, gist_description, gist_body):

    gist_post_data = {  'description': gist_description, 
                        'public': True,
                        'files': {gist_filename: {'content': gist_body}}}

    json_post_data = json.dumps(gist_post_data).encode('utf-8')

    def get_gist_url(found_json):
        wfile = json.JSONDecoder()
        wjson = wfile.decode(found_json)
        gist_url = 'https://gist.github.com/' + wjson['id']
        context.window_manager.clipboard = gist_url

    def upload_gist():
        print('sending')
        url = 'https://api.github.com/gists'
        json_to_parse = urlopen(url, data=json_post_data)
        
        print('received response from server')
        found_json = json_to_parse.readall().decode()
        get_gist_url(found_json)

    upload_gist()


class ButtonOne(bpy.types.Operator):
    bl_idname = "scene.upload_gist"
    bl_label = "Upload current text as gist"
 
    def execute(self, context):
        gist_description = context.scene.gist_description
        gist_filename = context.scene.gist_name
        gist_body = context.edit_text.as_string()

        # uploads gist, and stores link inside clipboard
        main_function(context, gist_filename, gist_description, gist_body)        

        return{'FINISHED'}  


class OperatorPanel(bpy.types.Panel):
    bl_label = "Upload Gist"
    bl_idname = "OBJECT_PT_uploadfunction"
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scn = bpy.context.scene

        # display stringbox and download button
        self.layout.prop(scn, "gist_name")
        self.layout.prop(scn, "gist_description")
        self.layout.operator("scene.upload_gist", text='Upload from .blend')



def initScenePropertiesUpload(scn):
 
    bpy.types.Scene.gist_name = StringProperty(
        name = "Name",
        description = "Name for Gist",
        default = ".py"
    )

    bpy.types.Scene.gist_description = StringProperty(
        name = "Description",
        description = "Description for Gist",
        default = ""
    )

 
initScenePropertiesUpload(bpy.context.scene)
classes = [OperatorPanel, ButtonOne]


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)


if __name__ == "__main__":
    register()