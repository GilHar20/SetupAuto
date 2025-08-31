bl_info = {
    "name": "SetupAuto",
    "version": (1, 2, 0),
    "blender": (4, 5, 0),
    "author": "Gilad Harnik",
    "location": "View3D > Tool Shelf",
    "description": "A plugin to help setup imported files in Blender, made for archviz.",
    "category": "3D View",
    "git_url": "https://github.com/GilHar20/AutoSetup.git",
    "git_branch": "main",
    "git_commit": "main",
    "tracker_url": "https://github.com/GilHar20/AutoSetup/issues",
    "doc_url": "https://github.com/GilHar20/AutoSetup",
}

import bpy
from .quicksort import register as register_quicksort, unregister as unregister_quicksort
from .bgimage import register as register_bgimage, unregister as unregister_bgimage
from .Tools import register as register_Tools, unregister as unregister_Tools

# Import the addon updater
from . import addon_updater_ops


#==============================================



class SetupAutoPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    # Addon updater preferences
    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False)

    updater_interval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0)

    updater_interval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31)

    updater_interval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23)

    updater_interval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59)

    def draw(self, context):
        layout = self.layout
        
        # Update section
        box = layout.box()
        box.label(text="Update Addon", icon='FILE_REFRESH')
        
        # Display current version
        row = box.row()
        row.label(text=f"Current Version: {bl_info['version'][0]}.{bl_info['version'][1]}.{bl_info['version'][2]}")
        
        # Display repository info
        row = box.row()
        row.label(text=f"Repository: {bl_info['git_url']}")
        
        row = box.row()
        row.label(text=f"Branch: {bl_info['git_branch']}")
        
        # Addon updater UI - this provides the update functionality
        addon_updater_ops.update_settings_ui(self, context)
        
        # Documentation links
        box = layout.box()
        box.label(text="Documentation & Support", icon='HELP')
        
        row = box.row()
        row.operator("wm.url_open", text="GitHub Repository", icon='URL').url = bl_info['doc_url']
        
        row = box.row()
        row.operator("wm.url_open", text="Report Issues", icon='URL').url = bl_info['tracker_url']


#==============================================



def register():
    # Addon updater code and configurations.
    # In case of a broken version, try to register the updater first so that
    # users can revert back to a working version.
    addon_updater_ops.register(bl_info)
    
    # Register preferences class
    addon_updater_ops.make_annotations(SetupAutoPreferences)  # Avoid blender 2.8 warnings
    bpy.utils.register_class(SetupAutoPreferences)
    
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
    # Addon updater unregister
    addon_updater_ops.unregister()
    
    # Unregister preferences class
    bpy.utils.unregister_class(SetupAutoPreferences)
    
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