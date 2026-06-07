#!/usr/bin/env python3
# ============================================================================
#  Gravitcase — drawbar deployment animation
#
#  Renders the tow bar swinging on its lower pivot from stowed (straight down)
#  out to full deploy (ball at COM height), handle held stowed, from a fixed
#  side camera, and assembles a looping (ping-pong) GIF.  The static scene is
#  built once; only the drawbar actor is swapped per frame.
# ============================================================================
import os
import tempfile

import cadquery as cq
from PIL import Image

import build_core as bc
import render_vtk as rv

HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(os.path.dirname(HERE), "renders")
FRAMES = os.path.join(RENDERS, "_deploy_frames")
os.makedirs(FRAMES, exist_ok=True)

N = 24                      # forward frames
SIZE = (960, 720)


def main():
    log = []
    # static scene = stowed handle/hub group + bracket + lower axle + fastener
    static = bc.moving_parts(0.0, log)
    static["bracket"] = bc.make_bracket(log)
    static["loweraxle"] = bc.make_lower_axle()
    static["fastener"] = bc.make_fasteners(log)

    ren, win, _ = rv.build_scene(static, SIZE)
    cam = ren.GetActiveCamera()

    td_dir = tempfile.mkdtemp()
    # fix the camera framing on the fully-deployed extent so nothing jumps
    probe, _ = rv.part_actor(bc.make_drawbar(bc.DRAW_DEPLOY), "drawbar",
                             bc.COL["drawbar"], td_dir)
    ren.AddActor(probe)
    ren.ResetCamera()
    fp = cam.GetFocalPoint()
    cam.SetPosition(fp[0] + 360, fp[1], fp[2])
    cam.SetViewUp(0, 0, 1)
    cam.Zoom(1.15)
    ren.ResetCameraClippingRange()
    ren.RemoveActor(probe)

    frame_paths = []
    drawbar_actor = None
    for i in range(N + 1):
        td = bc.DRAW_DEPLOY * i / N
        if drawbar_actor is not None:
            ren.RemoveActor(drawbar_actor)
        drawbar_actor, _ = rv.part_actor(bc.make_drawbar(td), "drawbar",
                                         bc.COL["drawbar"], td_dir)
        ren.AddActor(drawbar_actor)
        win.Render()
        from vtkmodules.vtkRenderingCore import vtkWindowToImageFilter
        from vtkmodules.vtkIOImage import vtkPNGWriter
        w2i = vtkWindowToImageFilter(); w2i.SetInput(win); w2i.Update()
        fp_png = os.path.join(FRAMES, f"f{i:03d}.png")
        wr = vtkPNGWriter(); wr.SetFileName(fp_png)
        wr.SetInputConnection(w2i.GetOutputPort()); wr.Write()
        frame_paths.append(fp_png)
    print("rendered", len(frame_paths), "frames")

    # ping-pong: deploy, hold, retract, hold
    imgs = [Image.open(p).convert("P", palette=Image.ADAPTIVE) for p in frame_paths]
    seq = imgs + [imgs[-1]] * 6 + imgs[::-1] + [imgs[0]] * 6
    out = os.path.join(RENDERS, "drawbar_deploy.gif")
    seq[0].save(out, save_all=True, append_images=seq[1:], duration=70, loop=0,
                optimize=True, disposal=2)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
