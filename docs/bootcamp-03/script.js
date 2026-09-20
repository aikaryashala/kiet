/* KIET Bootcamp 3 — the one script. Sidebar toggle, copy buttons, command hints, quiz, stepper. No library. */
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

  /* ---------- 1b. hints ----------
     A one-line description of each command in a terminal block, generated from the command itself.
     A line may override it with data-hint="…". Continuation lines (   ...> ) get none. */
  function sqlHint(q) {
    var u = q.replace(/\s+/g, " ").trim();
    if (/^CREATE TABLE/i.test(u)) return "define the table: its name and its columns. Runs once per database file";
    if (/^INSERT INTO/i.test(u)) return (/VALUES\s*\(.*\)\s*,\s*\(/i.test(u) ? "add several rows" : "add one row") + " to the table, values in column order";
    if (/^SELECT COUNT\(\*\)/i.test(u)) return "count the rows" + (/WHERE/i.test(u) ? " that match the WHERE condition" : " in the table");
    if (/^SELECT COUNT\(DISTINCT/i.test(u)) return "count how many different values that column has";
    if (/^SELECT DISTINCT/i.test(u)) return "list each different value of that column once" + (/ORDER BY/i.test(u) ? ", sorted" : "");
    if (/^SELECT \*/i.test(u)) return /WHERE/i.test(u) ? "read every column of the rows that match the WHERE condition" : "read every row, every column";
    if (/^SELECT/i.test(u)) return /WHERE/i.test(u) ? "read those columns from the rows that match the WHERE condition — the loop with the if inside" : "read those columns from every row";
    if (/^UPDATE/i.test(u)) return "change the rows that match the WHERE condition";
    if (/^DELETE/i.test(u)) return "remove the rows that match the WHERE condition";
    if (/^DROP TABLE/i.test(u)) return "delete the table and everything in it";
    return "";
  }
  function dotHint(c) {
    var m;
    if (/^\.headers on/.test(c)) return "print the column names above every result";
    if (/^\.mode box/.test(c)) return "draw every result as a table with borders and the column names on top";
    if (/^\.mode column/.test(c)) return "line the results up in plain columns, no borders";
    if (/^\.quit/.test(c)) return "leave the sqlite3 shell, back to the normal prompt";
    if ((m = c.match(/^\.read (\S+)/))) return "run every statement in the file " + m[1];
    if (/^\.tables/.test(c)) return "list the tables in this database file";
    if (/^\.schema/.test(c)) return "print the CREATE TABLE statements of this file";
    return "a sqlite3 shell setting, not SQL: no semicolon";
  }
  function curlHint(c) {
    var m, method = /-X POST/.test(c) ? "POST" : "GET";
    if (/"[^"]*localhost:\d+[^"]* [^"]*"/.test(c)) return "a URL with a space in it: curl refuses it. Write + for each space instead";
    var url = (c.match(/(?:^|\s)"?((?:https?:\/\/)?localhost:\d+[^\s"]*)"?/) || [])[1] || "";
    var path = url.replace(/^https?:\/\//, "").replace(/^localhost:\d+/, "") || "/";
    var port = (url.match(/localhost:(\d+)/) || [])[1];
    var out = "send a " + method + " for " + path + (port ? " to the server on port " + port : "");
    var notes = [];
    if (/\s-i(\s|$)/.test(c)) notes.push("-i: print the status line and headers above the body");
    if (/\s-s(\s|$)/.test(c)) notes.push("-s: no progress bar");
    if (/\s-X POST/.test(c)) notes.push("-X POST: use the POST method");
    if (/\s-H /.test(c)) notes.push("-H: tell the server what kind of body follows");
    if ((m = c.match(/\s-d '([^']*)'/))) notes.push("-d: send " + m[1] + " as the body");
    if (/\?/.test(path)) notes.push("after the ? is the query string; the quotes keep the & from the shell");
    if (/\|\s*bash/.test(c)) return "download the setup script and run it with bash";
    return out + (notes.length ? " — " + notes.join("; ") : "");
  }
  function hintFor(c) {
    var m;
    c = c.trim();
    if (/^curl /.test(c)) return curlHint(c);
    if ((m = c.match(/^cd\s+(\S+)(\s*&&\s*(.*))?/))) return "go into the folder " + m[1] + (m[3] ? ", then: " + hintFor(m[3]) : "");
    if (/^ls(\s|$)/.test(c)) return /-l/.test(c) ? "list the files here, with size and date" : "list the files here";
    if ((m = c.match(/^python3 -m http\.server (\d+)/))) return "serve the files of this folder on port " + m[1] + " (Ctrl+C stops it)";
    if ((m = c.match(/^python3 -m sqlite3 (\S+)/))) return "open " + m[1] + " with Python's built-in sqlite3 shell";
    if (/^python3 --version/.test(c)) return "print the Python version";
    if (/check_env\.py/.test(c)) return "check that this machine is ready for the bootcamp";
    if (/check\.py/.test(c)) return "run this stage's self-check" + (/--port/.test(c) ? ", against that port" : "");
    if ((m = c.match(/^python3 (\S+\.py)\s*(.*)$/))) {
      var args = m[2].trim(), s = "run " + m[1] + " with Python";
      if (/server\.py$/.test(m[1])) s = "start the server in " + m[1] + " and leave it running (Ctrl+C stops it)";
      if (/--db/.test(args)) s += ", reading the database file given after --db";
      else if (/--port/.test(args)) s += ", listening on the port given after --port";
      else if (args) s += ", with " + args + " as the argument";
      return s;
    }
    if ((m = c.match(/^sqlite3 (\S+) < (\S+)/))) return "run every statement in " + m[2] + " against " + m[1] + ", creating the file if it is not there";
    if ((m = c.match(/^sqlite3 (\S+) "(.+)"/))) return "run one statement on " + m[1] + " and exit: " + sqlHint(m[2]);
    if ((m = c.match(/^sqlite3 (\S+)/))) return "open the database file " + m[1] + " in the sqlite3 shell, creating it if it is not there";
    if ((m = c.match(/^head -(\d+) (\S+)/))) return "print the first " + m[1] + " lines of " + m[2];
    if ((m = c.match(/^lsof -i :(\d+)/))) return "show which process is listening on port " + m[1];
    if ((m = c.match(/^kill (\d+)/))) return "stop the process whose id is " + m[1];
    if ((m = c.match(/^fuser -k (\d+)/))) return "stop whatever is holding port " + m[1];
    if (/^sed /.test(c)) return "edit the file in place: remove the Windows \\r at the end of every line";
    if ((m = c.match(/^mv (\S+) (\S+)/))) return "move " + m[1] + " to " + m[2] + ", replacing what was there";
    if (/^omarchy ascii /.test(c)) return "draw the quoted text in the Omarchy wordmark font and write it into the file after >";
    if (/^omarchy-launch-screensaver/.test(c)) return "start the screensaver now, even if the idle one is switched off; any key exits";
    if (/^omarchy branding/.test(c)) return "Omarchy's own branding command: edit, set from an image, or reset";
    if (/^omarchy plymouth preview/.test(c)) return "render the boot screen with these colours and this logo into a PNG and open it; changes nothing";
    if (/^omarchy plymouth set/.test(c)) return "apply these colours and this logo to the boot screen and the login screen (asks for your password)";
    if (/^omarchy plymouth reset/.test(c)) return "put the Omarchy logo and colours back on the boot and login screens";
    if (/^omarchy plymouth current/.test(c)) return "print which boot theme is in use now";
    if (/^magick identify/.test(c)) return "print the image's format, width, height and file size";
    if ((m = c.match(/^magick (\S+) -resize (\S+) (\S+)/))) return "shrink " + m[1] + " to fit " + m[2] + " pixels and save it as " + m[3] + " (the extension picks the format)";
    if ((m = c.match(/^which (\S+)/))) return "print which file runs when you type " + m[1] + " — the first match on PATH";
    if (/^echo 'export PATH=.*>> ~\/\.bashrc/.test(c)) return "add one line to ~/.bashrc so ~/.local/bin is searched first in every new terminal";
    if (/^source ~\/\.bashrc/.test(c)) return "read ~/.bashrc into this terminal now, instead of opening a new one";
    if (/^git clone/.test(c)) return "download the repository";
    if (/^git pull/.test(c)) return "fetch the latest changes into the clone";
    if (/^\./.test(c)) return dotHint(c);
    if (/^(CREATE|INSERT|SELECT|UPDATE|DELETE|DROP)\b/i.test(c)) return sqlHint(c);
    return "";
  }

  function collectHints(pre) {
    var items = [];
    var lines = pre.querySelectorAll(".ln.cmd");
    for (var i = 0; i < lines.length; i++) {
      var ln = lines[i];
      var p = ln.querySelector(".p");
      var prompt = p ? p.textContent : "";
      if (/\.\.\.>/.test(prompt)) continue;                 // continuation of the previous statement
      var clone = ln.cloneNode(true);
      clone.querySelectorAll(".p").forEach(function (x) { x.remove(); });
      var text = clone.textContent.trim();
      // a multi-line SQL statement: join the continuation lines for the hint
      var full = text, k = i + 1;
      while (k < lines.length && /\.\.\.>/.test((lines[k].querySelector(".p") || {}).textContent || "")) {
        var cl = lines[k].cloneNode(true); cl.querySelectorAll(".p").forEach(function (x) { x.remove(); });
        full += " " + cl.textContent.trim(); k++;
      }
      var hint = ln.getAttribute("data-hint") || hintFor(full);
      if (hint) items.push([text, hint]);
    }
    return items;
  }

  function addCopyButtons() {
    document.querySelectorAll(".panel").forEach(function (panel) {
      var pre = panel.querySelector("pre.term, pre.code[data-copy]");
      var cap = panel.querySelector(":scope > .cap, :scope > h2");
      if (!pre || !cap || cap.querySelector(".copy")) return;
      if (pre.classList.contains("term") && !pre.querySelector(".ln.cmd")) return;

      if (pre.classList.contains("term")) {
        var items = collectHints(pre);
        if (items.length) {
          var hb = document.createElement("button");
          hb.className = "hintbtn";
          hb.type = "button";
          hb.textContent = "hint";
          var box = null;
          hb.addEventListener("click", function () {
            if (box) { box.remove(); box = null; hb.textContent = "hint"; return; }
            box = document.createElement("div");
            box.className = "hints";
            items.forEach(function (it) {
              var row = document.createElement("div");
              row.className = "hint";
              var c = document.createElement("code"); c.textContent = it[0];
              var d = document.createElement("span"); d.textContent = it[1];
              row.appendChild(c); row.appendChild(d);
              box.appendChild(row);
            });
            cap.insertAdjacentElement("afterend", box);
            hb.textContent = "hide";
          });
          cap.appendChild(hb);
        }
      }

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

  /* ---------- 5. sidebar toggle ----------
     "hide contents" at the top of the sidebar; a fixed "contents" button brings it back.
     The choice is remembered in this browser only. */
  function initNavToggle() {
    var nav = document.querySelector(".nav");
    if (!nav) return;
    var hide = document.createElement("button");
    hide.className = "navhide"; hide.type = "button"; hide.textContent = "hide contents";
    var show = document.createElement("button");
    show.className = "navshow"; show.type = "button"; show.textContent = "contents";
    function set(hidden) {
      document.body.classList.toggle("nav-hidden", hidden);
      try { localStorage.setItem("kiet-nav", hidden ? "hidden" : "shown"); } catch (e) { /* private window etc. */ }
    }
    hide.addEventListener("click", function () { set(true); show.focus(); });
    show.addEventListener("click", function () { set(false); hide.focus(); });
    nav.insertBefore(hide, nav.firstChild);
    document.body.appendChild(show);
    var saved = null;
    try { saved = localStorage.getItem("kiet-nav"); } catch (e) { saved = null; }
    if (saved === "hidden") document.body.classList.add("nav-hidden");
  }

  document.addEventListener("DOMContentLoaded", function () {
    initNavToggle();
    addCopyButtons();
    initQuiz();
    initSteppers();
  });
})();
