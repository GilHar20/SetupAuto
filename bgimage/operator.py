import bpy
import os
import re



class SETUPAUTO_OT_bgimage(bpy.types.Operator):
    '''Class assigns background images to cameras'''
    bl_idname = "setupauto.ot_bgimage"
    bl_label = "bg image"
    bl_description = "Operator assigns the background images to all selected camera from a selected folder location"

    def execute(self, context):
        bg_props = context.scene.bgimage_props
        
        background_folder_path = bg_props.bgimage_folder_path

        cameras = bpy.context.selected_objects

        scene = bpy.context.scene
        
        # Set initial resolution based on user preference
        if not bg_props.auto_detect_resolution:
            scene.render.resolution_x = bg_props.resolution_x
            scene.render.resolution_y = bg_props.resolution_y

        # Track if we've successfully loaded an image to get dimensions
        first_image_loaded = False
        detected_resolution_x = None
        detected_resolution_y = None

        for camera in cameras:

            if camera.type == 'CAMERA':
                base_name, _ = os.path.splitext(camera.name)
                background_image_path = os.path.join(background_folder_path, base_name + bg_props.image_fornmat)

                # Try exact match first
                background_image = None
                try:
                    background_image = bpy.data.images.load(background_image_path)
                    print(f"Exact match found for {camera.name}: {background_image_path}")
                except Exception as e:
                    print(f"Exact match failed for {camera.name}: {e}")
                    
                    # Fallback: Try to find sequential number in camera name
                    sequential_match = re.search(r'_(\d{4})_', camera.name)
                    if sequential_match:
                        sequential_number = sequential_match.group(1)
                        print(f"Trying sequential number match: {sequential_number}")
                        
                        # Look for any file with the same sequential number
                        try:
                            for filename in os.listdir(background_folder_path):
                                if sequential_number in filename and filename.endswith(bg_props.image_fornmat):
                                    fallback_path = os.path.join(background_folder_path, filename)
                                    background_image = bpy.data.images.load(fallback_path)
                                    print(f"Sequential match found for {camera.name}: {fallback_path}")
                                    break
                        except Exception as e2:
                            print(f"Sequential match also failed for {camera.name}: {e2}")
                            continue
                    else:
                        print(f"No sequential number pattern found in camera name: {camera.name}")
                        continue

                if background_image is None:
                    print(f"Could not load any image for {camera.name}")
                    continue

                # Get image dimensions from the first successfully loaded image (only if auto-detect is enabled)
                if not first_image_loaded and bg_props.auto_detect_resolution:
                    detected_resolution_x = background_image.size[0]
                    detected_resolution_y = background_image.size[1]
                    first_image_loaded = True
                    print(f"Detected image dimensions: {detected_resolution_x}x{detected_resolution_y}")
                    
                    # Update scene resolution with detected dimensions
                    scene.render.resolution_x = detected_resolution_x
                    scene.render.resolution_y = detected_resolution_y
                    print(f"Updated scene resolution to: {detected_resolution_x}x{detected_resolution_y}")
                elif not first_image_loaded:
                    first_image_loaded = True
                    if not bg_props.auto_detect_resolution:
                        print(f"Using manual resolution settings: {bg_props.resolution_x}x{bg_props.resolution_y}")
                    else:
                        print("Auto-detection enabled but no image loaded yet")

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
                bgimage.alpha = bg_props.opacity
            
            else:
                print(str(camera.name) + "camera does not exist")

        return {'FINISHED'}
