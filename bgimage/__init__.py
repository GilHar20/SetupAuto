import bpy

# Bgimage module registration
from . import properties, operator, ui

classes = [
    properties.SETUPAUTO_PG_bgimage_props,
    operator.SETUPAUTO_OT_bgimage,
    ui.SETUPAUTO_PT_bgimage_panel,
]

def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bgimage_props = bpy.props.PointerProperty(type=properties.SETUPAUTO_PG_bgimage_props)

def unregister():
    # Unregister classes
    if hasattr(bpy.types.Scene, 'bgimage_props'):
        delattr(bpy.types.Scene, 'bgimage_props')

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)