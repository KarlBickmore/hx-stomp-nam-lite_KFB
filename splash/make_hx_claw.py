# Draws splash/hx-claw.png (320x240), the HX Claw boot picture: python3 splash/make_hx_claw.py (needs Pillow and the Inter font).
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
W,H=320,240; S=4
bg=Image.new('RGB',(W*S,H*S),(5,5,7)); d=ImageDraw.Draw(bg)
for y in range(H*S):
    t=y/(H*S); k=max(0,1-abs(t-0.3)/0.4); c=int(22*k)
    d.line([(0,y),(W*S,y)],fill=(5+c,5+c//3,7+c//4))
f=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf',60*S)
txt='HX CLAW'; bb=d.textbbox((0,0),txt,font=f); tw=bb[2]-bb[0]
x=(W*S-tw)//2-bb[0]; y=30*S-bb[1]
# text layer
tl=Image.new('L',bg.size,0); ImageDraw.Draw(tl).text((x,y),txt,font=f,fill=255)
# claw slash polygons (tapered), 3 parallel
def slash(cx):
    top=(cx+52, 12); bot=(cx-38, 108); w=9
    # taper: thin at ends, wide in middle
    import math
    pts_l=[];pts_r=[]
    for i in range(21):
        t=i/20; px=top[0]+(bot[0]-top[0])*t; py=top[1]+(bot[1]-top[1])*t
        ww=w*math.sin(math.pi*t)**0.7+0.4
        pts_l.append(((px-ww)*S,py*S)); pts_r.append(((px+ww)*S,py*S))
    return pts_l+pts_r[::-1]
cuts=Image.new('L',bg.size,0); cd=ImageDraw.Draw(cuts)
for cx in (128,172,216): cd.polygon(slash(cx),fill=255)
# glow from cuts
glow=cuts.filter(ImageFilter.GaussianBlur(7*S))
img=bg.copy()
img.paste((255,70,20),mask=glow.point(lambda v:int(v*0.9)))
# text shadow + text minus cuts
sh=tl.filter(ImageFilter.GaussianBlur(4*S)); img.paste((0,0,0),mask=sh.point(lambda v:int(v*0.8)))
from PIL import ImageChops
tmask=ImageChops.subtract(tl,cuts.filter(ImageFilter.MaxFilter(5)))
img.paste((246,246,246),mask=tmask)
# hot cut cores
core=cuts.filter(ImageFilter.GaussianBlur(1*S))
img.paste((255,110,40),mask=core.point(lambda v:int(v*0.55)))
img.paste((255,210,150),mask=cuts.filter(ImageFilter.MinFilter(9)).point(lambda v:int(v*0.6)))
d=ImageDraw.Draw(img)
f2=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf',12*S)
sub='N A M   ·   C U S T O M   F I R M W A R E'; bb=d.textbbox((0,0),sub,font=f2)
d.text(((W*S-(bb[2]-bb[0]))//2-bb[0],150*S),sub,font=f2,fill=(210,85,40))
out=img.resize((W,H),Image.LANCZOS); out.save('splash/hx-claw.png')

