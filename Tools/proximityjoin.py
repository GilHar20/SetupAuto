import bpy
from mathutils import Vector



class SETUPAUTO_OT_proxjoin(bpy.types.Operator):
    '''Class join objects in proximity to each other'''
    bl_idname = "setupauto.ot_proxjoin"
    bl_label = "proximity join"
    bl_description = "Operator loops through objects in the scene, joining objects together if are closer than specified proximity."
    bl_options = {'REGISTER', 'UNDO'}


    proximity : bpy.props.FloatProperty(
        name = "Proximity",
        description = "Maximum distance to merge objects.",
        default = 1.5,
        min = 0.1,
        max = 1000
    )
    proximity_x : bpy.props.BoolProperty(
        name = "Proximity X",
        description = "Consider X axis for proximity calculation.",
        default = True
    )
    
    proximity_y : bpy.props.BoolProperty(
        name = "Proximity Y", 
        description = "Consider Y axis for proximity calculation.",
        default = True
    )

    proximity_z : bpy.props.BoolProperty(
        name = "Proximity Z",
        description = "Consider Z axis for proximity calculation.", 
        default = True
    )

    def execute(self, context):
        
        if not context.selected_objects:
            self.report({'INFO'}, "No objects were selected. Please select objects.")
            return {'CANCELLED'}

        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        remaining = set(selected)
        clusters = []
        
        axis_mask = Vector((
            1.0 if self.proximity_x else 0.0,
            1.0 if self.proximity_y else 0.0, 
            1.0 if self.proximity_z else 0.0
        ))

        while remaining:
            obj = remaining.pop()
            cluster = [obj]
            to_check = [obj]

            while to_check:
                current = to_check.pop()
                # Apply axis mask to current object's location
                current_loc_masked = Vector(current.location) * axis_mask

                close_objs = set()
                for other in remaining:
                    # Apply axis mask to other object's location
                    other_loc_masked = Vector(other.location) * axis_mask
                    # Calculate distance only on selected axes
                    if (current_loc_masked - other_loc_masked).length <= self.proximity:
                        close_objs.add(other)

                cluster.extend(close_objs)
                to_check.extend(close_objs)
                remaining -= close_objs

            clusters.append(cluster)

        # Join objects in cluster
        for cluster in clusters:
            if len(cluster) < 2:
                continue  # Nothing to join

            bpy.ops.object.select_all(action='DESELECT')

            for obj in cluster:
                obj.select_set(True)

            context.view_layer.objects.active = cluster[0]
            bpy.ops.object.join()

        self.report({'INFO'}, f"Joined {len([c for c in clusters if len(c) > 1])} clusters.")

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    

    def draw(self, context):
        layout = self.layout

        columnProximity = layout.column(align = True)

        rowAxis = columnProximity.row(align = True)
        rowAxis.prop(self, 'proximity_x', text = "X", toggle = True)
        rowAxis.prop(self, 'proximity_y', text = "Y", toggle = True)
        rowAxis.prop(self, 'proximity_z', text = "Z", toggle = True)

        rowProximity = columnProximity.row()
        rowProximity.prop(self, 'proximity', text = "Proximity")
