# The World in One Day — Tuesday, 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Indodegen/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Indodegen/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A single 1024×1024 newspaper front page that sums up 24 November 2026 world
news in one image: 40 stories from 6 regions, drawn with Python Pillow.

Lead stories: Nvidia reinstates Jensen Huang as chief executive after Trump
intervenes and Asian chip stocks soar; fourteen nations affirm the ICJ
genocide ruling against Myanmar; and the COP31 climate talks in Antalya
collapse without a deal after some 50 hours of overtime.

Below the leads, ten featured stories and 27 more one-line stories cover
Ukraine, Gaza, measles in the US, Sanofi's $41bn Insmed deal, the Solomon
Islands' China pact, and more — plus a dot-map of the world and a "Date
Check" box that keeps earlier days' news (the 19 Nov ICJ ruling, the
23 Nov COP31 collapse and Merkury sinking) clearly dated.

## How it works

`generate.py` draws the whole front page deterministically — no network,
no randomness, no timestamps, so two runs produce byte-identical PNGs.
`main.ts` copies the finished `entry.png` into the output directory.

## Run it

```bash
python3 generate.py entry.png
MAKEFUN_OUTPUT_DIR=/output node main.ts
```

## Sources

Reuters, AP, CNN, Al Jazeera, France24, Le Monde and other wires that
carried these stories on Tuesday 24 November 2026.

## License

MIT — see [LICENSE](LICENSE).
