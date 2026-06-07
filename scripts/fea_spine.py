"""Telescoping spine (pull-rod) — structural release analysis vs QB/T 2155 (>=1500 N, <3 mm,
>=3000 cycles).  numpy only.  Load path: grip -> stepped 6061 tubes -> lock pins -> core-S5."""
import math
import numpy as np
import build_core as bc

E = 68900.0; Sy6 = 275.0                 # 6061-T6 (MPa)
F_AX = 1500.0                            # QB/T 2155 axial lift/proof
SEC = bc.SPINE_TUBES                     # (OD, ID, wall) sec0..4


def props(od, idd):
    A = math.pi / 4 * (od ** 2 - idd ** 2)
    I = math.pi / 64 * (od ** 4 - idd ** 4)
    return A, I


def run():
    print("=" * 72)
    print("TELESCOPING SPINE — vs QB/T 2155 (>=1500 N, <3 mm, >=3000 cyc)")
    print("=" * 72)
    for i, (od, idd, w) in enumerate(SEC):
        A, I = props(od, idd)
        print("  sec%d  OD%4.1f ID%4.1f w%.1f | A %5.0f mm^2  I %6.0f mm^4" % (i, od, idd, w, A, I))

    # --- LOCK PIN: carries the axial load across each telescoping joint (in SERIES -> each pin
    #     sees the FULL load).  Binding element. ---
    dpin = bc.LOCK_PIN_D
    As = math.pi / 4 * dpin ** 2
    tau_ss = F_AX / As; tau_ds = F_AX / (2 * As)
    Sy_pin = 1000.0                       # hardened steel dowel
    print("\n  LOCK PIN Ø%.0f @ %.0f N axial:" % (dpin, F_AX))
    print("    single shear %3.0f MPa -> SF %.1f ; double shear %3.0f MPa -> SF %.1f (allow 0.5*Sy=%.0f)"
          % (tau_ss, 0.5 * Sy_pin / tau_ss, tau_ds, 0.5 * Sy_pin / tau_ds, 0.5 * Sy_pin))
    # bearing of the pin on the thin tube wall (the hole) — the OTHER failure mode
    wmin = min(s[2] for s in SEC)
    sb = F_AX / (dpin * wmin)             # bearing on one wall
    print("    pin bearing on %.1f mm tube wall : %.0f MPa -> SF %.1f  <-- WEAK (6061 brg ~%.0f)"
          % (wmin, sb, 1.5 * Sy6 / sb, 1.5 * Sy6))
    # FIX (same as the core-S5 joint): a flanged STEEL eyelet at each lock hole spreads the
    # bearing; the pin bears on steel (ID), the eyelet OD+flange bears on the aluminium.
    od_eye, flange = 6.0, 9.0
    sb_od = F_AX / (od_eye * wmin)                 # eyelet OD on the wall (in-plane)
    sb_fl = F_AX / (math.pi / 4 * (flange ** 2 - od_eye ** 2))   # flange face on the wall
    print("    FIX  flanged Ø%.0f/Ø%.0f steel eyelet: OD-brg %.0f MPa (SF %.1f), flange-face %.0f MPa"
          " (SF %.1f) -> pin now bears on STEEL" % (od_eye, flange, sb_od, 1.5 * Sy6 / sb_od,
          sb_fl, 1.5 * Sy6 / sb_fl))

    # --- BUCKLING: thinnest top section as a cantilever column under axial compression ---
    od, idd, w = SEC[-1]; A4, I4 = props(od, idd)
    Lexp = bc.spine_top(1.0) - bc.CASE_Z_TOP        # exposed cantilever above the case top
    K = 2.0
    Pcr = math.pi ** 2 * E * I4 / (K * Lexp) ** 2
    print("\n  BUCKLING (thinnest sec, cantilever L=%.0f): Pcr %.0f N -> SF %.1f @1500 N"
          % (Lexp, Pcr, Pcr / F_AX))

    # --- LATERAL STIFFNESS: stepped cantilever, exposed length, side load.  numerical
    #     moment-area (discretize, I from the exposed section at each height) ---
    # exposed sections top-down: sec4 (tip) .. sec1 (near case top); ~equal exposed lengths
    nexp = 4
    seg = Lexp / nexp
    Is = [props(*SEC[k][:2])[1] for k in (1, 2, 3, 4)]   # base->tip exposed
    P = 100.0                                            # firm push (stiffness/feel)
    nz = 400; dz = Lexp / nz
    defl = 0.0; slope = 0.0
    # integrate from tip(x=0) to base: curvature = M/EI, M = P*x (x from tip)
    for j in range(nz):
        x = (j + 0.5) * dz
        seg_idx = min(int(x / seg), nexp - 1)           # 0 near tip
        I = Is[nexp - 1 - seg_idx]
        M = P * x
        slope += M / (E * I) * dz
        defl += slope * dz
    print("\n  LATERAL stiffness: %.0f N push -> tip deflection %.1f mm (feel/wobble)" % (P, defl))
    print("  <3 mm QB/T deflection: AXIAL 1500 N -> elastic <0.1 mm; governed by JOINT SLOP")
    print("     (lock-pin fit + overlap take-up) -> control to keep total <3 mm.")
    print("-" * 72)


if __name__ == "__main__":
    run()
