"""Overlay layer for Cyan 01 AI roadmap. Renders RGBA frames to stdout (720x1280 @24fps)."""
import re, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 720, 1280, 24
SPEED = 1.1
DUR = 52.0

GF = '/usr/share/fonts/truetype/google-fonts/'
F_BOLD = GF + 'Poppins-Bold.ttf'
F_MED = GF + 'Poppins-Medium.ttf'
F_REG = GF + 'Poppins-Regular.ttf'
F_SERIF = '/home/claude/edit/fonts/InstrumentSerif-Italic.ttf'

WHITE = (255, 255, 255)
ACCENT = (120, 246, 238)      # soft Halcyon teal for serif accents
MUTED = (154, 164, 171)
_font_cache = {}
def font(path, size):
    k = (path, size)
    if k not in _font_cache:
        _font_cache[k] = ImageFont.truetype(path, size)
    return _font_cache[k]

# ---------------------------------------------------------------- timing
# clip trims (pre-speed) and spoken phrases mapped to detected speech segments
CLIPS = [
    dict(trim=0.20, length=13.75, segs=[
        ((0.32, 3.16), "Most traders still use AI like a search bar."),
        ((3.94, 5.74), "You can get good at it in 30 days."),
        ((6.50, 7.20), "I'm Cyan,"),
        ((7.58, 9.38), "I run my trading desk with AI."),
        ((10.02, 11.64), "Here's how I'd learn it from zero."),
        ((12.24, 12.68), "Save this,"),
        ((13.06, 13.84), "it's all free."),
    ]),
    dict(trim=0.22, length=13.71, segs=[
        ((0.34, 0.62), "First,"),
        ((1.06, 1.50), "prompting."),
        ((2.26, 4.04), "Do Anthropic's free tutorials,"),
        ((4.38, 6.40), "then their free AI Fluency course."),
        ((7.18, 9.40), "It teaches you what to hand over to AI,"),
        ((9.64, 11.02), "and how to check what comes back."),
        ((11.82, 13.78), "Like reviewing a junior analyst's work."),
    ]),
    dict(trim=0.00, length=14.89, segs=[
        ((0.12, 0.58), "Then,"),
        ((0.82, 1.90), "learn Claude Code."),
        ((2.54, 3.92), "Everyone talks about Cowork,"),
        ((4.34, 5.74), "but for building your own tools,"),
        ((6.08, 7.48), "Claude Code goes further."),
        ((7.84, 8.18), "Next,"),
        ((8.60, 10.68), "connect MCPs and build skills."),
        ((11.26, 12.78), "Show AI a task once,"),
        ((13.10, 14.74), "and it runs that workflow for you."),
    ]),
    dict(trim=0.08, length=14.77, segs=[
        ((0.20, 1.44), "And finally, agents."),
        ((2.30, 6.64), "Andrew Ng's free course on Agentic AI is the best place to start."),
        ((7.40, 8.44), "Give it thirty days,"),
        ((8.80, 10.98), "and you'll wonder how you ever traded without it."),
        ((11.80, 12.82), "Comment ROADMAP,"),
        ((13.22, 14.70), "and I'll send you the whole list."),
    ]),
]
offsets, acc = [], 0.0
for c in CLIPS:
    offsets.append(acc); acc += c['length']

def g(ci, t):
    """clip-local original time -> global output time"""
    return (offsets[ci] + t - CLIPS[ci]['trim']) / SPEED

SYL_OVERRIDE = {'30': 2, 'ai': 2, 'mcps': 4, 'roadmap': 2, "i'm": 1, "i'd": 1, "it's": 1, 'ng': 1,
                "anthropic's": 4, "analyst's": 3, "you'll": 1, "i'll": 1, 'cowork': 2, 'claude': 1}
def syl(w):
    k = re.sub(r'[^a-z0-9\']', '', w.lower())
    if k in SYL_OVERRIDE: return SYL_OVERRIDE[k]
    n = len(re.findall(r'[aeiouy]+', k))
    if k.endswith('e') and n > 1 and not k.endswith('le'): n -= 1
    return max(1, n)

WORDS = []  # (global_start, global_end, display_word, raw_word, clip, seg_index)
for ci, c in enumerate(CLIPS):
    for si, ((s, e), text) in enumerate(c['segs']):
        ws = text.split()
        wts = [syl(w) + 0.35 for w in ws]
        tot = sum(wts); t = s
        for w, wt in zip(ws, wts):
            d = (e - s) * wt / tot
            disp = re.sub(r'[.,]', '', w)
            WORDS.append([g(ci, t), g(ci, t + d), disp, w, ci, si])
            t += d

def word_time(ci, word, nth=0):
    hits = [x for x in WORDS if x[4] == ci and re.sub(r'[^a-z0-9]', '', x[3].lower()) == word]
    return hits[nth][0]

# caption chunks: up to 3 words, break after punctuation
CHUNKS = []
cur = []
for i, wd in enumerate(WORDS):
    cur.append(wd)
    nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
    brk = (len(cur) >= 3 or wd[3][-1] in '.,' or nxt is None or nxt[5] != wd[5] or nxt[4] != wd[4]
           or (len(cur) == 2 and nxt and len(nxt[2]) > 8))
    if brk:
        CHUNKS.append(cur); cur = []
for i, ch in enumerate(CHUNKS):
    end = CHUNKS[i + 1][0][0] if i + 1 < len(CHUNKS) else DUR
    end = min(end, ch[-1][1] + 0.6)
    ch_start = ch[0][0]
    CHUNKS[i] = (ch_start, end, ch)

# ---------------------------------------------------------------- drawing helpers
def shadowed(img_rgba, radius=5, alpha=150, offset=(0, 2)):
    a = img_rgba.split()[3]
    sh = Image.new('RGBA', img_rgba.size, (0, 0, 0, 0))
    sh.putalpha(a.point(lambda v: v * alpha // 255))
    sh = sh.filter(ImageFilter.GaussianBlur(radius))
    pad = radius * 4 + max(abs(offset[0]), abs(offset[1])) + 2
    out = Image.new('RGBA', (img_rgba.width + pad * 2, img_rgba.height + pad * 2), (0, 0, 0, 0))
    out.alpha_composite(sh, (pad + offset[0], pad + offset[1]))
    out.alpha_composite(img_rgba, (pad, pad))
    return out

def rich_line(parts):
    """parts: list of (text, style). styles: sans, serif, sansL, serifL, cap"""
    spec = {
        'sans': (F_BOLD, 46, WHITE), 'serif': (F_SERIF, 60, ACCENT),
        'sansL': (F_BOLD, 54, WHITE), 'serifL': (F_SERIF, 70, ACCENT),
        'head': (F_BOLD, 44, WHITE), 'headS': (F_SERIF, 56, ACCENT),
        'cap': (F_BOLD, 34, WHITE),
    }
    items = []
    for text, st in parts:
        p, s, col = spec[st]
        f = font(p, s)
        bb = f.getbbox(text)
        items.append((text, f, col, bb))
    asc = max(f.getmetrics()[0] for _, f, _, _ in items)
    desc = max(f.getmetrics()[1] for _, f, _, _ in items)
    width = sum(f.getlength(t) for t, f, _, _ in items)
    img = Image.new('RGBA', (int(width) + 8, asc + desc + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 4
    for t, f, col, _ in items:
        a = f.getmetrics()[0]
        d.text((x, 4 + asc - a), t, font=f, fill=col + (255,))
        x += f.getlength(t)
    return img

_cache = {}
def cached(key, fn):
    if key not in _cache: _cache[key] = fn()
    return _cache[key]

def place(frame, img, cx, cy, alpha=1.0, scale=1.0):
    if alpha <= 0: return
    if scale != 1.0:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.LANCZOS)
    if alpha < 1.0:
        img = img.copy(); a = img.split()[3].point(lambda v: int(v * alpha)); img.putalpha(a)
    frame.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))

def ease_out(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def pop(t, t0, t1, fin=0.16, fout=0.12):
    """alpha, scale for an element visible t0..t1"""
    if t < t0 or t > t1: return 0, 1
    a_in = ease_out((t - t0) / fin)
    a_out = max(0, min(1, (t1 - t) / fout))
    a = min(a_in, a_out)
    sc = 0.86 + 0.14 * ease_out((t - t0) / (fin * 1.4))
    if (t - t0) < fin * 1.4:
        over = math.sin(min(1, (t - t0) / (fin * 1.4)) * math.pi) * 0.04
        sc += over
    return a, sc

# ---------------------------------------------------------------- elements
def caption_img(words, n_shown):
    txt = ' '.join(w[2] for w in words[:n_shown])
    full = ' '.join(w[2] for w in words)
    def mk():
        f = font(F_BOLD, 34)
        wfull = f.getlength(full)
        img = Image.new('RGBA', (int(wfull) + 10, 56), (0, 0, 0, 0))
        ImageDraw.Draw(img).text(((img.width - f.getlength(txt)) / 2, 4), txt, font=f, fill=WHITE + (255,))
        return shadowed(img, radius=4, alpha=190)
    return cached(('cap', full, n_shown), mk)

def typed(parts, frac, cursor=True, t=0.0):
    total = sum(len(p[0]) for p in parts)
    n = int(round(total * frac))
    out = []
    for text, st in parts:
        if n <= 0: break
        out.append((text[:n], st)); n -= len(text)
    show_cursor = cursor and (frac < 1 or int(t * 2.2) % 2 == 0)
    key = ('typed', tuple(out), show_cursor)
    def mk():
        if not out:
            base = Image.new('RGBA', (4, 60), (0, 0, 0, 0))
        else:
            base = rich_line(out)
        if show_cursor:
            img = Image.new('RGBA', (base.width + 14, max(base.height, 60)), (0, 0, 0, 0))
            img.alpha_composite(base, (0, 0))
            ImageDraw.Draw(img).rectangle([base.width + 4, 10, base.width + 7, img.height - 12], fill=WHITE + (235,))
            base = img
        return shadowed(base, radius=5, alpha=170)
    return cached(key, mk)

def title_img(num, word):
    return cached(('title', num, word), lambda: shadowed(rich_line([(f'{num}. ', 'serifL'), (word, 'sansL')]), 6, 170))

def pop_img(lines):
    def mk():
        rows = [rich_line(l) for l in lines]
        w = max(r.width for r in rows); hgt = sum(r.height for r in rows) - 10 * (len(rows) - 1)
        img = Image.new('RGBA', (w, hgt), (0, 0, 0, 0)); y = 0
        for r in rows:
            img.alpha_composite(r, ((w - r.width) // 2, y)); y += r.height - 10
        return shadowed(img, 6, 170)
    return cached(('pop', str(lines)), mk)

def rounded(size, r, fill, outline=None, width=1):
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=fill, outline=outline, width=width)
    return img

def card_img(tag, title, sub, glyph):
    def mk():
        cw, ch = 640, 176
        card = rounded((cw, ch), 22, (13, 17, 21, 235), outline=(120, 246, 238, 90), width=2)
        d = ImageDraw.Draw(card)
        d.text((28, 22), tag.upper(), font=font(F_MED, 15), fill=ACCENT + (255,))
        # title (wrap to 2 lines if needed)
        ft = font(F_BOLD, 28); maxw = cw - 28 - 150
        words, lines, cur = title.split(), [], ''
        for w in words:
            tst = (cur + ' ' + w).strip()
            if ft.getlength(tst) <= maxw: cur = tst
            else: lines.append(cur); cur = w
        lines.append(cur)
        y = 50
        for ln in lines[:2]:
            d.text((28, y), ln, font=ft, fill=WHITE + (255,)); y += 36
        d.text((28, y + 6), sub, font=font(F_REG, 17), fill=MUTED + (255,))
        # free pill
        pf = font(F_MED, 14); pw = int(pf.getlength('FREE')) + 22
        pill = rounded((pw, 26), 13, (120, 246, 238, 40), outline=(120, 246, 238, 160))
        ImageDraw.Draw(pill).text((11, 3), 'FREE', font=pf, fill=ACCENT + (255,))
        card.alpha_composite(pill, (cw - pw - 26, 22))
        # round icon
        cx, cy, rr = cw - 74, 108, 38
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(120, 246, 238, 28), outline=(120, 246, 238, 200), width=2)
        col = ACCENT + (255,)
        if glyph == 'spark':
            r1, r2 = 20, 5
            pts = []
            for k in range(8):
                ang = math.pi / 4 * k - math.pi / 2
                r = r1 if k % 2 == 0 else r2
                pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
            d.polygon(pts, fill=col)
        elif glyph == 'nodes':
            P = [(cx - 16, cy + 12), (cx, cy - 16), (cx + 16, cy + 12)]
            d.line([P[0], P[1], P[2], P[0]], fill=col, width=3)
            for x, y in P: d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=col)
        else:
            gf = font(F_BOLD, 26)
            bb = gf.getbbox(glyph)
            d.text((cx - (bb[2] + bb[0]) / 2, cy - (bb[3] + bb[1]) / 2), glyph, font=gf, fill=col)
        return shadowed(card, 10, 150, (0, 6))
    return cached(('card', title), mk)

def save_img(clicked):
    def mk():
        bw, bh = 150, 52
        b = rounded((bw, bh), 26, (255, 255, 255, 250))
        d = ImageDraw.Draw(b)
        # bookmark icon
        x0, y0 = 28, 15
        pts = [(x0, y0), (x0 + 16, y0), (x0 + 16, y0 + 23), (x0 + 8, y0 + 16), (x0, y0 + 23)]
        if clicked: d.polygon(pts, fill=(10, 12, 14))
        else: d.line(pts + [pts[0]], fill=(10, 12, 14), width=3, joint='curve')
        d.text((58, 10), 'Save', font=font(F_BOLD, 22), fill=(10, 12, 14))
        return shadowed(b, 8, 140, (0, 4))
    return cached(('save', clicked), mk)

def cursor_img():
    def mk():
        c = Image.new('RGBA', (30, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
        pts = [(2, 2), (2, 32), (10, 25), (16, 38), (21, 36), (15, 23), (26, 23)]
        d.polygon(pts, fill=(255, 255, 255), outline=(0, 0, 0)); return c
    return cached('cursor', mk)

# ---------------------------------------------------------------- timeline
TOP_Y = 150
ev = []  # (t0, t1, kind, payload)
# headline
ev.append((0.0, g(0, 6.40), 'headline', None))
# save button
t_save = g(0, 12.24)
ev.append((t_save, g(0, 13.84) + 0.25, 'save', t_save))
# clip 2
ev.append((g(1, 0.30), g(1, 2.20), 'title', ('1', 'prompting')))
ev.append((g(1, 2.26), g(1, 4.38), 'card', ('Anthropic · GitHub', 'Prompt Engineering Interactive Tutorial', '9 chapters with hands-on exercises', '{ }')))
t_flu = word_time(1, 'fluency')
ev.append((g(1, 4.38), t_flu - 0.02, 'title', ('2', 'AI fluency')))
ev.append((t_flu, g(1, 7.10), 'card', ('Anthropic Academy', 'AI Fluency: Framework & Foundations', 'What to delegate, and how to check it', 'spark')))
ev.append((g(1, 7.18), g(1, 11.30), 'pop', [[('what to ', 'sans'), ('hand over', 'serif')], [('how to ', 'sans'), ('check', 'serif')]]))
ev.append((g(1, 11.82), g(1, 13.78) + 0.15, 'pop', [[('like a ', 'sans'), ('junior analyst', 'serif')]]))
# clip 3
ev.append((g(2, 0.10), g(2, 2.50), 'title', ('3', 'Claude Code')))
ev.append((g(2, 2.54), g(2, 6.00), 'card', ('Anthropic Academy', 'Claude Code in Action', 'Build real tools from your terminal', '>_')))
ev.append((g(2, 6.08), g(2, 7.70), 'pop', [[('goes ', 'sans'), ('further', 'serif')]]))
t_mcp = word_time(2, 'mcps'); t_sk = word_time(2, 'skills')
ev.append((g(2, 7.84), t_sk - 0.02, 'title', ('4', 'MCPs')))
ev.append((t_sk, g(2, 11.20), 'title', ('5', 'skills')))
ev.append((g(2, 11.26), g(2, 12.95), 'pop', [[('show it ', 'sans'), ('once', 'serif')]]))
ev.append((g(2, 13.05), g(2, 14.89) + 0.1, 'card', ('Anthropic Academy', 'Introduction to Agent Skills', 'Teach Claude your workflow once', 'spark')))
# clip 4
ev.append((g(3, 0.15), g(3, 2.20), 'title', ('6', 'agents')))
ev.append((g(3, 2.30), g(3, 7.30), 'card', ('DeepLearning.AI · Andrew Ng', 'Agentic AI', 'Design and build AI agents that act', 'nodes')))
ev.append((g(3, 7.40), g(3, 11.50), 'pop', [[('give it ', 'sans'), ('30 days', 'serif')]]))
t_cta = g(3, 11.80)
ev.append((t_cta, DUR, 'cta', t_cta))

def render(t):
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for t0, t1, kind, p in ev:
        if not (t0 <= t <= t1): continue
        if kind == 'headline':
            l1 = [('6 ', 'head'), ('free', 'headS'), (' AI skills', 'head')]
            l2 = [('to learn before 2027', 'head')]
            n1 = sum(len(x[0]) for x in l1); n2 = len(l2[0][0])
            ft = t - t0
            f1 = min(1, ft / 0.9); f2 = max(0, min(1, (ft - 0.95) / 0.9))
            a_out = max(0, min(1, (t1 - t) / 0.15))
            place(fr, typed(l1, f1, cursor=f2 == 0, t=t), W / 2, 112, a_out)
            if f2 > 0: place(fr, typed(l2, f2, cursor=True, t=t), W / 2, 168, a_out)
        elif kind == 'title':
            a, sc = pop(t, t0, t1); place(fr, title_img(*p), W / 2, TOP_Y, a, sc)
        elif kind == 'pop':
            a, sc = pop(t, t0, t1); place(fr, pop_img(p), W / 2, TOP_Y + 10, a, sc)
        elif kind == 'card':
            a_in = ease_out((t - t0) / 0.22); a_out = max(0, min(1, (t1 - t) / 0.14))
            dy = (1 - a_in) * -28
            place(fr, card_img(*p), W / 2, 150 + dy, min(a_in, a_out))
        elif kind == 'save':
            ft = t - t0
            a, sc = pop(t, t0, t1, fin=0.18)
            clicked = ft > 0.55
            if 0.55 < ft < 0.68: sc *= 0.94
            bx, by = W / 2, 92
            place(fr, save_img(clicked), bx, by, a, sc)
            # cursor glides in from lower right and clicks
            k = ease_out(ft / 0.5)
            cx = bx + 150 - 110 * k; cy = by + 120 - 95 * k
            place(fr, cursor_img(), cx + 12, cy + 18, a)
        elif kind == 'cta':
            ft = t - t0
            fc = min(1, ft / 0.45); fr_ = max(0, min(1, (ft - 0.5) / 0.6))
            place(fr, typed([('comment', 'serifL')], fc, cursor=fr_ == 0, t=t), W / 2, 110)
            if fr_ > 0:
                img = typed([('ROADMAP', 'sansL')], fr_, cursor=True, t=t)
                place(fr, img, W / 2, 172)
    # captions
    for c0, c1, ch in CHUNKS:
        if c0 <= t < c1:
            n = sum(1 for w in ch if w[0] <= t + 0.02)
            n = max(1, n)
            place(fr, caption_img(ch, n), W / 2, 985)
            break
    return fr

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for ts in sys.argv[2:]:
            render(float(ts)).save(f'/home/claude/edit/still_{ts}.png')
        sys.exit()
    if len(sys.argv) > 1 and sys.argv[1] == 'dump':
        for x in ev: print(round(x[0], 2), round(x[1], 2), x[2], str(x[3])[:60])
        sys.exit()
    n = int(DUR * FPS)
    out = sys.stdout.buffer
    for i in range(n):
        out.write(render(i / FPS).tobytes())
