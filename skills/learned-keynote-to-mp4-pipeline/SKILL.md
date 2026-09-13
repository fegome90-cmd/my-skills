---
disable-model-invocation: true
name: learned-keynote-to-mp4-pipeline
description: "Use when you need to generate a video MP4 from a Keynote presentation with slide-by-slide audio narration — Keynote scripting cannot create audio_clips (confirmed via sdef), so the solution is to export slides as vector PDF, rasterize at high DPI with pdftoppm, generate one MP4 per slide with ffmpeg, and concatenate the final video. Also covers when Keynote audio insertions break during reimport or when you need reproducible slide-by-slide video builds."
---

# Keynote → PDF → MP4 Pipeline

## Context

Keynote's AppleScript/JXA scripting dictionary (`sdef`) exposes `audio clip` objects but **does not expose a `file` property for creating new audio clips**. The only properties are `file name` (read-only string), `clip volume`, and `repetition method`. This means:

- You **cannot** create a new audio clip from a file path via AppleScript/JXA/OSA.
- You **cannot** automate embedding narration into slides vía scripting.
- You can only read/modify audio clips that were inserted manually via the UI.

The same limitation applies to JXA (JavaScript for Automation): `slide.audioClips.push(keynote.AudioClip({file: Path(...)}))` fails with "No se pueden convertir tipos" because `file` is not a recognized property.

**Documentation limit confirmed at:** `/Applications/Keynote.app` sdef class `audio clip` (code `shau`, inherits `iWork item`).

## Problem

You have a Keynote presentation with `n` slides, each with an audio narration file (MP3, M4A) that was either recorded via Keynote's Insert → Audio or provided externally. You want a single video MP4 with:

- HD slides (text readable, not pixelated)
- Audio synchronized per slide: each slide lasts exactly the duration of its narration
- A final slide with a fixed duration (e.g., 10s for closing credits)
- Reproducible builds: if one audio needs fixing, re-generate only that slide's MP4

Keynote's own export to video can work, but if slides have embedded audio from the original recording and became desynchronized (e.g., Keynote stripped references when reopening a manipulated `.key`), or if you don't want to fight the UI for 27+ manual drag-and-drops, this pipeline solves it.

## Solution

A 4-step pipeline using open-source tools (`ffmpeg`, `poppler`, built-in macOS scripting):

### Preflight Diagnostics

Before running the pipeline, verify required tooling and slide aspect ratio:

```bash
# 1. Verify required CLI tools
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: ffmpeg is required (install via package manager)" >&2; exit 1; }
command -v pdftoppm >/dev/null 2>&1 || { echo "ERROR: pdftoppm (poppler) is required" >&2; exit 1; }

# 2. Verify Keynote.app is accessible
osascript -e 'id of application "Keynote"' >/dev/null 2>&1 || { echo "ERROR: Keynote.app not accessible via AppleScript" >&2; exit 1; }

# 3. Identify slide aspect ratio:
# - Standard 4:3 (Keynote default): use scale=1440:1080:flags=lanczos
# - Widescreen 16:9: use scale=1920:1080:flags=lanczos
```

### Step 1: Export slides as vector PDF

```bash
# Via osascript (AppleScript)
osascript -e '
tell application "Keynote"
  activate
  export front document to POSIX file "/tmp/presentation-export.pdf" as PDF ¬
    with properties {PDF image quality:best, skipped slides:false}
end tell'
```

Or via JXA:
```javascript
const keynote = Application("Keynote");
const doc = keynote.documents[0];
doc.export({
  to: Path("/tmp/presentation-export.pdf"),
  as: "PDF",
  withProperties: {PDFImageQuality: "best"}
});
```

### Step 2: Rasterize PDF to HD PNGs

```bash
# 200 DPI → ~2000×1500 px for 4:3 slides (standard Keynote)
pdftoppm -png -r 200 /tmp/presentation-export.pdf /tmp/slides-hd/slide

# Rename to zero-padded order (slide-01.png, slide-02.png, …)
cd /tmp/slides-hd
for f in slide-*.png; do
  n=$(echo "$f" | sed -E 's/slide-([0-9]+)\.png/\1/')
  mv "$f" "$(printf "slide-%02d.png" "$n")"
done
```

**Why 200 DPI?** Keynote slides at standard 4:3 size (10×7.5 inches × 200 DPI = 2000×1500). This gives enough resolution for a **downscale** to target video resolution, which always look better than upscaling from the Keynote-native 720×540 export.

### Step 3: Generate one MP4 per slide

```bash
# Slide with audio: image loops infinitely, -shortest cuts at audio EOF
ffmpeg -loop 1 -i slide-NN.png -i "NN - Titulo.mp3" \
  -vf "scale=1440:1080:flags=lanczos" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  -shortest slide-NN.mp4

# Slide without audio (e.g., bibliography/final): fixed duration with -t
ffmpeg -loop 1 -i slide-28.png -t 10 \
  -vf "scale=1440:1080:flags=lanczos" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p slide-28.mp4
```

**Key parameters explained:**
- `-loop 1`: Make the (single) image a video stream that repeats indefinitely
- `-shortest`: Stop encoding when the shortest input stream ends — here, the audio. Result: video duration = audio duration
- `flags=lanczos`: Best upscaling/downscaling algorithm for text-heavy content
- `-preset slow -crf 18`: High-quality H.264 with efficient file size
- Slide without audio: use `-t 10` instead of `-i audio.mp3` to set a fixed duration

**For final slide without audio, create a silent audio track** so the concat filter (next step) has uniform inputs:

```bash
ffmpeg -i slide-28.mp4 \
  -f lavfi -i anullsrc=channel_layout=mono:sample_rate=44100 \
  -c:v copy -c:a aac -b:a 192k -shortest slide-28-fixed.mp4
mv slide-28-fixed.mp4 slide-28.mp4
```

### Step 4: Concatenate into final video

There are two strategies — choose based on your needs:

**Strategy A: `-c copy` (fast, 5s)** — only if all MP4s have identical codec parameters (same resolution, fps, timebase, audio format):

```bash
echo "file 'slide-01.mp4'" > filelist.txt
echo "file 'slide-02.mp4'" >> filelist.txt
# ... all n slides
echo "file 'slide-nn.mp4'" >> filelist.txt
ffmpeg -f concat -safe 0 -i filelist.txt -c copy final.mp4
```

**Strategy B: `filter_complex concat` (slower, ~2min, timestamps clean)** — works regardless of codec differences, produces clean timestamps. **Recommended** if you experienced audio dropouts with strategy A:

```bash
# Build filter for n slides
ARGS=""
FILTER=""
for i in $(seq 0 $((N-1))); do
  nn=$(printf "%02d" $((i+1)))
  ARGS="$ARGS -i slide-${nn}.mp4"
  FILTER="${FILTER}[${i}:v][${i}:a]"
done
FILTER="${FILTER}concat=n=${N}:v=1:a=1[v][a]"

ffmpeg $ARGS \
  -filter_complex "$FILTER" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  final.mp4
```

Strategy B was verified to fix audio dropouts that occurred with strategy A (symptom: audio missing on a specific slide in the concatenated output but present in the individual MP4).

## Example

Generating the first 3 slides of a medical presentation, 1440×1080:

```bash
# Verify prerequisites (ffmpeg, pdftoppm) are installed before starting:
command -v ffmpeg >/dev/null 2>&1 && command -v pdftoppm >/dev/null 2>&1 || exit 1

# 1. Export Keynote → PDF
osascript -e 'tell application "Keynote" to export front document to ¬
  POSIX file "/tmp/med-presentation.pdf" as PDF with properties ¬
    {PDF image quality:best, skipped slides:false}'

# 2. Rasterize
mkdir -p /tmp/slides
pdftoppm -png -r 200 /tmp/med-presentation.pdf /tmp/slides/slide

# 3. Rename to zero-padded
cd /tmp/slides && for f in slide-*.png; do
  n=$(echo "$f" | sed -E 's/slide-([0-9]+)\.png/\1/')
  mv "$f" "$(printf "slide-%02d.png" "$n")"
done

# 4. Generate MP4 per slide
for n in 01 02 03; do
  ffmpeg -hide_banner -loglevel error -y \
    -loop 1 -i "slide-$n.png" -i "./audio/slide-$n.mp3" \
    -vf "scale=1440:1080:flags=lanczos" \
    -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -shortest "slide-$n.mp4"
done

# 5. Concat (assuming slides 01-03 all have audio; slide 04 is silent)
ffmpeg -i slide-01.mp4 -i slide-02.mp4 -i slide-03.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k -movflags +faststart final.mp4
```

## Activation Signals

- You have a Keynote presentation and need a video with synchronized audio per slide.
- You tried to automate audio insertion in Keynote via AppleScript/JXA and got "No se pueden convertir tipos"
- Keynote's own "Export → Movie" produces a silent or desynchronized result
- You want a reproducible pipeline that doesn't require manually dragging audio to each slide
- You need to iterate on individual slides (fix one, re-concat, don't re-encode everything)
- The `.key` file already has its audio stripped by Keynote on reimport (common when the `.key` package was manipulated externally)

## Known Limitations

- **Transitions between slides are hard cuts.** The concat filter does not support fades between clips. For crossfade or other transitions, use `-filter_complex xfade` instead of concat, which requires recoding and more complex parameter setup.
- **Resolution scaling is manual.** The pipeline assumes 4:3 slides (common Keynote default). For widescreen (16:9), adjust `scale` target or use `pad` with `force_original_aspect_ratio=decrease`.
- **No embedded metadata in the final video.** Use `ffmpeg -metadata` if you need title/author tags.
