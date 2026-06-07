# Gravitcase — Material Selection & Rationale

Every material is now **selected with a documented rationale** (load = standard-derived per
`DESIGN_LOADS.md`; environment = consumer luggage: humidity, −20…60 °C, impact, some corrosion;
process keyed to volume; cost-aware). `[PROV]` flags are resolved. **Residual = coupon/lot
validation** (tensile, hardness, impact) on the production lot — a lab step, not CAD.

## Selection drivers
Luggage duty: **light** (every gram matters), **impact-tough** (drop tests), **corrosion-OK**
(travel, humidity), **fatigue** (≥3000 cycles), **moldable/castable at volume**, **low cost**.

## Structural metals (the load path)

| Part | **Material / process** | Rationale (load @1500 N standard) | Margin |
|---|---|---|---|
| **Pawl** | **17-4PH MIM H900** (machined 4140 proto) | net-shape complex latch, hard cyclic wear face, σy 1170 | SF 11 (FEA) |
| **Abutment insert** | **4140 QT ~40 HRC** (or 17-4PH) | cyclic bearing stop, high bending, needs σy ~1000 | SF 3.8 |
| **Pivot shaft** | **4140 alloy steel QT, zinc-plated** (was 17-4PH — over-spec; internal, no corrosion) — *or stock 12.9 M10 shoulder screw* | bending strength, cost; stainless unnecessary inside | SF 13 |
| **Hub (+lug+ears)** | **6061-T6** machined (proto) / **A380 die-cast or MIM** (prod); **Type-III hard-anodize** the clutch face | light, σy 275 ample (SF 11), complex shape → cast/MIM at volume, anodize for clutch wear | SF 11 |
| **U-bracket (frame)** | **A380 aluminum die-cast** (prod) / 6061 machined (proto) | complex frame, light; splay OK only with the backplate | SF 4.3 |
| **Bracket backplate + case mount pad** | **304 stainless** strip (corrosion, near exterior, no plating) | structural tie / mount, exposed-ish, formed | tie req'd (SF 4.3) |
| **Pawl pin / stow pin** | **A2 (304) stainless, hardened, ISO 8734 dowel** | COTS, corrosion, hard pivot | SF 19 |
| **Belleville clutch** | **51CrV4** spring steel, DIN 2093 (phosphate+oil) | COTS standard disc spring | >2×10⁶ cyc |
| **Hub journal bushing** | **bronze-backed PTFE** sleeve (oilite) | COTS, dry/low-friction journal vs plastic-on-steel | — |
| **S5 + spine tubes** | **6061-T6** (7075 if the top section needs it) | light, F_bry 386, telescoping | (core-joint) |
| **Core→S5 dowels + ferrules** | **304 stainless** | corrosion, pressed pin-bearing | SF 6.4 @1500 N |
| **Fasteners** (M6 mount, M10 nut) | **A2-70 stainless** + nylock/thread-locker | corrosion, standard | SF 24–28 |

## Structural polymers

| Part | **Material / process** | Rationale | 
|---|---|---|
| **T-handle core** | **PA66-GF33** (2-shot w/ TPE) | stiff, moldable, bonds the overmold; carries 1500 N (stem SF ~17) |
| **Case shells** | **Polycarbonate (PC)** — *PC/ABS or PP = cost options* | impact toughness for **SATRA TM242** corner drop; moldable ribs; cold-temp |
| **Release wedge** | **POM-C (acetal)** | low-friction ramp, dimensional stability |
| **Concentrator** | **PA66-GF30** | stiff cam arms, timed outputs |
| **Stow hook** | **PA66-GF30** (or zinc) | light-duty sprung latch |

## Soft goods / overmold / wheels

| Part | **Material** | Rationale |
|---|---|---|
| **Grip overmold** | **TPU or TPV (Santoprene), 60–80 Shore A** | grip feel, 2-shot bond to PA66, durable |
| **Wheel tread** | **TPU** (or rubber) | quiet roll, abrasion (TM248) |
| **Wheel hub / fork** | **PA66 / glass-filled nylon** | strength, light |
| **Wheel axle + bearings** | **steel axle, shielded stainless bearings** | TM248 rolling-road life |
| **Zipper** | **nylon coil + tape** | standard |

## Key decisions / changes
- **Shaft down-spec'd** 17-4PH → **4140** (internal, SF 13 — stainless was unnecessary, saves cost).
- **Hub clutch face hard-anodized** — the as-cast/machined 6061 face would gall against the Belleville/clutch.
- **Case = PC** for the corner-drop requirement (the single most impact-critical material choice; PP if cost dominates and the drop spec relaxes).
- **Core→S5 joint re-checked at 1500 N** (was 960 N): pin SF 6.4, bearing 7, stem 17 — **still passes**.

## Residual (lab, not CAD)
Coupon validation per lot: **tensile/yield** (the metals), **Izod/Charpy impact** (PC shell, GF-nylon),
**hardness** (abutment, pawl, dowels), **2-shot bond peel** (TPE↔PA66), **disc-spring load-deflection**.
