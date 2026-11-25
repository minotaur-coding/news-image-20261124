import * as fs from "node:fs";
import * as path from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
fs.mkdirSync(outDir, { recursive: true });
const src = path.join(import.meta.dirname ?? __dirname, "entry.png");
const dst = path.join(outDir, "entry.png");
fs.copyFileSync(src, dst);
console.log("copied", src, "->", dst, fs.statSync(dst).size, "bytes");
