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
        pattern_props = context.scene.pattern_props
        
        # Pattern Detection box:
        boxDetection = layout.box()
        boxDetection.label(text="Pattern Detection")
        
        rowDetection = boxDetection.row()
        rowDetection.operator('setupauto.ot_patternsdetection', text="Detect Patterns!")
        
        # quick sort settings:
        boxSort = layout.box()
        boxSort.label(text = "Quick Sort")

        rowLabel = boxSort.row()
        rowLabel.label(text=f"Number of patterns: {len(pattern_props)}")
        
        rowAddRemove = boxSort.row(align=True)
        rowAddRemove.operator("setupauto.add_pattern", text="Add Pattern", icon='ADD')
        rowAddRemove.operator("setupauto.remove_pattern", text="Remove Pattern", icon='REMOVE')

        # Draw sort button
        rowSort = boxSort.row()
        rowSort.operator('setupauto.ot_quicksort', text = "Quick Sort!")

        # Draw pattern properties for each item in the collection - each in its own box    
        for i, pattern_item in enumerate(pattern_props):
            # Create individual box for each pattern item
            patternBox = boxSort.box()
            patternBox.label(text=f"Pattern #{i+1}")
            
            # Action and parent collection properties on the same row
            rowAction = patternBox.row()
            rowAction.prop(pattern_item, "pattern_action", text="Action")
            rowAction.prop(pattern_item, "parent_collection", text="Parent")
            
            # Name and sample properties on the second row
            rowPattern = patternBox.row()
            rowPattern.prop(pattern_item, "pattern_name", text="Name")
            rowPattern.prop(pattern_item, "pattern_sample", text="Sample")

        # Draw sort button
        rowSort2 = boxSort.row()
        rowSort2.operator('setupauto.ot_quicksort', text = "Quick Sort!")
