bl_info = {
    "name": "SetupAuto",
    "version": (1, 2, 0),
    "blender": (4, 5, 0),
    "author": "Gilad Harnik",
    "location": "View3D > Tool Shelf",
    "description": "A plugin to help setup imported files in Blender, made for archviz.",
    "category": "3D View",
    "git_url": "https://github.com/GilHar20/SetupAuto.git",
    "git_branch": "main",
    "git_commit": "main",
    "tracker_url": "https://github.com/GilHar20/SetupAuto/issues",
    "doc_url": "https://github.com/GilHar20/SetupAuto",
}

import bpy

# Import all modules to ensure classes are available for auto-registration
from . import quicksort
from . import bgimage
from . import Tools

# Import the addon updater (not part of auto-registration)
from . import addon_updater_ops

# Import the auto-registration system
from . import auto_registration


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
    # Register preferences class (not part of auto-registration)
    addon_updater_ops.make_annotations(SetupAutoPreferences)  # Avoid blender 2.8 warnings
    bpy.utils.register_class(SetupAutoPreferences)
    
    # Use auto-registration system for all classes (including addon updater)
    auto_registration.register()
    
    # Configure addon updater (after classes are registered)
    addon_updater_ops.register(bl_info)

def unregister():
    # Addon updater unregister (before classes are unregistered)
    addon_updater_ops.unregister()
    
    # Unregister preferences class (not part of auto-registration)
    bpy.utils.unregister_class(SetupAutoPreferences)
    
    # Use auto-registration system to unregister all classes
    auto_registration.unregister()


#==============================================



if __name__ == "__main__":
    register()