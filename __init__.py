bl_info = {
    "name": "SetupAuto",
    "version": (1, 0, 1),
    "blender": (4, 3, 0),
    "author": "Gilad Harnik",
    "location": "View3D > Tool Shelf",
    "description": "A plugin to help setup imported files from CAD software in Blender, made for archviz.",
    "category": "3D View",
}

import bpy
from .quicksort import SETUPAUTO_OT_quicksort
from .quicksort import SETUPAUTO_PG_quicksort_props

from .bgimage import SETUPAUTO_OT_bgimage
from .bgimage import SETUPAUTO_PG_bgimage_props



#==============================================

import os
import shutil
import zipfile

class MyAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    update_filepath: bpy.props.StringProperty(
        name="Update File",
        description="Select the ZIP file to update the addon",
        subtype='FILE_PATH'
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Update Addon")

        # File selector for the ZIP file
        layout.prop(self, "update_filepath")

        # Button to trigger the update
        layout.operator("wm.update_addon", text="Update Addon")

class WM_OT_UpdateAddon(bpy.types.Operator):
    bl_idname = "wm.update_addon"
    bl_label = "Update Addon"

    def execute(self, context):
        preferences = context.preferences.addons.get("SetupAuto").preferences

        # Get the path to the selected ZIP file
        zip_path = preferences.update_filepath

        if not zip_path:
            self.report({'ERROR'}, "No ZIP file selected!")
            return {'CANCELLED'}

        # Get the directory of the current addon
        addon_dir = os.path.dirname(os.path.realpath(__file__))

        try:
            # Create a backup of the current addon
            backup_dir = addon_dir + "_backup"
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
            shutil.copytree(addon_dir, backup_dir)

            # Extract the ZIP file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(addon_dir)

            self.report({'INFO'}, "Addon updated successfully! Backup created at: " + backup_dir)

            # Reload the addon to apply changes
            bpy.ops.script.reload()

            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to update addon: {str(e)}")
            return {'CANCELLED'}


#==============================================


class SETUPAUTO_PT_mainpanel (bpy.types.Panel):
    '''Class draws UI panel'''
    bl_idname = "setupauto.pt_mainpanel"
    bl_label = "Setup Automation settings panel ahhhhhhhhhhhhhhhhh"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SetupAuto"

    def draw(self, context):
        layout = self.layout
        patternprops = context.scene.pattern_props
        bgimageprops = context.scene.bgimage_props

        # quick sort settings:
        box1 = layout.box()
        header = box1.row()
        header.label(text = "Quick Sort: ")

        row1 = box1.row()
        row1.prop(patternprops, "window_pattern")
        
        row2 = box1.row()    
        row2.prop(patternprops, "wall_pattern")

        row3 = box1.row()
        row3.prop(patternprops, "railings_pattern")

        row4 = box1.row()
        row4.prop(patternprops, "floor_pattern")

        row5 = box1.row()
        row5.prop(patternprops, "preserve_pattern")

        row6 = box1.row()
        row6.prop(patternprops, "shutter_pattern")

        row7 = box1.row()
        row7.prop(patternprops, "road_pattern")

        row8 = box1.row()
        row8.label(text = "Quick Sort:")
        row8.operator('setupauto.ot_quicksort', text = "Quick sort!")

        #bg image settings:
        box2 = layout.box()
        header = box2.row()
        header.label(text = "bgimage: ")
        
        row1 = box2.row()
        row1.prop(bgimageprops, "resolution_x")
        
        row2 = box2.row()    
        row2.prop(bgimageprops, "resolution_y")

        row3 = box2.row()
        row3.prop(bgimageprops, "bgimage_folder_path")

        row4 = box2.row()
        row4.prop(bgimageprops, "image_fornmat")

        row5 = box2.row()
        row5.prop(bgimageprops, "alpha")

        row6 = box2.row()
        row6.prop(bgimageprops, "frame_method")

        row7 = box2.row()
        row7.prop(bgimageprops, "display_depth")

        row10 = box2.row()
        row10.operator('setupauto.ot_bgimage', text = "Assign Images!")


#==============================================        


def register():
    bpy.utils.register_class(MyAddonPreferences)
    bpy.utils.register_class(WM_OT_UpdateAddon)
    
    bpy.utils.register_class(SETUPAUTO_OT_quicksort)
    bpy.utils.register_class(SETUPAUTO_PG_quicksort_props)
    
    bpy.utils.register_class(SETUPAUTO_OT_bgimage)
    bpy.utils.register_class(SETUPAUTO_PG_bgimage_props) 

    bpy.utils.register_class(SETUPAUTO_PT_mainpanel)

    bpy.types.Scene.pattern_props = bpy.props.PointerProperty(type = SETUPAUTO_PG_quicksort_props)
    bpy.types.Scene.bgimage_props = bpy.props.PointerProperty(type = SETUPAUTO_PG_bgimage_props)
    

def unregister():
    bpy.utils.unregister_class(MyAddonPreferences)
    bpy.utils.unregister_class(WM_OT_UpdateAddon)    
    
    bpy.utils.unregister_class(SETUPAUTO_OT_quicksort)
    bpy.utils.unregister_class(SETUPAUTO_PG_quicksort_props)

    bpy.utils.unregister_class(SETUPAUTO_OT_bgimage)
    bpy.utils.unregister_class(SETUPAUTO_PG_bgimage_props) 
    
    bpy.utils.unregister_class(SETUPAUTO_PT_mainpanel)

    del bpy.types.Scene.pattern_props
    del bpy.types.Scene.bgimage_props

#==============================================


if __name__ == "__main__":
    register()