#!/usr/bin/env python3
"""
Generate KiCad 7 schematic for LoRaWAN Modem LVM-485-SOLAR-01
Hierarchical sheets: Power, MCU+LoRa, RS-485, Memory+Indicators
"""

import uuid
import os

def uid():
    return str(uuid.uuid4())

def sch_header():
    return f"""(kicad_sch
  (version 20230121)
  (generator "eeschema")
  (generator_version "7.0")
  (paper "A3")
  (lib_symbols
    (symbol "power:GND" (power) (pin_names (offset 0.762)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR01" (at 0 -2.54 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "GND" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
      (symbol "GND_0_1"
        (polyline (pts (xy 0 0) (xy 0 -1.27)) (stroke (width 0)) (fill none))
        (polyline (pts (xy -1.27 -1.27) (xy 1.27 -1.27)) (stroke (width 0.254)) (fill none))
        (polyline (pts (xy -0.635 -1.905) (xy 0.635 -1.905)) (stroke (width 0.254)) (fill none))
        (polyline (pts (xy -0.254 -2.54) (xy 0.254 -2.54)) (stroke (width 0.254)) (fill none))
      )
      (symbol "GND_1_1"
        (pin power_in line (at 0 0 270) (length 0) (name "GND" (effects hide)) (number "1" (effects hide)))
      )
    )
    (symbol "power:+3V3" (power) (pin_names (offset 0.762)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR01" (at 0 -2.54 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+3V3" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (symbol "+3V3_0_1"
        (polyline (pts (xy 0 0) (xy 0 1.27)) (stroke (width 0)) (fill none))
        (polyline (pts (xy -0.762 1.27) (xy 0.762 1.27)) (stroke (width 0.254)) (fill none))
      )
      (symbol "+3V3_1_1"
        (pin power_in line (at 0 0 90) (length 0) (name "+3V3" (effects hide)) (number "1" (effects hide)))
      )
    )
    (symbol "power:+BATT" (power) (pin_names (offset 0.762)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR01" (at 0 -2.54 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+BATT" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (symbol "+BATT_0_1"
        (polyline (pts (xy 0 0) (xy 0 1.27)) (stroke (width 0)) (fill none))
        (polyline (pts (xy -0.762 1.27) (xy 0.762 1.27)) (stroke (width 0.254)) (fill none))
      )
      (symbol "+BATT_1_1"
        (pin power_in line (at 0 0 90) (length 0) (name "+BATT" (effects hide)) (number "1" (effects hide)))
      )
    )
    (symbol "power:VCC" (power) (pin_names (offset 0.762)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR01" (at 0 -2.54 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "VCC" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (symbol "VCC_0_1"
        (polyline (pts (xy 0 0) (xy 0 1.27)) (stroke (width 0)) (fill none))
        (polyline (pts (xy -0.762 1.27) (xy 0.762 1.27)) (stroke (width 0.254)) (fill none))
      )
      (symbol "VCC_1_1"
        (pin power_in line (at 0 0 90) (length 0) (name "VCC" (effects hide)) (number "1" (effects hide)))
      )
    )
  )
  (title_block
    (title "LoRaWAN Modem LVM-485-SOLAR-01")
    (company "AgroELEMENT")
    (rev "0.1")
    (date "2026-05-07")
    (source "lorawan-modem.kicad_sch")
  )
"""

def sheet(name, filename, x, y, w=200, h=150):
    return f"""  (sheet
    (at {x} {y})
    (size {w} {h})
    (stroke (width 0.1524) (type solid))
    (fill (color 0 0 0 0.0000))
    (uuid "{uid()}")
    (property "Sheet name" "{name}"
      (at {x} {y - 2} 0)
      (effects (font (size 1.27 1.27) bold) (bottom))
    )
    (property "Sheet file" "{filename}"
      (at {x} {y + h + 2} 0)
      (effects (font (size 1.27 1.27) italic) (top))
    )
  )
"""

def sch_footer():
    return ")\n"

def wire(x1, y1, x2, y2):
    return f"""  (wire
    (pts (xy {x1} {y1}) (xy {x2} {y2}))
    (stroke (width 0) (type default))
    (uuid "{uid()}")
  )"""

def junction(x, y):
    return f"""  (junction
    (at {x} {y} 0)
    (diameter 0)
    (color 0 0 0 0)
    (uuid "{uid()}")
  )"""

def label(name, x, y, angle=0):
    return f"""  (label "{name}"
    (at {x} {y} {angle})
    (effects (font (size 1.27 1.27)) (left))
    (uuid "{uid()}")
  )"""

def power_net(name, x, y):
    return f"""  (symbol
    (lib_id "power:{name}")
    (at {x} {y} 0)
    (unit 1)
    (uuid "{uid()}")
    (property "Reference" "#PWR01"
      (at {x} {y - 2} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{name}"
      (at {x} {y + 2} 0)
      (effects (font (size 1.27 1.27)))
    )
  )"""

def no_connect(x, y):
    return f"""  (no_connect
    (at {x} {y} 0)
    (uuid "{uid()}")
  )"""

def text_note(text, x, y, size=1.27):
    return f"""  (text "{text}"
    (at {x} {y} 0)
    (effects (font (size {size} {size})))
    (uuid "{uid()}")
  )"""

def symbol(lib_id, ref, value, x, y, unit=1, rotation=0, footprint="", datasheet="~", props=None):
    lines = [f'  (symbol']
    lines.append(f'    (lib_id "{lib_id}")')
    lines.append(f'    (at {x} {y} {rotation})')
    lines.append(f'    (unit {unit})')
    lines.append(f'    (uuid "{uid()}")')
    lines.append(f'    (property "Reference" "{ref}"')
    lines.append(f'      (at {x} {y - 5.08} 0)')
    lines.append(f'      (effects (font (size 1.27 1.27)))')
    lines.append(f'    )')
    lines.append(f'    (property "Value" "{value}"')
    lines.append(f'      (at {x} {y + 5.08} 0)')
    lines.append(f'      (effects (font (size 1.27 1.27)))')
    lines.append(f'    )')
    if footprint:
        lines.append(f'    (property "Footprint" "{footprint}"')
        lines.append(f'      (at {x} {y + 7.62} 0)')
        lines.append(f'      (effects (font (size 1.27 1.27) italic) (hide yes))')
        lines.append(f'    )')
    if props:
        for k, v in props.items():
            lines.append(f'    (property "{k}" "{v}"')
            lines.append(f'      (at {x} {y + 10.16} 0)')
            lines.append(f'      (effects (size 1.27 1.27) hide yes)')
            lines.append(f'    )')
    lines.append(f'  )')
    return '\n'.join(lines)

def hierarchical_label(name, x, y, shape="input", side="left"):
    return f"""  (hierarchical_label "{name}"
    (at {x} {y} 0)
    (effects (font (size 1.27 1.27}) ({side}))
    (uuid "{uid()}")
  )"""

def sheet_pin(name, x, y, side="left", shape="input"):
    return f"""  (sheetpin "{name}"
    (at {x} {y} 0)
    (effects (font (size 1.27 1.27}) ({side}))
    (uuid "{uid()}")
  )"""

# === MAIN SCHEMATIC ===
main_sch = sch_header()

# Hierarchical sheets
main_sch += sheet("Power Supply", "power_supply.kicad_sch", 50, 80, 200, 150)
main_sch += sheet("MCU + LoRa", "mcu_lora.kicad_sch", 300, 80, 200, 150)
main_sch += sheet("RS-485", "rs485.kicad_sch", 50, 280, 200, 150)
main_sch += sheet("Memory + Indicators", "memory_ind.kicad_sch", 300, 280, 200, 150)

# Inter-sheet connections (hierarchical labels on main sheet)
# Power -> MCU connections
main_sch += hierarchical_label("+3V3", 260, 100, "right")
main_sch += hierarchical_label("GND", 260, 120, "right")
main_sch += hierarchical_label("+BATT", 260, 140, "right")

# MCU -> RS485 connections
main_sch += hierarchical_label("UART1_TX", 150, 250, "down")
main_sch += hierarchical_label("UART1_RX", 170, 250, "down")
main_sch += hierarchical_label("RS485_DE", 190, 250, "down")

# MCU -> Memory connections
main_sch += hierarchical_label("SPI1_SCK", 310, 250, "down")
main_sch += hierarchical_label("SPI1_MOSI", 330, 250, "down")
main_sch += hierarchical_label("SPI1_MISO", 350, 250, "down")
main_sch += hierarchical_label("SPI1_CS_FLASH", 370, 250, "down")

# Power label
main_sch += text_note("LoRaWAN Modem LVM-485-SOLAR-01", 400, 30, 2.0)
main_sch += text_note("Main Sheet", 400, 40, 1.27)

main_sch += sch_footer()

with open("lorawan-modem.kicad_sch", "w") as f:
    f.write(main_sch)

print("Main schematic created")

# === SHEET 1: POWER SUPPLY ===
power_sch = sch_header()
power_sch += text_note("POWER SUPPLY", 100, 20, 2.0)
power_sch += text_note("Solar Input + Charge Controller + DC-DC + LDO", 100, 30, 1.27)

# Solar input connector
power_sch += symbol("Connector:Conn_01x02_Male", "J1", "SOLAR_IN", 30, 60,
    footprint="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical")
power_sch += text_note("Solar Panel\n6-18V / 5-20W", 30, 45, 0.8)

# TVS protection
power_sch += symbol("Device:D_TVS", "D1", "SMBJ18A", 60, 60,
    footprint="Diode_SMD:D_SMB")

# Schottky diode
power_sch += symbol("Device:D_Schottky", "D2", "SS34", 90, 60,
    footprint="Diode_SMD:D_SMA")

# Input caps
power_sch += symbol("Device:C", "C1", "100uF/25V", 120, 50,
    footprint="Capacitor_SMD:C_1210_3225Metric")
power_sch += symbol("Device:C", "C2", "100nF", 120, 70,
    footprint="Capacitor_SMD:C_0603_1608Metric")

# Charge controller BQ24650
power_sch += symbol("Battery_Management:BQ24650RGER", "U1", "BQ24650RGER", 80, 110,
    footprint="Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm")

# Charge controller passives
power_sch += symbol("Device:R", "R1", "100k", 40, 90, footprint="Resistor_SMD:R_0603_1608Metric")
power_sch += symbol("Device:R", "R2", "49.9k", 40, 110, footprint="Resistor_SMD:R_0603_1608Metric")
power_sch += symbol("Device:R", "R3", "10k", 40, 130, footprint="Resistor_SMD:R_0603_1608Metric")
power_sch += symbol("Device:R", "R8", "0.05", 130, 90, footprint="Resistor_SMD:R_0805_2012Metric")
power_sch += symbol("Device:C", "C7", "10nF", 40, 150, footprint="Capacitor_SMD:C_0603_1608Metric")
power_sch += symbol("Device:C", "C8", "1uF", 130, 110, footprint="Capacitor_SMD:C_0603_1608Metric")
power_sch += symbol("Device:C", "C9", "10uF", 130, 130, footprint="Capacitor_SMD:C_0805_2012Metric")
power_sch += symbol("Device:L", "L1", "10uH/3A", 160, 110, footprint="Inductor_SMD:L_7.3x7.3_H3.5")

# Battery connector
power_sch += symbol("Connector:Conn_01x02_Male", "J2", "BATTERY", 170, 60,
    footprint="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical")
power_sch += text_note("LiFePO4\n2S", 170, 45, 0.8)

# Battery sense
power_sch += symbol("Device:R", "R4", "100k", 150, 80, footprint="Resistor_SMD:R_0603_1608Metric")
power_sch += symbol("Device:R", "R5", "49.9k", 150, 100, footprint="Resistor_SMD:R_0603_1608Metric")
power_sch += symbol("Device:C", "C10", "100nF", 150, 120, footprint="Capacitor_SMD:C_0603_1608Metric")

# DC-DC TPS62840
power_sch += symbol("Regulator_Switching:TPS62840DLAR", "U2", "TPS62840DLAR", 230, 80,
    footprint="Package_SON:Texas_R-PDSO-N8")
power_sch += text_note("Iq=700nA\n3.3V/300mA", 230, 65, 0.8)

# DC-DC passives
power_sch += symbol("Device:L", "L2", "2.2uH", 270, 70, footprint="Inductor_SMD:L_2.0x1.6")
power_sch += symbol("Device:C", "C3", "22uF", 270, 90, footprint="Capacitor_SMD:C_0805_2012Metric")
power_sch += symbol("Device:C", "C4", "100nF", 270, 110, footprint="Capacitor_SMD:C_0603_1608Metric")
power_sch += symbol("Device:R", "R6", "1M", 250, 50, footprint="Resistor_SMD:R_0603_1608Metric")
power_sch += symbol("Device:R", "R7", "332k", 270, 50, footprint="Resistor_SMD:R_0603_1608Metric")

# LDO TPS7A02
power_sch += symbol("Regulator_Linear:TPS7A0233PDBVR", "U3", "TPS7A0233PDBVR", 330, 80,
    footprint="Package_TO_SOT_SMD:SOT-23-5")
power_sch += text_note("Iq=25nA\n3.3V/200mA\nRF Clean", 330, 65, 0.8)

# LDO caps
power_sch += symbol("Device:C", "C5", "1uF", 360, 70, footprint="Capacitor_SMD:C_0603_1608Metric")
power_sch += symbol("Device:C", "C6", "100nF", 360, 90, footprint="Capacitor_SMD:C_0603_1608Metric")

# Power nets
power_sch += power_net("GND", 30, 180)
power_sch += power_net("+BATT", 170, 150)
power_sch += power_net("+3V3", 270, 150)
power_sch += power_net("VCC", 90, 180)

# Sheet pins (hierarchical)
power_sch += sheet_pin("+3V3", 400, 80, "right", "output")
power_sch += sheet_pin("GND", 400, 100, "right", "output")
power_sch += sheet_pin("+BATT", 400, 120, "right", "output")
power_sch += sheet_pin("VBAT_ADC", 400, 140, "right", "output")
power_sch += sheet_pin("CHG_STAT", 400, 160, "right", "output")
power_sch += sheet_pin("I2C1_SCL", 400, 180, "right", "bidir")
power_sch += sheet_pin("I2C1_SDA", 400, 200, "right", "bidir")

# Wires
power_sch += wire(30, 60, 60, 60)
power_sch += wire(60, 60, 90, 60)
power_sch += wire(90, 60, 120, 60)
power_sch += wire(120, 60, 120, 50)
power_sch += wire(120, 60, 120, 70)
power_sch += wire(120, 60, 140, 60)
power_sch += wire(140, 60, 140, 110)
power_sch += wire(140, 110, 80, 110)
power_sch += wire(170, 60, 170, 80)
power_sch += wire(170, 80, 150, 80)
power_sch += wire(170, 80, 170, 150)
power_sch += wire(230, 80, 270, 80)
power_sch += wire(270, 80, 270, 70)
power_sch += wire(270, 80, 270, 90)
power_sch += wire(270, 80, 300, 80)
power_sch += wire(300, 80, 330, 80)
power_sch += wire(330, 80, 360, 80)
power_sch += wire(360, 80, 360, 70)
power_sch += wire(360, 80, 360, 90)

power_sch += sch_footer()

with open("power_supply.kicad_sch", "w") as f:
    f.write(power_sch)

print("Power supply sheet created")

# === SHEET 2: MCU + LoRa ===
mcu_sch = sch_header()
mcu_sch += text_note("MCU + LoRa", 100, 20, 2.0)
mcu_sch += text_note("STM32WL55JCI6 — MCU + LoRa Transceiver", 100, 30, 1.27)

# MCU
mcu_sch += symbol("RF_Module:STM32WL55JCI6", "U4", "STM32WL55JCI6", 100, 100,
    footprint="Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.6x5.6mm")

# Decoupling caps
mcu_sch += symbol("Device:C", "C11", "100nF", 50, 70, footprint="Capacitor_SMD:C_0603_1608Metric")
mcu_sch += symbol("Device:C", "C12", "100nF", 150, 70, footprint="Capacitor_SMD:C_0603_1608Metric")
mcu_sch += symbol("Device:C", "C13", "100nF", 50, 130, footprint="Capacitor_SMD:C_0603_1608Metric")
mcu_sch += symbol("Device:C", "C14", "1uF", 150, 130, footprint="Capacitor_SMD:C_0603_1608Metric")
mcu_sch += symbol("Device:C", "C15", "1uF", 170, 130, footprint="Capacitor_SMD:C_0603_1608Metric")

# HSE Crystal
mcu_sch += symbol("Device:Crystal_GND24", "Y1", "32MHz", 40, 100,
    footprint="Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm")
mcu_sch += symbol("Device:C", "C18", "10pF", 20, 85, footprint="Capacitor_SMD:C_0402_1005Metric")
mcu_sch += symbol("Device:C", "C19", "10pF", 20, 115, footprint="Capacitor_SMD:C_0402_1005Metric")

# LSE Crystal
mcu_sch += symbol("Device:Crystal", "Y2", "32.768kHz", 170, 100,
    footprint="Crystal:Crystal_SMD_3215-2Pin_3.2x1.5mm")
mcu_sch += symbol("Device:C", "C20", "6pF", 190, 90, footprint="Capacitor_SMD:C_0402_1005Metric")
mcu_sch += symbol("Device:C", "C21", "6pF", 190, 110, footprint="Capacitor_SMD:C_0402_1005Metric")

# RF matching
mcu_sch += symbol("Device:C", "C16", "1pF", 30, 160, footprint="Capacitor_SMD:C_0402_1005Metric")
mcu_sch += symbol("Device:L", "L3", "3.9nH", 50, 160, footprint="Inductor_SMD:L_0402_1005Metric")
mcu_sch += symbol("Device:C", "C17", "1.5pF", 70, 160, footprint="Capacitor_SMD:C_0402_1005Metric")
mcu_sch += symbol("Device:D_TVS", "D3", "PESD5V0S1BA", 20, 160, footprint="Diode_SMD:D_SOD-523")

# Antenna connector
mcu_sch += symbol("Connector:Coaxial_SMA", "J4", "SMA_ANT", 10, 170,
    footprint="Connector_Coaxial:SMA_Amphenol_132255_16_Horizontal")

# Power nets
mcu_sch += power_net("GND", 100, 200)
mcu_sch += power_net("+3V3", 50, 50)
mcu_sch += power_net("VCC", 150, 50)

# Sheet pins
mcu_sch += sheet_pin("+3V3", 250, 60, "right", "input")
mcu_sch += sheet_pin("GND", 250, 80, "right", "input")
mcu_sch += sheet_pin("SPI1_SCK", 250, 100, "right", "output")
mcu_sch += sheet_pin("SPI1_MOSI", 250, 120, "right", "output")
mcu_sch += sheet_pin("SPI1_MISO", 250, 140, "right", "input")
mcu_sch += sheet_pin("SPI1_CS_FLASH", 250, 160, "right", "output")
mcu_sch += sheet_pin("UART1_TX", 250, 180, "right", "output")
mcu_sch += sheet_pin("UART1_RX", 250, 200, "right", "input")
mcu_sch += sheet_pin("RS485_DE", 250, 220, "right", "output")
mcu_sch += sheet_pin("I2C1_SCL", 250, 240, "right", "bidir")
mcu_sch += sheet_pin("I2C1_SDA", 250, 260, "right", "bidir")
mcu_sch += sheet_pin("LED_PWR", -10, 60, "left", "output")
mcu_sch += sheet_pin("LED_LORA", -10, 80, "left", "output")
mcu_sch += sheet_pin("LED_RS485", -10, 100, "left", "output")
mcu_sch += sheet_pin("LED_ERR", -10, 120, "left", "output")
mcu_sch += sheet_pin("VBAT_ADC", -10, 140, "left", "input")
mcu_sch += sheet_pin("CHG_STAT", -10, 160, "left", "input")
mcu_sch += sheet_pin("SWDIO", -10, 180, "left", "bidir")
mcu_sch += sheet_pin("SWCLK", -10, 200, "left", "input")
mcu_sch += sheet_pin("NRST", -10, 220, "left", "input")

mcu_sch += sch_footer()

with open("mcu_lora.kicad_sch", "w") as f:
    f.write(mcu_sch)

print("MCU + LoRa sheet created")

# === SHEET 3: RS-485 ===
rs485_sch = sch_header()
rs485_sch += text_note("RS-485 Interface", 100, 20, 2.0)
rs485_sch += text_note("ADM2587EBRWZ — Isolated RS-485 Transceiver", 100, 30, 1.27)

# RS-485 transceiver
rs485_sch += symbol("Interface_UART:ADM2587EBRWZ", "U5", "ADM2587EBRWZ", 100, 100,
    footprint="Package_SO:SOIC-20W_7.5x12.8mm_P1.27mm")

# Decoupling
rs485_sch += symbol("Device:C", "C22", "100nF", 50, 70, footprint="Capacitor_SMD:C_0603_1608Metric")
rs485_sch += symbol("Device:C", "C23", "100nF", 150, 70, footprint="Capacitor_SMD:C_0603_1608Metric")
rs485_sch += symbol("Device:C", "C24", "10uF", 150, 90, footprint="Capacitor_SMD:C_0805_2012Metric")

# TVS protection
rs485_sch += symbol("Device:D_TVS", "D4", "SM712", 60, 150, footprint="Diode_SMD:D_SOT-23")
rs485_sch += symbol("Device:D_TVS", "D5", "SM712", 90, 150, footprint="Diode_SMD:D_SOT-23")

# Termination
rs485_sch += symbol("Device:R", "R9", "120", 120, 150, footprint="Resistor_SMD:R_0603_1608Metric")

# Bias resistors
rs485_sch += symbol("Device:R", "R10", "560", 50, 170, footprint="Resistor_SMD:R_0603_1608Metric")
rs485_sch += symbol("Device:R", "R11", "560", 80, 170, footprint="Resistor_SMD:R_0603_1608Metric")

# Connector
rs485_sch += symbol("Connector:Screw_Terminal_01x03", "J5", "RS-485", 160, 130,
    footprint="TerminalBlock:TerminalBlock_Altech_AK300-3_P5.00mm")
rs485_sch += text_note("A / B / GND", 160, 115, 0.8)

# Power nets
rs485_sch += power_net("GND", 100, 200)
rs485_sch += power_net("+3V3", 50, 50)

# Sheet pins
rs485_sch += sheet_pin("UART1_TX", -10, 60, "left", "input")
rs485_sch += sheet_pin("UART1_RX", -10, 80, "left", "output")
rs485_sch += sheet_pin("RS485_DE", -10, 100, "left", "input")
rs485_sch += sheet_pin("+3V3", -10, 120, "left", "input")
rs485_sch += sheet_pin("GND", -10, 140, "left", "input")

rs485_sch += sch_footer()

with open("rs485.kicad_sch", "w") as f:
    f.write(rs485_sch)

print("RS-485 sheet created")

# === SHEET 4: MEMORY + INDICATORS ===
mem_sch = sch_header()
mem_sch += text_note("Memory + Indicators + Service", 100, 20, 2.0)

# Flash memory
mem_sch += symbol("Memory_Flash:W25Q64JVSSIQ", "U6", "W25Q64JVSSIQ", 60, 60,
    footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm")
mem_sch += symbol("Device:C", "C25", "100nF", 30, 40, footprint="Capacitor_SMD:C_0603_1608Metric")

# Fuel gauge
mem_sch += symbol("Battery_Management:MAX17048G+T", "U7", "MAX17048G+T", 150, 60,
    footprint="Package_SON:Texas_R-PDSO-N8")
mem_sch += symbol("Device:C", "C26", "100nF", 180, 50, footprint="Capacitor_SMD:C_0603_1608Metric")

# LEDs
led_positions = [(30, 120), (60, 120), (90, 120), (120, 120)]
led_refs = ["D6", "D7", "D8", "D9"]
led_values = ["Green", "Blue", "Yellow", "Red"]
led_colors_text = ["PWR", "LORA", "RS485", "ERR"]

for i, (pos, ref, val, txt) in enumerate(zip(led_positions, led_refs, led_values, led_colors_text)):
    mem_sch += symbol("Device:LED", ref, val, pos[0], pos[1], footprint="LED_SMD:LED_0603_1608Metric")
    mem_sch += symbol("Device:R", f"R{12+i}", "1k", pos[0], pos[1] - 15, footprint="Resistor_SMD:R_0603_1608Metric")
    mem_sch += text_note(txt, pos[0], pos[1] + 10, 0.7)

# SWD connector
mem_sch += symbol("Connector:Conn_01x05_Male", "J6", "SWD", 30, 170,
    footprint="Connector_PinHeader_1.27mm:PinHeader_1x05_P1.27mm_Vertical")
mem_sch += text_note("VCC SWDIO GND SWCLK NRST", 30, 185, 0.7)

# UART connector
mem_sch += symbol("Connector:Conn_01x04_Male", "J7", "UART", 100, 170,
    footprint="Connector_PinHeader_1.27mm:PinHeader_1x04_P1.27mm_Vertical")
mem_sch += text_note("VCC TX RX GND", 100, 185, 0.7)

# Test points
tp_positions = [(140, 160), (155, 160), (170, 160), (140, 175), (155, 175)]
tp_refs = ["TP1", "TP2", "TP3", "TP4", "TP5"]
tp_values = ["VBAT", "3V3", "GND", "SWDIO", "SWCLK"]

for pos, ref, val in zip(tp_positions, tp_refs, tp_values):
    mem_sch += symbol("TestPoint:TestPoint_Pad_D1.0mm", ref, val, pos[0], pos[1],
        footprint="TestPoint:TestPoint_Pad_D1.0mm")

# Power nets
mem_sch += power_net("GND", 100, 200)
mem_sch += power_net("+3V3", 50, 30)

# Sheet pins
mem_sch += sheet_pin("SPI1_SCK", -10, 40, "left", "input")
mem_sch += sheet_pin("SPI1_MOSI", -10, 55, "left", "input")
mem_sch += sheet_pin("SPI1_MISO", -10, 70, "left", "output")
mem_sch += sheet_pin("SPI1_CS_FLASH", -10, 85, "left", "input")
mem_sch += sheet_pin("I2C1_SCL", -10, 100, "left", "bidir")
mem_sch += sheet_pin("I2C1_SDA", -10, 115, "left", "bidir")
mem_sch += sheet_pin("+3V3", -10, 130, "left", "input")
mem_sch += sheet_pin("GND", -10, 145, "left", "input")
mem_sch += sheet_pin("+BATT", -10, 160, "left", "input")
mem_sch += sheet_pin("LED_PWR", 200, 40, "right", "input")
mem_sch += sheet_pin("LED_LORA", 200, 55, "right", "input")
mem_sch += sheet_pin("LED_RS485", 200, 70, "right", "input")
mem_sch += sheet_pin("LED_ERR", 200, 85, "right", "input")
mem_sch += sheet_pin("SWDIO", 200, 100, "right", "bidir")
mem_sch += sheet_pin("SWCLK", 200, 115, "right", "input")
mem_sch += sheet_pin("NRST", 200, 130, "right", "input")
mem_sch += sheet_pin("UART1_TX", 200, 145, "right", "bidir")
mem_sch += sheet_pin("UART1_RX", 200, 160, "right", "bidir")

mem_sch += sch_footer()

with open("memory_ind.kicad_sch", "w") as f:
    f.write(mem_sch)

print("Memory + Indicators sheet created")
print("\nAll schematic files generated:")
print("  lorawan-modem.kicad_sch (main)")
print("  power_supply.kicad_sch")
print("  mcu_lora.kicad_sch")
print("  rs485.kicad_sch")
print("  memory_ind.kicad_sch")
