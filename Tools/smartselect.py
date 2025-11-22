import bpy



class SETUPAUTO_OT_smartselect(bpy.types.Operator):
    '''Class selects all batches of linked data of all currently selected objects'''
    bl_idname = "setupauto.ot_smartselect"
    bl_label = "smart select"
    bl_description = "Operator loops through selected objects and adds selections of all linked data of all every selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tools_props = context.scene.tools_props

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                view_3d = area.spaces.active

        if view_3d.local_view:
            self.report({'ERROR'}, "You must leave local view for this operator to work! Press ? to leave local view")
            return {"CANCELLED"}

        if not context.selected_objects:
            self.report({'INFO'}, "No objects were selected.")
            return {'CANCELLED'}

        selected = context.selected_objects
        remaining = set(selected)

        bpy.ops.object.select_all(action='DESELECT')

        '''
        while remaining:
            # Get the next object from the set
            obj = next(iter(remaining))
        '''    
        for obj in selected:
            if obj.data.users > 1 and obj not in context.selected_objects:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.select_linked(extend = True, type = 'OBDATA')

            elif obj not in context.selected_objects:
                obj.select_set(True)

        self.report({'INFO'}, "Selected: " + str(len(context.selected_objects)) + " objects overall")
        return {'FINISHED'}