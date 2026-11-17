# 01 AI roadmap – edit

- Source clips: 4 Seedance 2.5 480p drafts (scene1-4), trimmed to speech, joined, sped up 1.1x (pitch kept), upscaled to 720x1280, light handheld shake.
- `overlay.py` renders the overlay layer (headline, captions, section titles, course cards, pops, Save button, comment ROADMAP) as RGBA frames piped into ffmpeg.
- `vad.py` finds speech segments; caption word timings are estimated from those segments (no speech-to-text available), so a word can land a beat early or late.
- To finalise: swap in the 720p finals with the same trims and re-run.

## v2 – punch-ins and SFX
- `compose_v2.py` follows the zoom recipe: hook holds ~5.7s uncut, then 7 snap punch-ins (115–118%) on turning-point lines, each held ~1.6–2s and snapping back as the next text lands.
- Zooms replace the "like a junior analyst", "goes further" and "show it once" pops; text and zooms take turns.
- SFX generated in code: an accent click ~0.3s after each punch-in, soft clicks as cards/titles/pops arrive, typing ticks under the typed headline and CTA.
