#!/usr/bin/env node
// Revisión automática de slides web con Playwright.
//
// Uso:
//   node revisar-slides.mjs --url <url del deck> [opciones]
//
// Opciones:
//   --slides 0-7 | 0,2,5   Fragmentos (#n) a revisar. Sin esta opción revisa la URL tal cual.
//   --selector <css>       Raíz de la slide activa. Por defecto: article[data-active="true"],
//                          [data-slide-active], [aria-current="slide"], article[data-slide];
//                          si no hay, <main> o <body>.
//   --viewports <lista>    Por defecto 1920x1080,1366x768. FALP: agrega 1024x600,390x844.
//   --out <dir>            Carpeta de evidencia. Por defecto evidencia/slides/<AAAA-MM-DD>.
//   --min-ratio <n>        Texto mínimo = alto del viewport / n. Por defecto 60 (18 px a 1080).
//                          En viewports verticales (móvil) el mínimo es 12 px.
//   --max-words <n>        Aviso sobre n palabras visibles por slide. Por defecto 60.
//   --sin-movimiento-reducido   Omite la pasada con prefers-reduced-motion.
//
// Salida: capturas por slide y viewport, una captura desenfocada por slide (prueba de entrecerrar los ojos),
// informe.json e informe.md. Código de salida 1 si hay errores, 2 si el script falló.
//
// Mide: tamaño mínimo de texto, contraste WCAG sobre fondos sólidos, desbordes y texto fuera del viewport,
// cercanía al borde, largo de línea estimado, tamaños de texto distintos, palabras visibles, familias
// tipográficas y animaciones (duración, propiedades, iteraciones, y con movimiento reducido).
// No mide: texto sobre imagen o degradado (lo marca «sin medir»), equilibrio, alineación óptica ni foco.

import { execSync } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";

const require = createRequire(import.meta.url);

function loadPlaywright() {
  const candidates = [process.cwd(), path.dirname(new URL(import.meta.url).pathname)];
  for (const base of candidates) {
    try {
      return createRequire(path.join(base, "noop.js"))("playwright");
    } catch {}
  }
  try {
    const globalRoot = execSync("npm root -g", { encoding: "utf8" }).trim();
    return require(path.join(globalRoot, "playwright"));
  } catch {}
  throw new Error("No se encontró playwright (local ni global). Instálalo o usa el global del entorno.");
}

function parseArgs(argv) {
  const args = {
    url: null,
    slides: null,
    selector: 'article[data-active="true"], [data-slide-active], [aria-current="slide"], article[data-slide]',
    viewports: "1920x1080,1366x768",
    out: path.join("evidencia", "slides", new Date().toISOString().slice(0, 10)),
    minRatio: 60,
    maxWords: 60,
    reducedMotion: true,
  };
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    const next = () => argv[++i];
    if (key === "--url") args.url = next();
    else if (key === "--slides") args.slides = parseSlides(next());
    else if (key === "--selector") args.selector = next();
    else if (key === "--viewports") args.viewports = next();
    else if (key === "--out") args.out = next();
    else if (key === "--min-ratio") args.minRatio = Number(next());
    else if (key === "--max-words") args.maxWords = Number(next());
    else if (key === "--sin-movimiento-reducido") args.reducedMotion = false;
    else if (key === "--help" || key === "-h") {
      console.log("Uso: node revisar-slides.mjs --url <url> [--slides 0-7] [--viewports 1920x1080,1366x768] [--out dir]");
      process.exit(0);
    } else throw new Error(`Opción desconocida: ${key}`);
  }
  if (!args.url) throw new Error("Falta --url");
  args.viewports = args.viewports.split(",").map((v) => {
    const [width, height] = v.trim().split("x").map(Number);
    if (!width || !height) throw new Error(`Viewport inválido: ${v}`);
    return { width, height };
  });
  return args;
}

function parseSlides(spec) {
  const out = [];
  for (const part of spec.split(",")) {
    const [a, b] = part.split("-").map((s) => Number(s.trim()));
    if (Number.isNaN(a)) throw new Error(`--slides inválido: ${spec}`);
    if (b === undefined || Number.isNaN(b)) out.push(a);
    else for (let n = a; n <= b; n++) out.push(n);
  }
  return out;
}

// Se ejecuta en el navegador. Devuelve las animaciones activas bajo la raíz de la slide.
function collectAnimations(selector) {
  // Prueba cada selector en orden y toma el primer elemento visible (las slides inactivas suelen estar ocultas).
  const findRoot = (list) => {
    for (const part of list.split(",")) {
      for (const el of document.querySelectorAll(part.trim())) {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0 && getComputedStyle(el).visibility !== "hidden") return el;
      }
    }
    return null;
  };
  const root = findRoot(selector) ?? document.querySelector("main") ?? document.body;
  const describe = (el) => {
    if (!(el instanceof Element)) return "?";
    const cls = [...el.classList].slice(0, 2).join(".");
    return el.tagName.toLowerCase() + (cls ? `.${cls}` : "");
  };
  return root.getAnimations({ subtree: true }).map((anim) => {
    const effect = anim.effect;
    const timing = effect?.getComputedTiming?.() ?? {};
    let properties = [];
    if (anim.transitionProperty) properties = [anim.transitionProperty];
    else if (effect?.getKeyframes) {
      const props = new Set();
      for (const frame of effect.getKeyframes()) {
        for (const key of Object.keys(frame)) {
          if (!["offset", "computedOffset", "easing", "composite"].includes(key)) props.add(key);
        }
      }
      properties = [...props];
    }
    const transformValues = [];
    if (effect?.getKeyframes) {
      for (const frame of effect.getKeyframes()) {
        for (const key of ["transform", "translate", "scale", "rotate"]) {
          if (frame[key] && frame[key] !== "none") transformValues.push(`${key}: ${frame[key]}`);
        }
      }
    }
    return {
      name: anim.animationName ?? anim.transitionProperty ?? "animación",
      target: describe(effect?.target),
      duration: typeof timing.duration === "number" ? Math.round(timing.duration) : null,
      delay: Math.round(timing.delay ?? 0),
      iterations: timing.iterations === Infinity ? "infinite" : timing.iterations,
      properties,
      transformValues,
    };
  });
}

// Se ejecuta en el navegador. Mide la slide activa ya asentada.
function measureSlide({ selector, minRatio }) {
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  // Prueba cada selector en orden y toma el primer elemento visible (las slides inactivas suelen estar ocultas).
  const findRoot = (list) => {
    for (const part of list.split(",")) {
      for (const el of document.querySelectorAll(part.trim())) {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0 && getComputedStyle(el).visibility !== "hidden") return el;
      }
    }
    return null;
  };
  const found = findRoot(selector);
  const root = found ?? document.querySelector("main") ?? document.body;
  const usedFallbackRoot = !found;

  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 1;
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  const toRgba = (css) => {
    ctx.clearRect(0, 0, 1, 1);
    ctx.fillStyle = "rgba(0,0,0,0)";
    ctx.fillStyle = css;
    ctx.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;
    return { r, g, b, a: a / 255 };
  };
  const over = (top, bottom) => {
    const a = top.a + bottom.a * (1 - top.a);
    if (a === 0) return { r: 0, g: 0, b: 0, a: 0 };
    const mix = (k) => (top[k] * top.a + bottom[k] * bottom.a * (1 - top.a)) / a;
    return { r: mix("r"), g: mix("g"), b: mix("b"), a };
  };
  const luminance = ({ r, g, b }) => {
    const lin = (v) => {
      const c = v / 255;
      return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
    };
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  };
  const ratio = (a, b) => {
    const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
    return (hi + 0.05) / (lo + 0.05);
  };
  const hex = ({ r, g, b }) => "#" + [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, "0")).join("");

  // Fondo efectivo: compone fondos semitransparentes hasta uno opaco. Un degradado sin imágenes se
  // evalúa en cada parada de color (vale la peor); una imagen deja el contraste sin medir.
  const backgroundOf = (el) => {
    const layers = [];
    for (let node = el; node && node.nodeType === 1; node = node.parentElement) {
      const style = getComputedStyle(node);
      const image = style.backgroundImage;
      if (image && image !== "none") {
        if (/url\(|image-set\(|element\(/.test(image)) return { unmeasured: "imagen de fondo" };
        const stops = image.match(/(rgba?|hsla?|oklch|oklab|lab|lch|color)\([^()]*\)|#[0-9a-f]{3,8}\b|\btransparent\b/gi) ?? [];
        if (!stops.length) return { unmeasured: "degradado sin colores legibles" };
        layers.push(stops.map(toRgba));
        if (stops.every((s) => toRgba(s).a >= 0.999)) break;
        continue;
      }
      const color = toRgba(style.backgroundColor);
      if (color.a > 0) {
        layers.push([color]);
        if (color.a >= 0.999) break;
      }
    }
    let results = [{ r: 255, g: 255, b: 255, a: 1 }];
    for (let i = layers.length - 1; i >= 0; i--) {
      results = results.flatMap((below) => layers[i].map((layer) => over(layer, below)));
    }
    return { colors: results };
  };
  const opacityOf = (el) => {
    let value = 1;
    for (let node = el; node && node.nodeType === 1; node = node.parentElement) value *= Number(getComputedStyle(node).opacity);
    return value;
  };
  const describe = (el) => {
    const cls = [...el.classList].slice(0, 2).join(".");
    return el.tagName.toLowerCase() + (cls ? `.${cls}` : "");
  };
  const isVisible = (el) => {
    if (el.closest('[aria-hidden="true"]') && el.closest('[aria-hidden="true"]') !== root.closest('[aria-hidden="true"]')) return false;
    // Contenido de un <details> cerrado: no se ve hasta que alguien lo abre.
    const closed = el.closest("details:not([open])");
    if (closed && !el.closest("summary")) return false;
    const style = getComputedStyle(el);
    if (style.visibility === "hidden" || style.display === "none") return false;
    const rect = el.getBoundingClientRect();
    // Texto solo para lectores de pantalla (patrón sr-only: caja de ~1 px o recortada).
    if (rect.width <= 2 || rect.height <= 2) return false;
    for (let node = el; node && node.nodeType === 1; node = node.parentElement) {
      const s = getComputedStyle(node);
      if (s.position === "absolute" && (s.clip === "rect(0px, 0px, 0px, 0px)" || s.clipPath === "inset(50%)")) return false;
    }
    return opacityOf(el) > 0.05;
  };

  // En vertical (móvil) no se proyecta: se usa el piso de lectura en pantalla de 12 px.
  const minFont = vh > vw ? 12 : vh / minRatio;
  const textElements = new Map();
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    const text = node.textContent.replace(/\s+/g, " ").trim();
    if (!text) continue;
    const el = node.parentElement;
    if (!el || !isVisible(el)) continue;
    const entry = textElements.get(el) ?? { text: "" };
    entry.text = `${entry.text} ${text}`.trim();
    textElements.set(el, entry);
  }

  const findings = [];
  const add = (level, rule, message, extra = {}) => findings.push({ level, rule, message, ...extra });
  const sizes = new Set();
  const families = new Set();
  let words = 0;
  let worstContrast = null;

  for (const [el, { text }] of textElements) {
    const style = getComputedStyle(el);
    const size = parseFloat(style.fontSize);
    const weight = Number(style.fontWeight) || 400;
    sizes.add(Math.round(size));
    families.add(style.fontFamily.split(",")[0].replace(/["']/g, "").trim());
    words += text.split(/\s+/).filter((w) => /[\p{L}\p{N}]/u.test(w)).length;
    const sample = text.length > 60 ? `${text.slice(0, 57)}…` : text;

    if (size < minFont - 0.01) {
      add("error", "S3", `Texto de ${size.toFixed(1)} px bajo el mínimo de ${minFont.toFixed(1)} px`, { element: describe(el), text: sample });
    }

    // WCAG 1.4.3 exceptúa los controles deshabilitados.
    const disabled = el.closest(':disabled, [aria-disabled="true"]');
    const bg = disabled ? { skip: true } : backgroundOf(el);
    if (bg.skip) {
      // sin requisito de contraste
    } else if (bg.unmeasured) {
      add("sin-medir", "S4", `Contraste sin medir: ${bg.unmeasured}`, { element: describe(el), text: sample });
    } else {
      const fg = toRgba(style.color);
      fg.a *= opacityOf(el);
      let worst = null;
      for (const color of bg.colors) {
        const effective = over(fg, color);
        const value = ratio(effective, color);
        if (!worst || value < worst.value) worst = { value, effective, color };
      }
      const { value, effective } = worst;
      bg.color = worst.color;
      const large = size >= 24 || (size >= 18.66 && weight >= 700);
      const required = large ? 3 : 4.5;
      if (!worstContrast || value < worstContrast.ratio) worstContrast = { ratio: Number(value.toFixed(2)), element: describe(el), text: sample };
      const detail = { element: describe(el), text: sample, fg: hex(effective), bg: hex(bg.color), ratio: Number(value.toFixed(2)) };
      if (value < required) add("error", "S4", `Contraste ${value.toFixed(2)}:1 bajo el mínimo WCAG de ${required}:1`, detail);
      else if (value < 7 && !large) add("aviso", "S4", `Contraste ${value.toFixed(2)}:1 cumple WCAG pero queda bajo el objetivo de 7:1 para proyección`, detail);
      else if (value < 4.5 && large) add("aviso", "S4", `Texto grande con ${value.toFixed(2)}:1: cumple WCAG pero queda bajo el objetivo de 4,5:1 para proyección`, detail);
    }

    const display = style.display;
    if (["block", "list-item"].includes(display) && /^(p|li|dd|blockquote|figcaption|span|div)$/i.test(el.tagName)) {
      const rect = el.getBoundingClientRect();
      const lineHeight = style.lineHeight === "normal" ? size * 1.2 : parseFloat(style.lineHeight);
      const lines = Math.max(1, Math.round(rect.height / lineHeight));
      if (lines >= 2) {
        const perLine = Math.round(text.length / lines);
        if (perLine > 65) add("aviso", "S7", `≈${perLine} caracteres por línea (cuerpo de slide: 35–60)`, { element: describe(el), text: sample });
      }
    }

    const rect = el.getBoundingClientRect();
    if (rect.right > vw + 1 || rect.bottom > vh + 1 || rect.left < -1 || rect.top < -1) {
      add("error", "S8", "Texto fuera del viewport", { element: describe(el), text: sample });
    } else if (rect.left < vw * 0.03 || vw - rect.right < vw * 0.03) {
      add("aviso", "S8", "Texto a menos del 3 % del borde lateral", { element: describe(el), text: sample });
    }
    if (el.scrollWidth > el.clientWidth + 1 && ["hidden", "clip"].includes(style.overflowX)) {
      add("error", "S8", "Texto recortado horizontalmente", { element: describe(el), text: sample });
    }
  }

  if (root.scrollHeight > root.clientHeight + 2 && root !== document.body) {
    add("aviso", "S8", `La slide desborda verticalmente (${root.scrollHeight} px de contenido en ${root.clientHeight} px)`);
  }
  if (document.documentElement.scrollWidth > vw + 1) add("error", "S8", "La página tiene scroll horizontal");
  if (sizes.size > 4) add("aviso", "S5", `${sizes.size} tamaños de texto distintos (${[...sizes].sort((a, b) => b - a).join(", ")} px); máximo recomendado 3 + etiqueta`);
  if (textElements.size === 0) add("sin-medir", "S6", "No se encontró texto visible");

  return {
    viewport: `${vw}x${vh}`,
    root: usedFallbackRoot ? `${describe(root)} (selector no encontrado)` : describe(root),
    words,
    sizes: [...sizes].sort((a, b) => b - a),
    families: [...families],
    worstContrast,
    findings,
  };
}

function judgeAnimations(animations, { reduced }) {
  const findings = [];
  for (const anim of animations) {
    const label = `${anim.name} en ${anim.target}`;
    if (anim.iterations === "infinite") findings.push({ level: "error", rule: "M2", message: `Animación infinita: ${label}` });
    const total = (anim.duration ?? 0) + anim.delay;
    if (total > 400) findings.push({ level: "aviso", rule: "M2", message: `${label} dura ${total} ms (duración + retraso > 400 ms)` });
    const other = anim.properties.filter((p) => !["opacity", "transform", "translate", "scale", "rotate", "color", "background-color", "border-color", "fill", "stroke", "outline-color", "backgroundColor", "borderColor", "outlineColor"].includes(p));
    if (other.length) findings.push({ level: "aviso", rule: "M1", message: `${label} anima ${other.join(", ")} (preferir opacity y transform)` });
    if (anim.properties.includes("all")) findings.push({ level: "error", rule: "M1", message: `${label} usa transition: all` });
    if (reduced && anim.transformValues.length) {
      findings.push({ level: "error", rule: "M3", message: `Con movimiento reducido ${label} aún desplaza o escala (${anim.transformValues[0]})` });
    }
  }
  return findings;
}

async function settle(page, selector) {
  await page.evaluate(async (sel) => {
    const finite = document.getAnimations().filter((a) => a.effect?.getComputedTiming?.().iterations !== Infinity);
    await Promise.race([Promise.all(finite.map((a) => a.finished.catch(() => {}))), new Promise((r) => setTimeout(r, 2000))]);
    await document.fonts?.ready;
  }, selector);
  await page.waitForTimeout(80);
}

async function visit(page, url, slide, first) {
  if (slide === null) {
    await page.goto(url, { waitUntil: "networkidle" });
    return;
  }
  const target = `${url.split("#")[0]}#${slide}`;
  if (first) await page.goto(target, { waitUntil: "networkidle" });
  else await page.evaluate((hash) => { window.location.hash = hash; }, String(slide));
  await page.waitForTimeout(40);
}

function toMarkdown(report) {
  const lines = [`# Revisión de slides`, "", `- URL: ${report.url}`, `- Fecha: ${report.date}`, `- Viewports: ${report.viewports.join(", ")}`, `- Familias tipográficas en el deck: ${report.families.join(", ") || "—"}`, ""];
  const totals = { error: 0, aviso: 0, "sin-medir": 0 };
  for (const slide of report.slides) for (const f of slide.allFindings) totals[f.level]++;
  lines.push(`**Resumen**: ${totals.error} errores · ${totals.aviso} avisos · ${totals["sin-medir"]} sin medir`, "");
  if (report.families.length > 2) lines.push(`> Aviso D3: ${report.families.length} familias tipográficas (máximo 2 + mono).`, "");
  for (const slide of report.slides) {
    lines.push(`## Slide ${slide.slide ?? "(URL)"}`, "");
    for (const m of slide.measures) {
      const worst = m.worstContrast ? `${m.worstContrast.ratio}:1 («${m.worstContrast.text}»)` : "—";
      lines.push(`- ${m.viewport}: ${m.words} palabras · tamaños ${m.sizes.join("/")} px · peor contraste ${worst} · raíz ${m.root}`);
    }
    if (slide.animations.length) {
      lines.push(`- Animaciones: ${slide.animations.map((a) => `${a.name} (${a.duration} ms${a.delay ? ` + ${a.delay}` : ""}; ${a.properties.join(", ")})`).join("; ")}`);
    }
    if (!slide.allFindings.length) lines.push("", "Sin hallazgos.");
    else {
      // Agrupa hallazgos idénticos (misma regla, viewport y mensaje) y muestra hasta tres ejemplos.
      const groups = new Map();
      for (const f of slide.allFindings) {
        const key = `${f.level}|${f.rule}|${f.viewport}|${f.message}`;
        const group = groups.get(key) ?? { ...f, count: 0, examples: [] };
        group.count++;
        if (f.element && group.examples.length < 3) group.examples.push(`\`${f.element}\`${f.text ? ` «${f.text.replace(/\|/g, "/")}»` : ""}`);
        groups.set(key, group);
      }
      const order = { error: 0, aviso: 1, "sin-medir": 2 };
      const sorted = [...groups.values()].sort((a, b) => order[a.level] - order[b.level] || a.rule.localeCompare(b.rule));
      lines.push("", "| Nivel | Regla | Viewport | Hallazgo | Casos | Ejemplos |", "|---|---|---|---|---|---|");
      for (const g of sorted) lines.push(`| ${g.level} | ${g.rule} | ${g.viewport ?? "—"} | ${g.message} | ${g.count} | ${g.examples.join("<br>")} |`);
    }
    lines.push("");
  }
  return lines.join("\n");
}

async function main() {
  const args = parseArgs(process.argv);
  const { chromium } = loadPlaywright();
  await mkdir(args.out, { recursive: true });
  const browser = await chromium.launch();
  const slides = args.slides ?? [null];
  const report = { url: args.url, date: new Date().toISOString(), viewports: args.viewports.map((v) => `${v.width}x${v.height}`), slides: [], families: [] };
  const families = new Set();
  const bySlide = new Map(slides.map((s) => [s, { slide: s, measures: [], animations: [], allFindings: [] }]));

  for (const [index, viewport] of args.viewports.entries()) {
    const context = await browser.newContext({ viewport, deviceScaleFactor: 1 });
    const page = await context.newPage();
    let first = true;
    for (const slide of slides) {
      await visit(page, args.url, slide, first);
      first = false;
      const entry = bySlide.get(slide);
      if (index === 0) {
        const animations = await page.evaluate(collectAnimations, args.selector);
        entry.animations = animations;
        entry.allFindings.push(...judgeAnimations(animations, { reduced: false }).map((f) => ({ ...f, viewport: report.viewports[0] })));
      }
      await settle(page, args.selector);
      const measure = await page.evaluate(measureSlide, { selector: args.selector, minRatio: args.minRatio });
      measure.families.forEach((f) => families.add(f));
      if (measure.words > args.maxWords) measure.findings.push({ level: "aviso", rule: "S6", message: `${measure.words} palabras visibles (aviso sobre ${args.maxWords})` });
      entry.measures.push(measure);
      entry.allFindings.push(...measure.findings.map((f) => ({ ...f, viewport: measure.viewport })));
      const name = `${slide === null ? "pagina" : `slide-${String(slide).padStart(2, "0")}`}--${viewport.width}x${viewport.height}`;
      await page.screenshot({ path: path.join(args.out, `${name}.png`) });
      if (index === 0) {
        await page.addStyleTag({ content: "html { filter: blur(8px) !important; }" }).then((h) => page.screenshot({ path: path.join(args.out, `${name}--entrecerrar.png`) }).then(() => h.evaluate((n) => n.remove())));
      }
    }
    await context.close();
  }

  if (args.reducedMotion) {
    const context = await browser.newContext({ viewport: args.viewports[0], reducedMotion: "reduce" });
    const page = await context.newPage();
    let first = true;
    for (const slide of slides) {
      await visit(page, args.url, slide, first);
      first = false;
      const animations = await page.evaluate(collectAnimations, args.selector);
      const entry = bySlide.get(slide);
      const findings = judgeAnimations(animations, { reduced: true }).filter((f) => f.rule === "M3");
      if (!animations.some((a) => a.properties.includes("opacity")) && entry.animations.length) {
        findings.push({ level: "aviso", rule: "M3", message: "Con movimiento reducido no queda ningún fundido: el cambio de slide no se percibe" });
      }
      entry.allFindings.push(...findings.map((f) => ({ ...f, viewport: `${report.viewports[0]} reduce` })));
    }
    await context.close();
  }

  await browser.close();
  report.families = [...families];
  report.slides = [...bySlide.values()];
  await writeFile(path.join(args.out, "informe.json"), JSON.stringify(report, null, 2));
  const markdown = toMarkdown(report);
  await writeFile(path.join(args.out, "informe.md"), markdown);
  const errors = report.slides.reduce((n, s) => n + s.allFindings.filter((f) => f.level === "error").length, 0);
  const warnings = report.slides.reduce((n, s) => n + s.allFindings.filter((f) => f.level === "aviso").length, 0);
  console.log(`Revisadas ${slides.length} slide(s) × ${args.viewports.length} viewport(s): ${errors} errores, ${warnings} avisos.`);
  console.log(`Informe: ${path.join(args.out, "informe.md")}`);
  process.exit(errors ? 1 : 0);
}

main().catch((error) => {
  console.error(error.message ?? error);
  process.exit(2);
});
