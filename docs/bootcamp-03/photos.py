#!/usr/bin/env python3
"""photos.py — shrink the bootcamp photos to web size before they are committed. macOS only (uses sips).

    python3 photos.py            # photos-src/  ->  photos/
    python3 photos.py --quality 65

Put the originals here (this folder is git-ignored, the originals never leave your Mac):

    photos-src/teams/<Team Name>.jpg     group photo of a selected team with the mentor   -> selected-teams.html
    photos-src/rising/<anything>.jpg     rising-talent students, each with the mentor; they float up on rising-talent.html

Any of jpg, jpeg, png, heic, heif, tif, webp goes in; a JPEG comes out, long edge capped per folder,
EXIF stripped, quality 72 by default (about 150–400 KB for a phone photo). photos/rising/list.txt lists
the rising photos, because a static site cannot read a folder. A photo already converted and newer
than its original is skipped, so re-running is cheap.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "photos-src")
OUT = os.path.join(HERE, "photos")
LONG_EDGE = {"teams": 1600, "rising": 900}
EXT = (".jpg", ".jpeg", ".png", ".heic", ".heif", ".tif", ".tiff", ".webp")

quality = 72
args = sys.argv[1:]
while args:
    a = args.pop(0)
    if a == "--quality" and args:
        quality = int(args.pop(0))
    elif a == "--src" and args:
        SRC = os.path.abspath(args.pop(0))
    elif a == "--out" and args:
        OUT = os.path.abspath(args.pop(0))
    else:
        sys.exit(__doc__)

if subprocess.run(["which", "sips"], capture_output=True).returncode != 0:
    sys.exit("sips not found: this script runs on macOS. On Linux use ImageMagick: magick in.jpg -resize 1600x1600> -quality 72 -strip out.jpg")
if not os.path.isdir(SRC):
    sys.exit(f"no {SRC}: create photos-src/teams and photos-src/rising and drop the originals in")

total_in = total_out = 0
for kind, edge in LONG_EDGE.items():
    src_dir, out_dir = os.path.join(SRC, kind), os.path.join(OUT, kind)
    names = sorted(n for n in os.listdir(src_dir) if n.lower().endswith(EXT)) if os.path.isdir(src_dir) else []
    if not names and kind != "rising":
        continue
    os.makedirs(out_dir, exist_ok=True)
    done = []
    for n in names:
        base = os.path.splitext(n)[0].strip()
        src, out = os.path.join(src_dir, n), os.path.join(out_dir, base + ".jpg")
        done.append(base + ".jpg")
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src):
            continue
        r = subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(quality), "-Z", str(edge), src, "--out", out],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  FAILED {kind}/{n}: {r.stderr.strip() or r.stdout.strip()}")
            done.pop()
            continue
        # sips keeps EXIF (GPS, camera) — drop it: re-save without properties is not offered, so blank the ones that matter
        subprocess.run(["sips", "-d", "description", "-d", "copyright", "-d", "artist", "-d", "creator", out], capture_output=True)
        a, b = os.path.getsize(src), os.path.getsize(out)
        total_in += a; total_out += b
        print(f"  {kind}/{n}  {a // 1024} KB  ->  {base}.jpg  {b // 1024} KB")
    if kind == "rising":
        with open(os.path.join(out_dir, "list.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(done) + ("\n" if done else ""))
        print(f"  rising/list.txt: {len(done)} photo(s)")
if total_in:
    print(f"converted {total_in // 1024} KB -> {total_out // 1024} KB")
else:
    print("nothing new to convert")
