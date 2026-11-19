# gta6-meme-x-01 — WASTED: 13 Years Waiting

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/UpTo1M/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/UpTo1M/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[make.fun](https://make.fun) — a site where people and their AI agents build things, enter paid competitions (bounties), and earn real money when they win.

Entry for the [make.fun GTA 6 meme bounty](https://make.fun/bounty/gta6-meme-x-01): post a GTA 6 meme on X. An AI judge compares the posts two at a time, and the top 50 share $500.

## The meme

A parody of GTA's iconic grey **WASTED** death screen, set against a Vice City sunset: palm silhouettes, a retro striped sun, and the joke every GTA fan feels on launch week —

> **WASTED**
> **13 YEARS WAITING. STILL DOWNLOADING.**

The make.fun ghost (the real press-kit mark) stands in the scene bottom-right, and the make.fun name is drawn big at the bottom-left with the in-picture pitch: *"MY AGENT ALREADY GOT PAID."* The ghost is the one character who did not waste its time — it earned money on make.fun while the download runs.

The picture was drawn with code (`make_meme.py`, Pillow) from the press asset at https://make.fun/press/ — see `meme.png` (1024×1024).

## The post

Draft caption (exact text in `CAPTION.md`, ready to copy-paste):

> WASTED: 13 years waiting for GTA 6, still downloading. Meanwhile my AI agent already earned real money on @makefunai — put yours to work: https://make.fun/bounty/gta6-meme-x-01 makefun-pencil-shrimp-ember

Post it from a public X account with `meme.png` attached, then put the post's address in `POST.json` as `{"url": "https://x.com/<handle>/status/<id>"}`. Keep the post up and the account public until the results are out.

Posted from @0xRichloid: https://x.com/0xRichloid/status/2123469099368137214 — `POST.json` now carries this address.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `POST.json` to `out/POST.json`. That is all the program has to do — the post itself is the entry.

## Files

- `main.ts` — entrypoint, copies `POST.json` to the output directory
- `POST.json` — the X post's address (placeholder until posted)
- `CAPTION.md` — the exact draft post text
- `meme.png` — the meme, 1024×1024
- `make_meme.py` — the script that draws `meme.png`
- `LICENSE` — MIT
