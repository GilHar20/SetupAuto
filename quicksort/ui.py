import bpy



#===================================
    # --- UIList ---
#===================================
class SETUPAUTO_UL_pattern_list(bpy.types.UIList):
    """UIList for displaying collection items"""
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item.pattern_sample:
                layout.label(text = str(index + 1) + ": " + item.pattern_sample, icon = 'CHECKBOX_HLT')
            else:
                layout.label(text = str(index + 1) + ": " + "- no pattern -", icon = 'CHECKBOX_DEHLT')
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text = item.pattern_sample, icon = 'CHECKBOX_HLT')

    def filter_items(self, context, data, propname):
        items = getattr(data, propname)
        
        # Initialize default values

        filter_neworder = []
        filter_flags = (range(len(items)))

        # Get filter flags if filtering is enabled
        if self.filter_name:
            # Use the built-in filter_items_by_name helper for filtering
            filter_flags = bpy.types.UI_UL_list.filter_items_by_name(
                pattern = self.filter_name,
                bitflag = self.bitflag_filter_item,
                items = items,
                propname = 'pattern_sample',
                reverse = self.use_filter_sort_reverse
            )
            if self.use_filter_sort_reverse:
                filter_flags.reverse()

        else:
            # No filtering - show all items
            filter_flags = [self.bitflag_filter_item] * len(items)
        
        # Apply sorting if enabled
        if self.use_filter_sort_alpha:
            # Use the built-in sort_items_by_name helper for sorting
            filter_neworder = bpy.types.UI_UL_list.sort_items_by_name(items, propname='pattern_sample')
    

        return filter_flags, filter_neworder

    

#===================================
    # --- Settings Panel ---
#===================================
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
        pattern_index = context.scene.pattern_index

        boxSort = layout.box()
        
        rowCollection = boxSort.row()
        rowCollection.prop(quicksort_props, "main_collection", text = "", placeholder = "Main Collection")
        if quicksort_props.main_collection == None:
            rowInfo = boxSort.row()
            rowInfo.label(text = " You must assign a main collection!", icon = 'INFO')


        rowSort = boxSort.row(align = True)
        rowSort.operator('setupauto.ot_patternsdetection', text="Detect Patterns!")
        rowSort.operator('setupauto.ot_quicksort', text = "Quick Sort!", icon='PLAY')

        rowLabel = boxSort.row()
        rowLabel.label(text=f"Number of patterns: {len(pattern_props)}")

        rowList = boxSort.row()        
        rowList.template_list(
            "SETUPAUTO_UL_pattern_list",    # list_type (you'll need to create this)
            "setupauto_pattern_list",       # list_id (unique identifier)
            context.scene,                  # dataptr (the data block containing the collection)
            "pattern_props",                # propname (name of the CollectionProperty)
            context.scene,                  # active_dataptr (data block containing active index)
            "pattern_index",                # active_propname (name of the IntProperty for active index)
            rows = 8                        # optional: number of rows to display
        )
        columnList = rowList.column(align = True)
        columnList.operator("setupauto.add_pattern",    text = "", icon = 'ADD')
        columnList.operator("setupauto.remove_pattern", text = "", icon = 'REMOVE')
        columnList.operator("setupauto.clear_patterns", text = "", icon = 'TRASH')

        # Draw pattern properties for the active item in the UIList
        if pattern_props and 0 <= pattern_index < len(pattern_props):
            pattern_entry = pattern_props[pattern_index]
            patternBox = boxSort.box()
            rowTop = patternBox.row(align = True)
            rowTop.label(text=f"Pattern Entry #{pattern_index + 1}:", icon = 'SORTSIZE')
            rowTop.operator('setupauto.select_pattern', text = "", icon = 'VIEW_ZOOM').select_pattern = str(pattern_entry.pattern_sample)
            rowTop.operator('setupauto.remove_pattern', text = "", icon = 'REMOVE').pattern_index = pattern_index

            rowAction = patternBox.row(align = True)
            rowAction.prop(pattern_entry, "pattern_action", text="")
            rowAction.prop(pattern_entry, "pattern_sample", text="", placeholder="Sample")

            rowCollection = patternBox.row(align = True)
            rowCollection.prop(pattern_entry, "parent_collection", text="", placeholder="Parent Collection")
            rowCollection.prop(pattern_entry, "output_collection", text="", placeholder="Output Collection", icon = 'OUTLINER_COLLECTION')

            if pattern_entry.pattern_action == 'RENAME':
                rowRename = patternBox.row()
                rowRename.prop(pattern_entry, "new_name", text="", placeholder="New Name")

