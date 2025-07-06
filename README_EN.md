# rF2 Export Tools for Blender 4.0

This is an addon that exports camera, grid, and light information for rFactor2 from Blender 4.0.2.  
It integrates three tools into a single addon.

---

## Table of Contents

1. [Installation](#installation)  
2. [How to Use Each Tool](#how-to-use-each-tool)  
   - [2-1. How to Use ExportCamera](#2-1-how-to-use-exportcamera)  
   - [2-2. How to Use ExportGrid](#2-2-how-to-use-exportgrid)  
   - [2-3. How to Use ExportLight](#2-3-how-to-use-exportlight)  
3. [License](#license)  

---

## Installation

1. Download the ZIP file from the GitHub repository by clicking `Code` → `Download ZIP`.  
2. Open Blender and go to `Edit > Preferences > Add-ons > Install...`.  
3. Select the downloaded ZIP file without extracting it.  
4. Enable the addon named `rF2 Export Tools`.

---

## How to Use Each Tool

### 2-1. How to Use ExportCamera

- Found in the `rF2 tool` tab of the Sidebar under the "Export camera" panel.
- Select a camera object and configure the following:
  - `LOD multiplier`: LOD scale factor
  - `Valid Paths`: Checkboxes for Main and/or Pit
  - `Groups`: Camera groups (multiple can be selected)
  - `handle as movement`: Toggle for moving camera behavior
  - `Movement Rate`: Speed of camera movement (only when movement is enabled)
- Naming help is available optionally for guidance.

#### ✅ Setting Up Child Objects (Static & Moving Cameras)

- Add a **circle mesh** as a child of the camera.
  - This will be exported as the `ActivationLocation`.
- For **moving cameras**, additionally:
  - Add multiple **Plane** meshes as children of the camera.
  - These will be exported as `ControlPoint` entries in the `MovementPath`.
  - Name them sequentially like `Plane`, `Plane.001`, `Plane.002`, etc.

- Click the `Export` button to save the `.txt` output file.

---

### 2-2. How to Use ExportGrid

- Found in the `rF2 tool` tab of the Sidebar under the "Export Grid" panel.
- Click the `Add Triangle` button to insert a triangle mesh facing the +Z direction.
- Based on object names, they are categorized and transformed automatically into rFactor2's coordinate system.
- Adjust `Y Offset` to avoid objects being embedded in the ground.

#### ✅ About Triangle Orientation

- Make sure the **pointed tip of the triangle faces the driving direction** of the vehicle.

#### ⚠️ Important Notes

- Objects are categorized based on the **prefix of their name**, such as:
  - `grid`, `altgrid`, `pit`, `garage`, `teleport`, `aux`
- If other objects in the scene start with these same prefixes, they **may be mistakenly exported**.
- Do **not use these prefixes for unrelated objects**.

- Click the `Export` button to generate the `.txt` file.

---

### 2-3. How to Use ExportLight

- Found in the `rF2 tool` tab of the Sidebar under the "Export Light" panel.
- All **light objects (especially Point Lights)** in the Blender scene will be collected and exported in rFactor2 format.

#### ✅ Editing Light Parameters

- Configure the following parameters from the **Properties Editor > Light (bulb icon)**:
  - **Energy** → Exported as `Intensity`
  - **Color** → Converted to RGB (0–255)
  - **Shadow Soft Size** → Used as the maximum value in `Range`

- You can choose any filename, but the extension is forcibly set to `.txt`.

---

## Common Notes for All Export Targets

- Export order is determined by the **number suffix** in the object name (e.g. `.001`, `.002`).
- Objects with **smaller numbers are exported first**.
- Objects **without a number** are treated as `.000` and exported **before numbered ones**.
- To ensure proper ordering, use names like `name`, `name.001`, `name.002`, etc.

---

## License

This addon is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

- You are free to use, modify, and redistribute this software.
- If you modify the source code, you must release it under the same license.

For more details, see the [official GNU license page](https://www.gnu.org/licenses/gpl-3.0.html).

---
