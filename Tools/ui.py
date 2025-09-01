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

        # Join Seperate section
        boxjoin = layout.box()
        boxjoin.label(text="Join Seperate Tools")
        row1 = boxjoin.row()
        column1 = row1.column()
        column1.prop(toolprops, "proximity")
        column2 = row1.column()
        column2.operator('setupauto.ot_proxjoin', text = "Join By Proximity")

        row2 = boxjoin.row()
        row2.label(text="Add Grid Split/Join Tool Here")



        # Instances section
        boxInst = layout.box()
        boxInst.label(text="Instances Tools")
        row1 = boxInst.row()
        row1.operator('setupauto.ot_dups2inst', text = "Duplicate to Instances")

        row2a = boxInst.row()
        row2a.label(text="Smart Apply Transforms:")
        row2b = boxInst.row()
        col1 = row2b.column()
        col1.alignment = 'LEFT'
        col1.prop(toolprops, "location", text="Location")
        col2 = row2b.column()
        col2.alignment = 'CENTER'
        col2.prop(toolprops, "rotation", text="Rotation")
        col3 = row2b.column()
        col3.alignment = 'RIGHT'
        col3.prop(toolprops, "scale", text="Scale")
        row2c = boxInst.row()
        row2c.operator('setupauto.ot_smartapply', text = "Smart Apply")



        row3 = boxInst.row()
        row3.operator('setupauto.ot_singleuser', text = "Make Single Users")

        row4 = boxInst.row()
        row4.operator('setupauto.ot_purgeunused', text="Purge Unused Data")