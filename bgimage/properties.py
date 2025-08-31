import bpy



class SETUPAUTO_PG_bgimage_props (bpy.types.PropertyGroup):
    resolution_x : bpy.props.IntProperty(
        name = "Resolution X",
        default = 1920
    )

    resolution_y : bpy.props.IntProperty(
        name = "Resolution Y",
        default = 1080
    )

    bgimage_folder_path : bpy.props.StringProperty(
        name = "Images folder path",
        default = "",
        subtype = 'DIR_PATH'
    )

    opacity : bpy.props.FloatProperty(
        name = "Alpha",
        default = 1.0
    )

    frame_method : bpy.props.EnumProperty(
        name = "Frame Method",
        description = "Set background image frame method",
        items = [
        ('STRETCH', "Stretch", "Stretch image"),
        ('FIT', "Fit", "Fit image"),
        ('CROP', "Crop", "Crop image"),
        ],
        default = 'STRETCH'
    )

    display_depth : bpy.props.EnumProperty(
        name = "Display Depth",
        description = "Set background image diplay depth",
        items = [
        ('FRONT', "Front", "Disply in front of objects"),
        ('BACK', "Back", "Display behind objects"),
        ],
        default = 'BACK'
    )

    image_format : bpy.props.EnumProperty(
        name = "Image format",
        description = "Set background image frame method",
        items = [
        ('PNG', "PNG", "PNG image"),
        ('JPG', "JPG", "JPG image"),
        ('EXR', "EXR", "EXR image"),
        ('HDR', "HDR", "HDR image"),
        ],
        default = "JPG"
    )

    auto_detect_resolution : bpy.props.BoolProperty(
        name = "Auto-detect Resolution",
        description = "Automatically detect resolution from loaded images instead of using manual settings",
        default = True
    )
