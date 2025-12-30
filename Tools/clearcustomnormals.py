import bpy



class SETUPAUTO_OT_removecustomnormals(bpy.types.Operator):
    '''Class selects all batches of linked data of all currently selected objects'''
    bl_idname = "setupauto.ot_removecustomnormals"
    bl_label = "remove custom normals"
    bl_description = "Operator removes custom normals from selected objects"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        if not context.selected_objects:
            self.report({'INFO'}, "Please select objects to clear normals from")
            return {'FINISHED'}

        selected = context.selected_objects

        for obj in selected:
            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            bpy.ops.object.mode_set(mode='OBJECT')
        
        self.report({'INFO'}, "All normals are clear!")

        return {'FINISHED'}
