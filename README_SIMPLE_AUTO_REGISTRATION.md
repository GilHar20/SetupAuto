# Auto-Registration System for Blender Addon

This document explains the automatic registration system that eliminates the need for manual class registration in your Blender addon. This system is based on Jacques Lucke's proven approach from the Animation Nodes addon, updated for Blender 4.5.

## Overview

The auto-registration system automatically discovers and registers all Blender classes from all modules in your addon. It handles two main categories:

1. **PropertyGroups**: Classes that inherit from `bpy.types.PropertyGroup` (need special property registration)
2. **All Other Classes**: Operators, Panels, AddonPreferences, etc. (registered normally)

## How It Works

### 1. Class Discovery
The system automatically discovers classes from all imported modules in your addon:
- Uses module introspection to find all submodules
- Discovers classes that inherit from any `bpy.types.*` class
- Identifies classes with Blender-specific attributes (`bl_idname`, `bl_label`)
- Are not the auto-registration class itself

### 2. Class Categorization
Classes are automatically categorized into two groups:
- **PropertyGroups**: Classes inheriting from `bpy.types.PropertyGroup`
- **Other Classes**: All other Blender classes (Operators, Panels, etc.)

### 3. Registration Process
1. **PropertyGroups are registered first** (required for property registration)
2. **All other classes are registered**
3. **Properties are registered** (CollectionProperty/PointerProperty)

## Usage

### Basic Setup

1. **Import the auto-registration module** in your main `__init__.py`:
```python
from . import auto_registration
```

2. **Import all your modules** to ensure classes are available:
```python
from . import quicksort
from . import bgimage
from . import Tools
```

3. **Use the auto-registration functions**:
```python
def register():
    auto_registration.register()

def unregister():
    auto_registration.unregister()
```

### Property Registration Configuration

The system automatically handles PropertyGroups based on predefined mappings:

- **SETUPAUTO_PG_quicksort_props** → `bpy.types.Scene.pattern_props` (CollectionProperty)
- **SETUPAUTO_PG_bgimage_props** → `bpy.types.Scene.bgimage_props` (PointerProperty)
- **SETUPAUTO_PG_tools_props** → `bpy.types.Scene.tools_props` (PointerProperty)

To add new PropertyGroups, modify the `setup_property_registrations()` method in `auto_registration.py`:

```python
property_mappings = {
    'YOUR_PROPERTY_GROUP_CLASS': {
        'target': bpy.types.Scene,  # or other Blender type
        'name': 'your_property_name',
        'type': 'PointerProperty'  # or 'CollectionProperty'
    }
}
```

## Benefits

1. **No Manual Registration**: Eliminates the need to manually register each class
2. **Automatic Discovery**: New classes are automatically discovered and registered
3. **Simple Logic**: Only two categories to manage (PropertyGroups vs Others)
4. **Error Reduction**: Reduces registration errors and missing classes
5. **Maintainability**: Easier to maintain as the addon grows

## Migration from Manual Registration

### Before (Manual Registration)
```python
# In each module's __init__.py
def register():
    properties.register()
    operator.register()
    ui.register()

# In each file
def register():
    bpy.utils.register_class(MY_CLASS)

def unregister():
    bpy.utils.unregister_class(MY_CLASS)
```

### After (Auto Registration)
```python
# In main __init__.py
def register():
    auto_registration.register()

def unregister():
    auto_registration.unregister()

# Individual files no longer need register/unregister methods
```

## File Structure

```
your_addon/
├── __init__.py              # Main addon file with auto-registration
├── auto_registration.py     # Auto-registration system
├── test_simple_auto_registration.py # Test script
├── module1/
│   ├── __init__.py          # Just imports (no register/unregister)
│   ├── properties.py        # PropertyGroups (no register/unregister)
│   ├── operator.py          # Operators (no register/unregister)
│   └── ui.py               # Panels (no register/unregister)
└── module2/
    ├── __init__.py
    └── ...
```

## Testing

You can test the auto-registration system using the provided test script:

```bash
python test_simple_auto_registration.py
```

This will show you:
- All discovered classes
- How they're categorized
- Which properties will be registered

## Troubleshooting

### Common Issues

1. **Classes not discovered**: Ensure the class inherits from a `bpy.types.*` class
2. **Property not registered**: Check the property mappings in `setup_property_registrations()`
3. **Import errors**: Make sure all modules are imported in the main `__init__.py`

### Debug Information

The system provides detailed logging during registration:
- Which classes are being registered
- Any errors during registration
- Property registration details

## Key Features

- **Proven Approach**: Based on Jacques Lucke's successful Animation Nodes implementation
- **Simple**: Only two categories (PropertyGroups vs Others)
- **Automatic**: No manual class tracking needed
- **Module-based**: Uses Python's module system for reliable discovery
- **Flexible**: Easy to add new PropertyGroup mappings
- **Robust**: Handles errors gracefully with detailed logging
- **Maintainable**: Clean separation of concerns
- **Blender 4.5 Compatible**: Updated for modern Blender versions
