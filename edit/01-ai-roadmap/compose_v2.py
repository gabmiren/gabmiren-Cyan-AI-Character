"""v2: snap punch-ins + SFX, following the zoom recipe. Reads stitched.mp4 frames, zooms, adds overlay, writes raw RGB to stdout.
Also writes sfx.wav (48 kHz mono)."""
import sys, subprocess, math, wave
import numpy as np
from PIL import Image
sys.argv = [sys.argv[0]]  # keep overlay's __main__ out of the way
import overlay as ov

W, H, FPS = 720, 1280, 24

# --- edits to the overlay timeline: zooms carry these lines instead of text pops
drop = {"like a ", "goes ", "show it "}
ov.ev = [e for e in ov.ev if not (e[2] == 'pop' and e[3][0][0][0] in drop)]
# "give it 30 days" pop ends as the punch-in lands
ov.ev = [(e[0], ov.g(3, 8.75) if (e[2] == 'pop' and e[3][0][0][0] == 'give it ') else e[1], e[2], e[3]) for e in ov.ev]

g = ov.g
# --- punch-ins: (start, end, scale) on turning-point lines; snaps in and out, no push
ZOOMS = [
    (g(0, 6.50),  g(0, 8.30),  1.15),   # "I'm Cyan, I run my trading desk with AI"
    (g(0, 10.02), g(0, 12.20), 1.18),   # "Here's how I'd learn it from zero" -> snaps back as Save pops
    (g(1, 11.82), g(1, 13.70), 1.15),   # "Like reviewing a junior analyst's work"
    (g(2, 6.08),  g(2, 7.80),  1.18),   # "Claude Code goes further" -> snaps back as "4. MCPs" lands
    (g(2, 11.26), g(2, 13.00), 1.15),   # "Show AI a task once" -> snaps back as the skills card drops
    (g(3, 8.80),  g(3, 11.00), 1.18),   # "and you'll wonder how you ever traded without it"
    (g(3, 13.22), ov.DUR,      1.15),   # "and I'll send you the whole list" to the end
]
FACE = (360, 500)

def zoom_frame(img, s):
    cw, ch = W / s, H / s
    left = min(max(FACE[0] - cw / 2, 0), W - cw)
    top = min(max(FACE[1] - ch / 2, 0), H - ch)
    return img.resize((W, H), Image.LANCZOS, box=(left, top, left + cw, top + ch))

def scale_at(t):
    for a, b, s in ZOOMS:
        if a <= t < b: return s
    return 1.0

# --- SFX
SR = 48000
N = int(ov.DUR * SR)
sfx = np.zeros(N, np.float32)
rng = np.random.default_rng(7)
def add(sig, t, gain):
    i = int(t * SR)
    if i >= N: return
    j = min(N, i + len(sig)); sfx[i:j] += sig[:j - i] * gain
def accent():
    n = int(0.045 * SR); tt = np.arange(n) / SR
    tone = np.sin(2 * np.pi * 1900 * tt) * np.exp(-tt / 0.010)
    noise = np.diff(rng.standard_normal(n + 1)).astype(np.float32) * np.exp(-tt / 0.004)
    return (0.75 * tone + 0.35 * noise).astype(np.float32)
def soft():
    n = int(0.06 * SR); tt = np.arange(n) / SR
    env = (1 - np.exp(-tt / 0.002)) * np.exp(-tt / 0.018)
    return (np.sin(2 * np.pi * 1250 * tt) * env).astype(np.float32)
def tick():
    n = int(0.012 * SR); tt = np.arange(n) / SR
    return (np.diff(rng.standard_normal(n + 1)) * np.exp(-tt / 0.0025)).astype(np.float32)

ACC, SOFT, TICK = 0.30, 0.16, 0.07
# accent click ~0.3s after each punch-in (stressed word)
for a, b, s in ZOOMS: add(accent(), a + 0.3, ACC)
for t0, t1, kind, p in ov.ev:
    if kind in ('card', 'title', 'pop'): add(soft(), t0, SOFT)
    if kind == 'save':
        add(soft(), t0, SOFT); add(accent(), t0 + 0.55, ACC)
    if kind == 'headline':
        for k in range(16): add(tick(), t0 + 0.9 * k / 16 + rng.uniform(-0.01, 0.01), TICK)
        for k in range(20): add(tick(), t0 + 0.95 + 0.9 * k / 20 + rng.uniform(-0.01, 0.01), TICK)
    if kind == 'cta':
        for k in range(7): add(tick(), t0 + 0.45 * k / 7, TICK)
        for k in range(7): add(tick(), t0 + 0.5 + 0.6 * k / 7, TICK)
pcm = (np.clip(sfx, -1, 1) * 32767).astype(np.int16)
with wave.open('/home/claude/edit/sfx.wav', 'wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())

if __name__ == '__main__':
    mode = sys.stdin.isatty()
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', '/home/claude/edit/stitched.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                           stdout=subprocess.PIPE)
    out = sys.stdout.buffer
    n = int(ov.DUR * FPS)
    for i in range(n):
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        t = i / FPS
        img = Image.frombuffer('RGB', (W, H), buf, 'raw', 'RGB', 0, 1)
        s = scale_at(t)
        if s != 1.0: img = zoom_frame(img, s)
        fr = img.convert('RGBA'); fr.alpha_composite(ov.render(t))
        out.write(fr.convert('RGB').tobytes())
    dec.stdout.close(); dec.wait()
