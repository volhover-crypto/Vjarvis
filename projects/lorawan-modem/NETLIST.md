# LoRaWAN Modem LVM-485-SOLAR-01
# Schematic Netlist Description
# For manual entry in KiCad 7

## Sheet 1: Power Supply

### Power Rails
- **VSYS** — System bus voltage (~5-17V after reverse protection)
- **VBAT** — Battery voltage (5.0-7.4V for LiFePO4 2S)
- **VCC_3V3** — Main 3.3V rail (from DC-DC)
- **VCC_RF** — Clean 3.3V rail for RF (from LDO)
- **VISO** — Isolated RS-485 bus side power
- **GND** — Common ground
- **RS485_GND** — Isolated RS-485 ground

### Connections

#### Solar Input (J1)
- J1.1 → SOLAR_VIN (positive)
- J1.2 → GND

#### TVS Protection (D1)
- D1.1 → SOLAR_VIN
- D1.2 → GND

#### Reverse Polarity Protection (D2)
- D2.1 (anode) → SOLAR_VIN
- D2.2 (cathode) → VSYS

#### Input Capacitors
- C1: VSYS ↔ GND
- C2: VSYS ↔ GND

#### Charge Controller (U1 — BQ24650RGER)
- U1.VIN → VSYS
- U1.VBAT → VBAT
- U1.GND → GND
- U1.STAT → CHG_STAT (to MCU GPIO)
- U1.SCL → I2C1_SCL
- U1.SDA → I2C1_SDA
- U1.COMP → R3 → GND, C7 → GND
- U1.FB → R1 → VBAT, R2 → GND
- U1.SW → L1 → VBAT
- U1.SRP → VSYS (via R8 sense resistor)
- U1.SRN → VBAT (via R8 sense resistor)
- U1.CIN → C8 → GND
- U1.COUT → C9 → GND

#### Battery Connector (J2)
- J2.1 → VBAT
- J2.2 → GND

#### Battery Sense Divider
- R4: VBAT → VBAT_ADC
- R5: VBAT_ADC → GND
- C10: VBAT_ADC → GND

#### DC-DC Converter (U2 — TPS62840DLAR)
- U2.VIN → VSYS
- U2.VOUT → VCC_3V3
- U2.GND → GND
- U2.EN → VSYS (always on) or MCU GPIO
- U2.FB → R6 → VCC_3V3, R7 → GND
- U2.SW → L2 → VCC_3V3

#### DC-DC Output Caps
- C3: VCC_3V3 ↔ GND
- C4: VCC_3V3 ↔ GND

#### LDO (U3 — TPS7A0233PDBVR)
- U3.IN → VCC_3V3
- U3.OUT → VCC_RF
- U3.GND → GND
- U3.EN → VCC_3V3 (always on)

#### LDO Caps
- C5: VCC_3V3 ↔ GND
- C6: VCC_RF ↔ GND

---

## Sheet 2: MCU + LoRa

### Connections

#### MCU (U4 — STM32WL55JCI6)
Power:
- U4.VDD → VCC_3V3 (×3 pins, each with 100nF decap: C11, C12, C13)
- U4.VDDA → VCC_RF (RF power, clean)
- U4.VSS → GND
- U4.VCAP1 → C14 → GND
- U4.VCAP2 → C15 → GND

Clock:
- U4.OSC_IN → Y1 → OSC_OUT
- U4.OSC_IN → C18 → GND
- U4.OSC_OUT → C19 → GND
- U4.OSC32_IN → Y2 → OSC32_OUT
- U4.OSC32_IN → C20 → GND
- U4.OSC32_OUT → C21 → GND

Reset:
- U4.NRST → SWD connector (J6.5), 100nF cap to GND

SPI1 (Flash):
- U4.SPI1_SCK → U6.SCK
- U4.SPI1_MOSI → U6.MOSI
- U4.SPI1_MISO → U6.MISO
- U4.SPI1_CS_FLASH → U6.CS

UART1 (RS-485):
- U4.UART1_TX → U5.DI (RS-485 driver input)
- U4.UART1_RX → U5.RO (RS-485 receiver output)
- U4.RS485_DE → U5.DE (driver enable)

I2C1 (Fuel Gauge):
- U4.I2C1_SCL → U7.SCL
- U4.I2C1_SDA → U7.SDA

GPIO (LEDs):
- U4.LED_PWR → D6 (green) → R12 → GND
- U4.LED_LORA → D7 (blue) → R13 → GND
- U4.LED_RS485 → D8 (yellow) → R14 → GND
- U4.LED_ERR → D9 (red) → R15 → GND

ADC:
- U4.VBAT_ADC → R4/R5 divider (battery sense)
- U4.CHG_STAT → U1.STAT

SWD:
- U4.SWDIO → J6.2
- U4.SCLK → J6.4

RF:
- U4.RF_ANT → C16 → L3 → GND, C17 → GND (matching network)
- U4.RF_ANT → D3 (ESD) → GND
- U4.RF_ANT → J4 (SMA connector)

#### Flash Memory (U6 — W25Q64JVSSIQ)
- U6.CS → SPI1_CS_FLASH
- U6.SCK → SPI1_SCK
- U6.MOSI → SPI1_MOSI
- U6.MISO → SPI1_MISO
- U6.VCC → VCC_3V3
- U6.GND → GND
- U6.WP → VCC_3V3 (write protect disabled)
- U6.HOLD → VCC_3V3 (hold disabled)
- C25: VCC_3V3 ↔ GND

#### Antenna Connector (J4)
- J4.center → RF_ANT (via matching network)
- J4.gnd → GND

#### ESD Protection (D3)
- D3.1 → RF_ANT
- D3.2 → GND

---

## Sheet 3: RS-485 Interface

### Connections

#### RS-485 Transceiver (U5 — ADM2587EBRWZ)
Logic side:
- U5.VDD1 → VCC_3V3
- U5.GND1 → GND
- U5.DI → UART1_TX (from MCU)
- U5.RO → UART1_RX (to MCU)
- U5.DE → RS485_DE (from MCU)
- U5.RE → GND (receiver always enabled)
- U5.VISO_OUT → VISO (isolated power output)

Bus side:
- U5.VDD2 → VISO
- U5.GND2 → RS485_GND
- U5.A → RS485_A
- U5.B → RS485_B
- U5.Y → (connected internally)
- U5.Z → (connected internally)

#### Decoupling
- C22: VCC_3V3 ↔ GND (logic side)
- C23: VISO ↔ RS485_GND (bus side)
- C24: VISO ↔ RS485_GND (additional)

#### TVS Protection
- D4: RS485_A ↔ RS485_GND
- D5: RS485_B ↔ RS485_GND

#### Termination
- R9: RS485_A ↔ RS485_B (120 Ohm)

#### Bias Resistors
- R10: VISO → RS485_A (pull-up, 560 Ohm)
- R11: RS485_B → RS485_GND (pull-down, 560 Ohm)

#### Connector (J5)
- J5.1 → RS485_A
- J5.2 → RS485_B
- J5.3 → RS485_GND

---

## Sheet 4: Memory + Indicators + Service

### LED Indicators
- D6 (Green): VCC_3V3 → anode, cathode → R12 → GND, cathode → LED_PWR (MCU)
- D7 (Blue): VCC_3V3 → anode, cathode → R13 → GND, cathode → LED_LORA (MCU)
- D8 (Yellow): VCC_3V3 → anode, cathode → R14 → GND, cathode → LED_RS485 (MCU)
- D9 (Red): VCC_3V3 → anode, cathode → R15 → GND, cathode → LED_ERR (MCU)

### SWD Connector (J6)
- J6.1 → VCC_3V3
- J6.2 → SWDIO
- J6.3 → GND
- J6.4 → SWCLK
- J6.5 → NRST

### UART Connector (J7)
- J7.1 → VCC_3V3
- J7.2 → UART1_TX
- J7.3 → UART1_RX
- J7.4 → GND

### Fuel Gauge (U7 — MAX17048G+T)
- U7.VCC → VCC_3V3
- U7.GND → GND
- U7.BAT → VBAT
- U7.SCL → I2C1_SCL
- U7.SDA → I2C1_SDA
- U7.CTPIC → GND (no thermistor)
- C26: VCC_3V3 ↔ GND

### Test Points
- TP1 → VBAT
- TP2 → VCC_3V3
- TP3 → GND
- TP4 → SWDIO
- TP5 → SWCLK

---

## Power Budget Summary

| Rail | Source | Voltage | Max Current | Purpose |
|------|--------|---------|-------------|---------|
| VSYS | Solar/Battery | 5-17V | 2A | System bus |
| VBAT | LiFePO4 2S | 5.0-7.4V | 2A | Battery |
| VCC_3V3 | DC-DC (TPS62840) | 3.3V | 300mA | Logic, peripherals |
| VCC_RF | LDO (TPS7A02) | 3.3V | 200mA | RF section |
| VISO | ADM2587E internal | ~3.3V | 50mA | RS-485 bus side |

## Estimated Current Consumption

| Mode | Current | Duration |
|------|---------|----------|
| Deep sleep | 150 µA | ~297 s per 5 min cycle |
| Active (RS-485 poll) | 30 mA | ~200 ms per cycle |
| LoRa TX | 80 mA | ~500 ms per cycle |
| LoRa RX | 12 mA | ~3000 ms per cycle |
| **Average** | **~0.43 mA** | — |
| **Daily total** | **~10.3 mAh** | — |

## Battery Autonomy

| Battery | Capacity | Autonomy |
|---------|----------|----------|
| LiFePO4 2S 200mAh | 200 mAh | ~19 days |
| LiFePO4 2S 500mAh | 500 mAh | ~48 days |
| LiFePO4 2S 1Ah | 1000 mAh | ~97 days |

Target: 5-7 days → 200mAh minimum, 500mAh recommended
