# Ijr-X1-Core — Continue

## Current Status
**ERC: 0 violations ✅ — Schematic is clean.**

Last updated: 2026-08-20

## Completed Sections

### ✅ Phase 1 — USB-C Ports
- J1 (USB-C_PWR_IN, PowerOnly_6P): VBUS→+5V, CC1/CC2 labelled, GND on pins + shield
- J2 (USB-C_CPU_PROG, USB2.0_16P): VBUS→+5V, CC1/CC2, D+/D− (J2_DP/J2_DM), SBU no-connects, GND
- J3 (USB-C_UART_BRIDGE, USB2.0_16P): VBUS→+5V, CC1/CC2, D+/D−→GPIO_USB_DP/DM, SBU no-connects, GND
- R1–R6: 5.1kΩ CC pull-downs, each wired CC net → GND
- C1–C3: 100nF VBUS decoupling caps, +5V → GND

### ✅ Phase 2 — RP2040 GPIO Controller
- U1 (MCU_RaspberryPi:RP2040) placed and fully labelled:
  - Power: IOVDD/DVDD/ADC_AVDD/VREG_VIN/USB_VDD → +3V3, GND → GND
  - VREG_VOUT → VREG_VOUT net with C4 (1µF) filter cap
  - USB: USB_DM → GPIO_USB_DM, USB_DP → GPIO_USB_DP (connects to J3)
  - TESTEN → GND, XIN/XOUT → no-connect (using internal oscillator)
  - RUN → R7 (10kΩ pull-up to +3V3)
  - QSPI: QSPI_SS_N, QSPI_SCLK, QSPI_SD0–SD3 → U2 flash
  - SWD: SWD_CLK, SWD_DIO → J_SWD header
  - GPIO0–GPIO29 → J_GPIO header

- U2 (Memory_Flash:W25Q16JVSS) QSPI flash:
  - CS→QSPI_SS_N, CLK→QSPI_SCLK, IO0–IO3→QSPI_SD0–SD3
  - VCC→+3V3, GND→GND
  - C5 (100nF) decoupling cap on VCC

- J_GPIO (Conn_02x25_Odd_Even): GPIO0–GPIO29 on pins 1–30, +3V3 pin 49, GND pin 50, spare pins 31–48 no-connected
- J_SWD (Conn_02x03_Odd_Even): +3V3/SWDIO/GND/SWCLK/NC/NC (standard ARM SWD pinout)
- R7: 10kΩ RUN pull-up (+3V3 → RUN)
- PWR_FLAG: two flags placed — one on +3V3, one on GND (ERC power driver fix)

## Next Steps (in order)

### Step 1 — ATX Power Input
Place and wire:
- J_ATX24: Molex 24-pin ATX main power connector (Connector_Molex:Molex_Mini-Fit_Jr_5566-24A)
- J_EPS8: 2×4 EPS CPU power connector (Connector_Molex:Molex_Mini-Fit_Jr_5566-08A)
- J_PCIE1, J_PCIE2: 2× PCIe 6+2 connectors (Connector_PinHeader_2.54mm:PinHeader_2x04_P2.54mm)
- Power button: 2-pin header (SW_PWR)
- Power LED: 2-pin header + R (LED_PWR)
- Label rails: +12V, +5V, +3V3, -12V, PS_ON, PWRGOOD

### Step 2 — CPU VRM (i7-11800H VCORE)
- Multi-phase VRM IC: ISL69269 or MP2857 (4-phase)
- Inductors, MOSFETs, bulk caps on VCORE rail (~1.0–1.5V, up to 45A)
- VCCIO, VCCSA, VCCPLL rails (simpler, 1-phase each)

### Step 3 — SO-DIMM Slots
- 2× DDR4 260-pin SO-DIMM connectors
- VDDQ (1.2V) reference voltage circuit
- Address/data bus from CPU

### Step 4 — M.2 Slots
- M.2 Key-M x4 NVMe slot
- M.2 Key-M x8 GPU module slot (PCIe 4.0)

### Step 5 — PCB Layout
- Begin after schematic is fully complete and BOM is finalized

## Critical Notes

### Data Loss Incident (resolved)
`sch_build_circuit` is a **silent no-op** — it returns "updated" but writes nothing to disk.
**Never use it.** Always use `sch_add_component` + `sch_add_label` directly.

### Save Verification
After each session, verify schematic file size is growing:
```bash
ls -lh ~/Downloads/Ijr-X1-Core/Ijr-X1-Core.kicad_sch
```

### Component counts (end of Phase 2)
- 21 components total (19 + 2 PWR_FLAGs)
- 80 nets, 0 ERC violations
