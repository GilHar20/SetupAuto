import bpy
import hashlib



class SETUPAUTO_OT_dups2inst(bpy.types.Operator):
    '''Class links similar objects together'''
    bl_idname = "setupauto.ot_dups2inst"
    bl_label = "duplicates to instances"
    bl_description = "Operator loops through selected objects, linking objects data together if the topology is close enough."
    bl_options = {'REGISTER', 'UNDO'}


    accuracy : bpy.props.IntProperty(name="Floating Point Accuracy", description="Accurate of the vertex positions when comparing meshes; Or: how many numbers after decimal point. " + \
                                     "Higher number is more accurate, but slower.", default=6, min=1, max=7)

    rename : bpy.props.BoolProperty(name="Rename", description="Rename linked objects", default=False)

    new_name : bpy.props.StringProperty(name="New Name", description="New name to give all new linked objects. NOTE! Will name ALL selected objects!", default="")


    def mesh_hash(self, context, obj):
        mesh = obj.data
        verts = tuple(round(v.co.x, self.accuracy) for v in mesh.vertices) + \
                tuple(round(v.co.y, self.accuracy) for v in mesh.vertices) + \
                tuple(round(v.co.z, self.accuracy) for v in mesh.vertices)
        materials = tuple(mat.name if mat else "None" for mat in mesh.materials)
        return hashlib.md5(str((verts, materials)).encode()).hexdigest()


    def execute(self, context):
        if len(bpy.context.selected_objects) <= 1:
            self.report({'INFO'}, "You need to select two or more objects.")
            return {'CANCELLED'}

        selected = context.selected_objects

        seen = {}
        for obj in selected:
            if obj.type != 'MESH':
                continue
            key = self.mesh_hash(context, obj)
            if key not in seen:
                seen[key] = [obj]
            else:
                list = seen[key]
                list.append(obj)

        for key in seen:
            bpy.ops.object.select_all(action='DESELECT')
            list = seen[key]
            for obj in list:
                obj.select_set(True)
            bpy.context.view_layer.objects.active = list[0]
            bpy.ops.object.make_links_data(type='OBDATA')

        #new = bpy.data.objects.new(name=ref.name + "_inst", object_data=ref.data)
        #new.matrix_world = obj.matrix_world
        #bpy.context.collection.objects.link(new)
        #bpy.data.objects.remove(context, obj)

        self.report({'INFO'},"Finished linking" + str(len(selected)) + " objects!")
        return {'FINISHED'}
    

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
