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

        box1 = layout.box()
        box2.label(text="Single User")
        row1 = box1.row()
        row1.operator('setupauto.ot_singleuser', text = "Make Single Users")

        # Duplicates section
        box2 = layout.box()
        box2.label(text="Duplicate to Instances")
        row2 = box2.row()
        row2.operator('setupauto.ot_dups2inst', text = "Link Duplicates")

        # Proximity section
        box3 = layout.box()
        box3.label(text="Proximity Join")
        row3 = box3.row()
        row3.prop(toolprops, "proximity")
        row4 = box3.row()
        row4.operator('setupauto.ot_proxjoin', text = "Join By Proximity")



def register():
    bpy.utils.register_class(SETUPAUTO_PT_tools_panel)

def unregister():
    bpy.utils.unregister_class(SETUPAUTO_PT_tools_panel)