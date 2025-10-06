import bpy



class SETUPAUTO_OT_smartapply(bpy.types.Operator):
    '''Class apllies transforms of all selected objects, including batches of linked data'''
    bl_idname = "setupauto.ot_smartapply"
    bl_label = "smart apply"
    bl_description = "Operator loops through selected objects, apllies selected transform data, including batches of linked data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tools_props = context.scene.tools_props

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                view_3d = area.spaces.active

        if view_3d.local_view:
            self.report({'ERROR'}, "You must leave local view for this operator to work! Press ? to leave local view")
            return {"CANCELLED"}
        else:
            pass

        selected = context.selected_objects
        remaining = set(selected)

        bpy.ops.object.select_all(action='DESELECT')

        while remaining:
            # Get the next object from the set
            obj = next(iter(remaining))
            
            if obj.data and obj.data.users > 1:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.select_linked(extend = False, type = 'OBDATA')

                bpy.ops.object.transform_apply(location=tools_props.location, rotation=tools_props.rotation, scale=tools_props.scale)
                
                for linked_obj in context.selected_objects:
                    if linked_obj in remaining:
                        remaining.remove(linked_obj)
                bpy.ops.object.select_all(action='DESELECT')

            elif obj.data:
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=tools_props.location, rotation=tools_props.rotation, scale=tools_props.scale)
                remaining.remove(obj)
                bpy.ops.object.select_all(action='DESELECT')

            bpy.ops.object.select_all(action='DESELECT')

        for obj in selected:
            obj.select_set(True)

        return {'FINISHED'}