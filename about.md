# Ijr-X1-Core — Project Overview

## What is this?
A custom x86 carrier board / single-board computer designed from scratch in KiCad 10.
Codename: **Ijr X1 Core**

The board is designed around a **module-based CPU approach** — the CPU (Intel Core i7-11800H)
is a BGA mobile chip soldered directly to the board, with all heavy routing (DDR, power sequencing)
handled on-board. The board exposes M.2 slots, PCIe GPU slot, USB-C ports, GPIO, and a standard
ATX PSU power input — essentially a custom mini-ITX-style carrier board with full modularity.

---

## ⚠️ MCP Schematic Persistence Warning
kicad-mcp-pro writes to in-memory state during a session. When the Claude conversation ends,
that state is DROPPED unless it was flushed to disk. The `.kicad_sch` file must be verified
after every session — check file size (should be >> 1KB) and run `sch_get_circuit_ir` which
must return non-zero component counts. `sch_get_symbols` alone is NOT reliable — it can return
stale cached data from a previous session. See `continue.md` for the full incident log.

---

## Project Directory
`/home/bismillah/Downloads/Ijr-X1-Core`

## MCP Setup
- Commander MCP server: `/home/bismillah/Downloads/mcp-tool-commander/server.py`
- KiCad MCP Pro is bridged INTO Commander via `kicad_call()` and `kicad_list_tools()`
- Mode: `write`, Profile: `schematic_authoring`
- Default project dir is hardcoded in the bridge as `~/Downloads/Ijr-X1-Core`
- To restart MCP: restart Claude Desktop (fully quit from system tray, reopen)
- After restart always run `tool_search("kicad")` first to load the tools into context

---

## CPU — Intel Core i7-11800H (LOCKED)

| Property | Value |
|---|---|
| Architecture | Tiger Lake-H, Willow Cove, 10nm SuperFin |
| Cores / Threads | 8C / 16T |
| Base / Boost | 2.3 GHz / 4.6 GHz |
| TDP | 45W (configurable 35W–115W) |
| Package | FCBGA1787 (soldered directly to board) |
| PCIe Version | **4.0** |
| PCIe Lanes (CPU) | **20 lanes total** |
| Memory | DDR4-3200 SO-DIMM, up to 128GB, dual channel |
| iGPU | Intel UHD Graphics (32 EU, 350–1450 MHz) |
| Thunderbolt | **Thunderbolt 4 / USB4 integrated** |
| NPU | None |
| Grey-market price | ~$50–80 (AliExpress/eBay, pulled from laptops) |

### Why i7-11800H was chosen
- PCIe 4.0 with 20 lanes — enough for x8 GPU + x4 NVMe + misc with room to spare
- DDR4 SO-DIMM support (user-replaceable RAM)
- Thunderbolt 4 built-in (no extra chip needed)
- x86 — full Linux and Windows app compatibility
- Under $100 grey-market
- No NPU needed (GGUF/llama.cpp runs on CPU/GPU, NPU toolchain too immature for XDNA 1)

### PCIe Lane Allocation Plan
| Device | Lanes | PCIe Gen |
|---|---|---|
| GPU M.2 slot | x8 | 4.0 |
| NVMe M.2 slot | x4 | 4.0 |
| USB / misc peripherals | x4 | 4.0 |
| Remaining | x4 | 4.0 |

---

## Memory — DDR4 SO-DIMM

| Property | Value |
|---|---|
| Type | DDR4-3200 |
| Slots | 2× SO-DIMM |
| Max capacity | 128GB (64GB per slot) |
| Channels | Dual channel |
| Voltage | 1.2V |

User installs their own RAM modules. No soldered RAM on board.

---

## Storage

| Slot | Interface | Form Factor | Purpose |
|---|---|---|---|
| M.2 Slot 1 | PCIe 4.0 x4 NVMe | M.2 2280 | Primary SSD |
| M.2 Slot 2 | PCIe 4.0 x8 | M.2 (custom/extended) | Discrete GPU module |

### GPU M.2 Slot Notes
- Routed as PCIe 4.0 x8 — double the bandwidth of standard M.2
- Standard M.2 only carries 3.3V/3A (≈10W) — NOT enough for a GPU
- GPU requires a **dedicated 12V power rail** via external PCIe power connectors
- Users plug a PCIe GPU module or adapter into this slot + connect the power cables
- Fallback: if no GPU is installed, Intel UHD iGPU handles display output

---

## USB-C Ports (DESIGNED — schematic rebuild in progress after data loss)

| Port | Ref | Role | Protocol | Symbol Used |
|---|---|---|---|---|
| Port 1 | J1 | Power input only | USB-C PD 3.1 | USB_C_Receptacle_PowerOnly_6P |
| Port 2 | J2 | CPU programming / debug / data | USB 2.0 | USB_C_Receptacle_USB2.0_16P |
| Port 3 | J3 | GPIO controller firmware / UART | USB 2.0 | USB_C_Receptacle_USB2.0_16P |

### USB-C Schematic Design (confirmed correct, needs rebuild)
- J1, J2, J3 with CC resistors (6× 5.1kΩ), decoupling caps (3× 100nF), VBUS/GND symbols
- No-connect markers on SBU pins
- Target ERC: 0 violations

---

## GPIO Controller — RP2040 (CONFIRMED DESIGN DECISION)

| Property | Value |
|---|---|
| IC | Raspberry Pi RP2040 |
| KiCad symbol | MCU_RaspberryPi:RP2040 |
| Reference | U1 |
| USB connection | Native USB — USB_DM/USB_DP directly to J3 (no bridge chip needed) |
| CPU interface | UART / SPI / I2C via GPIO pins |
| GPIO pins | GPIO0–29 (30 pins) → 2×25 GPIO header (J_GPIO) |
| Firmware flash | Over J3 USB-C (BOOTSEL mode) |
| Flash IC | W25Q16JVSSIQ 2MB QSPI flash |
| Debug | SWD header (J_SWD) 2×3 pin |

### Why RP2040 (not CH340N/CP2102N)
- Native USB — plugs directly into J3 D+/D− without a bridge chip
- Programmable — flash new GPIO behavior without hardware redesign
- 30 GPIO pins via bit-bang (SPI, I2C, UART, PWM — all in software)
- PIO state machines for deterministic timing
- Extremely well-documented, open hardware, cheap (~$1)

### RP2040 Support Circuit
| Section | Components |
|---|---|
| Power input | VREG_VIN → +3V3 |
| Decoupling | 100nF caps on IOVDD, DVDD, ADC_AVDD, USB_VDD |
| Internal reg | 1µF cap on VREG_VOUT (1.1V) |
| USB | USB_DM/USB_DP → net labels → J3 D−/D+ |
| Reset | RUN → 10kΩ to +3V3 |
| Test disable | TESTEN → GND |
| Clock | 12MHz crystal on XIN/XOUT (or XIN NC, use internal oscillator) |
| QSPI flash | W25Q16 on QSPI_SS/SCLK/SD0–SD3, 100nF decoupling |
| GPIO header | GPIO0–29 → J_GPIO (2×25 pin) |
| Debug | SWCLK/SWDIO → J_SWD (2×3 pin) |

---

## Power System (DESIGNED — not yet in schematic)

### Design Target: 700W total board power budget

#### Worst-case power breakdown
| Component | Power |
|---|---|
| Intel i7-11800H CPU | 45W |
| DDR4 RAM (2× SO-DIMM) | ~10W |
| NVMe SSD | ~8W |
| Board misc (USB, GPIO, etc.) | ~15W |
| Max GPU (e.g. RTX 4090) | 450W |
| **Total worst case** | **~528W** |
| **+25% headroom** | **~660W** |
| **Design target** | **700W** |

#### Power Input Connectors (to be added to schematic)
| Connector | Voltage | Max Power | Purpose |
|---|---|---|---|
| ATX 24-pin socket | 12V / 5V / 3.3V | ~600W+ | Main board power |
| EPS 8-pin socket | 12V | 150W | CPU power |
| PCIe 6+2 pin #1 | 12V | 150W | GPU power rail 1 |
| PCIe 6+2 pin #2 | 12V | 150W | GPU power rail 2 |
| **Total deliverable** | | **~750W** | Covers 700W + margin |

#### Power Rails on Board
| Rail | Source | Used by |
|---|---|---|
| 12V | ATX 24-pin + EPS 8-pin | CPU VRM, GPU PCIe connectors |
| 5V | ATX 24-pin | USB ports, misc ICs |
| 3.3V | ATX 24-pin | M.2 slots, SO-DIMM, logic, RP2040 |
| 1.8V | On-board LDO/buck | DDR4 VTT termination |
| CPU core voltage | On-board VRM | i7-11800H core/uncore |
| 1.1V | RP2040 VREG_VOUT (internal) | RP2040 core |

---

## Board Identity
- **Codename:** Ijr X1 Core
- **Form factor:** Custom (carrier board style, ATX PSU compatible)
- **OS target:** Linux (Ubuntu), Windows compatible
- **Primary use:** Development board, AI inference, custom compute platform
- **Designer:** bismillah
- **Tool:** KiCad 10, headless MCP schematic authoring

---

## Key Decisions Log
| Decision | Choice | Reason |
|---|---|---|
| CPU | Intel i7-11800H | 20× PCIe 4.0 lanes, DDR4 SO-DIMM, TB4, under $100 |
| CPU packaging | BGA soldered | No socket available for mobile BGA |
| RAM | DDR4 SO-DIMM x2 | User replaceable, up to 128GB |
| GPU interface | PCIe 4.0 x8 via M.2 | Modular, user picks GPU |
| GPU power | Dual 6+2 PCIe + ATX | Supports up to RTX 4090 class |
| Power input | ATX 24-pin + EPS 8-pin | Standard, 700W capable, user owns PSU |
| Power budget | 700W | RTX 4090 (450W) + CPU/board + 25% headroom |
| USB-C ports | 3× (PD only, USB2, USB2) | Power + programming + GPIO UART |
| Thunderbolt | TB4 via CPU built-in | No extra chip needed |
| NPU | None | llama.cpp/GGUF runs on CPU/GPU, not NPU |
| ARM vs x86 | x86 | Full app compatibility |
| GPIO controller | RP2040 | Native USB, programmable, 30 GPIO, no bridge chip needed |
