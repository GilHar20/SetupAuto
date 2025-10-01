import bpy

# Quicksort module registration
from . import properties, operator, patternsdetection, ui

classes = [
    properties.SETUPAUTO_PG_quicksort_props,
    operator.SETUPAUTO_OT_quicksort,
    patternsdetection.SETUPAUTO_OT_patternsdetection,
    ui.SETUPAUTO_PT_quicksort_panel
]

def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.pattern_props = bpy.props.CollectionProperty(type=properties.SETUPAUTO_PG_quicksort_props)

def unregister():
    # Unregister classes
    if hasattr(bpy.types.Scene, 'pattern_props'):
        delattr(bpy.types.Scene, 'pattern_props')

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)