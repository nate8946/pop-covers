import sys, os, re, json, urllib.parse, urllib.request

OUT = "artists"
os.makedirs(OUT, exist_ok=True)

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=20).read()

def fetch(name, force=False):
    path = f"{OUT}/{slug(name)}.jpg"
    if os.path.exists(path) and not force:
        print("have:", path); return
    q = urllib.parse.quote(name)
    data = json.loads(get(f"https://api.deezer.com/search/artist?q={q}&limit=10"))
    hits = [a for a in data.get("data", []) if a["name"].lower() == name.lower()]
    if not hits:
        print("NO MATCH:", name); return
    best = max(hits, key=lambda a: a.get("nb_fan", 0))
    img = best.get("picture_xl") or best.get("picture_big")
    if not img or "/images/artist//" in img:
        print("NO PHOTO:", name); return
    open(path, "wb").write(get(img))
    print("saved:", path)

force = "--force" in sys.argv
names = [a for a in sys.argv[1:] if a != "--force"]
if names and names[0] == "list":
    names = [l.strip() for l in open(names[1]) if l.strip()]
for n in names:
    fetch(n, force)
