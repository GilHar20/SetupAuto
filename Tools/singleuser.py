import bpy



class SETUPAUTO_OT_singeluser(bpy.types.Operator):
    '''Class makes each selected object have a singel user data'''
    bl_idname = "setupauto.ot_singeluser"
    bl_label = "make singel user"
    bl_description = "Operator makes each selected object have a singel user data"

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            # Make the object data (like mesh, curve, etc.) single user
            if obj.data and obj.data.users > 1:
                obj.data = obj.data.copy()
