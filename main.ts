import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The World in One Image — 18 November 2026.
// The image is drawn by render.py and shipped in this repository;
// this program only copies it into the grader's output directory.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error(`entry.png not found next to main.ts: ${src}`);
}
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
// The grader runs this program twice and both runs must write the same
// bytes, so verify the copy landed whole before reporting success.
const srcSize = statSync(src).size;
const destSize = statSync(dest).size;
if (destSize !== srcSize) {
  throw new Error(
    `entry.png copy incomplete: ${destSize} bytes, expected ${srcSize}`,
  );
}
console.log(`wrote ${dest} (${destSize} bytes)`);
