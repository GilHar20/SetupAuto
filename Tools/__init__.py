import bpy

# Tools module registration
from . import properties, clearcustomnormals, smartapply, smartselect, proximityjoin, singleuser, duplicates2instances, ui

classes = [
    clearcustomnormals.SETUPAUTO_OT_removecustomnormals,
    properties.SETUPAUTO_PG_tools_props,
    smartapply.SETUPAUTO_OT_smartapply,
    smartselect.SETUPAUTO_OT_smartselect,
    proximityjoin.SETUPAUTO_OT_proxjoin,
    singleuser.SETUPAUTO_OT_singleuser,
    duplicates2instances.SETUPAUTO_OT_dups2inst,
    ui.SETUPAUTO_PT_tools_panel
]

def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.tools_props = bpy.props.PointerProperty(type=properties.SETUPAUTO_PG_tools_props)

def unregister():
    # Unregister classes
    if hasattr(bpy.types.Scene, 'tools_props'):
        delattr(bpy.types.Scene, 'tools_props')

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)