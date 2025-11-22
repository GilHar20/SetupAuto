import bpy

# Quicksort module registration
from . import properties, operator, patternsdetection, ui

classes = [
    properties.SETUPAUTO_PG_pattern_props,
    properties.SETUPAUTO_PG_quicksort_props,
    properties.SETUPAUTO_OT_add_pattern,
    properties.SETUPAUTO_OT_remove_pattern,
    properties.SETUPAUTO_OT_clear_patterns,
    properties.SETUPAUTO_OT_select_pattern,
    operator.SETUPAUTO_OT_quicksort,
    patternsdetection.SETUPAUTO_OT_patternsdetection,
    ui.SETUPAUTO_UL_pattern_list,
    ui.SETUPAUTO_PT_quicksort_panel
]

def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.pattern_props = bpy.props.CollectionProperty(type=properties.SETUPAUTO_PG_pattern_props)
    bpy.types.Scene.quicksort_props = bpy.props.PointerProperty(type=properties.SETUPAUTO_PG_quicksort_props)
    bpy.types.Scene.pattern_index = bpy.props.IntProperty(name="QuickSort Pattern Index", default=0)

def unregister():
    # Unregister classes
    if hasattr(bpy.types.Scene, 'pattern_props'):
        delattr(bpy.types.Scene, 'pattern_props')
    if hasattr(bpy.types.Scene, 'quicksort_props'):
        delattr(bpy.types.Scene, 'quicksort_props')

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)