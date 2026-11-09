#!/usr/bin/env python3
"""Backup cover fetcher using Deezer (no key needed). Run from the repo folder:
  python3 run_deezer.py roster_failed.txt
Lines look like:  Artist | Album.  Saves albums/artist--album.jpg (1000px) and updates manifest.json.
Anything it can't find is written to deezer_failed.txt."""
import sys, os, re, json, time, difflib, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.abspath(__file__)); MAN = os.path.join(ROOT, "manifest.json")

def slug(s):
    for a, b in (("é","e"),("á","a"),("ó","o"),("ñ","n"),("í","i"),("ë","e"),("ø","o")): s = s.lower().replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
def alnum(s):
    s = s.lower()
    for a, b in (("é","e"),("ø","o"),("ë","e"),("’","'")): s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "", s)
def clean(s): return re.sub(r"\s*[\(\[][^)\]]*(deluxe|edition|version|remaster|expanded|anniversary|bonus)[^)\]]*[\)\]]", "", s, flags=re.I).strip()
def get(url, binary=False):
    for i in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = r.read(); return d if binary else json.loads(d)
        except Exception as e:
            print("   retry:", e); time.sleep(5 * (i + 1))
    return None

def find(artist, album):
    best, score = None, 0
    for q in (f'artist:"{artist}" album:"{album}"', f"{artist} {album}", album):
        d = get("https://api.deezer.com/search/album?" + urllib.parse.urlencode({"q": q, "limit": 25}))
        for x in (d or {}).get("data", []):
            an = x.get("artist", {}).get("name", "")
            if not (alnum(artist) in alnum(an) or alnum(an) in alnum(artist)): continue
            r = difflib.SequenceMatcher(None, alnum(clean(x["title"])), alnum(album)).ratio()
            if r > score: best, score = x, r
        if best and score >= 0.8: break
        time.sleep(0.5)
    return best if score >= 0.72 else None

def main():
    m = json.load(open(MAN)) if os.path.exists(MAN) else {}
    for k in ("albums", "artists", "unsorted"): m.setdefault(k, [])
    failed = []
    lines = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if "|" in l and not l.startswith("#")]
    for i, line in enumerate(lines, 1):
        a, b = [s.strip() for s in line.split("|", 1)]
        rel = f"albums/{slug(a)}--{slug(b)}.jpg"; path = os.path.join(ROOT, rel)
        if os.path.exists(path): print(f"[{i}/{len(lines)}] have {rel}"); continue
        x = find(a, b)
        img = (x.get("cover_xl") or x.get("cover_big")) if x else None
        data = get(img, True) if img else None
        if not data:
            print(f"[{i}/{len(lines)}] NO MATCH {a} | {b}"); failed.append(line); continue
        os.makedirs(os.path.dirname(path), exist_ok=True); open(path, "wb").write(data)
        m["albums"] = [e for e in m["albums"] if e.get("file") != rel]
        m["albums"].append({"artist": a, "album": b, "file": rel})
        print(f"[{i}/{len(lines)}] saved {rel}" + (f"   (Deezer title: {x['title']})" if slug(x['title']) != slug(b) else ""))
        if i % 10 == 0: json.dump(m, open(MAN, "w"), indent=1, ensure_ascii=False)
        time.sleep(0.4)
    json.dump(m, open(MAN, "w"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "deezer_failed.txt"), "w").write("\n".join(failed) + "\n")
    print(f"\nDone. {len(failed)} not found -> deezer_failed.txt")
main()
