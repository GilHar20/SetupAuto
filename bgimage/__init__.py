# Bgimage module initialization

from . import operator
from . import properties
from . import ui

def register():
    properties.register()
    operator.register()
    ui.register()

def unregister():
    ui.unregister()
    operator.unregister()
    properties.unregister()
