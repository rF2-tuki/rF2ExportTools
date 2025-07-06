bl_info = {
    "name": "Export rF2 Lights",
    "author": "OpenAI",
    "version": (1, 0),
    "blender": (4, 0, 2),
    "location": "View3D > Sidebar > rF2 tool",
    "description": "Export nightlight to a formatted .txt file",
    "category": "Import-Export",
}

import bpy
from bpy.types import Panel, Operator
from bpy.props import StringProperty
import os

class ExportLightSettings(bpy.types.PropertyGroup):
    show_naming_help: bpy.props.BoolProperty(
        name="Show Naming Help",
        description="Display naming convention tips below",
        default=False
    )


def format_object_name(obj_name):
    if '.' in obj_name:
        suffix = obj_name.split('.')[-1]
        try:
            return f'{int(suffix):02d}'
        except ValueError:
            return '00'
    else:
        return '00'


def format_light_data(light_obj):
    light_index = format_object_name(light_obj.name)
    name_line = f'Light=Nightlight{light_index}'

    loc = light_obj.location
    pos = f'Pos=({loc.x:.6f}, {loc.z:.6f}, {loc.y:.6f})'

    data = light_obj.data
    clip_out = getattr(data, 'shadow_soft_size', 0.0)
    power = getattr(data, 'energy', 0.0)
    color = getattr(data, 'color', (1.0, 1.0, 1.0))

    range_line = f'Range=(0.000000, {clip_out:.6f})'
    intensity_line = f'Intensity=({power:.1f})'
    color_line = f'Color=({color[0]*255:.0f}, {color[1]*255:.0f}, {color[2]*255:.0f})'

    return (
        f'{name_line} \n'
        '{\n'
        f' Type=Omni {pos} {range_line} Active=True {intensity_line} {color_line} \n'
        '}\n'
    )


class EXPORT_OT_lights_to_txt(Operator):
    bl_idname = "export_scene.lights_to_txt"
    bl_label = "Export Lights to .txt"

    filepath: StringProperty(
        name="File Path",
        description="Filepath used for exporting",
        subtype='FILE_PATH',
    )

    def execute(self, context):
        if not self.filepath.lower().endswith(".txt"):
            self.filepath += ".txt"

        text_output = ""
        for obj in bpy.context.scene.objects:
            if obj.type == 'LIGHT':
                text_output += format_light_data(obj)

        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(text_output)
            self.report({'INFO'}, f"Exported to {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class EXPORT_PT_lights_panel(Panel):
    bl_label = "Export Light"
    bl_idname = "EXPORT_PT_lights_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'rF2 tool'

    def draw(self, context):
    
        settings = context.scene.export_Light_settings
    
        layout = self.layout
        layout.operator("export_scene.lights_to_txt", text="Export", icon='LIGHT')
        layout.prop(settings, "show_naming_help")

        if settings.show_naming_help:
            layout.label(text="Naming")
            layout.label(text="NightLight -> Nightlight.xxx")
            layout.label(text="Objects must be Light->Point")


classes = (
    EXPORT_OT_lights_to_txt,
    EXPORT_PT_lights_panel,
    ExportLightSettings
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.export_Light_settings = bpy.props.PointerProperty(type=ExportLightSettings)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.export_Light_settings


if __name__ == "__main__":
    register()
