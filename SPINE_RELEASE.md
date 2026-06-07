# Gravitcase — Telescoping Spine (Pull-Rod) Release

Release-grade pass (GD&T · FEA · BOM · DFA) for the **5-section telescoping pull-rod** — the
subsystem **QB/T 2155 governs directly** (≥1500 N, <3 mm deflection, ≥3000 cycles). Loads per
`DESIGN_LOADS.md`; materials per `MATERIALS.md`. Analysis: `scripts/fea_spine.py`.

## Architecture
5 stepped **6061-T6 drawn tubes** (OD 50→30, wall 1.2–1.5 mm), ~502 mm extension; each joint
**height-locked** by a sprung Ø3 detent pin seating in the outer tube (released together by the
telescope button). Load path: **grip → tubes → lock pins → core-S5 joint → hub → pivot**.

| Sec | OD | ID | wall | A (mm²) | I (mm⁴) |
|---|---|---|---|---|---|
| 0 (base) | 50 | 37 | 1.5 | 888 | 214 798 |
| 1 | 45 | 32 | 1.5 | 786 | 149 817 |
| 2 | 40 | 27 | 1.3 | 684 | 99 577 |
| 3 | 35 | 22 | 1.3 | 582 | 62 163 |
| 4 (tip) | 30 | 17 | 1.2 | 480 | 35 661 |

## Structural analysis (vs the 1500 N standard)
| Check | Result | Verdict |
|---|---|---|
| Lock-pin **shear** (Ø3, each joint, series) | single 212 MPa **SF 2.4** / double 106 **SF 4.7** | OK (use double-shear engagement) |
| Lock-pin **bearing on the 1.2 mm tube wall** | **417 MPa → SF 1.0** | ⚠ **WEAK — wall yields** |
| **Buckling** (thinnest sec, cantilever) | P_cr 30 kN → **SF 20** | OK |
| **Lateral stiffness** (100 N push) | tip **0.3 mm** | very stiff |
| **<3 mm** deflection (axial 1500 N) | elastic <0.1 mm | governed by **joint slop** |

### ⚠ Finding & fix — lock-hole wall bearing (the same failure the core-S5 joint already solved)
The Ø3 pin bears on the **1.2 mm 6061 wall** at 1500 N → **417 MPa, SF 1.0** (the hole yields/elongates).
**Fix:** a **flanged Ø6/Ø9 steel eyelet** pressed into each lock hole (identical to the core-S5
ferrule scheme): the pin now bears on **steel**, and the **flange face spreads the load on the
aluminium → 42 MPa, SF 9.7**. *Adopt the eyelet at every lock hole.*

## GD&T (datum **S** = the base-tube OD axis)
| Feature | Callout |
|---|---|
| Tube OD per section | hX/g-fit for the telescoping slide; **straightness 0.1/100 mm** (sets the <3 mm) |
| Wall thickness | ±0.1 (buckling + bearing) |
| Lock-hole position (each joint) | ⌖ Ø0.2 to S + the extension datum (height registration — Check #5) |
| Section overlap / engagement | ≥ 1.5×OD engaged at full extension (joint bending) |
| Concentricity section-to-section | 0.15 TIR (wobble / the <3 mm) |

## BOM
| Item | Spec | Source |
|---|---|---|
| Tubes ×5 | **6061-T6 drawn tube**, OD 30/35/40/45/50, wall 1.2–1.5 | drawn-tube mill (near-stock) |
| Lock pins ×4 | **Ø3 spring-loaded detent**, hardened steel | COTS (Vlier/Misumi) |
| **Lock-hole eyelets ×4** | **flanged steel eyelet Ø6/Ø9** (the fix) | turned / COTS shoulder eyelet |
| Slide guides | **POM/PA glide rings** per joint (smooth slide, kill wobble) | molded |
| Telescope button | release links all 4 pins | custom (in the grip) |

## DFA — assemblable? **Yes**
1. Press the **steel eyelet** into each section's lock hole; fit the **detent pin + spring**.
2. Fit the **glide ring** at each section's base.
3. **Nest** sections tip→base (each slides into the next; the detent rides in, clicks at the lock hole).
4. The base tube joins the **core-S5 joint** (twin Ø3.5 dowels — already released).
5. Route the actuation rods up the bore; cap with the **T-handle grip**.
Tool access: detent install before nesting (like the pawl pin pre-drop); button links accessible in the grip.

## Residual (bench / lab)
- **≥3000-cycle** extend/retract fatigue (QB/T 2919) on the lock pins + eyelets.
- Tube **straightness/concentricity lot check** (drives the <3 mm).
- Glide-ring friction tune (slide feel).
