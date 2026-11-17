/* ==========================================================================
   Teltech Networks, S.A. — Hero globe (canvas)
   A dot-matrix Earth built from Natural Earth data (js/globe-data.js).
   Opening: the camera arrives from orbit and zooms into Central America.
   Then arcs fire from the head office (Ciudad de Guatemala) to the other
   operation points, with data pulses travelling along them.

   Falls back to the inline static SVG (.hero__static) when:
     - prefers-reduced-motion: reduce
     - navigator.connection.saveData === true
     - navigator.hardwareConcurrency <= 2
   Uses requestAnimationFrame and pauses when the hero is off-screen or the
   tab is hidden. Network nodes (cities) stay far below the 80-node cap.
   ========================================================================== */
(() => {
  "use strict";

  const hero = document.querySelector("[data-hero]");
  const data = window.TELTECH_GLOBE;
  if (!hero || !data) return;
  const canvas = hero.querySelector(".hero__canvas");
  if (!canvas || !canvas.getContext) return;
  const chips = Array.from(hero.querySelectorAll("[data-loc]"));

  const reduceMQ = window.matchMedia("(prefers-reduced-motion: reduce)");
  const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  const useStatic = () =>
    reduceMQ.matches ||
    Boolean(conn && conn.saveData) ||
    (typeof navigator.hardwareConcurrency === "number" && navigator.hardwareConcurrency <= 2);
  const markHot = (ids) => chips.forEach((c) => c.classList.toggle("is-hot", ids.includes(c.dataset.loc)));

  if (useStatic()) { hero.dataset.mode = "static"; markHot(chips.map((c) => c.dataset.loc)); return; }

  const ctx = canvas.getContext("2d");
  const DEG = Math.PI / 180;

  /* ---------- Data decoding ---------- */
  const b64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
  const dotBytes = b64(data.dots);
  const dotView = new DataView(dotBytes.buffer);
  const flags = b64(data.flags);
  const N = flags.length;
  const vec = (lat, lon) => {
    const cl = Math.cos(lat * DEG);
    return [cl * Math.cos(lon * DEG), cl * Math.sin(lon * DEG), Math.sin(lat * DEG)];
  };
  const dots = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    const v = vec(dotView.getInt16(i * 4, true) / 100, dotView.getInt16(i * 4 + 2, true) / 100);
    dots[i * 3] = v[0]; dots[i * 3 + 1] = v[1]; dots[i * 3 + 2] = v[2];
  }
  const borderView = new DataView(b64(data.borders).buffer);
  const rings = [];
  let off = 0;
  data.rings.forEach((len) => {
    const r = [];
    for (let k = 0; k < len; k++, off++) r.push(vec(borderView.getInt16(off * 4, true) / 100, borderView.getInt16(off * 4 + 2, true) / 100));
    rings.push(r);
  });
  // Graticule (every 10 degrees) gives the ocean its curvature.
  const grat = [];
  for (let lon = -170; lon <= 180; lon += 10) for (let lat = -80; lat <= 80; lat += 2) grat.push(vec(lat, lon));
  for (let lat = -60; lat <= 70; lat += 10) for (let lon = -180; lon < 180; lon += 2) grat.push(vec(lat, lon));

  const CITIES = [
    // Label directions (degrees, screen space) for desktop (d) and phones (m).
    { id: "gt", name: "Ciudad de Guatemala", lat: 14.6349, lon: -90.5069, hq: true, d: -75, m: -95 },
    { id: "sv", name: "El Salvador", lat: 13.6929, lon: -89.2182, d: 160, m: 160 },
    { id: "ni", name: "Nicaragua", lat: 12.1364, lon: -86.2514, d: 15, m: 10 },
    { id: "cr", name: "Costa Rica", lat: 9.9281, lon: -84.0907, d: 30, m: 60 },
    { id: "mia", name: "Miami", lat: 25.7617, lon: -80.1918, d: -30, m: -150 },
  ].map((c) => ({ ...c, v: vec(c.lat, c.lon) }));
  const HQ = CITIES[0];

  // Great-circle arcs lifted above the surface.
  const ARC_SEG = 56;
  const arcs = CITIES.slice(1).map((c) => {
    const a = HQ.v, b = c.v;
    const dot = a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
    const om = Math.acos(Math.min(1, dot));
    const lift = 0.016 + om * 0.5;
    const pts = [];
    for (let s = 0; s <= ARC_SEG; s++) {
      const t = s / ARC_SEG;
      const k1 = Math.sin((1 - t) * om) / Math.sin(om), k2 = Math.sin(t * om) / Math.sin(om);
      const h = 1 + lift * Math.sin(Math.PI * t);
      pts.push([(a[0] * k1 + b[0] * k2) * h, (a[1] * k1 + b[1] * k2) * h, (a[2] * k1 + b[2] * k2) * h]);
    }
    return { city: c, pts };
  });

  /* ---------- Colors from tokens ---------- */
  const readColor = (name, fallback) => {
    const raw = getComputedStyle(document.documentElement).getPropertyValue(name).trim() || fallback;
    const probe = document.createElement("canvas").getContext("2d");
    probe.fillStyle = fallback; probe.fillStyle = raw;
    const m = /^#([0-9a-f]{6})$/i.exec(probe.fillStyle);
    const n = parseInt(m ? m[1] : fallback.slice(1), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  };
  const C = { accent: readColor("--c-accent", "#1ec0e8"), land: readColor("--c-neutral-400", "#8ea4bd"), label: readColor("--c-neutral-50", "#eef6fb") };
  const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;

  /* ---------- Camera ---------- */
  let w = 0, h = 0, dpr = 1, mobile = false;
  let cx = 0, cy = 0, R = 0, R0 = 0, R1 = 0;
  let lat0 = 16.5, lon0 = -86;
  const view = { lat: 16.5, lon: -86 };
  const pointer = { x: 0, y: 0 };
  let M = [1, 0, 0, 0, 1, 0, 0, 0, 1];

  function layout() {
    const r = hero.getBoundingClientRect();
    w = Math.max(1, Math.round(r.width)); h = Math.max(1, Math.round(r.height));
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    mobile = w < 768;
    if (mobile) { cx = w * 0.62; cy = Math.min(h * 0.27, 240); R1 = w * 2.8; R0 = w * 0.62; view.lat = 18; }
    else { cx = w * 0.72; cy = h * 0.5; R1 = h * 2.0; R0 = h * 0.62; view.lat = 16.5; }
  }

  // Rotation matrix so that (lat0, lon0) faces the viewer (+z), north up (+y).
  function setRotation(latC, lonC) {
    const la = latC * DEG, lo = lonC * DEG;
    const sl = Math.sin(la), cl = Math.cos(la), so = Math.sin(lo), co = Math.cos(lo);
    // rows: screen x (east), screen y (north), depth z (towards viewer)
    M = [-so, co, 0, -sl * co, -sl * so, cl, cl * co, cl * so, sl];
  }
  const project = (v, out) => {
    out[0] = M[0] * v[0] + M[1] * v[1] + M[2] * v[2];
    out[1] = M[3] * v[0] + M[4] * v[1] + M[5] * v[2];
    out[2] = M[6] * v[0] + M[7] * v[1] + M[8] * v[2];
    return out;
  };

  /* ---------- Timeline ---------- */
  const INTRO = 3200;        // arrival from orbit
  const CYCLE = 7200;        // arc loop
  const ease = (t) => (t < 0 ? 0 : t > 1 ? 1 : 1 - Math.pow(1 - t, 3));
  const easeIO = (t) => (t < 0 ? 0 : t > 1 ? 1 : t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  let time = 0, last = 0, running = false, inView = true, raf = 0, lastHot = "";
  const tmp = [0, 0, 0];
  const bucketsX = [[], [], [], []], bucketsY = [[], [], [], []];

  function frame(now) {
    if (!running) return;
    const dt = Math.min(48, now - (last || now));
    last = now; time += dt;
    draw();
    raf = requestAnimationFrame(frame);
  }

  function draw() {
    const ti = easeIO(time / INTRO);
    R = R0 + (R1 - R0) * ti;
    const sway = Math.sin(time / 5200) * 1.6;
    lon0 = view.lon + (1 - ti) * 62 + sway * ti + pointer.x * 2.2;
    lat0 = view.lat - (1 - ti) * 8 + pointer.y * 1.6;
    setRotation(lat0, lon0);
    ctx.clearRect(0, 0, w, h);

    // Atmosphere glow + limb
    const g = ctx.createRadialGradient(cx, cy, R * 0.92, cx, cy, R * 1.12);
    g.addColorStop(0, rgba(C.accent, 0.16)); g.addColorStop(1, rgba(C.accent, 0));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R * 1.12, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = rgba(C.accent, 0.28); ctx.lineWidth = 1;
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.stroke();

    // Graticule
    ctx.fillStyle = rgba(C.land, 0.16);
    for (let i = 0; i < grat.length; i++) {
      project(grat[i], tmp);
      if (tmp[2] <= 0) continue;
      const x = cx + R * tmp[0], y = cy - R * tmp[1];
      if (x < -2 || x > w + 2 || y < -2 || y > h + 2) continue;
      ctx.fillRect(x, y, 1, 1);
    }

    // Land dots bucketed by depth (few fillStyle changes)
    for (let b = 0; b < 4; b++) { bucketsX[b].length = 0; bucketsY[b].length = 0; }
    const hotX = [], hotY = [], flX = [], flY = [];
    const size = mobile ? 1.6 : 1.9;
    const stride = mobile && ti < 0.6 ? 2 : 1;
    for (let i = 0; i < N; i += stride) {
      const v0 = dots[i * 3], v1 = dots[i * 3 + 1], v2 = dots[i * 3 + 2];
      const z = M[6] * v0 + M[7] * v1 + M[8] * v2;
      if (z <= 0.02) continue;
      const x = cx + R * (M[0] * v0 + M[1] * v1 + M[2] * v2);
      const y = cy - R * (M[3] * v0 + M[4] * v1 + M[5] * v2);
      if (x < -3 || x > w + 3 || y < -3 || y > h + 3) continue;
      const f = flags[i];
      if (f === 1) { hotX.push(x); hotY.push(y); continue; }
      if (f === 2) { flX.push(x); flY.push(y); continue; }
      const b = z > 0.75 ? 3 : z > 0.5 ? 2 : z > 0.25 ? 1 : 0;
      bucketsX[b].push(x); bucketsY[b].push(y);
    }
    const alphas = [0.18, 0.32, 0.48, 0.62];
    for (let b = 0; b < 4; b++) {
      ctx.fillStyle = rgba(C.land, alphas[b]);
      const X = bucketsX[b], Y = bucketsY[b];
      for (let k = 0; k < X.length; k++) ctx.fillRect(X[k] - size / 2, Y[k] - size / 2, size, size);
    }
    ctx.fillStyle = rgba(C.accent, 0.55);
    for (let k = 0; k < flX.length; k++) ctx.fillRect(flX[k] - size / 2, flY[k] - size / 2, size, size);
    const hs = size + 0.6 * ti;
    ctx.fillStyle = rgba(C.accent, 0.35 + 0.55 * ti);
    for (let k = 0; k < hotX.length; k++) ctx.fillRect(hotX[k] - hs / 2, hotY[k] - hs / 2, hs, hs);

    // Borders of operating countries
    if (ti > 0.55) {
      ctx.strokeStyle = rgba(C.accent, 0.75 * ease((ti - 0.55) / 0.45));
      ctx.lineWidth = 1.2;
      for (const r of rings) {
        ctx.beginPath();
        let started = false;
        for (const v of r) {
          project(v, tmp);
          if (tmp[2] <= 0) { started = false; continue; }
          const x = cx + R * tmp[0], y = cy - R * tmp[1];
          if (!started) { ctx.moveTo(x, y); started = true; } else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
    }

    // Arcs + pulses (after arrival)
    const hot = [HQ.id];
    if (time > INTRO * 0.8) {
      const t = time - INTRO * 0.8;
      arcs.forEach((arc, i) => {
        const local = ((t - i * 650) % CYCLE + CYCLE) % CYCLE;
        if (t < i * 650) return;
        const grow = ease(local / 1100);
        const fade = local > CYCLE - 900 ? 1 - (local - (CYCLE - 900)) / 900 : 1;
        if (grow > 0.98 && fade > 0.2) hot.push(arc.city.id);
        const upto = Math.max(1, Math.round(ARC_SEG * grow));
        ctx.lineWidth = mobile ? 1.4 : 1.7;
        ctx.strokeStyle = rgba(C.accent, 0.85 * fade);
        ctx.beginPath();
        for (let s = 0; s <= upto; s++) {
          project(arc.pts[s], tmp);
          const x = cx + R * tmp[0], y = cy - R * tmp[1];
          s ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
        }
        ctx.stroke();
        // Pulse travelling along the completed arc
        if (grow >= 1 && fade > 0.3) {
          const pt = ((local - 1100) % 1600) / 1600;
          const idx = Math.min(ARC_SEG, Math.max(0, Math.floor(pt * ARC_SEG)));
          project(arc.pts[idx], tmp);
          const x = cx + R * tmp[0], y = cy - R * tmp[1];
          ctx.fillStyle = rgba(C.accent, 0.25 * fade); ctx.beginPath(); ctx.arc(x, y, 7, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = rgba(C.label, fade); ctx.beginPath(); ctx.arc(x, y, 2.2, 0, Math.PI * 2); ctx.fill();
        }
      });
    }

    // Cities: rings, dots, labels
    const showLabels = ease((time - INTRO * 0.7) / 900);
    for (const c of CITIES) {
      project(c.v, tmp);
      if (tmp[2] <= 0) continue;
      const x = cx + R * tmp[0], y = cy - R * tmp[1];
      const isHot = hot.includes(c.id);
      const cyc = ((time + (c.hq ? 0 : 700)) % 2400) / 2400;
      ctx.strokeStyle = rgba(C.accent, (1 - cyc) * (c.hq ? 0.7 : 0.45) * ti);
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.arc(x, y, (c.hq ? 6 : 4) + cyc * (c.hq ? 30 : 18), 0, Math.PI * 2); ctx.stroke();
      ctx.fillStyle = rgba(C.accent, c.hq || isHot ? 1 : 0.6);
      ctx.beginPath(); ctx.arc(x, y, c.hq ? 4.5 : 3.2, 0, Math.PI * 2); ctx.fill();
      if (showLabels > 0) {
        const a = (mobile ? c.m : c.d) * DEG, L = mobile ? 22 : 38;
        const lx = x + Math.cos(a) * L, ly = y + Math.sin(a) * L;
        ctx.strokeStyle = rgba(C.land, 0.6 * showLabels);
        ctx.beginPath(); ctx.moveTo(x + Math.cos(a) * 6, y + Math.sin(a) * 6); ctx.lineTo(lx, ly); ctx.stroke();
        const fs = mobile ? 11 : 13;
        ctx.font = `${c.hq ? 700 : 600} ${fs}px Saira, "Segoe UI", sans-serif`;
        ctx.textBaseline = "middle";
        ctx.textAlign = Math.cos(a) < -0.2 ? "right" : Math.cos(a) > 0.2 ? "left" : "center";
        const pad = Math.cos(a) < -0.2 ? -4 : Math.cos(a) > 0.2 ? 4 : 0;
        const ty = ly + (Math.sin(a) < -0.6 ? -8 : Math.sin(a) > 0.6 ? 8 : 0);
        ctx.fillStyle = rgba(isHot || c.hq ? C.label : C.land, showLabels);
        ctx.fillText(c.name.toUpperCase(), lx + pad, ty);
        if (c.hq) {
          ctx.font = `600 ${fs - 2}px "IBM Plex Sans", sans-serif`;
          ctx.fillStyle = rgba(C.accent, showLabels);
          ctx.fillText("SEDE CENTRAL", lx + pad, ty - fs - 2);
        }
      }
    }

    const key = hot.join(",");
    if (key !== lastHot) { lastHot = key; markHot(hot); }
  }

  function start() {
    if (running || document.hidden || !inView) return;
    running = true; last = 0;
    raf = requestAnimationFrame(frame);
  }
  function stop() { running = false; cancelAnimationFrame(raf); }

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(([e]) => { inView = e.isIntersecting; inView ? start() : stop(); }, { threshold: 0 }).observe(hero);
  }
  document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
  let lastW = 0, rt = 0;
  window.addEventListener("resize", () => {
    clearTimeout(rt);
    rt = setTimeout(() => {
      const nw = Math.round(hero.getBoundingClientRect().width);
      layout();
      if (nw !== lastW) lastW = nw;
      if (!running) draw();
    }, 160);
  });
  reduceMQ.addEventListener("change", () => {
    if (reduceMQ.matches) { stop(); hero.classList.remove("is-live"); hero.dataset.mode = "static"; markHot(chips.map((c) => c.dataset.loc)); }
  });
  if (window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    hero.addEventListener("pointermove", (e) => {
      const r = hero.getBoundingClientRect();
      pointer.x = ((e.clientX - r.left) / r.width - 0.5) * 2;
      pointer.y = ((e.clientY - r.top) / r.height - 0.5) * 2;
    });
    hero.addEventListener("pointerleave", () => { pointer.x = 0; pointer.y = 0; });
  }

  // Start once the intro (if any) is lifting, so the arrival is seen.
  const begin = () => {
    layout(); lastW = w;
    hero.classList.add("is-live");
    hero.dataset.mode = "live";
    start();
  };
  if (document.documentElement.classList.contains("intro-on")) {
    document.addEventListener("ttn:intro-done", begin, { once: true });
    setTimeout(() => { if (!running && hero.dataset.mode !== "live") begin(); }, 4000);
  } else begin();
})();
