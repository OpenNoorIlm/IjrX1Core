# Continue From Here

## ⚠️ DATA LOSS INCIDENT — Session of 2026-08-18
**What happened:** kicad-mcp-pro writes schematic changes to an in-memory state during a session.
When the Claude conversation ends (timeout, restart, context limit), that in-memory state is DROPPED.
`Ijr-X1-Core.kicad_sch` was found to be 418 bytes — essentially empty despite appearing populated.

**Root cause confirmed:** `sch_build_circuit` is a silent no-op — it returns "updated" but never
writes to disk. **Never use `sch_build_circuit` again.**

**Fix confirmed:** `sch_add_component` and `sch_add_label` write directly to disk and persist
across sessions. All future placement must use these tools only.

**Lesson / rules going forward:**
- Always use `sch_add_component` for placing symbols — NOT `sch_build_circuit`
- Always use `sch_add_label` for net labels — NOT `sch_build_circuit`
- After every section, call `sch_get_circuit_ir` and verify non-zero component count
- Ground truth = `.kicad_sch` file size (should be >> 1KB) + circuit IR output

---

## Current Schematic Status — 2026-08-19
**File:** `/home/bismillah/Downloads/Ijr-X1-Core/Ijr-X1-Core.kicad_sch`
**Verified on disk:** YES (circuit IR confirmed non-zero components)

### ✅ Phase 1 — USB-C Ports (COMPLETE)
- J1: USB_C_Receptacle_PowerOnly_6P @ (39.37, 39.37) — Power input only
- J2: USB_C_Receptacle_USB2.0_16P @ (39.37, 90.17) — CPU programming / debug
- J3: USB_C_Receptacle_USB2.0_16P @ (39.37, 139.70) — GPIO controller USB / firmware
- R1–R6: 5.1kΩ CC pull-down resistors (2 per port)
- C1–C3: 100nF VBUS decoupling caps
- ⚠️ STILL NEEDED: net labels on J1/J2/J3 pins (CC, VBUS, GND, D+/D−, SBU no-connects)

### ✅ Phase 2 — RP2040 GPIO Controller (COMPLETE — labelled)
- U1: MCU_RaspberryPi:RP2040 @ (149.86, 90.17)
- Power: IOVDD/DVDD/ADC_AVDD/VREG_VIN/USB_VDD → +3V3 labels ✅
- GND → GND label (pin 57, bottom) ✅
- VREG_VOUT → VREG_VOUT net label; C4 (1µF) on VREG_VOUT → GND ✅
- USB: USB_DM → GPIO_USB_DM; USB_DP → GPIO_USB_DP ✅
- TESTEN → GND ✅
- XIN, XOUT → no-connect (using internal oscillator) ✅
- RUN → R7 (10kΩ) pull-up; R7 between +3V3 and RUN net; RUN label on U1 pin 26 ✅
- QSPI: QSPI_SS_N, QSPI_SCLK, QSPI_SD0–SD3 net labels on pins 56/52/53/55/54/51 ✅
- SWD: SWD_CLK, SWD_DIO net labels on pins 24/25 ✅
- GPIO0–GPIO29 net labels on all right-side pins (pins 2–18, 27–41) ✅

### 🔄 Phase 2 — W25Q16 QSPI Flash (IN PROGRESS)
- U2: Memory_Flash:W25Q16JVSS @ (100.33, 110.49) — 2MB QSPI flash for RP2040 firmware
- Pin positions (absolute):
  - Pin 1 (~CS~)     @ (90.17, 102.87) — left side
  - Pin 2 (DO/IO1)   @ (90.17, 110.49)
  - Pin 3 (~WP~/IO2) @ (90.17, 113.03)
  - Pin 4 (GND)      @ (100.33, 123.19) — bottom right
  - Pin 5 (DI/IO0)   @ (90.17, 107.95)
  - Pin 6 (CLK)      @ (90.17, 105.41)
  - Pin 7 (~HOLD~/IO3) @ (90.17, 115.57)
  - Pin 8 (VCC)      @ (100.33, 97.79) — top right
- Labels placed so far:
  - QSPI_SS_N @ (90.17, 102.87) ✅
  - QSPI_SCLK @ (90.17, 105.41) ✅
  - QSPI_SD0  @ (90.17, 107.95) ✅
  - QSPI_SD1  @ (90.17, 110.49) ✅
- ⚠️ STILL NEEDED:
  - QSPI_SD2 label @ (90.17, 113.03)  [pin 3 ~WP~/IO2]
  - QSPI_SD3 label @ (90.17, 115.57)  [pin 7 ~HOLD~/IO3]
  - +3V3 label @ (100.33, 97.79)      [pin 8 VCC]
  - GND label @ (100.33, 123.19)      [pin 4 GND]
  - C5 (100nF) decoupling on VCC

---

## Resume Here — Remaining Work (in order)

### 1. Finish U2 (W25Q16) labels + decoupling cap
- QSPI_SD2 @ (90.17, 113.03), angle=180
- QSPI_SD3 @ (90.17, 115.57), angle=180
- +3V3 @ (100.33, 97.79), angle=270
- GND @ (100.33, 123.19), angle=90
- C5 (100nF) near U2 VCC pin with +3V3 and GND labels

### 2. GPIO Header — J_GPIO
- Symbol: Connector_PinHeader_2.54mm:PinHeader_2x25_P2.54mm_Vertical (or Conn_02x25_Odd_Even)
- Place at X≈220, Y≈90
- Labels: GPIO0–GPIO29 on signal pins, +3V3 and GND on power pins

### 3. SWD Debug Header — J_SWD
- Symbol: Connector:ARM_JTAG_SWD_10 or Conn_02x03_Odd_Even
- Place at X≈220, Y≈160
- Labels: SWD_CLK, SWD_DIO, +3V3, GND

### 4. J3 USB D+/D− net labels
- J3 D− pin (A7) → label GPIO_USB_DM
- J3 D+ pin (A6) → label GPIO_USB_DP
- J3 D− pin (B7) → label GPIO_USB_DM
- J3 D+ pin (B6) → label GPIO_USB_DP

### 5. J1/J2/J3 power and CC net labels
- All VBUS pins → +5V label
- All GND pins → GND label
- J1 CC1 → R1 top; R1 bottom → GND; J1 CC2 → R2 top; R2 bottom → GND
- J2 CC1 → R3 top; R3 bottom → GND; J2 CC2 → R4 top; R4 bottom → GND
- J3 CC1 → R5 top; R5 bottom → GND; J3 CC2 → R6 top; R6 bottom → GND
- J2/J3 SBU1, SBU2 → no-connect markers

### 6. Run ERC → target 0 violations

---

## Next Steps After RP2040 Section Complete (original plan)

### Step 1 — ATX Power Input Section
| Ref | Symbol | Value | Purpose |
|---|---|---|---|
| J_ATX | Connector:ATX-24 | Main board power | 12V/5V/3.3V/GND/PS_ON#/PWR_OK |
| J_EPS | Connector:EPS-8 | CPU 12V power | |
| J_PCIE1 | Connector:PCIe-8 | GPU power rail 1 | |
| J_PCIE2 | Connector:PCIe-8 | GPU power rail 2 | |

### Step 2 — CPU Power (VRM Section)
- Multi-phase VRM IC for i7-11800H VCORE
- Candidates: Renesas RAA229004, MP2857, ISL69269
- Reference: Framework 13 schematics (community Tiger Lake-H reference)

### Step 3 — SO-DIMM Slots
- 2× DDR4 SO-DIMM 260-pin connectors
- VDDQ = 1.2V, VTT = 0.6V reference voltage circuit

### Step 4 — M.2 Slots
- M.2 Slot 1: PCIe 4.0 x4 NVMe (M-key, 2280)
- M.2 Slot 2: PCIe 4.0 x8 GPU module (extended M-key)

### Step 5 — PCB Layout

---

## How to Resume MCP Work (new session)
```
# Step 1 — load tools
tool_search("kicad")        # loads kicad_call, kicad_list_tools
tool_search("read file")    # loads Commander:read_file
tool_search("write file")   # loads Commander:write_file

# Step 2 — verify schematic is real (ALWAYS do this first)
kicad_call("sch_get_circuit_ir")
# Must return non-zero components. If 0 → schematic empty, stop and investigate.

# Step 3 — read this file and about.md
Commander:read_file("/home/bismillah/Downloads/Ijr-X1-Core/continue.md")
Commander:read_file("/home/bismillah/Downloads/Ijr-X1-Core/about.md")

# Step 4 — resume from "Resume Here" section above
```

## Critical Rules for Next Claude
- NEVER use sch_build_circuit — it is a confirmed no-op that does not write to disk
- ALWAYS use sch_add_component + sch_add_label for all placement
- ALWAYS verify with sch_get_circuit_ir before doing any work
- Project dir: /home/bismillah/Downloads/Ijr-X1-Core
- about.md is the source of truth for all design decisions
