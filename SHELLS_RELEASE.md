# Gravitcase — Case Shells Release

Release-grade pass for the **two molded shells** (BACK = core side, FRONT = packing) that **zip
together**. Governing test: **SATRA TM242** (8-corner drop). Material **polycarbonate (PC)** for
impact (`MATERIALS.md`). Envelope 343 W × 508 H × 228.6 D mm; wall 3 mm; edge **R14**; draft 1.5°.

## Architecture
Two injection-molded **PC** half-shells, **9" deep total** (~4" each + the 1" zipper land), joined
by a perimeter zipper at mid-depth. **BACK** carries the molded core recesses + the **tow-impact
rib network** + the **steel pivot-mount pad**. **FRONT** carries the **tow-ball receiver** + its
rib frame. Rounded R14 edges, 1.5° draft, uniform 3 mm wall + 1.5 mm ribs (IM rule).

## Analysis — impact, not stress
| Item | Result | Verdict |
|---|---|---|
| **TM242 corner drop** (23 kg, ~1 m) | ~226 J at a corner | **PC ductility + R14 + ribs absorb** (material/test) |
| Wall + rib stiffness | 3 mm PC, 1.5 mm ribs @ ~95–100 mm pitch | resists oil-can / panel buckling |
| Back rib network (tow impact) | radiating + perimeter + pivot diagonals | spreads tow + pad load to corners/wheels |
| Pivot mount pad | steel inlay, flush | joint load → ribs (analyzed, SF 4.3 frame) |

→ The corner drop is an **impact/material event** — the design levers are **PC toughness, the R14
corner radius, the draft, and the rib layout**; final proof is the physical TM242 drop, not hand-calc.

## GD&T (datum **C** = the parting plane + two corner datums)
| Feature | Callout |
|---|---|
| Outer profile | profile **0.8** to C (cosmetic + fit) |
| Wall thickness | **3 ±0.3** (uniform — sink/warp control) |
| Edge radius | **R14** (impact); draft **1.5°** all outer walls |
| Zipper land (perimeter) | flatness **0.5**; width to the coil + tape |
| Mount-pad pocket / receiver pocket | ⌖ Ø0.3 to C (steel inlays) |
| Shell-to-shell mating | gap ≤ 0.5 along the zipper |

## BOM
| Item | Spec | Source |
|---|---|---|
| Shells ×2 | **Polycarbonate** (PC/ABS or PP = cost options), injection-molded | molder |
| Zipper | **nylon coil + tape**, perimeter | soft-goods |
| Corner bumpers (optional) | TPU overmold at the 8 corners (drop) | molder |
| Steel inlays | pivot mount pad (304) + receiver bracket (steel) | fab |
| Lining / dividers | fabric / foam | soft-goods |

## DFA — assemblable? **Yes**
1. **Mold** both PC shells (cored, ribbed, R14, drafted).
2. **Inlay** the steel mount pad (back) + receiver (front); bolt the bracket / receiver.
3. Install the **pivot assembly** (back) and **drawbar** (back); **wheels** to the base.
4. Sew/attach the **zipper** to each shell perimeter; fit lining.
5. **Zip** the two shells together — the product.
Mold draft + R14 ensure clean ejection; uniform wall avoids sink at the ribs/pads.

## Residual (bench / lab)
- **SATRA TM242** 8-corner drop (the gating test) on the filled case.
- PC **impact coupon** (Izod/Charpy) + the molded-corner section.
- **Zipper strength** + the shell-to-shell seal; **wall oil-can** under squeeze.
- Mold-flow / warp study on the 3 mm PC walls + ribs.
