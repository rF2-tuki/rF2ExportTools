# rF2 Export Tools for Blender 4.0

rFactor2 用のカメラ、グリッド、ライト情報を Blender 4.0.2 からエクスポートするアドオンです。  
3つの機能を1つのアドオンとして統合しています。

This is an addon that exports camera, grid, and light information for rFactor2 from Blender 4.0.2.  
It integrates three tools into a single addon.

---

## 目次 | Table of Contents

1. [インストール方法 | Installation](#インストール方法--installation)  
2. [それぞれのアドオンの使い方 | How to Use Each Tool](#それぞれのアドオンの使い方--how-to-use-each-tool)  
   - [2-1. ExportCameraの使い方 | How to Use ExportCamera](#2-1-exportcameraの使い方--how-to-use-exportcamera)  
   - [2-2. ExportGridの使い方 | How to Use ExportGrid](#2-2-exportgridの使い方--how-to-use-exportgrid)  
   - [2-3. ExportLightの使い方 | How to Use ExportLight](#2-3-exportlightの使い方--how-to-use-exportlight)  
3. [ライセンスについて | License](#ライセンスについて--license)  

---

## インストール方法 | Installation

1. GitHub リポジトリのページから `Code` → `Download ZIP` をクリックしてZIPファイルをダウンロードします。  
2. Blenderを起動し、`Edit > Preferences > Add-ons > Install...` を選択します。  
3. ダウンロードしたZIPファイルを選択してインストールします（展開せずにそのまま指定してください）。  
4. `rF2 Export Tools` を有効化します。

1. Download the ZIP file from the GitHub repository by clicking `Code` → `Download ZIP`.  
2. Open Blender and go to `Edit > Preferences > Add-ons > Install...`.  
3. Select the downloaded ZIP file without extracting it.  
4. Enable the addon named `rF2 Export Tools`.

---

## それぞれのアドオンの使い方 | How to Use Each Tool

### 2-1. ExportCameraの使い方 | How to Use ExportCamera

- サイドバーの「rF2 tool」タブにある「Export camera」パネルから使用します。
- カメラオブジェクトを選択し、以下を設定：

- Found in the `rF2 tool` tab of the Sidebar under the "Export camera" panel.
- Select a camera object and configure the following:

#### 設定項目 | Parameters

- `LOD multiplier`：LOD倍率 | LOD scale factor  
- `Valid Paths`：Main や Pit に対応するチェック | Main and/or Pit toggle  
- `Groups`：カメラグループ（複数可）| Camera groups (multiple)  
- `handle as movement`：可動カメラかどうか | Moving camera toggle  
- `Movement Rate`：動作速度（可動カメラのみ）| Movement speed (if enabled)  
- `Show Naming Help`：命名規則の表示 | Naming convention guidance  

#### ✅ 子オブジェクトの設定 | Setting Child Objects

- カメラの子として **circle（円）** オブジェクトを配置 → `ActivationLocation` として出力  
- Place a **circle mesh** as a child of the camera → used as `ActivationLocation`

- 可動カメラの場合、追加で **Plane（平面）** を複数配置 → `ControlPoint` として出力  
- For moving cameras, also add multiple **Plane** meshes → exported as `ControlPoint`

- `Export` を押すと `.txt` ファイルが出力されます。  
- Click `Export` to generate the `.txt` file.

---

### 2-2. ExportGridの使い方 | How to Use ExportGrid

- サイドバーの「rF2 tool」タブにある「Export Grid」パネルから使用します。  
- `Add Triangle` ボタンでZ+方向の三角形を追加できます。  
- `Y Offset` を調整して埋まりを防止可能。

- Found in the `rF2 tool` tab under "Export Grid".  
- Use `Add Triangle` to insert upward-facing triangles.  
- Use `Y Offset` to avoid sinking into ground.

#### ✅ 三角形の向き | Triangle Orientation

- 三角形の **尖った方向が進行方向を向く** ように配置してください。  
- Orient triangles so the **tip points in the driving direction**.

#### ⚠️ 名前による分類注意 | Name-Based Categorization

- オブジェクト名の接頭辞で分類されます：  
  `grid`, `altgrid`, `pit`, `garage`, `teleport`, `aux`  
- 他の目的でこれらの名前を使うと誤認識されます。

- Objects are categorized by **name prefix**, such as:  
  `grid`, `altgrid`, `pit`, `garage`, `teleport`, `aux`  
- Do not use these names for unrelated objects.

- `Export` を押すと `.txt` ファイルが出力されます。  
- Click `Export` to generate the `.txt` file.

---

### 2-3. ExportLightの使い方 | How to Use ExportLight

- サイドバーの「rF2 tool」タブにある「Export Light」パネルから使用します。  
- Blenderシーン内のすべてのライトを `.txt` 形式で出力します。  

- Found in the `rF2 tool` tab under "Export Light".  
- All light objects in the scene are exported in `.txt` format.

#### ✅ パラメータ編集 | Editing Light Parameters

- 以下の設定をライトの **データタブ（電球アイコン）** で調整します：  
  - Energy → `Intensity`  
  - Color → `Color` (0–255 RGB)  
  - Shadow Soft Size → `Range`

- Configure the following in the **Light Data tab (bulb icon)**:  
  - Energy → `Intensity`  
  - Color → `Color` (0–255 RGB)  
  - Shadow Soft Size → `Range`

- ファイル名は自由ですが、拡張子は `.txt` に固定されます。  
- Filename is flexible but will always end in `.txt`.

---

## 共通の注意点 | Common Notes

- オブジェクト名の末尾番号（例：`.001`, `.002`）で順序が決まります。  
- 小さい番号から順に出力され、番号なしは `.000` 扱いで先に出力されます。

- Export order is determined by the **suffix number** (e.g. `.001`, `.002`).  
- Lower numbers are exported first. Names without numbers are treated as `.000`.

- 正しい順で出力するには `name`, `name.001`, `name.002` などの命名を徹底してください。  
- Use consistent naming like `name`, `name.001`, `name.002` for proper order.

---

## ライセンスについて | License

このアドオンは **GNU General Public License v3.0 (GPL-3.0)** に準拠しています。

This addon is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

- 自由に利用、改変、再配布が可能です。  
- 改変した場合は同じライセンスで公開する必要があります。

- You are free to use, modify, and redistribute it.  
- If modified, it must be released under the same license.

詳しくは [GNU公式サイト](https://www.gnu.org/licenses/gpl-3.0.html) をご覧ください。  
For details, see the [official GNU site](https://www.gnu.org/licenses/gpl-3.0.html).

---
