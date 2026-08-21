#!/usr/bin/env python3
"""
Step 8 — Intel X550-AT 10GbE Ethernet circuit
Batch-inserts all symbols and net labels into Ijr-X1-Core.kicad_sch
"""
import uuid, shutil, sys
from pathlib import Path

SCH = Path("/home/bismillah/Downloads/Ijr-X1-Core/Ijr-X1-Core.kicad_sch")
BAK = SCH.with_suffix(".kicad_sch.bak_before_x550")

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

additions = []

# ── SPI Flash U9 (W25Q32 for X550-AT firmware) ──────────────────────────────
flash_x, flash_y = 1050, 155
additions.append(make_symbol("Memory_Flash", "W25Q16JVSSIQ", "U9", "W25Q32JV_ETH", flash_x, flash_y))
lx, rx = flash_x - 7.62, flash_x + 7.62
for net, px, py, ang in [
    ("ETH_FL_CS_N",   lx, flash_y-5.08, 0),
    ("ETH_FL_DO",     lx, flash_y-2.54, 0),
    ("ETH_FL_WP_N",   lx, flash_y,      0),
    ("GND",           lx, flash_y+2.54, 0),
    ("ETH_FL_DI",     rx, flash_y-5.08, 180),
    ("ETH_FL_CLK",    rx, flash_y-2.54, 180),
    ("ETH_FL_HOLD_N", rx, flash_y,      180),
    ("+3V3",          rx, flash_y+2.54, 180),
]:
    additions.append(make_label(net, px, py, ang))

# C28: U9 decoupling cap
additions.append(make_symbol("Device", "C", "C28", "100nF", flash_x+20, flash_y))
additions += [make_label("+3V3", flash_x+20, flash_y-3.81, 270),
              make_label("GND",  flash_x+20, flash_y+3.81, 90)]

# ── 1.0V LDO U10 (VCCP for X550-AT) ────────────────────────────────────────
ldo1_x, ldo1_y = 1100, 155
additions.append(make_symbol("Device", "Regulator_Linear", "U10", "AP7361C-10E", ldo1_x, ldo1_y))
additions += [make_label("+3V3",     ldo1_x-5.08, ldo1_y, 0),
              make_label("+1V0_ETH", ldo1_x+5.08, ldo1_y, 180),
              make_label("GND",      ldo1_x,      ldo1_y+5.08, 90)]
for i, (net, dx) in enumerate([("+3V3", ldo1_x-15), ("+1V0_ETH", ldo1_x+15)]):
    additions.append(make_symbol("Device", "C", f"C{29+i}", "10uF", dx, ldo1_y))
    additions += [make_label(net, dx, ldo1_y-3.81, 270), make_label("GND", dx, ldo1_y+3.81, 90)]

# ── 1.8V LDO U11 (VCCIO for X550-AT) ───────────────────────────────────────
ldo2_x, ldo2_y = 1100, 175
additions.append(make_symbol("Device", "Regulator_Linear", "U11", "AP7361C-18E", ldo2_x, ldo2_y))
additions += [make_label("+3V3",     ldo2_x-5.08, ldo2_y, 0),
              make_label("+1V8_ETH", ldo2_x+5.08, ldo2_y, 180),
              make_label("GND",      ldo2_x,      ldo2_y+5.08, 90)]
for i, (net, dx) in enumerate([("+3V3", ldo2_x-15), ("+1V8_ETH", ldo2_x+15)]):
    additions.append(make_symbol("Device", "C", f"C{31+i}", "10uF", dx, ldo2_y))
    additions += [make_label(net, dx, ldo2_y-3.81, 270), make_label("GND", dx, ldo2_y+3.81, 90)]

# ── RJ45 connector J_RJ45 ────────────────────────────────────────────────────
rj45_x, rj45_y = 1050, 220
additions.append(make_symbol("Connector", "RJ45", "J_RJ45", "10GBASE-T+Magnetics", rj45_x, rj45_y))
rj45_lx = rj45_x - 5.08
for i, net in enumerate(["ETH_MDI0_p","ETH_MDI0_n","ETH_MDI1_p","ETH_MDI1_n",
                          "ETH_MDI2_p","ETH_MDI2_n","ETH_MDI3_p","ETH_MDI3_n"]):
    additions.append(make_label(net, rj45_lx, rj45_y-8.89+i*2.54, 0))

# ── PCIe x4 signals from CPU to X550-AT ─────────────────────────────────────
eth_x, eth_y = 1140, 155
for i in range(4):
    additions += [make_label(f"ETH_PET{i}_p", eth_x, eth_y+i*5.08,         0),
                  make_label(f"ETH_PET{i}_n", eth_x, eth_y+i*5.08+2.54,    0),
                  make_label(f"ETH_PER{i}_p", eth_x, eth_y+25+i*5.08,      0),
                  make_label(f"ETH_PER{i}_n", eth_x, eth_y+25+i*5.08+2.54, 0)]

ctrl_y = eth_y + 50
for net in ["ETH_REFCLK_p","ETH_REFCLK_n","ETH_PERST_N","ETH_WAKE_N"]:
    additions.append(make_label(net, eth_x, ctrl_y, 0)); ctrl_y += 2.54

mdi_y = ctrl_y + 5
for i in range(4):
    additions += [make_label(f"ETH_MDI{i}_p", eth_x, mdi_y+i*5.08,      0),
                  make_label(f"ETH_MDI{i}_n", eth_x, mdi_y+i*5.08+2.54, 0)]

spi_y = mdi_y + 25
for net in ["ETH_FL_CS_N","ETH_FL_CLK","ETH_FL_DI","ETH_FL_DO","ETH_FL_WP_N","ETH_FL_HOLD_N"]:
    additions.append(make_label(net, eth_x, spi_y, 0)); spi_y += 2.54

pwr_y = spi_y + 5
for net in ["+1V0_ETH","+1V8_ETH","+3V3","+5VSB","ETH_LAN_PWR_GOOD"]:
    additions.append(make_label(net, eth_x, pwr_y, 0)); pwr_y += 2.54

# ── LAN_PWR_GOOD pull-up R28 ─────────────────────────────────────────────────
lpg_x, lpg_y = 1160, 170
additions.append(make_symbol("Device", "R", "R28", "100k", lpg_x, lpg_y))
additions += [make_label("+3V3",              lpg_x, lpg_y-3.81, 270),
              make_label("ETH_LAN_PWR_GOOD",  lpg_x, lpg_y+3.81, 90)]

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
