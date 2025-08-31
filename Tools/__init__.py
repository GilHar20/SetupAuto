#tools module  initialization

from . import duplicates2instances
from . import proximityjoin
from . import singleuser
from . import properties
from . import ui

def register():
    ui.register()
    properties.register()
    duplicates2instances.register()
    proximityjoin.register()
    singleuser.register()

def unregister():
    singleuser.unregister()
    proximityjoin.unregister()
    duplicates2instances.unregister()
    properties.unregister()
    ui.unregister()