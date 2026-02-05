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

        boxObjects = layout.box()
        boxObjects.label(text="Object Batch Tools:", icon = 'OBJECT_DATA')
        columnObjects = boxObjects.column(align = True)

        columnObjects.operator('setupauto.ot_proxjoin', text = "Join By Proximity")
        columnObjects.operator('setupauto.ot_removecustomnormals', text = "Remove Custom Normals")


        # Instances section
        boxInst = layout.box()
        boxInst.label(text="Instances Tools:", icon = 'LINKED')
        columnInst = boxInst.column(align = True)

        columnInst.operator('setupauto.ot_smartapply', text = "Smart Apply")
        columnInst.operator('setupauto.ot_smartselect', text = "Selecte All Linked")
        columnInst.operator('setupauto.ot_singleuser', text = "Make Single Users")
        columnInst.operator('setupauto.ot_dups2inst', text = "Duplicates to Instances")
        columnInst.operator('outliner.orphans_purge', text = "Purge Unused Data")
