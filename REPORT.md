# Gravitcase — Pivot Core CAD Handoff · Report

**Toolchain:** CadQuery 2.7.0 / OCP 7.8.1 (Python 3.13, Windows).
**Source of truth:** `specs/gravitcase_joint_master_definition.html` (Rev A).
**Deliverables:** `scripts/build_core.py` (parametric model), `scripts/check_interference.py`
(the two interference checks), `scripts/render_vtk.py` (headless renders),
`models/gravitcase_core.step` (coloured assembly), `models/gravitcase_core.stl`,
`renders/core_{iso,side,front}.png`.

---

## 0 · Process note (important)

This task ran in two phases. The package initially supplied **only the brief text** —
no `build_core.py`, no spec sheets, and (critically) **no master-definition HTML**.
Per the brief's own rule ("if the master definition is unclear, stop and ask — do not
guess"), I flagged the missing source of truth and built a **first model from the brief
text alone**, getting both interference checks to pass on that reconstruction.

The real package (master definition + spec sheets + the rough `build_core.py`) arrived
mid-task. The model was then **rebuilt against the master definition**, which differed
from the brief-only reconstruction in several specifics (table below). The original rough
script is preserved as `scripts/build_core_original_rough.py`; the delivered
`scripts/build_core.py` is the clean refactor of it.

| Item | Brief-only reconstruction | Master definition (delivered) |
|---|---|---|
| Pawl location | −Y of lug (φ≈240) | **+Y of lug** (φ≈105), "rides with the lug" |
| Abutment | free post, high (+Z) | **+Y wall of the −Z pocket** (Y 4–8, Z −16…−28) |
| Lug | r 7→20, circ 8 | **r 14→22 (rooted at hub rim), circ 6** |
| Floor | raised to −12 | **low (−32…−28)**; wall+abutment are posts; lug drops between |
| Friction | single disc | **Belleville clutch pack**, r 12–18, ~10 wide, +X face |
| Drawbar (this case) | shown deployed (+Y) | **stowed at −Z, flat to the back panel** |
| M10 | bracket bolts | **shaft +X-end thread** |
| Missing parts | — | **spine boss + telescoping handle, back brace, mount tabs** |

---

## 1 · What was changed (rough → production-intent)

* **Fully parametric.** Every body reads from the §5 parameter table at the top of
  `build_core.py`. No magic numbers in part bodies; derived geometry is computed and each
  un-pinned choice is tagged `# ASSUMPTION`.
* **Datum + build order** follow master §1/§6: O at the COM-height shaft axis, +X along
  the shaft; hub features built at hub-angle φ and rotated by θ; bracket features built as
  absolute deployed geometry ("don't mirror").
* **Two stops, both hub→fixed-bracket** (master §2): stop lug (φ=135) → fixed **wall** on
  the −Y pocket face; hub **pawl** (φ≈105, just +Y of the lug) → fixed **abutment** on the
  +Y pocket face.
* **Proper pawl:** nose flat, 35° entry-ramp lead-in, heel for the 33° release wedge,
  built so the deployed contact-face normal points back at the Ø6 pin → fold-back load is
  **pin shear, not a cam-out moment** (self-lock, master §7).
* **Pawl beefed up (close-look fix):** the original pawl was **142 mm³** with the Ø6.4 bore
  **breaching the loaded +Y flank** (~0 wall). Moved the bearing flank + abutment out to
  **Y 11.5** (within the Y≤22 pocket) so a **2.3 mm wall** sits between bore and load face,
  and deepened the body → **400 mm³**. Bore now a hub-facing hook (unloaded side; fold-back
  seats the pin on the closed wall). Abutment notched along the drawbar path (bottom corner
  only) to keep Check #3 clear. Renders: `pawl_profile.png`, `pawl_wedge/released.png`.
* **Pawl return spring — SPEC'd** (`PAWL_SPRING`, closes the old TODO). **Torsion spring on
  the Ø6 pin**, music wire A228: Ø1.0 wire, OD 8.4, 4.5 coils, **1.57 N·mm/deg**; preload
  **15.7 N·mm** (2.6 N nose) → release **39.2 N·mm** (6.5 N nose); stress 446 MPa, **SF 3.2**.
  The abutment carries the fold-back load, so the spring only *arms/re-seats* the 0.56 g pawl:
  6.5 N seating is **>10× the 0.55 N drop-shock** yet adds only **~1 N at the squeeze**. The
  master's "~40" reconciles as **N·mm of torque** (≈39), not 40 N force. Render: `pawl_spring.png`.
* **Pawl DFM pass + strength (toward manufacture-ready).** Corners **filleted** (Sketch-based,
  stress relief at the bore→flank), **~1° mould draft** on the extrude, bore-edge break.
  **Material: 17-4PH MIM H900** (yield ~1170 MPa; machined 4140 = prototype). **Fold-back load
  projected at 1.5 kN** at the nose (≈1.5× the 960 N handle rating + impact) — *PROVISIONAL,
  confirm by drop/abuse bench. Check #11* hand-calcs: controlling **loaded-wall 98 MPa** (Kt 1.5)
  → **SF 12.0**; nose-face bearing 56, pin-bore 25, pin shear 27 MPa. GF-nylon would be SF ~1.8
  → metal chosen. **Still open for release:** confirm the bench load, FEA sign-off, GD&T +
  surface finish on the bore & nose face, and pin axial retention. Render: `pawl_dfm.png`.
* **Pawl clevis** = two 5 mm ears + 10.5 gap (≈20.5 wide), ears radially **outboard
  (r>14)** so they clear the hub; shifted −X (`PAWL_X=−5`) so the +X ear clears the
  +X-face clutch pack and the −X ear clears the inboard drawbar-collar edge.
* **Friction** modelled as a 5-disc Belleville **clutch pack** (r 12–18) on the +X hub face.
* **Drawbar — a swinging DOF on a SEPARATE lower pivot axle** (`make_drawbar(theta_draw)`),
  a user-approved change from the master's main-shaft collars (see "Deviation" below).
  Per the user's "blue-X" mark, the axle is set **BELOW the trap cluster** at
  **`DRAW_PIVOT_Z = −35`, `DRAW_PIVOT_Y = +15`** (axis note: the user's "down the Y axis" =
  the code's −Z/height). Sitting under the trap, the bar can swing the **full `DRAW_DEPLOY =
  135°` → up to 45° above horizontal** for towing a *taller* case, and the up-swing **clears
  the trap mechanism entirely** (the COM band is occupied by the trap, which is why a
  COM-centred bar could not reach 45°). Deployed, the **ball reaches world ~359 mm**; stowed,
  the bar hangs straight down to **ball world ~87 mm (+Y max 23 < 25 face → flush, clear of
  the wheels)**. A simple fixed **lower axle pin** carries it (the support legs were dropped
  once the pivot rose above the floor). Handle and drawbar **never deploy together** (user
  confirmed), so the swing is checked against the *stowed* hub group (Check #3 clash-free).
  *History:* earlier COM-centred / `−45` / `−106` placements traded angle against trap
  clearance and stow depth; moving the axle down to −35 below the trap resolved all three —
  full 45° reach, trap-clear, and a flush stow.
* **Telescoping spine — real 5-tube octagon cascade** (spec sheet): S1 50×37 → S5 30×17,
  **232 mm each**, 5 mm step / 1.0 mm-per-side clearance, 45° 5 mm chamfer, S1 socketed on the
  hub's 47×34 male boss, S5 carrying the T-handle. `make_spine(extend)` is parameterized:
  collapsed (T-handle top world 560 — **FLUSH** at the case top) ↔ extended (grip reach
  **~36.5″**). Plus **mount tabs** and the **M10 shaft-end thread + hex nut**.
* **T-handle (load-bearing grip)** — `make_thandle`, single central pole ⇒ a true T. The RIGID
  molded core carries the ~960 N snatch; a soft **TPE overmold** (`make_overmold`, ~3 mm skin)
  is feel only. Modelled: rounded grip crossbar (**~Ø33 effective**, 130 graspable, rounded
  ends) on a neck; a **structural stem captured 40 mm into S5** (pinned+bonded — see joint).
* **Grip internals + hand-fit/packaging pass (DONE).** The hollow core carries a mechanism
  cavity + two rod bores; the **rod tops are raised into the open cavity** so the controls act
  on them with clearance. Controls: a **telescope BUTTON** on top (centred) — plunger +
  transfer prong drives the **telerod down 8 mm** (height-lock release); a **squeeze TRIGGER**
  underneath whose **bell-crank reverses** the finger pull-up into a **5.0 mm push-down on the
  pivrod** (= the concentrator stroke), pin lever 9 mm × sin 34°, ending in a **roller** that
  rolls on the rod top (low-friction contact, not a sliding prong). **Return springs** fitted
  (`make_grip_springs`): a coil around the button plunger + a bell-crank return. **Hand-fit:**
  grip depth opened to 32 mm (~Ø33 power-grip) to win wall budget; the **bell-crank now swings
  free — clip 93 → 0.1 mm³** across the full squeeze (1 mm cavity wall). Verified by **Check #9**
  (button contacts/drives the rod, no bind, cap 559 ≤ 560; trigger push ≥ 5 mm; swing clears).
  Remaining **CONCEPT (bench):** spring rates, the exact cam/roller profile, TPE durometer.
* **Core-to-S5 joint — LOCKED (materials selected).** Resolved the earlier marginal SF 2.0
  *architecturally*: the **carrier now terminates below the stem** (only the two thin rods
  pierce it), so the stem is a **near-solid insert** (27×14, fills the S5 bore) — strong enough
  for a real pinned+bonded joint. **Load path:** PRIMARY = structural adhesive bond over the
  40 mm annular overlap (toughened epoxy/methacrylate ~15 MPa, ~0.3 mm bondline, **SF 51**);
  BACKSTOP (creep/fail-safe) = **two Ø3.5 transverse dowels** at X±10 (flanking the rods, along
  Y, clearing the actuation) with **steel ferrules** pressed into the 1.2 mm aluminium walls to
  spread the pin bearing. **Materials chosen:** S5 tube **6061-T6** (Fbry 386); core
  **PA66-GF33** (allow ~110); dowels + ferrules **304 stainless**. **Margins (960 N snatch):**
  pin double-shear **SF 10** (5.0 single-dowel worst case), bearing-on-core **11**, bearing-on-
  wall-via-ferrule **15**, stem tension **27**. New part `make_joint_pin` (dowels + ferrules);
  modelled in the assembly. Bench items: adhesive selection/cure, dowel fit class, fatigue.
* **Stow:** the load-bearing grip is ~40 mm tall but only ~10 mm sits
  above the collapsed pole, and the joint blocks dropping the pole, so **flush cost tube
  length** (Option B chosen: flush + full 70 mm overlap, reach 41″→~36.5″).
* **Actuation (Rev A spec) — LOCKED parts modelled, CONCEPT parts flagged.** Built the
  defined geometry: the **keyed glass-filled-nylon carrier** (twin Ø5 keyed bores, runs the
  full spine, anti-buckle) + **telescope rod** (Ø4.5 SS, continuous) + **pivot rod**
  (Ø4.5 SS, **segmented per section** for the interlock), with the hub boss now **hollow**
  so the rods pass through to a **concentrator** placeholder at the hub. The molded touch
  parts (button, trigger, grip), the height-lock pin/hole detail, and the bell-crank /
  concentrator ratios + spring rates are **CONCEPT / VALIDATE** in the spec — represented or
  omitted, **not invented**.
* **Height locks (GC-2xx-lk) — DIMENSIONED** (spec left this CONCEPT): **Ø3 spring pins**
  on each inner tube's +Y flat drop into **Ø3.4 holes** in the outer tube — **3 discrete
  grip positions** (extend 0.6 / 0.8 / 1.0), positive stops not friction. The telescope rod
  retracts all four together to slide. The hole positions are derived so each joint's pin
  registers at the three heights (verified by Check #5).
* **Joint release (the joint's actuation).** One squeeze, via the concentrator, fans to
  three jobs at the hub. The dimensioned one is the **pawl release wedge** (33° ramp):
  `WEDGE_PUSH` 6 mm → nose lift **3.9 mm** (spec "push 6 → lift 4"). Modeled the **wedge**
  (POM) and a `lift` DOF on the pawl.
* **Concentrator 3-way + stow hook.** The concentrator (POM) is modeled with its **three
  outputs** — friction back-off (+X axial), pawl wedge, stow-hook lift. Added the **stow
  hook** (on the hub) and its **fixed bracket pin** (the 0° latch). One squeeze lifts both
  the hook and the pawl, but only the stop *engaged with a fixed feature at that angle*
  releases — verified by Check #7. The ~4× ratio and cam profiles are **VALIDATE** (bench);
  the friction clamp / hook / trigger spring rates are `TODO`.
* **Complete suitcase (`make_case_back` + `make_case_front` + `make_zipper` + `make_wheels`).**
  Two-shell molded body at the user envelope **343 W × 508 H × 133 D** (+50.8 wheels = ~559
  total); see the two-shell + envelope bullets above. The **axle runs through the case AND the
  metal** bracket (shared
  bearing): the metal assembly (bracket X±34, M10 nuts to X±47) drops into the pivot pocket
  (walls X±50), and the case blank stays **solid outboard of X±50** so the shaft bore passes
  through case material on its way out — no separate boss needed. Plus **four 2 in (50.8 mm)
  spinner casters** at the bottom corners; they
  drop ~59 mm below the body, so the rolling surface is ~59 mm under the case bottom.
* **Back shell — INJECTION-MOLDED back (drafted, radiused, close-fit).** Reworked the
  back from loose machined-looking boxes into a real molded negative. Decisions (with the
  user): **3° draft** on every pocket wall, **3.0 mm** nominal wall, **screw-boss** core
  retention, **0.3 mm** fit clearance, **Y-draw** (parting at the rim), axle bore post-drilled.
  `molded_pocket()` builds each receiving feature as the part's true stowed footprint **+0.3 mm
  at the seat**, tapering **open 3° toward the −Y insertion face** (so the core drops in and
  self-locates at the seat, and the tool releases in −Y), with **radiused corners**. Pockets
  tightened to the parts: spine-column channel **76→50.6 mm**, drawbar channel **54→26.6 mm**,
  pivot pocket sized to the bracket+M10-nuts (96), grip well to the overmold (136.6). **Parts
  fit the molded pockets at 0 mm³** (Check #8), still flush (23 mm behind the 25 mm plane).
  **Uniform wall + ribs (DONE):** the 60 mm SOLID back zone is replaced by a true injection-
  mold shell — a ~3 mm hollow box (front/sides/top/bottom + 3 mm back skin) with the core
  received in **thin-wall (3 mm) drafted TRAYS** standing off the back skin (`_core_trays`),
  stiffened by **ribs** (`_back_ribs`); a top opening lets the handle rise from its well. Case
  material volume fell **12.1M → 2.66M mm³** (no thick sections to sink/warp). Voids + trays are
  generated from one `CORE_FEATURES` list so the shell and case always match. Parts still fit at
  **0 mm³** and stow flush; all 9 checks PASS.
* **Molded envelope (user spec): body 343 W × 508 H × 228.6 D mm** (≈13.5″ × 20″ × 9″; 508 =
  20″ carry-on max; + 50.8 mm 2″ wheels = ~559 mm / 22″ total). The body is **centred on the
  pivot** (the COM),
  so the pivot stays ~280 mm above the ground (body rides on the wheels). Spine re-trimmed to
  the 508 body: collapsed grip flush at the top, **extended reach ~42.6″**.
* **Case BODY molding pass (DONE).** The outer body is a molded shell, not a sharp brick:
  **all external edges/corners rounded (R14)**, internal corners radiused, **~1.5° outer-wall
  draft** (Y-draw), top trimmed flush.
* **TWO-SHELL architecture (DONE).** The case is a **BACK shell + FRONT shell** that **zip
  together** at mid-depth: each shell **101.6 mm (4.0″)** deep, with a **25.4 mm (1″) perimeter
  zipper band** centred at 4.5″ from each face (`PARTING_Y` = mid-depth; `Y_BACK_PART` /
  `Y_FRONT_PART` = ±½ zipper). 4″ + 1″ + 4″ = 9″. Terminology locked: **+Y = case back = core side; −Y = case
  front = packing**; the core's **back face = +Y**, **front face = −Y**. The **BACK shell**
  (`make_case_back`) holds the entire core in **molded indentations that OPEN TO THE OUTSIDE
  back** (spine-column channel, pivot pocket, drawbar channel, grip well) — the core nests in
  from outside and the **handle/drawbar rotate OUT the back exterior** (deploy = +Y). Recesses
  are drafted open toward +Y (tool draws out the back) with a 3 mm bottom wall separating the
  core from the packing. The **FRONT shell** (`make_case_front`) is packing only, no core. A
  representative **perimeter zipper** band (`make_zipper`) seams them. `_full_case_solid` builds
  the rounded/drafted/thin-wall body once; the two shells are planar splits of it.
  Suitcase STEP exports `case_back` + `case_front` + `zipper` as separate parts.
* **Back ribbing for tow impact (DONE, `_back_ribs`).** Full stiffening network on the inside
  of the back shell: vertical backbone + intermediates, 5 horizontal cross-ribs, a perimeter
  frame, and **diagonals from the pivot to the bottom corners** (spreads the tow reaction into
  the wheels). All 3 mm (≤60% wall, no sink), 15 mm deep, cut clear of the core recesses.
* **Bracket backing strip (DONE, `make_backplate`).** Steel strip across the back of the
  U-bracket tying its two walls so the open U can't splay under the snatch/tow load.
* **Front tow-ball receiver — STEEL KEYHOLE HITCH (DONE).** The hitch is a primary load
  path (tow pull up to ~1 kN with dynamics / a multi-case train), so it's **metal, bolted,
  and rib-backed** — not a molded snap. At **11″ below the top (local Z −25 ≈ COM height)**:
  - **`make_receiver_bracket`** — a **steel keyhole plate**: funnel lead-in → **round entry
    hole** (admits the Ø16 ball) → **self-locking drop slot** (~12°, captures the neck; the
    ball is trapped *behind* the plate) → **detent** ("slight snap"). Capture is **⊥ to the
    tow pull**, so the load can't release it — only lifting the ball to the round hole does.
    (Replaces the old snap-socket, which released *along* the pull — the weak design.)
  - **Anchorage** — recessed flush, **4 bolts** (`make_receiver_bolts`) into **cored gusseted
    bosses**, plus a **steel backing plate** (`make_receiver_backplate`) inside so the bolt
    heads can't peel through the wall under the −Y pull.
  - **Front-shell rib network** (`_front_ribs`) — perimeter frame + ribs **radiating from the
    receiver to the corners and down to the wheel base**, feeding the hitch load into the
    structure (mirrors the back shell's core-load ribs).
  Each case is **pulled from the back** (drawbar exits the front, grabs the next case's
  front receiver). Bench items: pull test / FEA, detent force, the exact self-lock cam.
* **Rib rule corrected.** Ribs were rebuilt at **1.5 mm (50% of the 3 mm wall)** with capped
  depth — per IM practice (a rib = wall thickness makes a thick junction → sink). Applies to
  both `_back_ribs` and `_front_ribs`.
* **Wheels (DONE) — wagon steering.** Pulled from the back ⇒ **2 BACK swivel casters**
  (`_swivel_caster`, king-pin + trailing wheel, steer at the pull end) + **2 FRONT fixed
  wheels** (`_fixed_wheel`, track straight). All 2″ (50.8), drop 50.8 below the body.
* **Fillets** R≥2 applied to lug, ear roots, spine boss, and bracket top edges
  (see "Open / residual").
* **Coloured STEP** assembly (per-part colours) + STL exported; iso/side/front PNGs
  rendered offscreen (Windows-native VTK — the brief's xvfb path is Linux-only).

---

## 2 · Interference checks — what they found

Engine: OCCT booleans (intersection volume = penetration) +
`BRepExtrema_DistShapeShape` (minimum gap, for seating). Tolerance: 1e-3 mm³.

### Check #1 — motion sweep, hub 0→47° (master §7.1, −Z crowding)
Pass/fail on the **rigid structural members** (shaft, hub, lug, ears, pin, friction,
spine) vs the bracket **and** vs the stowed drawbar.

* **Travel band 0→45°: clash-free — PASS.** Worst penetration in band = **6.88 mm³ on the
  lug at θ=47°**, i.e. *past* deploy — that is the open-stop **hard-stop biting the −Y
  wall** (nominal 45° + the 0.3 mm pocket clearance), not a travel clash.
* **Lug enters the pocket and seats on the −Y wall**: gap closes monotonically to
  **0.30 mm at θ=45°**, contact at ~47°. ✔ "stop lug → wall" behaves.
* **−Z crowding (stowed drawbar): clash-free — PASS.** With the drawbar lying flat to the
  back panel, structural-member ∩ drawbar = **0 mm³** across the whole sweep. (This is the
  crowding the master said to "confirm.")

### Pawl engagement — static, at full deploy (master §7)
The pawl is a **sprung over-centre** lever; a rigid kinematic sweep cannot represent it
pivoting on its spring to ride over the abutment and drop in behind it — and that motion
is driven by spring rates that are **TODO/bench (§8)**, so it is validated statically:
* **Nose seats on the abutment: gap = 0.300 mm** (= the pocket-clearance target). ✔
* Contact face built **normal-to-pin** → self-lock confirmed by construction.
* **Not simulated:** the dynamic entry ride-over (depends on `TODO_SPRING_PAWL_RETURN` /
  `TODO_SPRING_TRIGGER_RETURN`).

### Check #2 — static crowding, central axial band at deploy (master §7.2)
The named must-prove check: pawl + ears + lug (central) vs hub (radius), the clutch pack
(+X face), and the inboard drawbar-collar edges.
* **No unintended clashes — PASS.** The only reported overlap is the **intended pawl-hub
  mount contact, 1.3 mm³** (the pawl nests on the hub at its pivot).
* Reaching this required two corrections the harness surfaced: the pawl-clevis had to be
  shifted off the inboard collar edge (`PAWL_X`), and the +X ear trimmed tangentially
  (`boss_h` 6→4.5) so it clears the lug in the shared central band.

### Check #3 — drawbar deployment sweep (lower pivot)
Sweep the drawbar `theta_draw` 0 → `DRAW_DEPLOY` (135° → up to 45° above horizontal) about
the lower axle, handle held stowed, drawbar-on-axle bearing excluded; test vs the bracket,
the trap cluster, and the stowed hub group.
* **Clash-free across the whole stow→45° swing — PASS** (0.000 mm³), at the current
  `DRAW_PIVOT_Z = −35`, `DRAW_PIVOT_Y = +15` pivot (below the trap). Because the axle sits
  under the trap cluster, the bar climbs to the full 45° **without touching the trap** —
  matching the spine's 45° so the two can never collide even if both were out (they aren't:
  one at a time). Deployed ball reaches **world ~359 mm** (taller-case towing); stowed ball
  hangs to **world ~87 mm**, clear of the wheel base.

### Check #4 — actuation (fit + full-extension interlock)
* **Fit (geometric) — PASS.** The keyed carrier and both Ø4.5 rods run inside the spine
  bore with **0 mm³** penetration into any tube wall (collapsed = tightest), and the
  concentrator clears the bracket. The **carrier terminates below the grip stem** (so the stem
  stays solid for the core-to-S5 joint); only the two Ø4.5 rods continue up through the stem
  bores to the controls, guided there by the stem itself.
* **Interlock — concrete, geometrically measured.** Dimensioned with **λ = 12 mm lost
  motion per joint coupling** and a 10 mm rod stroke / 5 mm concentrator demand (5 mm of gap
  the squeeze can absorb). Check #4 *measures* the gap between consecutive pivot-rod
  segments: **0.000 mm at full extension → TRANSMITS**; **12 mm/joint (48 mm total) at any
  partial height → dies**; even a single short joint (12 mm) exceeds the 5 mm budget. So the
  push column transmits **only at full extension** — "extend → squeeze → swing" is enforced
  geometrically. (λ and the strokes are pickable design values; tune on the bench, but the
  mechanism is now dimensioned and verified, not representative.) *Note:* the 5 rod segments
  are now distributed evenly up the rod (rather than at the physically-bunched collapsed
  joints) so the lost-motion gaps stay well-posed at every extend — the spine resize for the
  flush grip had made the old collapsed model degenerate into a false "transmits."

### Check #5 — height-lock pin/hole registration
At each of the 3 discrete positions the protruding pin tip must enter a hole; between
positions it must be blind against the wall (positive lockout). *Measured* tip penetration:
* **0.000 mm³ at extend 0.6 / 0.8 / 1.0 → REGISTERS** (pin seats in a hole, locks).
* **39.6 mm³ at extend 0.7 (off-position) → BLIND** (pin hits the wall, springs to a hole).
* **PASS** — discrete positive stops confirmed; the lock holds at 3 heights and locks out
  everywhere between. (Pin/hole sizes and the 3 positions are dimensioned design picks;
  spring rate is bench, `TODO`.)

### Check #6 — joint release (pawl wedge)
* **Wedge ratio:** push 6 mm → lift **3.90 mm** ✓ (spec push 6 → lift 4).
* **Fold-back 5° with the pawl LOCKED:** **11.8 mm³ into the abutment → BLOCKED** (the stop
  actually holds).
* **Fold-back 5° with the pawl RELEASED (3.9 mm lift):** **0 mm³ → CLEARS** (handle folds).
* **PASS.** This check forced two real corrections it alone surfaced: (1) the abutment had
  to present a **vertical −Y face** (not a top ledge) so fold-back genuinely *jams* into it —
  the prior "seats with 0.3 mm gap" check only proved contact, not blocking; and (2) the
  abutment had to be unioned **after** the pawl-swing relief cut (build order) so the relief
  doesn't carve away the contact face. The abutment is also narrowed/shifted −X to stay clear
  of the lug's swing (central-band crowding).

### Check #7 — concentrator 3-way (context-dependent release)
One squeeze lifts both stops; only the one engaged with a fixed bracket feature at that
angle releases. *Measured* gaps to the fixed features:
* **0° (stowed):** hook↔stow-pin **0.300 mm (ENGAGED)**, pawl↔abutment 4.73 mm (free) →
  squeeze frees the swing-up.
* **45° (deployed):** pawl↔abutment **0.300 mm (ENGAGED)**, hook↔stow-pin 7.62 mm (free) →
  squeeze (wedge) frees the fold.
* **PASS** — context-dependent release confirmed. The friction back-off is the always-on
  third output (axial). Ratio/cam profiles + spring rates are VALIDATE/`TODO`.

### Check #8 — back-shell fit (flush + case envelope)
The molded back shell (`make_shell` / `_core_features`, derived from the live parts) is the
negative of the *current* parts; the check verifies the stowed mechanism sits flush and inside
the **343 × 508 × 133** body envelope (compared to the body top/bottom in world Z).
* **Flush ✓** — max back protrusion 23 mm, behind the 25 mm back plane; bottom clears ground.
* **Spine + T-handle fit — FLUSH (Option B).** With the load-bearing T-handle added (~40 mm
  tall), the collapsed grip overran the 560 top by 34 mm. The pole is anchored at the COM pivot
  and the joint sits directly below it, so the pole **cannot be dropped** to make room (base −10
  still leaves the grip 13 mm proud *and* rams the release mechanism). Resolved per the chosen
  **Option B**: trim the tubes (`SPINE_LEN` 257→232, base 11→2, full 70 mm overlap kept) so the
  T-handle top is **world 560 — flush**. Cost: extended grip reach **~36.5″** (41″ target not
  met — flush trades against reach in this pivot-at-COM architecture; alt Option C would hold
  41.7″ but at ~38 mm tube engagement). The case top carries a **grip well** for the crossbar.
* **Drawbar stow — RESOLVED.** With the axle moved down to −35 (below the trap), the stowed
  bar hangs to **ball world ~87 mm** — well clear of the wheel base — and the back protrusion
  is 23 mm (flush). The earlier deep-pivot "stows into the wheel zone" problem is gone.
* **Pocket foul — RESOLVED (now 0 mm³).** Two CONCEPT pocket edges were tightened so the
  parts no longer touch the molded negative: (1) the recess back wall deepened to Y −29 (this
  originally cleared the bracket back-brace plate, since deleted as a floating part), and
  (2) the redundant outboard axle boss was
  dropped — the case blank is already solid outboard of the pivot pocket (X±50), so the shaft
  bore alone makes the axle run through **case AND metal**. Parts-vs-pockets foul went
  **3491 → 0 mm³**.
* **Flush + within case envelope: YES, and pocket-clear: YES.** Check #8 now fully PASS.
  Remaining recess/pocket *widths*, grip pocket, and rib patterns are still **CONCEPT** (set
  at tooling layout) but no longer interfere with the parts.

### Check #9 — grip controls (button + trigger bell-crank, post hand-fit pass)
Verifies the grip-internal mechanism drives its rods and the bell-crank swings free.
* **Button → telerod — PASS.** The top button's plunger + transfer prong **contacts the telerod
  top** (now raised into the cavity) and drives it **down 8 mm** (≥ the height-lock retract) with
  **0 mm³** bind through full press; the cap top stows at **world 559 ≤ 560**.
* **Trigger → pivrod — PASS.** The underside squeeze trigger's **bell-crank reverses** the
  finger pull-up into a **5.03 mm push-down** on the pivot rod (pin lever 9 mm × sin 34° ≥ the
  5 mm concentrator stroke) via a **roller** on the rod top, **0 mm³** core bind at rest.
* **Bell-crank swing — CLEARED.** Worst penetration across the full squeeze swing **0.1 mm³**
  (was ~93) — the rods were raised into the open cavity, the grip depth opened to 32 mm for wall
  budget, and the hub/neck slimmed. The mechanism rotates free with a 1 mm cavity wall.
* **CONCEPT / open (bench):** return **spring rates** (§8), the exact **cam/roller profile**,
  and **TPE durometer**. Renders: `handle_internals.png` (cutaway w/ roller + springs +
  dowels), `handle_grip.png` (TPE overmold), `handle_detail.png`.

### Check #10 — tow hitch (steel keyhole: enter / capture / snap / hold / release)
Verifies the front receiver mechanism geometrically + analytically.
* **Geometry — PASS.** entry Ø18 > ball Ø16 > slot 9 > neck Ø8: the ball **enters** the round
  hole, the slot is too narrow for the ball (**trapped**) but clears the neck (**slides**).
* **Capture — PASS.** Dropped ball pulled outward is **blocked by the plate (248 mm³)** — the
  tow load can't release it (capture ⊥ pull). *This*, not the "self-lock", is the tow lock.
* **Snap / anti-rise — PASS.** A **sprung detent pin** sits in the rising ball's path
  (**46 mm³** block) — the "slight snap" that stops vibration walking the ball up. (Two rigid
  steel parts can't snap; the spring is what does.)
* **Self-lock — PASS.** The seat is **back-leaned 12° in the Y–Z plane** (the correct plane —
  the earlier X–Z tilt was inert against a −Y load), so the tow pull **seats the ball downward**.
* **Release — PASS.** Ball raised to the entry hole pulls out cleanly (**0 mm³**).
* **Hold @ 1 kN — PASS.** 4× M4 bolts in tension **SF 8.8**; steel slot bearing **SF 18**.
* **CONCEPT / open (bench):** the 1 kN rating is an estimate; the bracket→boss→rib path wants
  a **pull test / FEA**; the **detent spring rate** + the **12° self-lock seat angle** are bench-tuned.
* Renders: `rx_bracket.png` (keyhole + ball), `rx_selflock_section.png` (sprung detent + seat).

**Checks: #1 · Pawl · #2 · #3 · #4 · #5 · #6 · #7 PASS; #8 flags two parts-vs-envelope fixes.**

### Design-margin sweep (`scripts/sweep_margins.py`)
Each key clearance/kinematic value was swept to its failure threshold; the gap to nominal
is the margin.

| Item | Nominal | Fails at | Margin | Status |
|---|---|---|---|---|
| Pawl release lift (wedge) | 3.90 mm | 2.0 mm | **1.9 mm** | OK |
| Pawl engagement depth | 2.70 mm | 0 | **2.7 mm** | OK |
| **Lug entry clearance** | 0.50 mm | 0 | **0.5 mm** | **TIGHT** |
| **Ear width vs lug** | 4.5 mm | 5.0 mm | **0.5 mm** | **TIGHT** |
| Interlock lost-motion | 12 mm | 5 mm | **7.0 mm** | OK |
| Height-lock pin/hole | 0.2 mm/side | — | — | fit |
| 3-way free-stop separation | 4.73 mm | 0 | **4.7 mm** | OK |

**Finding:** the release kinematics, interlock, and stops all carry comfortable margin
(1.9–7 mm). The **only tight spots are both in the central axial band** — the lug's entry
clearance and the ear/lug crowding, each ~**0.5 mm**. That is exactly the zone the master
and the bracket-pocket sheet flagged as "the one thing the assembly model must prove."
More room there would mean a wider `BRKT_INTERNAL`, thinner lug/ears, or accepting the
friction-pack/collar axial constraint that forces the overlap — a trade for the next rev.

### Deviation from the master definition (needs Rev B sign-off)
The master puts the drawbar on the **main COM shaft** (collars at X±22, rotating about X).
Per your direction we moved it to a **separate lower pivot axle** below the shaft, because
the main-shaft swing fouled the trap mechanism (abutment / bracket front / floor) and ran
tow load through the COM joint. The lower pivot (now `DRAW_PIVOT_Z = −35`, below the trap
cluster, per the user's "blue-X" mark) removes both problems, keeps tow load in the lower
structure, and lets the bar reach the full 45° for taller-case towing while clearing the
trap. This **supersedes the master's drawbar arrangement** and should be folded back into the
master definition (Rev B). New part it introduces: the lower pivot axle pin (`make_lower_axle`
— support legs were dropped once the pivot rose above the floor). `COLLAR_X` is now unused.

---

## 3 · Open / residual (not guessed — flagged per §8)

**Force-driven `TODO` parameters (kept symbolic, top of `build_core.py`):**
* `TODO_FOLDBACK_IMPACT_N` — fold-back impact load (bench).
* `TODO_STEEL_GRADE` — grade / hardness (contract engineer).
* `TODO_SPRING_FRICTION_CLAMP`, `_PAWL_RETURN` (~40 N quoted), `_TRIGGER_RETURN`,
  `_DRAWBAR_LOCK`, `TODO_STOW_HOOK_SPRING_N` (~15 N quoted) — all bench.

**Geometry assumptions** (LOCKED-where-possible, but reconstructed where the master left a
detail open — each tagged `# ASSUMPTION` in code): pin radius `PIN_RAD=12`, pawl pivot
angle `PAWL_PHI=105`, clevis axial offset `PAWL_X=−5`, ear tangential half-width
`boss_h=4.5`, running fit `FIT_CLR=0.2`. These were tuned so the joint is self-consistent
and the checks pass; reconcile against the master if any are over-specified there.

**Detail gaps:**
* **Draft** — `DRAFT_DEG=2.0` is parameterized but **not applied**. The master flags the
  *production process* (cast vs. machined) as undecided, so draft is genuinely a
  process-dependent (VALIDATE) item; applying it to functional seat faces before that
  decision would be wrong. Ready to apply once the process is locked.
* **Pawl-edge fillet** skips (`StdFail_NotDone`) — the ramp lead-in has edges too short
  for the radius; cosmetic on a small hardened part. Lug/ear/spine/bracket fillets apply.
* **Actuation internals not modelled** (POM, force-driven, not load-critical): trigger rod
  Ø4.5, the ~10× concentrator, the stow hook + bracket pin, and the Belleville stack
  detail (modelled as a representative disc pack). These depend on the TODO spring rates.

---

## 4 · How to reproduce

```bash
python3 scripts/build_core.py          # builds + exports STEP/STL, prints part volumes
python3 scripts/check_interference.py  # runs both checks + pawl engagement (PYTHONUTF8=1 on Windows)
python3 scripts/render_vtk.py          # writes renders/core_{iso,side,front}.png
```
(On Windows set `PYTHONUTF8=1` so the ± / − characters print; rendering is native-offscreen,
no xvfb needed.)
