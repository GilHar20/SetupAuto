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
    
    # TEMPORARY: Manual registration instead of auto-registration
    print("Manual registration starting...")
    
    # Import and register all classes manually
    from .quicksort.ui import SETUPAUTO_PT_quicksort_panel
    from .quicksort.operator import SETUPAUTO_OT_quicksort
    from .quicksort.properties import SETUPAUTO_PG_quicksort_props, SETUPAUTO_OT_add_pattern, SETUPAUTO_OT_remove_pattern
    
    from .bgimage.ui import SETUPAUTO_PT_bgimage_panel
    from .bgimage.operator import SETUPAUTO_OT_bgimage
    from .bgimage.properties import SETUPAUTO_PG_bgimage_props
    
    from .Tools.ui import SETUPAUTO_PT_tools_panel
    from .Tools.properties import SETUPAUTO_PG_tools_props
    from .Tools.proximityjoin import SETUPAUTO_OT_proxjoin
    from .Tools.duplicates2instances import SETUPAUTO_OT_dups2inst
    from .Tools.smartapply import SETUPAUTO_OT_smartapply
    from .Tools.singleuser import SETUPAUTO_OT_singleuser
    from .Tools.purgeunused import SETUPAUTO_OT_purgeunused
    
    # Register PropertyGroups first
    bpy.utils.register_class(SETUPAUTO_PG_quicksort_props)
    bpy.utils.register_class(SETUPAUTO_PG_bgimage_props)
    bpy.utils.register_class(SETUPAUTO_PG_tools_props)
    
    # Register UI panels
    bpy.utils.register_class(SETUPAUTO_PT_quicksort_panel)
    bpy.utils.register_class(SETUPAUTO_PT_bgimage_panel)
    bpy.utils.register_class(SETUPAUTO_PT_tools_panel)
    
    # Register operators
    
    bpy.utils.register_class(SETUPAUTO_OT_add_pattern)
    bpy.utils.register_class(SETUPAUTO_OT_remove_pattern)
    bpy.utils.register_class(SETUPAUTO_OT_quicksort)
    bpy.utils.register_class(SETUPAUTO_OT_bgimage)
    bpy.utils.register_class(SETUPAUTO_OT_proxjoin)
    bpy.utils.register_class(SETUPAUTO_OT_dups2inst)
    bpy.utils.register_class(SETUPAUTO_OT_smartapply)
    bpy.utils.register_class(SETUPAUTO_OT_singleuser)
    bpy.utils.register_class(SETUPAUTO_OT_purgeunused)
    
    # Register properties
    bpy.types.Scene.pattern_props = bpy.props.CollectionProperty(type=SETUPAUTO_PG_quicksort_props)
    bpy.types.Scene.bgimage_props = bpy.props.PointerProperty(type=SETUPAUTO_PG_bgimage_props)
    bpy.types.Scene.tools_props = bpy.props.PointerProperty(type=SETUPAUTO_PG_tools_props)
    
    print("Manual registration complete!")
    
    # Use auto-registration system for all classes (including addon updater)
    # auto_registration.register()
    
    # Configure addon updater (after classes are registered)
    addon_updater_ops.register(bl_info)

def unregister():
    # Addon updater unregister (before classes are unregistered)
    addon_updater_ops.unregister()
    
    # Unregister preferences class (not part of auto-registration)
    bpy.utils.unregister_class(SetupAutoPreferences)
    
    # Manual unregistration
    print("Manual unregistration starting...")
    
    # Unregister properties first
    if hasattr(bpy.types.Scene, 'pattern_props'):
        delattr(bpy.types.Scene, 'pattern_props')
    if hasattr(bpy.types.Scene, 'bgimage_props'):
        delattr(bpy.types.Scene, 'bgimage_props')
    if hasattr(bpy.types.Scene, 'tools_props'):
        delattr(bpy.types.Scene, 'tools_props')
    
    # Unregister operators
    from .Tools.purgeunused import SETUPAUTO_OT_purgeunused
    from .Tools.singleuser import SETUPAUTO_OT_singleuser
    from .Tools.smartapply import SETUPAUTO_OT_smartapply
    from .Tools.duplicates2instances import SETUPAUTO_OT_dups2inst
    from .Tools.proximityjoin import SETUPAUTO_OT_proxjoin
    from .bgimage.operator import SETUPAUTO_OT_bgimage
    from .quicksort.operator import SETUPAUTO_OT_quicksort
    from .quicksort.properties import SETUPAUTO_OT_add_pattern, SETUPAUTO_OT_remove_pattern
    
    bpy.utils.unregister_class(SETUPAUTO_OT_purgeunused)
    bpy.utils.unregister_class(SETUPAUTO_OT_singleuser)
    bpy.utils.unregister_class(SETUPAUTO_OT_smartapply)
    bpy.utils.unregister_class(SETUPAUTO_OT_dups2inst)
    bpy.utils.unregister_class(SETUPAUTO_OT_proxjoin)
    bpy.utils.unregister_class(SETUPAUTO_OT_bgimage)
    bpy.utils.unregister_class(SETUPAUTO_OT_quicksort)
    bpy.utils.unregister_class(SETUPAUTO_OT_add_pattern)
    bpy.utils.unregister_class(SETUPAUTO_OT_remove_pattern)
    
    # Unregister UI panels
    from .Tools.ui import SETUPAUTO_PT_tools_panel
    from .bgimage.ui import SETUPAUTO_PT_bgimage_panel
    from .quicksort.ui import SETUPAUTO_PT_quicksort_panel
    
    bpy.utils.unregister_class(SETUPAUTO_PT_tools_panel)
    bpy.utils.unregister_class(SETUPAUTO_PT_bgimage_panel)
    bpy.utils.unregister_class(SETUPAUTO_PT_quicksort_panel)
    
    # Unregister PropertyGroups
    from .Tools.properties import SETUPAUTO_PG_tools_props
    from .bgimage.properties import SETUPAUTO_PG_bgimage_props
    from .quicksort.properties import SETUPAUTO_PG_quicksort_props
    
    bpy.utils.unregister_class(SETUPAUTO_PG_tools_props)
    bpy.utils.unregister_class(SETUPAUTO_PG_bgimage_props)
    bpy.utils.unregister_class(SETUPAUTO_PG_quicksort_props)
    
    print("Manual unregistration complete!")
    
    # Use auto-registration system to unregister all classes
    # auto_registration.unregister()


#==============================================



if __name__ == "__main__":
    register()