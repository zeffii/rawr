import bpy
from bpy_extras.view3d_utils import location_3d_to_region_2d as loc3d2d

import os
from mathutils import Vector

output_filename = 'new_output2.svg'



header_string = """\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="%(width)s" height="%(height)s"
    xmlns="http://www.w3.org/2000/svg" version="1.1">
    <desc>some description here</desc>
"""


path_data = """\
       <path d="M %(x1)s,%(y1)s %(x2)s,%(y2)s"
             id="%(path_name)s"/>"""
    

group_style_info = """\
    <g style ="    fill:none;
                   stroke:#000000;
                   stroke-width:1.2;
                   stroke-linecap:butt;
                   stroke-linejoin:miter;
                   stroke-opacity:1;
                   stroke-miterlimit:4;
                   stroke-dasharray:none">"""


end_group_style_info = """\
    </g>"""


def printWarning(input):
    print("\033[31m%s\033[0m" % input) 


def write_svg(data):
    edge_list, region = data
    width, height =  region.width, region.height

    file_to_write = open(output_filename, 'w')
    file_to_write.write(header_string  % vars())
    file_to_write.write(group_style_info)

    for idx, edge in enumerate(edge_list):
        co1, co2 = edge
   
        x1 = co1.x
        y1 = height - co1.y
        x2 = co2.x
        y2 = height - co2.y
        path_name="path"+str(idx)
        
        file_to_write.write(path_data %  vars())

    file_to_write.write(end_group_style_info)
    file_to_write.write("""</svg>""")
    file_to_write.close()

    file_location = os.path.join(os.getcwd(), output_filename)
    printWarning('wrote: ' + file_location)
    return


def get_locals(context):
    region = context.region  
    rv3d = context.space_data.region_3d  
    obj = context.active_object
    vertlist = obj.data.vertices
    return region, rv3d, obj, vertlist


def generate_2d_draw_data(context):
    """
    this gets vertex coordinates, converts local to global
    generates edge_list with 2d screen coordinates.
    """
    region, rv3d, obj, vertlist = get_locals(context)

    edge_list = []
    for edge in obj.data.edges:
        local_coords = [vertlist[idx].co for idx in edge.vertices]
        world_coords = [obj.matrix_world * point for point in local_coords]    
        edge_as_2d = [loc3d2d(region, rv3d, point) for point in world_coords]
        edge_list.append(edge_as_2d)

    return edge_list, region


# Candidate for refactor.
def generate_2d_draw_list(unique_set, context):

    region, rv3d, obj, vertlist = get_locals(context)

    edge_list = []
    for edge in unique_set:
        local_coords = [vertlist[idx].co for idx in edge]
        world_coords = [obj.matrix_world * point for point in local_coords]    
        edge_as_2d = [loc3d2d(region, rv3d, point) for point in world_coords]
        edge_list.append(edge_as_2d)

    return edge_list, region


def select_unique_edges_from(face_list, context):
    """
    input: face_list        contains face indices for usable faces.
    input: context          a convenience variable.
    
    from the given face list, many faces will share edges, we reduce this list
    by exluding duplicate edge geometry from the drawable list.
    """
    obj = context.active_object
    edge_list_pre_unique = []
    
    def append_edge(idx1, idx2):
        edge_partial = sorted((vert_list[idx1],vert_list[idx2]))
        edge_list_pre_unique.append(tuple(edge_partial))
  
    # deal with quads and tris    
    for idx, face in enumerate(face_list):
        vert_list = obj.data.polygons[face].vertices

        # last addition occurs outside the loop to avoid interupting the loop
        # all the time.
        for i in range(len(vert_list)-1):
            append_edge(i, i+1)
        append_edge(-1, 0)

    unique_set = set(edge_list_pre_unique)
    printWarning(str(len(unique_set)) + " edges!")
    return unique_set
    



def select_front_facing(context):
    """
    from: http://freespace.virgin.net/hugo.elias/routines/r_dot.htm
    
    When deciding if a polygon is facing the camera, you need 
    only calculate the dot product of the normal vector of     
    that polygon, with a vector from the camera to one of the 
    polygon's vertices. 
    
    - If the dot product is less than zero, the polygon is facing the camera. 
    - If the value is greater than zero, it is facing away from the camera.
    """
    
    region, rv3d, obj, vertlist = get_locals(context)

    # [ ] be in object mode
    
    # neat eye location code with the help of paleajed
    eye = Vector(rv3d.view_matrix[2][:3])
    eye.length = rv3d.view_distance
    eye_location = rv3d.view_location + eye  

    face_list = []
    for idx, polygon in enumerate(obj.data.polygons):
        
        vert_index = polygon.vertices[0]
        pnormal = obj.matrix_world * polygon.normal
        world_coordinate = obj.matrix_world * vertlist[vert_index].co
        
        result_vector = eye_location-world_coordinate
        dot_value = pnormal.dot(result_vector.normalized())            

        if dot_value < 0.0:
            polygon.select = False
        else:
            polygon.select = True
            face_list.append(idx)
     
    return face_list


class RenderButton(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "svg.render"
    bl_label = "Renders to svg"
    country = bpy.props.StringProperty()
 
    def execute(self, context):
        obname = context.active_object.name
        print('all - rendering %s' % obname)

        data = generate_2d_draw_data(context)
        write_svg(data)
        return{'FINISHED'}  



class RenderFrontButton(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "svg.render_front_facing"
    bl_label = "Renders front facing to svg"
    country = bpy.props.StringProperty()
 
    def execute(self, context):
        obname = context.active_object.name
        print('front - rendering %s' % obname)

        face_list = select_front_facing(context)
        unique_set = select_unique_edges_from(face_list, context)
        data = generate_2d_draw_list(unique_set, context)
        write_svg(data)
        return{'FINISHED'}  



class SVGPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Render SVG"
    bl_idname = "OBJECT_PT_render"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        
        # display button
        self.layout.operator("svg.render", text='Render All')
        self.layout.operator("svg.render_front_facing", text='Render Front Facing')



classes = [SVGPanel, RenderButton, RenderFrontButton]

def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)


if __name__ == "__main__":
    register()