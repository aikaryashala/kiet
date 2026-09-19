/* KIET Bootcamp 3 — the one script. Three jobs: copy buttons, quiz, stepper. No library. */
(function () {
  "use strict";

  /* ---------- 1. copy buttons ----------
     Every .panel that holds a pre.term gets a "copy" button in its caption bar.
     It copies the .ln.cmd lines only, without the prompt symbol, one per line.
     A pre.code inside a panel with data-copy gets the same, copying every line. */
  function textToCopy(pre) {
    var lines = [];
    var sel = pre.classList.contains("term") ? ".ln.cmd" : ".ln";
    pre.querySelectorAll(sel).forEach(function (ln) {
      var clone = ln.cloneNode(true);
      clone.querySelectorAll(".p").forEach(function (p) { p.remove(); });
      lines.push(clone.textContent.replace(/\s+$/, ""));
    });
    return lines.join("\n");
  }

  function addCopyButtons() {
    document.querySelectorAll(".panel").forEach(function (panel) {
      var pre = panel.querySelector("pre.term, pre.code[data-copy]");
      var cap = panel.querySelector(":scope > .cap, :scope > h2");
      if (!pre || !cap || cap.querySelector(".copy")) return;
      if (pre.classList.contains("term") && !pre.querySelector(".ln.cmd")) return;
      var btn = document.createElement("button");
      btn.className = "copy";
      btn.type = "button";
      btn.textContent = "copy";
      btn.addEventListener("click", function () {
        var text = textToCopy(pre);
        var done = function () { btn.textContent = "copied"; setTimeout(function () { btn.textContent = "copy"; }, 1400); };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text); done(); });
        } else { fallbackCopy(text); done(); }
      });
      cap.appendChild(btn);
    });
  }

  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) { /* nothing more to try */ }
    ta.remove();
  }

  /* ---------- 2. quiz ----------
     <div class="quiz"><div class="q" data-answer="2"><p>…</p>
       <button class="opt">…</button> … <p class="exp">…</p></div></div>
     data-answer is the 1-based index of the correct .opt. */
  function initQuiz() {
    document.querySelectorAll(".quiz .q").forEach(function (q) {
      var answer = parseInt(q.getAttribute("data-answer"), 10);
      var opts = q.querySelectorAll(".opt");
      var exp = q.querySelector(".exp");
      opts.forEach(function (opt, i) {
        opt.type = "button";
        opt.addEventListener("click", function () {
          if (q.classList.contains("done")) return;
          q.classList.add("done");
          if (i + 1 === answer) {
            opt.classList.add("right");
          } else {
            opt.classList.add("wrong");
            if (opts[answer - 1]) opts[answer - 1].classList.add("right");
          }
          opts.forEach(function (o) { o.disabled = true; });
          if (exp) exp.classList.add("show");
        });
      });
    });
  }

  /* ---------- 3. stepper ----------
     <div class="stepper">
       <div class="stage"> …panels with pre.code / pre.term (each with an id), .slot (with ids), table (with id)… </div>
       <div class="controls"><button class="back">Back</button><button class="play">Play</button>
         <button class="fwd">Forward</button><span class="counter"></span></div>
       <div class="track"><span></span></div>
       <p class="narration"></p>
       <script type="application/json" class="steps">[ …steps… ]</script>
     </div>
     A step: {"note": "…",
              "hl": {"<pre id>": <0-based line index or null>},
              "slots": {"<slot id>": {"v": "…", "cls": "live|warn|dead|"}},
              "table": {"<table id>": {"cur": [row indexes], "skip": [row indexes]}},
              "show": {"<element id>": true|false}} */
  var steppers = [];
  var active = null;

  function initStepper(root) {
    var data = root.querySelector("script.steps");
    if (!data) return;
    var steps;
    try { steps = JSON.parse(data.textContent); } catch (e) { return; }
    if (!steps.length) return;

    var back = root.querySelector(".back"), play = root.querySelector(".play"), fwd = root.querySelector(".fwd");
    var counter = root.querySelector(".counter"), track = root.querySelector(".track span"), note = root.querySelector(".narration");
    var i = 0, timer = null;

    function byId(id) { return root.querySelector("#" + CSS.escape(id)); }

    function render() {
      var s = steps[i];
      root.querySelectorAll(".ln.on").forEach(function (l) { l.classList.remove("on"); });
      root.querySelectorAll("tr.cur, tr.skip").forEach(function (r) { r.classList.remove("cur", "skip"); });
      if (s.hl) Object.keys(s.hl).forEach(function (id) {
        var pre = byId(id); if (!pre || s.hl[id] === null) return;
        var lines = pre.querySelectorAll(".ln");
        if (lines[s.hl[id]]) lines[s.hl[id]].classList.add("on");
      });
      if (s.slots) Object.keys(s.slots).forEach(function (id) {
        var slot = byId(id); if (!slot) return;
        var v = slot.querySelector(".v"); if (!v) return;
        v.textContent = s.slots[id].v;
        v.className = "v " + (s.slots[id].cls || "");
      });
      if (s.table) Object.keys(s.table).forEach(function (id) {
        var t = byId(id); if (!t) return;
        var rows = t.querySelectorAll("tbody tr");
        (s.table[id].cur || []).forEach(function (r) { if (rows[r]) rows[r].classList.add("cur"); });
        (s.table[id].skip || []).forEach(function (r) { if (rows[r]) rows[r].classList.add("skip"); });
      });
      if (s.show) Object.keys(s.show).forEach(function (id) {
        var el = byId(id); if (el) el.hidden = !s.show[id];
      });
      if (note) note.textContent = s.note || "";
      if (counter) counter.textContent = (i + 1) + " / " + steps.length;
      if (track) track.style.width = ((i + 1) / steps.length * 100) + "%";
      if (back) back.disabled = i === 0;
      if (fwd) fwd.disabled = i === steps.length - 1;
    }

    function go(n) { i = Math.max(0, Math.min(steps.length - 1, n)); render(); }
    function stop() { if (timer) { clearInterval(timer); timer = null; } if (play) play.textContent = "Play"; }
    function start() {
      if (i === steps.length - 1) go(0);
      timer = setInterval(function () { if (i >= steps.length - 1) { stop(); } else { go(i + 1); } }, 3400);
      if (play) play.textContent = "Pause";
    }

    if (back) back.addEventListener("click", function () { stop(); go(i - 1); });
    if (fwd) fwd.addEventListener("click", function () { stop(); go(i + 1); });
    if (play) play.addEventListener("click", function () { timer ? stop() : start(); });
    root.addEventListener("click", function () { active = api; });
    root.addEventListener("focusin", function () { active = api; });

    var api = { next: function () { stop(); go(i + 1); }, prev: function () { stop(); go(i - 1); }, root: root };
    steppers.push(api);
    render();
  }

  function initSteppers() {
    document.querySelectorAll(".stepper").forEach(initStepper);
    if (steppers.length) active = steppers[0];
    document.addEventListener("keydown", function (e) {
      if (!active) return;
      var tag = (e.target.tagName || "").toLowerCase();
      if (tag === "input" || tag === "textarea" || tag === "select") return;
      if (e.key === "ArrowRight") { active.next(); e.preventDefault(); }
      if (e.key === "ArrowLeft") { active.prev(); e.preventDefault(); }
    });
  }

  /* ---------- 4. missing video ----------
     The demo videos are handed out separately. When the file is not there, the browser would show an
     empty black player; swap it for the fallback sentence instead so the panel keeps its size and says why. */
  function initMedia() {
    document.querySelectorAll(".panel.media video").forEach(function (v) {
      function swap() {
        var msg = document.createElement("div");
        msg.className = "missing";
        msg.textContent = v.textContent.trim() || "Demo video not available yet — follow the written steps below.";
        v.replaceWith(msg);
      }
      v.addEventListener("error", swap);
      if (v.error || v.networkState === HTMLMediaElement.NETWORK_NO_SOURCE) swap();   // the 404 may have come before this ran
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    addCopyButtons();
    initQuiz();
    initSteppers();
    initMedia();
  });
})();
