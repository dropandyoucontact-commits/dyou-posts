"""Planche de contrôle du shaker 3D — /usr/bin/python3 test3d.py"""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "moteur"))
import skia
from moteur import *
from studio3d import Cam, scene3d
import vorix as V

W, H = 1080, 1920

def plan(nom, rot, ax, niveau=0.0, led=0.0, tz=760):
    s = skia.Surface(W, H); c = s.getCanvas()
    c.clear(hexa(V.FOND))
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(W*0.44, H*0.42), W*0.85,
                [hexa("#1C2733", 0.95), hexa(V.FOND, 0.0)]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    cam = Cam(ax=ax, ay=0, tz=tz, cx=W/2, cy=H/2)
    ombre_sol(c, W/2, H*0.5 + 560, 300, 54, 0.55)
    scene3d(c, cam, V.shaker(cam, cy=0, h=1060, rot=math.radians(rot), ax=0, niveau=niveau, led=led))
    s.makeImageSnapshot().save(f"renders/{nom}.png", skia.kPNG)
    print("->", nom)

pathlib.Path("renders").mkdir(exist_ok=True)
plan("t-face", 0, 0)
plan("t-34", -32, -6, niveau=0.5, led=1.0)
plan("t-dos", 150, -10)
