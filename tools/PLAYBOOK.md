# Havtalia Content Playbook

Instructions for the daily content run. Havtalia LLC is Mohamed Elroby's agency: Facebook & Instagram ads plus appointment setting that books estimates for US tree service and home service companies. The goal of every post is **inbound leads from business owners** (more and bigger agency clients), not likes.

**Audience (Mohamed, 2026-11-12):** write for **home service business owners** in general: plumbers, roofers, HVAC, tree service, landscapers, painters, fencing and similar. Those are the people viewing the stories. Don't make posts tree-only. Use "Home service owners:" hooks, mix trades in examples, and say "your company" / "your average job", not "your tree co." A tree example is fine as one example among several, or when the proof itself came from a tree client.

**CTA keyword is BOOK** (changed from TREE on 2026-11-12): "Comment BOOK 👇" on every post and video.

## Where things live
- **Content Hub** (approval queue + material inbox): https://claude.ai/artifact/CryFyvpFr1cwxmKai611dH
  - Read/write its database with the ArtifactData tool.
  - `posts` collection: `{date: "YYYY-MM-DD", title, type: short|image|carousel, platforms: [fb,ig,li,yt], status: draft|approved|posted, assetId, assetType, caption, captions: {fb, ig, li, yt_title, yt}, mediaUrl, storyUrl, scheduledFor, ghlPostIds, postedOn, note, createdAt}`
  - `inbox` collection (uploads from Mohamed): `{assetId, contentType, kind: results|review|chat|work|other, note, status: new|used, createdAt, fileName}`. Read the file with Artifact `action: "read"`, `path: <assetId>`.
  - To show media in the Hub, upload the final file with Artifact `asset: true` and store the returned id as `assetId`.
- **Public media for posting**: GitHub repo `mohamedelropy/havtalia` (public). Put files in `media/YYYY-MM/` and use
  `https://raw.githubusercontent.com/mohamedelropy/havtalia/main/media/YYYY-MM/<file>` as the media URL. Never put client names, phone numbers or private data in this repo.
- **GHL** (MCP connector "GHL"): location `94Oe2XPx1Kw9MMguPAQH` (havtalia llc), userId/createdBy `1ImaIV4pC1Cs5dNKjlKe`. Operation `create-post`.
  - Facebook page: `68b57ff68a85b976bec20353_94Oe2XPx1Kw9MMguPAQH_621245324396607_page`
  - Instagram: `68b580734270a43fd4fa911d_94Oe2XPx1Kw9MMguPAQH_17841400959198021`
  - LinkedIn (Mohamed's profile): `68b5809f8a85b9b208c29a26_94Oe2XPx1Kw9MMguPAQH_RUXxiRvTvR_profile`
  - YouTube (@havtaliamarketing): `6af353696c5574ec85ec8981_94Oe2XPx1Kw9MMguPAQH_UCvTNddQsz9iwK6Z5MjwAQDw_profile`
  - Re-check accounts with `get-account` each run (TikTok may be added later; post videos there too when it appears).

## Daily run
1. **Publish what Mohamed approved.** For each `posts` doc with `status: approved` and no `ghlPostIds`, schedule it in GHL for **today 12:30 PM US/Eastern** (if that time has passed, 30 minutes from now):
   - Video: one `create-post` with type `reel` to FB + IG + YouTube (`facebookPostDetails.type: reel`, `instagramPostDetails: {type: reel, showOnFeed: true}`, `youtubePostDetails: {type: short, title, privacyLevel: public}`); a second `create-post` type `post` to LinkedIn with the LinkedIn caption.
   - Image: one `create-post` type `post` to FB + IG with the FB/IG caption, one to LinkedIn with the LinkedIn caption.
   - **Story every time**: `create-post` type `story` to FB + IG, 5 minutes after the feed post, `summary: ""` (stories take no caption). Use the 9:16 story image/video (`storyUrl`), or the short itself for videos.
   - Write `ghlPostIds`, `scheduledFor` back to the doc. Use an idempotencyKey per post.
2. **Mark yesterday's scheduled posts.** At publish time GHL marks the post you created as `deleted` and splits it into one child post per platform (`parentPostId` = your post id). So check with `get-posts` (body `{type: "all", fromDate, toDate, limit: "50"}`) and match children by `parentPostId`; each child has `status`, `error` and `previewLink`. If published set `status: posted`, `postedOn`; if failed, put the error in `note` and leave status `approved`.
3. **Make tomorrow's content** (one piece per day; aim for 4 videos + 3 image posts a week). First use any `inbox` items with `status: new` (case studies, reviews, results beat everything else), then mark them `used`. With no new material, use the content pillars below. Create the post as `status: draft` dated tomorrow, with the feed media, a 9:16 story version, and per-platform captions. Mohamed approves in the Hub. Never publish a draft he has not approved.

## Making media
Setup in a fresh session (tools/ folder):
```
cd tools && npm i && npm i playwright   # Chromium is preinstalled; don't run playwright install
pip install --break-system-packages kokoro-onnx soundfile
mkdir -p ~/kokoro && cd ~/kokoro && curl -sLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx && curl -sLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```
- **Short video (1080x1920, 25-40 s):** copy `templates/short-example.html`, rewrite scenes, script and timings (keep the `render(t)` engine, captions, progress bar, brand tag). Voice: `python3 tts.py lines.json out/tts`, then set scene/VO start times from the printed durations. `node render_video.js <html> out/silent.mp4 <dur>`; `python3 mix.py out/silent.mp4 out/final.mp4 <dur> out/tts a0:0.3 a1:... `. Check 5 frames before publishing (text inside frame, no overlaps, captions readable).
- **Image post (1080x1350) / story (1080x1920):** copy `templates/post-example.html`; `node render_image.js <html> out/post.jpg 1080 1350`. Instagram needs JPEG.
- Using Mohamed's screenshots: crop to the proof (numbers, booked appointments, review text) and **blur or cover every client name, face, phone number, address and ad-account ID** before it goes anywhere public. Never invent or change numbers; quote them exactly as shown and say where they came from (e.g. "tree service client, South Carolina").
- Brand tagline on videos: "Estimates for home service". Brand: forest green #1D4A37, signal orange #FF6B1A, lime #C9E27A, sand #F4F1EA, ink #121815. Fonts: Fraunces (headlines), Schibsted Grotesk (body), JetBrains Mono (labels). Logo `assets/logo.webp`. Handle on visuals: @havtaliallc.

## What to post (pillars)
1. **Proof** (top priority): case studies and results from the inbox. Format: situation → what we changed → numbers → "want the same? Comment BOOK".
2. **Money math**: what one job is worth vs. ad spend; cost of slow follow-up; missed calls.
3. **Ad teardowns**: a weak home-service ad vs. the stronger version (generic, no real competitor names).
4. **Mistakes & fixes**: price shoppers, no follow-up, stock photos, no reviews, slow reply time.
5. **Reviews**: client testimonial as a quote card (only real reviews from the inbox, verbatim, client name blurred or first name + state only if Mohamed says so).
6. **Offer**: what Havtalia does, who it's for, how to start (comment BOOK / book a call at https://app.havtalia.com).
Rotate pillars; no two days in a row from the same pillar. Hooks in the first 2 seconds/first line, written to home service owners across trades ("Home service owners:", "Plumbers, roofers, tree guys:", "If your crew is sitting idle…").

## Captions
- **FB/IG**: hook line, 3-6 short lines of value, CTA "Comment BOOK 👇" (or "DM us ESTIMATE"), then 8-12 hashtags.
- **LinkedIn**: written for owners/operators, a short story or lesson with numbers, arrows for steps, CTA to comment BOOK or message Mohamed, 4-6 hashtags.
- **YouTube**: title under 70 characters with a search phrase (e.g. "home service marketing", "facebook ads for contractors", "home service leads", "plumbing/roofing/tree service marketing"); description = FB caption + "Book a free call: https://app.havtalia.com".
- Never promise guaranteed results or make up stats. Results are "for one client", not "for everyone".

### Hashtag bank (mix per post, 8-12 on IG/FB)
Tree: #treeservice #treeservicebusiness #arborist #arboristlife #treeremoval #treecare #treetrimming #stumpgrinding #treeworker #treecompany
Home service (lead with these): #homeservicebusiness #homeservices #contractor #contractorlife #contractormarketing #plumbingbusiness #plumber #roofingbusiness #roofingcontractor #hvacbusiness #landscapingbusiness #fencecontractor #paintingcontractor
Growth/ads: #facebookads #metaads #leadgeneration #appointmentsetting #smallbusinessowner #smallbusinessmarketing #businessgrowth #marketingagency
LinkedIn: #homeservices #contractormarketing #plumbing #roofing #treeservice #leadgeneration #smallbusiness #facebookads

## Report
End each run with a short message to Mohamed in Egyptian Arabic: what was scheduled today (platform + time Cairo), what's waiting for his approval in the Hub, and anything that failed.
