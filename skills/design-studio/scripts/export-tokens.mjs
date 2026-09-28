#!/usr/bin/env node
// Export a React Native app's design tokens to CSS so HTML mockups render in
// the app's real colours, spacing, radii and type ramp.
//
// Usage:
//   node export-tokens.mjs --root <repo> --entry <tokens module> --out <dir/tokens.css>
//        [--alias @=src] [--light-overrides <file>:<flagExport>:<overridesExport>]
//
// The entry module should export any of: Colors { light, dark }, Spacing,
// Radius, Gap, IconSize, Shadows, Overlay, StatusColor, SeriesColor,
// TypeVariant. It bundles the entry with the project's own esbuild (the app
// must have esbuild in node_modules; Expo/Metro apps usually do), stubs
// react-native (tokens only touch Platform), and writes:
//   :root / [data-theme="dark"]  --c-<colorKey>   (from Colors.light / .dark)
//   --space-<k>  --radius-<role>  --shadow-<k>  --series-<n>
//   .t-<variant> classes          (from TypeVariant)
// Anything it can't find is skipped, not faked. A static palette the app
// spreads over Colors.light at runtime behind a flag can be applied with
// --light-overrides; logic-based theme changes are not, so a simulator
// screenshot still wins when they disagree.

import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";

const args = Object.fromEntries(
  process.argv.slice(2).reduce((acc, a, i, all) => {
    if (a.startsWith("--")) acc.push([a.slice(2), all[i + 1]]);
    return acc;
  }, []),
);
const root = path.resolve(args.root ?? process.cwd());
if (!args.entry) {
  console.error("usage: export-tokens.mjs --root <repo> --entry <path/to/tokens/index.ts> --out <tokens.css> [--alias @=src]");
  process.exit(2);
}
const entry = path.resolve(root, args.entry);
const [aliasKey, aliasDir] = (args.alias ?? "@=src").split("=");
const out = path.resolve(args.out ?? "tokens.css");

const require = createRequire(path.join(root, "package.json"));
let esbuild;
try {
  esbuild = require("esbuild");
} catch {
  console.error(`esbuild not found under ${root}/node_modules — write tokens.css by hand from the theme files.`);
  process.exit(2);
}

const exts = [".ts", ".tsx", ".js", "/index.ts", "/index.tsx", "/index.js", ""];
const resolveFile = (base) => exts.map((e) => base + e).find((p) => fs.existsSync(p) && fs.statSync(p).isFile());

async function load(file) {
const result = await esbuild.build({
  entryPoints: [file],
  bundle: true,
  write: false,
  format: "esm",
  platform: "node",
  logLevel: "silent",
  plugins: [
    {
      name: "tokens-env",
      setup(b) {
        b.onResolve({ filter: /^react-native$/ }, () => ({ path: "rn", namespace: "stub" }));
        b.onLoad({ filter: /.*/, namespace: "stub" }, () => ({
          contents: "export const Platform = { OS: 'ios', select: (o) => (o.ios ?? o.native ?? o.default) };",
          loader: "js",
        }));
        const prefix = new RegExp(`^${aliasKey.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}/`);
        b.onResolve({ filter: prefix }, (a) => {
          const p = resolveFile(path.join(root, aliasDir, a.path.slice(aliasKey.length + 1)));
          return p ? { path: p } : undefined;
        });
      },
    },
  ],
});

return import("data:text/javascript;base64," + Buffer.from(result.outputFiles[0].text).toString("base64"));
}

const t = { ...(await load(entry)) };

// Runtime light-palette overrides the static Colors export can't see.
// --light-overrides <file>:<flagExport>:<overridesExport>: applied when the
// flag export is truthy, the way the app's theme provider would at runtime.
const ovSpec = args["light-overrides"] ?? "";
const [ovFile, ovFlag, ovName] = ovSpec.split(":");
let overridesApplied = "";
if (ovFile && fs.existsSync(path.resolve(root, ovFile))) {
  const o = await load(path.resolve(root, ovFile));
  if (o[ovFlag] && o[ovName] && t.Colors?.light) {
    t.Colors = { ...t.Colors, light: { ...t.Colors.light, ...o[ovName] } };
    overridesApplied = `${ovName} (${ovFlag}=true)`;
  }
}

const kebab = (s) => String(s).replace(/([a-z0-9])([A-Z])/g, "$1-$2").replace(/[^a-zA-Z0-9-]/g, "-").toLowerCase();
const lines = [];
const light = [];
const dark = [];

if (t.Colors?.light) {
  for (const [k, v] of Object.entries(t.Colors.light)) if (typeof v === "string") light.push(`  --c-${kebab(k)}: ${v};`);
  for (const [k, v] of Object.entries(t.Colors.dark ?? {})) if (typeof v === "string") dark.push(`  --c-${kebab(k)}: ${v};`);
}
const statics = [];
for (const [k, v] of Object.entries(t.Spacing ?? {})) if (typeof v === "number") statics.push(`  --space-${kebab(k)}: ${v}px;`);
for (const [k, v] of Object.entries(t.Radius ?? {})) if (typeof v === "number") statics.push(`  --radius-${kebab(k)}: ${v}px;`);
for (const [k, v] of Object.entries(t.Gap ?? {})) if (typeof v === "number") statics.push(`  --gap-${kebab(k)}: ${v}px;`);
for (const [k, v] of Object.entries(t.IconSize ?? {})) if (typeof v === "number") statics.push(`  --icon-${kebab(k)}: ${v}px;`);
for (const [k, s] of Object.entries(t.Shadows ?? {})) {
  if (!s?.shadowOffset) continue;
  const a = s.shadowOpacity ?? 0.1;
  statics.push(`  --shadow-${kebab(k)}: 0 ${s.shadowOffset.height}px ${s.shadowRadius * 2}px rgba(0,0,0,${a});`);
}
for (const [group, ramp] of Object.entries(t.Overlay ?? {}))
  for (const [k, v] of Object.entries(ramp)) statics.push(`  --overlay-${kebab(group)}-${kebab(k)}: ${v};`);
for (const [k, v] of Object.entries(t.StatusColor ?? {})) statics.push(`  --status-${kebab(k)}: ${v};`);
(t.SeriesColor ?? []).forEach((c, i) => {
  light.push(`  --series-${i + 1}: ${c.light};`);
  dark.push(`  --series-${i + 1}: ${c.dark};`);
});

lines.push(`/* Generated by design-studio/export-tokens.mjs from ${path.relative(root, entry)}${overridesApplied ? ` + ${overridesApplied}` : ""} — ${new Date().toISOString().slice(0, 10)}. Do not hand-edit; re-run. */`);
lines.push(`:root {\n  --font-sans: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", system-ui, sans-serif;\n${statics.join("\n")}\n${light.join("\n")}\n}`);
if (dark.length) lines.push(`[data-theme="dark"] {\n${dark.join("\n")}\n}`);

for (const [k, v] of Object.entries(t.TypeVariant ?? {})) {
  if (!v?.fontSize) continue;
  const decl = [`font-size: ${v.fontSize}px`];
  if (v.lineHeight) decl.push(`line-height: ${v.lineHeight}px`);
  if (v.fontWeight) decl.push(`font-weight: ${v.fontWeight}`);
  if (v.letterSpacing != null) decl.push(`letter-spacing: ${v.letterSpacing}px`);
  if (v.fontVariant?.includes?.("tabular-nums")) decl.push("font-variant-numeric: tabular-nums");
  lines.push(`.t-${kebab(k)} { ${decl.join("; ")}; }`);
}

fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, lines.join("\n\n") + "\n");
const count = (lines.join("\n").match(/--|\.t-/g) ?? []).length;
console.log(`wrote ${out} (${count} tokens; colors light=${light.length} dark=${dark.length}, type=${Object.keys(t.TypeVariant ?? {}).length})${overridesApplied ? `; light overrides: ${overridesApplied}` : ""}`);
