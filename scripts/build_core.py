#!/usr/bin/env python3
# ============================================================================
#  Gravitcase — Pivot Core, parametric CadQuery model
#  Refactor of the rough build_core.py, driven entirely by the parameter table
#  and aligned to gravitcase_joint_master_definition.html (Rev A) — THE datum.
#
#  Datum (master §1):  O = shaft-axis centre = COM height (280 mm world),
#  modelled in a LOCAL frame with O at the origin.
#    +X along the shaft (the 14" width).   Shaft axis = X.
#    +Y fore/aft toward the case back / user (deploy).   +Z up.
#  Deploy angle theta measured in the Y-Z plane from +Z toward +Y; about +X.
#  A hub feature at hub-angle phi sits at world angle (theta + phi).
#
#  Arrangement (master §2-§3, pocket/pawl dimensioned sheets):
#    * Both stops are hub-feature -> fixed-bracket-feature:
#        stop lug (phi=135) -> fixed WALL on the −Y pocket face (open load)
#        hub PAWL (just +Y of the lug) -> fixed ABUTMENT on the +Y pocket face
#    * Bracket is a channel: two 3 mm walls tied by a −Z structural floor; the
#      fixed wall and the pawl-ear roots grow from that floor.
#    * Pawl mount ~20.5 mm wide (two 5 mm ears + 10.5 gap), central band, clears
#      the hub because the ears live radially OUTBOARD (r>14).
#    * Friction = Belleville clutch pack on the +X hub face (axis = shaft),
#      placed axially away from the lug.
#    * Drawbar = its own rotation on the shaft; on THIS (deployed-handle) case it
#      is STOWED at −Z (it only deploys on a towed case).
#
#  LOCKED = geometry/orientation/fits -> built here.
#  VALIDATE / TODO = force-driven sizing -> kept symbolic, never invented (§8).
# ============================================================================

import math
import os
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MODELS = os.path.join(ROOT, "models")
os.makedirs(MODELS, exist_ok=True)

# ============================================================================
#  Named parameters (master §5) — single source for all geometry (mm / deg)
# ============================================================================
COM_HEIGHT    = 280.0
SHAFT_DIA     = 14.0
SHAFT_X       = 35.0      # shaft spans X -35..+35 (master part table)
BRKT_INTERNAL = 50.0
WALL_T        = 3.0
HUB_OD        = 22.0
HUB_W         = 18.0
LUG_R         = 20.0      # contact radius (load-spec r=20)
LUG_W         = 10.0
LUG_PHI       = 135.0
DEPLOY_ANGLE  = 45.0
PAWL_W        = 10.0
NOSE_FACE     = 5.0
NOSE_TO_PIVOT = 14.0
PAWL_PIN_DIA  = 6.0
ENTRY_RAMP    = 35.0      # nose lead-in (ratchets open)
WEDGE_RAMP    = 33.0      # release wedge (push 6 -> lift 4)
DRAWBAR_LEN   = 150.0
COLLAR_X      = 22.0      # |X| of each drawbar collar centre
EAR_T         = 5.0
EAR_GAP       = 10.5

# --- TODO parameters — force-driven, must NOT be invented (master §7, §8) ----
TODO_FOLDBACK_IMPACT_N     = 1500.0  # STANDARD-DERIVED: QB/T 2155-2018 pull-rod load-bearing
                                     #   >=1500 N (defl <3 mm); SATRA TM243 handle 'snatch'
                                     #   (lift+drop+arrest) = the impact basis.  Residual: the
                                     #   physical drop/fatigue test to VALIDATE (>=3000 cycles).
TODO_STEEL_GRADE           = "17-4PH MIM H900"  # yield ~1170 MPa; net-shape, wear-resistant;
                                     #   machined 4140 = prototype equivalent
PAWL_DRAFT = 1.0                     # deg mould-pull draft on the pawl (MIM)
# Belleville clutch + return springs — SPEC'd analytically (fea_pivot.springs_and_clutch);
# music wire A228, fatigue SF >=1.8 (>3000 cyc, QB/T 2919).  Residual = bench feel/friction tune.
SPRING_FRICTION_CLAMP = dict(hold_Nm=2.5, preload_N=331, M10_nut_Nm=0.66, release_N=132)
SPRING_WEDGE_RETURN   = dict(d=0.7, OD=6.0, n=9, Fmax_N=12.7, SF=1.8)
SPRING_BUTTON_RETURN  = dict(d=0.7, OD=6.5, n=10, Fmax_N=11.8, SF=1.8)
#  Pawl RETURN spring — SPEC'd (was TODO ~40 "N"; reconciles as ~40 N*mm TORQUE).
#  Torsion spring on the O6 pin, music wire ASTM A228; biases the nose ENGAGED (armed).
PAWL_SPRING = dict(type="torsion, music wire ASTM A228",
                   wire_d=1.0, OD=8.4, mean_D=7.4, coils=4.5,
                   rate_Nmm_deg=1.57, preload_Nmm=15.7, release_Nmm=39.2,
                   nose_force_N=(2.6, 6.5), stress_MPa=(178, 446), stress_SF=3.2)
SPRING_TRIGGER_RETURN = dict(d=0.7, OD=6.0, n=9, Fmax_N=10.9, SF=2.1)
SPRING_DRAWBAR_LOCK   = dict(d=0.9, OD=8.0, n=6, Fmax_N=19.1, SF=1.8)
STOW_HOOK_SPRING_N    = 18.0       # ~15 N quoted; d0.9/OD8.0/7coils, SF 1.9

# ============================================================================
#  Derived geometry  (from §4/§5; LOCKED unless tagged ASSUMPTION)
# ============================================================================
SHAFT_R    = SHAFT_DIA / 2.0          # 7
HUB_R      = HUB_OD / 2.0             # 11
PIN_R      = PAWL_PIN_DIA / 2.0       # 3
WALL_IN_X  = BRKT_INTERNAL / 2.0      # 25
WALL_OUT_X = WALL_IN_X + WALL_T       # 28

POCKET_CLR = 0.3                      # master: pocket clearance ~0.3 mm
FIT_CLR    = 0.2                      # ASSUMPTION: running fit clearance

# Stop lug: radial root->22 (contact r20), 6 circ, 10 axial (X +/-5).
# Rooted 2 mm INTO the hub wall (was coincident at r=HUB_R -> 0 overlap; now a real weld).
LUG_R_IN   = HUB_R - 2.0              # root inside the hub wall (bore r7, OD r11) -> connected
LUG_R_OUT  = 22.0
LUG_CIRC   = 6.0

# Axial layout (pocket-sheet §B): lug (10) and pawl-clevis (20.5) sit SIDE BY
# SIDE along X, both central in the 50 channel, NOT stacked.  Friction on +X.
LUG_X      = 2.0                      # lug band centre -> X[-3, 7]
PAWL_X     = -5.0                     # clevis centre -> X[-15.25, 5.25]: −X ear clears
                                      #   the inboard collar edge (X=-18.5), +X ear (<=5.25)
                                      #   clears the friction pack (X>=9).  Overlaps the lug
                                      #   band in X but is 30deg away angularly (master §7.2).
# Pawl clevis: ears ROOTED ON THE HUB (r=8.5, overlapping the hub OD r11) so the clevis is
# integral with the hub — closes the 3 mm hub->ear gap that broke the pawl-hold load path.
EAR_R_IN   = 8.5                      # root inside the hub wall (bore r7, OD r11) -> connected
EAR_BOSS_H = 4.5                      # ear tangential half-width (sweepable margin)
PIN_RAD    = 12.0                     # ASSUMPTION: pin near the hub rim so the 14 mm
                                      #   nose-to-pivot lever reaches the abutment
PAWL_PHI   = 105.0                    # ASSUMPTION: pawl pivot hub-angle -> at deploy
                                      #   the pawl sits at world ~150, "just +Y of"
                                      #   the lug (world 180); tuned to seat on abut.
# Release wedge (spec): the concentrator pushes a 33deg wedge under the pawl heel;
# WEDGE_PUSH of axial push lifts the nose WEDGE_LIFT = push*tan(33deg) to clear it.
WEDGE_PUSH = 6.0                      # mm push from the concentrator (spec: "PUSH 6")
WEDGE_LIFT = WEDGE_PUSH * math.tan(math.radians(WEDGE_RAMP))   # ~3.9 mm ("lift 4")

# Friction Belleville clutch pack on the +X hub face — COTS: DIN 2093 40x20.4 disc spring
# (51CrV4), OD40/ID20.4; discs centre on a Ø20 clutch spigot turned on the hub +X face.
FRIC_R_OUT = 20.0                    # OD 40 (catalog)
FRIC_R_IN  = 10.2                    # ID 20.4 (catalog)
FRIC_X0    = HUB_W / 2.0             # 9, the +X hub face
FRIC_X1    = FRIC_X0 + 12.0          # 5x DIN 2093 40x20.4x2.0 series stack (~12 mm free)
FRIC_NDISC = 5

# Fixed wall (−Y) and fixed abutment (+Y) — ABSOLUTE deployed geometry
# (master §6: "both absolute, at theta=45 geometry. Don't mirror.")
WALL_Y0, WALL_Y1 = -8.0, -3.3         # −Y seat face at Y=-3.3 (lug −Y face at -3 -> ~0.3)
ABUT_Y0, ABUT_Y1 =  4.0,  8.0         # +Y catch face (wall-side reference)
POST_Z0, POST_Z1 = -28.0, -16.0       # wall post rises from floor to Z=-16
POST_X = 6.0                          # +/-6 (>=10 axial + boss)
NOSE_PLUSY_FACE = 11.5                # the pawl +Y bearing flank / abutment face (moved out
                                      #   from 9.0 so a real wall sits between bore and load face)
ABUT_TOP_Z      = -13.0               # abutment ledge top — nose+WEDGE_LIFT clears it,
                                      #   nose (Z=-15.7) engages it when not lifted

# Bracket channel (rough/master): floor 4 mm on −Z, walls Z -32..22
FLOOR_Z0, FLOOR_Z1 = -32.0, -28.0
WALL_Z0,  WALL_Z1  = -32.0, 22.0
WALL_Y     = 22.0                     # wall half-extent in Y
TAB_X      = 34.0                     # mount-tab outer X (M10 mount ends)

# Telescoping spine — 5-tube elongated-octagon cascade (spec sheet).
# Per tube: (bounding W, bounding D, wall).  5 mm step per section, 270 long,
# 45deg 5 mm chamfer, ~1 mm/side slide clearance (+ plastic bushing).
SPINE_TUBES = [(50.0, 37.0, 1.5),   # S1 base, bore 47x34 sockets onto the hub boss
               (45.0, 32.0, 1.5),   # S2
               (40.0, 27.0, 1.3),   # S3
               (35.0, 22.0, 1.3),   # S4
               (30.0, 17.0, 1.2)]   # S5 top / grip
SPINE_CH       = 5.0
SPINE_LEN      = 196.0                       # tube length, trimmed so the collapsed handle
                                             #   + load-bearing T-handle nests FLUSH under the
                                             #   560 top (Option B: flush, full 70 mm overlap;
                                             #   reach ~36.7" -- the joint blocks dropping the
                                             #   pole, so flush costs tube length here)
SPINE_OVERLAP  = 70.0
SPINE_BASE_Z   = 2.0                         # S1 base just above the hub boss base (lowered
                                             #   from the hub rim to help the grip nest flush)
SPINE_STEP_EXT = SPINE_LEN - SPINE_OVERLAP   # 187 (extended draw per joint)
SPINE_STEP_CLP = 0.5                         # ~true collapse (tubes nest, not stepped up)
BOSS_HW, BOSS_HD = 23.5, 17.0               # hub male boss 47x34 (engages S1)

# T-handle (load-bearing grip) at the top of S5 — single central pole -> true T.
# The RIGID molded core carries the ~960 N snatch; a soft TPE overmold (not modelled
# as a separate skin here) is grip feel only.  The core captures the top of S5 in a
# pinned + bonded stem socket (a STRUCTURAL joint, not a press-on cap).  Crossbar runs
# along X (grabbed across the hand).  Controls: a telescope BUTTON on the top face
# (centred over the stem) and a squeeze TRIGGER on the underside (pull up, drives the
# pivot rod).
# CONCEPT dimensions (proposed ergonomics — need a dedicated hand-fit pass):
TH_CB_H  = 32.0                               # crossbar section height (Z)
TH_CB_D  = 32.0                               # crossbar section depth (Y) — hand-fit pass:
                                              #   ~Ø33 effective power-grip + wall budget for
                                              #   the bell-crank swing (was 26; still comfortable)
TH_GRASP = 130.0                              # graspable span (X) ~ 95th-pct hand + clearance
TH_NECK  = 8.0                                # finger gap: S5 top -> crossbar underside
TH_STEM  = 40.0                               # core stem capture depth INTO S5
TH_RISE  = TH_NECK + TH_CB_H                   # crossbar top above the S5 tube top
# Grip-internal mechanism (representative; spring rates + cam ratios are CONCEPT/TODO).
# Both controls PUSH their rod down toward the hub: the BUTTON (top, centred) drives the
# telescope rod (telerod, X-ACT_BORE_X -> height locks); the TRIGGER (underside squeeze,
# bike-brake) drives the pivot rod (pivrod, X+ACT_BORE_X -> concentrator/deploy) via a
# bell-crank that REVERSES the pull-up into a push-down.
BTN_CAP_R   = 8.0                              # button cap radius (Ø16 top)
BTN_STEM_R  = 4.5                              # button plunger radius
BTN_TRAVEL  = 8.0                              # button press stroke (>= lock-pin retract)
TRIG_BLADE_W = 56.0                           # trigger finger-blade width (X)
TRIG_PIN_Y  = 9.0                             # bell-crank pivot (Y, toward the back/puller)
TRIG_PIN_DZ = 16.0                            # bell-crank pivot height above S5 top
TRIG_DEG    = 34.0                            # full-squeeze rotation; push = pin_Y*sin34 = 5 mm
TH_CAVITY_W = 26.0                            # internal mechanism cavity (X)
TH_CAVITY_D = 14.0                            #                            (Y)
TH_CAVITY_BACK = 15.0                         # cavity rear extent (+Y) — contains the swing arc

# ---- Core-to-S5 structural joint — LOCKED (materials selected w/ justification) -----
# Architecture: the carrier terminates BELOW the stem (see make_actuation) so the stem
# is a near-SOLID insert (fills the S5 bore, two small rod bores only).  Load path:
#   PRIMARY  = structural adhesive bond over the 40 mm annular overlap (toughened epoxy/
#              methacrylate, ~15 MPa shear, ~0.3 mm bondline);
#   BACKSTOP = a transverse dowel through the solid stem + S5 walls, with steel ferrules
#              in the (1.2 mm) aluminium walls to spread the pin bearing and resist
#              adhesive-creep pull-out.  The pin runs along Y at X=0, BETWEEN the two
#              rods, so it clears the actuation entirely.
# Materials (selected):
#   S5 tube : 6061-T6 aluminium  (standard handle-tube alloy; Fbry~386, Fty~276 MPa;
#             anodisable/weldable/low cost)
#   Core    : PA66-GF33 glass-filled nylon (design allow ~110 MPa after moisture/temp
#             knockdown of the ~190 MPa dry; tough enough for the snatch)
#   Dowel   : Ø3.5 AISI 304 (A2) stainless (corrosion; shear allow ~250 MPa)
#   Ferrule : 304 stainless bush, Ø8 OD x Ø3.5 ID, pressed into each S5 wall at the pin
JOINT_STEM_W   = 27.0                          # solid stem section (X) — fills S5 bore (27.6)
JOINT_STEM_D   = 14.0                          #                       (Y) — S5 bore 14.6
JOINT_ROD_BORE = 5.2                           # the two rod through-bores in the solid stem
JOINT_PIN_D    = 3.5                           # transverse dowels (Y), TWO, flanking the rods
JOINT_PIN_X    = 10.0                          # dowels at X=+/-10 (solid core outboard of rods)
JOINT_FERRULE_OD = 8.0                         # steel ferrule OD in the S5 wall at each pin
JOINT_PIN_DBELOW = 20.0                        # pin depth below S5 top (mid-engagement)

# Height locks (GC-2xx-lk) — DIMENSIONED here (spec left this CONCEPT).
# A spring pin on each inner tube drops radially (+Y flat) into one of N discrete
# holes in the outer tube -> positive height stops.  The telescope rod retracts
# all pins together to slide.  3 grip positions at extend = 0.6 / 0.8 / 1.0.
LOCK_PIN_D     = 3.0
LOCK_HOLE_D    = 3.4                         # 0.2 mm/side pin-in-hole clearance
LOCK_PIN_OFF   = 8.0                         # pin Z above its inner-tube base


def _step_of(e):
    return SPINE_STEP_CLP + e * (SPINE_STEP_EXT - SPINE_STEP_CLP)


LOCK_POSITIONS = [0.6, 0.8, 1.0]            # the 3 discrete height positions (extend)
LOCK_HOLE_RELZ = [_step_of(E) + LOCK_PIN_OFF for E in LOCK_POSITIONS]  # rel outer base

DRAFT_DEG = 2.0                       # ASSUMPTION: draft on would-be-cast faces
FILLET_R  = 2.0                       # master/brief: fillets R>=2
M10       = 10.0

COL = {
    "shaft":    cq.Color(0.55, 0.55, 0.60, 1.0),
    "hub":      cq.Color(0.30, 0.55, 0.85, 1.0),
    "spine":    cq.Color(0.20, 0.26, 0.32, 1.0),
    "lug":      cq.Color(0.85, 0.55, 0.20, 1.0),   # hardened
    "ears":     cq.Color(0.30, 0.55, 0.85, 1.0),
    "pawl":     cq.Color(0.85, 0.20, 0.25, 1.0),
    "pawlspring": cq.Color(0.30, 0.65, 0.85, 1.0),
    "pin":      cq.Color(0.20, 0.20, 0.22, 1.0),
    "friction": cq.Color(0.78, 0.58, 0.32, 0.9),   # bronze clutch
    "bracket":  cq.Color(0.62, 0.66, 0.70, 1.0),
    "backplate": cq.Color(0.45, 0.48, 0.52, 1.0),  # steel bracket backing strip
    "casebacking": cq.Color(0.40, 0.43, 0.47, 1.0), # steel case backing plate
    "mountbolts": cq.Color(0.15, 0.15, 0.18, 1.0),  # bracket->case mount bolts
    "drawbar":  cq.Color(0.20, 0.65, 0.45, 1.0),
    "loweraxle": cq.Color(0.50, 0.54, 0.58, 1.0),
    "fastener": cq.Color(0.15, 0.15, 0.18, 1.0),
    "carrier":  cq.Color(0.82, 0.74, 0.52, 1.0),   # GF-nylon carrier
    "telerod":  cq.Color(0.75, 0.77, 0.80, 1.0),   # SS height rod
    "pivrod":   cq.Color(0.55, 0.80, 0.85, 1.0),   # SS pivot rod (segmented)
    "concentrator": cq.Color(0.92, 0.92, 0.95, 1.0),  # POM (placeholder)
    "lockpins": cq.Color(0.90, 0.30, 0.30, 1.0),    # spring height-lock pins
    "wedge": cq.Color(0.95, 0.85, 0.30, 1.0),       # POM release wedge
    "stowhook": cq.Color(0.85, 0.45, 0.75, 1.0),    # stow latch hook (hub)
    "button": cq.Color(0.20, 0.45, 0.85, 1.0),      # telescope/height button (top)
    "trigger": cq.Color(0.90, 0.35, 0.25, 1.0),     # squeeze deploy trigger (under)
    "jointpin": cq.Color(0.80, 0.82, 0.85, 1.0),    # core-to-S5 dowel + steel ferrules
    "springs": cq.Color(0.62, 0.64, 0.68, 1.0),     # return springs (button + trigger)
    "overmold": cq.Color(0.14, 0.16, 0.20, 0.55),   # soft TPE grip skin (translucent)
    "stowpin": cq.Color(0.45, 0.48, 0.52, 1.0),     # fixed stow pin (bracket)
    "shell": cq.Color(0.72, 0.75, 0.80, 0.22),      # molded back shell (translucent)
    "brace": cq.Color(0.42, 0.34, 0.55, 1.0),       # internal steel brace
    "case":  cq.Color(0.60, 0.64, 0.70, 0.45),      # full case body (translucent)
    "rx_bracket": cq.Color(0.45, 0.47, 0.50, 1.0),  # steel keyhole receiver
    "rx_backplate": cq.Color(0.40, 0.42, 0.45, 1.0),  # steel backing plate
    "rx_bolts": cq.Color(0.15, 0.15, 0.18, 1.0),    # receiver bolts
    "rx_detent": cq.Color(0.85, 0.55, 0.20, 1.0),   # sprung detent (pin + spring)
    "case_back":  cq.Color(0.58, 0.62, 0.70, 0.55), # back (core) shell
    "case_front": cq.Color(0.66, 0.70, 0.76, 0.45), # front (packing) shell
    "zipper": cq.Color(0.20, 0.20, 0.22, 1.0),      # perimeter zipper seam
    "wheel": cq.Color(0.12, 0.12, 0.14, 1.0),       # spinner wheels
}

# ============================================================================
#  Helpers
# ============================================================================
def deploy_rotate(wp, theta_deg):
    """Rotate about +X so +Z moves toward +Y for +theta (master §1 sense)."""
    return wp.rotate((0, 0, 0), (1, 0, 0), -theta_deg)


def deploy_point(y, z, theta_deg):
    a = math.radians(theta_deg)
    return (y * math.cos(a) + z * math.sin(a),
            -y * math.sin(a) + z * math.cos(a))


def yz(alpha_deg, r):
    """(Y, Z) of a point at angle alpha (from +Z toward +Y) and radius r."""
    a = math.radians(alpha_deg)
    return (r * math.sin(a), r * math.cos(a))


def oct_prism(hw, hd, ch, z0, z1):
    pts = [(hw, hd - ch), (hw - ch, hd), (-hw + ch, hd), (-hw, hd - ch),
           (-hw, -hd + ch), (-hw + ch, -hd), (hw - ch, -hd), (hw, -hd + ch)]
    return (cq.Workplane("XY").polyline(pts).close()
            .extrude(z1 - z0).translate((0, 0, z0)))


def hex_prism_x(across_flats, x0, length):
    r = across_flats / math.sqrt(3.0)
    return (cq.Workplane("YZ").workplane(offset=x0)
            .polygon(6, 2 * r).extrude(length))


def try_op(fn, label, log):
    try:
        out = fn()
        log.append(("ok", label))
        return out
    except Exception as e:                       # noqa: BLE001
        log.append(("SKIP", f"{label}: {type(e).__name__}"))
        return None


def try_fillet(wp, selector, radius, label, log):
    try:
        out = wp.edges(selector).fillet(radius)
        log.append(("fillet ok", label))
        return out
    except Exception as e:                       # noqa: BLE001
        log.append(("fillet SKIP", f"{label}: {type(e).__name__}"))
        return wp


# ============================================================================
#  Moving (hub) parts — built in the STOWED frame, rotated by theta in assembly
# ============================================================================
def make_shaft():
    shaft = cq.Workplane("YZ").circle(SHAFT_R).extrude(SHAFT_X, both=True)
    return shaft


def make_hub():
    return (cq.Workplane("YZ").circle(HUB_R).circle(SHAFT_R)
            .extrude(HUB_W / 2, both=True))


def grip_geom(top_z):
    """Shared key Z-levels for the grip core + its controls (top_z = S5 top face)."""
    zc = top_z + TH_NECK + TH_CB_H / 2.0            # crossbar centreline
    cav_z0 = top_z + 5.0                            # mechanism cavity floor
    cav_z1 = zc + TH_CB_H / 2.0 - 4.0               # cavity ceiling (under the top skin)
    rod_top = top_z + 10.0                          # actuation rod tops — raised INTO the open
                                                    #   cavity so the controls act on them with
                                                    #   clearance (not down inside the solid stem)
    pin_z = top_z + TRIG_PIN_DZ                     # bell-crank pivot Z
    return dict(zc=zc, cav_z0=cav_z0, cav_z1=cav_z1, rod_top=rod_top, pin_z=pin_z)


def make_thandle(top_z):
    """The load-bearing T-handle core at the spine top (top_z = S5 top face).
    Rounded crossbar grip (along X) on a neck, with a structural stem captured into
    S5 (pinned + bonded).  Hollowed for the grip-internal mechanism: a central cavity
    housing the button transfer + trigger bell-crank, two rod guide bores down the
    stem, a button bore (top centre), a trigger slot (underside front), and the
    bell-crank pin bore.  Returns the rigid core solid (button/trigger are separate
    parts).  All dims CONCEPT (ergonomic hand-fit pass pending)."""
    g = grip_geom(top_z)
    zc = g["zc"]
    cb = cq.Workplane("XY").box(TH_GRASP, TH_CB_D, TH_CB_H).translate((0, 0, zc))
    try:
        cb = cb.edges().fillet(7.0)
    except Exception:
        pass
    neck = (cq.Workplane("XY").box(26, 10, TH_NECK + 4, centered=(True, True, False))
            .translate((0, 0, top_z - 2)))                 # narrow (Y) so the blade clears it
    # near-SOLID structural stem (fills the S5 bore for the bond + a solid pin land);
    # the carrier ends below it (make_actuation), so only two rod bores pierce it
    stem = (cq.Workplane("XY").box(JOINT_STEM_W, JOINT_STEM_D, TH_STEM, centered=(True, True, False))
            .translate((0, 0, top_z - TH_STEM)))
    core = cb.union(neck).union(stem)
    # -- internal mechanism cavity (houses button transfer + bell-crank); deeper toward
    #    the back (+Y) to give the bell-crank its lever to the central rod --
    cav = (cq.Workplane("XY").box(TH_CAVITY_W, TH_CAVITY_BACK + 8, g["cav_z1"] - g["cav_z0"],
           centered=(True, False, False)).translate((0, -8, g["cav_z0"])))
    core = core.cut(cav)
    # -- two rod through-bores down the solid stem to the cavity (the carrier ends below,
    #    so the rods alone pierce the stem and the stem stays solid for the pinned joint) --
    for sx in (-ACT_BORE_X, ACT_BORE_X):
        core = core.cut(cq.Workplane("XY").circle(JOINT_ROD_BORE / 2.0)
                        .extrude(g["cav_z0"] - (top_z - TH_STEM - 1))
                        .translate((sx, 0, top_z - TH_STEM - 1)))
    # -- button bore through the top skin into the cavity (top, centred) --
    top_face = zc + TH_CB_H / 2.0
    core = core.cut(cq.Workplane("XY").circle(BTN_STEM_R + 0.6)
                    .extrude(top_face + 2 - g["cav_z1"]).translate((0, 0, g["cav_z1"])))
    # button cap counterbore so the cap can travel down into the top face
    core = core.cut(cq.Workplane("XY").circle(BTN_CAP_R + 0.8)
                    .extrude(BTN_TRAVEL + 5).translate((0, 0, top_face - BTN_TRAVEL - 1)))
    # -- trigger slot: underside opening (back side, toward the puller) into the cavity;
    #    the bell-crank neck passes here, the wide finger blade hangs below in the gap --
    slot = (cq.Workplane("XY").box(30, 16, g["cav_z0"] - (top_z + 1) + 4,
            centered=(True, True, False)).translate((0, TRIG_PIN_Y, top_z + 1)))
    core = core.cut(slot)
    # -- bell-crank pivot pin bore (axis along X) --
    core = core.cut(cq.Workplane("YZ").circle(1.6).extrude(TH_GRASP, both=True)
                    .translate((0, TRIG_PIN_Y, g["pin_z"])))
    # (the structural joint dowel bore is cut in make_spine, after the S5 tube + core are
    #  unioned, so the dowel passes through BOTH; it runs along Y at X=0, between the rods)
    return core


def make_coil(coil_r, wire_r, length, turns):
    """A helical compression coil (axis +Z) for representing return springs."""
    helix = cq.Wire.makeHelix(pitch=length / turns, height=length, radius=coil_r)
    prof = cq.Workplane("XZ").center(coil_r, 0).circle(wire_r)
    return prof.sweep(cq.Workplane(obj=helix), isFrenet=True)


def make_grip_springs(top_z, press=0.0, squeeze=0.0):
    """Representative return springs (rates are CONCEPT/TODO, §8 bench): a compression
    coil around the button plunger (returns the height button) and a coil biasing the
    trigger bell-crank back to rest.  Geometry only — confirms the springs fit."""
    g = grip_geom(top_z)
    web_z = g["cav_z1"] - 9.0
    # button return: coil around the plunger, web -> cavity ceiling; shortens with press
    L = (g["cav_z1"] - web_z) - press * BTN_TRAVEL * 0.0   # envelope (compresses in service)
    btn_sp = make_coil(BTN_STEM_R + 2.0, 0.7, max(L - 1, 4), 5).translate((0, 0, web_z + 0.5))
    # trigger return: a small torsion-style coil about the pivot pin at the hub end
    trig_sp = (make_coil(3.4, 0.55, 8, 5)
               .rotate((0, 0, 0), (0, 1, 0), 90)               # lay the coil along X
               .translate((JOINT_PIN_X + 1.0, TRIG_PIN_Y, g["pin_z"])))
    return btn_sp.union(trig_sp)


def make_overmold(top_z):
    """Soft TPE grip overmold — a ~3 mm skin over the rigid crossbar (the hand surface;
    feel only, no load).  Openings for the button (top) and the trigger (underside)."""
    g = grip_geom(top_z); zc = g["zc"]
    out = cq.Workplane("XY").box(TH_GRASP + 6, TH_CB_D + 6, TH_CB_H + 6).translate((0, 0, zc))
    try:
        out = out.edges().fillet(9.0)
    except Exception:
        pass
    inner = cq.Workplane("XY").box(TH_GRASP + 0.6, TH_CB_D + 0.6, TH_CB_H + 0.6).translate((0, 0, zc))
    over = out.cut(inner)                                        # 3 mm shell
    over = over.cut(cq.Workplane("XY").circle(BTN_CAP_R + 1.5).extrude(12)
                    .translate((0, 0, zc + TH_CB_H / 2.0 - 3)))  # button opening (top)
    over = over.cut(cq.Workplane("XY").box(TRIG_BLADE_W + 6, 16, 16, centered=(True, True, False))
                    .translate((0, TRIG_PIN_Y, top_z + 1)))      # trigger finger access (under)
    return over


def make_grip_button(top_z, press=0.0):
    """Top telescope BUTTON: a thumb cap + plunger down through the top skin into the
    cavity, with a transfer web + prong onto the telerod (X-ACT_BORE_X).  press 0..1
    drives it down BTN_TRAVEL -> telerod down -> height-lock pins retract."""
    g = grip_geom(top_z)
    top_face = g["zc"] + TH_CB_H / 2.0
    web_z = g["cav_z1"] - 9.0                        # transfer web kept HIGH in the cavity
    cap = (cq.Workplane("XY").circle(BTN_CAP_R).extrude(4.0)
           .translate((0, 0, top_face - 1.0)))
    stem = (cq.Workplane("XY").circle(BTN_STEM_R)
            .extrude(top_face - 1.0 - web_z).translate((0, 0, web_z)))
    web = (cq.Workplane("XY").box(ACT_BORE_X + 8, 9, 5, centered=(False, True, False))
           .translate((-ACT_BORE_X - 4, 0, web_z)))
    prong = (cq.Workplane("XY").circle(ACT_ROD_R)        # long prong web -> telerod top
             .extrude(web_z + 1.0 - g["rod_top"]).translate((-ACT_BORE_X, 0, g["rod_top"])))
    btn = cap.union(stem).union(web).union(prong)
    return btn.translate((0, 0, -press * BTN_TRAVEL))


def make_joint_pin(top_z):
    """The core-to-S5 structural dowel + the two steel ferrules pressed into the S5
    aluminium walls (the pin-bearing reinforcement).  Runs along Y at X=0, between the
    two rods, mid-engagement of the 40 mm stem capture."""
    pin_z = top_z - JOINT_PIN_DBELOW
    part = None
    for sx in (-JOINT_PIN_X, JOINT_PIN_X):
        dowel = (cq.Workplane("XZ").circle(JOINT_PIN_D / 2.0).extrude(9.0, both=True)
                 .translate((sx, 0, pin_z)))
        part = dowel if part is None else part.union(dowel)
        for sy in (-1, 1):                          # ferrule bushes spread the pin bearing
            fer = (cq.Workplane("XZ").circle(JOINT_FERRULE_OD / 2.0).circle(JOINT_PIN_D / 2.0)
                   .extrude(2.0, both=True).translate((sx, sy * 7.5, pin_z)))
            part = part.union(fer)
    return part


def make_grip_trigger(top_z, squeeze=0.0):
    """Underside squeeze TRIGGER (bike-brake): a wide finger blade hanging below the
    crossbar, a neck up through the underside slot to a bell-crank hub on the pivot
    pin, and an actuator arm + prong onto the pivrod (X+ACT_BORE_X).  squeeze 0..1
    rotates it TRIG_DEG; the bell-crank REVERSES the pull-up into a push-down -> the
    prong drives the pivrod down (>= the concentrator stroke)."""
    g = grip_geom(top_z)
    py, pz = TRIG_PIN_Y, g["pin_z"]
    # finger tab in the back-underside finger gap (small travel release trigger), at Y=py
    blade = (cq.Workplane("XY").box(TRIG_BLADE_W, 8, 6, centered=(True, True, False))
             .translate((0, py, top_z + 1)))
    try:
        blade = blade.edges("|X").fillet(2.5)
    except Exception:
        pass
    neck = (cq.Workplane("XY").box(22, 5, pz - (top_z + 7), centered=(True, True, False))
            .translate((0, py, top_z + 7)))                        # up through the slot to the hub
    hub = (cq.Workplane("YZ").circle(3.0).extrude(11, both=True)
           .translate((0, py, pz)))                                # on the pivot pin
    # actuator arm reaches FORWARD from the pin (Y=py) to over the pivrod top (Y=0, now in
    # the open cavity); the pin sits BETWEEN the blade and the rod, so pulling the blade up
    # rotates the arm DOWN.  It ends in a ROLLER (axis X) that bears/rolls on the rod top,
    # so the contact is rolling (low friction, defined travel) rather than a sliding prong.
    arm = (cq.Workplane("XY").box(10, py, 5, centered=(True, False, False))
           .translate((ACT_BORE_X, 0.0, pz - 2.5)))
    roller = (cq.Workplane("YZ").circle(2.5).extrude(4, both=True)
              .translate((ACT_BORE_X, 0.0, g["rod_top"] + 2.5)))      # roller on the rod top
    trig = blade.union(neck).union(hub).union(arm).union(roller)
    return trig.rotate((0, py, pz), (1, py, pz), squeeze * TRIG_DEG)


def make_spine(log, extend=0.0):
    """5-tube telescoping octagon spine (spec sheet), at phi=0 (+Z stowed).
    extend: 0 = collapsed (~275 mm, fits the 279 recess) -> 1 = extended
    (~1070 mm, grip ~41" at deploy).  S1 sockets onto the hub male boss; S5 is
    the grip.  Each tube's bore clears the next tube's bound by ~1 mm/side."""
    step = SPINE_STEP_CLP + extend * (SPINE_STEP_EXT - SPINE_STEP_CLP)
    # hub boss (47x34) — HOLLOW (master) so the rod carrier passes through to the hub
    spine = oct_prism(BOSS_HW, BOSS_HD, SPINE_CH, 2.0, SPINE_BASE_Z + 45.0).cut(
        oct_prism(BOSS_HW - 3, BOSS_HD - 3, SPINE_CH, 1.0, SPINE_BASE_Z + 46.0))
    top = SPINE_BASE_Z
    for i, (W, D, wall) in enumerate(SPINE_TUBES):
        hw, hd = W / 2.0, D / 2.0
        bz = SPINE_BASE_Z + i * step
        outer = oct_prism(hw, hd, SPINE_CH, bz, bz + SPINE_LEN)
        bore = oct_prism(hw - wall, hd - wall, SPINE_CH, bz - 1, bz + SPINE_LEN + 1)
        tube = outer.cut(bore)
        if i < 4:                              # outer tube of joint i -> lock holes
            for relz in LOCK_HOLE_RELZ:
                hole = (cq.Workplane("XY").circle(LOCK_HOLE_D / 2)
                        .extrude(2 * (hd + 3)).rotate((0, 0, 0), (1, 0, 0), -90)
                        .translate((0, -(hd + 3), bz + relz)))
                tube = tube.cut(hole)
        spine = spine.union(tube)
        top = bz + SPINE_LEN
    spine = spine.union(make_thandle(top))         # real T-handle grip at the top
    # -- core-to-S5 structural dowel bore: along Y, at X=0 (between the two rods), through
    #    BOTH the S5 tube walls and the solid core stem; ferrule seats counterbored into
    #    the aluminium walls.  Cut here so it pierces the unioned tube + core. --
    pin_z = top - JOINT_PIN_DBELOW
    for sx in (-JOINT_PIN_X, JOINT_PIN_X):                            # two dowels flanking rods
        spine = spine.cut(cq.Workplane("XZ").circle(JOINT_PIN_D / 2.0).extrude(40, both=True)
                          .translate((sx, 0, pin_z)))                 # dowel hole (Y axis)
        for sy in (-1, 1):                                            # ferrule seats in S5 walls
            spine = spine.cut(cq.Workplane("XZ").circle(JOINT_FERRULE_OD / 2.0)
                              .extrude(2.0, both=True).translate((sx, sy * 7.5, pin_z)))
    # relieve the boss front-lower corner for the drawbar pivot bushings (user-OK'd
    # trim of the U/boss metal); only affects the stowed handle, where the drawbar lives
    spine = spine.cut(cq.Workplane("XY").box(28, 17, 17, centered=(True, False, True))
                      .translate((0, 13, 0)))
    log.append(("ok", "spine 5-tube cascade extend=%.2f" % extend))
    return spine


# ----------------------------------------------------------------------------
#  Actuation (Rev A spec).  LOCKED: twin Ø4.5 rods + keyed GF-nylon carrier.
#  Segmentation of the pivot rod creates the full-extension interlock — the
#  exact gap/lock geometry is CONCEPT (flagged), so it is REPRESENTED here, not
#  invented; Check #4 verifies the principle (gaps close on extension).
# ----------------------------------------------------------------------------
ACT_ROD_R    = 2.25                   # Ø4.5 SS rod
ACT_BORE_X   = 4.5                    # rod centres at X = +/- 4.5 (side by side)
# Interlock — CONCRETE dimensioned lost-motion model (no longer representative):
ACT_LOST_MOTION = 12.0   # mm of designed slop at EACH of the 4 joint couplings; it is
                         #   OPEN unless that joint is at its full-extension hard stop.
ACT_ROD_STROKE  = 10.0   # mm of push one squeeze delivers at the rod
ACT_CONC_STROKE = 5.0    # mm the concentrator needs to back off friction + lift hook/pawl
#   Transmit iff  ACT_ROD_STROKE - sum(open joint gaps) >= ACT_CONC_STROKE.
#   At full extension every joint is hard-stopped -> sum(gaps)=0 -> 10>=5 transmits.
#   With even ONE joint short, that joint's 12 mm gap alone exceeds the 10 mm stroke ->
#   push dies before the hub.  So release is mechanically locked out below full height.


def spine_top(extend):
    step = SPINE_STEP_CLP + extend * (SPINE_STEP_EXT - SPINE_STEP_CLP)
    return SPINE_BASE_Z + 4 * step + SPINE_LEN


def make_pivrod_segments(extend=0.0):
    """The pivot rod's 5 segments (one per section) as separate solids.  Each
    joint carries ACT_LOST_MOTION of slop unless fully extended, where it closes
    to 0 (segments butt -> solid push column).  Returned separately so Check #4
    can MEASURE the gaps geometrically."""
    # Representative model (interlock geometry is CONCEPT per spec): 5 equal
    # segments evenly distributed up the rod, separated by ACT_LOST_MOTION when not
    # fully extended and butted (gap 0) at full extension.  Distributing along the
    # whole rod (rather than at the physically-bunched collapsed joints) keeps the
    # gaps well-posed at every extend, including collapsed.
    z0 = SPINE_BASE_Z + 5.0
    top = spine_top(extend) + 10.0       # pivrod top RAISED into the grip cavity (trigger acts here)
    total = max(top - z0, 5.0)
    gap = 0.0 if extend >= 0.999 else ACT_LOST_MOTION
    n = 5
    seg_len = max((total - (n - 1) * gap) / n, 1.0)
    segs, zlo = [], z0
    for _ in range(n):
        segs.append(cq.Workplane("XY").circle(ACT_ROD_R).extrude(seg_len)
                    .translate((ACT_BORE_X, 0, zlo)))
        zlo += seg_len + gap
    return segs


# Stow hook (master: hook on hub, pin in bracket +Z side, engages at theta=0).
STOW_PHI   = 315.0                     # hub-angle: at theta=0 the hook sits at world 315
STOW_R     = 16.0                      # pin radius from O
STOW_PIN_R = 2.5


def make_stow_pin():
    """Fixed stow pin on the bracket (between the walls), caught by the hub hook
    at theta=0 to hold the handle stowed."""
    cy, cz = yz(STOW_PHI, STOW_R)
    return (cq.Workplane("YZ").workplane(offset=-WALL_OUT_X)
            .moveTo(cy, cz).circle(STOW_PIN_R).extrude(2 * WALL_OUT_X))


def make_stow_hook():
    """Hook on the hub (hub-angle STOW_PHI) that cradles the stow pin at theta=0
    and swings clear by theta=45.  Concentrator lifts it to release the stow."""
    # built pointing +Z; the pin maps to local (Y=0, Z=STOW_R).  Arm on +Y of the
    # pin, lip over its top — both with ~0.3 mm cradle clearance.
    arm = (cq.Workplane("XY").box(6, STOW_R * 0 + 4.2, 9, centered=(True, False, False))
           .translate((0, STOW_PIN_R + 0.3, STOW_R - 6)))
    lip = (cq.Workplane("XY").box(6, 9, 1.5, centered=(True, False, False))
           .translate((0, -(STOW_PIN_R + 2), STOW_R + STOW_PIN_R + 0.3)))
    return deploy_rotate(arm.union(lip), STOW_PHI)


def make_wedge(push=0.0):
    """Release wedge (POM): a 33deg ramp the concentrator drives under the pawl
    heel; `push` slides it +Y to lift the nose (WEDGE_LIFT = push*tan33).  Built in
    the deploy frame, rotates with the hub.  Representative geometry — the lift
    kinematics are what Check #6 verifies."""
    t = math.tan(math.radians(WEDGE_RAMP))
    prof = (cq.Workplane("YZ").moveTo(-1, -13).lineTo(11, -13)
            .lineTo(11, -13 + 12 * t).lineTo(-1, -13 + 0).close())
    wedge = (prof.extrude(PAWL_W / 2 - 1, both=True)
             .translate((PAWL_X - 2, push, 0)))
    return deploy_rotate(wedge, -DEPLOY_ANGLE)


def make_lock_pins(extend=0.0, tips_only=False):
    """Spring height-lock pins, one per joint, on each inner tube's +Y flat,
    seated radially into the outer-tube hole.  tips_only returns just the
    protruding outer end (for Check #5's registration measurement)."""
    step = _step_of(extend)
    pins = None
    for i in range(4):
        hd_in = SPINE_TUBES[i + 1][1] / 2.0           # inner tube +Y flat
        pz = SPINE_BASE_Z + (i + 1) * step + LOCK_PIN_OFF
        y0, L = (hd_in + 0.5, 2.0) if tips_only else (hd_in - 1.0, 3.5)
        pin = (cq.Workplane("XY").circle(LOCK_PIN_D / 2).extrude(L)
               .rotate((0, 0, 0), (1, 0, 0), -90).translate((0, y0, pz)))
        pins = pin if pins is None else pins.union(pin)
    return pins


def make_actuation(extend=0.0):
    """Twin push-only control lines in a keyed carrier inside the spine.
    Telescope rod (height) continuous; pivot rod (deploy) segmented per section
    for the full-extension interlock (see make_pivrod_segments)."""
    z0 = 4.0
    top = spine_top(extend) + 10.0       # rod tops RAISED into the grip cavity (controls act here)
    # the keyed carrier TERMINATES below the grip stem (top - TH_STEM - 5) so the stem
    # stays solid for the structural joint; the two rods continue up through the stem
    # bores to the controls, guided there by the stem itself.
    carr_top = spine_top(extend) - TH_STEM - 5.0
    carrier = (cq.Workplane("XY").box(15, 9, carr_top - z0, centered=(True, True, False))
               .translate((0, 0, z0)))
    for xc in (-ACT_BORE_X, ACT_BORE_X):
        carrier = carrier.cut(cq.Workplane("XY").circle(ACT_ROD_R + 0.4)
                              .extrude(carr_top - z0 + 2).translate((xc, 0, z0 - 1)))
    telerod = (cq.Workplane("XY").circle(ACT_ROD_R)
               .extrude(top - z0 - 2).translate((-ACT_BORE_X, 0, z0 + 1)))
    pivrod = None
    for seg in make_pivrod_segments(extend):
        pivrod = seg if pivrod is None else pivrod.union(seg)
    # concentrator (POM) — one input (pivot rod, +Z) fanned to THREE outputs:
    #   friction (+X axial), pawl wedge (toward −Z), stow hook (toward +Z).
    #   Representative geometry; the ~4x ratio + cam profiles are VALIDATE (bench).
    body = cq.Workplane("XY").box(10, 10, 10, centered=(True, True, False)).translate((0, 0, 1))
    f_arm = cq.Workplane("XY").box(6, 5, 4, centered=(False, True, False)).translate((4, 0, 1))
    h_arm = cq.Workplane("XY").box(5, 5, 5, centered=(True, True, False)).translate((0, 0, 11))
    w_arm = cq.Workplane("XY").box(5, 5, 10, centered=(True, True, False)).translate((-6, 0, -10))
    conc = body.union(f_arm).union(h_arm).union(w_arm)
    return {"carrier": carrier, "telerod": telerod, "pivrod": pivrod,
            "concentrator": conc}


def make_stop_lug(log):
    """Radial lug at phi=135: r14->22 (rooted at hub rim), 6 circ, 10 axial."""
    blk = (cq.Workplane("XY")
           .box(LUG_W, LUG_CIRC, LUG_R_OUT - LUG_R_IN, centered=(True, True, False))
           .translate((LUG_X, 0, LUG_R_IN)))
    blk = try_fillet(blk, "|Z", FILLET_R, "lug corners", log)
    return deploy_rotate(blk, LUG_PHI)


def make_ears(log):
    """Clevis: two ears (EAR_T each, EAR_GAP apart) rooted radially outboard
    (r>=EAR_R_IN) carrying the Ø6 pin at r=PIN_RAD.  Offset axially by PAWL_X."""
    half = EAR_GAP / 2.0
    boss_h = EAR_BOSS_H                           # tangential half-width (houses Ø6 pin);
                                                  # trimmed so the +X ear clears the lug
    r_out = PIN_RAD + 6.0
    one = (cq.Workplane("XY")
           .box(EAR_T, 2 * boss_h, r_out - EAR_R_IN, centered=(True, True, False))
           .translate((0, 0, EAR_R_IN)))
    earL = one.translate((PAWL_X + half + EAR_T / 2.0, 0, 0))
    earR = one.translate((PAWL_X - half - EAR_T / 2.0, 0, 0))
    ears = earL.union(earR)
    pin_hole = (cq.Workplane("YZ").workplane(offset=PAWL_X - (half + EAR_T + 0.5))
                .moveTo(0, PIN_RAD).circle(PIN_R + FIT_CLR)
                .extrude(2 * (half + EAR_T + 0.5)))
    ears = ears.cut(pin_hole)
    # clearance for the stop-lug (LUG_PHI, 30deg away): now the clevis is rooted on the hub
    # it would foul the lug — notch it back along the lug's swept zone (built at the relative
    # angle so it lands on the lug after the PAWL_PHI rotation).
    lugc = (cq.Workplane("XY")
            .box(LUG_W + 2.0, LUG_CIRC + 2.0, (LUG_R_OUT + 3.0) - (LUG_R_IN - 1.0),
                 centered=(True, True, False)).translate((LUG_X, 0, LUG_R_IN - 1.0)))
    ears = ears.cut(deploy_rotate(lugc, LUG_PHI - PAWL_PHI))
    ears = try_fillet(ears, ">Z", 0.8, "ear roots", log)
    return deploy_rotate(ears, PAWL_PHI)


def make_pin():
    half = EAR_GAP / 2.0
    ext = half + EAR_T + 1.0
    pin = (cq.Workplane("YZ").workplane(offset=PAWL_X - ext)
           .moveTo(0, PIN_RAD).circle(PIN_R).extrude(2 * ext))
    return deploy_rotate(pin, PAWL_PHI)


def make_pawl(log, lift=0.0):
    """Pawl on the hub.  Built directly in the DEPLOYED (theta=45) pose as a tight
    lever pivoting on the pin (deployed at world~150, r=PIN_RAD), then rotated back
    by −DEPLOY_ANGLE so the moving-group theta rotation returns it to deploy.
    Stays on the +Y side (Y>=3.5, clear of the lug at Y<=3) and outboard of the
    hub; nose 5x10 flat bears DOWN on the abutment top (Z=-16) — contact normal
    +Z points back at the pin (self-lock, master §7).  Heel for the 33deg wedge.
    `lift` (mm, +Z deploy frame) = the wedge release that raises the nose to clear
    the abutment so the handle can fold."""
    py, pz = deploy_point(0, PIN_RAD, PAWL_PHI + DEPLOY_ANGLE)   # pin @ deploy
    nose_z = -16.0 + POCKET_CLR                                  # 0.3 above abut top
    NF = NOSE_PLUSY_FACE                                         # +Y bearing flank (=11.5)
    # Beefed profile (DFM): +Y flank at NF -> ~2.3 mm wall between the Ø6.4 bore and the loaded
    # face; corners FILLETED (stress relief) via a Sketch; body extruded with ~1° mould draft.
    pts = [(4.0, -6.0),         # heel inner-top (toward hub)
           (NF, -7.5),          # +Y flank top (body bulged to house the bore)
           (NF, nose_z),        # nose +Y corner (flank bears on the abutment)
           (4.0, nose_z),       # nose flat (radial)
           (3.5, -13.0)]        # 35deg entry-ramp lead-in
    try:
        sk = cq.Sketch().polygon(pts).reset().vertices().fillet(0.8)   # round all corners
        pawl = cq.Workplane("YZ").placeSketch(sk).extrude(PAWL_W, taper=PAWL_DRAFT)
        pawl = pawl.translate((-PAWL_W / 2.0, 0, 0))                   # recenter on X
    except Exception:                                                  # fallback: no draft/fillet
        prof = cq.Workplane("YZ").polyline(pts).close()
        pawl = prof.extrude(PAWL_W / 2, both=True)
    pawl = pawl.cut(cq.Workplane("YZ").moveTo(py, pz)
                    .circle(PIN_R + FIT_CLR).extrude(PAWL_W, both=True))
    pawl = try_fillet(pawl, ">Z", 0.5, "pawl edges", log)
    pawl = try_fillet(pawl, "%CIRCLE", 0.4, "pawl bore edges", log)    # soften bore->flank
    pawl = pawl.translate((PAWL_X, 0, lift))            # +Z lift = wedge release
    return deploy_rotate(pawl, -DEPLOY_ANGLE)           # moving-group theta -> deploy


def make_pawl_spring():
    """Pawl RETURN spring (SPEC, see PAWL_SPRING): a torsion spring on the O6 pin biasing the
    nose ENGAGED.  d1.0 / OD8.4 / ~4.5 coils / ~1.57 N*mm/deg; ~16 N*mm preload -> ~2.6 N nose
    seat rising to ~6.5 N (>10x the 0.6 g pawl's drop-shock), adding ~1 N at the squeeze.
    Representative geometry on the pin axis (X), just outboard of the clevis."""
    py, pz = deploy_point(0, PIN_RAD, PAWL_PHI + DEPLOY_ANGLE)
    coil = make_coil(PAWL_SPRING["mean_D"] / 2.0, PAWL_SPRING["wire_d"] / 2.0, 5.0,
                     PAWL_SPRING["coils"]).rotate((0, 0, 0), (0, 1, 0), -90)   # axis -> X
    coil = coil.translate((PAWL_X - 9.5, py, pz))
    legA = (cq.Workplane("XY").box(1.0, 8.0, 1.0, centered=(True, False, True))
            .translate((PAWL_X - 9.5, py, pz)))                       # tang -> hub
    legB = (cq.Workplane("XY").box(1.0, 1.0, 8.0, centered=(True, True, False))
            .translate((PAWL_X - 9.5, py, pz)))                       # tang -> pawl heel
    return deploy_rotate(coil.union(legA).union(legB), -DEPLOY_ANGLE)


def make_friction(log):
    """Belleville clutch pack on the +X hub face (master): annular discs r12-18."""
    pack = None
    step = (FRIC_X1 - FRIC_X0) / FRIC_NDISC
    for i in range(FRIC_NDISC):
        x = FRIC_X0 + i * step
        d = (cq.Workplane("YZ").workplane(offset=x)
             .circle(FRIC_R_OUT).circle(FRIC_R_IN).extrude(step * 0.6))
        pack = d if pack is None else pack.union(d)
    return pack


# ============================================================================
#  Fixed (bracket) parts — absolute geometry; the pawl/lug land on these
# ============================================================================
# ============================================================================
#  Back shell (Rev A spec) — the molded "negative" the core seats into.
#  Case 560 H x 356 W x 229 D; pivot (local O) at world Z = COM_HEIGHT = 280, so
#  world Z = local Z + 280.  Modelled as a LOCAL section of the back wall with the
#  recess / pivot pocket / drawbar channel cut so the parts sit FLUSH.
# ============================================================================
# Molded BODY envelope (user spec): 343 W x 457 H x 133 D.  Body height = 508 mm (20" carry-on
# max) minus the 50.8 mm (2") wheels.  The body is CENTERED on the pivot (the COM), so the
# pivot stays ~280 mm above the ground (body sits on the wheels) exactly as locked.
CASE_W, CASE_D, CASE_H = 343.0, 228.6, 508.0   # 9"D x 20"H body; +50.8 (2") wheels = ~559 tall
CASE_Z_TOP = CASE_H / 2.0              # body top, local (pivot at local 0 = body centre)
CASE_Z_BOT = -CASE_H / 2.0            # body bottom, local
SHELL_BACK_Y = 25.0                    # back exterior plane (parts' max +Y = 22 -> flush)
SHELL_SKIN = 3.0
RIB_T = 1.5                            # rib thickness = 50% of wall (IM rule: ribs < wall, no sink)


# Injection-molding parameters for the back shell (decided with the user):
MOLD_DRAFT = 3.0          # deg draft on all molded pocket walls (textured hardshell)
MOLD_CLR   = 0.3          # mm core-to-pocket fit clearance at the locating seat
POCKET_FR  = 3.0          # mm internal corner radius on the molded pockets
Y_CAV      = -35.0        # back-zone inner (cavity-side) face — pockets OPEN here
#                           and the core drops in along -Y, seating toward +Y (the
#                           back wall) — same direction the Y-draw tool pulls.


def molded_pocket(xw, zh, cx, cz, y_seat, y_open, draft=MOLD_DRAFT, fr=POCKET_FR):
    """A draft-correct, radiused receiving pocket.  Cross-section (X=xw, Z=zh) is the
    part footprint + clearance at the SEAT (deep end); it tapers OPEN by `draft` toward
    the `y_open` face, so the core self-locates at the seat and the tool releases toward
    the opening.  Here the openings face the OUTSIDE back (y_open=+Y), so the core nests
    from outside and the handle/drawbar rotate OUT the back.  Corners radiused."""
    depth = abs(y_seat - y_open)
    frr = min(fr, xw / 2 - 0.3, zh / 2 - 0.3)
    s = cq.Sketch().rect(xw, zh).vertices().fillet(frr)
    wp = cq.Workplane("XZ").workplane(offset=-y_seat).placeSketch(s)
    p = wp.extrude(depth, taper=-draft) if y_open < y_seat else wp.extrude(-depth, taper=-draft)
    return p.translate((cx, 0, cz))


BACK_SKIN_INNER = SHELL_BACK_Y - SHELL_SKIN   # 22 — inner face of the 3 mm back skin
Y_OUT = SHELL_BACK_Y                          # 25 — the OUTSIDE back surface; recesses open here

def _core_features():
    """Receiving features (xw_seat, zh_seat, cx, cz, y_seat, y_open), DERIVED from the
    current collapsed core so they track SPINE_LEN / case size automatically.  Recesses
    OPEN to the OUTSIDE back (y_open = Y_OUT = +25): the core nests from outside and the
    handle/drawbar rotate OUT the back exterior.  y_seat = the part's deep (-Y front)
    face.  xw/zh include the 2*MOLD_CLR fit clearance."""
    C = MOLD_CLR
    st = spine_top(0.0)                       # collapsed spine tube top (local)
    return [
        (50 + 2 * C,  st + 8.0,      0, st / 2.0,    -18.5 - C, Y_OUT),  # spine column (0..st)
        (96.0,        62 + 2 * C,    0, -9.0,        -22 - C,   Y_OUT),  # pivot/core + lower axle
        (26 + 2 * C,  164 + 2 * C,   0, -111.0,      7 - C,     Y_OUT),  # drawbar nest
        (136 + 2 * C, 56.0,          0, st + 22.0,   -19 - C,   Y_OUT),  # grip well (covers overmold)
    ]


def _core_voids():
    """Union of the drafted pocket voids (the core's space) + the axle bore."""
    v = None
    for xw, zh, cx, cz, ys, yo in _core_features():
        pv = molded_pocket(xw, zh, cx, cz, ys, yo)
        v = pv if v is None else v.union(pv)
    axle = cq.Workplane("YZ").circle(SHAFT_R + 0.5).extrude(60, both=True)
    return v.union(axle)


def _core_trays():
    """The molded back as thin (3 mm) drafted-wall troughs around each core feature,
    OPEN to the outside back and protruding inward (a 3 mm bottom wall separates the
    core from the packing) — replaces the old 60 mm solid back zone."""
    W = SHELL_SKIN
    t = None
    for xw, zh, cx, cz, ys, yo in _core_features():
        outer = molded_pocket(xw + 2 * W, zh + 2 * W, cx, cz, ys - W, yo)   # +3 mm bottom wall
        void = molded_pocket(xw, zh, cx, cz, ys, yo)
        tray = outer.cut(void)
        t = tray if t is None else t.union(tray)
    return t


def _back_ribs():
    """Full stiffening rib network on the INSIDE of the back shell (toward the packing),
    sized for the tow-impact load: vertical backbone + intermediates, horizontal cross-ribs,
    diagonals from the pivot to the bottom corners (tow load -> wheels), and a perimeter
    frame.  Corrected IM rib rule: 1.5 mm (50% wall, no sink), capped depth, cut clear of
    the core recesses."""
    import math
    W = RIB_T
    yf = BACK_SKIN_INNER - 12.0; dy = BACK_SKIN_INNER - yf
    H, Wd = CASE_H, CASE_W
    ribs = None
    def U(r):
        nonlocal ribs
        ribs = r if ribs is None else ribs.union(r)
    # vertical ribs (backbone pair flanking the spine + outer pair)
    for cx in (-95, -48, 48, 95):
        U(cq.Workplane("XY").box(W, dy, H - 30, centered=(True, False, True)).translate((cx, yf, 0)))
    # horizontal cross-ribs
    for cz in (200, 100, 0, -100, -200):
        U(cq.Workplane("XY").box(Wd - 34, dy, W, centered=(True, False, True)).translate((0, yf, cz)))
    # perimeter frame (hoop stiffness + zipper land)
    for cx in (Wd / 2 - 14, -(Wd / 2 - 14)):
        U(cq.Workplane("XY").box(W, dy, H - 20, centered=(True, False, True)).translate((cx, yf, 0)))
    for cz in (H / 2 - 12, -(H / 2 - 12)):
        U(cq.Workplane("XY").box(Wd - 20, dy, W, centered=(True, False, True)).translate((0, yf, cz)))
    # diagonals: pivot (0,0) -> the two bottom corners (spreads the tow reaction to the wheels)
    for sx in (-1, 1):
        x1, z1 = sx * 150.0, -(H / 2 - 30)
        L = math.hypot(x1, z1); ang = math.degrees(math.atan2(z1, x1))
        d = (cq.Workplane("XY").box(L, dy, W, centered=(True, False, True))
             .rotate((0, yf, 0), (0, yf + 1, 0), -ang).translate((x1 / 2, yf, z1 / 2)))
        try:
            U(d)
        except Exception:
            pass
    # MOUNT-PAD TIE FRAME: a rib box around the steel mount pad so the joint load (bolts ->
    # pad) feeds straight into the rib network + the diagonals, not just the local wall.
    px, pz0, pz1 = 32.0, -32.0, 20.0
    for cx in (-px, px):
        U(cq.Workplane("XY").box(W, dy, pz1 - pz0, centered=(True, False, True)).translate((cx, yf, (pz0 + pz1) / 2)))
    for cz in (pz0, pz1):
        U(cq.Workplane("XY").box(2 * px, dy, W, centered=(True, False, True)).translate((0, yf, cz)))
    return ribs.cut(_core_voids())                     # never block the core


def make_shell():
    """Representative back-shell section (the molded negative) — the Check #8 fit proxy."""
    YB = SHELL_BACK_Y
    blank = (cq.Workplane("XY").box(TH_GRASP + 40, YB + 30, CASE_Z_TOP - (-275),
             centered=(True, False, False)).translate((0, -30, -275)))
    return blank.cut(_core_voids())


CASE_EDGE_R  = 14.0       # external molded edge/corner radius (rounded, per IM)
CASE_DRAFT   = 1.5        # deg draft on the outer body walls (Y-draw; never perpendicular)
ZIP_W        = 25.4       # perimeter zipper band (~1": coil + tape both sides)
PARTING_Y    = SHELL_BACK_Y - CASE_D / 2.0   # zipper CENTRE at mid-depth (4.5" from each face)
Y_BACK_PART  = PARTING_Y + ZIP_W / 2.0       # back shell ends here  -> 4.0" deep shell
Y_FRONT_PART = PARTING_Y - ZIP_W / 2.0       # front shell ends here -> 4.0" deep shell
#  Total 9" = back shell 4.0" + zipper 1.0" + front shell 4.0".


def _full_case_solid():
    """The complete molded suitcase body as ONE solid (before the back/front split):
    a uniform ~3 mm shell — rounded external edges (R14), ~1.5 deg outer-wall draft
    (Y-draw), top trimmed flush at 560 — with the core received in thin-wall drafted
    TRAYS off the back skin, stiffened by ribs (no solid mass)."""
    sk = SHELL_SKIN
    zc = CASE_Z_BOT + CASE_H / 2.0
    outer = (cq.Workplane("XZ").workplane(offset=-SHELL_BACK_Y).center(0, zc)
             .rect(CASE_W, CASE_H).extrude(CASE_D, taper=CASE_DRAFT))
    outer = outer.edges().fillet(CASE_EDGE_R)
    cav = (cq.Workplane("XZ").workplane(offset=-BACK_SKIN_INNER).center(0, zc)
           .rect(CASE_W - 2 * sk, CASE_H - 2 * sk).extrude(CASE_D - 2 * sk, taper=CASE_DRAFT))
    cav = cav.edges().fillet(CASE_EDGE_R - sk)
    case = outer.cut(cav).union(_core_trays()).union(_back_ribs()).cut(_core_voids())
    top_slot = (cq.Workplane("XY").box(140, 60, 40, centered=(True, True, False))
                .translate((0, -8, CASE_Z_TOP - 6)))
    case = case.cut(top_slot)
    cap = (cq.Workplane("XY").box(CASE_W + 60, CASE_D + 60, CASE_H, centered=(True, True, True))
           .translate((0, SHELL_BACK_Y - CASE_D / 2.0, zc)))
    return case.intersect(cap)


def _half_box(ymin, ymax):
    zc = CASE_Z_BOT + CASE_H / 2.0
    return (cq.Workplane("XY").box(CASE_W + 80, ymax - ymin, CASE_H + 80,
            centered=(True, False, True)).translate((0, ymin, zc)))


def make_case_back():
    """The BACK shell (4.0" deep, Y >= back parting): the core-side half — holds the core in
    its molded recesses (open to the outside back), ending a half-zipper short of mid-depth."""
    back = _full_case_solid().intersect(_half_box(Y_BACK_PART, SHELL_BACK_Y + 5))
    return back.cut(_case_mount_holes())            # clearance for the bracket->case bolts


RX_Z = -25.4              # tow receiver centre, local Z (= 11" below the case top, ~COM height)


# ---- Steel keyhole tow-ball receiver (metal; bolted to the front shell) ----------------
RX_PLATE_W, RX_PLATE_H, RX_PLATE_T = 72.0, 100.0, 3.0   # steel flange plate
RX_ENTRY_R = 9.0           # round entry hole (> Ø16 ball)
RX_SLOT_W  = 9.0           # capture slot width (> Ø7 neck, < Ø16 ball)
RX_SLOT_LO, RX_SLOT_HI = -16.0, 18.0   # slot span in Z (entry at top, capture below)
RX_LOCK    = 12.0          # self-locking slot tilt (deg)
RX_BOLT = [(28, 40), (-28, 40), (28, -40), (-28, -40)]   # 4 bolt holes (X,Z)


def _rx_xz(x, z):
    return cq.Workplane("XZ").moveTo(x, z)


RX_DET_Z = RX_SLOT_LO + 14.0   # detent height (above the seated ball neck)
RX_SEAT_Z = RX_SLOT_LO + 6.0   # seated ball-centre height in the slot


def make_receiver_bracket():
    """The STEEL keyhole receiver: a flange plate with a funnel lead-in, a round entry hole
    (admits the Ø16 ball) and a VERTICAL drop slot (captures the neck; ball trapped behind
    the plate — the tow-load lock, capture ⊥ pull).  A side DETENT HOUSING behind the plate
    holds a sprung pin (the 'slight snap' / anti-rise).  The seat is 12° back-leaned (in the
    pocket) so the tow pull seats the ball down.  Bolted to the front shell; placed at
    (0, yF, RX_Z)."""
    yF = SHELL_BACK_Y - CASE_D
    PT = RX_PLATE_T
    plate = _rx_xz(0, 0).rect(RX_PLATE_W, RX_PLATE_H).extrude(-PT)         # flange, Y 0..PT (+Y in)
    entry = _rx_xz(0, RX_SLOT_HI).circle(RX_ENTRY_R).extrude(-(PT + 2))    # round entry hole
    slot = (_rx_xz(0, (RX_SLOT_LO + RX_SLOT_HI) / 2.0)
            .rect(RX_SLOT_W, RX_SLOT_HI - RX_SLOT_LO).extrude(-(PT + 2)))  # VERTICAL drop slot
    bracket = plate.cut(entry).cut(slot)
    # funnel lead-in: countersink cone on the exterior (-Y) face at the entry
    funnel = (_rx_xz(0, RX_SLOT_HI).circle(14).workplane(offset=-6).circle(RX_ENTRY_R).loft())
    bracket = bracket.cut(funnel)
    # sprung-detent housing: a boss behind the plate (+X side) bored along X for the pin+spring
    house = (cq.Workplane("YZ").workplane(offset=RX_SLOT_W / 2 - 1).rect(11, 9)
             .extrude(16).translate((0, PT + 4.5, RX_DET_Z)))             # block X≈3.5..19.5
    bore = (cq.Workplane("YZ").workplane(offset=2.0).circle(1.9)
            .extrude(18).translate((0, PT + 4.5, RX_DET_Z)))              # pin/spring bore
    bracket = bracket.union(house).cut(bore)
    for bx, bz in RX_BOLT:                                                 # bolt holes
        bracket = bracket.cut(_rx_xz(bx, bz).circle(2.4).extrude(-(PT + 2)))
    return bracket.translate((0, yF, RX_Z))


def make_receiver_backplate():
    """Thin steel backing plate INSIDE the front shell so the bolt heads can't pull through
    the plastic under the tow load (spreads the −Y peel into the bosses/ribs)."""
    yF = SHELL_BACK_Y - CASE_D
    bp = _rx_xz(0, 0).rect(RX_PLATE_W + 8, RX_PLATE_H + 8).extrude(-2.5).translate((0, 22, 0))
    bp = bp.cut(_rx_xz(0, 0).rect(34, RX_PLATE_H - 20).extrude(-6).translate((0, 22, 0)))  # clear the ball pocket
    for bx, bz in RX_BOLT:
        bp = bp.cut(_rx_xz(bx, bz).circle(2.4).extrude(-6).translate((0, 22, 0)))
    return bp.translate((0, yF, RX_Z))


def make_receiver_bolts():
    """4 mounting bolts (front bracket -> backing plate), in tension under tow load."""
    yF = SHELL_BACK_Y - CASE_D
    out = None
    for bx, bz in RX_BOLT:
        b = _rx_xz(bx, bz).circle(2.0).extrude(-28).translate((0, 0, 0))    # shank, into +Y
        head = _rx_xz(bx, bz).circle(4.0).extrude(2)                        # head on the face
        b = b.union(head).translate((0, yF, RX_Z))
        out = b if out is None else out.union(b)
    return out


def make_receiver_detent():
    """Sprung detent (the 'slight snap' / anti-rise): a pin that protrudes from the side into
    the slot just above the seated ball, backed by a compression spring in the housing bore.
    The ball pushes it aside dropping in (snap); it springs back to block the ball rising;
    a deliberate lift pops it.  Two rigid steel parts can't snap — this sprung pin is what does."""
    yF = SHELL_BACK_Y - CASE_D
    PT = RX_PLATE_T
    pin = (cq.Workplane("YZ").workplane(offset=1.0).circle(1.8).extrude(7)   # tip into slot
           .translate((0, PT + 4.5, RX_DET_Z)))
    nose = (cq.Workplane("YZ").workplane(offset=1.0).sphere(1.8)
            .translate((0, PT + 4.5, RX_DET_Z)))                             # rounded nose
    spring = (make_coil(1.5, 0.35, 9, 6).rotate((0, 0, 0), (0, 1, 0), -90)
              .translate((9.5, PT + 4.5, RX_DET_Z)))                         # coil behind, along X
    det = pin.union(nose).union(spring)
    return det.translate((0, yF, RX_Z))


def _receiver_cuts():
    """Cut into the FRONT shell for the steel bracket: a flush recess for the plate, the ball
    pocket (with a 12° BACK-LEANED seat so the tow pull seats the ball down) + slot travel
    behind it, the funnel mouth, and the 4 bolt clearance holes."""
    yF = SHELL_BACK_Y - CASE_D
    recess = _rx_xz(0, 0).rect(RX_PLATE_W + 0.6, RX_PLATE_H + 0.6).extrude(-(RX_PLATE_T + 0.3)).translate((0, yF, RX_Z))
    mouth = _rx_xz(0, RX_SLOT_HI).circle(RX_ENTRY_R + 0.5).extrude(-(RX_PLATE_T + 30)).translate((0, yF, RX_Z))
    # upper pocket (vertical drop) + lower seat pocket leaned 12° toward the exterior (self-lock)
    up = _rx_xz(0, (RX_SEAT_Z + RX_SLOT_HI) / 2.0 + 2).rect(26, RX_SLOT_HI - RX_SEAT_Z + 6).extrude(-30).translate((0, yF + RX_PLATE_T, RX_Z))
    seat = (_rx_xz(0, 0).rect(26, 22).extrude(-30)
            .rotate((0, 0, 0), (1, 0, 0), RX_LOCK)                          # lean 12° in Y-Z (about X)
            .translate((0, yF + RX_PLATE_T, RX_Z + RX_SEAT_Z)))
    house = (cq.Workplane("YZ").workplane(offset=RX_SLOT_W / 2 - 1.5).rect(12, 10)
             .extrude(18).translate((0, RX_PLATE_T + 4.5, RX_Z + RX_DET_Z)).translate((0, yF, 0)))
    cut = recess.union(mouth).union(up).union(seat).union(house)
    for bx, bz in RX_BOLT:
        cut = cut.union(_rx_xz(bx, bz).circle(2.4).extrude(-30).translate((0, yF, RX_Z)))
    return cut


def _receiver_bosses():
    """4 cored, gusseted molded bosses behind the bracket bolt holes (tap the bolts)."""
    yF = SHELL_BACK_Y - CASE_D
    out = None
    for bx, bz in RX_BOLT:
        boss = (_rx_xz(bx, bz).circle(6).circle(2.4).extrude(-26)           # cored boss (tube)
                .translate((0, yF + RX_PLATE_T, RX_Z)))
        out = boss if out is None else out.union(boss)
    return out


def _front_ribs():
    """Front-shell rib network feeding the tow-hitch load into the structure: a perimeter
    frame + ribs RADIATING from the receiver out to the corners and DOWN to the wheel base.
    Corrected IM rib rules: 1.5 mm (50% wall), capped height, cut clear of the receiver."""
    import math
    yF = SHELL_BACK_Y - CASE_D
    y0 = yF + SHELL_SKIN
    dy = 12.0                                   # rib depth into the front shell (capped)
    H, Wd = CASE_H, CASE_W
    ribs = None
    def U(r):
        nonlocal ribs; ribs = r if ribs is None else ribs.union(r)
    for cx in (Wd / 2 - 14, -(Wd / 2 - 14)):
        U(cq.Workplane("XY").box(RIB_T, dy, H - 24, centered=(True, False, True)).translate((cx, y0, 0)))
    for cz in (H / 2 - 12, -(H / 2 - 12)):
        U(cq.Workplane("XY").box(Wd - 24, dy, RIB_T, centered=(True, False, True)).translate((0, y0, cz)))
    for tx, tz in [(150, H / 2 - 30), (-150, H / 2 - 30), (150, -(H / 2 - 30)),
                   (-150, -(H / 2 - 30)), (0, -(H / 2 - 30))]:
        L = math.hypot(tx, tz - RX_Z); ang = math.degrees(math.atan2(tz - RX_Z, tx))
        d = (cq.Workplane("XY").box(L, dy, RIB_T, centered=(True, False, True))
             .rotate((0, y0, 0), (0, y0 + 1, 0), -ang).translate((tx / 2, y0, (RX_Z + tz) / 2)))
        try:
            U(d)
        except Exception:
            pass
    return ribs.cut(_receiver_cuts())


def make_case_front():
    """The FRONT shell (4.0" deep): packing half + the molded mounts for the STEEL keyhole
    tow-ball receiver (recess + ball pocket + cored gusseted bosses) and the front-shell
    rib network that feeds the tow load into the structure."""
    fr = _full_case_solid().intersect(_half_box(SHELL_BACK_Y - CASE_D - 5, Y_FRONT_PART))
    fr = fr.union(_receiver_bosses()).union(_front_ribs())
    return fr.cut(_receiver_cuts())


def make_case():
    """The whole closed case (both shells as one solid) — for whole-case views."""
    return _full_case_solid()


def make_zipper():
    """Representative perimeter zipper band at the parting plane joining the two shells."""
    zc = CASE_Z_BOT + CASE_H / 2.0
    o = cq.Sketch().rect(CASE_W - 4, CASE_H - 4).vertices().fillet(CASE_EDGE_R - 2)
    i = cq.Sketch().rect(CASE_W - 18, CASE_H - 18).vertices().fillet(CASE_EDGE_R - 2)
    band = (cq.Workplane("XZ").workplane(offset=-PARTING_Y).center(0, zc)
            .placeSketch(o).extrude(ZIP_W / 2.0, both=True))
    hole = (cq.Workplane("XZ").workplane(offset=-PARTING_Y).center(0, zc)
            .placeSketch(i).extrude(ZIP_W, both=True))
    return band.cut(hole)


WHEEL_DIA = 50.8                           # 2 inch spinner wheels


def _wheel_disc(cx, cy, zb, R, spin=0.0):
    """A SPOKED wheel disc (rim + hub + cross spokes) so rotation is visible.  Axle along X;
    `spin` (deg) rolls it about the axle."""
    off = cx - 11; W = 22
    def yz():
        return cq.Workplane("YZ").workplane(offset=off).moveTo(cy, zb - R)
    rim = yz().circle(R).circle(R - 5).extrude(W)              # tire
    hub = yz().circle(7).extrude(W)                            # hub
    sp1 = yz().rect(2 * (R - 3), 4).extrude(W)                 # spoke (horizontal)
    sp2 = yz().rect(4, 2 * (R - 3)).extrude(W)                 # spoke (vertical)
    disc = rim.union(hub).union(sp1).union(sp2)
    if spin:
        disc = disc.rotate((cx - 1, cy, zb - R), (cx + 1, cy, zb - R), spin)
    return disc


def _fixed_wheel(cx, cy, zb, R, spin=0.0):
    """A FIXED (non-swivel) wheel — tracks straight.  Bracket + inline spoked wheel."""
    fork = (cq.Workplane("XY").box(40, 16, 10, centered=(True, True, False)).translate((cx, cy, zb)))
    return fork.union(_wheel_disc(cx, cy, zb, R, spin))


def _swivel_caster(cx, cy, zb, R, spin=0.0, trail=12.0):
    """A SWIVEL caster — king-pin (vertical) housing + a TRAILING spoked wheel that steers."""
    housing = (cq.Workplane("XY").circle(13).extrude(-14).translate((cx, cy, zb + 4)))
    yoke = (cq.Workplane("XY").box(26, 10, 8, centered=(True, True, False))
            .translate((cx, cy - trail / 2.0, zb - 10)))
    return housing.union(yoke).union(_wheel_disc(cx, cy - trail, zb, R, spin))


def make_wheels(spin=0.0):
    """Four 2 in (50.8 mm) SPOKED wheels at the bottom corners.  The case is pulled from the
    BACK, so (wagon rule) the BACK wheels SWIVEL and the FRONT wheels are FIXED.  All drop
    50.8 mm below the body bottom.  `spin` (deg) rolls every wheel about its axle."""
    R = WHEEL_DIA / 2.0
    zb = CASE_Z_BOT
    yf = SHELL_BACK_Y - CASE_D
    cy_front = yf + 28.0
    cy_back = SHELL_BACK_Y - 28.0
    out = None
    for cx in (-140.0, 140.0):
        for w in (_fixed_wheel(cx, cy_front, zb, R, spin), _swivel_caster(cx, cy_back, zb, R, spin)):
            out = w if out is None else out.union(w)
    return out


def make_brace():
    """Internal steel load backbone behind the recess (pivot -> corners/base)."""
    return (cq.Workplane("XY").box(52, 3, 275, centered=(True, False, False))
            .translate((0, -30, 0)))


def make_abutment():
    """Fixed fold-back stop the pawl nose bears against.  BUTTRESSED WEDGE (was a slender
    5 mm post that bent over @1.5 kN, SF 0.39): the −Y contact face is vertical at the top
    where the pawl engages, the back face slopes out to a DEEP base where the cantilever
    moment peaks, and it spans the FULL pawl width (X) so the bearing area is the full nose.
    Bearing SF ~4.9, post-bending SF ~2.2 (6061)."""
    fy = NOSE_PLUSY_FACE + POCKET_CLR                 # 11.8 contact face
    base_back = fy + 6.5                              # 18.3 base — clears the drawbar (Y>=18.8)
    top_back = fy + 2.5                               # 2.5 mm at the top (low moment there)
    prof = (cq.Workplane("YZ")
            .moveTo(fy, ABUT_TOP_Z)                   # top of contact face
            .lineTo(fy, FLOOR_Z1)                     # contact/front face (−Y, vertical)
            .lineTo(base_back, FLOOR_Z1)              # deep base
            .lineTo(top_back, ABUT_TOP_Z)             # back face slopes in toward the top
            .close())
    width = 11.0                                      # X — covers the full 10 mm pawl
    return prof.extrude(width / 2, both=True).translate((PAWL_X, 0, 0))   # STEEL insert


def make_bracket(log):
    wl = (cq.Workplane("XY")
          .box(WALL_T, 2 * WALL_Y, WALL_Z1 - WALL_Z0, centered=(False, True, False))
          .translate((-WALL_OUT_X, 0, WALL_Z0)))
    wr = wl.translate((2 * WALL_IN_X + WALL_T, 0, 0))
    floor = (cq.Workplane("XY")
             .box(2 * WALL_OUT_X, 2 * WALL_Y, FLOOR_Z1 - FLOOR_Z0,
                  centered=(True, True, False)).translate((0, 0, FLOOR_Z0)))
    # mount tabs (carry the M10 ends), one just outboard of each wall
    tabL = (cq.Workplane("XY").box(TAB_X - WALL_OUT_X, 16, 12,
            centered=(False, True, True)).translate((-TAB_X, 0, 0)))
    tabR = (cq.Workplane("XY").box(TAB_X - WALL_OUT_X, 16, 12,
            centered=(False, True, True)).translate((WALL_OUT_X, 0, 0)))
    bracket = wl.union(wr).union(floor).union(tabL).union(tabR)

    # shaft bore through the walls
    bore = cq.Workplane("YZ").circle(SHAFT_R + FIT_CLR).extrude(WALL_OUT_X * 3, both=True)
    bracket = bracket.cut(bore)

    # fixed WALL (−Y, open-load seat) at the LUG axial band; fixed ABUTMENT
    # (+Y, fold-back) at the PAWL axial band.  Both absolute, deployed geometry.
    wall = (cq.Workplane("XY")
            .box(LUG_W + 2, WALL_Y1 - WALL_Y0, POST_Z1 - POST_Z0,
                 centered=(True, False, False)).translate((LUG_X, WALL_Y0, POST_Z0)))
    # ABUTMENT: a ledge-post whose −Y face the pawl's +Y nose face bears against,
    # so FOLD-BACK (nose moves +Y) drives the nose INTO it = positive block.  Its
    # top (ABUT_TOP_Z) sits just below nose+WEDGE_LIFT, so the wedge release raises
    # the nose clear and the handle folds (verified by Check #6).
    abut = make_abutment()
    bracket = bracket.union(wall)            # lug seat — shaped by the lug sweep next

    # relieve the lug + pawl swept envelopes so they enter the pocket clash-free
    bracket = bracket.cut(make_lug_sweep())
    bracket = bracket.cut(make_pawl_sweep())
    # +Y deploy slot: relieve the floor along the drawbar's swung path (Check #3)
    bracket = bracket.cut(make_drawbar_sweep(), clean=False)
    # ABUTMENT (buttressed) added AFTER the bracket sweeps so the PAWL-swing relief does NOT
    # carve the contact face (build-order — Check #6).  But carve the buttress back along the
    # LUG swing and the DRAWBAR path (those zones are clear of the pawl-contact face).
    abut = abut.cut(make_lug_sweep()).cut(make_drawbar_sweep(dilate=1.5), clean=False)
    bracket = bracket.union(abut, clean=False)

    bracket = try_fillet(bracket, "|X and >Z", FILLET_R, "bracket top edges", log)
    return bracket


# --- swept envelopes (for pocket relief) ------------------------------------
def make_lug_sweep(extra_deg=0.6, steps=22):
    g = POCKET_CLR
    blk = (cq.Workplane("XY")
           .box(LUG_W + 2 * g, LUG_CIRC + 2 * g, (LUG_R_OUT + g) - LUG_R_IN,
                centered=(True, True, False)).translate((LUG_X, 0, LUG_R_IN)))
    blk = deploy_rotate(blk, LUG_PHI)
    th_max = DEPLOY_ANGLE + extra_deg
    env = None
    for i in range(steps + 1):
        piece = deploy_rotate(blk, th_max * i / steps)
        env = piece if env is None else env.union(piece)
    return env


def make_pawl_sweep(extra_deg=0.5, steps=18, dilate=0.4):
    log2 = []
    one = make_ears(log2).union(make_pin()).union(make_pawl(log2))
    th_max = DEPLOY_ANGLE + extra_deg
    env = None
    for i in range(steps + 1):
        piece = deploy_rotate(one, th_max * i / steps)
        env = piece if env is None else env.union(piece)
    dil = env
    for dy, dz in [(dilate, 0), (-dilate, 0), (0, dilate), (0, -dilate)]:
        dil = dil.union(env.translate((0, dy, dz)))
    return dil


# ============================================================================
#  Independent — drawbar (STOWED at −Z on this case) + fasteners
# ============================================================================
# Drawbar pivots on a SEPARATE lower axle below the COM shaft (design decision,
# user-approved): keeps the tow bar and its full swing clear of the trap
# mechanism, and keeps tow load out of the COM joint.  COLLAR_X (master, collars
# on the main shaft) is unused under this scheme.
# Drawbar axle: as HIGH as the geometry allows = at COM height (Z0), and forward
# at the deploy face (user direction: closer to COM is better for towing).  It
# deploys UP to 45deg — parallel with the spine's 45deg, so they can't collide
# even if both are out — to reach a taller case's higher socket.
# Drawbar axle moved DOWN (user's "down the Y" = my −Z), to the marked spot just
# below the trap cluster — the clear zone.  Forward toward the front face.
# (Axis-name note: user "Y/up-down" == code "Z/height".)
DRAW_PIVOT_Z = -35.0                  # ~35 mm below COM, just under the trap
DRAW_PIVOT_Y = 15.0                   # forward toward the front face
DRAW_AXLE_R  = 4.0
BALL_R       = 8.0
DRAW_DEPLOY  = 135.0                  # allow up to 45deg above horizontal (taller case)


def make_drawbar(theta_draw=0.0):
    """Independent tow bar on the lower pivot axle.  Built with the pivot at the
    origin and the arm straight down (−Z = stowed), swung by theta_draw toward +Y,
    then dropped onto the pivot at (0, DRAW_PIVOT_Y, DRAW_PIVOT_Z).
    theta_draw = 0 stowed; theta_draw = DRAW_DEPLOY -> ball at COM (local Z=0)."""
    bushL = (cq.Workplane("YZ").workplane(offset=7)
             .circle(6).circle(DRAW_AXLE_R + FIT_CLR).extrude(6))
    bushR = (cq.Workplane("YZ").workplane(offset=-13)
             .circle(6).circle(DRAW_AXLE_R + FIT_CLR).extrude(6))
    bridge = (cq.Workplane("XY").box(26, 8, 8, centered=True).translate((0, 0, -5)))
    arm = (cq.Workplane("XY").box(8, 8, DRAWBAR_LEN - 5, centered=(True, True, False))
           .translate((0, 0, -DRAWBAR_LEN)))
    ball = cq.Workplane("XY").sphere(BALL_R).translate((0, 0, -DRAWBAR_LEN))
    yoke = bushL.union(bushR).union(bridge).union(arm).union(ball)
    yoke = deploy_rotate(yoke, -theta_draw)        # −Z -> +Y for +theta_draw
    return yoke.translate((0, DRAW_PIVOT_Y, DRAW_PIVOT_Z))


def make_lower_axle():
    """Drawbar pivot axle — a pin across the front of the core at COM height,
    its ends supported in the bracket side walls (spans to X = +/-26)."""
    return (cq.Workplane("YZ").moveTo(DRAW_PIVOT_Y, DRAW_PIVOT_Z)
            .circle(DRAW_AXLE_R).extrude(26, both=True))


def make_drawbar_sweep(steps=18, dilate=0.5):
    """Swept envelope of the NEAR drawbar (a box arm-stub + bushing block, no ball
    or far arm) over 0 -> DRAW_DEPLOY, dilated for clearance.  Subtracted from the
    bracket to open the +Y deploy slot the arm swings through (Check #3).  Boxes
    only + clean=False to keep the boolean robust."""
    half = (10 + 2 * dilate) / 2.0
    # arm stub: pivot-frame box pointing −Z, long enough to span the bracket floor
    stub = (cq.Workplane("XY").box(10 + 2 * dilate, 10 + 2 * dilate, 60,
            centered=(True, True, False)).translate((0, 0, -60)))
    stub = stub.union(cq.Workplane("XY").box(30, 14, 14, centered=True))  # bushing block
    env = None
    for i in range(steps + 1):
        td = DRAW_DEPLOY * i / steps
        piece = deploy_rotate(stub, -td).translate((0, DRAW_PIVOT_Y, DRAW_PIVOT_Z))
        env = piece if env is None else env.union(piece, clean=False)
    return env


def make_fasteners(log):
    """Real M10 hex thread + nut at the +X shaft end (master part table)."""
    thread = (cq.Workplane("YZ").workplane(offset=SHAFT_X)
              .circle(M10 / 2).extrude(12))
    nut = hex_prism_x(M10 * 1.6, SHAFT_X + 3, 8)
    return thread.union(nut)


# ============================================================================
#  Assembly
# ============================================================================
def moving_parts(theta, log, spine_extend=0.0):
    parts = {
        "shaft":    make_shaft(),
        "hub":      make_hub(),
        "lug":      make_stop_lug(log),
        "ears":     make_ears(log),
        "pin":      make_pin(),
        "pawl":     make_pawl(log),
        "pawlspring": make_pawl_spring(),
        "friction": make_friction(log),
        "spine":    make_spine(log, spine_extend),
    }
    parts.update(make_actuation(spine_extend))     # carrier + rods + concentrator
    parts["lockpins"] = make_lock_pins(spine_extend)
    parts["wedge"] = make_wedge(0.0)               # release wedge (engaged/rest)
    parts["stowhook"] = make_stow_hook()           # 0deg stow latch (on the hub)
    gtop = spine_top(spine_extend)
    parts["button"] = make_grip_button(gtop, 0.0)  # grip controls at rest
    parts["trigger"] = make_grip_trigger(gtop, 0.0)
    parts["springs"] = make_grip_springs(gtop)     # button + trigger return springs
    parts["overmold"] = make_overmold(gtop)        # soft TPE grip skin
    parts["jointpin"] = make_joint_pin(gtop)       # core-to-S5 dowel + ferrules
    return {k: deploy_rotate(v, theta) for k, v in parts.items()}


def make_backplate():
    """Steel backing strip across the back of the U-bracket, tying the two walls together
    so the open U can't splay under the snatch/tow load.  Also the bracket->case mount face:
    the mount bolts thread into it (tapped M6)."""
    bp = (cq.Workplane("XY").box(2 * TAB_X, 3, (WALL_Z1 - WALL_Z0) + 4, centered=(True, False, False))
          .translate((0, WALL_Y - 3, WALL_Z0 - 2)))
    return bp


# ---- Bracket -> CASE attachment (the joint was NOT fastened to the case) -----------------
CASE_MOUNT = [(26, 18), (-26, 18), (26, -18), (-26, -18)]   # (X,Z) mount-bolt pattern @ pivot


def _ybolt(bx, bz, r, y0, length):
    """A cylinder along +Y (bolt/hole helper) from y0, of given length."""
    return cq.Workplane("XZ").moveTo(bx, bz).circle(r).extrude(-length).translate((0, y0, 0))


def make_case_backing_plate():
    """Steel mount pad INLAID FLUSH in the case back (replaces the 3 mm plastic wall locally
    -> a steel-to-steel mount, no plastic creep, no protrusion).  The bracket backplate bolts
    to it; it ties into the case back ribs and spreads the joint load into the shell."""
    yi = BACK_SKIN_INNER                                # 22 (inner wall face)
    plate = (cq.Workplane("XY").box(64, SHELL_BACK_Y - yi, 52, centered=(True, False, True))
             .translate((0, yi, -6)))                  # Y22..25 (flush exterior)
    for bx, bz in CASE_MOUNT:
        plate = plate.cut(_ybolt(bx, bz, 3.1, yi - 1, 6))   # M6 clearance
    return plate


def make_case_mount_bolts():
    """4 M6 bolts, FLAT/countersunk head flush at the back exterior, shank threaded into the
    bracket backplate -> clamps the joint to the case (nothing proud of the shell)."""
    yo = SHELL_BACK_Y
    out = None
    for bx, bz in CASE_MOUNT:
        b = _ybolt(bx, bz, 3.0, WALL_Y - 4, yo - (WALL_Y - 4))         # shank Y18..25
        b = b.union(_ybolt(bx, bz, 4.7, yo - 2.0, 2.0))               # countersunk head, flush
        out = b if out is None else out.union(b)
    return out


def _case_mount_holes():
    """Pocket in the case back wall for the flush steel mount pad (the pad fills it)."""
    return (cq.Workplane("XY").box(64.4, (SHELL_BACK_Y - BACK_SKIN_INNER) + 0.2, 52.4,
                                   centered=(True, False, True))
            .translate((0, BACK_SKIN_INNER - 0.1, -6)))


def fixed_parts(log, theta_draw=0.0):
    return {
        "bracket":   make_bracket(log),
        "backplate": make_backplate(),           # stiffens the U-bracket against splay
        "casebacking": make_case_backing_plate(),  # spreads the mount load into the case back
        "mountbolts": make_case_mount_bolts(),   # clamp the joint to the case
        "loweraxle": make_lower_axle(),
        "drawbar":   make_drawbar(theta_draw),   # independent DOF (0 = stowed)
        "stowpin":   make_stow_pin(),            # fixed catch for the stow hook
        "fastener":  make_fasteners(log),
    }


def build(theta=DEPLOY_ANGLE, theta_draw=0.0, spine_extend=0.0):
    log = []
    mv = moving_parts(theta, log, spine_extend)
    fx = fixed_parts(log, theta_draw)
    parts = {**mv, **fx}
    assy = cq.Assembly(name="gravitcase_core")
    for name, wp in parts.items():
        assy.add(wp, name=name,
                 color=COL.get(name, cq.Color(0.7, 0.7, 0.7, 1.0)))
    return assy, parts, mv, fx, log


def export(assy, parts):
    step_path = os.path.join(MODELS, "gravitcase_core.step")
    stl_path = os.path.join(MODELS, "gravitcase_core.stl")
    assy.export(step_path)
    # STL = a COMPOUND of every part's solids (no fragile boolean fusion)
    shapes = []
    for wp in parts.values():
        shapes.extend(wp.vals())
    comp = cq.Compound.makeCompound(shapes)
    cq.exporters.export(comp, stl_path)
    return step_path, stl_path


def export_suitcase():
    """Complete product: mechanism (stowed) + molded case + 2 in wheels."""
    parts = dict(build(0.0, 0.0, 0.0)[1])
    parts["case_back"] = make_case_back()      # core-side shell (molded recesses)
    parts["case_front"] = make_case_front()    # packing shell (no core) + receiver mounts
    parts["zipper"] = make_zipper()            # perimeter zipper seam
    parts["rx_bracket"] = make_receiver_bracket()    # steel keyhole tow receiver
    parts["rx_backplate"] = make_receiver_backplate()
    parts["rx_bolts"] = make_receiver_bolts()
    parts["rx_detent"] = make_receiver_detent()      # sprung anti-rise detent (the snap)
    parts["wheel"] = make_wheels()
    assy = cq.Assembly(name="gravitcase_suitcase")
    for name, wp in parts.items():
        assy.add(wp, name=name, color=COL.get(name, cq.Color(0.7, 0.7, 0.7, 1.0)))
    sp = os.path.join(MODELS, "gravitcase_suitcase.step")
    assy.export(sp)
    shapes = []
    for wp in parts.values():
        shapes.extend(wp.vals())
    st = os.path.join(MODELS, "gravitcase_suitcase.stl")
    cq.exporters.export(cq.Compound.makeCompound(shapes), st)
    return sp, st


if __name__ == "__main__":
    assy, parts, mv, fx, log = build(DEPLOY_ANGLE)
    for kind, msg in log:
        print(f"  [{kind}] {msg}")
    sp, st = export(assy, parts)
    print("exported:", os.path.basename(sp), os.path.getsize(sp), "|",
          os.path.basename(st), os.path.getsize(st))
    print("part volumes (mm^3):")
    for k, wp in parts.items():
        try:
            print(f"  {k:10s} {wp.val().Volume():12.1f}")
        except Exception as e:
            print(f"  {k:10s} <{e}>")
    ssp, sst = export_suitcase()
    print("suitcase:", os.path.basename(ssp), os.path.getsize(ssp), "|",
          os.path.basename(sst), os.path.getsize(sst))
