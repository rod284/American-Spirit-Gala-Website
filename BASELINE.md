# Gravitcase 06-07-26 — Validated Design Baseline (FROZEN)

**Design name:** **Gravitcase 06-07-26**   (the validated design of record)
**Release tags:** `Gravitcase-06-07-26`, `baseline-v1-validated`   **Date:** 2026-06-07
**Status:** validated paper design (TRL 3–4) — analysis/CAD complete, pre-prototype.

This is a **hard configuration freeze**. Everything below was verified at this commit. Modifications
(the cost/complexity re-engineering) proceed on the **`simplify-v2`** branch; this baseline stays
immutable and can be returned to at any time (see *How to return*).

## What is frozen here (the validated state)
- **Verification:** all **11 interference/motion/strength checks PASS** (`scripts/check_interference.py`).
- **Loads:** standard-derived — QB/T 2155 (≥1500 N, <3 mm, ≥3000 cyc) + SATRA TM242/243/248 (`DESIGN_LOADS.md`).
- **Materials:** selected with rationale (`MATERIALS.md`).
- **Springs/clutch:** analytical specs closed (`SPRING_*` in `build_core.py`, `fea_pivot.springs_and_clutch`).
- **Release-grade dossiers (all 6 subsystems):**
  `PIVOT_MFG_RELEASE.md`, `SPINE_RELEASE.md`, `HANDLE_RELEASE.md`, `HITCH_RELEASE.md`,
  `WHEELS_RELEASE.md`, `SHELLS_RELEASE.md` — each with GD&T + FEA + BOM + DFA.
- **Analysis modules:** `fea_pivot.py`, `fea_spine.py`, `fea_handle.py`.
- **CAD:** `models/*.step` (core, suitcase, shells, pawl, abutment, clevis, receiver).
- **Design report + investor memo:** `REPORT.md`.

## Carry-forward findings (fixed at baseline; keep validated through any change)
1. Clevis & stop-lug rooted into the hub (were disconnected). 2. Bracket fastened to the case
(4×M6 + steel pad). 3. Abutment = buttressed **steel insert** (a 6061 post failed). 4. Pawl loaded-wall
beefed + filleted. 5. Spine lock holes need **steel eyelets** (wall bearing). 6. Handle cavity wants a
rib frame (SF 2.3). 7. Drawbar up-spec OD18/steel (SF 1.9).

## Known residuals (bench/lab — not CAD)
Drop/fatigue (TM242/243/248), ≥3000-cycle cycling, clutch-friction measurement, coupon lots,
TPE↔PA66 bond peel. No open *analysis* gaps.

## Lowest safety factors at baseline (the watch list)
Drawbar 1.9 → spine eyelet (fixes to 9.7) → handle cavity 2.3 → abutment 3.8 → frame splay 4.3.

## How to return to this baseline
```
git checkout baseline-v1-validated      # detached, read-only look
git checkout main                        # the baseline branch
# discard everything on a modification branch and restart from frozen:
git checkout -B simplify-v2 baseline-v1-validated
```
Regenerate any model from frozen source: `PYTHONUTF8=1 python3 scripts/build_core.py` then `export_suitcase()`.
