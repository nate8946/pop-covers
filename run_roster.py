#!/usr/bin/env python3
"""Slow, resumable cover fetcher. Run from the repo folder:
  python3 run_roster.py wanted_roster.txt
Skips covers you already have, waits when Apple says 'too many requests', uses a looser title match,
and writes anything it can't find to roster_failed.txt."""
import sys, os, time, json, difflib, urllib.error
sys.argv = [sys.argv[0]] + sys.argv[1:]
import fetch_covers_itunes as fc

def safe_api(*a, **k):
    wait = 30
    for _ in range(8):
        try:
            return fc.api(*a, **k)
        except urllib.error.HTTPError as e:
            if e.code in (429, 403):
                print(f"   rate limited, waiting {wait}s ..."); time.sleep(wait); wait = min(wait * 2, 240)
            else:
                raise
        except Exception as e:
            print("   network error:", e); time.sleep(10)
    raise RuntimeError("gave up after repeated rate limits")

import re
def alnum(s):
    s = s.lower()
    for x, y in (("é","e"),("ø","o"),("ë","e"),("’","'")): s = s.replace(x, y)
    return re.sub(r"[^a-z0-9]+", "", s)
def norm(s): return alnum(fc.clean(s))
def same_artist(want, got):
    w, g = alnum(want), alnum(got)
    return bool(w) and (w in g or g in w)
def pick(r, album):
    r = [x for x in r if " - Single" not in x["collectionName"] and not x["collectionName"].endswith(" - EP") or alnum(x["collectionName"]).startswith(alnum(album))]
    if not r: return None
    want = alnum(album)
    exact = [x for x in r if norm(x["collectionName"]) == want or alnum(x["collectionName"]) == want]
    if exact: return sorted(exact, key=lambda x: len(x["collectionName"]))[0]
    best = max(r, key=lambda x: difflib.SequenceMatcher(None, norm(x["collectionName"]), want).ratio())
    if difflib.SequenceMatcher(None, norm(best["collectionName"]), want).ratio() >= 0.72: return best
    return None

def find(artist, album):
    # 1) plain searches (retry once if Apple returns nothing, which can mean it is throttling)
    for q in (f"{artist} {album}", album):
        for attempt in range(2):
            r = safe_api("search", term=q, entity="album", limit=50)
            if r: break
            time.sleep(8)
        r = [x for x in r if same_artist(artist, x["artistName"])]
        hit = pick(r, album)
        if hit: return hit
        time.sleep(2)
    # 2) look the artist up and scan their whole discography
    arts = safe_api("search", term=artist, entity="musicArtist", limit=5)
    arts = [x for x in arts if same_artist(artist, x["artistName"])] or arts[:1]
    if arts:
        r = safe_api("lookup", id=arts[0]["artistId"], entity="album", limit=200)
        r = [x for x in r if x.get("wrapperType") == "collection"]
        return pick(r, album)
    return None

def main():
    path = sys.argv[1]
    m = fc.manifest(); failed = []; n = 0
    lines = [l.strip() for l in open(path, encoding="utf-8") if "|" in l and not l.startswith("#")]
    for i, line in enumerate(lines, 1):
        a, b = [s.strip() for s in line.split("|", 1)]
        rel = f"albums/{fc.slug(a)}--{fc.slug(b)}.jpg"
        if os.path.exists(os.path.join(fc.ROOT, rel)):
            print(f"[{i}/{len(lines)}] have {rel}"); continue
        x = find(a, b)
        if x is None:
            print(f"[{i}/{len(lines)}] NO MATCH {a} | {b}"); failed.append(line)
        else:
            if fc.slug(x["collectionName"]) != fc.slug(b):
                print(f"   (using '{x['collectionName']}')")
            fc.put(a, b, fc.art(x), m)
        n += 1
        if n % 10 == 0: json.dump(m, open(fc.MAN, "w"), indent=1, ensure_ascii=False)
        time.sleep(3)
    json.dump(m, open(fc.MAN, "w"), indent=1, ensure_ascii=False)
    open(os.path.join(fc.ROOT, "roster_failed.txt"), "w").write("\n".join(failed) + "\n")
    print(f"\nDone. {len(failed)} not found -> roster_failed.txt")

main()
