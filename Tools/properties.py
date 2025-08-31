import bpy



class SETUPAUTO_PG_tools_props (bpy.types.PropertyGroup):
    proximity : bpy.props.FloatProperty(
        name = "Proximity",
        default = 1.5,
        min = 0.1,
        max = 1000
    )
