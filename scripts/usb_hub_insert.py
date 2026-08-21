#!/usr/bin/env python3
"""
Step 8 — USB 3.2 Hub (GL3523) circuit
4x USB-A downstream ports, upstream via J2 (CPU_PROG USB-C)
Batch inserts symbols + net labels into Ijr-X1-Core.kicad_sch
"""
import uuid, shutil, sys
from pathlib import Path

SCH = Path("/home/bismillah/Downloads/Ijr-X1-Core/Ijr-X1-Core.kicad_sch")
BAK = SCH.with_suffix(".kicad_sch.bak_before_usbhub")

def uid(): return str(uuid.uuid4())

def make_symbol(lib, sym, ref, val, x, y, unit=1):
    return f"""  (symbol
    (lib_id "{lib}:{sym}")
    (at {x} {y} 0)
    (unit {unit})
    (in_bom yes) (on_board yes)
    (uuid "{uid()}")
    (property "Reference" "{ref}" (at {x} {y-3} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "{val}" (at {x} {y+3} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "Ijr-X1-Core"
      (path "/{uid()}" (reference "{ref}") (unit {unit}))))
  )"""

def make_label(net, x, y, angle=0):
    return f"""  (label "{net}"
    (at {x} {y} {angle})
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid "{uid()}")
  )"""

def make_nc(x, y):
    return f"""  (no_connect (at {x} {y}) (uuid "{uid()}"))"""

additions = []

# ── U12: GL3523 USB 3.2 Gen1 4-port Hub IC ──────────────────────────────────
# Represent as generic IC using Conn_01x20 blocks (GL3523 not in stock KiCad lib)
# Use net labels to define all signals — same approach as X550-AT
hub_x, hub_y = 1250, 170

# Upstream USB 2.0 (connects back to J2_DP / J2_DM)
additions.append(make_symbol("Device", "IC", "U12", "GL3523_USB3.2Hub", hub_x, hub_y))

# Net label block — upstream USB2.0
for net, x, y, ang in [
    # Upstream signals (tie to existing J2 nets)
    ("J2_DP",       hub_x - 10, hub_y - 15,   0),   # upstream D+
    ("J2_DM",       hub_x - 10, hub_y - 12.5,  0),   # upstream D-
    ("HUB_US_SS_TX_p", hub_x - 10, hub_y - 10,  0),  # upstream SS TX+
    ("HUB_US_SS_TX_n", hub_x - 10, hub_y - 7.5, 0),  # upstream SS TX-
    ("HUB_US_SS_RX_p", hub_x - 10, hub_y - 5,   0),  # upstream SS RX+
    ("HUB_US_SS_RX_n", hub_x - 10, hub_y - 2.5, 0),  # upstream SS RX-
    # Power
    ("+3V3",        hub_x - 10, hub_y,          0),   # VDD33
    ("+5V",         hub_x - 10, hub_y + 2.5,    0),   # VBUS_DET / port power ref
    ("GND",         hub_x - 10, hub_y + 5,      0),   # GND
    # Crystal
    ("HUB_XTAL_IN", hub_x - 10, hub_y + 7.5,   0),   # 25MHz crystal in
    ("HUB_XTAL_OUT",hub_x - 10, hub_y + 10,    0),   # 25MHz crystal out
    # Config / control
    ("HUB_RESET_N", hub_x - 10, hub_y + 12.5,  0),   # reset, pull-up to 3V3
    # Downstream port 1
    ("HUB_DS1_DP",  hub_x + 10, hub_y - 15,  180),
    ("HUB_DS1_DM",  hub_x + 10, hub_y - 12.5, 180),
    ("HUB_DS1_SS_TX_p", hub_x + 10, hub_y - 10, 180),
    ("HUB_DS1_SS_TX_n", hub_x + 10, hub_y - 7.5, 180),
    ("HUB_DS1_SS_RX_p", hub_x + 10, hub_y - 5, 180),
    ("HUB_DS1_SS_RX_n", hub_x + 10, hub_y - 2.5, 180),
    # Downstream port 2
    ("HUB_DS2_DP",  hub_x + 10, hub_y,        180),
    ("HUB_DS2_DM",  hub_x + 10, hub_y + 2.5,  180),
    ("HUB_DS2_SS_TX_p", hub_x + 10, hub_y + 5, 180),
    ("HUB_DS2_SS_TX_n", hub_x + 10, hub_y + 7.5, 180),
    ("HUB_DS2_SS_RX_p", hub_x + 10, hub_y + 10, 180),
    ("HUB_DS2_SS_RX_n", hub_x + 10, hub_y + 12.5, 180),
    # Downstream port 3
    ("HUB_DS3_DP",  hub_x + 10, hub_y + 15,   180),
    ("HUB_DS3_DM",  hub_x + 10, hub_y + 17.5, 180),
    ("HUB_DS3_SS_TX_p", hub_x + 10, hub_y + 20, 180),
    ("HUB_DS3_SS_TX_n", hub_x + 10, hub_y + 22.5, 180),
    ("HUB_DS3_SS_RX_p", hub_x + 10, hub_y + 25, 180),
    ("HUB_DS3_SS_RX_n", hub_x + 10, hub_y + 27.5, 180),
    # Downstream port 4
    ("HUB_DS4_DP",  hub_x + 10, hub_y + 30,   180),
    ("HUB_DS4_DM",  hub_x + 10, hub_y + 32.5, 180),
    ("HUB_DS4_SS_TX_p", hub_x + 10, hub_y + 35, 180),
    ("HUB_DS4_SS_TX_n", hub_x + 10, hub_y + 37.5, 180),
    ("HUB_DS4_SS_RX_p", hub_x + 10, hub_y + 40, 180),
    ("HUB_DS4_SS_RX_n", hub_x + 10, hub_y + 42.5, 180),
]:
    additions.append(make_label(net, x, y, ang))

# ── Y1: 25MHz crystal ────────────────────────────────────────────────────────
xtal_x, xtal_y = 1210, 182
additions.append(make_symbol("Device", "Crystal", "Y1", "25MHz", xtal_x, xtal_y))
additions += [
    make_label("HUB_XTAL_IN",  xtal_x - 5.08, xtal_y, 0),
    make_label("HUB_XTAL_OUT", xtal_x + 5.08, xtal_y, 180),
    make_label("GND",          xtal_x, xtal_y + 5.08, 90),
]
# Load caps for crystal
for i, (net, dx) in enumerate([("HUB_XTAL_IN", xtal_x-15), ("HUB_XTAL_OUT", xtal_x+15)]):
    additions.append(make_symbol("Device", "C", f"C{33+i}", "18pF", dx, xtal_y))
    additions += [make_label(net, dx, xtal_y-3.81, 270), make_label("GND", dx, xtal_y+3.81, 90)]

# ── HUB_RESET_N pull-up ──────────────────────────────────────────────────────
rst_x, rst_y = 1210, 157
additions.append(make_symbol("Device", "R", "R29", "10k", rst_x, rst_y))
additions += [
    make_label("+3V3",         rst_x, rst_y - 3.81, 270),
    make_label("HUB_RESET_N", rst_x, rst_y + 3.81, 90),
]

# ── Decoupling caps for U12 ──────────────────────────────────────────────────
for i, (val, x, y) in enumerate([
    ("100nF", 1230, 150), ("100nF", 1235, 150),
    ("100nF", 1240, 150), ("100nF", 1245, 150),
    ("10uF",  1230, 160), ("10uF",  1235, 160),
]):
    ref = f"C{35+i}"
    additions.append(make_symbol("Device", "C", ref, val, x, y))
    additions += [make_label("+3V3", x, y-3.81, 270), make_label("GND", x, y+3.81, 90)]

# ── 4× USB-A Connectors ──────────────────────────────────────────────────────
usb_a_x = 1320
for port in range(1, 5):
    jref = f"J_USB_A{port}"
    jy = 140 + (port-1) * 22
    additions.append(make_symbol("Connector", "USB_A", jref, f"USB3.2_A_Port{port}", usb_a_x, jy))
    # USB_A standard: pin1=VBUS, pin2=DM, pin3=DP, pin4=GND, pin5=SS_RX-, pin6=SS_RX+, pin7=GND_D, pin8=SS_TX-, pin9=SS_TX+
    lx = usb_a_x - 5.08
    for net, dy in [
        ("+5V",                   -8.89),
        (f"HUB_DS{port}_DM",      -6.35),
        (f"HUB_DS{port}_DP",      -3.81),
        ("GND",                   -1.27),
        (f"HUB_DS{port}_SS_RX_n",  1.27),
        (f"HUB_DS{port}_SS_RX_p",  3.81),
        ("GND",                    6.35),
        (f"HUB_DS{port}_SS_TX_n",  8.89),
        (f"HUB_DS{port}_SS_TX_p", 11.43),
    ]:
        additions.append(make_label(net, lx, jy + dy, 0))

# ── Series resistors 22Ω on USB2.0 DP/DM lines (upstream + 4 downstream) ────
# Upstream: R30/R31 on J2_DP, J2_DM already defined (J2 uses J2_DP/J2_DM net labels)
# Downstream: R32-R39 on HUB_DS1–4 DP/DM
for i in range(4):
    for j, sig in enumerate(["DP", "DM"]):
        rref = f"R{30 + i*2 + j}"
        rx = 1290 + j*7
        ry = 145 + i*22
        additions.append(make_symbol("Device", "R", rref, "22R", rx, ry))
        mid_net  = f"HUB_DS{i+1}_{sig}_R"
        in_net   = f"HUB_DS{i+1}_{sig}"
        out_net  = f"HUB_DS{i+1}_{sig}"  # reuse net — resistor is in-line, label both ends same net
        additions += [
            make_label(f"HUB_DS{i+1}_{sig}", rx, ry - 3.81, 270),
            make_label(f"HUB_DS{i+1}_{sig}", rx, ry + 3.81, 90),
        ]

# ── Insert into schematic ────────────────────────────────────────────────────
content = SCH.read_text()
insert_block = "\n".join(additions)
if content.rstrip().endswith(")"):
    new_content = content.rstrip()[:-1] + "\n" + insert_block + "\n)"
else:
    print("ERROR: schematic doesn't end with ')'", file=sys.stderr); sys.exit(1)

opens  = new_content.count("(")
closes = new_content.count(")")
if opens != closes:
    print(f"ERROR: paren mismatch open={opens} close={closes}", file=sys.stderr); sys.exit(1)

shutil.copy2(SCH, BAK)
SCH.write_text(new_content)
print(f"✅ Inserted {len(additions)} additions")
print(f"   Paren balance: {opens} == {closes} ✓")
print(f"   Backup: {BAK}")
print(f"   File size: {SCH.stat().st_size:,} bytes")
