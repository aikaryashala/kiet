# KIET Bootcamp #3 — Build plan

Python backend with Bottle + SQLite. 21 September 2026, one day in three sessions; 22 September is presentations and Omarchy.

This is the execution plan. `spec.md` holds the content (routes, concept wording, sample data rules, check behaviour); `theme.md` holds the look. Where this plan and the spec name the same thing, the spec's detail wins; where they disagree on a decision, this plan is newer and wins.

---

## 1. Decisions (all settled)

| Topic | Decision |
|---|---|
| Where it lives | One student repo `aikaryashala/kiet-bootcamp-3` with `docs/` (material), `code/` (stages + frontend), `data/` side by side. Cloned to `~/kiet-bootcamp-3`. Used offline from `http://localhost:8000`. `docs/` also hosted at `https://aikaryashala.com/kiet-bootcamp-3/`. |
| Hub | This folder, `kiet/docs/bootcamp-03/`, published at `https://aikaryashala.com/kiet/bootcamp-03/`. Holds `index.html`, `setup.html`, `scripts/setup.sh`. Online only. |
| Setup script | `scripts/setup.sh` here, not in the student repo. Run once online via `curl -sSL https://aikaryashala.com/kiet/bootcamp-03/scripts/setup.sh \| bash`. Steps also written out on `setup.html`. |
| Offline | No Google Fonts, no CDN, no external images. Fonts are local `.woff2` in `docs/fonts/`, downloaded once and committed. |
| CSS/JS | One shared `docs/style.css` and one `docs/script.js`. No inline styles or scripts in material pages. |
| Look | `theme.md`. Page 1040px, prose 70ch, 16px base. Terminal blocks dark, everything else light. |
| Stage page | 8 sections: Concept, Demo video, Task, Expected output, Check yourself, Takeaway, Stuck?, Quiz. Left nav on every page. |
| Quiz | 4 questions per stage page, one correct, click to reveal, no score. Written during the build. |
| Steppers | Stages 1, 2, 3, 5, 8 (spec §5.7). Others prose only. |
| Frontend | `code/frontend/`: `index.html` + `app.js` + `README.md`. Plain HTML, no theme, no fonts, one short `<style>`. Focus stays on request/response. |
| Stages | 0–8. Stage 7 = run the frontend and read its request log. Stage 8 = the browser inspector, Network tab vs `curl -i`, CORS break-and-fix. |
| Sessions | All nine stages on 21 September. Morning: Stage 0–2. Afternoon: Stage 3–5. After dinner (until 11:30 pm): Stage 6–8. Day 2 (22 Sep): team presentations + Omarchy customization, outside this material. |
| Ports | 8000 material · 8080 given servers · 8081 student's server · 9000 frontend |
| Table | `students(student_name, inter_college, inter_city)`, no id |
| Python | ≥ 3.12, Bottle 0.13.x as `bottle.py` copied into each server folder, no pip, no venv |
| OS | Ubuntu 24.04 and Omarchy (Arch) |
| Videos | Not built. Placeholders + shot lists in `docs/videos/README.md`. |

---

## 2. What gets built, where

### 2.1 Student repo `kiet-bootcamp-3/` (sibling of this repo in the workspace)

```
kiet-bootcamp-3/
├── README.md
├── check_env.py
├── .gitignore
├── data/
│   ├── schema.sql
│   ├── sample_team_details.sql
│   └── all_students.sql
├── docs/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── fonts/            Fraunces, Inter Tight, JetBrains Mono (.woff2)
│   ├── img/              stage8 screenshot placeholders
│   ├── stage0.html … stage8.html
│   ├── troubleshooting.html
│   ├── videos/README.md
│   └── reference/        python-cheatsheet, c-to-python, sqlite-cli,
│                         sql-for-students-table, json, bottle, curl, http-basics
└── code/
    ├── stage0/   01_hello.py … 07_filter_pack.py, check.py, solution/
    ├── stage1/   check.py
    ├── stage2/   read_all.py, by_college.py (stub), check.py, solution/
    ├── stage3/   bottle.py, demo_server.py, curl_commands.txt, check.py
    ├── stage4/   bottle.py, server.py (stub), check.py, solution/
    ├── stage5/   bottle.py, server.py (partial), check.py, solution/
    ├── stage6/   check.py
    ├── stage7/   check.py
    ├── stage8/   check.py
    └── frontend/ index.html, app.js, README.md
```

### 2.2 This folder `kiet/docs/bootcamp-03/`

```
bootcamp-03/
├── index.html        hub, card style of bootcamp-02
├── setup.html        the setup steps, written out
├── scripts/setup.sh
├── plan.md           this file
├── spec.md
└── theme.md
```

---

## 3. Stage map

| Stage | Title | Student writes | Given | Check | Stepper |
|---|---|---|---|---|---|
| 0 | Just enough Python | 7 exercise files | headers + TODOs | stdout compare | – |
| 1 | Data that survives: SQLite and SQL | `team_details.db` via the CLI | `schema.sql` | file, table, ≥3 rows | SELECT…WHERE walking rows |
| 2 | Python talks to the database | `by_college.py` | `read_all.py`, stub | stdout vs sample DB | connect → execute → fetchall |
| 3 | What a server actually is | nothing, observe | `demo_server.py`, curl list | 4 routes + 404 + 400 | one request through path/query/body |
| 4 | Write your own server | 3 routes on 8081 | stub with `/hai` | 3 routes, `/about` keys | – |
| 5 | Join the two halves | 4 GET routes | `query`, `pack`, `/students`, CORS hook | 5 routes + 400s | unpack → query → pack |
| 6 | Swap the data, not the code | nothing, rebuild DB | `all_students.sql` | row count, `/colleges` length | – |
| 7 | Someone else's client | nothing, run and read | `code/frontend/` | 9000 serves, 8080 answers | – |
| 8 | The inspector | nothing, observe, break CORS | Stage 7 running | CORS header present | `curl -i` lines ↔ Network tab fields |

Concept wording, route tables, task steps, expected outputs and takeaways for each stage: spec §7 and §9.

---

## 4. Build order

Each step ends with something runnable or renderable. Nothing later is started until the step's check passes.

### Step 1 — Data (`data/`)
- `schema.sql`: the one `CREATE TABLE`.
- `sample_team_details.sql`: same CREATE + 4 rows, 2 colleges, 2 cities. These names appear in every Expected output.
- `all_students.sql`: same CREATE byte-identical + 200 rows, 12 colleges, 8 cities, Telugu names, uneven counts, one college in one city only, one city with one college only. Exact counts in a header comment.
- **Check:** load each into a temp DB with `sqlite3`, `SELECT COUNT(*)`, `SELECT DISTINCT` per column; record the counts for later Expected output blocks.

### Step 2 — Reference servers
- Fetch Bottle 0.13.x single file once; copy as `code/stage3/bottle.py`, `stage4/bottle.py`, `stage5/bottle.py`.
- `code/stage3/demo_server.py` (spec §9 Stage 3 route table).
- `code/stage5/solution/server.py` (all five routes + CORS hook + `query` + `pack`).
- Both honour `--port` and `--db`, print the start line, run with `debug=True`.
- **Check:** start each, run every curl from the spec, capture literal output and the server log lines into a scratch file. These captures become the Expected output blocks.

### Step 3 — Remaining code
- Derive `stage5/server.py` (partial) and `stage4/server.py` (stub) from the solutions; `stage4/solution/server.py`.
- `stage2/read_all.py`, `by_college.py` stub, `solution/by_college.py`.
- `stage0/01…07.py` with header comments and TODOs; `solution/`.
- `stage3/curl_commands.txt`.
- `check.py` for every stage 0–8, standard library only, PASS/FAIL lines, actionable "is the server running?" message.
- **Check:** every `check.py` passes against its `solution/` and fails meaningfully against the untouched stub. `grep` student-facing code for forbidden constructs (spec §2.4).

### Step 4 — Repo root
- `check_env.py` (spec §5.2), `.gitignore` (`data/*.db`, `__pycache__/`), `README.md` (5 lines: what it is, link to the hub setup page, `cd docs && python3 -m http.server 8000`).

### Step 5 — Frontend (`code/frontend/`)
- `index.html`: title, College dropdown, Location input, three buttons, results table with row count, Request log `<pre>`, backend-unreachable banner. One `<style>` block, ≤ 30 lines.
- `app.js`: `const BACKEND = "http://localhost:8080";` on line 1; `fetch` with `.then`; a comment above each `fetch` giving the curl it replaces; under 120 lines.
- `README.md`: two lines.
- **Check:** run against the Stage 5 solution server with `all_students.db`; all three buttons fill the table and the log; kill the server and reload to see the banner.

### Step 6 — Material site (`docs/`)
1. `fonts/`: download the three variable `.woff2` files once, commit.
2. `style.css` from `theme.md` §1–§4 plus the page skeleton and media rules.
3. `script.js`: copy buttons (copy `.cmd` lines only, strip prompt), quiz, stepper (arrow keys, play at 3.4s, progress track).
4. A template stage page with dummy content to prove the layout, the nav, a terminal block, a media panel with missing video, a quiz and a stepper. Render at 1366×768 and at phone width. Fix before going on.
5. `reference/` eight pages (spec §6), every example against `students` and this bootcamp's routes.
6. `stage0.html … stage8.html`, each with the 8 sections, Expected output pasted from the Step 2/3 captures, four quiz questions, stepper where listed.
7. `index.html`: what this is, day plan, port plan, links.
8. `troubleshooting.html` (spec §5.5).
9. `videos/README.md`: `stage0.mp4 … stage8.mp4`, length, shot list matching each Task section step for step.
10. `img/`: three Stage 8 placeholder images with descriptive alt text on the page.
- **Check:** serve with `python3 -m http.server 8000`, open every page, no console errors, no request leaves localhost (Network tab filtered). `grep -r "http" docs/` shows only localhost and the one README link.

### Step 7 — This folder
- `scripts/setup.sh` (spec §5.1): OS detect, install `git curl sqlite3|sqlite`, python ≥ 3.12 check, clone or pull `kiet-bootcamp-3`, run `check_env.py`, print next steps. Idempotent.
- `setup.html`: the same steps written out with terminal blocks: what gets installed and why, the one curl line, what success looks like, how to re-run `check_env.py`, how to start the material site, what to do on the day.
- `index.html`: card hub. Preparation (System setup, Material site, GitHub repo), three session sections (Stage 0–2, 3–5, 6–8), a Day 2 note, Reference.
- **Check:** run `setup.sh` in a fresh Ubuntu 24.04 container; run it twice.

### Step 8 — Definition of done
Spec §13, plus:
- Fresh Ubuntu 24.04 and fresh Omarchy: setup online → network off → `check_env.py` → every stage completes from the material site alone.
- 8000, 8080, 8081, 9000 all up at once.
- Stage 8: red Network row and Console error with the CORS line removed, while `curl -i` still returns 200; restored line fixes it.

---

## 5. Conventions carried into every file

- Servers: `--port`, `--db` via a `sys.argv` loop; DB path resolved relative to the server file; start line `Serving on http://localhost:<port>  (DB: <abs path>)  — Ctrl+C to stop`.
- Stubs run before the student touches them; `# TODO (Task N): …` marks the work.
- Student-facing Python uses only Stage 0 constructs. `check.py`, `check_env.py`, `setup.sh` are exempt.
- Every command in the material is literal and copy-pasteable; every Expected output is captured, not typed.
- Terminal blocks name their terminal in the panel caption. Source files shown on a page use the light code block.
- No emoji, no all-caps labels, no shadows, no cool greys, no external URLs.

---

## 6. Session plan

| Session | Stages | Shape |
|---|---|---|
| Morning | 0, 1, 2 | Python deltas from C (~2 h), the database by hand, Python reading it |
| Afternoon | 3, 4, 5 | Watch a server, write one, join it to the database |
| After dinner, until 11:30 pm | 6, 7, 8 | Swap in the big data (short), hand the backend to a browser, look inside the browser |

Stage 2 closes the morning with the students having read rows from their own database; the afternoon opens with the server. Stage 6 is short and sits first after dinner as a warm-up. Day 2 is team presentations and Omarchy customization, not covered here.

---|---|---|
| 1 | 0, 1, 2, 3 | Python deltas from C (~2 h), then the database, then Python reading it, then watching a server without writing one |
| 2 | 4, 5, 6, 7, 8 | Write a server, join it to the database, swap in the big data, hand it to a browser, look inside the browser |

Stage 3 closes Day 1 so that Day 2 opens with writing. Stage 6 is short and sits between the two heavy stages as a breather.

---

## 7. Status — 19 September 2026

Built and verified on this machine (macOS build host; targets untested on a fresh Ubuntu/Omarchy yet):

- **Step 1 data** — three `.sql` files, byte-identical CREATE TABLE, 200 rows / 12 colleges / 8 cities, counts in the header. `gen_data.py` in `build/` regenerates them deterministically.
- **Step 2 servers** — `demo_server.py`, Stage 5 solution; every curl captured literally and pasted into the pages.
- **Step 3 code** — stubs, solutions, nine `check.py`. Each check passes against its solution and fails meaningfully against the stub. No forbidden constructs in student code.
- **Step 4 root** — `check_env.py`, `.gitignore`, `README.md`.
- **Step 5 frontend** — plain `index.html` + `app.js`; all three buttons verified in Chrome; CORS break reproduced (server 200, browser refuses).
- **Step 6 material** — 19 pages, one `style.css`, one `script.js`, local fonts (500 KB), five steppers, 36 quiz questions, video fallback, link check clean.
- **Step 7 hub** — `index.html`, `setup.html`, `scripts/setup.sh` (syntax-checked, not yet run on a fresh VM).

Findings folded into the spec during the build: query values with spaces must be `+`-encoded; `range` added to Stage 0; commenting only the header line of the CORS hook is a syntax error, so Stage 8 comments all three lines.

Still to do, outside this machine:
1. Create the GitHub repo `aikaryashala/kiet-bootcamp-3`, push, enable Pages on `docs/`, point `aikaryashala.com/kiet-bootcamp-3/` at it.
2. Commit this folder in the `kiet` repo so `aikaryashala.com/kiet/bootcamp-03/scripts/setup.sh` resolves.
3. Run `setup.sh` on a fresh Ubuntu 24.04 and a fresh Omarchy; go offline; walk all nine stages from the material alone.
4. Record the nine demo videos per `docs/videos/README.md`; replace the three Stage 8 placeholder PNGs with real screenshots.
