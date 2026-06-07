# Gravitcase — Design Loads & Standards Basis

The design loads were **provisional projections**; they are now **derived from published luggage
test standards** so a reviewer sees a *cited* basis, not assumptions. The only residual is the
**physical test to validate** (a drop/fatigue rig — cannot be done in CAD).

## Standards referenced

| Standard | Scope | Key requirement |
|---|---|---|
| **QB/T 2155-2018** | trolley **pull-rod** (telescoping handle) | load-bearing **≥ 1500 N**, deflection **< 3 mm**, **≥ 3000** extend/retract cycles |
| **QB/T 2919** | trolley handle fatigue | **3000** pull-and-close cycles, no jam/loosen |
| **SATRA TM243:2008** | handle **"snatch" test** | loaded case lifted, **dropped a set distance, fall arrested** → impact load |
| **SATRA TM242:2008** | corner impact | filled case **dropped on each of 8 corners** ×2 |
| **SATRA TM248:2021** | wheel system | **5 h rolling road**, belt with two ridges (lift-and-drop impact) |
| ergonomic studies | steady pull/push | ~**100 / 196 / 294 N** at typical handle heights |

## Derived design loads (with the SF the model achieves)

| Load case | **Design value** | Basis | Where it's used | Margin in model |
|---|---|---|---|---|
| **Handle proof load** | **1500 N** | QB/T 2155 (≥1500 N, <3 mm) | shaft, hub lug, case mount | shaft **SF 13**, lug **SF 11** |
| **Fold-back / snatch (impact)** | **1500 N** | QB/T 2155 proof + SATRA TM243 | pawl, abutment, ears, pin | pawl **SF 11** (FEA), abutment **SF 3.8**, ear **SF 7.1** |
| **Frame side/abuse** | **750 N** (0.5×) | out-of-plane abuse | U-bracket walls + backplate | **SF 4.3** (backplate required) |
| **Case→case tow snatch** | **~1000 N** | dynamic/train (conservative vs 100–300 N steady) | tow-ball receiver / hitch | bolt SF 8.8, bearing SF 18 |
| **Steady tow/push** | **100–300 N** | ergonomic | rolling effort, feel | n/a (comfort) |
| **Corner drop** | per **SATRA TM242** | 8-corner drop | case shells, wheel mounts | *case release pass (TODO)* |
| **Wheel ridge impact** | per **SATRA TM248** | rolling road | wheels, swivel, axles | *wheel release pass (TODO)* |
| **Control forces** | **5–8 N** | (corroborated) | button + trigger | matches grip design |

## Fatigue / life targets (standard-derived)
- **Telescoping + deploy mechanism:** ≥ **3000** extend/retract cycles (QB/T 2919/2155), target 5000–10000.
- **Pawl / wedge / springs:** cycle every deploy → size springs for **>10⁴** cycles (infinite-life stress band).
- **Wheels:** survive the **5 h TM248 rolling road** with ridge impacts.

## What changed vs. the earlier provisional basis
- Fold-back **1500 N** — *was a 1.5× projection; now equals the QB/T 2155 proof load* (coincidentally validated).
- Handle working load **960 N → 1500 N** — re-based to the QB/T proof; all pivot parts re-checked and **still pass (SF ≥ 3.8)**.
- Every load now carries a **citation**; the residual is purely the **physical drop/fatigue test** to confirm the analysis.

## Residual (genuinely needs a physical rig — not CAD)
1. Drop/snatch test to **TM243/TM242** on the first prototype.
2. **3000+ cycle** fatigue on the telescope + deploy.
3. **TM248** wheel rolling-road.
4. Clutch **friction-torque** measurement (sets the Belleville preload).

*Sources: QB/T 2155-2018; QB/T 2919; SATRA TM242/TM243/TM248; ergonomic pull-force studies.*
