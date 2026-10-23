#!/usr/bin/env node
// Export a cover HTML at full + thumbnail size and check layout.
// Usage: node shoot_cover.cjs <cover.html> <outDir> [landscape|portrait|square] [name]
// The page is laid out at CSS size (1920×1080 / 1080×1920 / 1080×1080) and shot at a device scale
// that gives the full size; the thumbnail is a downscale of that shot.
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

function findPlaywright() {
  try { return require.resolve("playwright"); } catch (e) {}
  const base = path.join(process.env.HOME, ".npm/_npx");
  if (fs.existsSync(base)) {
    for (const d of fs.readdirSync(base)) {
      const p = path.join(base, d, "node_modules/playwright/index.js");
      if (fs.existsSync(p)) return p;
    }
  }
  throw new Error("playwright not found; run `npx playwright --version` once to cache it");
}

const SIZES = {
  landscape: { css: [1920, 1080], full: [2560, 1440], thumb: [1280, 720] },
  portrait: { css: [1080, 1920], full: [1440, 2560], thumb: [720, 1280] },
  square: { css: [1080, 1080], full: [2160, 2160], thumb: [1080, 1080] },
};

(async () => {
  const [html, outDir = ".", mode = "landscape", name = "cover"] = process.argv.slice(2);
  if (!html) { console.error("usage: shoot_cover.cjs <cover.html> <outDir> [landscape|portrait|square] [name]"); process.exit(2); }
  const S = SIZES[mode];
  if (!S) { console.error("mode must be landscape, portrait or square"); process.exit(2); }
  const { chromium } = require(findPlaywright());
  let browser;
  try { browser = await chromium.launch({ channel: "chrome" }); } catch (e) { browser = await chromium.launch(); }
  const page = await browser.newPage({ viewport: { width: S.css[0], height: S.css[1] }, deviceScaleFactor: S.full[0] / S.css[0] });
  await page.goto("file://" + path.resolve(html), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);

  const report = await page.evaluate(([W, H]) => {
    const blocks = [...document.querySelectorAll("[data-block]")].map((el) => {
      const r = el.getBoundingClientRect();
      return { name: el.dataset.block, allow: el.hasAttribute("data-allow-overlap"), l: r.left, t: r.top, r: r.right, b: r.bottom, el };
    });
    const issues = [];
    for (let i = 0; i < blocks.length; i++) {
      const a = blocks[i];
      if (a.l < 0 || a.t < 0 || a.r > W || a.b > H) {
        if (!a.allow) issues.push(`OUT OF CANVAS: ${a.name}`);
      }
      for (let j = i + 1; j < blocks.length; j++) {
        const b = blocks[j];
        if (a.allow || b.allow) continue;
        const ox = Math.min(a.r, b.r) - Math.max(a.l, b.l), oy = Math.min(a.b, b.b) - Math.max(a.t, b.t);
        if (ox > 1 && oy > 1) issues.push(`OVERLAP: ${a.name} × ${b.name} (${Math.round(ox)}×${Math.round(oy)}px)`);
      }
      // children wider than their block (e.g. nowrap text past a rule)
      for (const c of a.el.querySelectorAll("*:not(br)")) {
        const cr = c.getBoundingClientRect();
        if (cr.right > a.r + 1) issues.push(`OVERFLOW: ${a.name} child <${c.tagName.toLowerCase()} class="${c.className}"> ends at ${Math.round(cr.right)}, block ends at ${Math.round(a.r)}`);
      }
      if (a.el.scrollWidth > a.el.clientWidth + 1 && getComputedStyle(a.el).overflow !== "visible") issues.push(`CLIPPED: ${a.name}`);
    }
    const lines = blocks.map((x) => `${x.name.padEnd(8)} ${Math.round(x.l)},${Math.round(x.t)} → ${Math.round(x.r)},${Math.round(x.b)}`);
    return { lines, issues };
  }, S.css);

  fs.mkdirSync(outDir, { recursive: true });
  const full = path.join(outDir, `${name}-${S.full[0]}x${S.full[1]}.png`);
  const thumb = path.join(outDir, `${name}-${S.thumb[0]}x${S.thumb[1]}.png`);
  await page.screenshot({ path: full });
  await browser.close();
  execSync(`sips -z ${S.thumb[1]} ${S.thumb[0]} "${full}" --out "${thumb}"`, { stdio: "ignore" });

  console.log("Blocks (CSS px):\n  " + report.lines.join("\n  "));
  console.log(report.issues.length ? "Issues:\n  " + report.issues.join("\n  ") : "Check: no overlap, overflow or out-of-canvas blocks");
  console.log("Wrote\n  " + full + "\n  " + thumb);
  process.exit(report.issues.length ? 1 : 0);
})();
