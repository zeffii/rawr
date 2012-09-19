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
#	the Free Software Foundation Inc.
#	51 Franklin Street, Fifth Floor
#	Boston, MA 02110-1301, USA
#
# or go online at: http://www.gnu.org/licenses/ to view license options.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Text Appeal",
    "author": "zeffii",
    "version": (0, 1, 0),
    "blender": (2, 6, 1),
    "location": "TextEditor - multiple places",
    "description": "Adds eval and chroma button.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Text Editor"}


if "bpy" in locals():
    import imp
    imp.reload(text_editor_chroma)
    imp.reload(text_editor_eval)
    imp.reload(text_editor_searchpydocs)
    imp.reload(text_editor_searchbpydocs)
else:
    from text_editor_extras import text_editor_chroma
    from text_editor_extras import text_editor_eval
    from text_editor_extras import text_editor_searchpydocs
    from text_editor_extras import text_editor_searchbpydocs

import bpy


def draw_item(self, context):
    layout = self.layout
    layout.operator("txt.set_text_prefs", icon='COLOR')

def eval_menu_item(self, context):
    layout = self.layout
    layout.operator("txt.eval_selected_text", text='Eval Selected')
    layout.operator("txt.search_pydocs", text='Search Pydocs')
    layout.operator("txt.search_bpydocs", text='Search bpy docs')

def register():
    bpy.utils.register_module(__name__)
    bpy.types.TEXT_HT_header.prepend(draw_item)
    bpy.types.TEXT_MT_toolbox.prepend(eval_menu_item)    

def unregister():
    bpy.utils.unregister_module(__name__)    
    bpy.types.TEXT_HT_header.remove(draw_item)
    bpy.types.TEXT_MT_toolbox.remove(eval_menu_item)
    
if __name__ == "__main__":
    register()
