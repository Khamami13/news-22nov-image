// News-image entry for the 22 November 2026 front page (Node 22, stdlib only).
//
// The page itself is pre-rendered by tools/generate_image.py into entry.png
// (a deterministic Pillow drawing of the day's world news). All this program
// does is deliver that exact PNG to the grader's output directory, byte for
// byte — it draws nothing and fetches nothing.
//
// Run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # -> out/entry.png

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// The PNG sitting next to this file is the entry.
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');

// The grader sets MAKEFUN_OUTPUT_DIR; outside its container it defaults
// to /output, matching the usual convention.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
