#!/usr/bin/env python3
"""Download album covers from Apple's iTunes Search API (no account or keys needed).

Run from the pop-covers folder (the one containing albums/ and manifest.json):
  python3 fetch_covers_itunes.py album "Taylor Swift" "Midnights"
  python3 fetch_covers_itunes.py artist-albums "Sabrina Carpenter"
  python3 fetch_covers_itunes.py list wanted.txt      # lines: Artist | Album
Files are saved as albums/artist--album.jpg (1200px) and manifest.json is updated.
Existing files are skipped; add --force to overwrite.
"""
import json, os, re, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(ROOT, "manifest.json")
FORCE = "--force" in sys.argv
ARGS = [a for a in sys.argv[1:] if a != "--force"]

def slug(s):
    for a, b in (("é","e"),("á","a"),("ó","o"),("ñ","n"),("í","i")): s = s.lower().replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "pop-covers/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def api(path, **params):
    return json.loads(get("https://itunes.apple.com/" + path + "?" + urllib.parse.urlencode(params)))["results"]

def art(x):
    return re.sub(r"/\d+x\d+bb\.", "/1200x1200bb.", x["artworkUrl100"])

def manifest():
    m = json.load(open(MAN)) if os.path.exists(MAN) else {}
    for k in ("albums", "artists", "unsorted"): m.setdefault(k, [])
    return m

def put(artist, album, url, m):
    rel = f"albums/{slug(artist)}--{slug(album)}.jpg"
    path = os.path.join(ROOT, rel)
    if os.path.exists(path) and not FORCE:
        print("skip (exists):", rel); return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(get(url))
    m["albums"] = [e for e in m["albums"] if e.get("file") != rel]
    m["albums"].append({"artist": artist, "album": album, "file": rel})
    print("saved:", rel)

def clean(s): return re.sub(r"\s*[-(\[].*(deluxe|edition|version|taylor|remaster).*$", "", s, flags=re.I).strip().lower()

def do_album(artist, album, m):
    r = api("search", term=f"{artist} {album}", entity="album", limit=50)
    r = [x for x in r if artist.lower() in x["artistName"].lower()]
    exact = [x for x in r if clean(x["collectionName"]) == album.lower()]
    if not exact:
        names = ", ".join(sorted({x["collectionName"] for x in r})[:6]) or "nothing"
        print(f"NO MATCH for {artist} | {album}  (iTunes had: {names})"); return
    exact.sort(key=lambda x: (x["collectionName"].lower() != album.lower(), len(x["collectionName"])))
    put(artist, album, art(exact[0]), m)

def base(n):
    n = re.sub(r"\s*[\(\[][^)\]]*(deluxe|edition|anniversary|expanded|bonus|platinum|collector|special|complete|remaster)[^)\]]*[\)\]]", "", n, flags=re.I)
    return re.sub(r"\s*-\s*(deluxe|special|expanded).*$", "", n, flags=re.I).strip()

def do_artist_albums(artist, m):
    a = api("search", term=artist, entity="musicArtist", limit=5)
    a = [x for x in a if x["artistName"].lower() == artist.lower()] or a
    if not a: print("artist not found:", artist); return
    groups = {}
    for x in api("lookup", id=a[0]["artistId"], entity="album", limit=200):
        if x.get("wrapperType") != "collection": continue
        n = x["collectionName"]
        if re.search(r"\s-\s(Single|EP)$", n) or x.get("trackCount", 99) < 5: continue
        groups.setdefault(base(n).lower(), []).append(x)
    for k, xs in groups.items():
        x = min(xs, key=lambda y: len(y["collectionName"]))
        put(a[0]["artistName"], base(x["collectionName"]), art(x), m)

def main():
    if not ARGS: print(__doc__); return
    cmd, rest = ARGS[0], ARGS[1:]; m = manifest()
    if cmd == "album" and len(rest) == 2: do_album(rest[0], rest[1], m)
    elif cmd == "artist-albums" and len(rest) == 1: do_artist_albums(rest[0], m)
    elif cmd == "list" and len(rest) == 1:
        for line in open(rest[0], encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "|" not in line: continue
            a, b = [s.strip() for s in line.split("|", 1)]; do_album(a, b, m)
    else: print(__doc__); return
    json.dump(m, open(MAN, "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__": main()
