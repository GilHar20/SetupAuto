import bpy



class SETUPAUTO_PG_manager_props (bpy.types.PropertyGroup):

    inactivity_period : bpy.props.IntProperty(
        name = "Inactivity Period",
        description= "Amount of time, in minutes, before the timer stops counting",
        default = 10,
        min = 1,
        max = 120
    )
    
    auto_start_timer : bpy.props.BoolProperty(
        name = "Auto Start Timer",
        description = "Automatically start timer when opening a file",
        default = False
    )
