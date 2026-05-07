# LoRaWAN Modem LVM-485-SOLAR-01
# Bill of Materials (BOM) v0.1
# Date: 2026-05-07

## Power Input Section

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| J1 | SOLAR_IN | JST-PH 2-pin | JST_PH_B2B-PH-K | Solar panel input, 6-18V |
| D1 | SMBJ18A | SMB | SMBJ18A | TVS diode, 18V standoff |
| D2 | SS34 | SMA | SS34 | Schottky diode, 40V/3A |
| C1 | 100uF/25V | 1210 | GRM32ER71E107KA12L | Bulk input capacitor |
| C2 | 100nF | 0603 | GRM188R71H104KA93D | Input bypass capacitor |

## Power Management (Charge Controller)

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| U1 | BQ24650RGER | QFN-24 | BQ24650RGER | MPPT charge controller |
| R1 | 100k | 0603 | RC0603FR-07100KL | Charge FB upper |
| R2 | 49.9k | 0603 | RC0603FR-0749K9L | Charge FB lower |
| R3 | 10k | 0603 | RC0603FR-0710KL | Compensation R |
| R8 | 0.05 | 0805 | RL2512FK-070R05L | Current sense |
| C7 | 10nF | 0603 | GRM188R71H103KA01D | Compensation C |
| C8 | 1uF | 0603 | GRM188R71H105KA12D | VIN bypass |
| C9 | 10uF | 0805 | GRM21BR71A106KA73L | VBAT output |
| L1 | 10uH/3A | 7.3x7.3 | SRP7028A-100M | Charge inductor |

## Battery

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| J2 | BATTERY | JST-PH 2-pin | JST_PH_B2B-PH-K | LiFePO4 2S connection |
| R4 | 100k | 0603 | RC0603FR-07100KL | VBAT sense upper |
| R5 | 49.9k | 0603 | RC0603FR-0749K9L | VBAT sense lower |
| C10 | 100nF | 0603 | GRM188R71H104KA93D | VBAT sense filter |

## DC-DC Converter

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| U2 | TPS62840DLAR | DSBGA-8 | TPS62840DLAR | Buck, 3.3V/300mA, Iq=700nA |
| L2 | 2.2uH | 0806 | LQM21PN2R2MC0D | DC-DC inductor |
| C3 | 22uF | 0805 | GRM21BR71A226ME44L | Output cap |
| C4 | 100nF | 0603 | GRM188R71H104KA93D | Output bypass |
| R6 | 1M | 0603 | RC0603FR-071ML | FB upper |
| R7 | 332k | 0603 | RC0603FR-07332KL | FB lower |

## LDO (RF)

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| U3 | TPS7A0233PDBVR | SOT-23-5 | TPS7A0233PDBVR | LDO, 3.3V/200mA, Iq=25nA |
| C5 | 1uF | 0603 | GRM188R71H105KA12D | Input cap |
| C6 | 100nF | 0603 | GRM188R71H104KA93D | Output cap |

## MCU + LoRa

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| U4 | STM32WL55JCI6 | QFN-48 | STM32WL55JCI6 | MCU+LoRa, 868MHz |
| C11 | 100nF | 0603 | GRM188R71H104KA93D | VDD decap #1 |
| C12 | 100nF | 0603 | GRM188R71H104KA93D | VDD decap #2 |
| C13 | 100nF | 0603 | GRM188R71H104KA93D | VDD decap #3 |
| C14 | 1uF | 0603 | GRM188R71H105KA12D | VCAP1 |
| C15 | 1uF | 0603 | GRM188R71H105KA12D | VCAP2 |
| C16 | 1pF | 0402 | GRM1555C1H1R0BA01D | RF match C1 |
| L3 | 3.9nH | 0402 | LQP03TN3N9B02D | RF match L |
| C17 | 1.5pF | 0402 | GRM1555C1H1R5BA01D | RF match C2 |
| Y1 | 32MHz | 3.2x2.5 | ABM8-32.000MHZ-B2-T | HSE crystal |
| C18 | 10pF | 0402 | GRM1555C1H100JA01D | HSE load C1 |
| C19 | 10pF | 0402 | GRM1555C1H100JA01D | HSE load C2 |
| Y2 | 32.768kHz | 3.2x1.5 | ABS07-32.768KHZ-T | LSE crystal |
| C20 | 6pF | 0402 | GRM1555C1H6R0DA01D | LSE load C1 |
| C21 | 6pF | 0402 | GRM1555C1H6R0DA01D | LSE load C2 |
| J4 | SMA | Edge-mount | SMA_Edge_50Ohm | Antenna connector |
| D3 | PESD5V0S1BA | SOD-523 | PESD5V0S1BA | RF ESD protection |

## RS-485 Interface

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| U5 | ADM2587EBRWZ | SOIC-20 | ADM2587EBRWZ | Isolated RS-485 transceiver |
| C22 | 100nF | 0603 | GRM188R71H104KA93D | VDD1 decap |
| C23 | 100nF | 0603 | GRM188R71H104KA93D | VDD2 decap |
| C24 | 10uF | 0805 | GRM21BR71A106KA73L | VISO output |
| D4 | SM712 | SOT-23 | SM712-02HTG | TVS line A |
| D5 | SM712 | SOT-23 | SM712-02HTG | TVS line B |
| R9 | 120 | 0603 | RC0603FR-07120RL | Termination resistor |
| R10 | 560 | 0603 | RC0603FR-07560RL | Bias A (pull-up) |
| R11 | 560 | 0603 | RC0603FR-07560RL | Bias B (pull-down) |
| J5 | Screw Terminal | 3-pin 3.5mm | ScrewTerminal_3pin_3.5mm | RS-485 connector |

## Memory

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| U6 | W25Q64JVSSIQ | SOIC-8 | W25Q64JVSSIQ | SPI NOR Flash, 8MB |
| C25 | 100nF | 0603 | GRM188R71H104KA93D | Decoupling |

## Indicators

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| D6 | Green LED | 0603 | LTST-C191KGKT | Power LED |
| D7 | Blue LED | 0603 | LTST-C191KBKT | LoRa LED |
| D8 | Yellow LED | 0603 | LTST-C191KSKT | RS-485 LED |
| D9 | Red LED | 0603 | LTST-C191KRKT | Error LED |
| R12 | 1k | 0603 | RC0603FR-071KL | LED R1 |
| R13 | 1k | 0603 | RC0603FR-071KL | LED R2 |
| R14 | 1k | 0603 | RC0603FR-071KL | LED R3 |
| R15 | 1k | 0603 | RC0603FR-071KL | LED R4 |

## Service Interface

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| J6 | SWD | 5-pin 1.27mm | PinHeader_5pin_1.27mm | SWD debug |
| J7 | UART | 4-pin 1.27mm | PinHeader_4pin_1.27mm | UART service |

## Fuel Gauge

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| U7 | MAX17048G+T | TDFN-8 | MAX17048G+T | Battery fuel gauge |
| C26 | 100nF | 0603 | GRM188R71H104KA93D | Decoupling |

## Test Points

| Ref | Value | Package | MPN | Description |
|-----|-------|---------|-----|-------------|
| TP1 | TestPoint | 1mm | TestPoint_1mm | VBAT |
| TP2 | TestPoint | 1mm | TestPoint_1mm | 3.3V |
| TP3 | TestPoint | 1mm | TestPoint_1mm | GND |
| TP4 | TestPoint | 1mm | TestPoint_1mm | SWDIO |
| TP5 | TestPoint | 1mm | TestPoint_1mm | SWCLK |

---

## Total Component Count

| Section | Count |
|---------|-------|
| Power Input | 5 |
| Power Management | 10 |
| Battery | 4 |
| DC-DC | 6 |
| LDO | 3 |
| MCU + LoRa | 18 |
| RS-485 | 11 |
| Memory | 2 |
| Indicators | 8 |
| Service | 2 |
| Fuel Gauge | 2 |
| Test Points | 5 |
| **Total** | **76** |
