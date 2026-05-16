---
name: eda-kicad
description: AI-assisted EDA workflow for KiCad 7. Use for electronic schematics, PCB design, component selection, manufacturing file generation, DRC, Gerber export, and 3D visualization.
---

# EDA Workflow — KiCad 7

Electronic Design Automation workflow for KiCad 7.0+.

## Project Structure

```
project-name/
├── project-name.kicad_pro    # Project file
├── project-name.kicad_sch    # Schematic
├── project-name.kicad_pcb    # PCB layout
├── docs/design-constraints.json
├── datasheets/
├── production/               # Gerber, drill, BOM
└── .mcp.json
```

## Key Commands

```bash
# CLI export
kicad-cli pcb export gerbers <board.kicad_pcb> --output ./production/
kicad-cli pcb export drill <board.kicad_pcb> --output ./production/
kicad-cli sch export python-bom <sch.kicad_sch> --output ./production/bom.csv
```

## Gerber Export (Python API)

```python
import pcbnew
board = pcbnew.LoadBoard("board.kicad_pcb")
plot_ctrl = pcbnew.PLOT_CONTROLLER(board)
opts = plot_ctrl.GetPlotOptions()
opts.SetOutputDirectory("./production")
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

## KiCad 7 PCB Format (S-expression)

- Format version: `20221018`
- gr_line: `(gr_line (start X Y) (end X Y) (stroke (width W) (type solid)) (layer "Edge.Cuts"))`  
- Pad: `(pad "NUM" smd rect (at X Y) (size W H) (layers "F.Cu" "F.Paste" "F.Mask"))`
- Footprint: `(footprint "LIB:FP" (layer "F.Cu") (at X Y) (property "Reference" "REF"))`

## Workflow

1. Init: `npx claude-eda init <name> -y`
2. Source components via JLCPCB MCP
3. Create hierarchical schematic, run ERC
4. Import netlist, place components, route
5. Copper pour, ground planes, DRC
6. Export Gerber + drill + BOM to `production/`

## Key Libraries

- `Device`: R, C, L, D, LED, Crystal
- `Package_DFN_QFN`: QFN, DFN ICs
- `Regulator_Linear`: LDOs
- `MCU_ST_STM32WL`: STM32WL + LoRa
- `Connector_JST`, `Connector_Coaxial`: JST, SMA
- `Battery_Management`: Chargers, fuel gauges
- `Interface_UART`: RS-485 transceivers
