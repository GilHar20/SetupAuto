import bpy
import os



#==============================================


class SETUPAUTO_PG_bgimage_props (bpy.types.PropertyGroup):
    resolution_x : bpy.props.IntProperty(
        name = "Resolution X",
        default = 1920
    )

    resolution_y : bpy.props.IntProperty(
        name = "Resolution Y",
        default = 1080
    )

    image_fornmat : bpy.props.StringProperty(
        name = "Image format",
        default = ""
    )

    bgimage_folder_path : bpy.props.StringProperty(
        name = "Images folder path",
        default = "",
        subtype = 'DIR_PATH'
    )

    alpha : bpy.props.FloatProperty(
        name = "Alpha",
        default = 1.0
    )

    frame_method : bpy.props.EnumProperty(
        name = "Frame Method",
        description = "",
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


#==============================================


class SETUPAUTO_OT_bgimage(bpy.types.Operator):
    '''Class sorts objects'''
    bl_idname = "setupauto.ot_bgimage"
    bl_label = "bg image"
    bl_description = "Operator assigns the background images to all selected camera from a selected folder location"

    def execute(self, context):
        bg_props = context.scene.bgimage_props
        
        background_folder_path = bg_props.bgimage_folder_path

        cameras = bpy.context.selected_objects

        scene = bpy.context.scene
        scene.render.resolution_x = bg_props.resolution_x
        scene.render.resolution_y = bg_props.resolution_y

        for camera in cameras:

            if camera.type == 'CAMERA':
                base_name, _ = os.path.splitext(camera.name)
                background_image_path = os.path.join(background_folder_path, base_name + bg_props.image_fornmat)

                try:
                    background_image = bpy.data.images.load(background_image_path)
                
                except Exception as e:
                    print(f"Failed to load image for {camera.name}: {e}")
                    continue
                
                camera.data.show_background_images = True

                if len(camera.data.background_images) == 0:
                    camera.data.background_images.new()
                    camera.data.background_images[0].image = background_image
                    bgimage = camera.data.background_images[0]
                
                else:
                    camera.data.background_images[0].image = background_image
                    bgimage = camera.data.background_images[0]

                bgimage.display_depth = bg_props.display_depth
                bgimage.frame_method = bg_props.frame_method
                bgimage.alpha = bg_props.alpha
            
            else:
                print(str(camera.name) + "camera does not exist")

        return {'FINISHED'}