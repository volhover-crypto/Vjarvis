#!/usr/bin/env python3
"""
Generate KiCad 7 schematic for LoRaWAN Modem LVM-485-SOLAR-01
Sheet 1: Power Supply and Battery Management
"""

import uuid
import os

def make_uuid():
    return str(uuid.uuid4())

def ki_time():
    from datetime import datetime
    return int(datetime.now().timestamp())

def symbol(ref, lib_id, x, y, unit=1, props=None, pins=None):
    """Create a symbol instance for KiCad 7 schematic format"""
    uid = make_uuid()
    lines = []
    
    # Symbol instance header
    lines.append(f'  (symbol')
    lines.append(f'    (lib_id "{lib_id}")')
    lines.append(f'    (at {x} {y} 0)')
    lines.append(f'    (unit {unit})')
    lines.append(f'    (uuid "{uid}")')
    
    # Reference and value
    if props:
        for key, val in props.items():
            escaped = str(val).replace('"', '\\"')
            if key == 'Reference':
                lines.append(f'    (property "Reference" "{escaped}"')
                lines.append(f'      (at {x} {y - 1.27:.1f} 0)')
                lines.append(f'      (effects (font (size 1.27 1.27)) (bottom))')
                lines.append(f'    )')
            elif key == 'Value':
                lines.append(f'    (property "Value" "{escaped}"')
                lines.append(f'      (at {x} {y + 2.54:.1f} 0)')
                lines.append(f'      (effects (font (size 1.27 1.27)) (top))')
                lines.append(f'    )')
            elif key == 'Footprint':
                lines.append(f'    (property "Footprint" "{escaped}"')
                lines.append(f'      (at {x} {y + 5.08:.1f} 0)')
                lines.append(f'      (effects (font (size 1.27 1.27) italic) (hide yes))')
                lines.append(f'    )')
            elif key == 'Datasheet':
                lines.append(f'    (property "Datasheet" "{escaped}"')
                lines.append(f'      (at {x} {y + 7.62:.1f} 0)')
                lines.append(f'      (effects (font (size 1.27 1.27) italic) (hide yes))')
                lines.append(f'    )')
            else:
                lines.append(f'    (property "{key}" "{escaped}"')
                lines.append(f'      (at {x} {y + 7.62:.1f} 0)')
                lines.append(f'      (effects (size 1.27 1.27) hide yes)')
                lines.append(f'    )')
    
    lines.append(f'  )')
    return '\n'.join(lines)

def wire(x1, y1, x2, y2):
    uid = make_uuid()
    return f'''  (wire
    (pts (xy {x1} {y1}) (xy {x2} {y2}))
    (stroke (width 0) (type default))
    (uuid "{uid}")
  )'''

def junction(x, y):
    uid = make_uuid()
    return f'''  (junction
    (at {x} {y} 0)
    (diameter 0)
    (color 0 0 0 0)
    (uuid "{uid}")
  )'''

def label_net(name, x, y):
    uid = make_uuid()
    escaped = name.replace('"', '\\"')
    return f'''  (label "{escaped}"
    (at {x} {y} 0)
    (effects (font (size 1.27 1.27)) (left))
    (uuid "{uid}")
  )'''

def power_net(name, x, y):
    uid = make_uuid()
    return f'''  (symbol
    (lib_id "power:{name}")
    (at {x} {y} 0)
    (unit 1)
    (uuid "{uid}")
    (property "Reference" "#PWR01"
      (at {x} {y - 2} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{name}"
      (at {x} {y + 2} 0)
      (effects (font (size 1.27 1.27)))
    )
  )'''

def no_connect(x, y):
    uid = make_uuid()
    return f'''  (no_connect
    (at {x} {y} 0)
    (uuid "{uid}")
  )'''

def hsheet(name, filename, x, y, w=100, h=30):
    """Hierarchical sheet"""
    uid = make_uuid()
    return f'''  (sheet
    (at {x} {y})
    (size {w} {h})
    (stroke (width 0.1524) (type solid))
    (fill (color 0 0 0 0.0000))
    (uuid "{uid}")
    (property "Sheet name" "{name}"
      (at {x} {y - 1.5} 0)
      (effects (font (size 1.27 1.27) bold) (bottom))
    )
    (property "Sheet file" "{filename}"
      (at {x} {y + {h} + 1.5} 0)
      (effects (font (size 1.27 1.27) italic) (top))
    )
  )'''

def text_note(text, x, y, size=1.27):
    uid = make_uuid()
    escaped = text.replace('"', '\\"')
    return f'''  (text "{escaped}"
    (at {x} {y} 0)
    (effects (font (size {size} {size})))
    (uuid "{uid}")
  )'''

# === BUILD SCHEMATIC ===

T = ki_time()
output = []

# Header
output.append(f'''(kicad_sch
  (version 20230121)
  (generator "eeschema")
  (generator_version "7.0")
  (paper "A4")
  (lib_symbols
    (symbol "power:GND" (power) (pin_names (offset 0.762)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR01" (at 0 -2.54 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "GND" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
      (symbol "GND_0_1" (polyline (pts (xy 0 0) (xy 0 -1.27)) (stroke (width 0)) (fill none))
        (polyline (pts (xy -1.27 -1.27) (xy 1.27 -1.27)) (stroke (width 0.254)) (fill none))
        (polyline (pts (xy -0.635 -1.905) (xy 0.635 -1.905)) (stroke (width 0.254)) (fill none))
        (polyline (pts (xy -0.254 -2.54) (xy 0.254 -2.54)) (stroke (width 0.254)) (fill none))
      )
      (symbol "GND_1_1" (pin power_in line (at 0 0 270) (length 0) (name "GND" (effects hide)) (number "1" (effects hide))))
    )
    (symbol "power:+3V3" (power) (pin_names (offset 0.762)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR01" (at 0 -2.54 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+3V3" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (symbol "+3V3_0_1" (polyline (pts (xy 0 0) (xy 0 1.27)) (stroke (width 0)) (fill none))
        (polyline (pts (xy -0.762 1.27) (xy 0.762 1.27)) (stroke (width 0.254)) (fill none))
      )
      (symbol "+3V3_1_1" (pin power_in line (at 0 0 90) (length 0) (name "+3V3" (effects hide)) (number "1" (effects hide))))
    )
    (symbol "power:+BATT" (power) (pin_names (offset 0.762)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR01" (at 0 -2.54 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+BATT" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (symbol "+BATT_0_1" (polyline (pts (xy 0 0) (xy 0 1.27)) (stroke (width 0)) (fill none))
        (polyline (pts (xy -0.762 1.27) (xy 0.762 1.27)) (stroke (width 0.254)) (fill none))
      )
      (symbol "+BATT_1_1" (pin power_in line (at 0 0 90) (length 0) (name "+BATT" (effects hide)) (number "1" (effects hide))))
    )
  )
''')

# Sheet title block
output.append(f'''  (title_block
    (title "LoRaWAN Modem LVM-485-SOLAR-01")
    (company "AgroELEMENT")
    (rev "0.1")
    (date "2026-05-07")
    (source "lorawan-modem.kicad_sch")
  )
''')

# === POWER SUPPLY SECTION (left side, top) ===
# Solar input connector
output.append(text_note("SOLAR PANEL INPUT", 50, 30, 2.0))
output.append(text_note("5-20W, 6-18V", 50, 35, 1.27))

# Solar input protection
output.append(symbol("J1", "Connector:Conn_01x02_Male", 50, 50, props={
    "Reference": "J1", "Value": "SOLAR_IN",
    "Footprint": "Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical",
    "Datasheet": "~"
}))

# TVS diode for solar input
output.append(symbol("D1", "Device:D_TVS", 80, 50, props={
    "Reference": "D1", "Value": "SMBJ18A",
    "Footprint": "Diode_SMD:D_SMB",
    "Datasheet": "https://www.littelfuse.com/~/media/electronics/datasheets/tvs_diodes/littelfuse_tvs_diode_smbj_datasheet.pdf"
}))

# Schottky diode for reverse polarity protection
output.append(symbol("D2", "Device:D_Schottky", 100, 50, props={
    "Reference": "D2", "Value": "SS34",
    "Footprint": "Diode_SMD:D_SMA",
    "Datasheet": "~"
}))

# Input capacitor
output.append(symbol("C1", "Device:C", 120, 50, props={
    "Reference": "C1", "Value": "100uF/25V",
    "Footprint": "Capacitor_SMD:C_1210_3225Metric",
    "Datasheet": "~"
}))

output.append(symbol("C2", "Device:C", 135, 50, props={
    "Reference": "C2", "Value": "100nF",
    "Footprint": "Capacitor_SMD:C_0603_1608Metric",
    "Datasheet": "~"
}))

# === CHARGE CONTROLLER (center) ===
output.append(text_note("CHARGE CONTROLLER", 180, 30, 2.0))

# BQ24650 - MPPT charge controller for LiFePO4
output.append(symbol("U1", "Battery_Management:BQ24650RGER", 200, 70, props={
    "Reference": "U1", "Value": "BQ24650RGER",
    "Footprint": "Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm",
    "Datasheet": "https://www.ti.com/lit/ds/symlink/bq24650.pdf"
}))

# Charge controller passive components
output.append(symbol("R1", "Device:R", 170, 55, props={
    "Reference": "R1", "Value": "100k",
    "Footprint": "Resistor_SMD:R_0603_1608Metric",
    "Datasheet": "~"
}))
output.append(symbol("R2", "Device:R", 170, 65, props={
    "Reference": "R2", "Value": "49.9k",
    "Footprint": "Resistor_SMD:R_0603_1608Metric",
    "Datasheet": "~"
}))
output.append(symbol("R3", "Device:R", 170, 75, props={
    "Reference": "R3", "Value": "10k",
    "Footprint": "Resistor_SMD:R_0603_1608Metric",
    "Datasheet": "~"
}))

# Inductor for charge controller
output.append(symbol("L1", "Device:L", 240, 55, props={
    "Reference": "L1", "Value": "10uH/3A",
    "Footprint": "Inductor_SMD:L_7.3x7.3_H3.5",
    "Datasheet": "~"
}))

# Battery connection
output.append(symbol("J2", "Connector:Conn_01x02_Male", 280, 50, props={
    "Reference": "J2", "Value": "BATTERY",
    "Footprint": "Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical",
    "Datasheet": "~"
}))

# Battery voltage divider for monitoring
output.append(symbol("R4", "Device:R", 260, 70, props={
    "Reference": "R4", "Value": "100k",
    "Footprint": "Resistor_SMD:R_0603_1608Metric",
    "Datasheet": "~"
}))
output.append(symbol("R5", "Device:R", 260, 80, props={
    "Reference": "R5", "Value": "49.9k",
    "Footprint": "Resistor_SMD:R_0603_1608Metric",
    "Datasheet": "~"
}))

# === DC-DC CONVERTER (right side) ===
output.append(text_note("DC-DC CONVERTER", 350, 30, 2.0))

# TPS62840 - ultra-low Iq buck converter (700nA quiescent)
output.append(symbol("U2", "Regulator_Switching:TPS62840DLAR", 350, 60, props={
    "Reference": "U2", "Value": "TPS62840DLAR",
    "Footprint": "Package_SON:Texas_R-PDSO-N8",
    "Datasheet": "https://www.ti.com/lit/ds/symlink/tps62840.pdf"
}))

# Output inductor and caps
output.append(symbol("L2", "Device:L", 390, 50, props={
    "Reference": "L2", "Value": "2.2uH",
    "Footprint": "Inductor_SMD:L_2.0x1.6",
    "Datasheet": "~"
}))
output.append(symbol("C3", "Device:C", 400, 65, props={
    "Reference": "C3", "Value": "22uF",
    "Footprint": "Capacitor_SMD:C_0805_2012Metric",
    "Datasheet": "~"
}))
output.append(symbol("C4", "Device:C", 410, 65, props={
    "Reference": "C4", "Value": "100nF",
    "Footprint": "Capacitor_SMD:C_0603_1608Metric",
    "Datasheet": "~"
}))

# Feedback resistors for 3.3V output
output.append(symbol("R6", "Device:R", 380, 80, props={
    "Reference": "R6", "Value": "1M",
    "Footprint": "Resistor_SMD:R_0603_1608Metric",
    "Datasheet": "~"
}))
output.append(symbol("R7", "Device:R", 380, 90, props={
    "Reference": "R7", "Value": "332k",
    "Footprint": "Resistor_SMD:R_0603_1608Metric",
    "Datasheet": "~"
}))

# === LDO for analog/RF (optional, low noise) ===
output.append(text_note("LDO (RF)", 450, 30, 1.5))

output.append(symbol("U3", "Regulator_Linear:TPS7A0233PDBV", 450, 60, props={
    "Reference": "U3", "Value": "TPS7A0233PDBVR",
    "Footprint": "Package_TO_SOT_SMD:SOT-23-5",
    "Datasheet": "https://www.ti.com/lit/ds/symlink/tps7a02.pdf"
}))

output.append(symbol("C5", "Device:C", 480, 55, props={
    "Reference": "C5", "Value": "1uF",
    "Footprint": "Capacitor_SMD:C_0603_1608Metric",
    "Datasheet": "~"
}))
output.append(symbol("C6", "Device:C", 490, 55, props={
    "Reference": "C6", "Value": "100nF",
    "Footprint": "Capacitor_SMD:C_0603_1608Metric",
    "Datasheet": "~"
}))

# === POWER RAILS ===
output.append(power_net("+BATT", 100, 40))
output.append(power_net("+3V3", 420, 40))
output.append(power_net("GND", 50, 100))

# === WIRES ===
# Solar input to protection
output.append(wire(55, 50, 75, 50))
output.append(wire(85, 50, 95, 50))
output.append(wire(105, 50, 115, 50))

# To charge controller
output.append(wire(125, 50, 170, 50))

# Charge controller to battery
output.append(wire(240, 60, 270, 60))
output.append(wire(270, 60, 270, 55))
output.append(wire(270, 55, 280, 55))

# Battery to DC-DC
output.append(wire(280, 45, 320, 45))
output.append(wire(320, 45, 320, 60))
output.append(wire(320, 60, 340, 60))

# DC-DC output
output.append(wire(380, 60, 400, 60))
output.append(wire(400, 60, 400, 55))

# === NET LABELS ===
output.append(label_net("SOLAR_V", 130, 45))
output.append(label_net("VBAT_SENSE", 260, 75))
output.append(label_net("VSYS", 400, 50))

# === NOTES ===
output.append(text_note("LiFePO4 2S: 5.0-7.4V", 280, 35, 1.0))
output.append(text_note("Iq=700nA, 3.3V/300mA", 350, 100, 1.0))
output.append(text_note("Iq=25nA, 3.3V/200mA", 450, 100, 1.0))

# Close
output.append(")")

# Write schematic
sch_content = "\n".join(output)

with open("/root/.openclaw/workspace/projects/lorawan-modem/kicad/lorawan-modem.kicad_sch", "w") as f:
    f.write(sch_content)

print("Sheet 1 (Power Supply) generated")
print(f"File size: {len(sch_content)} bytes")
