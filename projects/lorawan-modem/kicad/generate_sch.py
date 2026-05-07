"""
Generate LoRaWAN Modem schematic using skidl
"""
import skidl
from skidl import *

# Set KiCad as the default tool
skidl.config.tool = skidl.TOOL_KICAD

# Create parts from KiCad libraries
# Power section
J1 = Part("Connector", "Conn_01x02_Male", footprint="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", dest=TEMPLATE)
J1.ref = "J1"
J1.value = "SOLAR_IN"

D1 = Part("Device", "D_TVS", footprint="Diode_SMD:D_SMB", dest=TEMPLATE)
D1.ref = "D1"
D1.value = "SMBJ18A"

D2 = Part("Device", "D_Schottky", footprint="Diode_SMD:D_SMA", dest=TEMPLATE)
D2.ref = "D2"
D2.value = "SS34"

C1 = Part("Device", "C", footprint="Capacitor_SMD:C_1210_3225Metric", dest=TEMPLATE)
C1.ref = "C1"
C1.value = "100uF/25V"

C2 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C2.ref = "C2"
C2.value = "100nF"

# Charge controller
U1 = Part("Battery_Management", "BQ24650RGER", footprint="Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm", dest=TEMPLATE)
U1.ref = "U1"
U1.value = "BQ24650RGER"

# Charge controller passives
R1 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R1.ref = "R1"
R1.value = "100k"

R2 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R2.ref = "R2"
R2.value = "49.9k"

R3 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R3.ref = "R3"
R3.value = "10k"

R8 = Part("Device", "R", footprint="Resistor_SMD:R_0805_2012Metric", dest=TEMPLATE)
R8.ref = "R8"
R8.value = "0.05"

C7 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C7.ref = "C7"
C7.value = "10nF"

C8 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C8.ref = "C8"
C8.value = "1uF"

C9 = Part("Device", "C", footprint="Capacitor_SMD:C_0805_2012Metric", dest=TEMPLATE)
C9.ref = "C9"
C9.value = "10uF"

L1 = Part("Device", "L", footprint="Inductor_SMD:L_7.3x7.3_H3.5", dest=TEMPLATE)
L1.ref = "L1"
L1.value = "10uH/3A"

# Battery connector
J2 = Part("Connector", "Conn_01x02_Male", footprint="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", dest=TEMPLATE)
J2.ref = "J2"
J2.value = "BATTERY"

# Battery sense
R4 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R4.ref = "R4"
R4.value = "100k"

R5 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R5.ref = "R5"
R5.value = "49.9k"

C10 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C10.ref = "C10"
C10.value = "100nF"

# DC-DC converter
U2 = Part("Regulator_Switching", "TPS62088DLAR", footprint="Package_SON:Texas_R-PDSO-N8", dest=TEMPLATE)
U2.ref = "U2"
U2.value = "TPS62088DLAR"

L2 = Part("Device", "L", footprint="Inductor_SMD:L_2.0x1.6", dest=TEMPLATE)
L2.ref = "L2"
L2.value = "2.2uH"

C3 = Part("Device", "C", footprint="Capacitor_SMD:C_0805_2012Metric", dest=TEMPLATE)
C3.ref = "C3"
C3.value = "22uF"

C4 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C4.ref = "C4"
C4.value = "100nF"

R6 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R6.ref = "R6"
R6.value = "1M"

R7 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R7.ref = "R7"
R7.value = "332k"

# LDO for RF
U3 = Part("Regulator_Linear", "MCP1700-3302E", footprint="Package_TO_SOT_SMD:SOT-23-5", dest=TEMPLATE)
U3.ref = "U3"
U3.value = "MCP1700-3302E"

C5 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C5.ref = "C5"
C5.value = "1uF"

C6 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C6.ref = "C6"
C6.value = "100nF"

# MCU
U4 = Part("MCU_ST_STM32WL", "STM32WL55JCIx", footprint="Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm", dest=TEMPLATE)
U4.ref = "U4"
U4.value = "STM32WL55JCIx"

# MCU decoupling
C11 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C11.ref = "C11"
C11.value = "100nF"

C12 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C12.ref = "C12"
C12.value = "100nF"

C13 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C13.ref = "C13"
C13.value = "100nF"

C14 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C14.ref = "C14"
C14.value = "1uF"

C15 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C15.ref = "C15"
C15.value = "1uF"

# Crystals
Y1 = Part("Device", "Crystal_GND24", footprint="Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm", dest=TEMPLATE)
Y1.ref = "Y1"
Y1.value = "32MHz"

Y2 = Part("Device", "Crystal", footprint="Crystal:Crystal_SMD_3215-2Pin_3.2x1.5mm", dest=TEMPLATE)
Y2.ref = "Y2"
Y2.value = "32.768kHz"

C18 = Part("Device", "C", footprint="Capacitor_SMD:C_0402_1005Metric", dest=TEMPLATE)
C18.ref = "C18"
C18.value = "10pF"

C19 = Part("Device", "C", footprint="Capacitor_SMD:C_0402_1005Metric", dest=TEMPLATE)
C19.ref = "C19"
C19.value = "10pF"

C20 = Part("Device", "C", footprint="Capacitor_SMD:C_0402_1005Metric", dest=TEMPLATE)
C20.ref = "C20"
C20.value = "6pF"

C21 = Part("Device", "C", footprint="Capacitor_SMD:C_0402_1005Metric", dest=TEMPLATE)
C21.ref = "C21"
C21.value = "6pF"

# RF matching
C16 = Part("Device", "C", footprint="Capacitor_SMD:C_0402_1005Metric", dest=TEMPLATE)
C16.ref = "C16"
C16.value = "1pF"

L3 = Part("Device", "L", footprint="Inductor_SMD:L_0402_1005Metric", dest=TEMPLATE)
L3.ref = "L3"
L3.value = "3.9nH"

C17 = Part("Device", "C", footprint="Capacitor_SMD:C_0402_1005Metric", dest=TEMPLATE)
C17.ref = "C17"
C17.value = "1.5pF"

D3 = Part("Device", "D_TVS", footprint="Diode_SMD:D_SOD-523", dest=TEMPLATE)
D3.ref = "D3"
D3.value = "PESD5V0S1BA"

# Antenna connector
J4 = Part("Connector", "Coaxial_SMA", footprint="Connector_Coaxial:SMA_Amphenol_132255_16_Horizontal", dest=TEMPLATE)
J4.ref = "J4"
J4.value = "SMA_ANT"

# RS-485 transceiver
U5 = Part("Interface_UART", "ADM2587E", footprint="Package_SO:SOIC-20W_7.5x12.8mm_P1.27mm", dest=TEMPLATE)
U5.ref = "U5"
U5.value = "ADM2587E"

C22 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C22.ref = "C22"
C22.value = "100nF"

C23 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C23.ref = "C23"
C23.value = "100nF"

C24 = Part("Device", "C", footprint="Capacitor_SMD:C_0805_2012Metric", dest=TEMPLATE)
C24.ref = "C24"
C24.value = "10uF"

D4 = Part("Device", "D_TVS", footprint="Diode_SMD:D_SOT-23", dest=TEMPLATE)
D4.ref = "D4"
D4.value = "SM712"

D5 = Part("Device", "D_TVS", footprint="Diode_SMD:D_SOT-23", dest=TEMPLATE)
D5.ref = "D5"
D5.value = "SM712"

R9 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R9.ref = "R9"
R9.value = "120"

R10 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R10.ref = "R10"
R10.value = "560"

R11 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R11.ref = "R11"
R11.value = "560"

J5 = Part("Connector", "Screw_Terminal_01x03", footprint="TerminalBlock:TerminalBlock_Altech_AK300-3_P5.00mm", dest=TEMPLATE)
J5.ref = "J5"
J5.value = "RS-485"

# Flash memory
U6 = Part("Memory_Flash", "W25Q64JVSNIQ", footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", dest=TEMPLATE)
U6.ref = "U6"
U6.value = "W25Q64JVSNIQ"

C25 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C25.ref = "C25"
C25.value = "100nF"

# Fuel gauge
U7 = Part("Power_Management", "BQ27441-G1A", footprint="Package_SON:Texas_R-PDSO-N8", dest=TEMPLATE)
U7.ref = "U7"
U7.value = "BQ27441-G1A"

C26 = Part("Device", "C", footprint="Capacitor_SMD:C_0603_1608Metric", dest=TEMPLATE)
C26.ref = "C26"
C26.value = "100nF"

# LEDs
D6 = Part("Device", "LED", footprint="LED_SMD:LED_0603_1608Metric", dest=TEMPLATE)
D6.ref = "D6"
D6.value = "Green"

D7 = Part("Device", "LED", footprint="LED_SMD:LED_0603_1608Metric", dest=TEMPLATE)
D7.ref = "D7"
D7.value = "Blue"

D8 = Part("Device", "LED", footprint="LED_SMD:LED_0603_1608Metric", dest=TEMPLATE)
D8.ref = "D8"
D8.value = "Yellow"

D9 = Part("Device", "LED", footprint="LED_SMD:LED_0603_1608Metric", dest=TEMPLATE)
D9.ref = "D9"
D9.value = "Red"

R12 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R12.ref = "R12"
R12.value = "1k"

R13 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R13.ref = "R13"
R13.value = "1k"

R14 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R14.ref = "R14"
R14.value = "1k"

R15 = Part("Device", "R", footprint="Resistor_SMD:R_0603_1608Metric", dest=TEMPLATE)
R15.ref = "R15"
R15.value = "1k"

# Service connectors
J6 = Part("Connector", "Conn_01x05_Male", footprint="Connector_PinHeader_1.27mm:PinHeader_1x05_P1.27mm_Vertical", dest=TEMPLATE)
J6.ref = "J6"
J6.value = "SWD"

J7 = Part("Connector", "Conn_01x04_Male", footprint="Connector_PinHeader_1.27mm:PinHeader_1x04_P1.27mm_Vertical", dest=TEMPLATE)
J7.ref = "J7"
J7.value = "UART"

# Test points
TP1 = Part("TestPoint", "TestPoint_Pad_D1.0mm", dest=TEMPLATE)
TP1.ref = "TP1"
TP1.value = "VBAT"

TP2 = Part("TestPoint", "TestPoint_Pad_D1.0mm", dest=TEMPLATE)
TP2.ref = "TP2"
TP2.value = "3V3"

TP3 = Part("TestPoint", "TestPoint_Pad_D1.0mm", dest=TEMPLATE)
TP3.ref = "TP3"
TP3.value = "GND"

TP4 = Part("TestPoint", "TestPoint_Pad_D1.0mm", dest=TEMPLATE)
TP4.ref = "TP4"
TP4.value = "SWDIO"

TP5 = Part("TestPoint", "TestPoint_Pad_D1.0mm", dest=TEMPLATE)
TP5.ref = "TP5"
TP5.value = "SWCLK"

# Mounting holes
MH1 = Part("Mechanical", "MountingHole_3.2mm_M3", dest=TEMPLATE)
MH1.ref = "MH1"

MH2 = Part("Mechanical", "MountingHole_3.2mm_M3", dest=TEMPLATE)
MH2.ref = "MH2"

MH3 = Part("Mechanical", "MountingHole_3.2mm_M3", dest=TEMPLATE)
MH3.ref = "MH3"

MH4 = Part("Mechanical", "MountingHole_3.2mm_M3", dest=TEMPLATE)
MH4.ref = "MH4"

# Create nets
SOLAR_VIN = Net("SOLAR_VIN")
VSYS = Net("VSYS")
VBAT = Net("VBAT")
VCC_3V3 = Net("VCC_3V3")
GND = Net("GND")
RF_ANT = Net("RF_ANT")
RS485_A = Net("RS485_A")
RS485_B = Net("RS485_B")
UART1_TX = Net("UART1_TX")
UART1_RX = Net("UART1_RX")
RS485_DE = Net("RS485_DE")
SPI1_SCK = Net("SPI1_SCK")
SPI1_MOSI = Net("SPI1_MOSI")
SPI1_MISO = Net("SPI1_MISO")
SPI1_CS = Net("SPI1_CS_FLASH")
I2C_SCL = Net("I2C1_SCL")
I2C_SDA = Net("I2C1_SDA")
VBAT_ADC = Net("VBAT_ADC")
CHG_STAT = Net("CHG_STAT")
SWDIO = Net("SWDIO")
SWCLK = Net("SWCLK")
NRST = Net("NRST")
LED_PWR = Net("LED_PWR")
LED_LORA = Net("LED_LORA")
LED_RS485 = Net("LED_RS485")
LED_ERR = Net("LED_ERR")

# Connect power section
J1[1] += SOLAR_VIN
J1[2] += GND
D1[1] += SOLAR_VIN
D1[2] += GND
D2[1] += SOLAR_VIN
D2[2] += VSYS
C1[1] += VSYS
C1[2] += GND
C2[1] += VSYS
C2[2] += GND

# Charge controller connections (simplified)
U1["VIN"] += VSYS
U1["VBAT"] += VBAT
U1["GND"] += GND
U1["STAT"] += CHG_STAT
R1[1] += VBAT
R1[2] += GND
R2[1] += VBAT
R2[2] += GND
R8[1] += VSYS
R8[2] += VBAT
C7[1] += VSYS
C7[2] += GND
C8[1] += VSYS
C8[2] += GND
C9[1] += VBAT
C9[2] += GND
L1[1] += VSYS
L1[2] += VBAT

# Battery
J2[1] += VBAT
J2[2] += GND
R4[1] += VBAT
R4[2] += VBAT_ADC
R5[1] += VBAT_ADC
R5[2] += GND
C10[1] += VBAT_ADC
C10[2] += GND

# DC-DC
U2["VIN"] += VSYS
U2["VOUT"] += VCC_3V3
U2["GND"] += GND
U2["EN"] += VSYS
U2["FB"] += VCC_3V3
L2[1] += VCC_3V3
L2[2] += GND
C3[1] += VCC_3V3
C3[2] += GND
C4[1] += VCC_3V3
C4[2] += GND
R6[1] += VCC_3V3
R6[2] += GND
R7[1] += VCC_3V3
R7[2] += GND

# LDO
U3["IN"] += VCC_3V3
U3["OUT"] += VCC_3V3
U3["GND"] += GND
C5[1] += VCC_3V3
C5[2] += GND
C6[1] += VCC_3V3
C6[2] += GND

# MCU (simplified connections)
U4["VDD"] += VCC_3V3
U4["VSS"] += GND
U4["PA0"] += SWDIO
U4["PA1"] += SWCLK
U4["NRST"] += NRST
U4["PA2"] += UART1_TX
U4["PA3"] += UART1_RX
U4["PB0"] += RS485_DE
U4["PB5"] += SPI1_SCK
U4["PB6"] += SPI1_MOSI
U4["PB7"] += SPI1_MISO
U4["PB8"] += SPI1_CS
U4["PB9"] += I2C_SCL
U4["PB10"] += I2C_SDA
U4["PA4"] += VBAT_ADC
U4["PA5"] += CHG_STAT
U4["PA6"] += LED_PWR
U4["PA7"] += LED_LORA
U4["PA8"] += LED_RS485
U4["PA9"] += LED_ERR
U4["RF_P"] += RF_ANT

# MCU decoupling
C11[1] += VCC_3V3
C11[2] += GND
C12[1] += VCC_3V3
C12[2] += GND
C13[1] += VCC_3V3
C13[2] += GND
C14[1] += VCC_3V3
C14[2] += GND
C15[1] += VCC_3V3
C15[2] += GND

# Crystals
Y1[1] += GND
Y2[1] += GND
C18[1] += GND
C19[1] += GND
C20[1] += GND
C21[1] += GND

# RF matching
C16[1] += RF_ANT
C16[2] += GND
L3[1] += RF_ANT
L3[2] += GND
C17[1] += RF_ANT
C17[2] += GND
D3[1] += RF_ANT
D3[2] += GND

# Antenna
J4[1] += RF_ANT
J4[2] += GND

# RS-485
U5["VCC"] += VCC_3V3
U5["GND"] += GND
U5["DI"] += UART1_TX
U5["RO"] += UART1_RX
U5["DE"] += RS485_DE
U5["A"] += RS485_A
U5["B"] += RS485_B
C22[1] += VCC_3V3
C22[2] += GND
C23[1] += VCC_3V3
C23[2] += GND
C24[1] += VCC_3V3
C24[2] += GND
D4[1] += RS485_A
D4[2] += GND
D5[1] += RS485_B
D5[2] += GND
R9[1] += RS485_A
R9[2] += RS485_B
R10[1] += VCC_3V3
R10[2] += RS485_A
R11[1] += RS485_B
R11[2] += GND
J5[1] += RS485_A
J5[2] += RS485_B
J5[3] += GND

# Flash
U6["VCC"] += VCC_3V3
U6["GND"] += GND
U6["CLK"] += SPI1_SCK
U6["DI"] += SPI1_MOSI
U6["DO"] += SPI1_MISO
U6["CS"] += SPI1_CS
C25[1] += VCC_3V3
C25[2] += GND

# Fuel gauge
U7["VCC"] += VCC_3V3
U7["GND"] += GND
U7["BAT"] += VBAT
U7["SCL"] += I2C_SCL
U7["SDA"] += I2C_SDA
C26[1] += VCC_3V3
C26[2] += GND

# LEDs
D6[1] += VCC_3V3
D6[2] += LED_PWR
D7[1] += VCC_3V3
D7[2] += LED_LORA
D8[1] += VCC_3V3
D8[2] += LED_RS485
D9[1] += VCC_3V3
D9[2] += LED_ERR
R12[1] += LED_PWR
R12[2] += GND
R13[1] += LED_LORA
R13[2] += GND
R14[1] += LED_RS485
R14[2] += GND
R15[1] += LED_ERR
R15[2] += GND

# Service connectors
J6[1] += VCC_3V3
J6[2] += SWDIO
J6[3] += GND
J6[4] += SWCLK
J6[5] += NRST
J7[1] += VCC_3V3
J7[2] += UART1_TX
J7[3] += UART1_RX
J7[4] += GND

# Test points
TP1[1] += VBAT
TP2[1] += VCC_3V3
TP3[1] += GND
TP4[1] += SWDIO
TP5[1] += SWCLK

# Mounting holes (no connections)
MH1[1] += GND
MH2[1] += GND
MH3[1] += GND
MH4[1] += GND

# Generate netlist
generate_netlist(file_="lorawan-modem.net")
print("Netlist generated!")

# Generate schematic
generate_xml(file_="lorawan-modem.xml")
print("XML generated!")

# Print stats
print(f"\nComponents: {len(Part.get_parts())}")
print(f"Nets: {len(Net.get_nets())}")
