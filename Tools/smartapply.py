import bpy



class SETUPAUTO_OT_smartapply(bpy.types.Operator):
    '''Class apllies transforms of all selected objects, including batches of linked data'''
    bl_idname = "setupauto.ot_smartapply"
    bl_label = "smart apply"
    bl_description = "Operator loops through selected objects, apllies selected transform data, including batches of linked data"

    def execute(self, context):
        tools_props = context.scene.tools_props

        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        remaining = set(selected)  # Keep track of unclustered objects
        clusters = []

        bpy.ops.object.select_all(action='DESELECT')

        while remaining:
            # Get the next object from the set
            obj = next(iter(remaining))
            
            # Check if this object has linked data
            if obj.data and obj.data.users > 1:
                # Find all objects with the same linked data
                linked_objects = [o for o in bpy.data.objects if o.data == obj.data]
                
                # Select all linked objects
                for linked_obj in linked_objects:
                    linked_obj.select_set(True)
                
                # Apply transforms to all linked objects at once
                bpy.ops.object.transform_apply(location=tools_props.location, rotation=tools_props.rotation, scale=tools_props.scale)
                
                # Remove all linked objects from the remaining set
                for linked_obj in linked_objects:
                    if linked_obj in remaining:
                        remaining.remove(linked_obj)
            else:
                # Single object, no linked data
                obj.select_set(True)
                bpy.ops.object.transform_apply(location=tools_props.location, rotation=tools_props.rotation, scale=tools_props.scale)
                remaining.remove(obj)
            
            # Deselect all for next iteration
            bpy.ops.object.select_all(action='DESELECT')


        return {'FINISHED'}