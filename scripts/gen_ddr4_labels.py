# JEDEC DDR4 260-pin SO-DIMM pin assignment table (Table 5, DDR4 SDRAM SO-DIMM Design Spec)
# Source cross-checked against Silicon Power Industrial DDR4 SODIMM datasheet Rev 1.3
DDR4_PINMAP = {
1:"VSS",2:"VSS",3:"DQ5",4:"DQ4",5:"VSS",6:"VSS",7:"DQ1",8:"DQ0",9:"VSS",10:"VSS",
11:"DQS0_c",12:"DM0_n_DBI0_n",13:"DQS0_t",14:"VSS",15:"VSS",16:"DQ6",17:"DQ7",18:"VSS",19:"VSS",20:"DQ2",
21:"DQ3",22:"VSS",23:"VSS",24:"DQ12",25:"DQ13",26:"VSS",27:"VSS",28:"DQ8",29:"DQ9",30:"VSS",
31:"VSS",32:"DQS1_c",33:"DM1_n_DBI1_n",34:"DQS1_t",35:"VSS",36:"VSS",37:"DQ15",38:"DQ14",39:"VSS",40:"VSS",
41:"DQ10",42:"DQ11",43:"VSS",44:"VSS",45:"DQ21",46:"DQ20",47:"VSS",48:"VSS",49:"DQ17",50:"DQ16",
51:"VSS",52:"VSS",53:"DQS2_c",54:"DM2_n_DBI2_n",55:"DQS2_t",56:"VSS",57:"VSS",58:"DQ22",59:"DQ23",60:"VSS",
61:"VSS",62:"DQ18",63:"DQ19",64:"VSS",65:"VSS",66:"DQ28",67:"DQ29",68:"VSS",69:"VSS",70:"DQ24",
71:"DQ25",72:"VSS",73:"VSS",74:"DQS3_c",75:"DM3_n_DBI3_n",76:"DQS3_t",77:"VSS",78:"VSS",79:"DQ30",80:"DQ31",
81:"VSS",82:"VSS",83:"DQ26",84:"DQ27",85:"VSS",86:"VSS",87:"CB5_NC",88:"CB4_NC",89:"VSS",90:"VSS",
91:"CB1_NC",92:"CB0_NC",93:"VSS",94:"VSS",95:"DQS8_c",96:"DM8_n_DBI_n_NC",97:"DQS8_t",98:"VSS",99:"VSS",100:"CB6_NC",
101:"CB2_NC",102:"VSS",103:"VSS",104:"CB7_NC",105:"CB3_NC",106:"VSS",107:"VSS",108:"RESET_n",109:"CKE0",110:"CKE1_NC",
111:"VDD",112:"VDD",113:"BG1",114:"ACT_n",115:"BG0",116:"ALERT_n",117:"VDD",118:"VDD",119:"A12",120:"A11",
121:"A9",122:"A7",123:"VDD",124:"VDD",125:"A8",126:"A5",127:"A6",128:"A4",129:"VDD",130:"VDD",
131:"A3",132:"A2",133:"A1",134:"EVENT_n_NF",135:"VDD",136:"VDD",137:"CK0_t",138:"CK1_t_NF",139:"CK0_c",140:"CK1_c_NF",
141:"VDD",142:"VDD",143:"PARITY",144:"A0",145:"BA1",146:"A10_AP",147:"VDD",148:"VDD",149:"CS0_n",150:"BA0",
151:"WE_n_A14",152:"RAS_n_A16",153:"VDD",154:"VDD",155:"ODT0",156:"CAS_n_A15",157:"CS1_n_NC",158:"A13",159:"VDD",160:"VDD",
161:"ODT1_NC",162:"C0_CS2_n_NC",163:"VDD",164:"VREFCA",165:"C1_CS3_n_NC",166:"SA2",167:"VSS",168:"VSS",169:"DQ37",170:"DQ36",
171:"VSS",172:"VSS",173:"DQ33",174:"DQ32",175:"VSS",176:"VSS",177:"DQS4_c",178:"DM4_n_DBI4_n",179:"DQS4_t",180:"VSS",
181:"VSS",182:"DQ39",183:"DQ38",184:"VSS",185:"VSS",186:"DQ35",187:"DQ34",188:"VSS",189:"VSS",190:"DQ45",
191:"DQ44",192:"VSS",193:"VSS",194:"DQ41",195:"DQ40",196:"VSS",197:"VSS",198:"DQS5_c",199:"DM5_n_DBI5_n",200:"DQS5_t",
201:"VSS",202:"VSS",203:"DQ46",204:"DQ47",205:"VSS",206:"VSS",207:"DQ42",208:"DQ43",209:"VSS",210:"VSS",
211:"DQ52",212:"DQ53",213:"VSS",214:"VSS",215:"DQ49",216:"DQ48",217:"VSS",218:"VSS",219:"DQS6_c",220:"DM6_n_DBI6_n",
221:"DQS6_t",222:"VSS",223:"VSS",224:"DQ54",225:"DQ55",226:"VSS",227:"VSS",228:"DQ50",229:"DQ51",230:"VSS",
231:"VSS",232:"DQ60",233:"DQ61",234:"VSS",235:"VSS",236:"DQ57",237:"DQ56",238:"VSS",239:"VSS",240:"DQS7_c",
241:"DM7_n_DBI7_n",242:"DQS7_t",243:"VSS",244:"VSS",245:"DQ62",246:"DQ63",247:"VSS",248:"VSS",249:"DQ58",250:"DQ59",
251:"VSS",252:"VSS",253:"SCL",254:"SDA",255:"VDDSPD",256:"SA0",257:"VPP",258:"VTT",259:"VPP",260:"SA1",
}
assert len(DDR4_PINMAP) == 260
assert sorted(DDR4_PINMAP.keys()) == list(range(1,261))

import uuid

def gen_uuid():
    return str(uuid.uuid4())

def net_name_for(dimm_tag, pin_num, sig):
    if sig == "VSS":
        return "GND"
    if sig == "VDD":
        return "VDD_DDR4"
    if sig == "VPP":
        return "VPP_DDR4"
    if sig == "VTT":
        return "VTT_DDR4"
    if sig == "VDDSPD":
        return "VDDSPD_DDR4"
    if sig == "VREFCA":
        return f"VREFCA_{dimm_tag}"
    if sig == "SCL":
        return "SCL_SPD"
    if sig == "SDA":
        return "SDA_SPD"
    if sig in ("SA0","SA1","SA2"):
        return f"{sig}_{dimm_tag}"
    return f"{sig}_{dimm_tag}"

def unit_pin_range(unit):
    starts = {1:1, 2:45, 3:89, 4:133, 5:177, 6:221}
    ends   = {1:44, 2:88, 3:132, 4:176, 5:220, 6:260}
    return starts[unit], ends[unit]

def build_symbol_block(lib_id, ref, unit, origin_x, origin_y, value, project_uuid_path):
    u = gen_uuid()
    return f'''\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {origin_x:.2f} {origin_y:.2f} 0)
\t\t(unit {unit})
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{u}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {origin_x:.2f} {origin_y-3.81:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at {origin_x:.2f} {origin_y+3.81:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {origin_x:.2f} {origin_y:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {origin_x:.2f} {origin_y:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(instances
\t\t\t(project "Ijr-X1-Core"
\t\t\t\t(path "{project_uuid_path}"
\t\t\t\t\t(reference "{ref}") (unit {unit})
\t\t\t\t)
\t\t\t)
\t\t)
\t)
'''

def build_label_block(net_name, x, y, angle=0):
    u = gen_uuid()
    return f'''\t(label "{net_name}"
\t\t(at {x:.2f} {y:.2f} {angle})
\t\t(effects (font (size 1.016 1.016)) (justify left))
\t\t(uuid "{u}")
\t)
'''

def build_gnd_power_block(x, y, project_uuid_path):
    u = gen_uuid()
    ref = f"#PWR{u[:4]}"
    return f'''\t(symbol
\t\t(lib_id "power:GND")
\t\t(at {x:.2f} {y:.2f} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{u}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x:.2f} {y+6.35:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Value" "GND"
\t\t\t(at {x:.2f} {y+5.08:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x:.2f} {y:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x:.2f} {y:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(instances
\t\t\t(project "Ijr-X1-Core"
\t\t\t\t(path "{project_uuid_path}"
\t\t\t\t\t(reference "{ref}") (unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)
'''

def main():
    sch_path = "/home/bismillah/Downloads/Ijr-X1-Core/Ijr-X1-Core.kicad_sch"
    project_uuid_path = "/0a8e2d86-540d-4bc7-908e-89ff2a8b35b6"

    with open(sch_path, "r") as f:
        data = f.read()

    dimms = [
        ("J_DIMM1", "D1", 459.74, 100.33),
        ("J_DIMM2", "D2", 580.39, 100.33),
    ]

    UNIT_Y_SPACING = 130.0

    new_symbol_blocks = []
    new_label_blocks = []
    new_power_blocks = []

    stats = {"labels":0, "gnd":0, "symbols":0}

    for ref, tag, base_x, unit1_y in dimms:
        for unit in range(1, 7):
            unit_origin_y = unit1_y + (unit - 1) * UNIT_Y_SPACING
            if unit != 1:
                block = build_symbol_block(
                    "dfdtc_Connector:DDR4_SODIMM_CONN260",
                    ref, unit, base_x, unit_origin_y,
                    "DDR4_SO-DIMM_260", project_uuid_path
                )
                new_symbol_blocks.append(block)
                stats["symbols"] += 1

            start, end = unit_pin_range(unit)
            for pin_num in range(start, end + 1):
                sig = DDR4_PINMAP[pin_num]
                local_i = pin_num - start
                px = base_x
                py = unit_origin_y + 2.54 * local_i

                if sig == "VSS":
                    new_power_blocks.append(build_gnd_power_block(px, py, project_uuid_path))
                    stats["gnd"] += 1
                else:
                    net_name = net_name_for(tag, pin_num, sig)
                    new_label_blocks.append(build_label_block(net_name, px, py, angle=0))
                    stats["labels"] += 1

    insertion = "".join(new_symbol_blocks) + "".join(new_power_blocks) + "".join(new_label_blocks)

    assert data.rstrip().endswith(")")
    idx = data.rstrip().rfind(")")
    new_data = data.rstrip()[:idx] + insertion + ")\n"

    with open(sch_path, "w") as f:
        f.write(new_data)

    print("Inserted:", stats)
    print("New file size:", len(new_data))

if __name__ == "__main__":
    main()
