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
        quicksort_props = context.scene.quicksort_props


        # quick sort settings:
        boxSort = layout.box()
        boxSort.label(text = "Quick Sort")

        rowLabel = boxSort.row()
        rowLabel.label(text=f"Number of patterns: {len(pattern_props)}")
        
        columnCollection = boxSort.column(align=True)

        #rowDetection = columnCollection.row()
        columnCollection.operator('setupauto.ot_patternsdetection', text="Detect Patterns!")
        
        rowAddRemove = columnCollection.row(align=True)
        rowAddRemove.operator("setupauto.add_pattern", text="Add Pattern", icon='ADD')
        rowAddRemove.operator("setupauto.remove_pattern", text="Remove Pattern", icon='REMOVE')

        columnCollection.operator("setupauto.clear_patterns", text="Clear All Paterns", icon='TRASH')

        rowCollection = columnCollection.row()
        rowCollection.prop(quicksort_props, "main_collection", text="Main Collection")

        rowSort = boxSort.row()
        rowSort.alignment = 'CENTER'
        columnSort = rowSort.column()
        columnSort.scale_x = 1
        columnSort.operator('setupauto.ot_quicksort', text = "Quick Sort!", icon='PLAY')


        # Draw pattern properties for each item in the collection - each in its own box    
        for i, pattern_item in enumerate(pattern_props):
            patternBox = boxSort.box()
            rowTop = patternBox.row(align=True)
            rowTop.label(text=f"Pattern Entry #{i+1}:", icon = 'SORTSIZE')
            rowTop.operator('object.select_pattern', text = "", icon = 'VIEW_ZOOM').pattern = "*" + str(pattern_item.pattern_sample) + "*"
            rowTop.operator('setupauto.remove_pattern', text = "", icon = 'REMOVE').pattern_index = i
            
            rowCollection = patternBox.row(align=True)
            rowCollection.prop(pattern_item, "parent_collection", text="", placeholder="Parent Collection")
            rowCollection.prop(pattern_item, "output_collection", text="", placeholder="Output Collection", icon = 'OUTLINER_COLLECTION')
            
            # ADD AUTOMATIC RENAME?

            rowAction = patternBox.row(align=True)
            rowAction.prop(pattern_item, "pattern_action", text="")
            rowAction.prop(pattern_item, "pattern_sample", text="", placeholder="Sample")

        rowSort2 = boxSort.row()
        rowSort2.alignment = 'CENTER'
        columnSort2 = rowSort2.column()
        columnSort2.scale_x = 1
        columnSort2.operator('setupauto.ot_quicksort', text = "Quick Sort!", icon='PLAY')
