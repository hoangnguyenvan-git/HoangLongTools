# 🧱 NguyenHoang.RBM – Rebar Detailing Toolkit for Revit

A comprehensive **Rebar Detailing Automation Tool** for Autodesk Revit 2024+, developed for **pyRevit v5.0.0**.  
This toolkit combines multiple modules that simplify and enhance **reinforcement bar (rebar)** workflows — from visualization and filtering to full detailing automation, dimensioning, and export.

---

## 🚀 Features

### 🔹 Rebar Visualization & Management
- **Filter & Colorize** rebars by parameters such as diameter, partition, or schedule mark.  
- **Visibility Control**: Toggle rebar visibility for clear drawing presentation.
- **Drafting View Creation**: Automatically generate drafting views per partition for detailing layouts.

### 🔹 Intelligent Rebar Calculation
- Automated **lap splice length** computation.
- Average and total **bar length calculation** with live progress tracking.
- Group-based classification and case detection.
- Supports both **M_SP**, **MT3**, and other custom shape logic.

### 🔹 Rebar Detailing Automation
- Auto-generate **detailing drawings** directly in Revit Drafting Views:
  - MSP, MT3, L-shape, C-shape, DVCKN, and more.
  - Includes annotation text, lap splice signature, header notes, and dimensions.
- **Rotate**, **scale**, or **delete** rebar detail groups dynamically.
- Group management with reusable **GroupType** creation and safe updates.

### 🔹 Dimensioning & Annotation
- Smart dimension generation for arcs, lines, and radii.
- Auto-offset and text rotation for clean readable annotations.
- Support for filled region arrows, lap splice notes, and header textnotes.

### 🔹 Built for Real-World Projects
- Optimized caching for large models.
- Minimal API calls and grouped transactions.
- Error-tolerant logging and UI feedback integration.

---

## 🧩 Project Structure

| Module | Description |
|--------|-------------|
| `NguyenHoang.RBM.RebarDetailing` | Main detailing and layout logic |
| `NguyenHoang.RBM.RebarCalculation` | Rebar calculation and classification engine |
| `NguyenHoang.RBM.RebarUltils` | Utility methods for parameter access, caching, and shape detection |
| `NguyenHoang.RBM.DimensionControl` | Helpers for drawing dimensions and filled regions |
| `NguyenHoang.RBM.AnnotationControl` | Handles annotation text placement and geometry |
| `NguyenHoang.RBM.ElementCollector` | Centralized element and type collection logic |
| `NguyenHoang.RBM.FilterColorize` | Visual filtering and colorization of rebars |
| `NguyenHoang.RBM.CoordinateSystem` | Coordinate transformation helpers |
| `NguyenHoang.RBM.Msb` | Custom message box UI |
| `NguyenHoang.RBM.Login` | Authentication session management |
| `NguyenHoang.RBM.Constant` | Global constants and default values |

---

## ⚙️ Requirements

| Component | Version |
|------------|----------|
| **Autodesk Revit** | 2024 or later |
| **pyRevit** | v5.0.0 ([Download here](https://github.com/pyrevitlabs/pyRevit/releases)) |
| **.NET Framework** | 4.8+ |
| **Windows OS** | Windows 10 / 11 |

---

## 🪜 Installation Guide

### 1️⃣ Install pyRevit (if not yet installed)
- Go to: [https://github.com/pyrevitlabs/pyRevit/releases](https://github.com/pyrevitlabs/pyRevit/releases)
- Download and install **pyRevit v5.0.0**.
- Verify installation by running in CMD:
  ```bash
  pyrevit env
  ```

### 2️⃣ Clone or Download this Extension
Clone this repository into your desired folder:
```bash
git clone https://github.com/<your-username>/NguyenHoang.RBM.git
```

or download and extract it manually.

### 3️⃣ Add the Extension Path to pyRevit
Run the following command in Command Prompt:
```bash
pyrevit extensions paths add "C:\Path\To\NguyenHoang.RBM"
```

### 4️⃣ Launch Revit
- Open **Revit 2024 or newer**.
- You’ll see a new **"NguyenHoang.RBM"** tab in the pyRevit ribbon.
- Start exploring the rebar detailing tools.

---

## 🔁 Updating the Tool

To update to the latest version:

1. Pull the latest version from GitHub, or overwrite your local folder.
2. Run the included **`Update.BAT`** file — it will automatically refresh the extension path in pyRevit.
3. Restart Revit and enjoy the new features.

---

## 📘 Usage Overview

1. **Open your Revit Project** containing structural rebars.  
2. Launch **NguyenHoang.RBM** from the pyRevit tab.  
3. Use the available buttons:
   - **Rebar Calculation** → computes rebar lengths, laps, and classification.
   - **Rebar Detailing** → generates drafting views with annotations.
   - **Colorize / Filter Rebars** → visualize model rebars by attributes.
   - **Rotate / Scale / Delete** → adjust generated detail groups.
4. The tool will log progress and colorize messages per partition and mark.

---

## 🧠 Developer Notes

- Developed in **C# 7.3**, compatible with **Revit 2024 API**.  
- Uses pyRevit’s dynamic command registration system.
- Transactions are safely managed for all Revit DB operations.
- Fully modular architecture — easy to expand for new shape logics.

---

## 🧑‍💻 Contributing

Contributions are welcome!  
If you’d like to improve or add new shape detection/visualization logic:
- Fork the repo.
- Create a new branch: `feature/new-shape-support`.
- Submit a pull request with clear comments.

---

## 🛠️ Troubleshooting

| Issue | Solution |
|--------|-----------|
| ❌ “pyRevit not recognized” | Ensure pyRevit v5.0.0 is installed and added to PATH |
| ❌ “Object reference not set” | Check that your rebars have valid Partition & Schedule Mark |
| ❌ “Missing styles or templates” | Run detailing again — it will auto-create missing styles |
| ⚠️ “No drafting views found” | The tool auto-generates them; verify project permissions |

---

## 📜 License

This project is distributed for testing and educational use.  
All rights reserved © 2025 Nguyen Hoang.
