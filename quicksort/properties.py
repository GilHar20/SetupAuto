import bpy



class SETUPAUTO_PG_quicksort_props (bpy.types.PropertyGroup):
    main_collection : bpy.props.PointerProperty(
        name = "Main Collection",
        description = "Main collection to cotain all new created collections. Leave empty to link to scene collection.",
        type = bpy.types.Collection
    )

class SETUPAUTO_PG_pattern_props (bpy.types.PropertyGroup):
    pattern_sample : bpy.props.StringProperty(
        name = "Pattern Sample",
        description = "The string pattern used to select objects.",
        default = ""
    )

    output_collection : bpy.props.StringProperty(
        name = "Output Collection",
        description = "Collection to contain all objects selected by this pattern will be stored with this name." \
        "If empty, the collection will be named the same as the pattern sample.",
        default = ""
    )

    parent_collection : bpy.props.PointerProperty(
        name = "Parent Collection",
        description = "Collection to contain the new Output Collection. Leave empty to link Output Collection to Main Collection." \
        "If Main Collection also empty, Output Collection will link to scene collection.",
        type = bpy.types.Collection
    )

    pattern_action : bpy.props.EnumProperty(
        name = "Pattern Action",
        description = "Operation to perform on objects selected by the pattern.",
        items = [
        ('ORGANIZE', "Organize", "Organize objects"),
        ('RENAME', "Rename", "Rename objects"),
        ('JOIN', "Join", "Join objects"),
        ('DELETE', "Delete", "Delete objects"),
        ],
        default = 'ORGANIZE'
    )

    new_name : bpy.props.StringProperty(
        name="New Name",
        description="New name to give all new linked objects. NOTE! Will name ALL selected objects!",
        default=""
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

    pattern_index : bpy.props.IntProperty(
        name = "pattern index",
        default = -1
    )

    def execute(self, context):
        pattern_props = context.scene.pattern_props

        if len(pattern_props) == 0:
            self.report({'INFO'}, "Pattern list is empty.")
            
        if self.pattern_index == -1:
            pattern_props.remove(len(pattern_props) - 1)
        
        else:
            pattern_props.remove(self.pattern_index)
            self.pattern_index = -1
        
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