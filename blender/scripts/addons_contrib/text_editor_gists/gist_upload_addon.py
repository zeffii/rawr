import bpy
import json
from urllib.request import urlopen

def main_upload_function(context, gist_filename, gist_description, gist_body):

    gist_post_data = {  'description': gist_description, 
                        'public': True,
                        'files': {gist_filename: {'content': gist_body}}}

    json_post_data = json.dumps(gist_post_data).encode('utf-8')

    def get_gist_url(found_json):
        wfile = json.JSONDecoder()
        wjson = wfile.decode(found_json)
        gist_url = 'https://gist.github.com/' + wjson['id']
        context.window_manager.clipboard = gist_url
        print(gist_url)

    def upload_gist():
        print('sending')
        url = 'https://api.github.com/gists'
        json_to_parse = urlopen(url, data=json_post_data)
        
        print('received response from server')
        found_json = json_to_parse.readall().decode()
        get_gist_url(found_json)

    upload_gist()


class GistUploadButton(bpy.types.Operator):
    bl_idname = "scene.upload_gist"
    bl_label = "Upload current text as gist"
 
    def execute(self, context):
        gist_description = context.scene.gist_description
        gist_filename = context.scene.gist_name
        gist_body = context.edit_text.as_string()

        # uploads gist, and stores link inside clipboard
        main_upload_function(context, gist_filename, gist_description, gist_body)        
        return{'FINISHED'}  


class GistUploadPanel(bpy.types.Panel):
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
