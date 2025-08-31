import bpy



class SETUPAUTO_OT_singleuser(bpy.types.Operator):
    '''Class copies selected object data single user'''
    bl_idname = "setupauto.ot_singleuser"
    bl_label = "make single user"
    bl_description = "Operator makes each selected object have a single user data"

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            # Make the object data (like mesh, curve, etc.) single user
            if obj.data and obj.data.users > 1:
                obj.data = obj.data.copy()



def register():
    bpy.utils.register_class(SETUPAUTO_OT_singleuser)

def unregister():
    bpy.utils.unregister_class(SETUPAUTO_OT_singleuser)
