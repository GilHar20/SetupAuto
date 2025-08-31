bl_info = {
    "name": "SetupAuto",
    "version": (1, 2, 0),
    "blender": (4, 5, 0),
    "author": "Gilad Harnik",
    "location": "View3D > Tool Shelf",
    "description": "A plugin to help setup imported files from CAD software in Blender, made for archviz.",
    "category": "3D View",
}

import bpy
from .quicksort import register as register_quicksort, unregister as unregister_quicksort
from .bgimage import register as register_bgimage, unregister as unregister_bgimage
from .Tools import register as register_Tools, unregister as unregister_Tools



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


def register():
    bpy.utils.register_class(MyAddonPreferences)
    bpy.utils.register_class(WM_OT_UpdateAddon)
    
    # Register modules
    register_quicksort()
    register_bgimage()
    register_Tools()

    # Create a collection property to hold multiple pattern property groups
    from .quicksort.properties import SETUPAUTO_PG_quicksort_props
    from .bgimage.properties import SETUPAUTO_PG_bgimage_props
    from .Tools.properties import SETUPAUTO_PG_tools_props
    
    bpy.types.Scene.pattern_props = bpy.props.CollectionProperty(type=SETUPAUTO_PG_quicksort_props)
    bpy.types.Scene.bgimage_props = bpy.props.PointerProperty(type=SETUPAUTO_PG_bgimage_props)
    bpy.types.Scene.tools_props = bpy.props.PointerProperty(type=SETUPAUTO_PG_tools_props)

def unregister():
    bpy.utils.unregister_class(MyAddonPreferences)
    bpy.utils.unregister_class(WM_OT_UpdateAddon)    
    
    # Unregister modules
    unregister_bgimage()
    unregister_quicksort()
    unregister_Tools()

    del bpy.types.Scene.pattern_props
    del bpy.types.Scene.bgimage_props
    del bpy.types.Scene.tools_props



#==============================================


if __name__ == "__main__":
    register()