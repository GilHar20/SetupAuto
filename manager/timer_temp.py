"""
Work Time Tracker for Blender
A self-contained script that tracks active work time in Blender projects.

Features:
- Tracks time only when actively working (stops after inactivity period)
- Saves session data as JSON files next to .blend files
- Provides UI panel with timer controls
- Auto-start option and activity detection

To use: Copy and paste this entire script into Blender's Script Editor and run it.
"""

import bpy
import time
import os
import json
from bpy.app.handlers import persistent


# ===============================================================================
# PROPERTY GROUP
# ===============================================================================

class WorkTimeTracker_PG_Props(bpy.types.PropertyGroup):
    """Property group for work time tracker settings"""
    
    inactivity_period: bpy.props.IntProperty(
        name="Inactivity Period",
        description="Amount of time, in minutes, before the timer stops counting",
        default=10,
        min=1,
        max=120
    )
    
    auto_start_timer: bpy.props.BoolProperty(
        name="Auto Start Timer",
        description="Automatically start timer when opening a file",
        default=False
    )
    


# ===============================================================================
# OPERATORS
# ===============================================================================

class WTT_OT_timer_start(bpy.types.Operator):
    """Start tracking the current .blend file usage time"""
    bl_idname = "wtt.ot_timer_start"
    bl_label = "Start Timer"
    bl_description = "Start tracking the current .blend file usage time"

    def execute(self, context):
        # Get the timer instance and start it
        timer_instance = WorkTimeTracker.get_instance()
        success = timer_instance.start_tracking(context)
        if success:
            self.report({'INFO'}, "Work time tracking started")
        else:
            self.report({'ERROR'}, "File must be saved for time tracking to begin")
        return {'FINISHED'}


class WTT_OT_timer_stop(bpy.types.Operator):
    """Stop tracking the current .blend file usage time"""
    bl_idname = "wtt.ot_timer_stop"
    bl_label = "Stop Timer"
    bl_description = "Stop tracking the current .blend file usage time"

    def execute(self, context):
        # Get the timer instance and stop it
        timer_instance = WorkTimeTracker.get_instance()
        timer_instance.stop_tracking()
        self.report({'INFO'}, "Work time tracking stopped")
        return {'FINISHED'}


class WTT_OT_timer_restart(bpy.types.Operator):
    """Restart the current session (saves current session and starts a new one)"""
    bl_idname = "wtt.ot_timer_restart"
    bl_label = "Restart Session"
    bl_description = "Save current session and immediately start a new tracking session"

    def execute(self, context):
        # Get the timer instance and restart the session
        timer_instance = WorkTimeTracker.get_instance()
        success = timer_instance.restart_session(context)
        if success:
            self.report({'INFO'}, "Work session restarted")
        else:
            self.report({'ERROR'}, "File must be saved for time tracking to begin")
        return {'FINISHED'}


# ===============================================================================
# WORK TIME TRACKER CLASS
# ===============================================================================

class WorkTimeTracker:
    """Singleton class to track work time for the current blend file"""
    _instance = None
    
    def __init__(self):
        self.is_tracking = False
        self.start_time = None
        self.total_time = 0  # Total accumulated time in seconds
        self.last_activity_time = None
        self.timer = None
        self.current_file_path = None
        self.data_file_path = None
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_data_file_path(self):
        """Get the path where timer data should be saved"""
        if bpy.data.filepath:
            # Save timer data next to the blend file
            blend_dir = os.path.dirname(bpy.data.filepath)
            blend_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
            return os.path.join(blend_dir, f"{blend_name}_timetracker.json")
        else:
            # If file hasn't been saved, return None to indicate no tracking possible
            return None
    
    def load_existing_time(self):
        """Load existing time data from file"""
        try:
            data_file = self.get_data_file_path()
            if data_file and os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    # Calculate total time from all sessions
                    total_time = 0
                    for session_key, session_data in data.items():
                        if session_key.startswith('session_') and isinstance(session_data, dict):
                            duration = session_data.get('session_duration', 0)
                            # Handle both old format (seconds) and new format (HH:MM)
                            if isinstance(duration, str) and ':' in duration:
                                # New format: HH:MM
                                try:
                                    hours, minutes = map(int, duration.split(':'))
                                    duration_seconds = hours * 3600 + minutes * 60
                                    total_time += duration_seconds
                                except:
                                    pass  # Skip invalid formats
                            elif isinstance(duration, (int, float)):
                                # Old format: seconds
                                total_time += duration
                    self.total_time = total_time
            else:
                self.total_time = 0
        except Exception as e:
            print(f"Error loading timer data: {e}")
            self.total_time = 0
    
    def save_time_data(self):
        """Save current session data to file as a new session entry"""
        try:
            data_file = self.get_data_file_path()
            if not data_file:
                return  # Can't save if file hasn't been saved
            
            # Don't save if we don't have valid session data
            if not self.start_time or not hasattr(self, '_session_end_time'):
                print("No valid session data to save")
                return
                
            # Calculate session duration (only the time that was just tracked)
            session_duration_seconds = self._session_end_time - self.start_time
                           
            os.makedirs(os.path.dirname(data_file), exist_ok=True)
            
            # Load existing data or create new structure
            existing_data = {}
            if os.path.exists(data_file):
                try:
                    with open(data_file, 'r') as f:
                        existing_data = json.load(f)
                except:
                    existing_data = {}
            
            # Find the next session number
            session_numbers = []
            for key in existing_data.keys():
                if key.startswith('session_'):
                    try:
                        session_num = int(key.split('_')[1])
                        session_numbers.append(session_num)
                    except:
                        continue
            
            next_session_number = max(session_numbers, default=0) + 1
            
            # Format session duration as HH:MM
            hours = int(session_duration_seconds // 3600)
            minutes = int((session_duration_seconds % 3600) // 60)
            session_duration_formatted = f"{hours:02d}:{minutes:02d}"
            
            # Format session start as DD/MM HH:MM
            start_time_obj = time.localtime(self.start_time)
            session_start_formatted = f"{start_time_obj.tm_mday:02d}/{start_time_obj.tm_mon:02d} {start_time_obj.tm_hour:02d}:{start_time_obj.tm_min:02d}"
            
            # Format session end as HH:MM
            end_time_obj = time.localtime(self._session_end_time)
            session_end_formatted = f"{end_time_obj.tm_hour:02d}:{end_time_obj.tm_min:02d}"
            
            # Format JSON saved time as HH:MM
            current_time = time.time()
            current_time_obj = time.localtime(current_time)
            json_saved_formatted = f"{current_time_obj.tm_hour:02d}:{current_time_obj.tm_min:02d}"
            
            # Get blend file name
            blend_file_name = os.path.basename(bpy.data.filepath) if bpy.data.filepath else "unsaved"
            
            # Create new session entry
            session_key = f"session_{next_session_number:04d}"
            session_data = {
                'session_number': next_session_number,
                'session_duration': session_duration_formatted,
                'session_start': session_start_formatted,
                'session_end': session_end_formatted,
                'json_saved_at': json_saved_formatted,
                'blend_file_name': blend_file_name
            }
            
            print(f"TIMER DEBUG: Saving session: {session_duration_formatted} (from {session_start_formatted} to {session_end_formatted})")
            print(f"TIMER DEBUG: Session duration in seconds: {session_duration_seconds:.2f}")
            print(f"TIMER DEBUG: Start time: {self.start_time}, End time: {self._session_end_time}")
            
            # Add the new session to existing data
            existing_data[session_key] = session_data
            
            # Save updated data
            with open(data_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving timer data: {e}")
    
    def start_tracking(self, context):
        """Start tracking time for current session"""
        # Abort if already tracking
        if self.is_tracking:
            return True  # Return True since we're already tracking successfully
        
        # Check if file is saved - required for tracking
        if not bpy.data.filepath:
            print("File must be saved for time tracking to begin")
            return False
        
        # Load existing time if this is a new file or first time starting
        current_file = bpy.data.filepath
        if self.current_file_path != current_file:
            self.current_file_path = current_file
            self.load_existing_time()
        
        # Clear any previous session end time
        if hasattr(self, '_session_end_time'):
            delattr(self, '_session_end_time')
        
        self.is_tracking = True
        self.start_time = time.time()
        self.last_activity_time = self.start_time
        
        # Register the timer function
        if self.timer is None:
            self.timer = bpy.app.timers.register(self.timer_update, first_interval=1.0, persistent=True)
        
        return True
    
    def stop_tracking(self):
        """Stop tracking time and save data"""
        # Abort if tracking already stopped
        if not self.is_tracking:
            print("TIMER DEBUG: stop_tracking called but not tracking")
            return
        
        print("TIMER DEBUG: stop_tracking called - saving session")
        
        # Record session end time before stopping
        self._session_end_time = time.time()
        
        # Load existing time data first
        self.load_existing_time()
        
        # Add current session time to total
        if self.start_time:
            session_time = self._session_end_time - self.start_time
            self.total_time += session_time
        
        self.is_tracking = False
        
        # Save data (includes session info)
        self.save_time_data()
        
        # Clean up
        self.start_time = None
        
        # Unregister timer
        if self.timer:
            bpy.app.timers.unregister(self.timer)
            self.timer = None
    
    def restart_session(self, context):
        """Restart session: stop current session (save data) and start new session"""
        # Stop current session if tracking (this will save the data)
        if self.is_tracking:
            self.stop_tracking()
        
        # Start a new session immediately
        return self.start_tracking(context)
    
    def timer_update(self):
        """Timer function called periodically to check for inactivity"""
        if not self.is_tracking:
            return None  # Stop the timer
        
        # Get inactivity period from properties
        try:
            manager_props = bpy.context.scene.wtt_props
            inactivity_minutes = manager_props.inactivity_period
        except:
            inactivity_minutes = 10  # Default fallback
        
        current_time = time.time()
        inactivity_seconds = inactivity_minutes * 60
        
        # Check if we've been inactive too long
        if current_time - self.last_activity_time > inactivity_seconds:
            # Stop tracking due to inactivity
            self.stop_tracking()
            print(f"Timer stopped due to {inactivity_minutes} minutes of inactivity")
            return None
        
        # Continue the timer
        return 1.0  # Check again in 1 second
    
    def register_activity(self):
        """Register user activity"""
        if self.is_tracking:
            current_time = time.time()
            # Throttle activity registration to prevent spam (max once per second)
            if not hasattr(self, '_last_activity_registered') or current_time - self._last_activity_registered > 1.0:
                self.last_activity_time = current_time
                self._last_activity_registered = current_time
    
    def get_current_time_formatted(self):
        """Get current total time formatted as HH:MM"""
        # Check if file is saved
        if not bpy.data.filepath:
            return "File must be saved"
        
        # If not tracking, show the saved total time
        if not self.is_tracking:
            # Load existing time if we haven't already for this file
            current_file = bpy.data.filepath
            if self.current_file_path != current_file:
                self.current_file_path = current_file
                self.load_existing_time()
            current_total = self.total_time
        else:
            # If tracking, show saved time + current session time
            current_total = self.total_time
            if self.start_time:
                current_total += time.time() - self.start_time
        
        hours = int(current_total // 3600)
        minutes = int((current_total % 3600) // 60)
        
        return f"{hours:02d}:{minutes:02d}"


# ===============================================================================
# UI PANEL
# ===============================================================================

class WTT_PT_manager_panel(bpy.types.Panel):
    """Work Time Tracker UI panel"""
    bl_idname = "wtt.pt_manager_panel"
    bl_label = "Work Time Tracker"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SetupAuto"

    def draw(self, context):
        layout = self.layout
        manager_props = context.scene.wtt_props
        
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
        row_time.label(text=f"Total time tracked: {current_time}", icon='PREVIEW_RANGE')
        
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
            row_controls.operator('wtt.ot_timer_start', text="Start", icon='PLAY')
        else:
            row_controls.operator('wtt.ot_timer_stop', text="Stop", icon='PAUSE')
        
        row_controls.operator('wtt.ot_timer_restart', text="Restart Session", icon='FILE_REFRESH')

        # Technical settings
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
            seconds = int(total_seconds % 60)
            row_total.label(text=f"Saved Time: {hours:02d}:{minutes:02d}:{seconds:02d}")


# ===============================================================================
# APP HANDLERS
# ===============================================================================

# Global tracker instance
work_tracker = WorkTimeTracker.get_instance()


@persistent
def activity_handler(scene):
    """Handler to register activity when scene changes"""
    # Skip activity registration during file save/load operations
    if bpy.context.mode == 'OBJECT' and hasattr(bpy.context, 'window'):
        work_tracker.register_activity()


@persistent
def load_handler(dummy):
    """Handler called when file is loaded"""
    # Reset tracker for new file
    work_tracker.current_file_path = None
    work_tracker.stop_tracking()
    
    # Auto-start timer if enabled
    try:
        if bpy.context.scene.wtt_props.auto_start_timer:
            work_tracker.start_tracking(bpy.context)
    except:
        pass  # Properties might not be available during load



# ===============================================================================
# REGISTRATION
# ===============================================================================

classes = [
    WorkTimeTracker_PG_Props,
    WTT_OT_timer_start,
    WTT_OT_timer_stop,
    WTT_OT_timer_restart,
    WTT_PT_manager_panel,
]


def register():
    """Register all classes and setup"""
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register property group to scene
    bpy.types.Scene.wtt_props = bpy.props.PointerProperty(type=WorkTimeTracker_PG_Props)
    
    # Register handlers for activity detection
    if activity_handler not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(activity_handler)
    
    if load_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(load_handler)
    
    print("Work Time Tracker registered successfully!")


def unregister():
    """Unregister all classes and cleanup"""
    # Stop tracking
    work_tracker.stop_tracking()
    
    # Remove handlers
    if activity_handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(activity_handler)
    
    if load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_handler)
    
    # Unregister property group
    if hasattr(bpy.types.Scene, 'wtt_props'):
        delattr(bpy.types.Scene, 'wtt_props')
    
    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    print("Work Time Tracker unregistered successfully!")


# ===============================================================================
# MAIN EXECUTION
# ===============================================================================

if __name__ == "__main__":
    # Unregister first (in case script was run before)
    try:
        unregister()
    except:
        pass
    
    # Register the addon
    register()
    
    print("Work Time Tracker script loaded! Check the 'WorkTimer' tab in the 3D Viewport sidebar.")
