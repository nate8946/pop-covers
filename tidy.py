#!/usr/bin/env python3
"""Move karaoke, remix, live, instrumental and other extra releases out of albums/ into albums/_extras/
and drop them from manifest.json. Nothing is deleted. Run from the repo folder: python3 tidy.py"""
import json, os, re, shutil
ROOT = os.path.dirname(os.path.abspath(__file__))
JUNK = re.compile(r"karaoke|remix|dance-mixes|relax-mix|instrumental|a-cappella|live-|-live|world-tour|tour-usa|video-album|video-ep|"
                  r"anthology|message-from|the-encore|behind-the-curtain|acoustic-collection|track-by-track|surprise-song|"
                  r"long-pond|itunes-live|clear-channel|irreemplazable|deluxe|ego-sweet|single-ladies|telephone-|"
                  r"if-i-were-a-boy|above-and-beyonce|beyonce-experience|club-future|dawn-of-chromatica|"
                  r"petal-(the|making)|k-bye|yes-and|up-next|radio-volume|re-up|paradise-edition|bichota-season|"
                  r"anniversary|soundtrack|motion-picture|black-panther|extended|dj-mix|the-remix|a-star-is-born", re.I)
KEEP = {"beyonce--homecoming-the-live-album.jpg"}
os.makedirs(os.path.join(ROOT, "albums", "_extras"), exist_ok=True)
m = json.load(open(os.path.join(ROOT, "manifest.json")))
moved = []
for f in sorted(os.listdir(os.path.join(ROOT, "albums"))):
    if f.endswith(".jpg") and f not in KEEP and JUNK.search(f):
        shutil.move(os.path.join(ROOT, "albums", f), os.path.join(ROOT, "albums", "_extras", f)); moved.append(f)
m["albums"] = [e for e in m["albums"] if os.path.basename(e["file"]) not in moved]
json.dump(m, open(os.path.join(ROOT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
print(f"moved {len(moved)} files to albums/_extras:"); [print("  ", f) for f in moved]
