---
name: eda-kicad
description: AI-assisted EDA workflow for KiCad 7. Use when working with electronic schematics, PCB design, component selection, or manufacturing file generation. Triggers on: schematic, PCB, layout, routing, Gerber, BOM, component sourcing, KiCad, electronics design.
---

# EDA Workflow — KiCad 7

AI-assisted Electronic Design Automation workflow optimized for KiCad 7.0+.

## When to Use

- Creating or modifying electronic schematics
- PCB layout and routing
- Component selection and sourcing
- Generating manufacturing files (Gerber, drill, BOM)
- Design rule checking (DRC)
- 3D visualization of PCB

## Project Structure

```
project-name/
├── project-name.kicad_pro    # Project file
├── project-name.kicad_sch    # Schematic
├── project-name.kicad_pcb    # PCB layout
├── docs/
│   ├── design-constraints.json
│   └── project-spec.md
├── datasheets/               # Component documentation
├── production/               # Gerber, drill, BOM
└── .mcp.json                 # MCP server configuration
```

## Workflow

### 1. Project Initialization
```bash
# Create new EDA project
npx claude-eda init <project-name> -y --no-git

# Check environment
npx claude-eda doctor --fix
```

### 2. Component Sourcing
- Search LCSC/JLCPCB for components using `@jlcpcb/mcp`
- Check stock levels and pricing
- Download datasheets to `datasheets/`
- Create component library entries

### 3. Schematic Design
- Create hierarchical schematic sheets
- Use `kicad-sch` MCP server for schematic manipulation
- Run ERC (Electrical Rule Check)
- Generate netlist for PCB layout

### 4. PCB Layout
- Import netlist from schematic
- Place components according to design constraints
- Route traces (manual or autoroute with FreeRouter)
- Add copper pour, ground planes
- Run DRC (Design Rule Check)

### 5. Manufacturing Export
```bash
# Export Gerber files
kicad-cli pcb export gerbers <board.kicad_pcb> --output ./production/

# Export drill files
kicad-cli pcb export drill <board.kicad_pcb> --output ./production/

# Export BOM
kicad-cli sch export python-bom <schematic.kicad_sch> --output ./production/bom.csv

# Export pick-and-place
kicad-cli pcb export pos <board.kicad_pcb> --output ./production/
```

## MCP Servers

### JLCPCB Component Sourcing
- Search components by keyword, category, or specification
- Check real-time stock and pricing
- Access LCSC part numbers

### KiCad PCB MCP
- Read and modify PCB files programmatically
- Access board statistics, DRC results
- Manipulate footprints, tracks, zones

### KiCad Schematic MCP
- Read and modify schematic files
- Access netlist, component properties
- Run ERC checks

## Design Constraints

Store in `docs/design-constraints.json`:
```json
{
  "project": {
    "name": "board-name",
    "revision": "0.1",
    "description": "Board description"
  },
  "board": {
    "size": {"width": 100, "height": 150, "unit": "mm"},
    "layers": 4,
    "min_trace_width": 0.2,
    "min_clearance": 0.2,
    "min_via_drill": 0.3,
    "copper_weight": 1.0
  },
  "manufacturing": {
    "surface_finish": "ENIG",
    "solder_mask_color": "green",
    "silkscreen_color": "white",
    "min_hole_size": 0.3
  }
}
```

## KiCad 7 PCB Format Notes

When generating PCB files programmatically:
- Format version: `20221018`
- `gr_line` format: `(gr_line (start X Y) (end X Y) (stroke (width W) (type solid)) (layer "Edge.Cuts"))`
- `gr_text` format: `(gr_text "text" (at X Y) (layer "F.SilkS") (effects (font (size W H) (thickness T))))`
- Pad format: `(pad "NUM" smd rect (at X Y) (size W H) (layers "F.Cu" "F.Paste" "F.Mask") (net NUM "NET_NAME") (pinfunction "FUNC") (pintype "TYPE"))`
- Footprint format: `(footprint "LIB:FOOTPRINT" (layer "F.Cu") (at X Y) (property "Reference" "REF") (property "Value" "VALUE"))`

## Gerber Export via Python API

```python
import pcbnew
import os

board = pcbnew.LoadBoard("board.kicad_pcb")
output_dir = "./production"
os.makedirs(output_dir, exist_ok=True)

plot_ctrl = pcbnew.PLOT_CONTROLLER(board)
opts = plot_ctrl.GetPlotOptions()
opts.SetOutputDirectory(output_dir)

layers = [
    (pcbnew.F_Cu, "F.Cu"), (pcbnew.B_Cu, "B.Cu"),
    (pcbnew.F_Mask, "F.Mask"), (pcbnew.B_Mask, "B.Mask"),
    (pcbnew.F_Paste, "F.Paste"), (pcbnew.B_Paste, "B.Paste"),
    (pcbnew.F_SilkS, "F.SilkS"), (pcbnew.B_SilkS, "B.SilkS"),
    (pcbnew.Edge_Cuts, "Edge_Cuts"),
]

for layer_id, layer_name in layers:
    plot_ctrl.SetLayer(layer_id)
    plot_ctrl.OpenPlotfile(f"board-{layer_name}", pcbnew.PLOT_FORMAT_GERBER, layer_name)
    plot_ctrl.PlotLayer()
    plot_ctrl.ClosePlot()
```

## Integration with Existing Workflow

For OpenClaw agents:
1. Use `kicad-cli` for command-line operations
2. Use `pcbnew` Python API for programmatic PCB manipulation
3. Use `eeschema` Python API for schematic manipulation (if available)
4. Store manufacturing files in `production/` directory
5. Archive project as `.kicad_pro` + source files

## Component Libraries

Standard KiCad 7 libraries:
- `Device`: Passive components (R, C, L, D, LED, Crystal)
- `Connector`: Connectors (JST, USB, SMA, PinHeader)
- `Package_DFN_QFN`: IC packages (QFN, DFN, SON)
- `Package_SO`: IC packages (SOIC, TSSOP)
- `Package_TO_SOT_SMD`: Transistors, regulators
- `Crystal`: Crystal oscillators
- `Diode_SMD`: Diodes, TVS
- `LED_SMD`: LEDs
- `Resistor_SMD`: Resistors
- `Capacitor_SMD`: Capacitors
- `Inductor_SMD`: Inductors
- `MountingHole`: Mounting holes
- `TestPoint`: Test points
- `TerminalBlock`: Screw terminals
- `Connector_JST`: JST connectors
- `Connector_Coaxial`: SMA, U.FL connectors
- `Interface_UART`: UART transceivers (ADM2587E, MAX3232)
- `Battery_Management`: Battery chargers, fuel gauges
- `Regulator_Switching`: DC-DC converters
- `Regulator_Linear`: LDO regulators
- `MCU_ST_STM32WL`: STM32WL MCUs with LoRa
- `RF_Module`: LoRa modules
