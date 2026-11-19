// gta6-meme-x-01 entrypoint. Node 22, standard library only.
//
// The entry is the X post itself: the meme, its picture and its text, is
// what the house reads and the judge ranks. This program does nothing to
// the post; it only hands the house the post's address, by copying
// POST.json from the repository root into the output directory, where the
// gate reads it.
//
// It uses no network, no wall clock and no files outside the repository,
// so two runs over the same repository write the same bytes.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

// Until the meme is posted, POST.json holds the starter's placeholder
// address; the copy still succeeds, and the gate refuses the placeholder
// until it is replaced with the real post's address.
const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

try {
  copyFileSync(source, target);
} catch (error) {
  console.error(
    `could not copy ${source} to ${target}: ${(error as Error).message}`,
  );
  process.exit(1);
}
