#!/usr/bin/env python3
# ============================================================================
#  Gravitcase — design-margin sweep
#
#  For each key clearance / kinematic parameter, vary it and find the threshold
#  where the relevant check flips pass->fail.  The distance from nominal to that
#  threshold is the design margin.  Surfaces the TIGHT spots.
# ============================================================================
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_core as bc
from check_interference import penetration_volume, min_gap

PEN = 1.0e-3
rows = []   # (item, nominal, fails_at, margin, units, note)


def frange(a, b, step):
    n = int(round((b - a) / step))
    return [round(a + i * step, 4) for i in range(n + 1)]


print("building fixed geometry once ...")
bracket = bc.make_bracket([])
abut = bc.make_abutment()
base0 = bc.moving_parts(0.0, [])           # stowed hub group (handle in)
stowpin = bc.make_stow_pin()

# ----------------------------------------------------------------------------
# 1. Pawl release LIFT margin (Check #6): min lift that clears the abutment on
#    fold-back, vs the wedge's actual lift.
# ----------------------------------------------------------------------------
th = bc.DEPLOY_ANGLE - 5.0
clear_lift = None
for lift in frange(0.0, 6.0, 0.2):
    pen = penetration_volume(bc.deploy_rotate(bc.make_pawl([], lift), th), abut)
    if pen <= PEN:
        clear_lift = lift
        break
rows.append(("Pawl release lift (wedge)", bc.WEDGE_LIFT, clear_lift,
             round(bc.WEDGE_LIFT - clear_lift, 2), "mm",
             "33deg wedge gives %.1f; needs %.1f to clear" % (bc.WEDGE_LIFT, clear_lift)))

# ----------------------------------------------------------------------------
# 2. Pawl ENGAGEMENT depth (Check #6 blocking): how much the nose overlaps the
#    abutment when locked = how deep the positive stop bites.
# ----------------------------------------------------------------------------
nose_foot = -16.0 + bc.POCKET_CLR
engage_depth = bc.ABUT_TOP_Z - nose_foot
rows.append(("Pawl engagement depth", round(engage_depth, 2), 0.0,
             round(engage_depth, 2), "mm", "abutment overlap with the nose"))

# ----------------------------------------------------------------------------
# 3. Lug clearance during the 0->45 entry (Check #1): tightest gap to the bracket
#    while the lug swings into the pocket (before it seats).
# ----------------------------------------------------------------------------
min_lug = min(min_gap(bc.deploy_rotate(base0["lug"], t), bracket)
              for t in frange(0.0, 44.0, 2.0))
rows.append(("Lug entry clearance", round(min_lug, 3), 0.0, round(min_lug, 3),
             "mm", "min lug<->bracket gap over 0..44 deg"))

# ----------------------------------------------------------------------------
# 4. Central-band crowding (Check #2): how far the ear can grow tangentially
#    before its +X ear fouls the lug.
# ----------------------------------------------------------------------------
lug45 = bc.deploy_rotate(base0["lug"], bc.DEPLOY_ANGLE)
foul_boss = None
for b in frange(4.5, 9.0, 0.5):
    bc.EAR_BOSS_H = b
    ears = bc.deploy_rotate(bc.make_ears([]), bc.DEPLOY_ANGLE)
    if penetration_volume(ears, lug45) > PEN:
        foul_boss = b
        break
bc.EAR_BOSS_H = 4.5
rows.append(("Ear width (vs lug)", 4.5, foul_boss,
             round((foul_boss - 4.5), 2) if foul_boss else ">4.5", "mm half-width",
             "ear fouls lug beyond this"))

# ----------------------------------------------------------------------------
# 5. Interlock lost-motion margin (Check #4): one short joint must exceed the
#    stroke budget to lock out.  Margin = lost motion - budget.
# ----------------------------------------------------------------------------
budget = bc.ACT_ROD_STROKE - bc.ACT_CONC_STROKE
rows.append(("Interlock lost-motion", bc.ACT_LOST_MOTION, budget,
             round(bc.ACT_LOST_MOTION - budget, 2), "mm",
             "one short joint (%g) vs %g budget" % (bc.ACT_LOST_MOTION, budget)))

# ----------------------------------------------------------------------------
# 6. Height-lock registration tolerance (Check #5): pin-in-hole radial slack.
# ----------------------------------------------------------------------------
reg_tol = (bc.LOCK_HOLE_D - bc.LOCK_PIN_D) / 2.0
rows.append(("Height-lock pin/hole", reg_tol, 0.0, round(reg_tol, 2), "mm/side",
             "Ø%g pin in Ø%g hole" % (bc.LOCK_PIN_D, bc.LOCK_HOLE_D)))

# ----------------------------------------------------------------------------
# 7. 3-way context separation (Check #7): gap between the FREE stop and its
#    feature at each angle (how clearly the wrong stop is disengaged).
# ----------------------------------------------------------------------------
free0 = min_gap(bc.deploy_rotate(bc.make_pawl([], 0.0), 0.0), abut)         # pawl free @0
free45 = min_gap(bc.deploy_rotate(bc.make_stow_hook(), bc.DEPLOY_ANGLE), stowpin)  # hook free @45
rows.append(("3-way free-stop sep.", round(min(free0, free45), 2), 0.0,
             round(min(free0, free45), 2), "mm", "worst free-stop disengagement"))

# ----------------------------------------------------------------------------
#  report
# ----------------------------------------------------------------------------
print("\n" + "=" * 88)
print("DESIGN-MARGIN SWEEP")
print("=" * 88)
print(f"{'item':28} | {'nominal':>9} | {'fails at':>9} | {'margin':>8} | {'units':10} | status")
print("-" * 88)


def status(name, margin):
    if "pin/hole" in name:                 # a deliberate fit tolerance, not a margin
        return "fit"
    if "lost-motion" in name:
        return "OK" if margin >= 3 else "TIGHT"
    if "engagement" in name or "free-stop" in name:
        return "OK" if margin >= 1.0 else "TIGHT"
    return "OK" if margin >= 0.6 else "TIGHT"


def fmt(v):
    return f"{v:.2f}" if isinstance(v, (int, float)) else str(v)


for item, nom, fail, margin, units, note in rows:
    m = margin if isinstance(margin, (int, float)) else 0.0
    st = status(item, m)
    print(f"{item:28} | {fmt(nom):>9} | {fmt(fail):>9} | {fmt(margin):>8} | {units:13} | "
          f"{st:5}  {note}")
print("-" * 88)
tight = [r[0] for r in rows
         if isinstance(r[3], (int, float)) and status(r[0], r[3]) == "TIGHT"]
print("TIGHT spots:", ", ".join(tight) if tight else "none")
print("=" * 88)
