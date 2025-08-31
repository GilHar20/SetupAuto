import bpy



class SETUPAUTO_PT_quicksort_panel(bpy.types.Panel):
    '''Class draws quicksort UI panel'''
    bl_idname = "setupauto.pt_quicksort_panel"
    bl_label = "Quick Sort Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SetupAuto"

    def draw(self, context):
        layout = self.layout
        patternprops = context.scene.pattern_props
        
        # quick sort settings:
        box1 = layout.box()
        header = box1.row()
        header.label(text = "Quick Sort: ")

        # Show collection length and add/remove buttons
        rowtop = box1.row()
        rowtop.label(text=f"Number of patterns: {len(patternprops)}")
        
        row_buttons = box1.row()
        row_buttons.operator("setupauto.add_pattern", text="Add Pattern", icon='ADD')
        if len(patternprops) > 0:
            row_buttons.operator("setupauto.remove_pattern", text="Remove Pattern", icon='REMOVE')

        # Ensure there's at least one pattern item
        if len(patternprops) == 0:
            # Add a default pattern if none exists
            patternprops.add()

        # Draw pattern properties for each item in the collection
        for i, pattern_item in enumerate(patternprops):
            row1 = box1.row()
            column1 = row1.column(align=True)
            column1.prop(pattern_item, "pattern_name", text=f"#{i+1} name")
            
            column2 = row1.column(align=True)
            column2.prop(pattern_item, "pattern_sample", text=f"sample")

            column3 = row1.column(align=True)
            column3.prop(pattern_item, "pattern_action", text=f"action")

        row8 = box1.row()
        row8.alignment = 'CENTER'
        row8.operator('setupauto.ot_quicksort', text = "Quick Sort!")



def register():
    bpy.utils.register_class(SETUPAUTO_PT_quicksort_panel)

def unregister():
    bpy.utils.unregister_class(SETUPAUTO_PT_quicksort_panel)
