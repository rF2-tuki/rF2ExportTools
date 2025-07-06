bl_info = {
    "name": "Export rF2 camera",
    "author": "OpenAI",
    "version": (1, 0),
    "blender": (4, 0, 2),
    "location": "View3D > Sidebar > rF2 tool",
    "description": "Export camera by child circle mesh data ",
    "category": "Import-Export",
}

import bpy
import math
import os
import mathutils
import pathlib

pi = math.pi

class ExportCameraSettings(bpy.types.PropertyGroup):

    LOD_val: bpy.props.FloatProperty(
        name="LOD multiplier",
        description="LOD Multiplier",
        default=1.0,
        min=0.1,
        max=6.0
    )
    use_path_main: bpy.props.BoolProperty(
        name="Main", 
        description="Enable on main path", 
        default=False
    )
    use_path_pit: bpy.props.BoolProperty(
        name="Pit", 
        description="Enable on pit path", 
        default=False
    )
    #set group
    group_1: bpy.props.BoolProperty(
    name="1", 
    description="Group1", 
    default=False
    )
    group_2: bpy.props.BoolProperty(
    name="2", 
    description="Group2", 
    default=False
    )
    group_3: bpy.props.BoolProperty(
    name="3", 
    description="Group3", 
    default=False
    )
    group_4: bpy.props.BoolProperty(
    name="4", 
    description="Group4", 
    default=False
    )
    #for movement camera
    export_controlpoint: bpy.props.BoolProperty(
    name="handle as movement",
    description="when checked camera is handled as movement.",
    default=False
    )
    movement_rate: bpy.props.FloatProperty(
    name="Movement Rate",
    description="Speed of movement",
    default=0.25,
    min=0.0,
    max=1.0
    )
    show_naming_help: bpy.props.BoolProperty(
    name="Show Naming Help",
    description="Display naming convention tips below",
    default=False
    )


class ExportTrackingCameraOperator(bpy.types.Operator):
    bl_idname = "export_scene.tracking_static_camera"
    bl_label = "Export"
    bl_description = "Export selected camera"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(
        subtype="FILE_PATH",
        default="camera_export.txt"
    )

    def execute(self, context):
        path = pathlib.Path(self.filepath)
        if path.suffix.lower() != ".txt":
            path = path.with_suffix(".txt")
        self.filepath = str(path)

        cam = context.object
        if not cam or cam.type != 'CAMERA':
            self.report({'ERROR'}, "Please select a camera object")
            return {'CANCELLED'}

        cam_name = cam.name
        cam_type = "Static" if cam_name.lower().startswith('s') else "Tracking"
        circles = [child for child in cam.children if child.type == 'MESH' and 'circle' in child.name.lower()]

        if not circles:
            self.report({'ERROR'}, "No child circle mesh found under the camera")
            return {'CANCELLED'}

        cam_loc = cam.location
        cam_rot_euler = cam.rotation_euler
        cam_rot_rad = tuple(cam_rot_euler)

        # Obtained from the camera body, such as FOV
        cam_data = cam.data
        fov_val = math.degrees(cam_data.angle)
        clip_start = cam_data.clip_start
        clip_end = cam_data.clip_end
        settings = context.scene.export_camera_settings
        LOD_val = settings.LOD_val
        main = settings.use_path_main
        pit = settings.use_path_pit

        if main and not pit:
            valid_path = 1
        elif pit and not main:
            valid_path = 2
        else:
            valid_path = 0
            
        # Groups（bit addition）
        group_val = 0
        if settings.group_1:
            group_val += 1
        if settings.group_2:
            group_val += 2
        if settings.group_3:
            group_val += 4
        if settings.group_4:
            group_val += 8
        if group_val == 0:
            group_val = 15 #when nothing are chosen set as all
            
        activation_lines = []
        for circle in circles:
            loc = circle.location
            radius = (circle.dimensions.x + circle.dimensions.y) / 4.0
            activation_lines.append(f"  ActivationLocation=({-loc.x:.6f}, {-loc.z:.6f}, {-loc.y:.6f})\n")
            activation_lines.append(f"  ActivationRadius=({radius:.6f})\n")

        LOD_val = context.scene.export_camera_settings.LOD_val
        settings = context.scene.export_camera_settings
        main = settings.use_path_main
        pit = settings.use_path_pit

        with open(self.filepath, 'w') as f:
            f.write(f"{cam_type}Cam={cam_name} \n")
            f.write("{\n")
            f.write(f"  Fov=(38.000000, {fov_val:.6f})\n")
            f.write("  Clear=FALSE\n")
            f.write("  Color=(0, 0, 0)\n")
            f.write(f"  ClipPlanes=({clip_start:.6f}, {clip_end:.6f})\n")
            f.write(f"  LODMultiplier=({LOD_val:.1f})\n")
            f.write("  Size=(1.000000, 1.000000)\n")
            f.write("  Center=(0.500000, 0.500000)\n")
            f.write("  MipmapLODBias=(1.000000)\n")
            f.write("  Flags1=(2)\n")
            f.write("  Flags2=(0)\n")
            f.write(f"  ValidPaths=({valid_path})\n")
            f.write("  SoundName=\"\"\n")
            f.write("  SoundParams=(1.000,1,15)\n")
            f.write("  MinShadowRange=(0.100)\n")
            f.write("  MaxShadowRange=(200.000)\n")
            f.write("  ShadowSplitRatio=(0.920)\n")
            f.write("  mPostProcessPresetIndex=(3)\n")
            for i in range(6):
                f.write("  ShadowParams=(0.000050,1.000,100.000)\n")
            f.write("  ShadowParams=(0.000050,1.000,0.000)\n")
            f.write("  ShadowParams=(0.000000,0.000,0.000)\n")
            f.write(f"  Position=({-cam_loc.x:.6f}, {-cam_loc.z:.6f}, {-cam_loc.y:.6f})\n")
            f.write(f"  Orientation=({cam_rot_rad[0]-pi/2:.6f}, {cam_rot_rad[2]:.6f}, {cam_rot_rad[1]:.6f})\n")

            for line in activation_lines:
                f.write(line)

            f.write("  ListenerVol=(1.200000)\n")
            f.write("  RainVol=(1.000000)\n")
            f.write(f"  Groups={group_val}\n")
            f.write("  TrackingRate=(30.0)\n")
            f.write("  PositionOffset=(0.000000, 0.000000, 0.000000)\n")
        # Use movement_rate only if export_controlpoint is enabled
            if settings.export_controlpoint:
                movement_rate_val = settings.movement_rate
            else:
                movement_rate_val = 0.0

            f.write(f"  MovementRate=({movement_rate_val:.6f})\n")
            f.write("  MinimumFOV=(10.000006)\n")
            f.write("  MaximumZoomFactor=(0.100000)\n")

            if settings.export_controlpoint:
                # Extract Plane.xxx out of camera children
                plane_children = []
                for child in cam.children:
                    if child.type == 'MESH' and child.name.startswith("Plane"):
                        # Collect child objects named "Plane" or "Plane.xxx"
                        suffix = child.name[5:]  # Portion after "Plane"
                        if suffix.startswith(".") and suffix[1:].isdigit():
                            number = int(suffix[1:])
                        elif suffix == "":
                            number = 0
                        else:
                            continue  # Skip if name is not in expected format, like "PlaneExtra"
                        plane_children.append((number, child))

                if not plane_children:
                    self.report({'ERROR'}, "Camera has no child objects named 'Plane.xxx'")
                    return {'CANCELLED'}
                    
                f.write("  MovementPath\n")
                f.write("  {\n")
                    
                # sort by number and output ControlPoint
                for _, plane_obj in sorted(plane_children, key=lambda x: x[0]):
                    loc = plane_obj.location
                    f.write(f"    ControlPoint=({-loc.x:.6f}, {-loc.z:.6f}, {-loc.y:.6f})\n")
                f.write("  }\n")
            f.write("}\n")

        self.report({'INFO'}, "Camera export successful")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class Camera_PT_ExportPanel(bpy.types.Panel):
    bl_label = "Export camera"
    bl_idname = "camera setting"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'rF2 tool'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.export_camera_settings
        layout.prop(settings, "LOD_val")
        #path activates cam
        layout.label(text="activate on:")
        row = layout.row(align=True)
        row.prop(settings, "use_path_main", toggle=True)
        row.prop(settings, "use_path_pit", toggle=True)
        #group
        layout.label(text="Groups:")
        row = layout.row(align=True)
        row.prop(settings, "group_1", toggle=True)
        row.prop(settings, "group_2", toggle=True)
        row.prop(settings, "group_3", toggle=True)
        row.prop(settings, "group_4", toggle=True)
        layout.prop(settings, "export_controlpoint")
        if settings.export_controlpoint:
            layout.prop(settings, "movement_rate")
        layout.operator("export_scene.tracking_static_camera")
        layout.prop(settings, "show_naming_help")

        if settings.show_naming_help:
            layout.label(text="Naming")
            layout.label(text="TrakingCam -> Trackingxxx")
            layout.label(text="StaticCam -> Staticxxx")
            layout.label(text="ActivationLocation -> circle.xxx")
            layout.label(text="ControlPoint -> plane.xxx")

classes = [
    ExportCameraSettings,
    ExportTrackingCameraOperator,
    Camera_PT_ExportPanel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.export_camera_settings = bpy.props.PointerProperty(type=ExportCameraSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.export_camera_settings

if __name__ == "__main__":
    register()
