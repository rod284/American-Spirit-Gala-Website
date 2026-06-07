import cadquery as cq
from cadquery import Solid, Vector, Workplane
import math, json

def box_mm(x0,x1,y0,y1,z0,z1):
    return Solid.makeBox(x1-x0, y1-y0, z1-z0, Vector(x0,y0,z0))

def cyl_x(r,x0,x1,y=0,z=0):
    return Solid.makeCylinder(r, x1-x0, Vector(x0,y,z), Vector(1,0,0))

def cyl_z(r,z0,z1,x=0,y=0):
    return Solid.makeCylinder(r, z1-z0, Vector(x,y,z0), Vector(0,0,1))

def oct_prism(hw, hd, ch, z0, z1):
    pts=[(hw,hd-ch),(hw-ch,hd),(-hw+ch,hd),(-hw,hd-ch),
         (-hw,-hd+ch),(-hw+ch,-hd),(hw-ch,-hd),(hw,-hd+ch)]
    return Workplane("XY").polyline(pts).close().extrude(z1-z0).translate((0,0,z0))

# ---- STEEL group ----
steel = []
steel.append(cyl_x(7,-35,35))                                   # shaft
steel.append(box_mm(-28,-25,-22,22,-32,22))                     # left wall
steel.append(box_mm( 25, 28,-22,22,-32,22))                     # right wall
steel.append(box_mm(-28, 28,-22,22,-32,-28))                    # floor
# mount tabs
steel.append(box_mm(-34,-28,-8,8,-6,6))
steel.append(box_mm( 28, 34,-8,8,-6,6))
# brace (tapered plate at back), extruded in Y
brace = Workplane("XZ").polyline([(-15,22),(15,22),(8,92),(-8,92)]).close().extrude(6)
brace = brace.translate((0,-22,0))
steel.append(brace.val())
# hub
hub = cyl_x(11,-9,9).cut(cyl_x(7,-9,9))
steel.append(hub)
# boss tube
boss = oct_prism(25,18.5,5,11,56).cut(oct_prism(21,14.5,4,11,56).val())
steel.append(boss.val())
# collars
steel.append(cyl_x(10,-23,-16).cut(cyl_x(7,-23,-16)))
steel.append(cyl_x(10, 16, 23).cut(cyl_x(7, 16, 23)))
# drawbar arm + ball (stowed, down)
steel.append(box_mm(-3,3,-3,3,-55,-18))
steel.append(Solid.makeSphere(8).translate((0,0,-60)))
# pawl + pin
steel.append(box_mm(-5,5,3,9,-15,-6))
steel.append(cyl_x(3,-7,7,y=6,z=-10))

# ---- ANODIZED spine ----
anod = [oct_prism(22.5,16,4,48,84).val()]

# ---- HARDENED faces ----
hard = []
hard.append(box_mm(-5,5,-3,3,-22,-11))      # lug
hard.append(box_mm(-6,6,-8,-4,-28,-16))     # fixed wall
hard.append(box_mm(-6,6, 4, 8,-28,-16))     # abutment

# ---- BRONZE friction discs ----
bronze=[]
for xx in (9,11,13,15):
    bronze.append(cyl_x(12, xx, xx+1.5))

def comp(lst):
    c=lst[0]
    for s in lst[1:]:
        c=c.fuse(s) if hasattr(c,'fuse') else c
    return cq.Compound.makeCompound([ (s if isinstance(s,Solid) else s) for s in lst])

groups = {"steel":steel, "anod":anod, "hard":hard, "bronze":bronze}
colors = {"steel":(0.66,0.69,0.73), "anod":(0.20,0.26,0.32),
          "hard":(0.80,0.62,0.25), "bronze":(0.78,0.58,0.32)}

asm = cq.Assembly()
for name, solids in groups.items():
    comp_solids=[]
    for s in solids:
        comp_solids.append(s.val() if hasattr(s,'val') else s)
    cmp = cq.Compound.makeCompound(comp_solids)
    asm.add(cmp, name=name, color=cq.Color(*colors[name]))

asm.save("/home/claude/gravitcase_core.step")
print("STEP saved")

# tessellate each group for rendering
out={}
for name, solids in groups.items():
    comp_solids=[s.val() if hasattr(s,'val') else s for s in solids]
    cmp = cq.Compound.makeCompound(comp_solids)
    verts, tris = cmp.tessellate(0.3)
    out[name]={"v":[[p.x,p.y,p.z] for p in verts], "f":tris, "c":colors[name]}
json.dump(out, open("/home/claude/mesh.json","w"))
print("mesh saved", {k:len(v["f"]) for k,v in out.items()})
