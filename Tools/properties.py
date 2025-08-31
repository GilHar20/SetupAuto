import bpy



class SETUPAUTO_PG_tools_props (bpy.types.PropertyGroup):
    proximity : bpy.props.FloatProperty(
        name = "Proximity",
        default = 1.5,
        min = 0.1,
        max = 1000
    )



def register():
    bpy.utils.register_class(SETUPAUTO_PG_tools_props)

def unregister():
    bpy.utils.unregister_class(SETUPAUTO_PG_tools_props)