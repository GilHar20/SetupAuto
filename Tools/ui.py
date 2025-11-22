import bpy



class SETUPAUTO_PT_tools_panel(bpy.types.Panel):
    '''Class draws tools UI panel'''
    bl_idname = "setupauto.pt_tools_panel"
    bl_label = "Tools Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SetupAuto"

    def draw(self, context):
        layout = self.layout
        toolprops = context.scene.tools_props

        # Proximity Join section
        boxJoin = layout.box()
        boxJoin.label(text="Proximity Join")
        columnJoin = boxJoin.column(align=True)

        rowAxis = columnJoin.row(align=True)
        rowAxis.prop(toolprops, "proximity_x", text="X", toggle=True)
        rowAxis.prop(toolprops, "proximity_y", text="Y", toggle=True)
        rowAxis.prop(toolprops, "proximity_z", text="Z", toggle=True)
        
        columnJoin.prop(toolprops, "proximity")
        columnJoin.operator('setupauto.ot_proxjoin', text = "Join By Proximity")


        # Smart Apply Transforms section
        boxSmart = layout.box()
        boxSmart.label(text="Smart Apply Transforms")
        columnSmart = boxSmart.column(align=True)

        rowFlags = columnSmart.row(align=True)
        rowFlags.prop(toolprops, "location", text="Location", toggle=True)
        rowFlags.prop(toolprops, "rotation", text="Rotation", toggle=True)
        rowFlags.prop(toolprops, "scale", text="Scale", toggle=True)
        
        columnSmart.operator('setupauto.ot_smartapply', text = "Smart Apply")


        # Instances section
        boxInst = layout.box()
        boxInst.label(text="Instances Tools")
        columnInst = boxInst.column(align=True)

        columnInst.operator('setupauto.ot_smartselect', text = "Selecte All Linked")
        columnInst.operator('setupauto.ot_singleuser', text = "Make Single Users")
        columnInst.operator('setupauto.ot_dups2inst', text = "Duplicate to Instances")
        columnInst.operator('outliner.orphans_purge', text = "Purge Unused Data")
