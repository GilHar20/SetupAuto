import bpy
import hashlib



class SETUPAUTO_OT_dups2inst(bpy.types.Operator):
    '''Class links similar objects together'''
    bl_idname = "setupauto.ot_dups2inst"
    bl_label = "duplicates to instances"
    bl_description = "Operator loops through selected objects, linking objects data together if the topology is close enough."
    bl_options = {'REGISTER', 'UNDO'}


    mode : bpy.props.EnumProperty(
        name = "",
        description = "",
        items = [
        ('BOX', "Bounding Box", "Use bounding box"),
        ('FULL', "Full Topology", "Use Full Topology"),
        ],
        default = 'BOX'
    )

    accuracy : bpy.props.IntProperty(
        name = "Floating Point Accuracy", 
        description = "Accurate of the vertex positions when comparing meshes; Or: how many numbers after decimal point. Higher number is more accurate, but slower.", 
        default = 2, 
        min = 1, 
        max = 7
    )

    rename : bpy.props.BoolProperty(
        name = "Rename",
        description = "Rename linked objects",
        default = False
    )

    new_name : bpy.props.StringProperty(name = "New Name", description = "New name to give all new linked objects. NOTE! Will name ALL selected objects!", default = "")


    def mesh_hash(self, context, obj):
        mesh = obj.data
        
        if self.mode == 'BOX':
            # Use bounding box dimensions for comparison
            dimensions = tuple(round(d, self.accuracy) for d in obj.dimensions)
            materials = tuple(mat.name if mat else "None" for mat in mesh.materials)
            return hashlib.md5(str((dimensions, materials)).encode()).hexdigest()
        elif self.mode == 'FULL':
            # Full topology mode - use all vertex positions
            verts = tuple(round(v.co.x, self.accuracy) for v in mesh.vertices) + \
                    tuple(round(v.co.y, self.accuracy) for v in mesh.vertices) + \
                    tuple(round(v.co.z, self.accuracy) for v in mesh.vertices)
            materials = tuple(mat.name if mat else "None" for mat in mesh.materials)
            return hashlib.md5(str((verts, materials)).encode()).hexdigest()


    def execute(self, context):
        selected = context.selected_objects

        if len(selected) <= 1:
            self.report({'INFO'}, "You need to select two or more objects.")
            return {'CANCELLED'}

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

        self.report({'INFO'},"Finished linking" + str(len(selected)) + " objects!")
        return {'FINISHED'}
    

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    

    def draw(self, context):
        layout = self.layout
        layout.label(text = "'BOX': Less accurate, easier to link data.", icon = 'INFO')
        layout.label(text = "'FULL': More accurate, harder to link data.", icon = 'INFO')

        layout.prop(self, 'mode', text = "Mode")
        layout.prop(self, 'accuracy', text = "Accuracy")
        layout.prop(self, 'rename', text = "Rename")
        layout.prop(self, 'new_name', text = "New Name")
