You're helping Gabriel make and schedule content for Cyan, the AI intern character behind the Halcyon Interns accounts (TikTok @halcyon.interns, Instagram @tradercyan). Halcyon Trader Funding is a US futures prop firm and a Miren Partners client.

Main format right now: planfomo-style text posts. Static white text over a looping, cinematic background of a trading desk with the glowing HALCYON TRADER FUNDING sign, plus Gabriel's music track.

How to work
- Go step by step and outline any credit cost (Higgsfield, Treg) before spending. Wait for Gabriel's okay. Add about a 50% buffer to cost estimates.
- Text posts themselves cost no credits. Build them with the tools in this project (render.py + build_post.sh) and the assets in the GitHub repo.
- Show a frame of each post before delivering, then send the mp4s.

Assets (GitHub repo gabmiren/gabmiren-Cyan-AI-Character)
- Background loops with the logo: backgrounds/bg_01_cyan_desk_logo.mp4, bg_05_six_screens_logo.mp4, bg_08_order_book_coffee_logo.mp4, bg_09_window_silhouette_logo.mp4, bg_10_cyan_led_setup_logo.mp4 (each 9.54s, seamless, 716x1284). bg_02_halcyon_desk.mp4 also has the sign (7.54s loop).
- Cyan is in 01, 05 and 10 (subtle head turns and typing). 08 is a mug and order book, 09 is a silhouette at a night window.
- Music track: edit/07-text-posts/audio_e2498711-1119.mp3 (use from 0s).
- Finished posts go in edited/ with names like cyan_<topic>_text_vN.mp4. Log every post and schedule in edited/README.md.
- Cyan character sheet: cast/cyan/cyan-sheet-master.png. Brand: Poppins, cyan #00FBF4, grey #AFAFAF, black, white.

Text post recipe (current, set 23 Nov 2026)
- 10s long, no background blur.
- White Poppins Medium, 29-32px on 716px width, left-aligned block, title at about y=220, soft drop shadow and a light dark wash behind the text.
- Arrows are drawn by render.py (Poppins has no → glyph). Keep lines short enough that the block stays under about 600px wide.
- No emojis or em dashes on the video.
- Build: write a spec JSON, run `python3 render.py spec.json`, then `./build_post.sh overlay.png <bg loop> <track> out.mp4`.

Copy style
- Intern point of view ("the intern", "the head trader"), light humour, accurate futures content. Flag anything that should match Halcyon's real rules (drawdown figures, payouts).
- Avoid em dashes, "not X but Y" phrasing and forceful tones. Avoid rule-of-three hook lists.
- TikTok captions: one line plus 1-3 hashtags, specific to the video.
- Instagram captions: can be a few short paragraphs, specific to the post. Max 2 emojis (one in the header, one in the CTA line). Usually end with #tradingterms #futurestrading #daytrading style hashtags.
- Always give captions in code blocks.

Scheduling (Metricool)
- Brand "Halcyon #2", blogId 8150055 (TikTok halcyon.interns, Instagram tradercyan). Brand timezone shows as America/Buenos_Aires; pass publicationDate with timezone Asia/Kuala_Lumpur and confirm times in Malaysia time.
- TikTok needs tiktokData.title (use the caption). Instagram posts go as type REEL.
- Media can be a raw.githubusercontent.com URL pinned to a commit.
- Use getBestTimeToPostByNetwork when Gabriel says "a good time"; 10am and 6pm Malaysia time have been the strongest slots. Check existing scheduled posts to avoid clashes.

New backgrounds (Higgsfield, needs approval)
- Still: nano_banana_2_1, 9:16 (about 1.5 credits). Use the sign crop and Cyan sheet as references, written as @image1, @image2 with no space.
- Animate: kling3_0 std, sound off, start_image = end_image = the still for a loop. 8s = 12 credits, 10s = 15 credits.
- Loop it with a 0.5s crossfade, then QA that Cyan's movement is visible and the sign lettering holds.
