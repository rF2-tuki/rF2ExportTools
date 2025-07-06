bl_info = {
    "name": "rF2 Export Tools",
    "author": "OpenAI",
    "version": (1, 0),
    "blender": (4, 0, 2),
    "location": "View3D > Sidebar > rF2 tool",
    "description": "Export tools for rFactor2: camera, grid, and lights",
    "category": "Import-Export",
}

import importlib
import bpy

# サブモジュールのインポート
from . import exportcamera
from . import exportgrid
from . import exportlight

# モジュールをホットリロード（Blenderの再読み込みで反映されるように）
importlib.reload(exportcamera)
importlib.reload(exportgrid)
importlib.reload(exportlight)

def register():
    exportcamera.register()
    exportgrid.register()
    exportlight.register()

def unregister():
    exportcamera.unregister()
    exportgrid.unregister()
    exportlight.unregister()
