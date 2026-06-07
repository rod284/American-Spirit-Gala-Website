# Gravitcase — T-Handle Core Release

Release-grade pass (GD&T · FEA · BOM · DFA) for the **T-handle** — the load+mechanism grip:
a PA66-GF33 **load core** + TPE **overmold**, housing the telescope **button** and deploy
**trigger**. Load 1500 N (QB/T 2155); materials per `MATERIALS.md`. Analysis: `scripts/fea_handle.py`.

## Architecture
Crossbar **130 mm grasp, 32×32 core**, central **stem** into S5 (core-S5 joint = twin Ø3.5
dowels, already released). A central **cavity (26×15)** houses the button (top, telescope
release) + trigger (underside squeeze, deploy release). 2-shot: PA66-GF33 core → TPE skin.

## Structural analysis (1500 N)
| Item | Stress | SF |
|---|---|---|
| Crossbar bending, solid section (offset lift 50 mm) | 14 MPa | 8.0 |
| **Crossbar bending AT THE CAVITY** | **49 MPa** | **2.3 ← governs** |
| Stem Ø16 tension | 7 MPa | 15 |
| Core-S5 dowels (Ø3.5, 304 SS) | — | 6.4 |
| TPE 2-shot bond shear (grasp) | 0.11 MPa | ≫ (bond ~3–5 MPa) |

### Finding & recommendation — the cavity is the soft spot
The button/trigger cavity sits at the **centre**, exactly where a **one-hand offset lift** makes the
bending moment peak → it cuts the crossbar section and drops the margin to **SF 2.3** (still >2,
PA66-GF33). **Recommend a rib/boss frame around the cavity** (closes the section back toward the
solid SF 8) — cheap in a molded part, and it stiffens the mechanism mounts too.

## GD&T (datum **H** = the stem axis)
| Feature | Callout |
|---|---|
| Stem OD → S5 bore | slip-fit; **⌖ Ø0.1 H** (core-S5 dowel registration) |
| Dowel holes (×2, Ø3.5) | ⌖ Ø0.1 H (shared with S5 — match-drill or jig) |
| Cavity + button bore (plunger) | ⌖ Ø0.2 H; plunger bore ⌭ 0.05 |
| Trigger pivot bore (Ø, TRIG_PIN_Y) | ⌖ Ø0.2 H; coaxial 0.05 |
| Grasp profile / overmold interface | profile 0.5 (ergonomic); **interlock undercuts** for the 2-shot lock |

## BOM
| Item | Spec | Source |
|---|---|---|
| **Load core** | **PA66-GF33**, injection-molded (with overmold interlock features) | molder |
| **Overmold** | **TPU or TPV (Santoprene) 60–80 Shore A**, 2-shot bond to PA66 | 2-shot molder |
| Button + plunger | POM-C molded | molder |
| Trigger + bell-crank + roller | PA66-GF30 + steel roller pin | molder / COTS pin |
| Button/trigger springs | per `SPRING_BUTTON_RETURN` / `SPRING_TRIGGER_RETURN` (SF 1.8–2.1) | COTS |
| Core-S5 dowels ×2 | Ø3.5 **304 stainless** + steel ferrules | COTS |

## DFA — assemblable? **Yes**
1. **2-shot mold:** shot 1 = PA66-GF33 core (cavity + interlock undercuts); shot 2 = TPE skin.
2. Drop the **trigger + bell-crank + roller + spring** into the underside cavity; pin the pivot.
3. Drop the **button + plunger + spring** into the top bore.
4. Route the **telerod + pivrod** up the stem bore to the controls (rod tops raised into the cavity).
5. Join the **stem to S5** (twin dowels + ferrules) — match-drilled.
Tool access: mechanism loads into the open cavity before the grip is capped; dowels cross-drilled at the stem.

## Residual (bench / lab)
- **TPE↔PA66 2-shot bond peel** (edge adhesion, the real overmold risk).
- **≥3000-cycle** button + trigger actuation fatigue (QB/T 2919).
- Confirm the **cavity rib** restores the bending margin (FEA/test).
- Grip ergonomics (hand-fit already checked — Check #9).
