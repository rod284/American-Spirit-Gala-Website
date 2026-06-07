# Gravitcase — Pivot-Area Manufacturing Release

Per-part DFM + GD&T + surface-finish + retention callouts for **every part in the handle-pivot
cluster** (the COM hinge: shaft, hub/lug/ears, pawl + pin + spring, release wedge, friction
clutch, U-bracket + abutment, backing plate, fasteners).

**Status:** geometry & load path verified (Checks #1–#11 PASS). **Loads are now standard-derived**
(`DESIGN_LOADS.md` — QB/T 2155 / SATRA TM243) and **materials selected** (`MATERIALS.md`); residual
is physical validation only (drop/fatigue rig, coupon lots).
Loads: **handle proof 1500 N** (QB/T 2155); **fold-back 1500 N** (SATRA TM243 snatch).

GD&T per ASME Y14.5. Dimensions mm. Ra in µm.

---

## Datum scheme (whole rotating group)

| Datum | Feature | Used by |
|---|---|---|
| **A** | **Pivot axis** — the Ø14 shaft cylindrical axis (the journals) | shaft, hub bore, bracket bores, friction, pin radius |
| **B** | Hub **+X clutch face** (axial stack reference) | hub, friction stack, nut preload |
| **C** | Assembly **mid-plane** (X=0, between the bracket walls) | bracket, backing plate, tab holes |

Everything that rotates is toleranced to **A**; the axial clutch stack to **B**; the fixed
structure to **A/B/C**.

---

## 1 · Pivot shaft  (CUSTOM) — Ø14 × 70, M10 thread one end
**Function:** the hinge axle; carries the handle bending moment, locates the hub, anchors the clutch nut.
**Material/process (selected):** **4140 alloy steel QT, zinc-plated** — turned + centerless-ground
(internal, no corrosion exposure → stainless was over-spec; SF 13). *Or* a stock **12.9 M10 shoulder
screw.* See `MATERIALS.md`.
**DFM:** simple turned part; add a relief groove at the thread runout and a lead chamfer; one shoulder (−X) for axial location.

| Control | Callout |
|---|---|
| Running journals Ø14 | **Ø14 g6** ⌭0.01 Ⓐ (this *establishes* A); two journals coaxial |
| Cylindricity | ⌭ 0.01 on each journal |
| M10 thread pitch-Ø to A | ⤢ runout 0.05 Ⓐ |
| Shoulder face ⟂ A | ⊥ 0.02 Ⓐ |

**Finish:** journals **Ra 0.4**; thread 6g; balance Ra 1.6.
**Retention:** shoulder at −X + **M10 nylock at +X** clamps the hub/Belleville stack; medium thread-locker. Anti-rotation of the shaft in the bracket: flats or a cross-pin at one tab.

---

## 2 · Hub assembly  (CUSTOM) — OD22 × 18, Ø14 bore, **integral stop-lug + clevis ears**
**Function:** the rotating body — carries the spine, the stop-lug (open-load seat), the clevis/pin (pawl), and the clutch face.
**Consolidation:** the **lug and the two ears are FEATURES of the hub, machined as one part** (the model draws them separately). One part, no joints in the load path.
**Material/process (selected):** **6061-T6** machined, **Type-III hard-anodize on the +X friction face** (controlled µ, wear); investment-cast/MIM steel if open-load proves high.
**DFM:** generous root fillets where the lug & ears meet the hub (stress risers); the ear gap is a slot — confirm cutter access; anodize-mask the bore.

| Feature | Callout |
|---|---|
| Bore Ø14 (rides shaft) | **Ø14 H7** ⌭0.01 Ⓐ → H7/g6 running fit |
| Clutch face (B) | ⊥ 0.02 Ⓐ, flatness 0.02 |
| Pin bores, both ears Ø6 | **Ø6 H8**, ⌖ Ø0.1 Ⓐ Ⓑ (radius 12, φ105), coaxial 0.02 to each other |
| Ear gap | **10.5 +0.10/0** (pawl axial fit) |
| Lug contact face (r20, −Y) | profile ⌓ 0.1 Ⓐ Ⓑ; angular φ135 **±0.5°** Ⓐ |

**Finish:** bore **Ra 0.8**; pin bores Ra 1.6; **clutch face Ra 0.4** (then anodize); lug face Ra 1.6.
**Retention:** running fit on the shaft, **axially captured between the shaft shoulder (−X) and the Belleville stack + nut (+X)**; not keyed (it must rotate). Spine clamps to the hub OD (separate joint, out of this cluster).
**Open:** if open-load (tow/snatch) at the lug exceeds 6061 bearing, add a **steel wear pad** on the lug face or go steel hub.

---

## 3 · Pawl  (CUSTOM) — released, see Check #11
**Function:** positive fold-back stop (self-lock).
**Material/process:** **17-4PH MIM H900** (σy ~1170) — machined 4140 = prototype. ~1° draft, corners filleted.
**Strength:** controlling loaded-wall 98 MPa @ 1.5 kN → **SF 12** (Check #11).

| Feature | Callout |
|---|---|
| Pivot bore Ø6.4 (on the Ø6 pin) | **Ø6.4 H9** running; ⌭ 0.02 Ⓐ |
| Nose +Y bearing face | profile ⌓ **0.05** Ⓐ (the engagement face) |
| Nose face ⟂ to pin | ⊥ 0.05 Ⓐ |
| Heel ramp (wedge contact) | profile ⌓ 0.1 Ⓐ |
| Bore→flank fillet | **R0.8 min** (stress relief — do not break sharp) |

**Finish:** bore **Ra 0.8**; **nose bearing face Ra 0.4** (cyclic); heel Ra 1.6; MIM as-sintered elsewhere.
**Retention:** hub-facing open hook rides the pin; **axially located between the ears (gap 10.5) and biased by the torsion spring**; the load seats it on the closed +Y wall.

---

## 4 · Pawl pivot pin  (PURCHASED dowel) — Ø6 × ~22.5
**Function:** pawl pivot.
**Spec:** **Ø6 m6 hardened ground dowel pin**, A2/A4 stainless or through-hardened (ISO 8734),
length to suit ear span + retention.
**GD&T (catalog):** Ø6 m6, ⌭0.005, straightness 0.01 — supplier-controlled.
**Finish:** **Ra 0.4** ground (as-supplied).
**Retention:** **press-fit (m6) into the −X ear**, slip-fit through the pawl bore and the +X ear; **E-clip / circlip groove or staked end** on the +X side so it can't walk. The pawl spring resists axial creep.

---

## 5 · Pawl return spring  (PURCHASED/CUSTOM) — torsion, see `PAWL_SPRING`
**Function:** arms/re-seats the pawl (nose engaged).
**Spec:** **music wire ASTM A228, Ø1.0 wire, OD 8.4, 4.5 active coils, 1.57 N·mm/deg**; preload
15.7 N·mm → release 39.2 N·mm; stress 446 MPa, **SF 3.2**. Shot-peened, oil-tempered finish.
**Retention:** coil seats on the **pin or a hub boss**; **leg 1 anchored in a hub/ear hole, leg 2 bears on the pawl heel**. Define wind direction (closes onto engaged).

---

## 6 · Release wedge  (CUSTOM mold) — 33° ramp, ~8 × 8.5 × 14
**Function:** the concentrator drives it under the pawl heel; push 6 → lift ~3.9 to clear the abutment.
**Material/process:** **POM-C (acetal) injection-molded** — low friction on the ramp; ~1° draft, gate off a non-functional face.
**DFM:** uniform wall / core out any bulk to avoid sink; radius the ramp/heel junction.

| Feature | Callout |
|---|---|
| Ramp face 33° | angle **33° ±0.5°**, profile ⌓ 0.1 to the guide datum |
| Guide faces (slide in channel) | parallelism 0.05; width to a slip fit in the hub slot |
| Heel-contact pad | flatness 0.05 |

**Finish:** **ramp Ra 0.8** (low µ); molded elsewhere.
**Retention:** captured in a **guide slot** (hub/concentrator), driven by the concentrator output, returned by its bias spring (TODO_SPRING — bench). End stops at both travel limits.

---

## 7 · Friction clutch — Belleville stack  (PURCHASED) — 5 × Ø40/Ø20.4
**Function:** sets the height-hold drag torque (released by the concentrator’s friction back-off).
**Spec:** **DIN 2093 disc springs, 51CrV4**, **OD 40 / ID 20.4 / t 2.0**, 5 in series (catalog).
**Preload (spec'd):** hold **2.5 N·m** → axial **331 N** → **M10 nut torque 0.66 N·m** (`SPRING_FRICTION_CLAMP`).
Phosphate-&-oil. Discs centre on a Ø20 spigot on the hub +X face.
**GD&T:** catalog washer; the **stack height & preload are set by the nut torque** (spec the torque, not a drawing).
**Finish:** as-supplied; the **mating hub face is the controlled friction surface** (Ra 0.4, hard-anodized — see Hub).
**Retention:** stacked on the shaft/hub boss between the **hub clutch face (B)** and the **M10 nut**; nut torque = preload = drag torque.

---

## 8 · U-bracket  (CUSTOM) — 68 × 44 × 54, walls 3, **integral wall-seat + abutment**
**Function:** the fixed hinge structure; carries the shaft, the open-load **−Y wall seat** (lug), the **+Y abutment** (pawl), mounts to the case backing plate.
**Material/process (selected):** **A380 die-cast aluminum** (production) / **6061-T6 machined** (prototype). Abutment bearing 55 MPa @1.5 kN « 6061 yield → aluminum OK.
**DFM:** die-cast needs **1–2° draft** on all walls + the pocket, **uniform ~3 mm wall + ribs** (no thick bosses), generous fillets; machine only the bores + the two load faces.

| Feature | Callout |
|---|---|
| Shaft bores (both walls) Ø14 | **Ø14 H7**, coaxial **⌖ Ø0.02 Ⓐ**, this establishes A |
| Abutment | **separate ALLOY/HARDENED STEEL insert** (buttressed wedge), pressed/bonded into a bracket pocket — NOT cast integral (a 6061 post bends over @1.5 kN) |
| Abutment −Y face (pawl bearing) | profile ⌓ **0.1** Ⓐ; position **Y 11.8 ±0.1** (0.3 nose gap); contact face **Ra 0.4** (cyclic) |
| −Y wall seat (lug) | profile ⌓ 0.1 Ⓐ; set 0.3 lug clearance |
| Mounting face (B) to backing plate | flatness 0.1 |
| Tab / M10 mount holes | ⌖ Ø0.2 Ⓑ Ⓒ |
| Internal channel width | **50 ±0.1** |

**Finish:** **shaft bores Ra 0.8**; abutment & lug-seat faces **Ra 1.6**; mounting face Ra 3.2; as-cast elsewhere.
**Retention:** bolted to the **steel backing plate + case back ribs** via the tabs; the backing plate ties the U walls against splay.

---

## 9 · Bracket backing plate  (CUSTOM) — 68 × 3 × 58 steel strip
**Function:** ties the open-U walls so they can’t splay under snatch/tow.
**Material/process:** **CRS 1018 or 304** strip, **laser-cut + formed**, zinc-plated (or 304 bare).
**DFM:** flat blank, simple bends; deburr edges.

| Feature | Callout |
|---|---|
| Thickness | 3 ±0.1 |
| Flatness | 0.3 |
| Bolt holes → bracket tabs | ⌖ Ø0.2 Ⓒ |

**Finish:** Ra 3.2; zinc-plate (or passivate).
**Retention:** bolted across the bracket back at the two walls (shares the M10 ends or M5 screws); torque + thread-locker.

---

## 10 · Fasteners  (PURCHASED)
- **Pivot nut:** M10 nylock, **A2-70 stainless** (or 8.8 zinc) — torque sets the Belleville preload (spec value, bench).
- **Backing-plate / mount screws:** M5 socket cap, A2-70 + thread-locker.
- **Retention:** nylock / medium thread-locker throughout; pivot nut torque is the clutch-preload control.

---

## 11 · Concentrator  (CUSTOM mold) — ~18.5 × 10 × 26
**Function:** the "one-squeeze" router — takes a single trigger input (pivot-rod push, +Z, ~5 mm stroke)
and fans it to **three timed outputs**: friction-clutch back-off (+X), **pawl-wedge drive (−Z)**, and **stow-hook lift (+Z)**.
**Material/process (selected):** **30% GF PA66 injection-molded** (stiffness for the cam arms); POM-C if low-friction cam faces dominate. ~1° draft, cored body.
**DFM:** uniform ~3 mm wall + core the 10×10 block (no solid bulk → sink); radius the arm roots; gate off a non-cam face.

| Feature | Callout |
|---|---|
| Guide axis (slides +Z) | **Datum D**; guide faces ∥ D 0.05, sliding fit |
| 3 cam/output faces | profile ⌓ 0.1 D each |
| **Output timing (Z-phasing of the 3 cams)** | relative **±0.1** (sets the release sequence) |
| Input seat (pivot rod) | coaxial to D |

**Finish:** **cam faces Ra 0.8** (low µ); molded elsewhere.
**Retention:** captured in its **guide channel**, driven by the pivot rod from the trigger, **returned by the trigger-return spring**; hard stops at both travel ends.
**Open:** the **~4× input→output ratio and the cam profiles are VALIDATE (bench)** — see master §7.

---

## 12 · Stow latch  (two parts) — holds the handle folded at θ=0 (light load, ~18 N spec)

### 12a · Stow hook  (CUSTOM mold) — on the hub at φ315, ~6 × 15 × 9
**Function:** cradles the fixed stow pin at θ=0 to hold the handle stowed; the concentrator **lifts it to unlatch**, then deploy (θ→45) swings it clear.
**Material/process (selected):** **30% GF PA66 molded** (light duty) or zinc; sprung to engage.
**DFM:** uniform wall, radius the cradle & lip roots, 1° draft.

| Feature | Callout |
|---|---|
| Cradle face (on the Ø5 pin) | profile ⌓ 0.2 Ⓐ; **0.3 cradle clearance** |
| Lip overlap (retains the pin) | 1.5 ±0.1 engagement |
| Hub mount / pivot | ⌖ Ø0.2 Ⓐ at r16, φ315 |

**Finish:** cradle **Ra 1.6**; molded elsewhere.
**Retention:** mounts to the hub; **sprung to engage (~18 N (`STOW_HOOK_SPRING_N`), `TODO_STOW_HOOK_SPRING_N` — bench)**; lifted by the concentrator’s stow output to release.

### 12b · Stow pin  (PURCHASED dowel) — Ø5 across the bracket, r16 @ φ315
**Function:** the fixed catch the hook cradles.
**Spec:** **Ø5 m6 hardened ground dowel**, A2/A4 stainless, length ≈ 56 (spans both walls).
**GD&T:** Ø5 m6; **∥ 0.1 Ⓐ**; position ⌖ Ø0.2 Ⓐ at r16/φ315 (catch alignment).
**Finish:** **Ra 0.4** ground (as-supplied).
**Retention:** **press-fit into both bracket walls** (or integral cast boss); the cast-in option removes a part.

---

## FEA results  (`scripts/fea_pivot.py`, numpy — no external solver)

**Pawl — 2D plane-stress FEM** (CST, load plane, t=10 mm, fold-back 1.5 kN on the +Y flank,
bonded-pin bore reaction). **Mesh-convergence** (peak von Mises vs element size h):

| h (mm) | nodes | elems | peak vM |
|---|---|---|---|
| 0.30 | 458 | 748 | 108 |
| 0.20 | 1016 | 1786 | 104 |
| 0.15 | 1793 | 3254 | 108 |
| 0.12 | 2765 | 5120 | 105 |

→ **converged peak ≈ 105 MPa → SF ≈ 11** on 17-4PH H900 (yield 1170). Matches the Check #11
hand calc (98 MPa / SF 12) — the beefed pawl is well clear of yield.

**Closed-form confirmation** (clean geometries — FEM adds nothing):

| Part | Load | Stress | SF |
|---|---|---|---|
| Shaft Ø14 (bending, span 56) | 960 N | 50 MPa, δ 0.009 mm | 20 |
| Pin Ø6 (double shear) | 1.5 kN | 27 MPa | 19 |
| Abutment bearing (steel insert) | 1.5 kN | 56 MPa | 18 |
| **Abutment post bending (steel)** | 1.5 kN | 264 MPa | **3.8 ← lowest** |
| Hub lug bearing (6061) | 960 N | 16 MPa | 17 |
| Clevis ear root bending (6061) | 750 N/ear | 39 MPa | 7.1 |

### ⚠ Flaw found & fixed — abutment was a slender post that yielded
The "lowest-margin" look exposed that **SF 4.9 was only the bearing** — the abutment was a
**5 mm-thick, 15 mm-tall 6061 post cantilevered off the floor with nothing behind it**, taking
the full 1.5 kN side-load at the top: **post bending 702 MPa → SF 0.39 — it bends over.** Real
bearing was also only **SF 3.2** (the 7 mm post is narrower than the 10 mm pawl, so only 6.5 mm
engaged). **Fix:** redesigned as a **buttressed wedge STEEL insert** — vertical contact face,
deep sloped base where the moment peaks, full pawl width, kept compact (base Y≤18.3) to clear
the drawbar, and carved along the lug + drawbar sweeps. **Must be alloy/hardened steel** (y≈1000
→ bending SF 3.8; mild steel y250 would be SF 0.9). Render: `abutment_buttress.png`.

### ⚠ Flaw found & fixed — clevis was disconnected from the hub
A load-path review of the **pawl-hold chain** (hub → ears → pin → pawl → abutment) found the
**clevis ears rooted at r14 while the hub OD is only r11 — a 3 mm radial gap, `ears ∩ hub = 0`.**
The ears (which carry the *entire* fold-back reaction) were a floating body: the load path was
broken at the first link. **Fix:** rooted the ears at **r8.5** (into the hub wall) → integral
clevis, `ears ∩ hub = 45 mm³`, and notched a lug-clearance so the deeper clevis clears the
stop-lug (30° away). Ear volume 311 → 488 mm³; root bending **SF 7.1**. Renders:
`joint_ear_gap.png` (the flaw) → `joint_ear_fixed.png` (connected).

**Verdict:** after the two flaw fixes (clevis-to-hub connection, steel buttressed abutment), every
pivot part clears the projected 1.5 kN with **SF ≥ ~3.8**; the pawl is FEM-confirmed at **SF ~11**.
Lowest margin is now the **steel abutment post-bending (SF 3.8)** — acceptable, and the item to
re-check first if the bench fold-back load comes in above 1.5 kN.

**Caveats (for formal sign-off):** 2D plane-stress + CST (slightly stiff) + bonded-bore (vs
contact) idealisations; a 3D contact FEM on the final mesh is the release-grade check. But the
convergence + hand-calc agreement give high confidence the parts are far from yield.

## Connection audit — "stress-blind" sweep of the joint load chain
The interference checks test *clearance*, so a part that should be welded/bolted but reads
**0 mm³ overlap** looks identical to one correctly held apart.  A load-path audit
(`telescoping poles → hub → shaft → bracket(frame) → case`) found **three broken/absent
connections** the checks were blind to:

| Rigid interface | Before | After fix |
|---|---|---|
| spine (poles) → hub | 181 mm³ | ✅ already solid |
| bracket → backplate (frame) | 1207 mm³ | ✅ already solid |
| **clevis ears → hub** | **0 (3 mm gap)** | rooted into hub → **45 → 28 mm³** |
| **stop-lug → hub** | **0 (coincident)** | rooted 2 mm in → **106 mm³** |
| **bracket → CASE** | **0 (not fastened)** | 4× M6 + steel backing plate → bolts∩backplate **339 mm³** |
| hub↔shaft, shaft↔bracket, dowel↔spine | 0 | ✅ correct (running fits / bearing) |

**Bracket→case mount (new):** the entire pivot had **no attachment to the case**.  Added 4× M6
that **clamp the 3 mm case back wall between the bracket backplate and an exterior steel backing
plate** (`make_case_backing_plate`, `make_case_mount_bolts`).  Load transfer @960 N: bolt shear
**8 MPa (SF 38)**, case-wall pressure under the plate **0.29 MPa** (the plate spreads it so the
joint can't pull through / creep the shell). Render: `joint_case_mount.png`.
**Bolt preload (bench → spec'd):** M6 class 8.8, ~**6 N·m** torque → **~7 kN preload** (gentle on
the inlaid pad), vs **458 N** applied tension → joint stays clamped, **no gapping**.
**Pad → ribs:** added a **rib-frame tie** around the pad footprint in `_back_ribs`, so the joint
load feeds the back rib network + the pivot→corner diagonals, not just the local wall.

### Frame + mount load case (`fea_pivot.frame_and_mount`)
| Item | Result |
|---|---|
| **U-bracket wall splay**, 750 N side/abuse, **no backplate** | 184 MPa, splay 0.47 mm → **SF 1.5 (marginal)** |
| same **with steel backplate** (back edge tied) | 64 MPa, splay 0.09 mm → **SF 4.3** |
| → **the backplate is structurally REQUIRED** (turns a marginal cantilever into SF 4.3) | |
| Mount bolt **shear** @1.5 kN snatch | 13 MPa → SF 24 |
| Mount bolt **tension** @1.5 kN×22 mm moment | 23 MPa (458 N) → SF 28 |
| Preload vs applied | 7 kN ≫ 458 N → no gapping |

The frame is the last structural link before the case, and it clears with the backplate in place;
the mount is comfortable in shear, tension, and clamp margin.

## Sourcing — off-the-shelf (COTS) parts
The purchased items map to real catalog parts (re-spec'd to nearest stock where noted):

| Part | COTS spec | Source |
|---|---|---|
| Belleville clutch (×5) | **DIN 2093** disc spring, 51CrV4, **40 × 20.4 × 2.0** ✅ *model now matches this stock size*; discs centre on a Ø20 spigot on the hub +X face | McMaster / Aspen / Lee |
| Pawl pin | **Ø6 ISO 8734** hardened dowel, A2 stainless | McMaster |
| Stow pin | **Ø5 ISO 8734** hardened dowel, A2 stainless | McMaster |
| Pawl return spring | **music-wire torsion**, Ø1.0 wire, OD 8.4, 4.5 coils (per `PAWL_SPRING`) | McMaster / spring house |
| Hub journal | **flanged sleeve bearing** (bronze/PTFE "oilite"), Ø14 ID — *add this* (was a bare 6061 bore) | McMaster / Oilite |
| Pivot shaft + nut | Ø14 turned + M10 thread; **or resize Ø12 shoulder → stock M10 socket shoulder screw** (shaft SF 20 → 12, fine) | McMaster |
| Mount bolts (×4) | **M6 flat/countersunk SHCS**, A2-70 | std |
| Wedge / trigger / button springs | catalog **compression springs** | McMaster / Lee |

Custom (machined/molded): hub (+ integral lug & ears), pawl (17-4PH MIM), abutment (steel insert),
bracket (A380), backplate, case mount pad, wedge (POM), concentrator (GF-PA66), stow hook.
**Two sourcing wins:** a stock **shoulder screw** can replace the custom shaft, and a COTS **sleeve
bearing** gives a proper journal instead of plastic-on-steel.

## Assembly review (DFA) — *can it actually be built? **Yes.***
Verified the insertion path geometrically (`bracket ∩ hub-assembly = 0 mm³ at every drop height
+40→0 mm`). Sequence:
1. **Sub-assemble the hub** (outside the bracket — full tool access): press the sleeve bearing in;
   fit pawl + pin + torsion spring on the clevis ears (press pin, circlip); attach the spine.
2. Press the **stow pin** into the bracket walls.
3. **Drop the hub sub-assembly into the open-top U** (path proven clear at θ=0), align the bores.
4. **Slide the shaft** in from −X through wall → hub bearing → +X wall.
5. Stack the **Belleville washers** on the +X end, thread the **M10 nut**, torque to set clutch drag.
6. **Press the steel abutment insert** in from the back (+Y) — *after* the hub, so it never blocks drop-in.
7. Install **wedge + concentrator + actuation** from the spine side.
8. Bolt the **backplate** to the bracket back.
9. Mount to the case: seat against the inner wall (pad inlaid), **4× M6 from the case exterior** (flush).

**Two design decisions doubled as DFA wins:** the **open-top U** is what lets the hub drop in (a
closed frame couldn't be assembled), and making the **abutment a separate insert** (from the
strength fix) means it installs last instead of blocking the hub. **Tool access confirmed:** M10
nut (+X, external), M6 bolts (case exterior, flush), abutment press (+Y back), pin press (pre-drop).
Render: `pivot_exploded.png`.

## Springs + clutch — analytical specs (closed the bench TODOs)
First-pass specs (music wire A228; fatigue allow ~0.45·Sut; target ≥3000 cycles / QB/T 2919).
Residual = bench tuning of feel/friction only.

| Spring | d / OD / coils | F max | fatigue SF |
|---|---|---|---|
| Wedge return | 0.7 / 6.0 / 9 | 12.7 N | 1.8 |
| Trigger return | 0.7 / 6.0 / 9 | 10.9 N | 2.1 |
| Button return | 0.7 / 6.5 / 10 | 11.8 N | 1.8 |
| Stow-hook | 0.9 / 8.0 / 7 | 18 N (~15 quoted) | 1.9 |
| Drawbar detent | 0.9 / 8.0 / 6 | 19 N | 1.8 |
| Pawl return (earlier) | torsion 1.0/8.4/4.5 | 6.5 N nose | 3.2 |

**Belleville clutch** (DIN 2093 40×20.4×2 ×5 in series): hold torque **2.5 N·m** (handle weight
×~2.5) → axial **preload 331 N** → **M10 nut torque 0.66 N·m**; the concentrator backs the preload
to **132 N** (<1 N·m) to fold. Single-disc F_flat ~2.7 kN ≫ 331 N → small deflection, large
wear/release-travel margin, >2×10⁶-cycle life. Specs in `SPRING_*` constants + `fea_pivot.springs_and_clutch`.

## Release checklist (what still gates full sign-off)
1. **Confirm the 1.5 kN fold-back load** (drop/abuse bench) — re-runs Check #11 instantly.
2. **FEA** — pawl ✅ (2D, SF ~11, converged); shaft/pin/abutment/lug ✅ (closed-form, SF ≥5).
   Remaining: a **3D contact FEM** on the final mesh + the **hub ear/lug root fillets** for sign-off.
3. **Materials — selected** (`MATERIALS.md`): shaft 4140, hub 6061-T6, bracket A380, pawl 17-4PH MIM,
   abutment 4140-HRC, case PC. Residual: **coupon/lot validation** (tensile, impact, hardness).
4. **Spring rates + cam ratio (bench):** Belleville clutch preload, wedge-return spring, **stow-hook spring (~15 N)**, and the **concentrator ~4× ratio + cam profiles** (open TODOs / VALIDATE).
5. **Tolerance stack** on the pivot axis A across shaft↔hub↔bracket bores (running fit + the 0.3 clearances).
