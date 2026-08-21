# Ijr-X1-Core — External Library Log Form

> **Purpose:** Track every external symbol, footprint, or 3D model downloaded for this project.
> Fill in one row per file. Claude fills this automatically when downloading with user permission.

---

## Downloads Table

| Date | Source Repo | File Downloaded | Saved As | License | Purpose | Installed In |
|------|-------------|-----------------|----------|---------|---------|--------------|
| 2026-08-21 | [dfdtc/dfdtc_kicad_lib](https://github.com/dfdtc/dfdtc_kicad_lib) | `9.0/symbols/dfdtc_Connector.kicad_sym` | `external-libs/symbols/dfdtc_Connector.kicad_sym` | None stated (public GitHub) | DDR4_SODIMM_CONN260 260-pin SO-DIMM schematic symbol | `sym-lib-table` as `dfdtc_Connector` |
| 2026-08-21 | [dfdtc/dfdtc_kicad_lib](https://github.com/dfdtc/dfdtc_kicad_lib) | `9.0/footprints/dfdtc_connector.pretty/DDR4_SODIMM_CONN260.kicad_mod` | `external-libs/footprints/dfdtc_connector.pretty/DDR4_SODIMM_CONN260.kicad_mod` | None stated (public GitHub) | DDR4 SO-DIMM 260-pin footprint, 4.0mm height (TE 2309407-1 compatible) | `fp-lib-table` as `dfdtc_connector` |
| 2026-08-21 | [futureshocked/kicad_latte_panda_mu](https://github.com/futureshocked/kicad_latte_panda_mu) | `Libraries/A_HDJ_Library.pretty/DDR4_SODIMM_260P_8.0H_STD.kicad_mod` | `external-libs/footprints/dfdtc_connector.pretty/DDR4_SODIMM_260P_8.0H_STD.kicad_mod` | None stated (public educational project) | DDR4 SO-DIMM 260-pin footprint, 8.0mm height variant (backup) | `fp-lib-table` as `dfdtc_connector` |

---

## Notes

### Why these sources?
- **dfdtc_kicad_lib** — Only public KiCad v9-native DDR4 SO-DIMM 260-pin symbol found with correct 260 pins in a multi-unit symbol format. Verified: `DDR4_SODIMM_CONN260` has exactly 260 pins, 6 sub-units.
- **futureshocked/kicad_latte_panda_mu** — LattePanda Mu reference SBC design, same class of board as Ijr-X1-Core. Footprint verified KiCad v8 format, 2059 lines, locked production footprint.

### License notes
Neither source has an explicit LICENSE file. Both are public GitHub repositories used by the open-source hardware community. Files are used in good faith for open-source hardware design. If a license concern is identified, replacements should be sourced from:
- SnapEDA (free download with account): https://www.snapeda.com/parts/2309409-1/TE%20Connectivity/
- Ultra Librarian: https://app.ultralibrarian.com/details/fb52a18c-103e-11e9-ab3a-0a3560a4cccc/
- KiCad official (once merged — see MR !3928): https://gitlab.com/kicad/libraries/kicad-footprints/-/merge_requests/3928

### Physical part (recommended)
**TE Connectivity 2309407-1** — DDR4 SO-DIMM 260-pin socket, 4.0mm height, standard orientation
- Mouser: https://www.mouser.com/ProductDetail/TE-Connectivity/2309407-1
- Alternate 5.2mm height: TE 2309409-1

---

## Template (for future additions)

```
| YYYY-MM-DD | [author/repo](URL) | `path/to/file` | `external-libs/...` | LICENSE | Purpose | Where registered |
```
