import bpy
from ..manager.timer import WorkTimeTracker



class SETUPAUTO_PT_manager_panel(bpy.types.Panel):
    '''Class draws manager UI panel'''
    bl_idname = "setupauto.pt_manager_panel"
    bl_label = "Work Time Tracker"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SetupAuto"

    def draw(self, context):
        layout = self.layout
        manager_props = context.scene.manager_props
        
        # Get timer instance for status
        timer_instance = WorkTimeTracker.get_instance()

        # Additional info (moved to first position)
        box_info = layout.box()
        box_info.label(text="Timer Information", icon='INFO')
        
        info_text = [
            "• Timer tracks active work time",
            "• Stops automatically after inactivity period",
            "• Data is saved with your .blend file",
            "• Activity detected from scene changes"
        ]
        
        for info in info_text:
            row_info = box_info.row()
            row_info.label(text=info)

        # Work Time Tracker section
        box_timer = layout.box()
        box_timer.label(text="Work Time Tracker", icon='TIME')
        
        # Current time display
        row_time = box_timer.row()
        current_time = timer_instance.get_current_time_formatted()
        row_time.label(text=f"Total time tracked:: {current_time}", icon='PREVIEW_RANGE')
        
        # Status indicator
        row_status = box_timer.row()
        if timer_instance.is_tracking:
            row_status.label(text="Status: Tracking", icon='PLAY')
        else:
            row_status.label(text="Status: Stopped", icon='PAUSE')
        
        # Settings
        row_inactivity = box_timer.row()
        row_inactivity.prop(manager_props, "inactivity_period", text="Inactivity Period (minutes)")
        
        row_auto = box_timer.row()
        row_auto.prop(manager_props, "auto_start_timer", text="Auto-start timer on file load")
        
        # Timer control buttons
        row_controls = box_timer.row(align=True)
        
        # Start button (only show if not tracking)
        if not timer_instance.is_tracking:
            row_controls.operator('setupauto.ot_timer_start', text="Start", icon='PLAY')
        else:
            row_controls.operator('setupauto.ot_timer_stop', text="Stop", icon='PAUSE')
        
        row_controls.operator('setupauto.ot_timer_restart', text="Restart Session", icon='FILE_REFRESH')

        # Technical information
        box_tech = layout.box()
        box_tech.label(text="Technical Info:", icon='INFO_LARGE')
        
        # Data file location
        if timer_instance:
            data_file = timer_instance.get_data_file_path()
            if data_file:
                row_file = box_tech.row()
                row_file.label(text=f"Data File: {bpy.path.basename(data_file)}", icon='FILE_BLEND')
            
            # Total accumulated time
            row_total = box_tech.row()
            total_seconds = timer_instance.total_time
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            row_total.label(text=f"Saved Time: {hours:02d}:{minutes:02d}")

