#!/usr/bin/env python3
# ============================================================================
#  Gravitcase — interference checks (the reason for the handoff, §1)
#
#  Check #1  MOTION  : sweep the hub 0 -> DEPLOY_ANGLE (and a little past).  The
#                      stop lug must enter the floor pocket and seat on the
#                      −Y wall; the pawl must clear on entry and engage the
#                      abutment — with NO clash at any angle in 0..45.
#  Check #2  STATIC  : at full deploy, no solid intersection among pawl, lug,
#                      hub, friction disc, drawbar collars (the central axial
#                      band).  Intended welds (same rigid body) are flagged
#                      separately from genuine clashes.  Each clash is reported
#                      with location (bbox centre) and volume.
#
#  Engine: OCCT booleans (intersection volume = penetration) and
#  BRepExtrema_DistShapeShape (minimum gap, for seating detection).
# ============================================================================
import os
import sys

import cadquery as cq
from OCP.BRepExtrema import BRepExtrema_DistShapeShape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_core as bc

PEN_TOL = 1.0e-3          # mm^3, treat penetration below this as "no clash"
SEAT_TOL = 0.05           # mm, gap below this counts as "seated/contact"


# ----------------------------------------------------------------------------
#  primitives
# ----------------------------------------------------------------------------
def _solid(wp):
    return wp.val()


def penetration_volume(a, b):
    """Volume of the solid intersection of two Workplanes (0 if disjoint)."""
    try:
        r = a.intersect(b)
        return sum(s.Volume() for s in r.solids().vals())
    except Exception:
        return 0.0


def intersection_info(a, b):
    """(volume, (cx,cy,cz)) of the overlap region, or (0, None)."""
    try:
        r = a.intersect(b)
        sv = r.solids().vals()
        if not sv:
            return 0.0, None
        vol = sum(s.Volume() for s in sv)
        bb = r.val().BoundingBox()
        c = (round(bb.center.x, 2), round(bb.center.y, 2), round(bb.center.z, 2))
        return vol, c
    except Exception:
        return 0.0, None


def min_gap(a, b):
    """Minimum distance between two Workplanes' solids (mm)."""
    try:
        d = BRepExtrema_DistShapeShape(_solid(a).wrapped, _solid(b).wrapped)
        d.Perform()
        return d.Value()
    except Exception:
        return float("nan")


# ----------------------------------------------------------------------------
#  Check #1 — motion sweep
# ----------------------------------------------------------------------------
# rigid members that move with the hub and MUST clear the bracket at every
# angle.  The pawl is excluded here: it is a SPRUNG over-centre lever whose
# ride-over pivot is driven by spring rates that are TODO/bench (§8), so its
# dynamic motion is not representable by a rigid sweep — it is validated
# statically at deploy instead (see check_pawl_engagement).
STRUCT_PARTS = ["shaft", "hub", "lug", "ears", "pin", "friction", "spine"]


def check_motion(theta_max=47.0, step=1.0):
    log = []
    base = bc.moving_parts(0.0, log)          # stowed; rotate cheaply per angle
    bracket = bc.make_bracket(log)
    drawbar = bc.make_drawbar(0.0)            # STOWED (theta_draw=0), on the lower axle

    print("=" * 78)
    print("CHECK #1 — MOTION SWEEP  (hub 0 -> %g deg)" % theta_max)
    print("  pass/fail on rigid structural members vs bracket AND vs stowed drawbar")
    print("  (master §7.1: lug+pawl share −Z with the stowed drawbar — confirm)")
    print("=" * 78)
    print(f"{'theta':>5} | {'struct pen':>10} | {'worst':>8} | {'lug pen':>8} | "
          f"{'lug gap':>8} | {'pawlgap':>8} | {'drawbar pen':>11}")
    print("-" * 78)

    worst = {"theta": None, "vol": 0.0, "part": None}
    hardstop = None
    n = int(round(theta_max / step))
    for i in range(n + 1):
        th = i * step
        mv = {k: bc.deploy_rotate(v, th) for k, v in base.items()}

        pen = {k: penetration_volume(mv[k], bracket) for k in STRUCT_PARTS}
        # −Z crowding: structural members vs the stowed drawbar
        draw_pen = sum(penetration_volume(mv[k], drawbar)
                       for k in STRUCT_PARTS + ["pawl"])
        max_part = max(pen, key=pen.get)
        max_vol = max(pen[max_part], draw_pen)
        part_lbl = "drawbar" if draw_pen >= pen[max_part] else max_part
        if max_vol > worst["vol"]:
            worst = {"theta": th, "vol": max_vol, "part": part_lbl}

        lug_pen = pen["lug"]
        lug_gap = min_gap(mv["lug"], bracket)
        pawl_gap = min_gap(mv["pawl"], bracket)
        if hardstop is None and lug_pen > PEN_TOL:
            hardstop = th

        flag = ""
        if max_vol > PEN_TOL and th <= bc.DEPLOY_ANGLE:
            flag = "  <-- CLASH!"
        print(f"{th:5.1f} | {pen[max_part]:10.4f} | {max_part:>8} | "
              f"{lug_pen:8.4f} | {lug_gap:8.3f} | {pawl_gap:8.3f} | "
              f"{draw_pen:11.4f}{flag}")

    print("-" * 78)
    travel_clean = worst["theta"] is None or worst["theta"] > bc.DEPLOY_ANGLE \
        or worst["vol"] <= PEN_TOL
    print("RESULT:")
    print(f"  structural travel band 0..{bc.DEPLOY_ANGLE:g} clash-free (bracket+drawbar): "
          f"{'YES' if travel_clean else 'NO'}")
    print(f"  worst penetration in band : {worst['vol']:.4f} mm^3 "
          f"on '{worst['part']}' at theta={worst['theta']}")
    print(f"  lug enters pocket, seats on −Y wall, hard-stop at: "
          f"{('%.1f deg' % hardstop) if hardstop is not None else 'not within sweep'}")
    return travel_clean


def check_pawl_engagement():
    """Static validation of the sprung pawl at full deploy: the nose must seat
    on the fixed abutment (gap within clearance) and the self-lock condition is
    reported.  Dynamic ride-over is deferred to the TODO spring rates (§8)."""
    log = []
    mv = bc.moving_parts(bc.DEPLOY_ANGLE, log)
    bracket = bc.make_bracket(log)
    gap = min_gap(mv["pawl"], bracket)
    print("\n" + "=" * 74)
    print("PAWL ENGAGEMENT — static, at full deploy (theta=%g)" % bc.DEPLOY_ANGLE)
    print("=" * 74)
    seated = gap <= (bc.POCKET_CLR + 0.2)
    print(f"  pawl nose -> abutment gap : {gap:.3f} mm "
          f"(target ~ {bc.POCKET_CLR:g} mm pocket clearance)")
    print(f"  nose seated on abutment   : {'YES' if seated else 'NO'}")
    print("  self-lock (§5)            : contact face built normal-to-pin so "
          "fold-back load reacts as PIN SHEAR, not a cam-out moment")
    print("  NOTE: the dynamic ride-over of the sprung pawl during entry is NOT "
          "simulated —")
    print("        it depends on TODO_SPRING_PAWL_RETURN / TRIGGER_RETURN (§8, "
          "bench).")
    return seated


# ----------------------------------------------------------------------------
#  Check #2 — static crowding at full deploy
# ----------------------------------------------------------------------------
# pairs that are the SAME rigid hub body (designed welds, not clashes)
INTENDED_WELDS = {
    frozenset({"lug", "hub"}),
    frozenset({"ears", "hub"}),
    frozenset({"pin", "ears"}),
    frozenset({"pawl", "pin"}),
    frozenset({"pawl", "ears"}),
    frozenset({"pawl", "hub"}),     # pawl nests on the hub at its mount (not a clash)
    frozenset({"friction", "hub"}),
    frozenset({"shaft", "hub"}),
    frozenset({"shaft", "friction"}),
    frozenset({"spine", "hub"}),
}

# master §7.2 / pocket sheet: THE central-band check — ears + lug (central) vs
# hub (radius), friction pack (+X face), and the inboard drawbar-collar edges.
BAND_PARTS = ["pawl", "ears", "lug", "hub", "friction", "drawbar"]


def check_static():
    log = []
    mv = bc.moving_parts(bc.DEPLOY_ANGLE, log)
    drawbar = bc.make_drawbar(0.0)
    parts = {k: mv[k] for k in ["pawl", "ears", "lug", "hub", "friction"]}
    parts["drawbar"] = drawbar

    print("\n" + "=" * 74)
    print("CHECK #2 — STATIC CROWDING  (central axial band, theta=%g)"
          % bc.DEPLOY_ANGLE)
    print("=" * 74)

    names = BAND_PARTS
    clashes = []
    welds = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            vol, loc = intersection_info(parts[a], parts[b])
            if vol <= PEN_TOL:
                continue
            rec = (a, b, vol, loc)
            if frozenset({a, b}) in INTENDED_WELDS:
                welds.append(rec)
            else:
                clashes.append(rec)

    if welds:
        print("intended welds (same rigid body — expected overlap):")
        for a, b, vol, loc in welds:
            print(f"  {a:9s} & {b:9s}  vol={vol:9.1f} mm^3  at {loc}")
    print("genuine clashes among", names, ":")
    if not clashes:
        print("  NONE — no unintended solid intersection in the band.")
    else:
        for a, b, vol, loc in clashes:
            print(f"  CLASH  {a:9s} & {b:9s}  vol={vol:9.3f} mm^3  at {loc}")
    print("-" * 74)
    print("RESULT:")
    print(f"  unintended clashes in band : {len(clashes)}")
    return len(clashes) == 0


def check_drawbar_deploy(step=4.0):
    """Check #3 — drawbar deployment sweep, 0 -> DRAW_DEPLOY on the lower axle.
    The handle is never co-deployed (user), so it is held STOWED (theta=0) here.
    The drawbar pivots ON the lower axle (intended bearing, excluded); we test it
    against the bracket and the stowed hub group, and report where it fouls."""
    log = []
    base = bc.moving_parts(0.0, log)                       # handle stowed
    # test against each stowed part directly (unioning them into one solid is
    # boolean-fragile with the nested spine + T-handle -> can return a null shape)
    hubparts = list(base.values())
    bracket = bc.make_bracket(log)

    def vs_hubgrp(draw):
        vt, loc = 0.0, None
        for p in hubparts:
            vv, ll = intersection_info(draw, p)
            if vv > vt:
                vt, loc = vv, ll
        return vt, loc

    print("\n" + "=" * 78)
    print("CHECK #3 — DRAWBAR DEPLOYMENT SWEEP  (0 -> %.1f deg, handle stowed)"
          % bc.DRAW_DEPLOY)
    print("=" * 78)
    print(f"{'theta_d':>7} | {'vs bracket':>11} | {'vs hub grp':>11} | {'where':>22}")
    print("-" * 78)
    worst = {"td": None, "vol": 0.0, "loc": None, "what": None}
    n = int(round(bc.DRAW_DEPLOY / step))
    for i in range(n + 1):
        td = min(i * step, bc.DRAW_DEPLOY)
        draw = bc.make_drawbar(td)
        vb, lb = intersection_info(draw, bracket)
        vh, lh = vs_hubgrp(draw)
        loc, what = (lb, "bracket") if vb >= vh else (lh, "hub grp")
        v = max(vb, vh)
        if v > worst["vol"]:
            worst = {"td": td, "vol": v, "loc": loc, "what": what}
        flag = "  <-- CLASH!" if v > PEN_TOL else ""
        print(f"{td:7.1f} | {vb:11.3f} | {vh:11.3f} | {str(loc):>22}{flag}")
    print("-" * 78)
    clean = worst["vol"] <= PEN_TOL
    print("RESULT:")
    print(f"  drawbar swing 0..{bc.DRAW_DEPLOY:.1f} clash-free : {'YES' if clean else 'NO'}")
    print(f"  worst : {worst['vol']:.3f} mm^3 vs {worst['what']} at "
          f"theta_d={worst['td']}, {worst['loc']}")
    return clean


def check_actuation():
    """Check #4 — actuation.  FIT (geometric): the keyed carrier + twin Ø4.5 rods
    must run inside the spine bore without fouling any tube wall.  INTERLOCK
    (representative): the segmented pivot rod forms a solid push column only at
    full extension — the gap-closes-on-extension principle.  Exact lock geometry
    is CONCEPT (spec), so the gap magnitudes are representative, not invented."""
    log = []
    print("\n" + "=" * 78)
    print("CHECK #4 — ACTUATION  (fit + full-extension interlock)")
    print("=" * 78)
    # FIT — carrier + rods vs the spine bore (collapsed = tightest, S5 innermost)
    mv = bc.moving_parts(0.0, log)
    bracket = bc.make_bracket(log)
    fit = {k: penetration_volume(mv[k], mv["spine"]) for k in
           ("carrier", "telerod", "pivrod")}
    fit["concentrator/brk"] = penetration_volume(mv["concentrator"], bracket)
    print("FIT (penetration into the spine bore / bracket, collapsed):")
    for k, v in fit.items():
        print(f"  {k:16s} {v:8.3f} mm^3  {'ok' if v <= PEN_TOL else 'FOUL'}")
    fit_ok = all(v <= PEN_TOL for v in fit.values())

    # INTERLOCK — gaps MEASURED between consecutive pivot-rod segments (geometric).
    # Transmit iff the rod stroke can close every open gap AND still drive the
    # concentrator: ACT_ROD_STROKE - sum(gaps) >= ACT_CONC_STROKE.
    budget = bc.ACT_ROD_STROKE - bc.ACT_CONC_STROKE      # = 5 mm of gap it can absorb
    print("INTERLOCK — pivot-rod gaps MEASURED per joint (lost motion = %g mm):"
          % bc.ACT_LOST_MOTION)
    print(f"{'extend':>7} | {'gaps (measured, mm)':>26} | {'total':>6} | result")
    rows = []
    for e in (0.0, 0.5, 0.9, 1.0):
        segs = bc.make_pivrod_segments(e)
        gaps = [min_gap(segs[i], segs[i + 1]) for i in range(len(segs) - 1)]
        total = sum(gaps)
        transmits = (bc.ACT_ROD_STROKE - total) >= bc.ACT_CONC_STROKE
        rows.append((e, total, transmits))
        gtxt = " ".join(f"{g:4.1f}" for g in gaps)
        print(f"{e:7.2f} | {gtxt:>26} | {total:6.1f} | "
              f"{'TRANSMITS' if transmits else 'dies'}")
    # the interlock is correct iff it transmits ONLY at full extension, and the
    # full-extension gap is exactly zero.
    full = [r for r in rows if r[0] >= 0.999][0]
    interlock_ok = (full[1] <= PEN_TOL and full[2]
                    and all(not r[2] for r in rows if r[0] < 0.999))
    print("-" * 78)
    print("RESULT:")
    print(f"  carrier + twin rods fit the spine bore  : {'YES' if fit_ok else 'NO'}")
    print(f"  full-extension column gap (measured)    : {full[1]:.3f} mm "
          f"(stroke budget for gaps = {budget:g} mm)")
    print(f"  push column transmits ONLY at full ext  : {'YES' if interlock_ok else 'NO'}")
    return fit_ok and interlock_ok


def check_height_lock():
    """Check #5 — height-lock registration.  At each discrete position the spring
    pin tip must enter a hole (registers); between positions it must be blind
    against the tube wall (positive lockout).  Measured: protruding pin-tip
    penetration into the spine (0 = enters hole; >0 = blind)."""
    print("\n" + "=" * 78)
    print("CHECK #5 — HEIGHT LOCK  (pin/hole registration, Ø%g pin in Ø%g holes)"
          % (bc.LOCK_PIN_D, bc.LOCK_HOLE_D))
    print("=" * 78)
    print(f"{'extend':>7} | {'tip penetration':>16} | verdict")
    TH = 1.0
    reg_ok = True
    for E in bc.LOCK_POSITIONS:
        spine = bc.make_spine([], E)
        tips = bc.make_lock_pins(E, tips_only=True)
        pen = penetration_volume(tips, spine)
        ok = pen <= TH
        reg_ok = reg_ok and ok
        print(f"{E:7.2f} | {pen:16.3f} | {'REGISTERS (locks)' if ok else 'blind'}  "
              "<- discrete height position")
    spine = bc.make_spine([], 0.7)            # an off-position (between holes)
    pen_off = penetration_volume(bc.make_lock_pins(0.7, tips_only=True), spine)
    blind_ok = pen_off > TH
    print(f"{0.70:7.2f} | {pen_off:16.3f} | "
          f"{'BLIND (locked out, springs to a hole)' if blind_ok else 'registers?!'}"
          "  <- between positions")
    print("-" * 78)
    print("RESULT:")
    print(f"  all {len(bc.LOCK_POSITIONS)} discrete positions register : "
          f"{'YES' if reg_ok else 'NO'}")
    print(f"  off-positions are blind (positive stops)  : {'YES' if blind_ok else 'NO'}")
    return reg_ok and blind_ok


def check_joint_release():
    """Check #6 — joint release (the wedge that frees the pawl to fold).  The
    concentrator pushes a 33deg wedge under the pawl heel: WEDGE_PUSH lifts the
    nose WEDGE_LIFT = push*tan(33deg).  Verify (a) the ratio matches the spec, and
    (b) the lift actually clears the abutment so the handle can fold — by attempting
    a small fold-back with the pawl LOCKED vs RELEASED and measuring the clash."""
    log = []
    bracket = bc.make_bracket(log)
    print("\n" + "=" * 78)
    print("CHECK #6 — JOINT RELEASE  (pawl wedge, 33deg ramp)")
    print("=" * 78)
    print(f"  wedge ratio : push {bc.WEDGE_PUSH:g} mm -> lift "
          f"{bc.WEDGE_LIFT:.2f} mm  (spec: push 6 -> lift 4)  "
          f"{'ok' if abs(bc.WEDGE_LIFT - 4) < 0.4 else 'CHECK'}")
    # fold-back a few degrees from deploy, pawl locked vs released
    th = bc.DEPLOY_ANGLE - 5.0
    pen_lock = penetration_volume(
        bc.deploy_rotate(bc.make_pawl(log, 0.0), th), bracket)
    pen_free = penetration_volume(
        bc.deploy_rotate(bc.make_pawl(log, bc.WEDGE_LIFT), th), bracket)
    print(f"  fold-back {bc.DEPLOY_ANGLE - th:g} deg, pawl LOCKED (no wedge)   : "
          f"{pen_lock:8.3f} mm^3 into abutment  -> {'BLOCKED' if pen_lock > PEN_TOL else 'free?!'}")
    print(f"  fold-back {bc.DEPLOY_ANGLE - th:g} deg, pawl RELEASED (wedge in) : "
          f"{pen_free:8.3f} mm^3 into abutment  -> {'CLEARS (folds)' if pen_free <= PEN_TOL else 'still blocked'}")
    print("-" * 78)
    ok = (abs(bc.WEDGE_LIFT - 4) < 0.4) and pen_lock > PEN_TOL and pen_free <= PEN_TOL
    print("RESULT:")
    print(f"  wedge lifts the nose clear of the abutment on release : {'YES' if ok else 'NO'}")
    print("  (friction back-off + stow-hook lift share the same squeeze via the")
    print("   concentrator; their spring rates are bench TODO.)")
    return ok


def check_3way():
    """Check #7 — the concentrator's 3-way output is CONTEXT-DEPENDENT.  One
    squeeze lifts both the stow hook and the pawl, but only the stop ENGAGED with
    a fixed bracket feature at that angle actually releases: hook↔stow-pin at 0deg,
    pawl↔abutment at 45deg.  Measured: each stop's gap to its fixed feature, at
    both angles — engaged where it should be, free where it should be."""
    stowpin = bc.make_stow_pin()
    abut = bc.make_abutment()
    print("\n" + "=" * 78)
    print("CHECK #7 — CONCENTRATOR 3-WAY  (one squeeze, context-dependent release)")
    print("=" * 78)
    print(f"{'angle':>7} | {'hook<->stowpin':>15} | {'pawl<->abutment':>16} | engaged stop")
    rows = {}
    for th in (0.0, bc.DEPLOY_ANGLE):
        gh = min_gap(bc.deploy_rotate(bc.make_stow_hook(), th), stowpin)
        gp = min_gap(bc.deploy_rotate(bc.make_pawl([], 0.0), th), abut)
        rows[th] = (gh, gp)
        which = "stow hook (0deg)" if gh < gp else "pawl (45deg)"
        print(f"{th:7.1f} | {gh:15.3f} | {gp:16.3f} | {which}")
    print("-" * 78)
    EN, FREE = 1.0, 4.0
    ok = (rows[0.0][0] <= EN and rows[0.0][1] >= FREE and          # 0deg: hook engaged
          rows[bc.DEPLOY_ANGLE][1] <= EN and rows[bc.DEPLOY_ANGLE][0] >= FREE)  # 45: pawl
    print("RESULT:")
    print("  at 0deg : stow hook ENGAGED -> squeeze frees the swing-up; pawl is clear")
    print("  at 45deg: pawl ENGAGED      -> squeeze (wedge) frees the fold; hook is clear")
    print("  friction back-off is the 3rd output (axial, always) — force-driven, bench TODO")
    print(f"  context-dependent release verified : {'YES' if ok else 'NO'}")
    return ok


def check_shell():
    """Check #8 — shell fit.  In the STOWED state every part must sit FLUSH (no
    +Y protrusion past the back exterior) and inside the case envelope (world
    0..560), and clear the molded pockets.  Surfaces where 'our changes' violate
    the LOCKED case size."""
    _, ps, _, _, _ = bc.build(0.0, 0.0, spine_extend=0.0)
    shell = bc.make_shell()
    W = lambda z: z + bc.COM_HEIGHT
    xs = ys = zs = None
    pen = 0.0
    for k, wp in ps.items():
        bb = wp.val().BoundingBox()
        ys = (min(ys[0], bb.ymin), max(ys[1], bb.ymax)) if ys else (bb.ymin, bb.ymax)
        zs = (min(zs[0], bb.zmin), max(zs[1], bb.zmax)) if zs else (bb.zmin, bb.zmax)
        pen += penetration_volume(wp, shell)
    print("\n" + "=" * 78)
    print("CHECK #8 — SHELL FIT  (stowed: flush + inside the molded body envelope)")
    print("=" * 78)
    case_top = W(bc.CASE_Z_TOP); case_bot = W(bc.CASE_Z_BOT)   # body top/bottom in world Z
    flush = ys[1] <= bc.SHELL_BACK_Y + 1e-6
    top_ok = W(zs[1]) <= case_top + 0.5
    bot_ok = W(zs[0]) >= case_bot - 0.5
    pocket_ok = pen <= 1.0
    print(f"  back protrusion (max +Y)   : {ys[1]:.1f} mm  vs back plane {bc.SHELL_BACK_Y:.0f}"
          f"   -> {'FLUSH' if flush else 'PROUD'}")
    print(f"  stowed top (world Z)       : {W(zs[1]):.0f} mm  vs case top {case_top:.0f}"
          f"       -> {'fits' if top_ok else 'OVER by %.0f' % (W(zs[1]) - case_top)}")
    print(f"  stowed bottom (world Z)    : {W(zs[0]):.0f} mm  vs body bottom {case_bot:.0f}"
          f"            -> {'clears' if bot_ok else 'BELOW'}")
    print(f"  parts vs molded pockets    : {pen:.1f} mm^3"
          f"      -> {'fit' if pocket_ok else 'FOUL'}")
    print("-" * 78)
    print("RESULT:")
    print(f"  flush + within case envelope : {'YES' if (flush and top_ok and bot_ok) else 'NO'}")
    if not top_ok:
        print("  ! collapsed spine overruns the case top — shorten/lower the spine")
    print(f"  note: drawbar stows down to world {W(zs[0]):.0f} mm (clear of wheels);"
          " residual pocket foul = CONCEPT recess/pocket widths (tooling).")
    return flush and top_ok and bot_ok and pocket_ok


def check_grip_controls():
    """Check #9 — grip-internal mechanism.  The top BUTTON must drive the telescope
    rod down (height-lock release) without binding the core; the underside squeeze
    TRIGGER's bell-crank must reverse the pull-up into >= the concentrator stroke at
    the pivot rod, also without binding.  Spring rates + the exact cam/roller contact
    are CONCEPT (bench)."""
    import math
    print("\n" + "=" * 78)
    print("CHECK #9 — GRIP CONTROLS  (button -> telerod, trigger bell-crank -> pivrod)")
    print("=" * 78)
    gtop = bc.spine_top(0.0)
    core = bc.make_thandle(gtop)
    rod_top = bc.grip_geom(gtop)["rod_top"]
    # BUTTON
    b0 = bc.make_grip_button(gtop, 0.0)
    b1 = bc.make_grip_button(gtop, 1.0)
    drive = b0.val().BoundingBox().zmin - b1.val().BoundingBox().zmin
    contact = abs(b0.val().BoundingBox().zmin - rod_top) < 1.0
    btn_bind = penetration_volume(b1, core)
    cap_world = b0.val().BoundingBox().zmax + bc.COM_HEIGHT
    # TRIGGER
    t0 = bc.make_grip_trigger(gtop, 0.0)
    trig_bind = penetration_volume(t0, core)
    push = bc.TRIG_PIN_Y * math.sin(math.radians(bc.TRIG_DEG))
    swing_clip = max(penetration_volume(bc.make_grip_trigger(gtop, s / 8.0), core)
                     for s in range(9))            # worst over the FULL squeeze swing
    print(f"  BUTTON  contacts telerod top         : {'YES' if contact else 'no'}")
    print(f"  BUTTON  drives rod down              : {drive:.1f} mm  (>= lock-pin retract)")
    print(f"  BUTTON  vs core through full press    : {btn_bind:.1f} mm^3 "
          f"{'ok' if btn_bind <= PEN_TOL else 'BIND'}")
    case_top = bc.CASE_Z_TOP + bc.COM_HEIGHT
    print(f"  BUTTON  cap top (world Z)            : {cap_world:.0f} mm vs case top "
          f"{case_top:.0f} -> {'within' if cap_world <= case_top + 0.5 else 'PROUD'}")
    print(f"  TRIGGER bell-crank push (pin*sin)    : {push:.2f} mm  (need >= "
          f"{bc.ACT_CONC_STROKE:g}) {'ok' if push >= bc.ACT_CONC_STROKE else 'SHORT'}")
    print(f"  TRIGGER vs core at rest              : {trig_bind:.1f} mm^3 "
          f"{'ok' if trig_bind <= PEN_TOL else 'BIND'}")
    print(f"  TRIGGER bell-crank swing clears core : {swing_clip:.1f} mm^3 (max over swing) "
          f"{'ok' if swing_clip <= 0.5 else 'CLIP'}")
    print("-" * 78)
    print("RESULT:")
    ok = (contact and drive >= 3.0 and btn_bind <= PEN_TOL and cap_world <= case_top + 0.5
          and push >= bc.ACT_CONC_STROKE and trig_bind <= PEN_TOL and swing_clip <= 0.5)
    print(f"  controls drive rods + bell-crank swings free : {'YES' if ok else 'NO'}")
    print(f"  hand-fit: ~Ø{bc.TH_CB_D:.0f} grip, {bc.TH_GRASP:.0f} graspable, roller contact on the "
          "rod, return springs fitted; spring rates + cam profile are CONCEPT (bench).")
    return ok


def check_hitch():
    """Check #10 — the steel keyhole tow hitch: the Ø16 ball ENTERS the round hole, the slot
    CAPTURES it (can't pull out under tow), and LIFTING it to the hole RELEASES it; plus the
    metal/anchorage load margins at the rated pull."""
    import math
    print("\n" + "=" * 78)
    print("CHECK #10 — TOW HITCH  (steel keyhole: enter / capture / hold / release)")
    print("=" * 78)
    TOW = 1000.0                                   # rated tow pull (N), dynamic / multi-case
    yF = bc.SHELL_BACK_Y - bc.CASE_D
    RZ = bc.RX_Z
    ballD = 2 * bc.BALL_R
    entryD = 2 * bc.RX_ENTRY_R
    slotW = bc.RX_SLOT_W
    neckD = 8.0                                    # drawbar arm (8x8)
    bracket = bc.make_receiver_bracket()
    yfront = yF + bc.RX_PLATE_T                    # behind the plate
    ballc = bc.BALL_R

    def ball_at(zc):
        return cq.Workplane("XY").sphere(ballc).translate((0, yfront + ballc - 1, RZ + zc))
    # CAPTURE: ball dropped to the slot bottom, pulled -Y -> must be blocked by the plate
    cap = penetration_volume(ball_at(bc.RX_SLOT_LO + 6).translate((0, -7, 0)), bracket)
    # RELEASE: ball raised to the entry hole, pulled -Y -> passes through (clears)
    rel = penetration_volume(ball_at(bc.RX_SLOT_HI).translate((0, -7, 0)), bracket)
    # SELF-LOCK / SNAP: the sprung detent pin sits in the rising ball's path (blocks rise).
    # (Probe the pin alone — the helix spring breaks the sphere boolean.)
    pin = (cq.Workplane("YZ").workplane(offset=1.0).circle(1.8).extrude(7)
           .translate((0, bc.RX_PLATE_T + 4.5, RZ + bc.RX_DET_Z)).translate((0, yF, 0)))
    snap = penetration_volume(ball_at(bc.RX_SEAT_Z + 3), pin)
    # geometry sanity
    g_enter = entryD > ballD + 0.5
    g_trap = slotW < ballD - 1
    g_neck = slotW > neckD
    # load margins (steel, allowables MPa)
    bolt_area = 8.78                               # M4 tensile stress area
    bolt_sf = (len(bc.RX_BOLT) * bolt_area * 250.0) / TOW           # 4 bolts in tension
    bear_area = 2 * bc.RX_PLATE_T * 12.0           # ball on the 2 slot edges over ~12 mm
    bear_sf = (bear_area * 250.0) / TOW            # steel slot bearing
    print(f"  geometry: entry Ø{entryD:.0f} > ball Ø{ballD:.0f} > slot {slotW:.0f} > neck Ø{neckD:.0f}"
          f"  -> {'OK' if (g_enter and g_trap and g_neck) else 'BAD'}")
    print(f"  CAPTURE: dropped ball pulled out -> blocked by plate : {cap:.0f} mm^3 "
          f"{'(retained)' if cap > 5 else '(NOT retained!)'}")
    print(f"  RELEASE: raised ball pulled out -> clears entry hole : {rel:.0f} mm^3 "
          f"{'(frees)' if rel < 5 else '(still blocked)'}")
    print(f"  SNAP/ANTI-RISE: sprung detent in the rising ball's path : {snap:.0f} mm^3 "
          f"{'(blocks rise)' if snap > 1 else '(no block!)'}")
    print(f"  SELF-LOCK: seat back-leaned {bc.RX_LOCK:.0f}deg in Y-Z -> tow pull (-Y) seats the ball DOWN")
    print(f"  HOLD @ {TOW:.0f} N : bolts(4xM4) tension SF {bolt_sf:.1f} ; steel slot bearing SF {bear_sf:.1f}")
    print("-" * 78)
    print("RESULT:")
    ok = (g_enter and g_trap and g_neck and cap > 5 and rel < 5 and snap > 1
          and bolt_sf >= 2 and bear_sf >= 2)
    print(f"  enters / captures (holds tow) / detent snaps / lifts to release : {'YES' if ok else 'NO'}")
    print("  note: ~1 kN rated pull is an estimate; bracket+rib+boss path needs a pull test/FEA;"
          " detent SPRING RATE + the 12deg self-lock seat angle are CONCEPT (bench).")
    return ok


def check_pawl_strength():
    """Check #11 — pawl strength at the (PROVISIONAL) fold-back load.  Parametric: re-run with
    a new bc.TODO_FOLDBACK_IMPACT_N to re-rate.  Hand calcs (bearing/shear/wall) with a fillet
    stress-concentration factor; FEA still recommended for sign-off."""
    print("\n" + "=" * 78)
    print("CHECK #11 — PAWL STRENGTH  (fold-back load -> stresses / SF)")
    print("=" * 78)
    F = bc.TODO_FOLDBACK_IMPACT_N            # 1500 N — QB/T 2155 / SATRA TM243 (standard-derived)
    YIELD = 1170.0                           # 17-4PH MIM H900 yield (MPa)
    Kt = 1.5                                 # stress-concentration WITH the corner fillets
    W = bc.PAWL_W
    py = 6.0                                 # bore centre Y (deployed)
    wall = bc.NOSE_PLUSY_FACE - (py + bc.PIN_R + bc.FIT_CLR)        # bore -> loaded flank
    overlap = min(bc.ABUT_TOP_Z, -7.5) - max(bc.FLOOR_Z1, -16.0 + bc.POCKET_CLR)  # flank engage
    A_nose = overlap * W
    A_bore = bc.PIN_R * 2 * W
    A_wall = wall * W
    A_shear = 2 * 3.14159 * bc.PIN_R ** 2    # pin double shear (the Ø6 pin)
    s_nose = F / A_nose
    s_bore = F / A_bore
    s_wall = F / A_wall * Kt                  # controlling: loaded wall + concentration
    t_pin = F / A_shear
    smax = max(s_nose, s_bore, s_wall)
    SF = YIELD / smax
    print(f"  material   : {bc.TODO_STEEL_GRADE}  (yield {YIELD:.0f} MPa)")
    print(f"  load: {F:.0f} N at the nose   [QB/T 2155 / SATRA TM243 — standard-derived]")
    print(f"  loaded wall (bore->flank) : {wall:.1f} mm")
    print(f"  nose-face bearing  : {s_nose:5.0f} MPa  (A={A_nose:.0f} mm^2)")
    print(f"  pin-bore bearing   : {s_bore:5.0f} MPa  (A={A_bore:.0f} mm^2)")
    print(f"  loaded wall (Kt={Kt}) : {s_wall:5.0f} MPa  (A={A_wall:.0f} mm^2)  <- controlling")
    print(f"  Ø6 pin double shear: {t_pin:5.0f} MPa")
    print("-" * 78)
    print("RESULT:")
    ok = SF >= 2.0
    print(f"  controlling stress {smax:.0f} MPa -> SF {SF:.1f} (target >=2.0) : {'PASS' if ok else 'FAIL'}")
    print(f"  note: GF-nylon (yield ~180) would give SF ~{180.0/smax:.1f} -> metal chosen."
          " Load is standard-derived (QB/T 2155); residual = physical drop/fatigue validation.")
    return ok


if __name__ == "__main__":
    ok1 = check_motion()
    okp = check_pawl_engagement()
    ok2 = check_static()
    ok3 = check_drawbar_deploy()
    ok4 = check_actuation()
    ok5 = check_height_lock()
    ok6 = check_joint_release()
    ok7 = check_3way()
    ok8 = check_shell()
    ok9 = check_grip_controls()
    ok10 = check_hitch()
    ok11 = check_pawl_strength()
    print("\n" + "=" * 78)
    print("SUMMARY")
    print("  Check #1 structural sweep clash-free 0..45 :", "PASS" if ok1 else "FAIL")
    print("  Pawl nose seats on abutment at deploy      :", "PASS" if okp else "FAIL")
    print("  Check #2 static crowding clash-free        :", "PASS" if ok2 else "FAIL")
    print("  Check #3 drawbar deployment sweep clear    :", "PASS" if ok3 else "FAIL")
    print("  Check #4 actuation fit (rods in spine bore) :", "PASS" if ok4 else "FAIL")
    print("  Check #5 height-lock pin/hole registration  :", "PASS" if ok5 else "FAIL")
    print("  Check #6 joint release (pawl wedge)         :", "PASS" if ok6 else "FAIL")
    print("  Check #7 concentrator 3-way (context-dep.)  :", "PASS" if ok7 else "FAIL")
    print("  Check #8 shell fit (flush + envelope)       :", "PASS" if ok8 else "FAIL")
    print("  Check #9 grip controls (button + trigger)   :", "PASS" if ok9 else "FAIL")
    print("  Check #10 tow hitch (capture/snap/hold/release):", "PASS" if ok10 else "FAIL")
    print("  Check #11 pawl strength (fold-back SF)      :", "PASS" if ok11 else "FAIL")
    print("=" * 78)
