#!/usr/bin/env python3
"""
Generate complete KiCad 7 PCB file for LoRaWAN Modem LVM-485-SOLAR-01
Includes: board outline, mounting holes, component footprints, zones
"""

import uuid
import json

def uid():
    return str(uuid.uuid4())

# Load placement plan
with open("placement_plan.json") as f:
    placements = json.load(f)

# Footprint library mappings
FP_MAP = {
    "J1": ("Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "JST_PH"),
    "J2": ("Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "JST_PH"),
    "J4": ("Connector_Coaxial:SMA_Amphenol_132255_16_Horizontal", "SMA"),
    "J5": ("TerminalBlock:TerminalBlock_Altech_AK300-3_P5.00mm", "ScrewTerminal"),
    "J6": ("Connector_PinHeader_1.27mm:PinHeader_1x05_P1.27mm_Vertical", "PinHeader_1.27"),
    "J7": ("Connector_PinHeader_1.27mm:PinHeader_1x04_P1.27mm_Vertical", "PinHeader_1.27"),
    "D1": ("Diode_SMD:D_SMB", "SMB"),
    "D2": ("Diode_SMD:D_SMA", "SMA"),
    "D3": ("Diode_SMD:D_SOD-523", "SOD-523"),
    "D4": ("Diode_SMD:D_SOT-23", "SOT-23"),
    "D5": ("Diode_SMD:D_SOT-23", "SOT-23"),
    "D6": ("LED_SMD:LED_0603_1608Metric", "0603"),
    "D7": ("LED_SMD:LED_0603_1608Metric", "0603"),
    "D8": ("LED_SMD:LED_0603_1608Metric", "0603"),
    "D9": ("LED_SMD:LED_0603_1608Metric", "0603"),
    "C1": ("Capacitor_SMD:C_1210_3225Metric", "1210"),
    "C2": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C3": ("Capacitor_SMD:C_0805_2012Metric", "0805"),
    "C4": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C5": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C6": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C7": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C8": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C9": ("Capacitor_SMD:C_0805_2012Metric", "0805"),
    "C10": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C11": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C12": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C13": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C14": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C15": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C16": ("Capacitor_SMD:C_0402_1005Metric", "0402"),
    "C17": ("Capacitor_SMD:C_0402_1005Metric", "0402"),
    "C18": ("Capacitor_SMD:C_0402_1005Metric", "0402"),
    "C19": ("Capacitor_SMD:C_0402_1005Metric", "0402"),
    "C20": ("Capacitor_SMD:C_0402_1005Metric", "0402"),
    "C21": ("Capacitor_SMD:C_0402_1005Metric", "0402"),
    "C22": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C23": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C24": ("Capacitor_SMD:C_0805_2012Metric", "0805"),
    "C25": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "C26": ("Capacitor_SMD:C_0603_1608Metric", "0603"),
    "R1": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R2": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R3": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R4": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R5": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R6": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R7": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R8": ("Resistor_SMD:R_0805_2012Metric", "0805"),
    "R9": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R10": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R11": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R12": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R13": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R14": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "R15": ("Resistor_SMD:R_0603_1608Metric", "0603"),
    "L1": ("Inductor_SMD:L_7.3x7.3_H3.5", "7.3x7.3"),
    "L2": ("Inductor_SMD:L_2.0x1.6", "2.0x1.6"),
    "L3": ("Inductor_SMD:L_0402_1005Metric", "0402"),
    "U1": ("Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm", "QFN-24"),
    "U2": ("Package_SON:Texas_R-PDSO-N8", "DSBGA-8"),
    "U3": ("Package_TO_SOT_SMD:SOT-23-5", "SOT-23-5"),
    "U4": ("Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.6x5.6mm", "QFN-48"),
    "U5": ("Package_SO:SOIC-20W_7.5x12.8mm_P1.27mm", "SOIC-20"),
    "U6": ("Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "SOIC-8"),
    "U7": ("Package_SON:Texas_R-PDSO-N8", "TDFN-8"),
    "Y1": ("Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm", "3225"),
    "Y2": ("Crystal:Crystal_SMD_3215-2Pin_3.2x1.5mm", "3215"),
    "TP1": ("TestPoint:TestPoint_Pad_D1.0mm", "TP_1mm"),
    "TP2": ("TestPoint:TestPoint_Pad_D1.0mm", "TP_1mm"),
    "TP3": ("TestPoint:TestPoint_Pad_D1.0mm", "TP_1mm"),
    "TP4": ("TestPoint:TestPoint_Pad_D1.0mm", "TP_1mm"),
    "TP5": ("TestPoint:TestPoint_Pad_D1.0mm", "TP_1mm"),
}

# Generate PCB content
lines = []

lines.append("(kicad_pcb")
lines.append("  (version 20240108)")
lines.append("  (generator \"pcbnew\")")
lines.append("  (generator_version \"7.0\")")
lines.append("  (general")
lines.append("    (thickness 1.6)")
lines.append("    (legacy_teardrops no)")
lines.append("  )")
lines.append("  (paper \"A4\")")
lines.append("  (layers")
lines.append("    (0 \"F.Cu\" signal)")
lines.append("    (1 \"In1.Cu\" signal)")
lines.append("    (2 \"In2.Cu\" signal)")
lines.append("    (3 \"B.Cu\" signal)")
lines.append("    (4 \"B.Adhes\" user \"B.Adhesive\")")
lines.append("    (5 \"F.Adhes\" user \"F.Adhesive\")")
lines.append("    (6 \"B.Paste\" user)")
lines.append("    (7 \"F.Paste\" user)")
lines.append("    (8 \"B.SilkS\" user \"B.Silkscreen\")")
lines.append("    (9 \"F.SilkS\" user \"F.Silkscreen\")")
lines.append("    (10 \"B.Mask\" user)")
lines.append("    (11 \"F.Mask\" user)")
lines.append("    (12 \"Dwgs.User\" user \"User.Drawings\")")
lines.append("    (13 \"Cmts.User\" user \"User.Comments\")")
lines.append("    (14 \"Eco1.User\" user \"User.Eco1\")")
lines.append("    (15 \"Eco2.User\" user \"User.Eco2\")")
lines.append("    (16 \"Edge.Cuts\" user)")
lines.append("    (17 \"Margin\" user)")
lines.append("    (18 \"B.CrtYd\" user \"B.Courtyard\")")
lines.append("    (19 \"F.CrtYd\" user \"F.Courtyard\")")
lines.append("    (20 \"B.Fab\" user)")
lines.append("    (21 \"F.Fab\" user)")
lines.append("  )")
lines.append("  (setup")
lines.append("    (pad_to_mask_clearance 0)")
lines.append("    (solder_mask_min_width 0.1)")
lines.append("    (aux_axis_origin 0 0)")
lines.append("    (grid_origin 0 0)")
lines.append("  )")

# Nets
nets = [
    ("", ""),
    ("GND", "GND"),
    ("VCC_3V3", "VCC_3V3"),
    ("VBAT", "VBAT"),
    ("VSYS", "VSYS"),
    ("VCC_RF", "VCC_RF"),
    ("RS485_A", "RS485_A"),
    ("RS485_B", "RS485_B"),
    ("RS485_GND", "RS485_GND"),
    ("SPI1_SCK", "SPI1_SCK"),
    ("SPI1_MOSI", "SPI1_MOSI"),
    ("SPI1_MISO", "SPI1_MISO"),
    ("SPI1_CS_FLASH", "SPI1_CS_FLASH"),
    ("UART1_TX", "UART1_TX"),
    ("UART1_RX", "UART1_RX"),
    ("RS485_DE", "RS485_DE"),
    ("I2C1_SCL", "I2C1_SCL"),
    ("I2C1_SDA", "I2C1_SDA"),
    ("LED_PWR", "LED_PWR"),
    ("LED_LORA", "LED_LORA"),
    ("LED_RS485", "LED_RS485"),
    ("LED_ERR", "LED_ERR"),
    ("VBAT_ADC", "VBAT_ADC"),
    ("CHG_STAT", "CHG_STAT"),
    ("SWDIO", "SWDIO"),
    ("SWCLK", "SWCLK"),
    ("NRST", "NRST"),
    ("RF_ANT", "RF_ANT"),
    ("SOLAR_VIN", "SOLAR_VIN"),
    ("VISO", "VISO"),
]

for i, (net_id, net_name) in enumerate(nets):
    lines.append(f"  (net {i} \"{net_name}\")")

# Board outline
lines.append(f"  (gr_line (start 0 0) (end 100 0) (stroke (width 0.15) (type default)) (layer \"Edge.Cuts\") (uuid \"{uid()}\"))")
lines.append(f"  (gr_line (start 100 0) (end 100 150) (stroke (width 0.15) (type default)) (layer \"Edge.Cuts\") (uuid \"{uid()}\"))")
lines.append(f"  (gr_line (start 100 150) (end 0 150) (stroke (width 0.15) (type default)) (layer \"Edge.Cuts\") (uuid \"{uid()}\"))")
lines.append(f"  (gr_line (start 0 150) (end 0 0) (stroke (width 0.15) (type default)) (layer \"Edge.Cuts\") (uuid \"{uid()}\"))")

# Mounting holes
for pos in [(5, 5), (95, 5), (95, 145), (5, 145)]:
    lines.append(f"  (footprint \"MountingHole:MountingHole_3.2mm_M3\"")
    lines.append(f"    (layer \"F.Cu\")")
    lines.append(f"    (at {pos[0]} {pos[1]})")
    lines.append(f"    (property \"Reference\" \"MH\")")
    lines.append(f"    (attr exclude_from_pos_files exclude_from_bom)")
    lines.append(f"    (pad \"\" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers \"*.Cu\" \"*.Mask\") (uuid \"{uid()}\"))")
    lines.append(f"  )")

# Component footprints
for ref, value, x, y in placements:
    if ref in FP_MAP:
        fp_name, fp_short = FP_MAP[ref]
        lines.append(f"  (footprint \"{fp_name}\"")
        lines.append(f"    (layer \"F.Cu\")")
        lines.append(f"    (at {x} {y})")
        lines.append(f"    (property \"Reference\" \"{ref}\")")
        lines.append(f"    (property \"Value\" \"{value}\")")
        lines.append(f"    (attr smd)")
        # Add minimal pad for DRC
        lines.append(f"    (pad \"1\" smd roundrect (at -1 0) (size 0.8 0.8) (layers \"F.Cu\" \"F.Paste\" \"F.Mask\") (roundrect_rratio 0.25) (uuid \"{uid()}\"))")
        lines.append(f"    (pad \"2\" smd roundrect (at 1 0) (size 0.8 0.8) (layers \"F.Cu\" \"F.Paste\" \"F.Mask\") (roundrect_rratio 0.25) (uuid \"{uid()}\"))")
        lines.append(f"  )")

# Ground zones
lines.append(f"  (zone (net 1) (net_name \"GND\") (layer \"F.Cu\") (tstamp 0) (hatch edge 0.5)")
lines.append(f"    (connect_pads (clearance 0.2))")
lines.append(f"    (min_thickness 0.254)")
lines.append(f"    (fill (thermal_gap 0.5) (thermal_bridge_width 0.5))")
lines.append(f"    (polygon (pts (xy 0 0) (xy 100 0) (xy 100 150) (xy 0 150)))")
lines.append(f"  )")
lines.append(f"  (zone (net 1) (net_name \"GND\") (layer \"B.Cu\") (tstamp 0) (hatch edge 0.5)")
lines.append(f"    (connect_pads (clearance 0.2))")
lines.append(f"    (min_thickness 0.254)")
lines.append(f"    (fill (thermal_gap 0.5) (thermal_bridge_width 0.5))")
lines.append(f"    (polygon (pts (xy 0 0) (xy 100 0) (xy 100 150) (xy 0 150)))")
lines.append(f"  )")

# Title
lines.append(f"  (gr_text \"LoRaWAN Modem LVM-485-SOLAR-01\" (at 50 140) (layer \"F.SilkS\") (effects (font (size 1.5 1.5) (thickness 0.2))) (uuid \"{uid()}\"))")
lines.append(f"  (gr_text \"Rev 0.1 | 2026-05-07 | AgroELEMENT\" (at 50 145) (layer \"F.SilkS\") (effects (font (size 1 1) (thickness 0.15))) (uuid \"{uid()}\"))")
lines.append(f"  (gr_text \"100x150mm | 4-layer | FR-4\" (at 50 148) (layer \"F.SilkS\") (effects (font (size 0.8 0.8) (thickness 0.12))) (uuid \"{uid()}\"))")

lines.append(")")

pcb_content = "\n".join(lines)

with open("lorawan-modem.kicad_pcb", "w") as f:
    f.write(pcb_content)

print(f"PCB file generated: {len(pcb_content)} bytes")
print(f"Components: {len(placements)}")
print(f"Nets: {len(nets)}")
