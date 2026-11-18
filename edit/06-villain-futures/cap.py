from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=720,1280
L=["POV: you're a villain","who trades futures on the side"]
f=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf',40)
img=Image.new('RGBA',(W,H),(0,0,0,0)); sh=Image.new('RGBA',(W,H),(0,0,0,0))
d=ImageDraw.Draw(img); s=ImageDraw.Draw(sh); y=200
for ln in L:
    x=(W-d.textlength(ln,font=f))/2
    s.text((x,y+2),ln,font=f,fill=(0,0,0,220),stroke_width=4,stroke_fill=(0,0,0,170)); d.text((x,y),ln,font=f,fill=(255,255,255,255)); y+=52
Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3.5)),img).save('cap.png')
