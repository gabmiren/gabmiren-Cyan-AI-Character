# Handoff: everything from the first Cyan chat (17 to 23 Nov 2026)

This chat built the Halcyon Interns content with Gabriel. It's now retired. Use this file plus PROJECT_INSTRUCTIONS and posts_log.md as the starting context.

## Accounts and places
- TikTok @halcyon.interns and Instagram @tradercyan, both on Metricool brand "Halcyon #2" (blogId 8150055).
- Repo: gabmiren/gabmiren-Cyan-AI-Character (folders: cast/, renders/, edit/, edited/, backgrounds/, claude-project/). edited/README.md is the status log for every video.
- Google Drive folder "Cyan Clips / Edited" (id 1R3iWzhVG392H32m1YRB6_1rd_bh55_WJ), owned by gab@mirenpartners.com. The Drive connector and the gabrielyaozk@gmail.com Chrome profile can't reach it. Use the Chrome profile signed in to Miren.
- Higgsfield team plan. About 380 credits left as of 23 Nov.

## Videos made (all in edited/)
- cyan_nq_meme_v3: chair POV first post, "introducing yourself nonchalantly but...". Posted.
- goingLong / goingShort: earlier skits. goingLong is published ("Our intern is somewhat of a pro trader").
- cyan_stairs_meme_v1: skip-the-stairs priorities (Sleep, Breakfast, Social life, Family dinner, Gym, Trading). Scheduled 20 Nov 6am MYT, "Priorities done right".
- cyan_tradingview_meme_v2: TradingView first-time POV (Genjutsu plus Jasper voice change, scream cut).
- cyan_glide_meme_v3: office chair glide, "free to trade during work" (Seedance). Open issue: too many background people. A 24-credit redraft was offered.
- cyan_villain_futures_meme_v4: "POV: you're a villain who trades futures on the side" (Genjutsu plus Gabriel's TTS plus order-filled sound effect, lip sync fixed by hand). Caption "Villain by day, trader by night 🫡".
- Text posts: see posts_log.md.

## Proven techniques
- Genjutsu (hf_mult_motion_control) copies burned-in text from the ref. Inpaint the text out of the ref first (cv2 inpaint, with a mask of bright pixels next to dark ones).
- Voice change only converts speech and roughly the first 4s. Split the audio into about 4s chunks.
- Lip sync fix: find mouth movement with an OpenCV face cascade, then place each phrase with atempo.
- Seedance with video refs copies the ref's movement but ignores prompt changes. Prompt-only gives more natural movement but loses the specific action.
- Downloading Higgsfield outputs (cloudfront is blocked in the sandbox):
  1. In Chrome, open any cloudfront image URL.
  2. Run a JS fetch of all the files.
  3. Bundle them into one .bin with a 300-byte JSON header and click a download anchor.
  4. Stage ~/Downloads/<file>.bin.
  - Chrome allows one download per page load. If a download silently fails, open a fresh tab group.
- Importing into Higgsfield: push the file to the repo's tmp/, import with media_import_url via a jsDelivr URL pinned to the commit (raw.githubusercontent gets refused), then delete tmp/.
- Drive upload: inject an input[type=file], fill it with file_upload (3.8MB max), then send a drag-and-drop event to the Drive page. Files over 3.8MB get re-encoded at about 3Mbps first.
- Seamless loop: split the clip and trim from 0.5s to the end, then crossfade 0.5s into the first 0.5s.

## Backgrounds
- backgrounds/bg_01..10: the original cyan loops (Kling 3.0 std 8s). Dropped from use: 03 rainy window, 04 chart macro, 06 keyboard, 07 trading floor.
- backgrounds/*_logo.mp4: 01, 05, 08, 09, 10 with the HALCYON sign. Cyan is in 01, 05 and 10. Made with Nano Banana 2.1 stills (logo-stills/) and Kling 3.0 std 10s.
  - Still job IDs: 6dbef7c5-f42f-4e25-8a1b-ab7517c5d59f (01), 7898fe0c-c2bf-48a7-b664-681788afbe0f (05), 314c4bb2-19c9-4bfc-af66-471de80a00da (08), e1e6d744-f228-4b4d-97d6-60d0536803bd (09), fd7a33d0-f68f-42d9-8cac-abe1d4811d79 (10). Reuse them as media values for rerolls.
  - The 09 sign looks like it's on the window glass. Gabriel kept it anyway.

## Docs made
- Claude Doc "Halcyon Interns: planfomo study and Cyan content ideas": https://claude.ai/artifact/4UyuUQqxaS6VUp6wDaUx35
- Research artifact: https://claude.ai/artifact/P1Cku8Gd3D1HhUwKxFVp8D
- Carousel style study of the ishitglitterrr education carousel (the photo post format) is in the chat only. It's the reference for future Cyan education carousels.

## Waiting on Gabriel
- Rebuild glossary, head trader rules, sessions ranked and trailing drawdown without blur before posting. Also check the drawdown numbers against Halcyon's real rules.
- Chibi Cyan sticker pack for carousels (about 18 credits with buffer). First carousel topic is still open: eval rules or futures glossary.
- 6-loop Cyan b-roll pack (about 126 credits with buffer).
- Chair glide v3 redraft to cut the background people (24 credits).
- Captions and schedule for the remaining text posts.

## Treg endpoints that worked
- anyapi.tiktok.user.videos (handle, cursor)
- treg.tiktok.user.profile (username)
- anyapi.tiktok.search.videos (query, sortBy 1, datePosted 90)
- anyapi.tiktok.photos
- anyapi.tiktok.video_transcript_full
- Use the fields and max_items parameters, because jq on output.data often fails.
