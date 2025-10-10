import bpy



class SETUPAUTO_OT_singleuser(bpy.types.Operator):
    '''Class copies selected object data single user'''
    bl_idname = "setupauto.ot_singleuser"
    bl_label = "make single user"
    bl_description = "Operator makes each selected object have a single user data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.selected_objects:
            self.report({'INFO'}, "No objects were selected. Please select objects.")
            return {'CANCELLED'}
        
        selected = context.selected_objects

        for obj in selected:
            # Make the object data (like mesh, curve, etc.) single user
            if obj.data and obj.data.users > 1:
                obj.data = obj.data.copy()

        self.report({'INFO'}, "All " + str(len(selected)) + " selected objects are now single users!")

        return {'FINISHED'}