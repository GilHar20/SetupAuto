import bpy



class SETUPAUTO_PG_tools_props (bpy.types.PropertyGroup):
    # Proximity Join Properties
    proximity : bpy.props.FloatProperty(
        name = "Proximity",
        description = "Maximum distance to merge objects.",
        default = 1.5,
        min = 0.1,
        max = 1000
    )
    
    # Proximity Join Axis Selection
    proximity_x : bpy.props.BoolProperty(
        name = "Proximity X",
        description = "Consider X axis for proximity calculation.",
        default = True
    )
    
    proximity_y : bpy.props.BoolProperty(
        name = "Proximity Y", 
        description = "Consider Y axis for proximity calculation.",
        default = True
    )

    proximity_z : bpy.props.BoolProperty(
        name = "Proximity Z",
        description = "Consider Z axis for proximity calculation.", 
        default = True
    )



    # Purge Unsused Data Properties
    do_local : bpy.props.BoolProperty(
        name = "Do Local Data",
        description = "Check to perform purge on data stored in this file.",
        default= True
    )

    do_linked : bpy.props.BoolProperty(
        name = "Do Linked Data",
        description = "Check to perform purge on data linked to this file.",
        default= True
    )

    do_recursive : bpy.props.BoolProperty(
        name = "Do Recursive Data",
        description = "Check to perform recursive purge on data.",
        default= True
    )



    # Smart Apply Properties
    location : bpy.props.BoolProperty(
        name = "Apply Location",
        default= False
    )

    rotation : bpy.props.BoolProperty(
        name = "Apply Rotation",
        default= False
    )

    scale : bpy.props.BoolProperty(
        name = "Apply Scale",
        default= True
    ) 