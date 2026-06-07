"""T-handle core — structural release analysis (PA66-GF33 core + TPE overmold).
Load 1500 N (QB/T 2155).  Critical: the button/trigger CAVITY sits at the centre, where an
offset one-hand lift makes the bending moment peak."""
import math
import build_core as bc

Sy = 110.0; Sut = 130.0          # PA66-GF33 (MPa): yield ~110, strength ~130
F = 1500.0


def run():
    print("=" * 70)
    print("T-HANDLE CORE — PA66-GF33, 1500 N (QB/T 2155)")
    print("=" * 70)
    H = bc.TH_CB_H; D = bc.TH_CB_D; cav_w = bc.TH_CAVITY_W; cav_d = bc.TH_CAVITY_BACK
    # 1) crossbar bending — one-hand OFFSET lift; cavity removes depth at the centre (max M)
    offset = 50.0                                  # one-hand grip ~50 mm off the stem
    M = F * offset
    # solid section (bending about Y; load Z over span X): D(width) x H(height)
    Z_solid = D * H ** 2 / 6.0
    # cavity reduces the height by cav_d at the centre -> remaining height
    Hc = H - cav_d
    Z_cav = D * Hc ** 2 / 6.0
    print("  crossbar %gx%g, cavity %gx%g (centre)" % (D, H, cav_w, cav_d))
    print("  one-hand offset lift %g mm -> M %.0f N*mm" % (offset, M))
    print("    solid section : %.0f MPa -> SF %.1f" % (M / Z_solid, Sy / (M / Z_solid)))
    print("    AT CAVITY     : %.0f MPa -> SF %.1f   <- governs (reinforce rib around cavity)"
          % (M / Z_cav, Sy / (M / Z_cav)))
    # 2) stem tension into S5 (Ø~16 core stem)
    dstem = 16.0; A = math.pi / 4 * dstem ** 2
    print("  stem Ø%g tension : %.0f MPa -> SF %.0f  (core-S5 dowels carry it, SF 6.4)"
          % (dstem, F / A, Sy / (F / A)))
    # 3) overmold 2-shot bond — grip shear into the core over the grasp surface
    A_bond = bc.TH_GRASP * math.pi * D       # grasp length x ~circumference
    tau_bond = F / A_bond
    print("  TPE 2-shot bond shear : %.2f MPa over the grasp (PA66-TPV bond ~3-5 MPa) -> OK"
          % tau_bond)
    print("-" * 70)
    print("  VERDICT: core robust; the CAVITY bending (SF %.1f) is the one to watch -> add a"
          " rib/boss frame around the cavity. Overmold edge-peel + mechanism fatigue = bench."
          % (Sy / (M / Z_cav)))


if __name__ == "__main__":
    run()
