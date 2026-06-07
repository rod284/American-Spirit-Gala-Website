# Gravitcase — Pivot Core CAD Handoff

## 0. What this is
The pivot core of a center-of-mass wheeled-luggage handle. The handle pivots from the
**center of the case back at center-of-mass height (280 mm)** so the loaded case tows
upright. The handle locks at **45°** in two directions: a rigid **stop** blocks opening
past 45° (tow/lift load), and a **pawl** blocks folding back toward 0° (impact, e.g. a
rock-hit). A separate **drawbar** on the same shaft tows the next case.

A rough parametric model already exists (`build_core.py`, cadquery). **Your job is to
refine it into a clean, production-intent parametric solid and run the interference
checks that paper can't.** This is genuinely a coding task — that's why it's here.

---

## 1. Definition of done
- [ ] One clean parametric cadquery model, **every dimension driven by the parameter table** (§4). No magic numbers in part bodies.
- [ ] Manufacturing detail added: fillets, draft on would-be-cast faces, real hex bolt heads, proper pawl geometry, proper drawbar yoke.
- [ ] **Interference check #1 (motion):** sweep the hub 0→45°; the stop lug must enter the pocket and seat on the wall, and the pawl must clear on entry and engage the abutment — with no clash at any angle.
- [ ] **Interference check #2 (static crowding):** no solid intersection among pawl, lug, hub, friction disc, and drawbar collars in the central axial band. Report any clash with its location and volume.
- [ ] Exports a colored **STEP** and an **STL**; renders **iso / side / front** PNGs.
- [ ] A short report of what was changed, what the interference checks found, and what remains open.

---

## 2. THE single source of truth
**`gravitcase_joint_master_definition.html`** — the datum, every part's position /
orientation / size, the named parameters, and the build order. **Code against this.**
If any other sheet conflicts with it, the master definition wins; if the master
definition itself is unclear, stop and ask — do not guess.

Supporting specs (dimensions + reasoning, same authority for their own parts):
`gravitcase_load_spec.html`, `gravitcase_pawl_spec.html`, `gravitcase_bracket_spec.html`,
`gravitcase_core_assembly_pack.html`, plus dimensioned drawings
`gravitcase_pawl_dimensioned.html`, `gravitcase_bracket_pocket_dimensioned.html`,
`gravitcase_oriented_core.html`.

---

## 3. Datum convention — DO NOT CHANGE
- **Origin O** = shaft-axis center = case mid-width, height **280 mm** (COM).
- **+X** = along the shaft, side-to-side (the 14" width). The shaft axis *is* X.
- **+Y** = fore-aft; **+Y points toward the case back / the user** — the deploy direction. −Y = toward the front / packing.
- **+Z** = vertical up. −Z = down toward the wheel base.
- **Deploy angle θ** = measured in the Y–Z plane from +Z toward +Y. θ = 0° stowed, 45° deployed. All rotations about +X.
- A hub feature fixed at hub-angle φ sits at world angle (θ + φ). Stop lug φ = 135°, so at θ = 45° it points −Z (down into the floor pocket).

---

## 4. Named parameters — drive everything from these (mm / deg)
```
COM_HEIGHT     = 280      SHAFT_DIA      = 14
BRKT_INTERNAL  = 50       WALL_T         = 3
HUB_OD         = 22       HUB_W          = 18
LUG_R          = 20       LUG_W          = 10
LUG_PHI        = 135      DEPLOY_ANGLE   = 45
PAWL_W         = 10       NOSE_FACE      = 5
NOSE_TO_PIVOT  = 14       PAWL_PIN_DIA   = 6
ENTRY_RAMP     = 35       WEDGE_RAMP     = 33
DRAWBAR_LEN    = 150      COLLAR_X       = 22
EAR_T          = 5        EAR_GAP        = 10.5
```

---

## 5. The arrangement rules that must not drift
- **The pawl is ON THE HUB** (the moving part); the **wall and abutment are FIXED on the bracket**. Two stops, both "hub feature → fixed bracket feature": stop lug → wall (blocks open), hub pawl → abutment (blocks fold-back). **Do not move the pawl onto the bracket** — the trigger lives on the hub and must reach it.
- **Self-lock:** the fold-back contact normal aims at the pawl pivot pin so the load goes into the pin as shear and cannot cam the pawl open; a backstop catches residual. Only the wedge opens it.
- **Friction** = a disc on the **+X hub face**, axis = shaft (not a radial part).
- **Drawbar** = its own rotation on the same shaft, lower arc, −Z stowed → +Y deployed; ball lands at Z = 280 (COM).
- Bracket = a **channel**: two 3 mm walls tied by a **structural floor** on the −Z side; pocket, wall, abutment, and (in the current rough model) features grow from the floor.

---

## 6. Loads (from the load spec) — for sizing, not for changing geometry
- Design contact **5,500 N** at r = 20 (110 N·m snatch); ultimate **15,000 N** (300 N·m hard-yank).
- Pawl pin Ø6 double shear; ear bearing on 5 mm ears. All comfortable at design.
- Use these to *check* sections, not to resize geometry — resizing waits on the open numbers below.

---

## 7. Tasks, in order
1. **Refactor** `build_core.py` so all geometry reads from the parameter table (§4) at the top.
2. **Detail the parts:** fillets on bracket edges and ear roots (R ≥ 2); draft on cast faces; real **M10 hex** head + nut; proper **pawl** (nose 5×10, 35° entry ramp, heel, over-center contact normal to the pivot); proper **drawbar yoke** (two collars bridged to one arm + ball, not a plain bar).
3. **Interference check #1 (motion sweep)** — see §1.
4. **Interference check #2 (static crowding)** — see §1. This is the whole reason for the handoff; do not skip it.
5. **Export** STEP + STL; **render** iso/side/front (see §9 for headless rendering).
6. **Write the report** (§1, last box).

---

## 8. DO NOT invent — leave these as TODO parameters, do not fabricate values
- **Fold-back impact load** — comes from a bench test, not a script.
- **Steel grade / hardness** — comes from the contract engineer.
- **Spring rates** (friction clamp, pawl return, trigger return, drawbar lock) — bench.

Flag each as a clearly-marked `TODO` parameter. Do **not** pick a value and present it as
final. **LOCKED** = geometry / orientation / fits → build them. **VALIDATE** =
force-driven sizing → keep as parameters, note "pending FEA/bench."

---

## 9. Environment
```
pip install cadquery --break-system-packages
# headless rendering needs a virtual display + software GL:
apt-get install -y xvfb libgl1 libglx-mesa0 libgl1-mesa-dri
LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a -s "-screen 0 1300x1100x24" python3 render_vtk.py
# (or skip rendering and just open the exported STEP/STL in a CAD viewer)
```

---

## 10. Files in this package
```
HANDOFF.md                              ← this brief
scripts/build_core.py                   ← the rough parametric model (your starting point)
scripts/render_vtk.py                   ← headless renderer
models/gravitcase_core.step             ← solid it produces (colored assembly)
models/gravitcase_core.stl              ← mesh (for slicing / quick view)
renders/core_iso.png, core_side.png     ← current look
specs/  ← the HTML spec sheets (master definition is the source of truth)
```

## 11. What "good" looks like
A clean parametric script that rebuilds the whole core from §4, with the pawl on the hub,
the two stops landing on fixed bracket features, fillets and real fasteners, a passing
(or clearly-reported) interference sweep, and STEP/STL out — with the three open numbers
still flagged TODO, not guessed.
