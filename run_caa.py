#!/usr/bin/env python3
"""Third cover source: MusicBrainz + Cover Art Archive (no key). Run from the repo folder:
  python3 run_caa.py caa_list.txt        (lines: Artist | Album)
Saves albums/artist--album.jpg and updates manifest.json. Failures -> caa_failed.txt."""
import sys, os, re, json, time, difflib, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.abspath(__file__)); MAN = os.path.join(ROOT, "manifest.json")
UA = {"User-Agent": "pop-covers/1.0 (nathanh8946@gmail.com)"}
def slug(s):
    for a, b in (("é","e"),("á","a"),("ó","o"),("ñ","n"),("í","i")): s = s.lower().replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
def alnum(s): return re.sub(r"[^a-z0-9]+", "", s.lower())
def get(url, binary=False):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                d = r.read(); return d if binary else json.loads(d)
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(5 * (i + 1))
        except Exception as e:
            time.sleep(5 * (i + 1))
    return None
def find(artist, album):
    q = f'releasegroup:"{album}" AND artist:"{artist}"'
    d = get("https://musicbrainz.org/ws/2/release-group?fmt=json&limit=15&query=" + urllib.parse.quote(q))
    time.sleep(1.2)
    best, score = None, 0
    for x in (d or {}).get("release-groups", []):
        if x.get("primary-type") not in (None, "Album"): continue
        names = " ".join(c["name"] for c in x.get("artist-credit", []) if isinstance(c, dict) and "name" in c)
        if alnum(artist)[:5] not in alnum(names): continue
        r = difflib.SequenceMatcher(None, alnum(x["title"]), alnum(album)).ratio()
        if r > score: best, score = x, r
    return best if score >= 0.7 else None
def main():
    m = json.load(open(MAN)) if os.path.exists(MAN) else {}
    for k in ("albums", "artists", "unsorted"): m.setdefault(k, [])
    failed = []
    lines = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if "|" in l and not l.startswith("#")]
    for i, line in enumerate(lines, 1):
        a, b = [s.strip() for s in line.split("|", 1)]
        rel = f"albums/{slug(a)}--{slug(b)}.jpg"; path = os.path.join(ROOT, rel)
        if os.path.exists(path): print(f"[{i}/{len(lines)}] have {rel}"); continue
        x = find(a, b); data = get(f"https://coverartarchive.org/release-group/{x['id']}/front-500", True) if x else None
        time.sleep(1)
        if not data: print(f"[{i}/{len(lines)}] NO MATCH {a} | {b}"); failed.append(line); continue
        open(path, "wb").write(data)
        m["albums"] = [e for e in m["albums"] if e.get("file") != rel]; m["albums"].append({"artist": a, "album": b, "file": rel})
        print(f"[{i}/{len(lines)}] saved {rel}")
    json.dump(m, open(MAN, "w"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "caa_failed.txt"), "w").write("\n".join(failed) + "\n")
    print(f"\nDone. {len(failed)} not found -> caa_failed.txt")
main()
