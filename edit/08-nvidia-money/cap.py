# Caption overlay for cyan_nvidia_meme: centred white Poppins with soft shadow, glide-meme style
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
W, H = 720, 1280
F = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
text, size, y = 'NVIDIA traders be like', 46, 150
img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d, s = ImageDraw.Draw(img), ImageDraw.Draw(sh)
f = ImageFont.truetype(F, size)
while d.textlength(text, font=f) > W - 80:
    size -= 1; f = ImageFont.truetype(F, size)
x = (W - d.textlength(text, font=f)) / 2
s.text((x, y + 3), text, font=f, fill=(0, 0, 0, 235), stroke_width=6, stroke_fill=(0, 0, 0, 190))
d.text((x, y), text, font=f, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0, 120))
Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)), img).save(sys.argv[1] if len(sys.argv) > 1 else 'cap.png')
