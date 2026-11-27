// news-image-20261126: copies the front-page image drawn for Thursday
// 26 November 2026 into the grader's output directory as entry.png.
// Node 22, standard library only, no network, no dependencies. The
// output is byte-for-byte the entry.png committed beside this file,
// so repeated runs agree.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const bytes = readFileSync(join(here, 'entry.png'));
mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
writeFileSync(target, bytes);

// Confirm the copy landed intact: what we wrote must match the source.
const written = readFileSync(target);
if (!written.equals(bytes)) {
  throw new Error('entry.png copy mismatch');
}
