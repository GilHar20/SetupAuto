import bpy



#==============================================


class SETUPAUTO_PG_quicksort_props (bpy.types.PropertyGroup):
    window_pattern : bpy.props.StringProperty(
        name = "Windows pattern",
        default = ""
    )

    wall_pattern : bpy.props.StringProperty(
        name = "Walls pattern",
        default = ""
    )

    railings_pattern : bpy.props.StringProperty(
        name = "Railings pattern",
        default = ""
    )

    floor_pattern : bpy.props.StringProperty(
        name = "Floors pattern",
        default = ""
    )

    preserve_pattern : bpy.props.StringProperty(
        name = "Preservence pattern",
        default = ""
    )

    shutter_pattern : bpy.props.StringProperty(
        name = "Shutters pattern",
        default = ""
    )

    road_pattern : bpy.props.StringProperty(
        name = "Roads pattern",
        default = ""
    )


#==============================================


class SETUPAUTO_OT_quicksort(bpy.types.Operator):
    '''Class sorts objects'''
    bl_idname = "setupauto.ot_quicksort"
    bl_label = "Sort objects"
    bl_description = "Operator sorts all MESH objects in scene into collection based on string patterns"

    def execute(self, context):
        pattern_props = context.scene.pattern_props

        patterns = {
            "Windows": pattern_props.window_pattern,
            "Walls": pattern_props.wall_pattern,
            "Railings": pattern_props.railings_pattern,
            "Floors": pattern_props.floor_pattern,
            "Preserve": pattern_props.preserve_pattern,
            "Shutters": pattern_props.shutter_pattern,
            "Roads": pattern_props.road_pattern
        }

        for name, pattern in patterns.items():
            if not pattern:
                print("no pattern defined")
                continue

            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern="*" + pattern + "*")

            if name not in bpy.data.collections:
                collection = bpy.data.collections.new(name)
                context.scene.collection.children.link(collection)
            else:
                collection = bpy.data.collections[name]
                                                  
            for obj in bpy.context.selected_objects:
                originalCollection = obj.users_collection[0]
                originalCollection.objects.unlink(obj)
                collection.objects.link(obj)
            
            bpy.ops.object.select_all(action='DESELECT')

            print(name)
        
        return {'FINISHED'}