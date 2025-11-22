import bpy
from mathutils import Vector



class SETUPAUTO_OT_proxjoin(bpy.types.Operator):
    '''Class join objects in proximity to each other'''
    bl_idname = "setupauto.ot_proxjoin"
    bl_label = "proximity join"
    bl_description = "Operator loops through objects in the scene, joining objects together if are closer than specified proximity."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tools_props = context.scene.tools_props
        
        if not context.selected_objects:
            self.report({'INFO'}, "No objects were selected. Please select objects.")
            return {'CANCELLED'}

        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        remaining = set(selected)
        clusters = []
        
        axis_mask = Vector((
            1.0 if tools_props.proximity_x else 0.0,
            1.0 if tools_props.proximity_y else 0.0, 
            1.0 if tools_props.proximity_z else 0.0
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
                    if (current_loc_masked - other_loc_masked).length <= tools_props.proximity:
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

            bpy.context.view_layer.objects.active = cluster[0]
            bpy.ops.object.join()

        self.report({'INFO'}, f"Joined {len([c for c in clusters if len(c) > 1])} clusters.")

        return {'FINISHED'}
