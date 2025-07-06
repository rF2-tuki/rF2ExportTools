bl_info = {
    "name": "Export rF2 grid",
    "author": "OpenAI",
    "version": (2, 0),
    "blender": (4, 0, 2),
    "location": "View3D > Sidebar > rF2 tool",
    "description": "Export grid by triangle mesh data",
    "category": "Import-Export",
}

import bpy
import math
import os
import mathutils
import pathlib
import re
from collections import defaultdict

pi=math.pi

class AddTriangleOperator(bpy.types.Operator):
    bl_idname = "object.add_triangle_at_cursor"
    bl_label = "Add Triangle"
    bl_description = "Add a triangle at the 3D cursor"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        mesh = bpy.data.meshes.new("rename_it")
        obj = bpy.data.objects.new("rename_it", mesh)

        verts = [
            (0, 0, -2.25),
            (1, 0, 2.25),
            (-1, 0, 2.25)
        ]
        faces = [(0, 2, 1)]
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        obj.location = context.scene.cursor.location
        obj.rotation_euler = (math.radians(90), 0, 0)  # ← X軸に90度回転を追加
        context.collection.objects.link(obj)
        obj.select_set(True)
        context.view_layer.objects.active = obj

        return {'FINISHED'}
        
class ExportGridSettings(bpy.types.PropertyGroup):
    grid_z_offset: bpy.props.FloatProperty(
        name="Y Offset",
        description="Add y-coordinates to avoid being buried in the ground",
        default=0.0,
        min=0.0,
        max=10.0
    )
    show_naming_help: bpy.props.BoolProperty(
        name="Show Naming Help",
        description="Display naming convention tips below",
        default=False
    )
    
class ExportGridDataOperator(bpy.types.Operator):
    bl_idname = "export_scene.grid_data"
    bl_label = "Export Grid Data"
    bl_description = "Export triangle-based grid data"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(
        subtype="FILE_PATH",
        default="grid_export.txt"
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        
        grid_z_offset = context.scene.export_grid_settings.grid_z_offset
        
        path = pathlib.Path(self.filepath)
        if path.suffix.lower() != ".txt":
            path = path.with_suffix(".txt")
        self.filepath = str(path)

        sections = {
            "grid": [],
            "altgrid": [],
            "teleport": [],
            "aux": [],
            "pits": defaultdict(lambda: {"pit": None, "garages": []}),
        }

        for obj in bpy.data.objects:
            if obj.type != 'MESH':
                continue

            name = obj.name.lower()
            base_name = name.split('.')[0]  

# ガレージの extra_suffix 抽出（_n が .の前にある場合のみ）
# 例: garage_2.001 → extra_suffix = 2
            extra_gar_match = re.search(r"_(\d+)(?:\.\d+)?$", name)
            extra_suffix = int(extra_gar_match.group(1)) if extra_gar_match else None
               

# インデックス抽出（.001 → 1）、なければ 0（つまり .000 相当）
            match = re.search(r"\.(\d+)$", name)
            index = int(match.group(1)) if match else 0
            
            # 座標と回転の変換
            pos = obj.location
            rot = obj.rotation_euler
            conv_pos = (pos.x, pos.z+grid_z_offset, pos.y)
            conv_rot = (rot.x - pi/2, -rot.z + pi, rot.y)

            if name.startswith("grid"):
                sections["grid"].append((index, conv_pos, conv_rot))

            elif name.startswith("altgrid"):
                sections["altgrid"].append((index, conv_pos, conv_rot))

            elif name.startswith("teleport"):
                sections["teleport"].append((index, conv_pos, conv_rot))

            elif name.startswith("aux"):
                sections["aux"].append((index, conv_pos, conv_rot))

            elif name.startswith("pit"):
                sections["pits"][index]["pit"] = (conv_pos, conv_rot)

            elif name.startswith("garage"):
                sections["pits"][index]["garages"].append((extra_suffix or 1, conv_pos, conv_rot))

        # 書き出し開始
        with open(self.filepath, 'w') as f:
            def write_section(title, data, index_name):
                f.write(f"[{title.upper()}]\n")
                for i, (idx, pos, ori) in enumerate(sorted(data, key=lambda x: x[0])):
                    f.write(f"{index_name}={idx}\n")
                    f.write(f"Pos=({pos[0]:.3f},{pos[1]:.3f},{pos[2]:.3f})\n")
                    f.write(f"Ori=({ori[0]:.3f},{ori[1]:.3f},{ori[2]:.3f})\n")
                f.write("\n")  # ← セクション末尾に空行（中身が空でも付ける）

            write_section("GRID", sections["grid"], "GridIndex")
            write_section("ALTGRID", sections["altgrid"], "GridIndex")
            write_section("TELEPORT", sections["teleport"], "GridIndex")

            # PITS
            f.write("[PITS]\n")
            any_written = False
            for team_index in sorted(sections["pits"].keys()):
                pit_data = sections["pits"][team_index]
                if pit_data["pit"]:
                    any_written = True
                    pit_pos, pit_ori = pit_data["pit"]
                    f.write(f"TeamIndex={team_index}\n")
                    f.write(f"PitPos=({pit_pos[0]:.3f},{pit_pos[1]:.3f},{pit_pos[2]:.3f})\n")
                    f.write(f"PitOri=({pit_ori[0]:.3f},{pit_ori[1]:.3f},{pit_ori[2]:.3f})\n")
                    for suffix, gar_pos, gar_ori in sorted(pit_data["garages"], key=lambda x: x[0]):
                        x_val = max(suffix - 1, 0)
                        f.write(f"GarPos=({x_val},{gar_pos[0]:.3f},{gar_pos[1]:.3f},{gar_pos[2]:.3f})\n")
                        f.write(f"GarOri=({x_val},{gar_ori[0]:.3f},{gar_ori[1]:.3f},{gar_ori[2]:.3f})\n")
            f.write("\n")  # ← PITSも必ず空行

            write_section("AUX", sections["aux"], "LocationIndex")

        self.report({'INFO'}, "Grid data exported successfully.")
        return {'FINISHED'}
        
class Grid_PT_ExportPanel(bpy.types.Panel):
    bl_label = "Export Grid"
    bl_idname = "Grid_PT_setting"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'rF2 tool'
    
    def draw(self, context):
        
        settings = context.scene.export_grid_settings
        
        layout = self.layout
        layout.operator("object.add_triangle_at_cursor", text="Add Triangle")
        layout.prop(settings, "grid_z_offset")
        layout.operator("export_scene.grid_data", text="Export")
        layout.prop(settings, "show_naming_help")

        if settings.show_naming_help:
            layout.label(text="Naming")
            layout.label(text="pitbox -> pit.xxx")
            layout.label(text="garage1 -> garage.xxx")
            layout.label(text="garage2 -> garage_2.xxx")
            layout.label(text="garage3 -> garage_3.xxx")
            layout.label(text="SafetyCar -> aux.xxx")
            layout.label(text="grid -> grid.xxx")
            layout.label(text="altgrid -> altgrid.xxx")
            layout.label(text="teleport -> teleport.xxx")
        
classes = [
    AddTriangleOperator,
    ExportGridSettings,
    ExportGridDataOperator,
    Grid_PT_ExportPanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.export_grid_settings = bpy.props.PointerProperty(type=ExportGridSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.export_grid_settings

if __name__ == "__main__":
    register()