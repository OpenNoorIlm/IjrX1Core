#!/usr/bin/env python3
"""
Step 8 — VL817 USB 3.1 Hub circuit
Places: U12 (VL817), X1 12MHz crystal, C33-C38 decoupling, R29 REXT,
        J_USB_A1-J_USB_A4 (Type-A receptacles), all net labels.
Hub upstream: USB_HUB_DP/DM → J2 CPU port; USB_HUB_SS_TX/RX → CPU in Step 10.
"""
import re, shutil, uuid, pathlib

SCH = pathlib.Path("/home/bismillah/Downloads/Ijr-X1-Core/Ijr-X1-Core.kicad_sch")
BAK = SCH.with_suffix(".kicad_sch.bak_before_usb_hub")
shutil.copy(SCH, BAK)
print(f"Backup: {BAK}")

text = SCH.read_text()

def uid(): return str(uuid.uuid4())

additions = []

# ---------------------------------------------------------------------------
# Helper: label sexpr
def label(net, x, y, angle=0):
    return f'''
  (label "{net}"
    (at {x} {y} {angle})
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid "{uid()}")
  )'''

# Helper: power symbol
def pwr(net, x, y, angle=0):
    return f'''
  (power_symbol
    (at {x} {y} {angle})
    (lib_id "power:{net}")
    (uuid "{uid()}")
    (property "Reference" "#PWR" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "{net}" (at {x} {y+2.54} 0) (effects (font (size 1.27 1.27))))
    (pin "1" (at {x} {y} {angle}))
  )'''

# Helper: component
def comp(ref, lib, sym, x, y, val="", fp=""):
    fp_str = f'"{fp}"' if fp else '""'
    return f'''
  (symbol
    (lib_id "{lib}:{sym}")
    (at {x} {y} 0)
    (uuid "{uid()}")
    (property "Reference" "{ref}" (at {x+1} {y-1} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "{val if val else sym}" (at {x+1} {y+1} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" {fp_str} (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "Ijr-X1-Core" (path "/{uid()}" (reference "{ref}") (unit 1))))
  )'''

# ---------------------------------------------------------------------------
# Placement layout — below X550 section (X550 is around Y=100-200, X=950-1100)
# USB hub goes at X=1150, Y=100

HUB_X, HUB_Y = 1160, 120   # U12 VL817 center
XTAL_X, XTAL_Y = 1120, 120 # Crystal
# USB-A ports stacked below
UA_X = 1200

# U12: VL817 hub — use Conn placeholder since VL817 not in stock KiCad lib
# Pins: upstream D+/D-, upstream SS TX/RX, 4x downstream D+/D-, SS TX/RX,
#       VDD33, VDD18, GND, REXT, XTAL
# We embed the VL817 as a 48-LQFP using Connector_Generic:Conn_01x48 stub
# with proper net labels connecting everything by name.

additions.append(comp("U12", "Connector_Generic", "Conn_01x48", HUB_X, HUB_Y, "VL817",
                       "Package_QFP:LQFP-48_7x7mm_P0.5mm"))

# Crystal 12MHz for hub
additions.append(comp("X1", "Device", "Crystal", XTAL_X, XTAL_Y, "12MHz",
                       "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm"))

# Decoupling caps: C33-C38
cap_positions = [
    ("C33", 1130, 100, "100nF"),
    ("C34", 1130, 108, "100nF"),
    ("C35", 1130, 116, "100nF"),
    ("C36", 1130, 124, "4.7uF"),
    ("C37", 1130, 132, "4.7uF"),
    ("C38", 1130, 140, "100nF"),
]
for ref, x, y, val in cap_positions:
    additions.append(comp(ref, "Device", "C", x, y, val, "Capacitor_SMD:C_0402_1005Metric"))

# REXT resistor
additions.append(comp("R29", "Device", "R", XTAL_X, 140, "27.4k",
                       "Resistor_SMD:R_0402_1005Metric"))

# 4x USB-A downstream ports
for i in range(1, 5):
    additions.append(comp(f"J_USB_A{i}", "Connector_Generic", "Conn_01x08",
                           UA_X, 100 + (i-1)*25, f"USB3.1-A",
                           "Connector_USB:USB_A_Molex_105057_Vertical"))

# ---------------------------------------------------------------------------
# Net labels — VL817 key signals connected by name to the schematic

# Upstream USB 2.0 (to J2 CPU port via J2_DP/J2_DM nets)
net_labels = [
    # Hub upstream HS (connects to J2)
    ("J2_DP",        HUB_X - 5, HUB_Y + 0,  0),
    ("J2_DM",        HUB_X - 5, HUB_Y + 2.54, 0),
    # Hub upstream SS (to CPU in Step 10)
    ("USB_HUB_SS_TX_p", HUB_X - 5, HUB_Y + 5.08, 0),
    ("USB_HUB_SS_TX_n", HUB_X - 5, HUB_Y + 7.62, 0),
    ("USB_HUB_SS_RX_p", HUB_X - 5, HUB_Y + 10.16, 0),
    ("USB_HUB_SS_RX_n", HUB_X - 5, HUB_Y + 12.70, 0),
    # Hub downstream port 1
    ("HUB_D1_DP", HUB_X + 5, HUB_Y + 0,  180),
    ("HUB_D1_DM", HUB_X + 5, HUB_Y + 2.54, 180),
    ("HUB_D1_SS_TX_p", HUB_X + 5, HUB_Y + 5.08, 180),
    ("HUB_D1_SS_TX_n", HUB_X + 5, HUB_Y + 7.62, 180),
    ("HUB_D1_SS_RX_p", HUB_X + 5, HUB_Y + 10.16, 180),
    ("HUB_D1_SS_RX_n", HUB_X + 5, HUB_Y + 12.70, 180),
    # Hub downstream port 2
    ("HUB_D2_DP", HUB_X + 5, HUB_Y + 15.24, 180),
    ("HUB_D2_DM", HUB_X + 5, HUB_Y + 17.78, 180),
    ("HUB_D2_SS_TX_p", HUB_X + 5, HUB_Y + 20.32, 180),
    ("HUB_D2_SS_TX_n", HUB_X + 5, HUB_Y + 22.86, 180),
    ("HUB_D2_SS_RX_p", HUB_X + 5, HUB_Y + 25.40, 180),
    ("HUB_D2_SS_RX_n", HUB_X + 5, HUB_Y + 27.94, 180),
    # Hub downstream port 3
    ("HUB_D3_DP", HUB_X + 5, HUB_Y + 30.48, 180),
    ("HUB_D3_DM", HUB_X + 5, HUB_Y + 33.02, 180),
    ("HUB_D3_SS_TX_p", HUB_X + 5, HUB_Y + 35.56, 180),
    ("HUB_D3_SS_TX_n", HUB_X + 5, HUB_Y + 38.10, 180),
    ("HUB_D3_SS_RX_p", HUB_X + 5, HUB_Y + 40.64, 180),
    ("HUB_D3_SS_RX_n", HUB_X + 5, HUB_Y + 43.18, 180),
    # Hub downstream port 4
    ("HUB_D4_DP", HUB_X + 5, HUB_Y + 45.72, 180),
    ("HUB_D4_DM", HUB_X + 5, HUB_Y + 48.26, 180),
    ("HUB_D4_SS_TX_p", HUB_X + 5, HUB_Y + 50.80, 180),
    ("HUB_D4_SS_TX_n", HUB_X + 5, HUB_Y + 53.34, 180),
    ("HUB_D4_SS_RX_p", HUB_X + 5, HUB_Y + 55.88, 180),
    ("HUB_D4_SS_RX_n", HUB_X + 5, HUB_Y + 58.42, 180),
]

for net, x, y, ang in net_labels:
    additions.append(label(net, x, y, ang))

# Power on caps and hub IC
pwr_labels = [
    ("+3V3", 1130, 96.19),   # C33 pin1 — VDD33
    ("+1V8_HUB", 1130, 104.19), # C34 — VDD18
    ("+3V3", 1130, 112.19), # C35
    ("+3V3", 1130, 120.19), # C36
    ("+1V8_HUB", 1130, 128.19), # C37
    ("+3V3", 1130, 136.19), # C38
]
for net, x, y in pwr_labels:
    additions.append(label(net, x, y, 0))

# GND on cap pin 2
gnd_labels = [
    (1130, 103.81),
    (1130, 111.81),
    (1130, 119.81),
    (1130, 127.81),
    (1130, 135.81),
    (1130, 143.81),
]
for x, y in gnd_labels:
    additions.append(label("GND", x, y, 0))

# USB-A port downstream labels
for i in range(1, 5):
    port_y = 100 + (i-1)*25
    port_x_right = UA_X + 5
    additions.append(label(f"HUB_D{i}_DP",       port_x_right, port_y+0,    180))
    additions.append(label(f"HUB_D{i}_DM",       port_x_right, port_y+2.54, 180))
    additions.append(label(f"HUB_D{i}_SS_TX_p",  port_x_right, port_y+5.08, 180))
    additions.append(label(f"HUB_D{i}_SS_TX_n",  port_x_right, port_y+7.62, 180))
    additions.append(label(f"HUB_D{i}_SS_RX_p",  port_x_right, port_y+10.16,180))
    additions.append(label(f"HUB_D{i}_SS_RX_n",  port_x_right, port_y+12.70,180))
    additions.append(label("+5V",                 UA_X-5,       port_y+15.24, 0))
    additions.append(label("GND",                 UA_X-5,       port_y+17.78, 0))

# Crystal labels
additions.append(label("HUB_XTAL_IN",  XTAL_X-5, XTAL_Y+0,    0))
additions.append(label("HUB_XTAL_OUT", XTAL_X+5, XTAL_Y+0,    180))

# REXT
additions.append(label("HUB_REXT",  XTAL_X-5, 140, 0))
additions.append(label("GND",       XTAL_X+5, 140, 180))

# ---------------------------------------------------------------------------
# Write additions before closing paren
insert_point = text.rfind("\n)")
if insert_point == -1:
    print("ERROR: could not find closing paren")
    exit(1)

new_text = text[:insert_point] + "".join(additions) + text[insert_point:]

# Verify paren balance
opens  = new_text.count("(")
closes = new_text.count(")")
print(f"Paren balance: {opens} open, {closes} close — delta={opens-closes}")
if abs(opens - closes) > 10:
    print("WARNING: large paren imbalance, check output")

SCH.write_text(new_text)
print(f"Written {len(additions)} additions to {SCH}")
print("Done.")
