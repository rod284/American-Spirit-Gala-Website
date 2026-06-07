import json, numpy as np, vtk
data = json.load(open("/home/claude/mesh.json"))
ren = vtk.vtkRenderer(); ren.SetBackground(0.93,0.94,0.96)
for name,g in data.items():
    pts=vtk.vtkPoints()
    for v in g["v"]: pts.InsertNextPoint(*v)
    polys=vtk.vtkCellArray()
    for f in g["f"]:
        polys.InsertNextCell(3)
        for idx in f: polys.InsertCellPoint(idx)
    pd=vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(polys)
    nrm=vtk.vtkPolyDataNormals(); nrm.SetInputData(pd); nrm.SetFeatureAngle(50); nrm.Update()
    m=vtk.vtkPolyDataMapper(); m.SetInputConnection(nrm.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); c=g["c"]
    a.GetProperty().SetColor(*c); a.GetProperty().SetSpecular(0.35)
    a.GetProperty().SetSpecularPower(30); a.GetProperty().SetDiffuse(0.9); a.GetProperty().SetAmbient(0.28)
    ren.AddActor(a)
rw=vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.AddRenderer(ren); rw.SetSize(1200,1000)
for pos,inten in [((-0.5,-1,1.2),0.95),((1,-0.4,0.5),0.45),((0,0.6,0.4),0.3)]:
    L=vtk.vtkLight(); L.SetPosition(*pos); L.SetIntensity(inten); L.SetLightTypeToSceneLight(); ren.AddLight(L)
views={"iso":(0.75,-1.0,0.5),"side":(1.0,-0.06,0.16),"front":(0.05,-1.0,0.18)}
for vn,d in views.items():
    cam=vtk.vtkCamera(); ren.SetActiveCamera(cam)
    cam.SetViewUp(0,0,1); cam.SetFocalPoint(0,0,12)
    d=np.array(d,float); d/=np.linalg.norm(d)
    cam.SetPosition(*(np.array([0,0,12])+d*400))
    cam.ParallelProjectionOn()
    ren.ResetCamera(); cam.SetParallelScale(cam.GetParallelScale()*0.82)
    ren.ResetCameraClippingRange(); rw.Render()
    w2i=vtk.vtkWindowToImageFilter(); w2i.SetInput(rw); w2i.Update()
    wr=vtk.vtkPNGWriter(); wr.SetFileName(f"/home/claude/core_{vn}.png")
    wr.SetInputConnection(w2i.GetOutputPort()); wr.Write(); print("wrote",vn)
