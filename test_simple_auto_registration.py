#!/usr/bin/env python3
"""
Simple test script for the auto-registration system.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock bpy for testing outside of Blender
class MockBpy:
    class types:
        class PropertyGroup:
            pass
        class Operator:
            pass
        class Panel:
            pass
        class AddonPreferences:
            pass
        class Scene:
            pass
        class props:
            @staticmethod
            def CollectionProperty(type=None):
                return "CollectionProperty"
            @staticmethod
            def PointerProperty(type=None):
                return "PointerProperty"

# Mock bpy if not in Blender
try:
    import bpy
except ImportError:
    bpy = MockBpy()
    print("Warning: bpy not available, using mock for testing")

# Import the auto-registration module
try:
    from auto_registration import AutoRegistration
except ImportError as e:
    print(f"Error importing auto_registration: {e}")
    sys.exit(1)

def test_auto_registration():
    """Test the auto-registration system."""
    print("Testing Auto-Registration System (Based on Jacques Lucke's approach)")
    print("=" * 70)
    
    # Create an instance of AutoRegistration
    auto_reg = AutoRegistration("AutoSetup")
    
    # Discover classes
    print("Discovering classes...")
    try:
        auto_reg.discover_classes()
    except Exception as e:
        print(f"Error during class discovery: {e}")
        return None
    
    # Get registration info
    info = auto_reg.get_registration_info()
    
    print(f"\nFound {len(auto_reg.classes)} total classes:")
    print(f"- PropertyGroups: {len(info['PropertyGroups'])}")
    print(f"- Other Classes: {len(info['Other Classes'])}")
    print(f"- Properties to register: {len(info['Properties'])}")
    
    print("\nDetailed breakdown:")
    print("-" * 30)
    
    if info['PropertyGroups']:
        print("\nPropertyGroups:")
        for pg in info['PropertyGroups']:
            print(f"  - {pg}")
    
    if info['Other Classes']:
        print("\nOther Classes:")
        for cls in info['Other Classes']:
            print(f"  - {cls}")
    
    if info['Properties']:
        print("\nProperties to register:")
        for prop in info['Properties']:
            print(f"  - {prop}")
    
    print("\n" + "=" * 50)
    print("Test completed successfully!")
    
    return auto_reg

if __name__ == "__main__":
    test_auto_registration()
