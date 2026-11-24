// The World in One Day — Tuesday, 24 November 2026
// make.fun bounty: news-image-20261124
// "Sum up 24 November's world news in one image"
//
// Copies the generated entry.png (drawn by generate.py) into the output
// directory the harness provides. Node 22, standard library only.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
console.log(`Copied entry.png to ${outDir}`);
