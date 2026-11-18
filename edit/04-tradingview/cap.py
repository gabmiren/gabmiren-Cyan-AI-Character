from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=720,1280
L=["POV: you open TradingView","for the first time"]
f=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf',40)
img=Image.new('RGBA',(W,H),(0,0,0,0)); sh=Image.new('RGBA',(W,H),(0,0,0,0))
d=ImageDraw.Draw(img); s=ImageDraw.Draw(sh); y=596
for ln in L:
    x=(W-d.textlength(ln,font=f))/2
    s.text((x,y+2),ln,font=f,fill=(0,0,0,200)); d.text((x,y),ln,font=f,fill=(255,255,255,255)); y+=48
Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)),img).save('cap.png')
