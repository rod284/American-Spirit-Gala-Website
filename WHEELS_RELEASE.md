# Gravitcase — Wheels Release

Release-grade pass for the **wagon-style wheel system**: **back swivel casters** + **front fixed
wheels** (Ø50.8 / 2"), so the train tracks straight when pulled from the back. Governing test:
**SATRA TM248** (5 h rolling road with ridges). Loads per `DESIGN_LOADS.md`; materials per `MATERIALS.md`.

## Architecture
- **Front (×2): fixed wheels** — axle in a rigid fork; track straight.
- **Back (×2): swivel casters** — king-pin + **trailing** wheel; turn to follow the pull.
- Loaded **23 kg → 56 N/wheel static, ~169 N dynamic** (curb/ridge, TM248).

## Structural analysis
| Item | Result | Verdict |
|---|---|---|
| Axle Ø6 shear @169 N | 6 MPa | **SF 33** |
| King-pin Ø8 bending (trail 20 mm) | 67 MPa | **SF 5.9** |
| Fork / yoke | low | robust |

→ **Strength is not the limit — wear & fatigue are.** The release driver is surviving the **5 h
TM248 rolling road** (tread wear, bearing life, swivel smoothness) — a material + test item.

## GD&T (datum **W** = the wheel/axle axis)
| Feature | Callout |
|---|---|
| Wheel OD Ø50.8 | **runout 0.2** to W (roll quality / no wobble) |
| Hub bore / bearing seat | **H7** press for the bearing |
| Axle Ø6 | g6; ⌭ 0.02 |
| King-pin axis (caster) | ⊥ to the mount face 0.1; **trail** set for self-centering |
| Caster mount holes | ⌖ Ø0.3 to the case base |

## BOM
| Item | Spec | Source |
|---|---|---|
| Tread | **TPU** (or rubber) overmold | molder |
| Hub / wheel body | **PA66 / GF-nylon** | molder |
| Bearings | **shielded stainless** ball bearings (×2/wheel) | COTS |
| Axle | **steel**, zinc-plated | COTS |
| King-pin + thrust washer (casters) | steel + PTFE thrust | COTS |
| Fork / caster yoke | **GF-nylon or steel** | molder/fab |

## DFA — assemblable? **Yes**
1. Press the **bearings** into the hub; fit the **tread** (or 2-shot).
2. Axle through the **fork**, retain (circlip/peen).
3. Casters: press the **king-pin + thrust washer** into the yoke; the wheel trails.
4. Bolt the **fixed forks (front)** and **caster yokes (back)** to the case base.
Tool access: all fasteners from the case underside.

## Residual (bench / lab)
- **SATRA TM248** 5 h rolling road (tread wear, bearing life, swivel) — the gating test.
- Bearing **seal/grease** for grit; swivel **self-centering** trail tune.
- Tread compound abrasion + noise.
