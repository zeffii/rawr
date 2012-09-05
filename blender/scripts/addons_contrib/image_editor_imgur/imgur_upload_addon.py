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

import bpy
import json

import base64
import os
import re

from urllib.request import urlopen
from urllib.parse import urlencode


# def main_upload_function(context, gist_filename, gist_description, gist_body):

#     gist_post_data = {  'description': gist_description, 
#                         'public': True,
#                         'files': {gist_filename: {'content': gist_body}}}

#     json_post_data = json.dumps(gist_post_data).encode('utf-8')

#     def get_gist_url(found_json):
#         wfile = json.JSONDecoder()
#         wjson = wfile.decode(found_json)
#         gist_url = 'https://gist.github.com/' + wjson['id']
#         context.window_manager.clipboard = gist_url
#         print(gist_url)

#     def upload_imgur():
#         print('sending')
#         url = 'https://api.github.com/gists'
#         json_to_parse = urlopen(url, data=json_post_data)
        
#         print('received response from server')
#         found_json = json_to_parse.readall().decode()
#         get_gist_url(found_json)


def upload_image(path_to_image):

    def xml_regex(xml_to_parse):
        identifiers = 'imgur_page, original, delete_page, large_thumbnail'.split(', ')
        for identifier in identifiers:
            pattern = '<' + identifier+ '>(.*)</+' + identifier + '>'
            match = re.search(pattern, xml_to_parse)
            print('%-18s %s' % (identifier, match.groups()[0]))


    def encode_image(path_to_image):
        source = open(path_to_image, 'rb')
        picture = base64.b64encode(source.read())
        print('encoded')
        return picture


    url = 'http://api.imgur.com/2/upload.xml'
    apikey = '----------your api key-----'
    image_name = '------your image-------'
    
    picture = encode_image(path_to_image)
    parameters = { 'key' : apikey, 'image' : picture }
    data = urlencode(parameters)

    print('sending')
    xml_to_parse = urlopen(url, data)

    print('received response from server')
    xml_to_parse = xml_to_parse.readall().decode()
    xml_regex(xml_to_parse)


class ImageUploadButton(bpy.types.Operator):
    bl_idname = "scene.upload_imgur"
    bl_label = "Upload image slot to imgur"
 
    def execute(self, context):
        print(dir(context.edit_image))
        c_img = context.edit_image
        file_name = c_img.name        
        file_format = c_img.file_format
        print(file_name, file_format)
        # uploads gist, and stores link inside clipboard
        # path_to_image = os.path.join(os.getcwd(), image_name)
        # upload_image(path_to_image)
        return{'FINISHED'}  


class ImageUploadPanel(bpy.types.Panel):
    bl_label = "Upload Imgur"
    bl_idname = "OBJECT_PT_imgurfunction"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scn = bpy.context.scene
        self.layout.operator("scene.upload_imgur", text='Upload from .blend')
