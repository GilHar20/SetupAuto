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
        boxBGImage = layout.box()
        
        rowAutoDetect = boxBGImage.row()
        rowAutoDetect.prop(bgimageprops, "auto_detect_resolution", text="Auto-detect from images", toggle = True)
        
        if not bgimageprops.auto_detect_resolution:
            columnResolution2 = boxBGImage.column(align=True)
            columnResolution2.prop(bgimageprops, "resolution_x")
            columnResolution2.prop(bgimageprops, "resolution_y")

        
        rowFolderPath = boxBGImage.row()
        rowFolderPath.prop(bgimageprops, "bgimage_folder_path")

        rowFormat = boxBGImage.row()
        rowFormat.prop(bgimageprops, "image_format")

        rowOpacity = boxBGImage.row()
        rowOpacity.prop(bgimageprops, "opacity")

        rowDepth = boxBGImage.row()
        rowDepth.label(text="Display depth:")
        rowDepth.prop(bgimageprops, "display_depth", expand=True)
    
        rowMethod = boxBGImage.row()
        rowMethod.label(text="Frame Method:")
        rowMethod.prop(bgimageprops, "frame_method", expand=True)

        rowAssign = boxBGImage.row()
        rowAssign.operator('setupauto.ot_bgimage', text = "Assign Images!")
