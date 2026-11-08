"use strict";

// Verifica la lógica real con un DOM mínimo y tiempo simulado; no es un navegador.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const test = require("node:test");
const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
const css = fs.readFileSync(path.join(__dirname, "styles.css"), "utf8");
const source = fs.readFileSync(path.join(__dirname, "script.js"), "utf8");

function element() {
  const listeners = new Map();
  const attributes = new Map();
  return {
    textContent: "",
    hidden: false,
    value: 0,
    dataset: {},
    setAttribute: (name, value) => attributes.set(name, value),
    getAttribute: (name) => attributes.get(name),
    addEventListener(name, callback) {
      if (!listeners.has(name)) listeners.set(name, []);
      listeners.get(name).push(callback);
    },
    emit(name) { for (const callback of listeners.get(name) || []) callback(); }
  };
}

function app(reducedMotion = false) {
  const elements = new Map([...html.matchAll(/\bid="([^"]+)"/g)].map((match) => [match[1], element()]));
  const buttons = [...html.matchAll(/<button\b[^>]*\bdata-stage="(\d+)"/g)].map(() => {
    const button = element();
    const state = element();
    button.querySelector = (selector) => selector === ".stage-state" ? state : null;
    return button;
  });
  let now = 0;
  let nextId = 1;
  const timers = new Map();
  const motion = Object.assign(element(), { matches: reducedMotion });
  const document = Object.assign(element(), {
    hidden: false,
    getElementById: (id) => elements.get(id) || null,
    querySelectorAll: (selector) => selector === "[data-stage]" ? buttons : []
  });
  const window = Object.assign(element(), {
    matchMedia(query) {
      assert.equal(query, "(prefers-reduced-motion: reduce)");
      return motion;
    },
    setTimeout(callback, delay) {
      const id = nextId++;
      timers.set(id, { at: now + Math.max(0, delay), callback });
      return id;
    },
    clearTimeout(id) { timers.delete(id); }
  });

  vm.runInNewContext(source, { document, window, performance: { now: () => now } }, { filename: "script.js" });
  return {
    el: (id) => elements.get(id),
    buttons,
    timers,
    click: (id) => elements.get(id).emit("click"),
    select: (index) => buttons[index].emit("click"),
    title: () => elements.get("stage-title").textContent,
    tick(ms) {
      const target = now + ms;
      let iterations = 0;
      while (true) {
        const next = [...timers].sort((a, b) => a[1].at - b[1].at)[0];
        if (!next || next[1].at > target) break;
        assert.ok(++iterations < 100, "Sin bucles de temporizadores");
        timers.delete(next[0]);
        now = next[1].at;
        next[1].callback();
      }
      now = target;
    },
    reduced(value) { motion.matches = value; motion.emit("change"); },
    hidden(value) { document.hidden = value; document.emit("visibilitychange"); },
    pagehide() { window.emit("pagehide"); }
  };
}

test("Fuentes locales, cuatro selectores nativos y nombres de etapa requeridos", () => {
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]);
  assert.equal(new Set(ids).size, ids.length);
  assert.match(html, /<html lang="es">/);
  assert.equal([...html.matchAll(/\bdata-stage="[0-3]"/g)].length, 4);
  for (const stage of ["Preparar", "Explorar", "Construir", "Compartir"]) assert.ok(html.includes(stage));
  for (const match of html.matchAll(/\b(?:src|href)="([^"]+)"/g)) {
    assert.ok(!/^(https?:|\/\/|data:)/.test(match[1]));
    assert.ok(fs.existsSync(path.join(__dirname, match[1])));
  }
  for (const match of html.matchAll(/<button\b[^>]*>/g)) assert.ok(match[0].includes('type="button"'));
  assert.ok(!/\bfetch\s*\(|\bimport\s*\(|@import|url\(/.test(source + css));
  assert.match(css, /@media\s*\(prefers-reduced-motion:\s*reduce\)/);
  assert.match(css, /transition:\s*none\s*!important/);
});

test("Inicio estático y selección directa de las cuatro etapas", () => {
  const a = app();
  assert.equal(a.title(), "Preparar");
  assert.equal(a.el("workshop-progress").value, 1);
  assert.equal(a.timers.size, 0);
  for (const index of [3, 0, 2, 1]) {
    a.select(index);
    assert.equal(a.title(), ["Preparar", "Explorar", "Construir", "Compartir"][index]);
    assert.equal(a.el("workshop-progress").value, index + 1);
    assert.equal(a.el("progress-value").textContent, `${(index + 1) * 25} %`);
    assert.equal(a.buttons.filter((b) => b.getAttribute("aria-pressed") === "true").length, 1);
    assert.equal(a.buttons[index].getAttribute("aria-pressed"), "true");
    assert.ok(a.el("stage-description").textContent.length > 40);
    assert.equal(a.timers.size, 0);
  }
});

test("Secuencia completa: 6 s por etapa, final estable y repetición", () => {
  const a = app();
  a.click("play-button");
  assert.equal(a.timers.size, 1);
  assert.equal(a.el("play-label").textContent, "Pausar");
  for (const title of ["Explorar", "Construir", "Compartir"]) {
    a.tick(5999);
    assert.notEqual(a.title(), title);
    a.tick(1);
    assert.equal(a.title(), title);
    assert.equal(a.timers.size, 1);
  }
  a.tick(6000);
  assert.equal(a.el("playback-state").textContent, "Recorrido completo");
  assert.equal(a.timers.size, 0);
  a.tick(60000);
  assert.equal(a.title(), "Compartir");
  a.click("play-button");
  assert.equal(a.title(), "Preparar");
  assert.equal(a.timers.size, 1);
});

test("Pausa conserva exactamente los 3.8 s restantes de la etapa", () => {
  const a = app();
  a.click("play-button");
  a.tick(2200);
  a.click("play-button");
  assert.equal(a.el("play-label").textContent, "Reanudar");
  assert.equal(a.timers.size, 0);
  a.tick(10000);
  assert.equal(a.title(), "Preparar");
  a.click("play-button");
  a.tick(3799);
  assert.equal(a.title(), "Preparar");
  a.tick(1);
  assert.equal(a.title(), "Explorar");
});

test("Reinicio cancela cambios tardíos y restaura posición inicial", () => {
  const a = app();
  a.click("play-button");
  a.tick(7500);
  a.click("reset-button");
  a.tick(30000);
  assert.equal(a.title(), "Preparar");
  assert.equal(a.timers.size, 0);
  assert.equal(a.el("play-label").textContent, "Reproducir");
  assert.equal(a.el("progress-value").textContent, "25 %");
});

test("Elegir una etapa durante la reproducción detiene y cancela el temporizador anterior", () => {
  const a = app();
  a.click("play-button");
  a.tick(5500);
  a.select(2);
  a.tick(20000);
  assert.equal(a.title(), "Construir");
  assert.equal(a.timers.size, 0);
  a.click("play-button");
  a.tick(6000);
  assert.equal(a.title(), "Compartir");
  a.tick(6000);
  assert.equal(a.el("playback-state").textContent, "Recorrido completo");
});

test("Movimiento reducido inicial permite reproducción explícita y se anuncia en pantalla", () => {
  const a = app(true);
  assert.equal(a.el("motion-note").hidden, false);
  assert.equal(a.timers.size, 0);
  a.click("play-button");
  a.tick(6000);
  assert.equal(a.title(), "Explorar");
});

test("Cambiar movimiento reducido durante la secuencia pausa sin perder el estado", () => {
  const a = app();
  a.click("play-button");
  a.tick(2000);
  a.reduced(true);
  assert.equal(a.el("motion-note").hidden, false);
  assert.equal(a.el("play-label").textContent, "Reanudar");
  assert.equal(a.timers.size, 0);
  a.tick(9000);
  a.reduced(false);
  assert.equal(a.el("motion-note").hidden, true);
  assert.equal(a.timers.size, 0);
  a.click("play-button");
  a.tick(4000);
  assert.equal(a.title(), "Explorar");
});

test("Ocultar la pestaña y salir de la página pausan; volver no inicia reproducción", () => {
  const a = app();
  a.click("play-button");
  a.tick(1000);
  a.hidden(true);
  a.tick(15000);
  a.hidden(false);
  assert.equal(a.title(), "Preparar");
  assert.equal(a.timers.size, 0);
  a.click("play-button");
  a.tick(5000);
  assert.equal(a.title(), "Explorar");
  a.pagehide();
  assert.equal(a.timers.size, 0);
  assert.equal(a.el("play-label").textContent, "Reanudar");
});

test("Activaciones rápidas no generan más de un temporizador", () => {
  const a = app();
  for (let i = 0; i < 31; i++) {
    a.click("play-button");
    assert.ok(a.timers.size <= 1);
  }
  a.tick(6000);
  assert.equal(a.title(), "Explorar");
  a.select(3);
  a.select(1);
  a.click("reset-button");
  assert.equal(a.timers.size, 0);
  assert.equal(a.title(), "Preparar");
});
