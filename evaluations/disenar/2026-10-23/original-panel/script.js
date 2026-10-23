(() => {
  "use strict";

  const stages = [
    {
      title: "Preparar",
      description: "Alinea al grupo: define el objetivo, reúne los materiales y acuerda qué queréis conseguir al terminar.",
      outcome: "Un objetivo común y los materiales a mano.",
      question: "¿Qué queremos llevarnos de este taller?"
    },
    {
      title: "Explorar",
      description: "Escucha, pregunta y observa. Comparte referencias y reúne ideas antes de decidir qué camino seguir.",
      outcome: "Ideas agrupadas y un rumbo compartido.",
      question: "¿Qué posibilidades todavía no hemos considerado?"
    },
    {
      title: "Construir",
      description: "Convierte una idea en algo concreto. Crea un primer borrador, pruébalo y ajusta lo que haga falta.",
      outcome: "Una primera versión para poner a prueba.",
      question: "¿Qué podemos hacer tangible ahora?"
    },
    {
      title: "Compartir",
      description: "Presenta el trabajo, recoge lo aprendido y acuerda el siguiente paso para que el taller continúe fuera de la sala.",
      outcome: "Aprendizajes y próximos pasos claros.",
      question: "¿Qué aprendimos y qué haremos después?"
    }
  ];

  const STEP_MS = 6000;
  const byId = (id) => document.getElementById(id);
  const stageButtons = [...document.querySelectorAll("[data-stage]")];
  const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
  const playButton = byId("play-button");
  let current = 0;
  let mode = "idle";
  let timer = null;
  let remaining = STEP_MS;
  let deadline = 0;

  function clearTimer() {
    window.clearTimeout(timer);
    timer = null;
  }

  function announce(message) {
    byId("announcement").textContent = message;
  }

  function render() {
    const stage = stages[current];
    stageButtons.forEach((button, index) => {
      const selected = index === current;
      button.setAttribute("aria-pressed", String(selected));
      button.querySelector(".stage-state").textContent = selected ? "Estás aquí" : "Elegir etapa";
    });

    byId("stage-title").textContent = stage.title;
    byId("stage-description").textContent = stage.description;
    byId("stage-outcome").textContent = stage.outcome;
    byId("stage-question").textContent = stage.question;
    byId("stage-counter").textContent = `Etapa ${current + 1} de ${stages.length}`;
    byId("progress-value").textContent = `${Math.round(((current + 1) / stages.length) * 100)} %`;
    const progress = byId("workshop-progress");
    progress.value = current + 1;
    progress.textContent = `${current + 1} de ${stages.length}`;
    progress.setAttribute("aria-valuetext", `Etapa ${current + 1} de ${stages.length}: ${stage.title}`);

    const labels = {
      idle: ["Listo para empezar", "Reproducir"],
      manual: ["Etapa elegida", "Reproducir"],
      playing: ["Reproduciendo", "Pausar"],
      paused: ["En pausa", "Reanudar"],
      complete: ["Recorrido completo", "Repetir recorrido"]
    };
    byId("playback-state").textContent = labels[mode][0];
    byId("playback-state").dataset.playing = String(mode === "playing");
    byId("play-label").textContent = labels[mode][1];
    byId("play-icon").setAttribute("d", mode === "playing" ? "M6 5h4v14H6zm8 0h4v14h-4z" : "M8 5v14l11-7z");
    byId("motion-note").hidden = !motionPreference.matches;
  }

  function schedule() {
    clearTimer();
    deadline = performance.now() + remaining;
    timer = window.setTimeout(() => {
      timer = null;
      if (mode !== "playing") return;
      if (current < stages.length - 1) {
        current += 1;
        remaining = STEP_MS;
        render();
        announce(`Etapa ${current + 1} de ${stages.length}: ${stages[current].title}. ${stages[current].description}`);
        schedule();
      } else {
        mode = "complete";
        remaining = STEP_MS;
        render();
        announce("Recorrido completo. Puedes repetirlo o elegir cualquier etapa.");
      }
    }, remaining);
  }

  function pause(message = "Recorrido en pausa.") {
    if (mode !== "playing") return;
    remaining = Math.max(0, deadline - performance.now());
    clearTimer();
    mode = "paused";
    render();
    announce(`${message} Etapa ${current + 1} de ${stages.length}: ${stages[current].title}.`);
  }

  function play() {
    if (mode === "playing") return;
    if (mode === "complete") {
      current = 0;
      remaining = STEP_MS;
    }
    mode = "playing";
    render();
    announce(`Reproduciendo desde ${stages[current].title}. Puedes pausar en cualquier momento.`);
    schedule();
  }

  stageButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
      clearTimer();
      current = index;
      remaining = STEP_MS;
      mode = "manual";
      render();
      announce(`Etapa ${current + 1} de ${stages.length}: ${stages[current].title}. ${stages[current].description}`);
    });
  });

  playButton.addEventListener("click", () => mode === "playing" ? pause() : play());

  byId("reset-button").addEventListener("click", () => {
    clearTimer();
    current = 0;
    remaining = STEP_MS;
    mode = "idle";
    render();
    announce("Recorrido reiniciado. Etapa 1 de 4: Preparar. Pulsa Reproducir para empezar.");
  });

  motionPreference.addEventListener("change", () => {
    if (motionPreference.matches && mode === "playing") {
      pause("Recorrido en pausa al activar movimiento reducido.");
    } else {
      render();
    }
  });

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) pause("Recorrido en pausa al salir de esta pestaña.");
  });

  window.addEventListener("pagehide", () => pause("Recorrido en pausa al salir de la página."));
  render();
})();
