import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=1.5; W,H=720,1280
# riser centres measured on the 480x854 draft (bottom to top)
risers=[754,657,581,518,467,422]
heights=[56,42,46,40,34,28]
labels=["SLEEP","BREAKFAST","SOCIAL LIFE","FAMILY DINNER","GYM","TRADING"]
cx0,cx1=268,312
F='/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
img=Image.new('RGBA',(W,H),(0,0,0,0)); sh=Image.new('RGBA',(W,H),(0,0,0,0))
d=ImageDraw.Draw(img); s=ImageDraw.Draw(sh)
for i,(y,h,t) in enumerate(zip(risers,heights,labels)):
    size=int(round((26-1.4*i)*S))
    f=ImageFont.truetype(F,size)
    cx=(cx0+(cx1-cx0)*i/5)*S
    bb=d.textbbox((0,0),t,font=f); tw,th=bb[2]-bb[0],bb[3]-bb[1]
    x=cx-tw/2-bb[0]; yy=y*S-th/2-bb[1]
    s.text((x,yy+2),t,font=f,fill=(0,0,0,230))
    d.text((x,yy),t,font=f,fill=(255,255,255,255))
out=Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(2.5)),img)
out.save('labels.png')
