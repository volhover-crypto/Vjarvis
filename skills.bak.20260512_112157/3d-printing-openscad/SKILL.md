---
name: openscad-3d
description: "3D modeling, CAD design, and STL file analysis. Generate 3D-printable models from text descriptions, analyze/inspect STL files, render previews, modify parametric designs, and convert between 3D formats."
metadata: {"clawdbot":{"emoji":"🧊","requires":{"bins":["openscad","python3","xvfb-run"]}}}
version: 1.0.0
---

# OpenSCAD 3D Modeling & STL Analysis

Full 3D modeling pipeline: generate models from descriptions, analyze STL files, render previews, and export for 3D printing.

## When to Trigger
- User asks to "design", "model", "create", "generate", or "make" a 3D object/part/model
- User asks to "analyze", "inspect", "read", "check", or "view" an STL/3MF file
- User mentions: 3D print, CAD, STL, OpenSCAD, parametric, model, part, enclosure, bracket, mount, gear
- User sends/references an STL file and wants info about it
- User asks to modify dimensions or parameters of a 3D model

## Commands

### Generate a 3D model from SCAD code
Write .scad code, then compile:
```bash
python3 {baseDir}/scripts/generate.py --code '<openscad_code>' --name 'part_name' --format stl
```

### Generate with parametric overrides
```bash
python3 {baseDir}/scripts/generate.py --code '<openscad_code>' --name 'part_name' --params 'width=50,height=30,wall=2'
```

### Render a PNG preview
```bash
python3 {baseDir}/scripts/generate.py --code '<openscad_code>' --name 'part_name' --format png --camera '0,0,0,45,0,35,200'
```

### Generate both STL and preview
```bash
python3 {baseDir}/scripts/generate.py --code '<openscad_code>' --name 'part_name' --format both
```

### Analyze an STL file
```bash
python3 {baseDir}/scripts/analyze.py '<path_to_stl>'
```
Returns: dimensions, volume, surface area, triangle count, watertight check, printability assessment, PLA cost estimate.

### Convert between formats
```bash
python3 {baseDir}/scripts/convert.py '<input_file>' --to <stl|3mf|obj|off|ply|glb>
```

### Generate from Python (SolidPython2)
For complex models, write a Python script using SolidPython2:
```bash
python3 {baseDir}/scripts/solidpy_gen.py --script '<python_code>' --name 'part_name'
```
The Python code must assign the result to a variable called `model`.

## OpenSCAD Quick Reference

### Primitives
- `cube([x,y,z])` or `cube(size, center=true)`
- `sphere(r=5)` or `sphere(d=10)`
- `cylinder(h=10, r=5)` or `cylinder(h=10, r1=5, r2=3)`
- `polyhedron(points, faces)`

### Transforms
- `translate([x,y,z])`, `rotate([x,y,z])`, `scale([x,y,z])`
- `mirror([1,0,0])`, `color("red")`
- `linear_extrude(height)` — extrude 2D to 3D
- `rotate_extrude(angle)` — lathe/revolve

### Boolean Operations
- `union() { ... }` — combine shapes
- `difference() { ... }` — subtract (first minus rest)
- `intersection() { ... }` — keep overlap only

### 2D Shapes (for extrusion)
- `square([x,y])`, `circle(r=5)`, `polygon(points)`
- `text("string", size=10)`, `import("file.svg")`

### Useful Patterns
- `for (i = [0:n]) { ... }` — loop
- `module name() { ... }` — reusable component
- `$fn = 100;` — curve smoothness

## Output Directory
`/root/openclaw-workspace/3d-models/`

## Tips for Code Generation
1. Always set `$fn` for curved surfaces (50-100)
2. Use `module` for reusable components
3. Use `difference()` for holes, cutouts, recesses
4. Think in adding and subtracting primitive shapes
5. Use `linear_extrude()` + 2D shapes for complex profiles
6. Common wall thickness for 3D printing: 1.5-3mm
