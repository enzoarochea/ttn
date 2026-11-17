/* ==========================================================================
   Teltech Networks, S.A. — Isometric scroll stories (vertical pages), v2
   While the visitor scrolls through a [data-story] section, a CSS-3D scene
   assembles itself: fibre routes draw (scaleX), towers and buildings rise
   (scale), layers separate (translateZ), labels appear (opacity) and the
   whole world slowly turns (rotateZ). Only transforms and opacity change.
   With reduced motion the scene is rendered complete and not sticky.
   ========================================================================== */
(() => {
  "use strict";

  const stories = document.querySelectorAll("[data-story]");
  if (!stories.length) return;
  const reduceMQ = window.matchMedia("(prefers-reduced-motion: reduce)");
  const SPAN = 0.12;
  const clamp = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
  const ease = (t) => 1 - Math.pow(1 - clamp(t), 3);

  const setup = (story) => {
    const world = story.querySelector(".iso-world");
    const q = (sel) => Array.from(story.querySelectorAll(sel)).map((el) => ({ el, t: Number(el.dataset.t) || 0, i: Number(el.dataset.i) || 0 }));
    const edges = q(".st-e"), nodes = q(".st-n"), grow = q(".st-p, .st-b"), waves = q(".st-w"), tags = q(".st-tag"), layers = q(".st-l"), beams = q(".st-beam");
    const caps = Array.from(story.querySelectorAll("[data-cap]")).map((el) => ({ el, t: Number(el.dataset.cap) || 0 }));
    const bar = story.querySelector(".story__progress span");
    const BASE_GAP = Number(story.dataset.gap || 58);

    const render = (p) => {
      if (world) world.style.setProperty("--rz", `${-42 + p * 22}deg`);
      for (const e of edges) e.el.style.transform = `scaleX(${clamp((p - e.t) / SPAN)})`;
      for (const n of nodes) { const k = clamp((p - n.t) / 0.05); n.el.style.opacity = String(k); n.el.style.transform = `scale(${0.3 + 0.7 * k})`; }
      for (const g of grow) g.el.style.setProperty("--k", ease((p - g.t) / SPAN).toFixed(3));
      for (const w of waves) w.el.style.transform = `scaleX(${clamp((p - w.t) / SPAN)})`;
      for (const t of tags) { const k = clamp((p - t.t) / 0.06); t.el.style.opacity = String(k); }
      const spread = ease((p - 0.04) / 0.5);
      const GAP = BASE_GAP * (window.innerWidth < 960 ? 0.62 : 1);
      for (const l of layers) {
        const k = clamp((p - l.t) / 0.08);
        l.el.style.opacity = String(0.25 + 0.75 * k);
        l.el.style.transform = `translateZ(${(l.i * GAP * spread).toFixed(1)}px)`;
      }
      for (const b of beams) b.el.style.setProperty("--k", spread.toFixed(3));
      for (const c of caps) c.el.classList.toggle("is-on", p >= c.t);
      if (bar) bar.style.transform = `scaleX(${p})`;
    };

    const staticMode = () => {
      story.classList.add("is-static");
      render(1);
      if (world) world.style.setProperty("--rz", "-36deg");
    };
    if (reduceMQ.matches) { staticMode(); return; }

    let ticking = false, active = false;
    const progress = () => {
      const r = story.getBoundingClientRect();
      const travel = r.height - window.innerHeight;
      return travel > 0 ? clamp(-r.top / travel) : 1;
    };
    const update = () => { ticking = false; render(progress()); };
    const onScroll = () => { if (active && !ticking) { ticking = true; requestAnimationFrame(update); } };
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(([e]) => { active = e.isIntersecting; if (active) onScroll(); }, { rootMargin: "20% 0px" }).observe(story);
    } else active = true;
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    reduceMQ.addEventListener("change", () => { if (reduceMQ.matches) { active = false; staticMode(); } });
    render(progress());
  };

  stories.forEach(setup);
})();
