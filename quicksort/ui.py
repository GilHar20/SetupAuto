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
        
        # Pattern Detection box:
        boxdetection = layout.box()
        header_pattern = boxdetection.row()
        header_pattern.label(text="Pattern Detection:")
        
        row_detection = boxdetection.row()
        row_detection.alignment = 'CENTER'
        row_detection.operator('setupauto.ot_patternsdetection', text="Detect Patterns!")
        
        # quick sort settings:
        boxsort = layout.box()
        header = boxsort.row()
        header.label(text = "Quick Sort: ")

        # Show collection length and add/remove buttons
        rowtop = boxsort.row()
        rowtop.label(text=f"Number of patterns: {len(patternprops)}")
        
        row_buttons = boxsort.row()
        row_buttons.operator("setupauto.add_pattern", text="Add Pattern", icon='ADD')
        if len(patternprops) > 0:
            row_buttons.operator("setupauto.remove_pattern", text="Remove Pattern", icon='REMOVE')

        # Draw pattern properties for each item in the collection - each in its own box
        # Only draw if there are patterns
        if len(patternprops) > 0:
            for i, pattern_item in enumerate(patternprops):
                # Create individual box for each pattern item
                pattern_box = boxsort.box()
                pattern_header = pattern_box.row()
                pattern_header.label(text=f"Pattern #{i+1}")
                
                # Action and parent collection properties on the same row
                row_action = pattern_box.row()
                column_action = row_action.column(align=True)
                column_action.prop(pattern_item, "pattern_action", text="Action")
                
                column_parent = row_action.column(align=True)
                column_parent.prop(pattern_item, "parent_collection", text="Parent")
                
                # Name and sample properties on the second row
                row1 = pattern_box.row()
                column1 = row1.column(align=True)
                column1.prop(pattern_item, "pattern_name", text="Name")
                
                column2 = row1.column(align=True)
                column2.prop(pattern_item, "pattern_sample", text="Sample")

        row8 = boxsort.row()
        row8.alignment = 'CENTER'
        row8.operator('setupauto.ot_quicksort', text = "Quick Sort!")
