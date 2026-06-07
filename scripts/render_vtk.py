#!/usr/bin/env python3
# ============================================================================
#  Gravitcase — headless presentation renderer
#
#  Windows-native offscreen VTK (no xvfb).  Each part is tessellated to its own
#  STL and given a material (metal / bronze / anodised) under a 4-light kit with
#  MSAA + FXAA, gradient backdrop, and a ground shadow.  Produces hero, front,
#  side, a zoomed pocket close-up, and a cutaway (near wall removed) that shows
#  the pawl + lug engaging in the pocket.
# ============================================================================
import os
import tempfile

import cadquery as cq
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingCore import (
    vtkRenderer, vtkRenderWindow, vtkActor, vtkPolyDataMapper,
    vtkWindowToImageFilter, vtkLight,
)
from vtkmodules.vtkRenderingCore import vtkLightKit
from vtkmodules.vtkIOImage import vtkPNGWriter
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401  registers GL backend

import build_core as bc

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RENDERS = os.path.join(ROOT, "renders")
os.makedirs(RENDERS, exist_ok=True)

# material finish per part: (specular, specular_power, metallic_tint, opacity)
#   metallic_tint True -> white highlights (metal); False -> coloured (anodised)
MAT = {
    "shaft":    (0.55, 45, True,  1.0),
    "hub":      (0.45, 35, True,  1.0),
    "ears":     (0.45, 35, True,  1.0),
    "pin":      (0.60, 60, True,  1.0),
    "bracket":  (0.30, 20, True,  1.0),
    "lug":      (0.65, 55, True,  1.0),   # hardened steel
    "friction": (0.40, 25, True,  1.0),   # bronze clutch
    "pawl":     (0.35, 30, False, 1.0),   # red anodised
    "spine":    (0.30, 25, False, 1.0),   # dark anodised
    "drawbar":  (0.35, 30, False, 1.0),   # green anodised
    "fastener": (0.55, 50, True,  1.0),
    "carrier":  (0.20, 18, False, 1.0),   # GF nylon
    "telerod":  (0.55, 50, True,  1.0),   # SS
    "pivrod":   (0.55, 50, True,  1.0),   # SS (segmented)
    "concentrator": (0.25, 20, False, 1.0),  # POM
    "shell":    (0.10, 12, False, 0.22),  # translucent molded shell
    "brace":    (0.45, 35, True,  1.0),   # steel brace
    "case":     (0.15, 16, False, 0.45),  # full case body (translucent)
    "wheel":    (0.30, 25, False, 1.0),   # spinner wheels
}


def part_actor(wp, name, color, tmpdir):
    stl = os.path.join(tmpdir, name + ".stl")
    cq.exporters.export(wp, stl, tolerance=0.04, angularTolerance=0.1)
    rdr = vtkSTLReader(); rdr.SetFileName(stl); rdr.Update()
    m = vtkPolyDataMapper(); m.SetInputConnection(rdr.GetOutputPort())
    a = vtkActor(); a.SetMapper(m)
    p = a.GetProperty()
    r, g, b, op = color.toTuple()
    spec, sp, metal, _o = MAT.get(name, (0.4, 30, True, 1.0))
    p.SetInterpolationToPhong()
    p.SetColor(r, g, b)
    p.SetOpacity(op)
    p.SetAmbient(0.18); p.SetDiffuse(0.72)
    p.SetSpecular(spec); p.SetSpecularPower(sp)
    if metal:
        p.SetSpecularColor(1.0, 1.0, 1.0)
    else:
        p.SetSpecularColor(min(1, r + 0.3), min(1, g + 0.3), min(1, b + 0.3))
    return a, m


def build_scene(parts, size):
    ren = vtkRenderer()
    ren.GradientBackgroundOn()
    ren.SetBackground(0.06, 0.07, 0.09)      # bottom
    ren.SetBackground2(0.20, 0.23, 0.28)     # top
    ren.UseFXAAOn()
    win = vtkRenderWindow(); win.SetOffScreenRendering(1)
    win.SetMultiSamples(8)
    win.AddRenderer(ren); win.SetSize(*size)

    kit = vtkLightKit()
    kit.SetKeyLightIntensity(1.15)
    kit.SetKeyToFillRatio(2.5)
    kit.SetKeyToHeadRatio(3.0)
    kit.SetKeyToBackRatio(3.5)
    kit.AddLightsToRenderer(ren)

    td = tempfile.mkdtemp()
    mappers = []
    for name, wp in parts.items():
        col = bc.COL.get(name, cq.Color(0.7, 0.7, 0.7, 1.0))
        a, m = part_actor(wp, name, col, td)
        ren.AddActor(a)
        mappers.append(m)
    return ren, win, mappers


def shoot(ren, win, fname):
    win.Render()
    w2i = vtkWindowToImageFilter(); w2i.SetInput(win)
    w2i.SetScale(1); w2i.Update()
    out = os.path.join(RENDERS, fname)
    wr = vtkPNGWriter(); wr.SetFileName(out)
    wr.SetInputConnection(w2i.GetOutputPort()); wr.Write()
    print("wrote", out, os.path.getsize(out), "bytes")


def set_clip(mappers, clip):
    for m in mappers:
        m.RemoveAllClippingPlanes()
        if clip is not None:
            origin, normal = clip
            pl = vtkPlane(); pl.SetOrigin(*origin); pl.SetNormal(*normal)
            m.AddClippingPlane(pl)


def render(parts, views, size=(1600, 1200)):
    ren, win, mappers = build_scene(parts, size)
    cam = ren.GetActiveCamera()
    for v in views:
        set_clip(mappers, v.get("clip"))
        if "focal" in v:                       # explicit framed close-up
            fx, fy, fz = v["focal"]
            dx, dy, dz = v["dir"]
            d = v.get("dist", 200)
            cam.SetFocalPoint(fx, fy, fz)
            cam.SetPosition(fx + dx * d, fy + dy * d, fz + dz * d)
            cam.SetViewUp(*v["up"])
            cam.SetViewAngle(v.get("angle", 30))
            ren.ResetCameraClippingRange()
        else:                                  # frame whole model, then offset
            ren.ResetCamera()
            fp = cam.GetFocalPoint()
            dx, dy, dz = v["dir"]
            cam.SetPosition(fp[0] + dx, fp[1] + dy, fp[2] + dz)
            cam.SetViewUp(*v["up"])
            ren.ResetCameraClippingRange()
        shoot(ren, win, v["name"])


if __name__ == "__main__":
    # State A — handle DEPLOYED (45 deg), drawbar STOWED: case being hand-towed.
    _, parts, _, _, _ = bc.build(bc.DEPLOY_ANGLE, 0.0)
    POCKET = (-2, 1, -15)                       # centre of the lug/pawl pocket
    views = [
        {"name": "core_hero.png",  "dir": (-230, -200, 150), "up": (0, 0, 1)},
        {"name": "core_front.png", "dir": (0, -320, 0),      "up": (0, 0, 1)},
        {"name": "core_side.png",  "dir": (320, 0, 0),       "up": (0, 0, 1)},
        # zoomed close-up of the pocket (lug seated on wall, pawl on abutment)
        {"name": "pocket_closeup.png", "focal": POCKET, "dir": (-0.55, -0.7, 0.45),
         "up": (0, 0, 1), "dist": 95, "angle": 28},
        # tight close-up on the red pawl seated on its +Y abutment (fold-back stop)
        {"name": "pawl_closeup.png", "focal": (-5, 5, -13), "dir": (-0.45, -0.75, 0.25),
         "up": (0, 0, 1), "dist": 70, "angle": 26},
        # iso kept for parity with the original handoff renders
        {"name": "core_iso.png",   "dir": (-200, -200, 160), "up": (0, 0, 1)},
    ]
    render(parts, views)

    # State B — drawbar DEPLOYED on its lower axle, handle STOWED (+Z recess):
    # case towing the next one.  The two never deploy together (per design).
    _, partsB, _, _, _ = bc.build(0.0, bc.DRAW_DEPLOY)
    viewsB = [
        {"name": "drawbar_deployed_hero.png", "dir": (-260, -200, 150), "up": (0, 0, 1)},
        {"name": "drawbar_deployed_side.png", "dir": (320, 0, 0),       "up": (0, 0, 1)},
    ]
    render(partsB, viewsB)

    # State C — handle EXTENDED (5-tube spine fully telescoped), shown VERTICAL
    # (theta=0) so the whole ~1070 mm cascade reads cleanly, like the spec.
    _, partsC, _, _, _ = bc.build(0.0, 0.0, spine_extend=1.0)
    viewsC = [
        {"name": "handle_extended_side.png", "dir": (340, 0, 0), "up": (0, 0, 1)},
    ]
    render(partsC, viewsC, size=(640, 1600))
    # (Actuation rods/carrier/concentrator are inside the spine bore — best viewed
    #  in the STEP or via the spec's own section diagrams; verified by Check #4.)

    # State E — STOWED mechanism seated in the molded back shell (translucent) +
    # brace.  Side view down −X shows the recess/pivot pocket/drawbar channel and
    # the spine overrunning the case top (Check #8 finding).
    _, partsE, _, _, _ = bc.build(0.0, 0.0, spine_extend=0.0)
    partsE["shell"] = bc.make_shell()
    partsE["brace"] = bc.make_brace()
    render(partsE, [{"name": "shell_fit_side.png", "dir": (340, 0, 0), "up": (0, 0, 1)}],
           size=(820, 1500))
    # pivot close-up from the FRONT (−Y), brace dropped, so the axle is seen running
    # horizontally (X) through the case bosses AND the metal bracket walls.
    partsP = {k: v for k, v in partsE.items() if k != "brace"}
    render(partsP, [{"name": "shell_pivot.png", "focal": (0, 0, -3),
                     "dir": (0.35, -1, 0.22), "up": (0, 0, 1), "dist": 130, "angle": 30}],
           size=(1150, 900))

    # State F — COMPLETE SUITCASE: mechanism + molded case (translucent) + 2" wheels
    def suitcase(theta, td, ext):
        _, p, _, _, _ = bc.build(theta, td, ext)
        p["case"] = bc.make_case()
        p["wheel"] = bc.make_wheels()
        return p
    render(suitcase(0.0, 0.0, 0.0),
           [{"name": "suitcase_iso.png", "dir": (-320, -270, 190), "up": (0, 0, 1)}],
           size=(950, 1250))
    render(suitcase(bc.DEPLOY_ANGLE, 0.0, 0.0),   # handle swung to 45 (collapsed length)
           [{"name": "suitcase_deployed.png", "dir": (-320, -240, 170), "up": (0, 0, 1)}],
           size=(1000, 1250))
