import bpy



class SETUPAUTO_OT_purgeunused(bpy.types.Operator):
    '''Class purges unused data from the blend file'''
    bl_idname = "setupauto.ot_purgeunused"
    bl_label = "purge unused data"
    bl_description = "Operator purges unused data from the blend file"

    def execute(self, context):
        tools_props = context.scene.tools_props

        bpy.ops.outliner.orphans_purge(do_local=tools_props.do_local, do_linked=tools_props.do_linked, do_recursive=tools_props.do_recursive)
        
        return {'FINISHED'}
