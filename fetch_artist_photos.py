#!/usr/bin/env python3
"""Fetch one Deezer artist photo per name in ladies.txt (or another file given as arg).
Run from the repo folder:  python3 fetch_artist_photos.py ladies.txt
Saves to deezer_photos/<slug>.jpg (skips ones already there or already in artists/),
writes deezer_report.txt (name -> matched Deezer name, fans, FUZZY flag) and deezer_failed.txt."""
import sys, os, re, json, time, unicodedata, urllib.request, urllib.parse, urllib.error

src = sys.argv[1] if len(sys.argv) > 1 else "ladies.txt"
OUT = "deezer_photos"; os.makedirs(OUT, exist_ok=True)

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", s)

def get(url, binary=False):
    wait = 10
    for _ in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = r.read()
                return d if binary else json.loads(d)
        except urllib.error.HTTPError as e:
            if e.code in (429, 403, 500, 502, 503):
                print(f"   waiting {wait}s ({e.code})"); time.sleep(wait); wait = min(wait * 2, 120)
            else:
                return None
        except Exception as e:
            print("   network error:", e); time.sleep(5)
    return None

names = [l.strip() for l in open(src, encoding="utf-8") if l.strip() and not l.startswith("#")]
rep, failed = [], []
for i, n in enumerate(names, 1):
    s = slug(n)
    if os.path.exists(f"{OUT}/{s}.jpg") or os.path.exists(f"artists/{s}.jpg"):
        print(f"[{i}/{len(names)}] {n}: have it"); continue
    j = get("https://api.deezer.com/search/artist?limit=10&q=" + urllib.parse.quote(n))
    res = (j or {}).get("data") or []
    if not res:
        print(f"[{i}/{len(names)}] {n}: NOT FOUND"); failed.append(n); continue
    exact = [x for x in res if norm(x["name"]) == norm(n)]
    pick = max(exact, key=lambda x: x.get("nb_fan", 0)) if exact else res[0]
    flag = "" if exact else "FUZZY"
    url = pick.get("picture_xl") or pick.get("picture_big")
    img = get(url, binary=True) if url else None
    if not img or len(img) < 5000:
        print(f"[{i}/{len(names)}] {n}: no image"); failed.append(n); continue
    open(f"{OUT}/{s}.jpg", "wb").write(img)
    rep.append(f"{n} | {pick['name']} | fans {pick.get('nb_fan',0)} | {flag}")
    print(f"[{i}/{len(names)}] {n} -> {pick['name']} {flag}")
    time.sleep(0.4)
open("deezer_report.txt", "a", encoding="utf-8").write("\n".join(rep) + "\n")
open("deezer_failed.txt", "w", encoding="utf-8").write("\n".join(failed) + "\n")
print(f"Done. {len(rep)} saved, {len(failed)} not found -> deezer_failed.txt")
