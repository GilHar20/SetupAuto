import bpy
import os
import re



class SETUPAUTO_OT_bgimage(bpy.types.Operator):
    '''Class assigns background images to cameras'''
    bl_idname = "setupauto.ot_bgimage"
    bl_label = "bg image"
    bl_description = "Operator assigns the background images to all selected camera from a selected folder location"
    bl_options = {'REGISTER', 'UNDO'}


    def exact_match(self, context, camera, background_folder_path):
        bg_props = context.scene.bgimage_props
        
        base_name, _ = os.path.splitext(camera.name)
        background_image_path = os.path.join(background_folder_path, base_name + "." + bg_props.image_format)

        background_image = None

        try:
            background_image = bpy.data.images.load(background_image_path)
            print(f"Exact match found for {camera.name}: {background_image_path}")
            return background_image
        
        except Exception as e:
            print(f"Exact match failed for {camera.name}: {e}")
            return background_image


    def sequential_match(self, context, camera, background_folder_path):
        bg_props = context.scene.bgimage_props
        
        background_image = None

        sequential_match = re.search(r'(\d+)', camera.name)
        if not sequential_match:
            print(f"No sequential number pattern found in camera name: {camera.name}")
            return background_image  
        else:    
            sequential_number = sequential_match.group(1)
            print(f"Trying sequential number match: {sequential_number}")
            
            for filename in os.listdir(background_folder_path):
                if sequential_number in filename and filename.endswith(bg_props.image_format):
                    background_image_path = os.path.join(background_folder_path, filename)
                    background_image = bpy.data.images.load(background_image_path)
                    print(f"Sequential match found for {camera.name}: {background_image_path}")
                    return background_image


    def execute(self, context):
        bg_props = context.scene.bgimage_props
        scene = context.scene

        background_folder_path = bg_props.folder_path
        auto_detect_resolution = bg_props.autodetect_resolution
        cameras = [obj for obj in bpy.context.selected_objects if obj.type == 'CAMERA']
        failed = 0

        if background_folder_path == "":
            self.report({'WARNING'}, "You must specify a folder path!")
            return {'CANCELLED'}
        
        if cameras == []:
            self.report({'WARNING'}, "You must select atleast one camera!")
            return {'CANCELLED'}            
        
        # Set initial resolution based on user preference
        if not auto_detect_resolution:
            scene.render.resolution_x = bg_props.resolution_x
            scene.render.resolution_y = bg_props.resolution_y

        # Track if we've successfully loaded an image to get dimensions
        first_image = True
        detected_resolution_x = None
        detected_resolution_y = None

        for camera in cameras:
            
            background_image = self.exact_match(context, camera, background_folder_path)

            if background_image == None:
                # try sequentail
                background_image = self.sequential_match(context, camera, background_folder_path)

            if background_image is None:
                print(f"Could not load any image for {camera.name}")
                failed += 1
                continue

            # Get image dimensions from the first successfully loaded image (only if auto-detect is enabled)
            if first_image and auto_detect_resolution:
                detected_resolution_x = background_image.size[0]
                detected_resolution_y = background_image.size[1]
                first_image = False
                print(f"Detected image dimensions: {detected_resolution_x}x{detected_resolution_y}")
                
                # Update scene resolution with detected dimensions
                scene.render.resolution_x = detected_resolution_x
                scene.render.resolution_y = detected_resolution_y
                print(f"Updated scene resolution to: {detected_resolution_x}x{detected_resolution_y}")
            elif first_image:
                first_image = False

            camera.data.show_background_images = True

            if len(camera.data.background_images) == 0:
                camera.data.background_images.new()
                camera.data.background_images[0].image = background_image
                bgimage = camera.data.background_images[0]
            
            else:
                camera.data.background_images.clear()
                camera.data.background_images.new()
                camera.data.background_images[0].image = background_image
                bgimage = camera.data.background_images[0]

            bgimage.display_depth = bg_props.display_depth
            bgimage.frame_method = bg_props.frame_method
            bgimage.alpha = bg_props.opacity

        if failed == 0:
            self.report({'INFO'}, "Success! All images matched to a camera")            
        elif failed == len(cameras):
            self.report({'INFO'}, "Failure! No imaged matched a camera")
        else:
            self.report({'INFO'}, str(failed) + " of images could not be matched to a camera")
        return {'FINISHED'}
