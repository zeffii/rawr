# be in edit mode to run this code  
  
import bpy  
from mathutils import Vector  

myob = bpy.context.active_object  
bpy.ops.object.mode_set(mode = 'OBJECT')  
  
# collect selected verts
selected_idx = [i.index for i in myob.data.vertices if i.select]
original_object = myob.name

for v_index in selected_idx:
    # get local coordinate, turn into word coordinate
    vert_coordinate = myob.data.vertices[v_index].co  
    vert_coordinate = myob.matrix_world * vert_coordinate
      
    # unselect all  
    for item in bpy.context.selectable_objects:  
        item.select = False  
    
    # this deals with adding the empty      
    bpy.ops.object.add(type='EMPTY', location=vert_coordinate)  
    mt = bpy.context.active_object  
    mt.location = vert_coordinate
    mt.empty_draw_size = mt.empty_draw_size / 4  
      
    bpy.ops.object.select_all(action='TOGGLE')  
    bpy.ops.object.select_all(action='DESELECT')  
    
# set original object to active, selects it, place back into editmode
bpy.context.scene.objects.active = myob
myob.select = True  
bpy.ops.object.mode_set(mode = 'EDIT')
