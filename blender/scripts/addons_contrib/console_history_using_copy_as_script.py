bl_info = {
    "name": "Console History",
    "author": "Dealga McArdle",
    "version": (0, 1, 0),
    "blender": (2, 6, 4),
    "location": "Console - Copy History",
    "description": "Adds Copy History options to Console button.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Console"}
    
import bpy

def sanitize_console_dump(tm):


    def of_interest(line):
        return not starts_with_token(line) and not incomplete(line)

    
    def starts_with_token(line):
        tokens = "#~","#!"
        for token in tokens:
            if line.startswith(token):
                return True
        return False
    
    
    def incomplete(line):
        return line.endswith('.')
    
   
    tm = tm.split('\n')
    cleaner = [line for line in tm if of_interest(line)]
    return'\n'.join(cleaner)


class AddToClipboard(bpy.types.Operator):
    bl_label = ""
    bl_idname = "console.copy_history_n"
    
    def execute(self, context):
        bpy.ops.console.copy_as_script()
        tm = context.window_manager.clipboard
        context.window_manager.clipboard = sanitize_console_dump(tm)
        return {'FINISHED'}


def history_menu(self, context):
    layout = self.layout
    layout.operator("console.copy_history_n", text='Copy History')    
    

def register():
    bpy.utils.register_class(AddToClipboard)
    bpy.types.CONSOLE_MT_console.prepend(history_menu)    

def unregister():
    bpy.utils.unregister_class(AddToClipboard)
    bpy.types.CONSOLE_MT_console.remove(history_menu)
    
if __name__ == "__main__":
    register()
    
    