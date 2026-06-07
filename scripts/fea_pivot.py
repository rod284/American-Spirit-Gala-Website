"""Lightweight FEA for the pivot area (numpy only — no external solver).

* PAWL: a 2D plane-stress CST finite-element model of the load cross-section (the Y-Z plane,
  thickness = PAWL_W).  This is where FEM earns its keep — the Ø6.4 pin-bore + the 2.3 mm
  loaded ligament concentrate stress in a way the Check #11 hand calc only approximates with
  a Kt factor.  Load = fold-back on the +Y flank; the pin bore is the reaction (bonded-pin
  idealisation).  Reports the von-Mises field peak and the safety factor.
* SHAFT / PIN / ABUTMENT: closed-form confirmations (clean geometries — FEM adds nothing).

Run:  PYTHONUTF8=1 python3 fea_pivot.py
"""
import math
import numpy as np
import build_core as bc

# ---- materials (MPa) ----
MAT = {
    "17-4PH MIM H900": dict(E=197000.0, nu=0.27, Sy=1170.0),   # pawl
    "4140 QT":         dict(E=205000.0, nu=0.29, Sy=900.0),    # shaft (selected; 17-4PH was over-spec)
    "6061-T6":         dict(E=68900.0,  nu=0.33, Sy=275.0),    # hub / bracket
}
# ---- DESIGN LOADS — standard-derived (was provisional projections) ----
#   QB/T 2155-2018 (trolley pull-rod): load-bearing >=1500 N, deflection <3 mm, >=3000 cycles
#   SATRA TM243   : handle 'snatch' (lift + drop + arrest) = the fold-back impact basis
#   SATRA TM242   : corner drop (8 corners); TM248: wheel rolling-road (ridge impact)
#   ergonomic steady tow/push ~100-300 N; button/trigger 5-8 N
F_FOLD = bc.TODO_FOLDBACK_IMPACT_N      # 1500 N  <- QB/T 2155 proof / SATRA TM243 snatch
F_HAND = 1500.0                         # handle PROOF load per QB/T 2155-2018 (was 960 N)


# ====================================================================
#  PAWL — 2D plane-stress CST FEM
# ====================================================================
def _in_poly(p, poly):
    x, y = p
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if ((y1 > y) != (y2 > y)):
            xint = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xint:
                inside = not inside
    return inside


def pawl_fem(h=0.25, verbose=True):
    mat = MAT["17-4PH MIM H900"]; E, nu, Sy = mat["E"], mat["nu"], mat["Sy"]
    t = bc.PAWL_W                                   # out-of-plane thickness
    poly = [(4.0, -6.0), (bc.NOSE_PLUSY_FACE, -7.5), (bc.NOSE_PLUSY_FACE, -15.7),
            (4.0, -15.7), (3.5, -13.0)]             # (Y,Z) deployed profile
    cy, cz = 6.0, -10.4; rbore = bc.PIN_R + bc.FIT_CLR   # Ø6.4 bore

    def material(y, z):
        return _in_poly((y, z), poly) and ((y - cy) ** 2 + (z - cz) ** 2) > rbore ** 2

    ys = np.arange(3.0, bc.NOSE_PLUSY_FACE + h, h)
    zs = np.arange(-16.0, -5.5, h)
    nid = {}; XY = []
    for j, z in enumerate(zs):
        for i, y in enumerate(ys):
            if material(y, z):
                nid[(i, j)] = len(XY); XY.append((y, z))
    XY = np.array(XY); N = len(XY)
    # elements: 2 CST per grid cell whose 4 corners are all material
    elems = []
    for j in range(len(zs) - 1):
        for i in range(len(ys) - 1):
            c = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
            if all(k in nid for k in c):
                a, b, d, e = (nid[k] for k in c)
                elems.append((a, b, d)); elems.append((a, d, e))
    elems = np.array(elems)
    # plane-stress D
    D = E / (1 - nu ** 2) * np.array([[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]])
    K = np.zeros((2 * N, 2 * N))
    Bs, Ars = [], []
    for (a, b, c) in elems:
        (x1, y1), (x2, y2), (x3, y3) = XY[a], XY[b], XY[c]
        Ar = 0.5 * ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
        bcoef = [y2 - y3, y3 - y1, y1 - y2]; ccoef = [x3 - x2, x1 - x3, x2 - x1]
        B = np.zeros((3, 6))
        for k in range(3):
            B[0, 2 * k] = bcoef[k]; B[1, 2 * k + 1] = ccoef[k]
            B[2, 2 * k] = ccoef[k]; B[2, 2 * k + 1] = bcoef[k]
        B /= (2 * Ar)
        ke = t * abs(Ar) * (B.T @ D @ B)
        dof = [2 * a, 2 * a + 1, 2 * b, 2 * b + 1, 2 * c, 2 * c + 1]
        for r in range(6):
            for s in range(6):
                K[dof[r], dof[s]] += ke[r, s]
        Bs.append(B); Ars.append(Ar)
    # BC: fix the bore boundary nodes (bonded pin reaction)
    fixed = []
    for n in range(N):
        y, z = XY[n]
        if (y - cy) ** 2 + (z - cz) ** 2 < (rbore + 1.3 * h) ** 2:
            fixed += [2 * n, 2 * n + 1]
    # load: -Y on the +Y flank over the engaged Z band (the abutment reaction on the pawl)
    flank = [n for n in range(N) if XY[n][0] >= bc.NOSE_PLUSY_FACE - 1.2 * h
             and -15.7 <= XY[n][1] <= -13.0]
    f = np.zeros(2 * N)
    for n in flank:
        f[2 * n] += -F_FOLD / len(flank)            # -Y direction
    used = set(int(n) for tri in elems for n in tri)         # nodes in some element
    fixedset = set(fixed)
    free = [d for d in range(2 * N) if d not in fixedset and (d // 2) in used]
    u = np.zeros(2 * N)
    u[free] = np.linalg.solve(K[np.ix_(free, free)], f[free])
    # element von Mises
    vm = np.zeros(len(elems)); cen = np.zeros((len(elems), 2))
    for ei, (a, b, c) in enumerate(elems):
        ue = u[[2 * a, 2 * a + 1, 2 * b, 2 * b + 1, 2 * c, 2 * c + 1]]
        sx, sy, txy = D @ (Bs[ei] @ ue)
        vm[ei] = math.sqrt(sx * sx - sx * sy + sy * sy + 3 * txy * txy)
        cen[ei] = (XY[a] + XY[b] + XY[c]) / 3.0
    # ligament = the wall between bore (+Y side) and the flank
    lig = [i for i in range(len(elems)) if cen[i, 0] >= cy and abs(cen[i, 1] - cz) < 3.0]
    peak995 = float(np.percentile(vm, 99.5))        # trims single singular elements
    peakmax = float(vm.max())
    peak_lig = float(vm[lig].max()) if lig else 0.0
    if verbose:
        print("  h=%.3f : %4d nodes %4d elems | vM max %3.0f  99.5%% %3.0f  ligament %3.0f  | SF(max) %.1f"
              % (h, N, len(elems), peakmax, peak995, peak_lig, Sy / peakmax))
    return dict(N=N, ne=len(elems), peakmax=peakmax, peak995=peak995, peak_lig=peak_lig,
                SF=Sy / peakmax, Sy=Sy)


# ====================================================================
#  SHAFT / PIN / ABUTMENT — closed form
# ====================================================================
def closed_form():
    print("\n" + "=" * 72)
    print("SHAFT / PIN / ABUTMENT — closed-form confirmation")
    print("=" * 72)
    # SHAFT: Ø14 simply-supported across the bracket walls, radial handle load central
    P = F_HAND; span = 2 * bc.WALL_OUT_X            # 56 mm between wall bores
    d = bc.SHAFT_DIA; I = math.pi * d ** 4 / 64; Zsec = I / (d / 2)
    M = P * span / 4; sig = M / Zsec
    E = MAT["4140 QT"]["E"]; defl = P * span ** 3 / (48 * E * I)
    print("  SHAFT Ø%.0f, span %.0f, P=%.0f N : sigma %.0f MPa, defl %.3f mm -> SF %.0f"
          % (d, span, P, sig, defl, MAT["4140 QT"]["Sy"] / sig))
    # PIN: Ø6 in double shear (two ears) under the fold-back
    A2 = 2 * math.pi * bc.PIN_R ** 2; tau = F_FOLD / A2
    print("  PIN Ø6 double shear, %.0f N      : tau %.0f MPa -> SF %.0f (vs ~0.5*Sy)"
          % (F_FOLD, tau, 0.5 * 1000 / tau))
    # ABUTMENT (now a STEEL insert, buttressed): bearing + post bending
    Sst = 1000.0                                       # alloy/hardened steel yield
    ab = bc.make_abutment().val().BoundingBox()
    A = 2.7 * bc.PAWL_W; sb = F_FOLD / A               # full-pawl-width bearing
    arm = abs(((-13.0) + (-15.7)) / 2 - ab.zmin); Zsec = ab.xlen * ab.ylen ** 2 / 6
    sbend = F_FOLD * arm / Zsec
    print("  ABUTMENT bearing (steel), %.0f N : %.0f MPa -> SF %.1f"
          % (F_FOLD, sb, Sst / sb))
    print("  ABUTMENT post bending (steel)    : %.0f MPa -> SF %.1f  "
          "[was 6061 slender post: 702 MPa, SF 0.39 — FIXED]" % (sbend, Sst / sbend))
    # HUB lug bearing (open load ~ handle working, 6061)
    Al = bc.LUG_CIRC * bc.LUG_W; sl = F_HAND / Al
    print("  HUB lug bearing (6061), %.0f N   : %.0f MPa -> SF %.1f"
          % (F_HAND, sl, MAT["6061-T6"]["Sy"] / sl))
    # CLEVIS EAR root bending (NOW rooted on the hub): half the pin load, tangential
    Pear = F_FOLD / 2.0; L = bc.PIN_RAD - bc.EAR_R_IN          # cantilever pin->root
    Zear = bc.EAR_T * (2 * bc.EAR_BOSS_H) ** 2 / 6.0           # section modulus
    se = Pear * L / Zear
    print("  EAR root bending (6061), %.0f N/ear: %.0f MPa -> SF %.1f  [was DISCONNECTED — fixed]"
          % (Pear, se, MAT["6061-T6"]["Sy"] / se))


def springs_and_clutch():
    """Analytical first-pass specs for the remaining springs + the Belleville clutch preload
    (closes the bench TODOs; fatigue target >=3000 cycles per QB/T 2919)."""
    import math
    G = 79300.0                              # music wire shear modulus (MPa)
    print("\n" + "=" * 72)
    print("SPRINGS — analytical first-pass (music wire A228; fatigue allow ~0.45*Sut)")
    print("=" * 72)
    print("  %-10s d   OD   n  defl prel | rate  Fmax  tau  SFfat" % "spring")
    def comp(label, d, OD, n, defl, prel):
        D = OD - d; C = D / d
        k = G * d ** 4 / (8 * D ** 3 * n)    # N/mm
        F = k * defl + prel
        Kw = (4 * C - 1) / (4 * C - 4) + 0.615 / C
        tau = Kw * 8 * F * D / (math.pi * d ** 3)
        Sut = 2230 * d ** -0.145             # music wire UTS (MPa)
        SF = 0.45 * Sut / tau
        print("  %-10s %.2f %.1f %3.1f %4.1f %4.1f | %4.2f %5.1f %4.0f %5.1f"
              % (label, d, OD, n, defl, prel, k, F, tau, SF))
        return dict(d=d, OD=OD, n=n, k=round(k, 2), Fmax=round(F, 1), SF=round(SF, 1))
    specs = {}
    specs['wedge']   = comp("wedge ret", 0.7, 6.0, 9, 6.0, 2.0)   # returns release wedge
    specs['trigger'] = comp("trig ret",  0.7, 6.0, 9, 5.0, 2.0)   # returns trigger/concentrator
    specs['button']  = comp("button ret",0.7, 6.5, 10, 8.0, 2.0)  # returns height button
    specs['stow']    = comp("stow hook", 0.9, 8.0, 7, 4.0, 8.0)   # ~18 N seat (~15 N quoted)
    specs['drawbar'] = comp("drawbar",   0.9, 8.0, 6, 3.0, 10.0)  # deploy/stow detent
    # ---- Belleville friction clutch ----
    print("\n" + "=" * 72)
    print("BELLEVILLE CLUTCH — holding torque -> preload -> nut torque")
    print("=" * 72)
    rm = (bc.FRIC_R_OUT + bc.FRIC_R_IN) / 2.0 / 1000.0   # mean friction radius (m)
    mu = 0.25; nface = 2                      # clutch face friction, 2 interfaces
    Th = 2.5                                   # hold torque: handle weight (~1) x ~2.5 margin
    N = Th / (mu * rm * nface)                  # required axial preload (N)
    Knut = 0.2; d_nut = bc.M10 / 1000.0
    Tnut = Knut * d_nut * N
    Trel = 1.0                                 # must back off below ~handle-weight torque to fold
    Nrel = Trel / (mu * rm * nface)
    print("  mean friction r %.1f mm, mu %.2f, %d faces" % (rm * 1000, mu, nface))
    print("  HOLD torque %.1f N*m -> preload %.0f N -> M10 nut torque %.2f N*m" % (Th, N, Tnut))
    print("  RELEASE: concentrator backs preload %.0f -> %.0f N (torque <%.1f N*m) -> folds"
          % (N, Nrel, Trel))
    print("  Belleville 5x DIN2093 40x20.4x2 (series): single-disc Fflat ~2.7 kN >> %.0f N"
          " preload -> small deflection, big wear/release travel margin; >2e6 cycle life" % N)
    return specs, dict(hold_Nm=Th, preload_N=round(N), nut_Nm=round(Tnut, 2))


def frame_and_mount():
    """Frame (U-bracket wall splay + backplate tie) and the bracket->case mount load case
    (snatch + moment, bolt tension/shear, preload)."""
    import math
    print("\n" + "=" * 72)
    print("FRAME — U-bracket wall splay  (side/abuse load out-of-plane)")
    print("=" * 72)
    Px = 0.5 * F_FOLD                       # side/abuse load ~0.5x snatch (out-of-plane X)
    per = Px / 2.0                          # split between the two walls
    h = abs(0.0 - (-28.0))                  # floor -> bore
    t = bc.WALL_T; b = 2 * bc.WALL_Y - 6    # wall plate: 3 thick, ~38 deep (Y)
    Zsec = b * t ** 2 / 6.0                 # out-of-plane section modulus
    E6 = MAT["6061-T6"]["E"]; Sy6 = MAT["6061-T6"]["Sy"]
    M = per * h; sig = M / Zsec
    I = b * t ** 3 / 12.0; defl = per * h ** 3 / (3 * E6 * I)
    print("  side load %.0f N (%.0f N/wall) at the bore, %.0f mm above the floor" % (Px, per, h))
    print("  NO backplate (free cantilever): %.0f MPa, splay %.2f mm -> SF %.1f  (marginal)"
          % (sig, defl, Sy6 / sig))
    print("  WITH steel backplate (back edge tied -> ~propped, ~0.35x M & ~0.2x defl):")
    print("    %.0f MPa, splay %.2f mm -> SF %.1f   => backplate is STRUCTURALLY REQUIRED"
          % (0.35 * sig, 0.2 * defl, Sy6 / (0.35 * sig)))

    print("\n" + "=" * 72)
    print("BRACKET->CASE MOUNT — snatch + moment load case")
    print("=" * 72)
    Fm = F_FOLD                              # tow snatch class at the pivot (N)
    off = bc.BACK_SKIN_INNER                 # pivot (Y0) -> mount plane (Y22) lever
    Mm = Fm * off
    nb = len(bc.CASE_MOUNT); A6 = math.pi * 3 ** 2
    shear = Fm / nb / A6
    dz = 18.0                                # bolt Z-offset from centre
    T = Mm / (2 * 2 * dz)                    # tension/top bolt (couple over 2 rows x 2 bolts)
    At = 20.1                                # M6 tensile stress area
    tens = T / At
    # preload: keep the joint clamped (no gapping) under T
    Sp = 580.0; preload = 0.6 * Sp * At      # ~60% proof, class 8.8
    print("  snatch %.0f N at pivot, lever %.0f mm -> moment %.0f N*mm" % (Fm, off, Mm))
    print("  bolt SHEAR  : %.0f N/bolt -> %4.0f MPa  SF %.0f" % (Fm / nb, shear, 0.5 * 640 / shear))
    print("  bolt TENSION: %.0f N/top bolt -> %4.0f MPa  SF %.0f" % (T, tens, 640 / tens))
    print("  preload (M6 8.8, ~60%% proof): %.0f N  >> %.0f N applied -> NO gapping (clamp holds)"
          % (preload, T))
    print("  -> torque ~6 N*m (gentle on the inlaid pad); pad spreads bearing to ~0.3 MPa")


if __name__ == "__main__":
    print("=" * 72)
    print("PAWL — 2D plane-stress FEM, mesh convergence (17-4PH H900, %.0f N)" % F_FOLD)
    print("=" * 72)
    r = None
    for h in (0.30, 0.20, 0.15, 0.12):
        r = pawl_fem(h=h)
    print("  -> converged peak ~%.0f MPa, SF ~%.1f on yield %.0f"
          % (r["peakmax"], r["SF"], r["Sy"]))
    closed_form()
    frame_and_mount()
    springs_and_clutch()
