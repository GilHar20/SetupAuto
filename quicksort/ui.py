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
        box_detection = layout.box()
        header_detection = box_detection.row()
        header_detection.label(text="Pattern Detection:")
        
        row_detection = box_detection.row()
        row_detection.alignment = 'CENTER'
        row_detection.operator('setupauto.ot_patternsdetection', text="Detect Patterns!")
        
        # quick sort settings:
        box_sort = layout.box()
        header = box_sort.row()
        header.label(text = "Quick Sort: ")

        # Show collection length and add/remove buttons
        rowtop = box_sort.row()
        rowtop.label(text=f"Number of patterns: {len(patternprops)}")
        
        row_buttons = box_sort.row()
        row_buttons.operator("setupauto.add_pattern", text="Add Pattern", icon='ADD')
        if len(patternprops) > 0:
            row_buttons.operator("setupauto.remove_pattern", text="Remove Pattern", icon='REMOVE')

        # Draw sort button
        row_sort_a = box_sort.row()
        row_sort_a.alignment = 'CENTER'
        row_sort_a.operator('setupauto.ot_quicksort', text = "Quick Sort!")

        # Draw pattern properties for each item in the collection - each in its own box    
        for i, pattern_item in enumerate(patternprops):
            # Create individual box for each pattern item
            pattern_box = box_sort.box()
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

        # Draw sort button
        row_sort_b = box_sort.row()
        row_sort_b.alignment = 'CENTER'
        row_sort_b.operator('setupauto.ot_quicksort', text = "Quick Sort!")
