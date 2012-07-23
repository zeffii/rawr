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