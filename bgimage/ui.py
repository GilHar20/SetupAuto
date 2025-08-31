import bpy



class SETUPAUTO_PT_bgimage_panel(bpy.types.Panel):
    '''Class draws bgimage UI panel'''
    bl_idname = "setupauto.pt_bgimage_panel"
    bl_label = "Background Image Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SetupAuto"

    def draw(self, context):
        layout = self.layout
        bgimageprops = context.scene.bgimage_props

        #bg image settings:
        box1 = layout.box()
        
        row1 = box1.row()
        row1.prop(bgimageprops, "auto_detect_resolution", text="Auto-detect from images")
        
        if not bgimageprops.auto_detect_resolution:
            row2 = box1.row()
            column1 = row2.column(align=True)
            column1.prop(bgimageprops, "resolution_x")

            column2 = row2.column(align=True)
            column2.prop(bgimageprops, "resolution_y")
        
        row3 = box1.row()
        row3.prop(bgimageprops, "bgimage_folder_path")

        row4 = box1.row()
        row4.prop(bgimageprops, "image_format")

        row5 = box1.row()
        row5.prop(bgimageprops, "opacity")

        row7 = box1.row()
        row7.label(text="Depth:")
        row7.prop(bgimageprops, "display_depth", expand=True)
    
        row6 = box1.row()
        row6.label(text="Frame Method:")
        row6.prop(bgimageprops, "frame_method", expand=True)

        row10 = box1.row()
        row10.operator('setupauto.ot_bgimage', text = "Assign Images!")
