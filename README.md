# pop-covers

Cover art for @PopByNumbers posts.

- `albums/` named `artist--album.jpg` (identified albums)
- `artists/` one cover per artist, album not yet identified
- `unsorted/` covers not yet matched to an artist or album (numbered)
- `manifest.json` lists every file with its artist and album

Rename or move files from `unsorted/` as you identify them, and update `manifest.json`.

Direct link pattern once pushed:
`https://raw.githubusercontent.com/<user>/pop-covers/main/albums/taylor-swift--1989.jpg`

## Adding new covers from Spotify

`fetch_covers.py` downloads covers straight from Spotify (needs a free developer app, steps at the top of the file; Python only, no installs).

    python fetch_covers.py album "Taylor Swift" "Midnights"
    python fetch_covers.py artist-albums "Sabrina Carpenter"
    python fetch_covers.py artist-photo "Rihanna"
    python fetch_covers.py list wanted.txt
