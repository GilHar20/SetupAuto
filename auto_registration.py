import bpy
import inspect
import importlib
import sys
from typing import List, Dict, Any, Optional

class AutoRegistration:
    """
    Automatic registration system for Blender addon classes.
    Based on Jacques Lucke's auto_load.py approach, updated for Blender 4.5.
    """
    
    def __init__(self, addon_name: str):
        self.addon_name = addon_name
        self.classes = []
        self.property_groups = {}
        self.property_registrations = {}
        
    def discover_classes(self) -> None:
        """Discover all classes from all modules in the addon."""
        # Get the addon module
        addon_module = sys.modules.get(self.addon_name)
        if not addon_module:
            print(f"Warning: Addon module {self.addon_name} not found")
            return
            
        # Get all submodules
        submodules = self._get_submodules(addon_module)
        
        # Discover classes from each submodule
        for module in submodules:
            self._discover_classes_from_module(module)
            
        # Also discover classes from addon updater modules
        self._discover_addon_updater_classes()
    
    def _get_submodules(self, module) -> List:
        """Get all submodules of the addon."""
        submodules = []
        
        # Get the module's directory
        module_dir = getattr(module, '__path__', None)
        if not module_dir:
            return submodules
            
        # Get all attributes of the module
        for name in dir(module):
            obj = getattr(module, name)
            
            # Check if it's a module
            if inspect.ismodule(obj):
                # Check if it's a submodule of our addon
                if hasattr(obj, '__name__') and obj.__name__.startswith(self.addon_name):
                    submodules.append(obj)
                    
                    # Recursively get submodules of this submodule
                    submodules.extend(self._get_submodules(obj))
        
        return submodules
    
    def _discover_classes_from_module(self, module) -> None:
        """Discover all Blender classes from a module."""
        for name in dir(module):
            obj = getattr(module, name)
            
            # Check if it's a class
            if inspect.isclass(obj):
                # Check if it's a Blender class
                if self._is_blender_class(obj):
                    self._categorize_class(obj)
    
    def _discover_addon_updater_classes(self) -> None:
        """Discover classes from addon updater modules."""
        # Check if addon updater modules exist
        addon_updater_ops = sys.modules.get(f"{self.addon_name}.addon_updater_ops")
        if addon_updater_ops:
            self._discover_classes_from_module(addon_updater_ops)
            print(f"Discovered classes from addon_updater_ops module")
    
    def _is_blender_class(self, cls) -> bool:
        """Check if a class is a Blender class."""
        # Skip the auto-registration class itself
        if cls == AutoRegistration:
            return False
            
        # Check if it has Blender-specific attributes
        if hasattr(cls, 'bl_idname') or hasattr(cls, 'bl_label'):
            return True
            
        # Check if it inherits from a Blender type
        if hasattr(cls, '__bases__'):
            for base in cls.__bases__:
                if hasattr(base, '__module__') and 'bpy.types' in str(base.__module__):
                    return True
                    
        return False
    
    def _categorize_class(self, cls) -> None:
        """Categorize a Blender class."""
        # Check if it's a PropertyGroup
        if issubclass(cls, bpy.types.PropertyGroup):
            self.property_groups[cls.__name__] = cls
        else:
            # All other Blender classes
            self.classes.append(cls)
    
    def setup_property_registrations(self) -> None:
        """Set up property registrations for PropertyGroups."""
        # Define property registrations based on class names
        property_mappings = {
            'SETUPAUTO_PG_quicksort_props': {
                'target': bpy.types.Scene,
                'name': 'pattern_props',
                'type': 'CollectionProperty'
            },
            'SETUPAUTO_PG_bgimage_props': {
                'target': bpy.types.Scene,
                'name': 'bgimage_props',
                'type': 'PointerProperty'
            },
            'SETUPAUTO_PG_tools_props': {
                'target': bpy.types.Scene,
                'name': 'tools_props',
                'type': 'PointerProperty'
            }
        }
        
        for class_name, config in property_mappings.items():
            if class_name in self.property_groups:
                self.property_registrations[class_name] = config
    
    def register(self) -> None:
        """Register all discovered classes."""
        print(f"Auto-registering {len(self.classes)} classes and {len(self.property_groups)} PropertyGroups...")
        
        # Set flag to indicate auto-registration is active
        bpy.context.auto_registration_active = True
        
        # First register PropertyGroups
        for class_name, cls in self.property_groups.items():
            try:
                bpy.utils.register_class(cls)
                print(f"Registered PropertyGroup: {class_name}")
            except Exception as e:
                print(f"Error registering PropertyGroup {class_name}: {e}")
        
        # Register all other classes
        for cls in self.classes:
            try:
                bpy.utils.register_class(cls)
                print(f"Registered {cls.__name__}")
            except Exception as e:
                print(f"Error registering {cls.__name__}: {e}")
        
        # Register properties
        self.setup_property_registrations()
        for class_name, config in self.property_registrations.items():
            if class_name in self.property_groups:
                cls = self.property_groups[class_name]
                target = config['target']
                prop_name = config['name']
                prop_type = config['type']
                
                try:
                    if prop_type == 'CollectionProperty':
                        setattr(target, prop_name, bpy.props.CollectionProperty(type=cls))
                    elif prop_type == 'PointerProperty':
                        setattr(target, prop_name, bpy.props.PointerProperty(type=cls))
                    print(f"Registered property: {target.__name__}.{prop_name} ({prop_type})")
                except Exception as e:
                    print(f"Error registering property {target.__name__}.{prop_name}: {e}")
    
    def unregister(self) -> None:
        """Unregister all registered classes."""
        print(f"Auto-unregistering {len(self.classes)} classes and {len(self.property_groups)} PropertyGroups...")
        
        # Unregister properties first
        for class_name, config in self.property_registrations.items():
            target = config['target']
            prop_name = config['name']
            
            try:
                if hasattr(target, prop_name):
                    delattr(target, prop_name)
                    print(f"Unregistered property: {target.__name__}.{prop_name}")
            except Exception as e:
                print(f"Error unregistering property {target.__name__}.{prop_name}: {e}")
        
        # Unregister all classes in reverse order
        for cls in reversed(self.classes + list(self.property_groups.values())):
            try:
                bpy.utils.unregister_class(cls)
                print(f"Unregistered {cls.__name__}")
            except Exception as e:
                print(f"Error unregistering {cls.__name__}: {e}")
        
        # Clear auto-registration flag
        if hasattr(bpy.context, 'auto_registration_active'):
            delattr(bpy.context, 'auto_registration_active')
    
    def get_registration_info(self) -> Dict[str, List[str]]:
        """Get information about what will be registered."""
        return {
            'PropertyGroups': list(self.property_groups.keys()),
            'Other Classes': [cls.__name__ for cls in self.classes],
            'Properties': list(self.property_registrations.keys())
        }

# Global instance
auto_reg = AutoRegistration(__name__)

def register():
    """Register all classes automatically."""
    auto_reg.discover_classes()
    auto_reg.register()

def unregister():
    """Unregister all classes automatically."""
    auto_reg.unregister()

# Utility function to get registration info
def get_registration_info():
    """Get information about what classes will be registered."""
    return auto_reg.get_registration_info()
