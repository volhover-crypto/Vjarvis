# lorawan-modem-eda - EDA Project

## Project Overview

AI-assisted EDA project using @claude-eda toolkit.

## Project Structure

- `lorawan-modem-eda.kicad_pro`: KiCad project file (in root)
- `lorawan-modem-eda.kicad_sch`: Schematic
- `lorawan-modem-eda.kicad_pcb`: PCB layout
- `docs/`: Design documentation
- `datasheets/`: Component datasheets
- `production/`: Manufacturing outputs

## Component Libraries

Components are stored in the **global EDA-MCP library** at:
- `~/Documents/KiCad/9.0/symbols/EDA-MCP.kicad_sym` - Unified symbol library
- `~/Documents/KiCad/9.0/footprints/EDA-MCP.pretty/` - Footprints
- `~/Documents/KiCad/9.0/3dmodels/EDA-MCP.3dshapes/` - 3D models

This global library is automatically discovered by kicad-mcp.

## EDA Workflow

Use these commands for the EDA workflow:

1. `/eda-new` - Define project requirements
2. `/eda-source [role]` - Source components
3. `/eda-schematic [sheet]` - Create schematic
4. `/eda-layout [phase]` - Layout PCB
5. `/eda-check [scope]` - Validate design
6. `/eda-export [format]` - Export manufacturing files

## IMPORTANT

- Always run `/eda-check full` before `/eda-export`
- Check stock levels before finalizing component selection
