import bpy



class SETUPAUTO_PG_quicksort_props (bpy.types.PropertyGroup):
    main_collection : bpy.props.PointerProperty(
        name = "Main Collection",
        description = "Main collection to cotain all created collections. Leave empty to link to scene collection",
        type = bpy.types.Collection
    )



class SETUPAUTO_PG_pattern_props (bpy.types.PropertyGroup):
    pattern_name : bpy.props.StringProperty(
        name = "Pattern name",
        default = ""
    )

    pattern_sample : bpy.props.StringProperty(
        name = "Pattern sample",
        default = ""
    )

    pattern_action : bpy.props.EnumProperty(
        name = "Pattern Method",
        description = "Operation to perform on objects selected by the pattern",
        items = [
        ('ORGANIZE', "Organize", "Organize objects"),
        ('JOIN', "Join", "Join objects"),
        ('DELETE', "Delete", "Delete objects"),
        ],
        default = 'ORGANIZE'
    )

    parent_collection : bpy.props.PointerProperty(
        name = "Parent Collection",
        description = "Parent collection to link the new collection under. Leave empty to link to scene collection",
        type = bpy.types.Collection
    )

class SETUPAUTO_OT_add_pattern(bpy.types.Operator):
    '''Add a new pattern to the collection'''
    bl_idname = "setupauto.add_pattern"
    bl_label = "Add Pattern"
    bl_description = "Add a new pattern to the collection"

    def execute(self, context):
        context.scene.pattern_props.add()
        return {'FINISHED'}



class SETUPAUTO_OT_remove_pattern(bpy.types.Operator):
    '''Remove the last pattern from the collection'''
    bl_idname = "setupauto.remove_pattern"
    bl_label = "Remove Pattern"
    bl_description = "Remove the last pattern from the collection"

    def execute(self, context):
        if len(context.scene.pattern_props) > 0:
            context.scene.pattern_props.remove(len(context.scene.pattern_props) - 1)
        return {'FINISHED'}



class SETUPAUTO_OT_clear_patterns(bpy.types.Operator):
    '''Clears all patterns from the collection'''
    bl_idname = "setupauto.clear_patterns"
    bl_label = "Clear Patterns"
    bl_description = "Clears all patterns from the collection"

    def execute(self, context):
        if len(context.scene.pattern_props) > 0:
            bpy.context.scene.pattern_props.clear()
        return {'FINISHED'}