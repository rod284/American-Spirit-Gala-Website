#!/usr/bin/env python3
# ============================================================================
#  Gravitcase — MP4 animations (offscreen VTK frames -> imageio/ffmpeg)
#    deploy_handle.mp4 : single case, handle pulls UP then pivots OUT (two-phase)
#    two_case_hitch.mp4: lead case deploys while towing a second case (hitched)
#  Case shells are translucent so the mechanism reads.
# ============================================================================
import os, tempfile
import cadquery as cq
import imageio.v2 as imageio
from vtkmodules.vtkRenderingCore import vtkWindowToImageFilter
from vtkmodules.util.numpy_support import vtk_to_numpy
import render_handle as rh
import build_core as bc

HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(os.path.dirname(HERE), "renders")
TD = tempfile.mkdtemp()
_fid = [0]

DEP = bc.DEPLOY_ANGLE


def capture(win):
    win.Render()
    w2i = vtkWindowToImageFilter(); w2i.SetInput(win); w2i.ReadFrontBufferOff(); w2i.Update()
    img = w2i.GetOutput(); dx, dy, _ = img.GetDimensions()
    arr = vtk_to_numpy(img.GetPointData().GetScalars()).reshape(dy, dx, -1)[::-1]
    return arr[:, :, :3].copy()


def handle_actors(theta, extend, off=(0, 0, 0)):
    """The MOVING handle group at (theta, extend), optionally translated by `off`."""
    _fid[0] += 1; t = "h%d" % _fid[0]
    gt = bc.spine_top(extend)
    raw = [("spine", bc.make_spine([], extend), False),
           ("overmold", bc.make_overmold(gt), False),
           ("button", bc.make_grip_button(gt, 0.0), True),
           ("trigger", bc.make_grip_trigger(gt, 0.0), False),
           ("shaft", bc.make_shaft(), True),
           ("hub", bc.make_hub(), True)]
    out = []
    for nm, wp, metal in raw:
        wp = bc.deploy_rotate(wp, theta).translate(off)
        out.append(rh.actor(wp, bc.COL.get(nm, cq.Color(.7, .7, .72, 1)), TD, t + nm, metal=metal))
    return out


def static_actors(off=(0, 0, 0), theta_draw=0.0):
    _fid[0] += 1; t = "s%d" % _fid[0]
    items = [("case_back", bc.make_case_back(), cq.Color(0.60, 0.64, 0.72, 0.22), False),
             ("case_front", bc.make_case_front(), cq.Color(0.66, 0.70, 0.78, 0.16), False),
             ("wheels", bc.make_wheels(), cq.Color(0.13, 0.13, 0.15, 1.0), True),
             ("bracket", bc.make_bracket([]), cq.Color(0.60, 0.64, 0.70, 1.0), True),
             ("drawbar", bc.make_drawbar(theta_draw), bc.COL["drawbar"], False)]
    out = []
    for nm, wp, col, metal in items:
        out.append(rh.actor(wp.translate(off), col, TD, t + nm, metal=metal))
    return out


def deploy_schedule():
    s = [(0.0, 0.0)] * 3
    s += [(i / 12.0, 0.0) for i in range(13)]                 # phase 1: telescope UP
    s += [(1.0, i / 10.0 * DEP) for i in range(1, 11)]        # phase 2: pivot OUT
    s += [(1.0, DEP)] * 4
    return s


def write_mp4(frames, name, fps=20):
    out = os.path.join(RENDERS, name)
    w = imageio.get_writer(out, fps=fps, codec="libx264", quality=8, macro_block_size=8)
    for f in frames:
        w.append_data(f)
    w.close()
    print("wrote", out, os.path.getsize(out), "bytes,", len(frames), "frames")


def frame_camera(ren, extra_actors, dirv, zoom=0.82):
    for a in extra_actors:
        ren.AddActor(a)
    cam = ren.GetActiveCamera(); ren.ResetCamera(); fp = cam.GetFocalPoint()
    cam.SetPosition(fp[0] + dirv[0], fp[1] + dirv[1], fp[2] + dirv[2]); cam.SetViewUp(0, 0, 1)
    ren.ResetCamera(); cam.Zoom(zoom); ren.ResetCameraClippingRange()
    for a in extra_actors:
        ren.RemoveActor(a)


def anim_deploy():
    ren, win = rh.scene((940, 1040))
    for a in static_actors():
        ren.AddActor(a)
    sched = deploy_schedule()
    N = len(sched); phi0, orbit = -22.0, 44.0       # slow orbit across the clip
    frames = []
    for k, (ext, th) in enumerate(sched):
        acts = handle_actors(th, ext)
        for a in acts:
            ren.AddActor(a)
        orbit_cam(ren, (0, -40, 150), 1500, 14, phi0 + orbit * k / (N - 1))
        frames.append(capture(win))
        for a in acts:
            ren.RemoveActor(a)
    write_mp4(frames, "deploy_handle.mp4")


def case_static(off=(0, 0, 0), with_handle=False, with_drawbar=False, with_wheels=True):
    """Static case actors at `off`: shells + bracket (+ wheels), optionally a STOWED
    handle (spine+overmold) and/or a STOWED drawbar (when the OTHER one animates)."""
    _fid[0] += 1; t = "c%d" % _fid[0]
    items = [("case_back", bc.make_case_back(), cq.Color(0.60, 0.64, 0.72, 0.22), False),
             ("case_front", bc.make_case_front(), cq.Color(0.66, 0.70, 0.78, 0.16), False),
             ("bracket", bc.make_bracket([]), cq.Color(0.60, 0.64, 0.70, 1.0), True)]
    if with_wheels:
        items.append(("wheels", bc.make_wheels(), cq.Color(0.13, 0.13, 0.15, 1.0), True))
    if with_handle:
        items += [("spine", bc.make_spine([], 0.0), bc.COL["spine"], False),
                  ("overmold", bc.make_overmold(bc.spine_top(0.0)), bc.COL["overmold"], False)]
    if with_drawbar:
        items += [("drawbar", bc.make_drawbar(0.0), bc.COL["drawbar"], False)]
    return [rh.actor(wp.translate(off), col, TD, t + nm, metal=m) for nm, wp, col, m in items]


def make_ground(zg):
    """A striped ground strip along Y so the rolling motion reads."""
    _fid[0] += 1; t = "gr%d" % _fid[0]
    acts = []
    for i, yc in enumerate(range(-900, 1000, 100)):
        col = cq.Color(0.82, 0.84, 0.87, 1) if i % 2 else cq.Color(0.70, 0.73, 0.77, 1)
        tile = cq.Workplane("XY").box(620, 100, 4, centered=(True, True, False)).translate((0, yc, zg - 4))
        acts.append(rh.actor(tile, col, TD, t + str(i)))
    return acts


def orbit_cam(ren, focal, R, el_deg, phi_deg):
    import math
    el, ph = math.radians(el_deg), math.radians(phi_deg)
    cam = ren.GetActiveCamera()
    cam.SetFocalPoint(*focal)
    cam.SetPosition(focal[0] + R * math.cos(el) * math.sin(ph),
                    focal[1] - R * math.cos(el) * math.cos(ph),
                    focal[2] + R * math.sin(el))
    cam.SetViewUp(0, 0, 1); ren.ResetCameraClippingRange()


def anim_two_case():
    """BACK case deploys the HANDLE; FRONT case deploys its TOW BAR to hitch it; then the
    hitched pair ROLLS forward over a striped ground while the camera slowly ORBITS."""
    import math
    L = bc.DRAWBAR_LEN
    td_hitch = math.degrees(math.acos((bc.DRAW_PIVOT_Z - bc.RX_Z) / L))
    ball_y = bc.DRAW_PIVOT_Y + L * math.sin(math.radians(td_hitch))
    B_OFF_Y = ball_y - (bc.SHELL_BACK_Y - bc.CASE_D)                  # BACK case behind, +Y
    zg = bc.CASE_Z_BOT - bc.WHEEL_DIA                                 # ground (wheel bottom)
    ren, win = rh.scene((1280, 800))
    ground = make_ground(zg)
    A_body = case_static((0, 0, 0), with_handle=True, with_wheels=False)   # front: stowed handle
    B_body = case_static((0, B_OFF_Y, 0), with_drawbar=True, with_wheels=False)  # back: stowed drawbar
    for a in ground + A_body + B_body:
        ren.AddActor(a)
    R_w = bc.WHEEL_DIA / 2.0
    # schedule: (extend, theta, td, y_roll)
    s = [(0, 0, 0, 0)] * 2
    s += [(i / 10.0, 0, 0, 0) for i in range(11)]                     # back handle UP
    s += [(1, i / 8.0 * DEP, 0, 0) for i in range(1, 9)]              # back handle PIVOT
    s += [(1, DEP, i / 10.0 * td_hitch, 0) for i in range(1, 11)]     # front tow bar HITCH
    s += [(1, DEP, td_hitch, 0)] * 2
    ROLL = -480.0
    s += [(1, DEP, td_hitch, i / 16.0 * ROLL) for i in range(1, 17)]  # ROLL forward
    s += [(1, DEP, td_hitch, ROLL)] * 3
    N = len(s); phi0, orbit = -30.0, 60.0
    cy = B_OFF_Y / 2.0
    frames = []
    for k, (ext, th, td, yr) in enumerate(s):
        for a in A_body:
            a.SetPosition(0, yr, 0)
        for a in B_body:
            a.SetPosition(0, yr, 0)
        mov = handle_actors(th, ext, off=(0, B_OFF_Y + yr, 0))                       # BACK handle
        mov.append(rh.actor(bc.make_drawbar(td).translate((0, yr, 0)),               # FRONT tow bar
                            bc.COL["drawbar"], TD, "db%d" % _fid[0], False))
        spin = -math.degrees(yr / R_w)                                               # roll the wheels
        wc = cq.Color(0.13, 0.13, 0.15, 1.0)
        mov.append(rh.actor(bc.make_wheels(spin).translate((0, yr, 0)), wc, TD, "wa%d" % _fid[0], True))
        mov.append(rh.actor(bc.make_wheels(spin).translate((0, B_OFF_Y + yr, 0)), wc, TD, "wb%d" % _fid[0], True))
        for a in mov:
            ren.AddActor(a)
        orbit_cam(ren, (0, cy + yr, 150), 2050, 16, phi0 + orbit * k / (N - 1))
        frames.append(capture(win))
        for a in mov:
            ren.RemoveActor(a)
    write_mp4(frames, "two_case_hitch.mp4", fps=24)


def grip_actors(press=0.0, squeeze=0.0):
    """The grip (translucent core) + button + trigger + the two driven rod stubs, at the
    extended grip top.  press drives the telerod down; squeeze drives the pivrod down."""
    _fid[0] += 1; t = "g%d" % _fid[0]
    gt = bc.spine_top(1.0)
    rt = bc.grip_geom(gt)["rod_top"]
    tele = cq.Workplane("XY").circle(bc.ACT_ROD_R).extrude(70).translate((-bc.ACT_BORE_X, 0, rt - 70 - press * bc.BTN_TRAVEL))
    piv = cq.Workplane("XY").circle(bc.ACT_ROD_R).extrude(70).translate((bc.ACT_BORE_X, 0, rt - 70 - squeeze * bc.ACT_CONC_STROKE))
    raw = [("core", bc.make_thandle(gt), cq.Color(0.55, 0.60, 0.70, 0.30), False),
           ("button", bc.make_grip_button(gt, press), bc.COL["button"], True),
           ("trigger", bc.make_grip_trigger(gt, squeeze), bc.COL["trigger"], False),
           ("tele", tele, cq.Color(0.80, 0.82, 0.85, 1.0), True),
           ("piv", piv, cq.Color(0.55, 0.80, 0.85, 1.0), True)]
    return [rh.actor(wp, col, TD, t + nm, metal=m) for nm, wp, col, m in raw]


def _control_anim(kind, name, dirv, zoom):
    ren, win = rh.scene((1000, 850))
    frame_camera(ren, grip_actors(0, 0), dirv, zoom=zoom)
    ramp = [0, 0] + [i / 10.0 for i in range(11)] + [1.0] * 4 + [1 - i / 10.0 for i in range(11)] + [0, 0]
    frames = []
    for v in ramp:
        acts = grip_actors(press=v) if kind == "button" else grip_actors(squeeze=v)
        for a in acts:
            ren.AddActor(a)
        frames.append(capture(win))
        for a in acts:
            ren.RemoveActor(a)
    write_mp4(frames, name)


def anim_button():
    _control_anim("button", "button_push.mp4", (-90, -230, 130), zoom=1.7)   # from front-above


def anim_trigger():
    _control_anim("trigger", "trigger_pull.mp4", (-70, 210, -60), zoom=1.7)   # from back-below


def make_master():
    """Stitch the four clips into one master reel (letterboxed to a common canvas)."""
    import numpy as np
    from PIL import Image
    W, H = 1200, 820
    clips = ["deploy_handle.mp4", "two_case_hitch.mp4", "button_push.mp4", "trigger_pull.mp4"]
    out = os.path.join(RENDERS, "gravitcase_reel.mp4")
    w = imageio.get_writer(out, fps=24, codec="libx264", quality=8, macro_block_size=8)
    for c in clips:
        canvas = None
        for fr in imageio.get_reader(os.path.join(RENDERS, c)):
            im = Image.fromarray(fr); im.thumbnail((W, H))
            canvas = Image.new("RGB", (W, H), (226, 229, 234))
            canvas.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
            w.append_data(np.asarray(canvas))
        for _ in range(10):                      # hold the last frame between clips
            w.append_data(np.asarray(canvas))
    w.close()
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or ["all"]
    if "all" in which or "deploy" in which:
        anim_deploy()
    if "all" in which or "two" in which:
        anim_two_case()
    if "all" in which or "button" in which:
        anim_button()
    if "all" in which or "trigger" in which:
        anim_trigger()
    if "all" in which or "master" in which:
        make_master()
