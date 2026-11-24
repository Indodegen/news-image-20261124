# The World in One Day — 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Indodegen/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Indodegen/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A 1024×1024 newspaper front page summing up the world news of **Tuesday 24 November 2026** — 40 stories from 6 regions, drawn entirely in code.

## The leads

1. **Nvidia** — Jensen Huang is reinstated as chief executive after Trump intervenes; Asian stocks soar (Seoul +6%, Nikkei +3.9%, Taiwan +9%).
2. **Myanmar** — Fourteen countries affirm the ICJ ruling that Myanmar committed genocide against the Rohingya; the UK sanctions Myanmar generals; Malaysia moves to return Rohingya refugees.
3. **COP31** — The climate talks in Antalya collapse without a deal after ~50 hours of overtime; 90+ nations rejected a draft that never said "fossil fuels".

Plus 10 featured stories (the Merkury sinking off Libya, Medvedev's nuclear warning, Estonia's border warning, strikes in Ukraine, Gaza, US measles, the $41bn Sanofi–Insmed deal, the Grok lawsuits, the Solomon Islands, and Iran/Hormuz) and 27 more in a numbered list — with a **DATE CHECK** box naming what was left out because it belongs to an earlier day (the COP31 collapse itself, late 23 Nov; the ICJ ruling, 19 Nov; the Merkury sinking, 23 Nov; Russian missiles in Poland, 20 Nov; the Democrats' midterm majorities, 3 Nov).

## How it works

`generate.py` draws the whole front page with Pillow and Liberation fonts: masthead, stats strip, region bar, 3 lead cards, 10 featured cards, a world dot-map, the 27-story list, and the date-check box. Every scene is drawn from flat PIL shapes — no photos, no AI images, no network, no randomness, no timestamps. Running it twice writes a byte-identical PNG.

`main.ts` (Node 22, standard library only) copies `entry.png` beside it to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`), resolving the path via `import.meta.url` so it works from any working directory.

## Run it

```sh
python3 generate.py entry.png   # draw the front page
node main.ts                     # copy it to /output/entry.png
```

## Sources

Reuters · AP · CNN · Le Monde · Al Jazeera · France24

## License

MIT — see [LICENSE](LICENSE).
