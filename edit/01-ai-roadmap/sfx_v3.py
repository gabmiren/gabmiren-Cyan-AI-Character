"""v3 audio: replace the synthesized clicks with Gabriel's SFX library, aligned to the v2 visual timeline."""
import subprocess, wave, sys
import numpy as np
sys.argv = [sys.argv[0]]
import compose_v2 as c2
ov = c2.ov

SR = 48000
LIB = '/mnt/user-data/uploads/_originals/'
def load(name):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', LIB + name, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def onset(x, frac=0.1):
    a = np.abs(x); return int(np.argmax(a > a.max() * frac))

S = {}
for key, fname, peak_db, align in [
    ('cam',    'Camera Click.MP3',  -11, 'onset'),   # accent on punch-ins
    ('app',    'appClick.mp3',      -12, 'onset'),   # Save button click
    ('pop',    'pop.mp3',           -17, 'onset'),   # section titles / Save appears
    ('flick',  'flick.MP3',         -18, 'onset'),   # keyword pop-ups
    ('whoosh', 'simplewhoosh.mp3',  -19, 'peak'),    # course cards drop in
    ('ding',   'ding.mp3',          -15, 'onset'),   # ROADMAP finishes typing
]:
    x = load(fname)
    x = x / (np.abs(x).max() + 1e-9) * (10 ** (peak_db / 20))
    off = int(np.abs(x).argmax()) if align == 'peak' else onset(x)
    S[key] = (x, off)

typing = load('typing.mp3')
typing = typing[int(0.26 * SR):]  # skip the lead-in silence

N = int(ov.DUR * SR)
out = np.zeros(N, np.float32)
def add(key, t, gain_db=0.0):
    x, off = S[key]
    i = int(t * SR) - off
    xs = x * (10 ** (gain_db / 20))
    if i < 0: xs = xs[-i:]; i = 0
    j = min(N, i + len(xs)); out[i:j] += xs[:j - i]
def add_typing(t0, dur, peak_db=-23):
    seg = typing[:int(dur * SR)].copy()
    seg = seg / (np.abs(seg).max() + 1e-9) * (10 ** (peak_db / 20))
    fade = int(0.08 * SR); seg[-fade:] *= np.linspace(1, 0, fade)
    i = int(t0 * SR); j = min(N, i + len(seg)); out[i:j] += seg[:j - i]

log = []
for a, b, s in c2.ZOOMS:
    add('cam', a + 0.3); log.append((a + 0.3, 'Camera Click (punch-in accent)'))
for t0, t1, kind, p in ov.ev:
    if kind == 'card':
        add('whoosh', t0 + 0.12); log.append((t0, 'simplewhoosh (card drops in)'))
    elif kind == 'title':
        add('pop', t0); log.append((t0, f'pop (title {p[0]}. {p[1]})'))
    elif kind == 'pop':
        add('flick', t0); log.append((t0, 'flick (keyword pop)'))
    elif kind == 'save':
        add('pop', t0, -3); add('app', t0 + 0.55); log.append((t0, 'pop + appClick (Save button)'))
    elif kind == 'headline':
        add_typing(t0, 1.9); log.append((t0, 'typing (headline types on)'))
    elif kind == 'cta':
        add_typing(t0, 1.15); add('ding', t0 + 1.12); log.append((t0, 'typing + ding (comment ROADMAP)'))

pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
with wave.open('/home/claude/edit/sfx_v3.wav', 'wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
for t, what in sorted(log): print(f'{t:6.2f}s  {what}')
