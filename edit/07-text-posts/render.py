from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json, sys

W, H = 716, 1284
FD = '/usr/share/fonts/truetype/google-fonts/'
ARROWF = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def font(w, s):
    return ImageFont.truetype(FD + f'Poppins-{w}.ttf', s)


def seg_width(d, txt, f, af):
    w = 0
    for ch in txt.split('→'):
        pass
    parts = txt.split('→')
    for i, p in enumerate(parts):
        w += d.textlength(p, font=f)
        if i < len(parts) - 1:
            w += f.size * 0.92
    return w


def draw_line(d, x, y, txt, f, af, fill):
    parts = txt.split('→')
    for i, p in enumerate(parts):
        d.text((x, y), p, font=f, fill=fill)
        x += d.textlength(p, font=f)
        if i < len(parts) - 1:
            bx = f.getbbox('x'); cy = y + (bx[1] + bx[3]) / 2
            L = f.size * 0.62; sw = max(2, int(f.size * 0.085)); hx = f.size * 0.2
            x0 = x + f.size * 0.08; x1 = x0 + L
            d.line([(x0, cy), (x1 - sw * 0.6, cy)], fill=fill, width=sw)
            d.line([(x1 - hx, cy - hx), (x1, cy), (x1 - hx, cy + hx)], fill=fill, width=sw, joint='curve')
            x += L + f.size * 0.3


def render(spec, out):
    size = spec.get('size', 32)
    lh = int(size * spec.get('lh', 1.5))
    f = font(spec.get('weight', 'Medium'), size)
    af = ImageFont.truetype(ARROWF, int(size * 0.9))
    align = spec.get('align', 'left')
    lines = spec['lines']
    y0 = spec.get('y', 220)
    scratch = ImageDraw.Draw(Image.new('L', (1, 1)))
    widths = [seg_width(scratch, l, f, af) for l in lines]
    block_w = max(widths)
    xl = (W - block_w) / 2 if align == 'left' else None

    txt = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dt, ds = ImageDraw.Draw(txt), ImageDraw.Draw(sh)
    y = y0
    for l, w in zip(lines, widths):
        if l.strip():
            x = xl if align == 'left' else (W - w) / 2
            draw_line(ds, x + 2, y + 3, l, f, af, (0, 0, 0, 230))
            draw_line(dt, x, y, l, f, af, (255, 255, 255, 255))
        y += lh if l.strip() else int(lh * 0.6)
    sh = sh.filter(ImageFilter.GaussianBlur(6))

    # soft dark wash behind the text block for legibility
    wash = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    top, bot = y0 - 120, y + 120
    for yy in range(max(0, top), min(H, bot)):
        t = min(yy - top, bot - yy) / 120
        a = int(110 * max(0, min(1, t)))
        wd.line([(0, yy), (W, yy)], fill=(0, 0, 0, a))

    out_img = Image.alpha_composite(Image.alpha_composite(wash, sh), txt)
    out_img.save(out)
    print(out, 'block', int(block_w), 'bottom', y)


if __name__ == '__main__':
    specs = json.load(open(sys.argv[1]))
    for name, spec in specs.items():
        render(spec, f'/home/claude/textposts/{name}.png')
