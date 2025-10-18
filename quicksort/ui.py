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
        
        columnCollection = boxSort.column(align=True)

        #rowDetection = columnCollection.row()
        columnCollection.operator('setupauto.ot_patternsdetection', text="Detect Patterns!")
        
        rowAddRemove = columnCollection.row(align=True)
        rowAddRemove.operator("setupauto.add_pattern", text="Add Pattern", icon='ADD')
        rowAddRemove.operator("setupauto.remove_pattern", text="Remove Pattern", icon='REMOVE')

        columnCollection.operator("setupauto.clear_patterns", text="Clear All Paterns", icon='TRASH')

        rowCollection = columnCollection.row()
        rowCollection.prop(quicksort_props, "main_collection", text="Main Collection")
        if quicksort_props.main_collection == None:
            rowInfo = boxSort.row()
            rowInfo.label(text = " You must assign a main collection!", icon = 'INFO')

        if pattern_props:
            rowSort = boxSort.row()
            rowSort.alignment = 'CENTER'
            columnSort = rowSort.column()
            columnSort.scale_x = 1
            columnSort.operator('setupauto.ot_quicksort', text = "Quick Sort!", icon='PLAY')

        rowLabel = boxSort.row()
        rowLabel.label(text=f"Number of patterns: {len(pattern_props)}")


        # Draw pattern properties for each item in the collection - each in its own box    
        for i, pattern_entry in enumerate(pattern_props):
            patternBox = boxSort.box()
            rowTop = patternBox.row(align=True)
            rowTop.label(text=f"Pattern Entry #{i+1}:", icon = 'SORTSIZE')
            rowTop.operator('setupauto.select_pattern', text = "", icon = 'VIEW_ZOOM').select_pattern = str(pattern_entry.pattern_sample)
            rowTop.operator('setupauto.remove_pattern', text = "", icon = 'REMOVE').pattern_index = i

            rowAction = patternBox.row(align=True)
            rowAction.prop(pattern_entry, "pattern_action", text="")
            rowAction.prop(pattern_entry, "pattern_sample", text="", placeholder="Sample")

            rowCollection = patternBox.row(align=True)
            rowCollection.prop(pattern_entry, "parent_collection", text="", placeholder="Parent Collection")
            rowCollection.prop(pattern_entry, "output_collection", text="", placeholder="Output Collection", icon = 'OUTLINER_COLLECTION')

            match pattern_entry.pattern_action:
                case 'RENAME':
                    rowRename = patternBox.row()
                    rowRename.prop(pattern_entry, "new_name", text="", placeholder="New Name")
                case 'ORGANIZE', 'JOIN', 'DELETE':
                    pass

        if pattern_props:
            rowSort2 = boxSort.row()
            rowSort2.alignment = 'CENTER'
            columnSort2 = rowSort2.column()
            columnSort2.scale_x = 1
            columnSort2.operator('setupauto.ot_quicksort', text = "Quick Sort!", icon='PLAY')
