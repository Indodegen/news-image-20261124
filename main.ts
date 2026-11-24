// news-image-20261124 entry (Node 22, standard library only).
//
// The entry image sits beside this file as entry.png, and this program
// copies it to /output/entry.png. The image is a 1024x1024 newspaper
// front page summing up the world news of Tuesday 24 November 2026; it
// was drawn by generate.py (Pillow + Liberation fonts, deterministic,
// no network, no timestamps) from that day's wires, and running the
// generator twice writes byte-identical PNGs. The gate takes a whole
// PNG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees
// exactly the bytes copied here.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url),
  join(outDir, 'entry.png'));
