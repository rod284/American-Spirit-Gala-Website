# Gravitcase — Tow Hitch Release

Release-grade pass for the **case-to-case tow hitch**: the steel **keyhole receiver** (front
shell) + the **drawbar/ball** (back). Verified functionally by **Check #10** (enter / capture /
snap / hold / release). Tow design load **~1 kN** (dynamic snatch / train; steady tow 100–300 N
per `DESIGN_LOADS.md`). Materials per `MATERIALS.md`.

## Architecture
- **Receiver** (front): steel **keyhole** plate 72×100×3 — funnel + Ø18 entry → Ø9 capture slot
  with a **12° self-lock seat** + a **sprung detent** (the snap). Bolted to the front shell
  (4× M6 → gusseted cored bosses + interior steel backing plate).
- **Drawbar** (back): a pivoting tow bar, **150 mm**, carrying the **Ø16 ball**; height-adjustable;
  deploys to drop the ball into the next case's receiver.

## Structural analysis (~1 kN tow)
| Item | Result | Verdict |
|---|---|---|
| Ball capture (slot ⊥ pull) | 248 mm³ blocked | retained (Check #10) |
| Sprung detent / anti-rise | 46 mm³ block | snaps (Check #10) |
| Steel slot **bearing** | — | **SF 18** |
| Mount bolts ×M6 **shear/tension** | 35 MPa | **SF 8.8** |
| Drawbar **axial** (2-force) | 9 MPa | **SF 29** |
| **Drawbar bending** (OD16, ~30% off-axis) | 144 MPa | **SF 1.9 ← governs** |

### Finding & recommendation — drawbar bending under off-axis tow
The drawbar is near-pure axial when the cases are aligned (SF 29), but **misalignment/turning** puts
a lateral component over the 150 mm length → **SF 1.9** (OD16 6061). **Recommend OD18 6061 tube
(→ SF 2.5) or a steel drawbar (→ SF 4.5).** The receiver/mount/capture all clear with margin; the
drawbar tube is the one to up-spec.

## GD&T (datum **R** = the receiver plate face / ball-seat axis)
| Feature | Callout |
|---|---|
| Entry Ø18 / capture slot 9 | profile 0.1 R; slot width **9 +0.1/0** (ball Ø16 > slot > neck Ø8) |
| 12° self-lock seat | angle **12° ±1°**; bearing face Ra 0.4 (cyclic) |
| Mount bolt pattern (×4) | ⌖ Ø0.2 R |
| Drawbar ball Ø16 | **Ø16 g6** (mates the slot/seat); surface hardened |
| Drawbar pivot + height-lock | pivot ⌭ 0.05; lock-hole ⌖ Ø0.2 |

## BOM
| Item | Spec | Source |
|---|---|---|
| Receiver bracket | **steel** (stamped/machined), keyhole | fab |
| Tow ball Ø16 | **steel, hardened** (trailer-ball style) | COTS |
| Drawbar | **6061-T6 OD18 tube** (or steel) — *up-spec from OD16* | drawn tube |
| Sprung detent | spring + pin (music wire) | COTS |
| Mount bolts ×4 + backing plate | M6 A2-70 + 304 plate | std |
| Drawbar pivot + height-lock | sprung detent pin (steel eyelet — see spine) | COTS |

## DFA — assemblable? **Yes**
1. Bolt the **receiver** into the front shell from inside (backing plate spreads load) — flush mount pad.
2. Fit the **detent** (spring + pin) into the receiver housing.
3. Pivot the **drawbar** into the back of the case; press the **ball** + the height-lock detent.
4. **Connect:** deploy the drawbar, push the ball through the entry hole, **lower into the slot** (12° self-lock), detent snaps. Lift to release.
Tool access: receiver bolts from inside before the shell closes; drawbar pivot from the back.

## Residual (bench / lab)
- **Drawbar up-spec** (OD18 / steel) confirmed by test.
- **Detent spring force** + the 12° self-lock cam (feel) — bench.
- Tow **fatigue / jerk** cycling (the dynamic ~1 kN snatch); refine the snatch magnitude from a real duty cycle.
