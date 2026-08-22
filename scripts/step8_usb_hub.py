#!/usr/bin/env python3
"""
Step 8 — VL817 USB 3.1 Gen1 Hub
Components: U12 (VL817 stub via Conn_01x48), X1 (12MHz crystal),
            C33–C38 (decoupling), R29 (REXT 27.4k),
            J_USB_A1–J_USB_A4 (USB-A Type-A receptacles)
Net labels use only valid (net_label ...) sexpr — no power_symbol token.
Layout: X=1150-1280, Y=80-200
"""
import re, shutil, uuid, pathlib

SCH = pathlib.Path("/home/bismillah/Downloads/Ijr-X1-Core/Ijr-X1-Core.kicad_sch")
BAK = SCH.with_suffix(".kicad_sch.bak_before_step8_hub")
shutil.copy(SCH, BAK)
print(f"Backup: {BAK}")

text = SCH.read_text()

def uid(): return str(uuid.uuid4())

blocks = []

def net_label(net, x, y, angle=0):
    """Valid KiCad 7+ net_label sexpr"""
    return f"""
  (net_label "{net}"
    (at {x:.2f} {y:.2f} {angle})
    (fields_autoplaced yes)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid "{uid()}")
  )"""

def global_label(net, x, y, angle=0, shape="passive"):
    """Power-style global label for VCC/GND"""
    return f"""
  (global_label "{net}"
    (shape {shape})
    (at {x:.2f} {y:.2f} {angle})
    (fields_autoplaced yes)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid "{uid()}")
  )"""

def symbol(ref, lib_id, x, y, val, fp=""):
    """Place a schematic symbol"""
    return f"""
  (symbol
    (lib_id "{lib_id}")
    (at {x:.2f} {y:.2f} 0)
    (unit 1)
    (in_bom yes) (on_board yes)
    (uuid "{uid()}")
    (property "Reference" "{ref}" (at {x+2:.2f} {y-2:.2f} 0)
      (effects (font (size 1.27 1.27))))
    (property "Value" "{val}" (at {x+2:.2f} {y+2:.2f} 0)
      (effects (font (size 1.27 1.27))))
    (property "Footprint" "{fp}" (at {x:.2f} {y:.2f} 0)
      (effects (font (size 1.27 1.27)) hide))
    (instances (project "Ijr-X1-Core"
      (path "/{uid()}" (reference "{ref}") (unit 1))))
  )"""

# ── Placement coordinates ─────────────────────────────────────
HX, HY   = 1160.0, 120.0   # U12 VL817 hub IC
XX, XY   = 1120.0, 105.0   # X1 crystal
RX, RY   = 1120.0, 140.0   # R29 REXT
# Decoupling caps column at X=1130
CAPS = [
    ("C33", 1130.0,  92.0, "100nF", "Capacitor_SMD:C_0402_1005Metric"),
    ("C34", 1130.0, 100.0, "100nF", "Capacitor_SMD:C_0402_1005Metric"),
    ("C35", 1130.0, 108.0, "100nF", "Capacitor_SMD:C_0402_1005Metric"),
    ("C36", 1130.0, 116.0, "4.7uF", "Capacitor_SMD:C_0402_1005Metric"),
    ("C37", 1130.0, 124.0, "4.7uF", "Capacitor_SMD:C_0402_1005Metric"),
    ("C38", 1130.0, 132.0, "100nF", "Capacitor_SMD:C_0402_1005Metric"),
]
# USB-A ports
UA_X = 1210.0

# ── Place symbols ────────────────────────────────────────────
# U12 — VL817 hub (Conn_01x48 placeholder, 48-pin LQFP footprint)
blocks.append(symbol("U12", "Connector_Generic:Conn_01x48",
                      HX, HY, "VL817",
                      "Package_QFP:LQFP-48_7x7mm_P0.5mm"))

# X1 — 12MHz crystal
blocks.append(symbol("X1", "Device:Crystal",
                      XX, XY, "12MHz",
                      "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm"))

# R29 — REXT 27.4k
blocks.append(symbol("R29", "Device:R",
                      RX, RY, "27.4k",
                      "Resistor_SMD:R_0402_1005Metric"))

# Decoupling caps
for ref, cx, cy, val, fp in CAPS:
    blocks.append(symbol(ref, "Device:C", cx, cy, val, fp))

# 4× USB-A downstream ports
for i in range(1, 5):
    blocks.append(symbol(f"J_USB_A{i}", "Connector_Generic:Conn_01x08",
                         UA_X, 90.0 + (i-1)*25.0,
                         "USB3.1-A",
                         "Connector_USB:USB_A_Molex_105057_Vertical"))

# ── Net labels — hub upstream (connects to existing J2 nets) ─
# USB 2.0 upstream to J2 (J2_DP/J2_DM already exist from Phase 1)
blocks.append(net_label("J2_DP",  HX-5, HY+0.00))
blocks.append(net_label("J2_DM",  HX-5, HY+2.54))
# SuperSpeed upstream — stub nets for CPU wiring in Step 10
blocks.append(net_label("USB_HUB_SS_TX_p", HX-5, HY+5.08))
blocks.append(net_label("USB_HUB_SS_TX_n", HX-5, HY+7.62))
blocks.append(net_label("USB_HUB_SS_RX_p", HX-5, HY+10.16))
blocks.append(net_label("USB_HUB_SS_RX_n", HX-5, HY+12.70))

# Hub downstream port nets (right side of U12 stub)
for port in range(1, 5):
    yo = (port-1)*15.24
    blocks.append(net_label(f"HUB_D{port}_DP",      HX+5, HY+yo+0.00,  180))
    blocks.append(net_label(f"HUB_D{port}_DM",      HX+5, HY+yo+2.54,  180))
    blocks.append(net_label(f"HUB_D{port}_SS_TX_p", HX+5, HY+yo+5.08,  180))
    blocks.append(net_label(f"HUB_D{port}_SS_TX_n", HX+5, HY+yo+7.62,  180))
    blocks.append(net_label(f"HUB_D{port}_SS_RX_p", HX+5, HY+yo+10.16, 180))
    blocks.append(net_label(f"HUB_D{port}_SS_RX_n", HX+5, HY+yo+12.70, 180))

# Crystal labels
blocks.append(net_label("HUB_XTAL_IN",  XX-5, XY))
blocks.append(net_label("HUB_XTAL_OUT", XX+5, XY, 180))

# REXT
blocks.append(net_label("HUB_REXT", RX-5, RY))
blocks.append(global_label("GND",   RX+5, RY, 180))

# Decoupling cap power rails (pin1=+3V3 or +1V8_HUB, pin2=GND)
# Caps are Device:C so pin1 is at (cx, cy-3.81), pin2 at (cx, cy+3.81)
cap_rails = [
    ("C33", "+3V3",    "+3V3"),
    ("C34", "+1V8_HUB", "+1V8_HUB"),
    ("C35", "+3V3",    "+3V3"),
    ("C36", "+3V3",    "+3V3"),
    ("C37", "+1V8_HUB", "+1V8_HUB"),
    ("C38", "+3V3",    "+3V3"),
]
for (ref, top_net, _), (_, cx, cy, *__) in zip(cap_rails, CAPS):
    blocks.append(global_label(top_net, cx, cy-3.81))
    blocks.append(global_label("GND",  cx, cy+3.81, 180))

# USB-A port downstream labels
for i in range(1, 5):
    py = 90.0 + (i-1)*25.0
    # Conn_01x08: pins at (UA_X+5, py + n*2.54) for n=0..7
    blocks.append(net_label(f"HUB_D{i}_DP",      UA_X+5, py+0.00,  180))
    blocks.append(net_label(f"HUB_D{i}_DM",      UA_X+5, py+2.54,  180))
    blocks.append(net_label(f"HUB_D{i}_SS_TX_p", UA_X+5, py+5.08,  180))
    blocks.append(net_label(f"HUB_D{i}_SS_TX_n", UA_X+5, py+7.62,  180))
    blocks.append(net_label(f"HUB_D{i}_SS_RX_p", UA_X+5, py+10.16, 180))
    blocks.append(net_label(f"HUB_D{i}_SS_RX_n", UA_X+5, py+12.70, 180))
    blocks.append(global_label("+5V", UA_X-5, py+15.24))
    blocks.append(global_label("GND", UA_X-5, py+17.78, 180))

# ── Insert before closing paren ───────────────────────────────
insert_at = text.rfind("\n)")
if insert_at == -1:
    print("ERROR: closing paren not found"); exit(1)

new_text = text[:insert_at] + "".join(blocks) + text[insert_at:]

opens  = new_text.count("(")
closes = new_text.count(")")
delta  = opens - closes
print(f"Paren balance: {opens} open, {closes} close, delta={delta}")
if abs(delta) > 20:
    print("WARNING: large imbalance — aborting"); exit(1)

SCH.write_text(new_text)
print(f"Written {len(blocks)} blocks. Done.")
