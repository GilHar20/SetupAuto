import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

def get_blender_addons_path():
    """Get the Blender addons path from user input with default"""
    # Default addons path for Windows
    default_addons_path = r"C:\Users\Michael\AppData\Roaming\Blender Foundation\Blender\4.5\extensions\user_default"
    
    print(f"Default Blender addons path: {default_addons_path}")
    user_input = input("Enter Blender addons path (or press Enter to use default): ").strip()
    
    if user_input:
        addons_path = user_input
    else:
        addons_path = default_addons_path
    
    # Verify the path exists
    if not os.path.exists(addons_path):
        print(f"Warning: Addons path does not exist: {addons_path}")
        print("Please ensure the path is correct.")
        return addons_path  # Return anyway, let the calling function handle it
    
    return addons_path

def create_addon_package():
    """Create a proper addon package structure"""
    # Create temporary directory for the addon
    temp_dir = tempfile.mkdtemp()
    addon_dir = os.path.join(temp_dir, "setupauto")
    
    # Create addon directory
    os.makedirs(addon_dir)
    
    # Copy plugin files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Copy main plugin files
    files_to_copy = [
        "__init__.py",
        "bgimage.py", 
        "quicksort.py"
    ]
    
    for file in files_to_copy:
        src = os.path.join(current_dir, file)
        dst = os.path.join(addon_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
    
    # Copy Tools directory
    tools_src = os.path.join(current_dir, "Tools")
    tools_dst = os.path.join(addon_dir, "Tools")
    if os.path.exists(tools_src):
        shutil.copytree(tools_src, tools_dst)
    
    return temp_dir

def launch_blender_with_addon():
    """Launch Blender with the addon pre-registered"""
    addons_path = get_blender_addons_path()
    
    if not addons_path:
        print("Could not find Blender addons directory. Please install Blender first.")
        return False
    
    if not os.path.exists(addons_path):
        print(f"Blender addons directory not found: {addons_path}")
        return False
    
    print(f"Found Blender addons directory: {addons_path}")
    
    # Create addon package
    temp_dir = create_addon_package()
    addon_dir = os.path.join(temp_dir, "setupauto")
    
    # Copy to Blender addons directory
    addon_dest = os.path.join(addons_path, "setupauto")
    if os.path.exists(addon_dest):
        shutil.rmtree(addon_dest)
    
    shutil.copytree(addon_dir, addon_dest)
    print(f"Copied addon to: {addon_dest}")
    
    # Create a startup script to enable the addon
    startup_script = os.path.join(temp_dir, "startup.py")
    with open(startup_script, 'w') as f:
        f.write("""
import bpy

# Enable the SetupAuto addon
try:
    bpy.ops.preferences.addon_enable(module="setupauto")
    print("SetupAuto addon enabled successfully!")
except Exception as e:
    print(f"Failed to enable addon: {e}")

# Set up the addon if it has a setup function
try:
    if hasattr(bpy.ops, 'setupauto'):
        print("SetupAuto addon is available!")
    else:
        print("SetupAuto addon not found in operators")
except Exception as e:
    print(f"Error checking addon: {e}")
""")
    
    # Get Blender executable path from user with default
    default_blender_path = r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
    
    print(f"Default Blender path: {default_blender_path}")
    user_input = input("Enter Blender executable path (or press Enter to use default): ").strip()
    
    if user_input:
        blender_exe = user_input
    else:
        blender_exe = default_blender_path
    
    # Verify the executable exists
    if not os.path.exists(blender_exe):
        print(f"Blender executable not found at: {blender_exe}")
        return False
    
    print(f"Found Blender executable: {blender_exe}")
    
    # Launch Blender with the startup script
    try:
        cmd = [blender_exe, "--python", startup_script]
        print(f"Launching Blender with command: {' '.join(cmd)}")
        
        # Launch in foreground (window mode)
        print("Launching Blender in window mode...")
        process = subprocess.run(cmd)
        print(f"Blender process completed with return code: {process.returncode}")
        
        return True
        
    except Exception as e:
        print(f"Failed to launch Blender: {e}")
        return False

if __name__ == "__main__":
    print("Launching Blender with SetupAuto plugin...")
    success = launch_blender_with_addon()
    
    if success:
        print("Blender launched successfully!")
    else:
        print("Failed to launch Blender with plugin.") 