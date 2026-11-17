/* ==========================================================================
   Teltech Networks, S.A. — Shared behaviour (all pages), v2
   Intro, navigation, kinetic type, reveals, counters, horizontal track,
   marquee, hover physics, page transitions and forms. No dependencies.
   ========================================================================== */
(() => {
  "use strict";

  const root = document.documentElement;
  const reduceMQ = window.matchMedia("(prefers-reduced-motion: reduce)");
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  const motionOK = () => !reduceMQ.matches;
  const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);

  root.classList.add("ready");
  if (!motionOK()) root.classList.remove("motion");

  /* ---------- Hero entrance (kinetic headline + sequenced copy) ---------- */
  function startHeroSequence() {
    document.querySelectorAll(".kin[data-kin-auto], .hero").forEach((el) => el.classList.add("is-in"));
  }

  /* ---------- Intro: logo assembles once per session ---------- */
  const introDone = () => {
    root.classList.remove("intro-on", "intro-play", "intro-out");
    try { sessionStorage.setItem("ttn-intro", "1"); } catch (e) { /* storage unavailable */ }
    document.dispatchEvent(new CustomEvent("ttn:intro-done"));
    startHeroSequence();
  };
  if (root.classList.contains("intro-on")) {
    if (!motionOK()) introDone();
    else {
      root.classList.add("intro-play");
      setTimeout(() => root.classList.add("intro-out"), 1500);
      setTimeout(introDone, 2300);
    }
  } else {
    requestAnimationFrame(startHeroSequence);
  }

  /* ---------- Header: scrolled state + mobile menu ---------- */
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  const panel = document.getElementById("nav-panel");
  const desktopMQ = window.matchMedia("(min-width: 1200px)");
  const onScrollHeader = () => header && header.classList.toggle("is-scrolled", window.scrollY > 24);
  window.addEventListener("scroll", onScrollHeader, { passive: true });
  onScrollHeader();

  const setMenu = (open) => {
    if (!header || !toggle) return;
    header.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
    document.body.style.overflow = open ? "hidden" : "";
    if (open) { const first = panel.querySelector("a"); if (first) first.focus(); }
  };
  if (toggle && panel) {
    toggle.addEventListener("click", () => setMenu(toggle.getAttribute("aria-expanded") !== "true"));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && header.classList.contains("is-open")) { setMenu(false); toggle.focus(); }
      if (e.key === "Tab" && header.classList.contains("is-open") && !desktopMQ.matches) {
        const items = [toggle, ...panel.querySelectorAll("a, button")];
        const first = items[0], last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    panel.addEventListener("click", (e) => { if (e.target.closest("a")) setMenu(false); });
    desktopMQ.addEventListener("change", () => setMenu(false));
  }

  /* ---------- Kinetic lines: index each line for staggering ---------- */
  document.querySelectorAll(".kin").forEach((el) => {
    el.querySelectorAll(".kin-line").forEach((line, i) => line.style.setProperty("--l", i));
  });

  /* ---------- Scroll reveals ---------- */
  const revealTargets = document.querySelectorAll("[data-reveal], [data-stagger], .fiber, .kin:not([data-kin-auto])");
  document.querySelectorAll("[data-stagger]").forEach((g) => Array.from(g.children).forEach((c, i) => c.style.setProperty("--i", i)));
  if ("IntersectionObserver" in window && motionOK()) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealTargets.forEach((el) => io.observe(el));
  } else {
    revealTargets.forEach((el) => el.classList.add("is-in"));
    document.querySelectorAll(".kin").forEach((el) => el.classList.add("is-in"));
  }

  /* ---------- Ticker (cycling specialty in the hero) ---------- */
  document.querySelectorAll(".ticker__list").forEach((list) => {
    const items = list.children.length;
    if (items < 2 || !motionOK()) return;
    let i = 0;
    setInterval(() => {
      if (document.hidden) return;
      i = (i + 1) % items;
      list.style.transform = `translateY(${-i * 1.3}em)`;
    }, 2200);
  });

  /* ---------- Count-up numbers ---------- */
  const counters = document.querySelectorAll("[data-count]");
  const runCount = (el) => {
    const end = Number(el.dataset.count);
    const from = Number(el.dataset.from || 0);
    if (!motionOK()) { el.textContent = String(end); return; }
    const t0 = performance.now(), dur = 1600;
    const step = (now) => {
      const k = clamp((now - t0) / dur);
      const e = 1 - Math.pow(1 - k, 3);
      el.textContent = String(Math.round(from + (end - from) * e));
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if ("IntersectionObserver" in window) {
    const cio = new IntersectionObserver((entries) => entries.forEach((en) => { if (en.isIntersecting) { runCount(en.target); cio.unobserve(en.target); } }), { threshold: 0.6 });
    counters.forEach((c) => cio.observe(c));
  } else counters.forEach(runCount);

  /* ---------- Horizontal pinned track ("Ecosistema") ---------- */
  document.querySelectorAll("[data-htrack]").forEach((track) => {
    const rail = track.querySelector(".htrack__rail");
    const bar = track.querySelector(".htrack__bar span");
    const current = track.querySelector("[data-htrack-current]");
    const panels = Array.from(rail.children);
    const pinMQ = window.matchMedia("(min-width: 900px)");
    let distance = 0, ticking = false, active = false;

    const setStatic = (on) => {
      track.classList.toggle("is-static", on);
      track.style.height = "";
      rail.style.transform = "";
    };
    const measure = () => {
      if (!pinMQ.matches || !motionOK()) { setStatic(true); return; }
      setStatic(false);
      distance = Math.max(0, rail.scrollWidth - window.innerWidth);
      track.style.height = `${window.innerHeight + distance}px`;
      update();
    };
    const update = () => {
      ticking = false;
      if (track.classList.contains("is-static")) return;
      const r = track.getBoundingClientRect();
      const p = clamp(-r.top / Math.max(1, r.height - window.innerHeight));
      rail.style.transform = `translate3d(${-distance * p}px,0,0)`;
      if (bar) bar.style.transform = `scaleX(${p})`;
      if (current) current.textContent = String(Math.min(panels.length, Math.floor(p * panels.length) + 1)).padStart(2, "0");
    };
    const onScroll = () => { if (active && !ticking) { ticking = true; requestAnimationFrame(update); } };
    if ("IntersectionObserver" in window) new IntersectionObserver(([e]) => { active = e.isIntersecting; onScroll(); }, { rootMargin: "10% 0px" }).observe(track);
    else active = true;
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", measure);
    pinMQ.addEventListener("change", measure);
    reduceMQ.addEventListener("change", measure);
    // Keyboard users: bring a focused panel into view by scrolling vertically.
    rail.addEventListener("focusin", (e) => {
      if (track.classList.contains("is-static")) return;
      const i = panels.findIndex((p) => p.contains(e.target));
      if (i < 0) return;
      const top = track.getBoundingClientRect().top + window.scrollY;
      const target = top + (distance * (panels[i].offsetLeft - parseFloat(getComputedStyle(rail).paddingLeft))) / Math.max(1, rail.scrollWidth - window.innerWidth);
      window.scrollTo({ top: target, behavior: "auto" });
    });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    measure();
  });

  /* ---------- Marquee: duplicate content for a seamless loop ---------- */
  document.querySelectorAll(".marquee").forEach((m) => {
    const track = m.querySelector(".marquee__track");
    if (!motionOK()) { m.classList.add("is-static"); return; }
    Array.from(track.children).forEach((item) => {
      const clone = item.cloneNode(true);
      clone.setAttribute("aria-hidden", "true");
      clone.querySelectorAll("a, button").forEach((a) => a.setAttribute("tabindex", "-1"));
      clone.querySelectorAll("img").forEach((img) => img.setAttribute("alt", ""));
      track.appendChild(clone);
    });
  });

  /* ---------- Hover physics: tilt cards + magnetic CTAs ---------- */
  if (finePointer.matches && motionOK()) {
    document.querySelectorAll(".tilt").forEach((card) => {
      let frame = 0;
      card.addEventListener("pointermove", (e) => {
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(() => {
          const r = card.getBoundingClientRect();
          const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
          card.style.transform = `perspective(900px) rotateX(${(0.5 - y) * 6}deg) rotateY(${(x - 0.5) * 8}deg)`;
          card.style.setProperty("--gx", `${e.clientX - r.left}px`);
          card.style.setProperty("--gy", `${e.clientY - r.top}px`);
        });
      });
      card.addEventListener("pointerleave", () => { cancelAnimationFrame(frame); card.style.transform = ""; });
    });
    document.querySelectorAll(".magnetic").forEach((btn) => {
      btn.addEventListener("pointermove", (e) => {
        const r = btn.getBoundingClientRect();
        btn.style.transform = `translate(${((e.clientX - (r.left + r.width / 2)) / r.width) * 12}px, ${((e.clientY - (r.top + r.height / 2)) / r.height) * 10}px)`;
      });
      btn.addEventListener("pointerleave", () => { btn.style.transform = ""; });
    });
  }

  /* ---------- Page transitions ---------- */
  const nativeVT = "CSSViewTransitionRule" in window && location.protocol !== "file:";
  if (!nativeVT && motionOK()) {
    const veil = document.createElement("div");
    veil.className = "page-veil"; veil.setAttribute("aria-hidden", "true");
    document.body.appendChild(veil);
    document.addEventListener("click", (e) => {
      const a = e.target.closest("a[href]");
      if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      if ((a.target && a.target !== "_self") || a.hasAttribute("download")) return;
      if (/^(mailto|tel):/.test(a.getAttribute("href"))) return;
      const url = new URL(a.href, location.href);
      if (url.protocol !== location.protocol || url.host !== location.host) return;
      if (url.pathname === location.pathname && url.search === location.search) return;
      e.preventDefault();
      root.classList.add("is-leaving");
      setTimeout(() => { location.href = url.href; }, 260);
    });
    window.addEventListener("pageshow", (e) => { if (e.persisted) root.classList.remove("is-leaving"); });
  }

  /* ---------- Soluciones: highlight the chip of the section in view ---------- */
  const solIndex = document.querySelector(".sol-index");
  if (solIndex && "IntersectionObserver" in window) {
    const chips = new Map(Array.from(solIndex.querySelectorAll("a")).map((a) => [a.hash.slice(1), a]));
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        chips.forEach((a) => { a.classList.remove("is-active"); a.removeAttribute("aria-current"); });
        const act = chips.get(en.target.id);
        if (act) {
          act.classList.add("is-active"); act.setAttribute("aria-current", "true");
          act.closest("ul").scrollTo({ left: act.offsetLeft - 16, behavior: motionOK() ? "smooth" : "auto" });
        }
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    document.querySelectorAll(".sol[id]").forEach((s) => spy.observe(s));
  }

  /* ---------- Forms: validation + success state (no backend) ---------- */
  const messages = {
    valueMissing: "Este campo es obligatorio.",
    typeMismatch: "Revisa el formato de este dato.",
    patternMismatch: "Revisa el formato de este dato.",
    tooShort: "Agrega un poco más de detalle.",
    rangeUnderflow: "Elige una fecha a partir de hoy.",
  };
  const fieldMessage = (el) => {
    for (const key of Object.keys(messages)) {
      if (el.validity[key]) return el.dataset[`msg${key[0].toUpperCase()}${key.slice(1)}`] || messages[key];
    }
    return "";
  };
  const showError = (el) => {
    const box = document.getElementById(`${el.dataset.errorId || el.id}-error`);
    const msg = el.checkValidity() ? "" : fieldMessage(el);
    el.setAttribute("aria-invalid", msg ? "true" : "false");
    if (box) box.textContent = msg;
    return !msg;
  };
  const today = new Date();
  const iso = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  document.querySelectorAll('input[type="date"][data-min-today]').forEach((d) => { d.min = iso; });
  const preset = new URLSearchParams(location.search).get("servicio");
  if (preset) {
    document.querySelectorAll('select[name="servicio"]').forEach((sel) => {
      if (Array.from(sel.options).some((o) => o.value === preset)) sel.value = preset;
    });
  }
  document.querySelectorAll("form[data-form]").forEach((form) => {
    const fields = Array.from(form.querySelectorAll("input, select, textarea")).filter((el) => el.id && !el.closest(".hp"));
    fields.forEach((el) => {
      el.addEventListener("blur", () => { if (el.value && el.type !== "radio" || el.getAttribute("aria-invalid") === "true") showError(el); });
      el.addEventListener("input", () => { if (el.getAttribute("aria-invalid") === "true") showError(el); });
      el.addEventListener("change", () => {
        if (el.type === "radio") form.querySelectorAll(`input[name="${el.name}"]`).forEach(showError);
        else if (el.getAttribute("aria-invalid") === "true") showError(el);
      });
    });
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const status = form.querySelector(".form__status");
      const results = fields.map(showError);
      const firstBad = fields[results.indexOf(false)];
      if (firstBad) { if (status) status.textContent = "Revisa los campos marcados antes de enviar."; firstBad.focus(); return; }
      if (status) status.textContent = "";
      const trap = form.querySelector(".hp input");
      const data = Object.fromEntries(new FormData(form).entries());
      if (trap && trap.value) return;
      // TODO: send `data` to the endpoint in data-endpoint once the client confirms the backend.
      // e.g. fetch(form.dataset.endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) })
      void data;
      const success = document.getElementById(form.dataset.success);
      form.reset();
      fields.forEach((el) => el.removeAttribute("aria-invalid"));
      if (success) { form.hidden = true; success.hidden = false; success.setAttribute("tabindex", "-1"); success.focus(); }
    });
  });
  document.querySelectorAll("[data-form-reset]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const success = btn.closest(".form-success");
      const form = document.querySelector(`form[data-success="${success.id}"]`);
      success.hidden = true; form.hidden = false;
      const first = form.querySelector("input:not([type=hidden]):not([tabindex='-1']), select, textarea");
      if (first) first.focus();
    });
  });

  document.querySelectorAll("[data-year]").forEach((el) => { el.textContent = String(new Date().getFullYear()); });
})();
