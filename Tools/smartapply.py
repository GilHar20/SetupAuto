import bpy



class SETUPAUTO_OT_smartapply(bpy.types.Operator):
    '''Class apllies transforms of all selected objects, including batches of linked data'''
    bl_idname = "setupauto.ot_smartapply"
    bl_label = "smart apply"
    bl_description = "Operator loops through selected objects, apllies selected transform data, including batches of linked data"
    bl_options = {'REGISTER', 'UNDO'}


    location : bpy.props.BoolProperty(
        name = "Apply Location",
        default= False
    )

    rotation : bpy.props.BoolProperty(
        name = "Apply Rotation",
        default= False
    )

    scale : bpy.props.BoolProperty(
        name = "Apply Scale",
        default= True
    )


    def execute(self, context):
        for area in context.screen.areas:
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

        while remaining:
            # Get the next object from the set
            obj = remaining.pop()
            
            if obj.data and obj.data.users > 1:
                context.view_layer.objects.active = obj
                bpy.ops.object.select_linked(extend = False, type = 'OBDATA')

                bpy.ops.object.transform_apply(location = self.location, rotation = self.rotation, scale = self.scale)
                
                remaining -= set(context.selected_objects)

                bpy.ops.object.select_all(action='DESELECT')

            elif obj.data:
                obj.select_set(True)
                context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location = self.location, rotation = self.rotation, scale = self.scale)
                #bpy.ops.object.select_all(action='DESELECT')

        for obj in selected:
            obj.select_set(True)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    

    def draw(self, context):
        layout = self.layout

        layout.label(text = "This operator is VERY heavy.", icon = 'INFO')
        layout.label(text = "!USE CAREFULLY IN SMALL BATCHES!")

        rowAxis = layout.row(align = True)
        rowAxis.prop(self, 'location', text = "Location", toggle = True)
        rowAxis.prop(self, 'rotation', text = "Rotation", toggle = True)
        rowAxis.prop(self, 'scale', text = "Scale", toggle = True)