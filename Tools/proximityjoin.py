import bpy



class SETUPAUTO_OT_proxjoin(bpy.types.Operator):
    '''Class join objects in proximity to each other'''
    bl_idname = "setupauto.ot_proxjoin"
    bl_label = "proximity join"
    bl_description = "Operator loops through objects in the scene, joining objects together if are closer than specified proximity."

    def execute(self, context):
        tools_props = context.scene.tools_props
        
        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        remaining = set(selected)  # Keep track of unclustered objects
        clusters = []

        while remaining:
            obj = remaining.pop()
            cluster = [obj]
            to_check = [obj]

            while to_check:
                current = to_check.pop()
                current_loc = current.location

                close_objs = {other for other in remaining
                            if (current_loc - other.location).length <= tools_props.proximity}

                cluster.extend(close_objs)
                to_check.extend(close_objs)
                remaining.difference_update(close_objs)

            clusters.append(cluster)

        # === JOIN OBJECTS IN EACH CLUSTER ===
        for cluster in clusters:
            if len(cluster) < 2:
                continue  # Nothing to join

            bpy.ops.object.select_all(action='DESELECT')

            for obj in cluster:
                obj.select_set(True)

            bpy.context.view_layer.objects.active = cluster[0]
            bpy.ops.object.join()

        print(f"Joined {len([c for c in clusters if len(c) > 1])} clusters.")

        return {'FINISHED'}
