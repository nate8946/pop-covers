#!/usr/bin/env python3
"""Check that every album in a list of matchups has a cover in albums/.

Run from the repo folder:   python3 check_pairs.py pairs.txt
pairs.txt, one matchup per line (artist - album, then vs, then artist - album):
    Taylor Swift - 1989 vs Beyoncé - Lemonade
    Sabrina Carpenter - Short n' Sweet vs Olivia Rodrigo - GUTS
Prints which covers are found, which are missing, and writes missing.txt,
which you can feed straight to:  python3 fetch_covers_itunes.py list missing.txt
"""
import difflib, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ALB = os.path.join(ROOT, "albums")

def slug(s):
    for a, b in (("é","e"),("á","a"),("ó","o"),("ñ","n"),("í","i"),("ü","u")): s = s.lower().replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

have = {f[:-4]: f for f in os.listdir(ALB) if f.endswith(".jpg")} if os.path.isdir(ALB) else {}

def find(artist, album):
    key = f"{slug(artist)}--{slug(album)}"
    if key in have: return have[key], "exact"
    near = [k for k in have if k.startswith(slug(artist) + "--")]
    close = difflib.get_close_matches(key, near, n=1, cutoff=0.82)
    if close: return have[close[0]], f"close match to {close[0]}"
    return None, None

def parse(line):
    sides = re.split(r"\s+vs\.?\s+", line.strip(), flags=re.I)
    out = []
    for s in sides:
        if " - " not in s and "|" not in s: return None
        a, b = re.split(r"\s+-\s+|\s*\|\s*", s, maxsplit=1)
        out.append((a.strip(), b.strip()))
    return out

def main():
    if len(sys.argv) < 2: print(__doc__); return
    missing, seen, total = [], set(), 0
    for n, line in enumerate(open(sys.argv[1], encoding="utf-8"), 1):
        line = line.strip()
        if not line or line.startswith("#"): continue
        sides = parse(line)
        if not sides: print(f"line {n}: can't read '{line}' (use: Artist - Album vs Artist - Album)"); continue
        for a, b in sides:
            if (a, b) in seen: continue
            seen.add((a, b)); total += 1
            f, how = find(a, b)
            if f: print(f"  ok      {a} - {b}" + ("" if how == "exact" else f"   [{how}]"))
            else: print(f"  MISSING {a} - {b}"); missing.append((a, b))
    print(f"\n{total - len(missing)} of {total} albums have covers.")
    if missing:
        with open(os.path.join(ROOT, "missing.txt"), "w", encoding="utf-8") as fh:
            fh.write("# Artist | Album\n" + "\n".join(f"{a} | {b}" for a, b in missing) + "\n")
        print("Wrote missing.txt. Fetch them with:\n  python3 fetch_covers_itunes.py list missing.txt")

main()
