from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=720,1280
F='/usr/share/fonts/opentype/inter/Inter-Bold.otf'
lines=[('"bro are you free to trade after work?"',30,168),('bro i\'m free to trade during work',33,228)]
img=Image.new('RGBA',(W,H),(0,0,0,0)); sh=Image.new('RGBA',(W,H),(0,0,0,0))
d=ImageDraw.Draw(img); s=ImageDraw.Draw(sh)
for t,size,y in lines:
    f=ImageFont.truetype(F,size)
    while d.textlength(t,font=f)>W-60: size-=1; f=ImageFont.truetype(F,size)
    x=(W-d.textlength(t,font=f))/2
    s.text((x,y+2),t,font=f,fill=(0,0,0,230),stroke_width=2,stroke_fill=(0,0,0,200))
    d.text((x,y),t,font=f,fill=(255,255,255,255))
Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(2.5)),img).save('cap.png')
