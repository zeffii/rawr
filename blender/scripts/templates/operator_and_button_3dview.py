"""
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


Categories:
3D View, Add Curve, Add Mesh, Animation, Development, Game Engine,
Import-Export, Material, Mesh, Object, Paint, Render, Rigging, Sequencer, System, Text Editor


bl_space_type: 
enum in [‘WINDOW’, ‘HEADER’, ‘CHANNELS’, ‘TEMPORARY’, ‘UI’, ‘TOOLS’, 
‘TOOL_PROPS’, ‘PREVIEW’], 
default ‘WINDOW’

region_type:
enum in [‘EMPTY’, ‘VIEW_3D’, ‘GRAPH_EDITOR’, ‘OUTLINER’, ‘PROPERTIES’, 
‘FILE_BROWSER’, ‘IMAGE_EDITOR’, ‘INFO’, ‘SEQUENCE_EDITOR’, ‘TEXT_EDITOR’, 
‘AUDIO_WINDOW’, ‘DOPESHEET_EDITOR’, ‘NLA_EDITOR’, ‘SCRIPTS_WINDOW’, 
‘TIMELINE’, ‘NODE_EDITOR’, ‘LOGIC_EDITOR’, ‘CONSOLE’, ‘USER_PREFERENCES’], 
default ‘EMPTY’

""" 

import bpy
from mathutils import Vector


class ButtonOne(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "scene.dostuff"
    bl_label = "Sometype of operator"
 
    def execute(self, context):
        # do your stuff here, this will have view3d as context
        print('rawr')
        return{'FINISHED'}  


class OperatorPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Some Utility"
    bl_idname = "OBJECT_PT_somefunction"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        row = layout.row()

        # display label and button
        if not obj == None:
            row.label(text="Active object is: " + obj.name)
            self.layout.operator("scene.dostuff", text='Description of utility')



classes = [OperatorPanel, ButtonOne]

def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)


if __name__ == "__main__":
    register()