#!/usr/bin/env python3
# ============================================================================
#  Gravitcase — HANDLE-focused renders (clean, light background)
#
#  The telescoping handle (5-tube octagon spine + grip cap) was hard to read in
#  the assembly shots (dark, over-zoomed, washed out behind the translucent
#  case).  This renders it on its own and in the real towing pose:
#    handle_full.png  — fully extended, standing vertical, whole cascade + grip
#    handle_tow.png   — deployed 45 deg AND extended: the actual tow position
#    handle_stowed.png— collapsed in the case (handle nested, flush)
# ============================================================================
import os, tempfile
import cadquery as cq
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingCore import (
    vtkRenderer, vtkRenderWindow, vtkActor, vtkPolyDataMapper,
    vtkWindowToImageFilter, vtkLightKit,
)
from vtkmodules.vtkIOImage import vtkPNGWriter
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import build_core as bc

HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(os.path.dirname(HERE), "renders")
os.makedirs(RENDERS, exist_ok=True)

# give each telescoping section its own tint so the cascade reads clearly
SECTION_COLS = [
    cq.Color(0.20, 0.42, 0.62, 1.0),   # S1 (root, biggest)
    cq.Color(0.25, 0.52, 0.66, 1.0),   # S2
    cq.Color(0.32, 0.62, 0.68, 1.0),   # S3
    cq.Color(0.42, 0.72, 0.70, 1.0),   # S4
    cq.Color(0.62, 0.82, 0.74, 1.0),   # S5 (grip, smallest)
]


def split_spine_sections(extend):
    """Rebuild the spine as separate per-section solids so each tube can be a
    distinct colour (the model unions them into one part for export)."""
    step = bc.SPINE_STEP_CLP + extend * (bc.SPINE_STEP_EXT - bc.SPINE_STEP_CLP)
    secs = []
    for i, (W, D, wall) in enumerate(bc.SPINE_TUBES):
        hw, hd = W / 2.0, D / 2.0
        bz = bc.SPINE_BASE_Z + i * step
        outer = bc.oct_prism(hw, hd, bc.SPINE_CH, bz, bz + bc.SPINE_LEN)
        bore = bc.oct_prism(hw - wall, hd - wall, bc.SPINE_CH, bz - 1, bz + bc.SPINE_LEN + 1)
        tube = outer.cut(bore)
        if i == 4:
            top = bz + bc.SPINE_LEN
            tube = tube.union(bc.make_thandle(top))   # real T-handle grip
        secs.append(tube)
    return secs


def actor(wp, color, td, name, metal=False):
    stl = os.path.join(td, name + ".stl")
    cq.exporters.export(wp, stl, tolerance=0.04, angularTolerance=0.1)
    rdr = vtkSTLReader(); rdr.SetFileName(stl); rdr.Update()
    m = vtkPolyDataMapper(); m.SetInputConnection(rdr.GetOutputPort())
    a = vtkActor(); a.SetMapper(m)
    p = a.GetProperty()
    r, g, b, op = color.toTuple()
    p.SetInterpolationToPhong()
    p.SetColor(r, g, b); p.SetOpacity(op)
    p.SetAmbient(0.25); p.SetDiffuse(0.75)
    p.SetSpecular(0.45 if metal else 0.30); p.SetSpecularPower(40 if metal else 25)
    p.SetSpecularColor(1, 1, 1) if metal else p.SetSpecularColor(min(1, r+.3), min(1, g+.3), min(1, b+.3))
    return a


def scene(size):
    ren = vtkRenderer()
    ren.GradientBackgroundOn()
    ren.SetBackground(0.93, 0.94, 0.96)      # light, clean
    ren.SetBackground2(0.78, 0.82, 0.88)
    ren.UseFXAAOn()
    win = vtkRenderWindow(); win.SetOffScreenRendering(1)
    win.SetMultiSamples(8); win.AddRenderer(ren); win.SetSize(*size)
    kit = vtkLightKit()
    kit.SetKeyLightIntensity(1.15); kit.SetKeyToFillRatio(2.0)
    kit.SetKeyToHeadRatio(2.5); kit.SetKeyToBackRatio(3.0)
    kit.AddLightsToRenderer(ren)
    return ren, win


def shoot(ren, win, fname):
    win.Render()
    w2i = vtkWindowToImageFilter(); w2i.SetInput(win); w2i.SetScale(1); w2i.Update()
    out = os.path.join(RENDERS, fname)
    wr = vtkPNGWriter(); wr.SetFileName(out)
    wr.SetInputConnection(w2i.GetOutputPort()); wr.Write()
    print("wrote", out, os.path.getsize(out))


def render(actors, view, fname, size):
    ren, win = scene(size)
    for a in actors:
        ren.AddActor(a)
    cam = ren.GetActiveCamera()
    ren.ResetCamera()
    fp = cam.GetFocalPoint()
    dx, dy, dz = view["dir"]
    cam.SetPosition(fp[0] + dx, fp[1] + dy, fp[2] + dz)
    cam.SetViewUp(*view["up"])
    ren.ResetCamera()                      # re-fit ALONG the new direction
    cam.Zoom(view.get("zoom", 0.92))       # slight margin so nothing is clipped
    ren.ResetCameraClippingRange()
    shoot(ren, win, fname)


if __name__ == "__main__":
    td = tempfile.mkdtemp()

    # ---- 1) extended handle on its own, standing vertical -------------------
    secs = split_spine_sections(1.0)
    _, parts, _, _, _ = bc.build(0.0, 0.0, spine_extend=1.0)
    base = [actor(parts[k], bc.COL.get(k, cq.Color(0.7, 0.7, 0.7, 1)), td, k, metal=True)
            for k in ("shaft", "hub", "ears") if k in parts]
    sec_actors = [actor(s, SECTION_COLS[i], td, f"sec{i}") for i, s in enumerate(secs)]
    render(base + sec_actors,
           {"dir": (-360, -480, 120), "up": (0, 0, 1), "zoom": 0.9},
           "handle_full.png", (760, 1500))

    # ---- 2) THE TOW POSE: handle deployed 45 deg AND fully extended ---------
    secsT = split_spine_sections(1.0)
    secsT = [s.rotate((0, 0, 0), (1, 0, 0), -bc.DEPLOY_ANGLE) for s in secsT]
    _, partsT, _, _, _ = bc.build(bc.DEPLOY_ANGLE, 0.0, spine_extend=1.0)
    baseT = [actor(partsT[k], bc.COL.get(k, cq.Color(0.7, 0.7, 0.7, 1)), td, k + "T", metal=True)
             for k in ("shaft", "hub", "ears") if k in partsT]
    caseT = actor(bc.make_case(), cq.Color(0.62, 0.66, 0.72, 0.18), td, "caseT")
    wheelsT = actor(bc.make_wheels(), cq.Color(0.30, 0.30, 0.34, 1.0), td, "whT", metal=True)
    sec_actorsT = [actor(s, SECTION_COLS[i], td, f"secT{i}") for i, s in enumerate(secsT)]
    render(baseT + sec_actorsT + [caseT, wheelsT],
           {"dir": (-520, -620, 240), "up": (0, 0, 1), "zoom": 0.88},
           "handle_tow.png", (1300, 1150))

    # ---- 2b) GRIP DETAIL close-up: crossbar, button (top), trigger (under) ---
    grip = bc.make_thandle(bc.spine_top(1.0))
    s5 = split_spine_sections(1.0)[4]
    ga = actor(grip, cq.Color(0.30, 0.40, 0.52, 1.0), td, "grip", metal=False)
    s5a = actor(s5, SECTION_COLS[4], td, "s5only")
    ren, win = scene((1300, 1000))
    ren.AddActor(ga); ren.AddActor(s5a)
    cam = ren.GetActiveCamera()
    fz = bc.spine_top(1.0) + 8
    cam.SetFocalPoint(0, 0, fz)
    cam.SetPosition(-150, -260, fz + 70)
    cam.SetViewUp(0, 0, 1); cam.SetViewAngle(30)
    ren.ResetCameraClippingRange()
    shoot(ren, win, "handle_detail.png")

    # ---- 2c) GRIP INTERNALS: translucent core revealing button + bell-crank +
    #          rod tops (the height button drives the telerod, the squeeze trigger's
    #          bell-crank drives the pivrod) ----------------------------------------
    gt = bc.spine_top(1.0)
    rod_top = gt - 6.0
    corei = bc.make_thandle(gt)
    btn = bc.make_grip_button(gt, 0.0)
    trg = bc.make_grip_trigger(gt, 0.55)        # mid-squeeze, to read the bell-crank
    telerod = (cq.Workplane("XY").circle(bc.ACT_ROD_R).extrude(40)
               .translate((-bc.ACT_BORE_X, 0, rod_top - 40)))
    pivrod = (cq.Workplane("XY").circle(bc.ACT_ROD_R).extrude(40)
              .translate((bc.ACT_BORE_X, 0, rod_top - 40)))
    jpin = bc.make_joint_pin(gt)                 # core-to-S5 twin dowels + ferrules
    springs = bc.make_grip_springs(gt)           # button + trigger return springs
    acts = [
        actor(corei, cq.Color(0.55, 0.62, 0.72, 0.22), td, "corei"),       # translucent core
        actor(btn, cq.Color(0.20, 0.45, 0.85, 1.0), td, "btni", metal=True),
        actor(trg, cq.Color(0.90, 0.35, 0.25, 1.0), td, "trgi"),
        actor(telerod, cq.Color(0.78, 0.80, 0.82, 1.0), td, "teli", metal=True),
        actor(pivrod, cq.Color(0.55, 0.80, 0.85, 1.0), td, "pivi", metal=True),
        actor(jpin, cq.Color(0.85, 0.86, 0.88, 1.0), td, "jpini", metal=True),
        actor(springs, cq.Color(0.60, 0.62, 0.66, 1.0), td, "spri", metal=True),
    ]
    ren, win = scene((1300, 1050))
    for a in acts:
        ren.AddActor(a)
    cam = ren.GetActiveCamera()
    fz = gt + 6
    cam.SetFocalPoint(0, 2, fz)
    cam.SetPosition(-120, -240, fz + 40)
    cam.SetViewUp(0, 0, 1); cam.SetViewAngle(32)
    ren.ResetCameraClippingRange()
    shoot(ren, win, "handle_internals.png")

    # ---- 2d) FINISHED GRIP: soft TPE overmold over the core + button (hand surface) --
    over = bc.make_overmold(gt)
    coreg = bc.make_thandle(gt)
    btng = bc.make_grip_button(gt, 0.0)
    actsg = [
        actor(coreg, cq.Color(0.40, 0.44, 0.50, 1.0), td, "coreg"),         # rigid core
        actor(over, cq.Color(0.12, 0.13, 0.16, 0.78), td, "overg"),         # soft TPE skin
        actor(btng, cq.Color(0.20, 0.45, 0.85, 1.0), td, "btng", metal=True),
    ]
    ren, win = scene((1300, 1000))
    for a in actsg:
        ren.AddActor(a)
    cam = ren.GetActiveCamera()
    fz = gt + 16
    cam.SetFocalPoint(0, 2, fz)
    cam.SetPosition(-160, -260, fz + 90)
    cam.SetViewUp(0, 0, 1); cam.SetViewAngle(32)
    ren.ResetCameraClippingRange()
    shoot(ren, win, "handle_grip.png")

    # ---- 3) stowed: handle collapsed/nested in the case (flush) -------------
    secsS = split_spine_sections(0.0)
    _, partsS, _, _, _ = bc.build(0.0, 0.0, spine_extend=0.0)
    baseS = [actor(partsS[k], bc.COL.get(k, cq.Color(0.7, 0.7, 0.7, 1)), td, k + "S", metal=True)
             for k in ("shaft", "hub", "ears") if k in partsS]
    caseS = actor(bc.make_case(), cq.Color(0.62, 0.66, 0.72, 0.16), td, "caseS")
    sec_actorsS = [actor(s, SECTION_COLS[i], td, f"secS{i}") for i, s in enumerate(secsS)]
    render(baseS + sec_actorsS + [caseS],
           {"dir": (-360, -520, 160), "up": (0, 0, 1), "zoom": 0.9},
           "handle_stowed.png", (1000, 1250))
