import bpy
import hashlib



class SETUPAUTO_OT_dups2inst(bpy.types.Operator):
    '''Class links similar objects together'''
    bl_idname = "setupauto.ot_dups2inst"
    bl_label = "duplicates to instances"
    bl_description = "Operator loops through selected objects, linking objects data together if the topology is close enough."


    def mesh_hash(self, obj):
        mesh = obj.data
        verts = tuple(round(v.co.x, 6) for v in mesh.vertices) + \
                tuple(round(v.co.y, 6) for v in mesh.vertices) + \
                tuple(round(v.co.z, 6) for v in mesh.vertices)
        materials = tuple(mat.name if mat else "None" for mat in mesh.materials)
        return hashlib.md5(str((verts, materials)).encode()).hexdigest()

    def replace_with_instances(self):
        seen = {}
        for obj in list(bpy.context.selected_objects):
            if obj.type != 'MESH':
                continue
            key = self.mesh_hash(obj)
            if key not in seen:
                seen[key] = obj
            else:
                ref = seen[key]
                new = bpy.data.objects.new(name=ref.name + "_inst", object_data=ref.data)
                new.matrix_world = obj.matrix_world
                bpy.context.collection.objects.link(new)
                bpy.data.objects.remove(obj)

    def execute(self, context):
        if bpy.context.selected_objects:
            self.replace_with_instances()
        else:
            self.report({'INFO'}, "No objects selected.")
        return {'FINISHED'}
