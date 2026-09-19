# KIET Bootcamp #3 — Python Backend with Bottle + SQLite

**Spec for building the bootcamp repository. Read fully before writing any file.**

---

## 1. Purpose

Students with a C background, no Python and no web experience, build — in one guided day, 21 September 2026, in three sessions (morning, afternoon, after dinner until 11:30 pm) — a working HTTP backend in Python that serves JSON from a SQLite database, and then watch a browser frontend consume it.

Two deliverables come out of this spec:

| Where | Purpose | Used |
|---|---|---|
| `aikaryashala/kiet-bootcamp-3` | Material website (`docs/`) + all stage code (`code/`, including the Stage 7 frontend in `code/frontend/`) + data | cloned to `~/kiet-bootcamp-3` by `scripts/setup.sh` before the bootcamp (online), then used offline from `http://localhost:8000`. The same `docs/` is also hosted at `https://aikaryashala.com/kiet-bootcamp-3/` |
| `aikaryashala/kiet` → `docs/bootcamp-03/` (this folder) | Online hub page + setup page + `scripts/setup.sh` | online only, before the bootcamp; nothing here is needed on the day |

The bootcamp repo is built as a sibling directory in the workspace, as its own git repo. The hub lives in this repo next to `bootcamp-01/` and `bootcamp-02/`, and is published at `https://aikaryashala.com/kiet/bootcamp-03/`.

## 2. Hard constraints

1. **Offline on bootcamp day.** After `setup.sh` runs once (online), nothing may need the network. No pip, no CDN links, no Google Fonts, no external images. Fonts ship as local `.woff2` files in `docs/fonts/` (theme.md §2).
2. **Only `python3` (≥ 3.12), `curl`, `git`, and optionally the `sqlite3` CLI.** Bottle is used by copying `bottle.py` (single file, version 0.13.x) into every folder that has a server. No venv, no PYTHONPATH tricks, no `sys.path` edits.
3. **Target OS:** Ubuntu 24.04 (VM) and Omarchy (Arch-based). Scripts must handle both (`apt` / `pacman`).
4. **Beginner-honest code.** Given code uses only the Python constructs taught in Stage 0 (see §7). No classes, list comprehensions, `try/except`, `with`, `if __name__ == "__main__"`, lambdas, type hints, f-string format specs, `*args`. If a construct isn't in the Stage 0 list, don't use it in student-facing code. `check.py` scripts and `setup.sh` are exempt (students only run them).
5. **Every command in the material is copy-pasteable and exact.** Expected outputs are literal, not described.

## 3. Decisions taken (defaults — change here, nothing else needs to move)

| Item | Decision |
|---|---|
| Table | `students(student_name TEXT, inter_college TEXT, inter_city TEXT)` — three columns, no id |
| Team DB | `data/team_details.db`, created by students in Stage 1, one per team (team = the students sharing one machine) |
| Big DB | `data/all_students.db`, built in Stage 6 from `data/all_students.sql` |
| Ports | 8000 material site · 8080 given servers (Stage 3, 5, 6) · 8081 student's own server (Stage 4) · 9000 frontend (Stage 7, 8) |
| Clone location | `~/kiet-bootcamp-3` — one clone holds everything |
| Dates | 21 September 2026, three sessions: morning Stage 0–2 · afternoon Stage 3–5 · after dinner (until 11:30 pm) Stage 6–8. 22 September is team presentations and Omarchy customization, not covered by this material. |
| Frontend styling | Plain HTML, no theme, no fonts, one short `<style>` block. It is "someone else's client"; theme.md does not apply to it. |
| Setup script | `scripts/setup.sh` in this folder, run from `https://aikaryashala.com/kiet/bootcamp-03/scripts/setup.sh`. Not in the student repos. |
| Self-check | every stage has a `check.py` printing PASS/FAIL lines |
| Demo videos | none. No video, no screenshot placeholders; the pages stand on their own. |
| Solutions | every task has a solution in `code/stageN/solution/`; material links to it under "Stuck? Compare with the solution" |
| Look and feel | `theme.md` in this folder is the visual system. Where this spec and theme.md disagree on appearance, theme.md wins. |

## 4. Repository layout — `kiet-bootcamp-3/`

`code/` and `docs/` sit side by side so that one clone gives the student both the material and the files it talks about, with no network. `docs/` is also what GitHub Pages publishes.

```
kiet-bootcamp-3/
├── README.md                     # 5 lines: what, link to the hub setup page, cd docs && python3 -m http.server 8000
├── check_env.py                  # §5.2
├── .gitignore                    # data/*.db, __pycache__/
├── data/
│   ├── schema.sql                # CREATE TABLE only
│   ├── sample_team_details.sql   # schema + 5 sample rows (for anyone who skipped Stage 1)
│   └── all_students.sql          # schema + ~200 rows (§10, Stage 6)
├── docs/                         # material site, served offline by python3 -m http.server 8000
│   ├── index.html                # landing page: what this is, port plan, day plan, links to stage0..stage8
│   ├── style.css                 # the one stylesheet, from theme.md; no inline styles in pages
│   ├── script.js                 # the one script: copy buttons, quiz, stepper (§5.6, §5.7)
│   ├── fonts/                    # Fraunces, Inter Tight, JetBrains Mono as .woff2 (theme.md §2)
│   ├── stage0.html … stage8.html
│   ├── troubleshooting.html
│   └── reference/
│       ├── python-cheatsheet.html
│       ├── c-to-python.html
│       ├── sqlite-cli.html
│       ├── sql-for-students-table.html
│       ├── json.html
│       ├── bottle.html
│       ├── curl.html
│       └── http-basics.html
└── code/
    ├── stage0/   exercises 01..07 + solution/
    ├── stage1/   check.py
    ├── stage2/   read_all.py  by_college.py (stub)  check.py  solution/
    ├── stage3/   bottle.py  demo_server.py  curl_commands.txt  check.py
    ├── stage4/   bottle.py  server.py (stub)  check.py  solution/
    ├── stage5/   bottle.py  server.py (partial)  check.py  solution/
    ├── stage6/   check.py   (uses stage5 server with --db)
    ├── stage7/   check.py   (verifies 9000 serves the frontend, 8080 answers)
    ├── stage8/   check.py   (verifies the CORS header on 8080)
    └── frontend/ index.html  app.js  README.md   (§11, served on 9000 in Stage 7 and 8)
```

### 4.1 Code conventions (apply everywhere)

- Servers accept `--port N` and `--db PATH` via `sys.argv` scanning (simple loop, no argparse). Defaults: port per §3, db `../../data/team_details.db` **resolved relative to the server file** (`os.path.dirname(os.path.abspath(__file__))`) so running from any directory works.
- Every server prints on start: `Serving on http://localhost:<port>  (DB: <absolute db path>)  — Ctrl+C to stop`.
- Bottle's `run(host="localhost", port=..., debug=True)`; debug so request lines print in the terminal (students watch this).
- Student stubs mark work with `# TODO (Task N): ...` comments and contain enough scaffolding that the file runs before they start.
- `check.py` scripts use only the standard library (`urllib.request`, `json`, `sqlite3`). They print one line per check, `PASS: <what>` or `FAIL: <what> — expected X, got Y`, and end with a summary. They must give an actionable message if the server isn't running (`Cannot connect to localhost:8081 — is the server running?`).
- Given servers include a CORS hook from Stage 5 onwards (see §9 Stage 5), with the comment `# This line matters in Stage 8. Ignore it for now.`

## 5. Cross-cutting components

### 5.1 `setup.sh` and the hub (this folder)

`setup.sh` lives in this repo at `docs/bootcamp-03/scripts/setup.sh` and is run once, online:

```
curl -sSL https://aikaryashala.com/kiet/bootcamp-03/scripts/setup.sh | bash
```

It is deliberately not inside the student repos: nothing a student uses offline should depend on it, and it can be fixed without touching the material.

This folder (`docs/bootcamp-03/`) holds, in the same card-hub style as `bootcamp-02/index.html`:

- `index.html` — hub. Header "KIET Bootcamp #3, 21st & 22nd Sep 2026". Sections: **Preparation** (System setup → `setup.html`; Material → `https://aikaryashala.com/kiet-bootcamp-3/`; the repo on GitHub), **Session 1 · morning**, **Session 2 · afternoon**, **Session 3 · after dinner** (one card per stage, linking into the published material), a one-line **Day 2** note (presentations, Omarchy), **Reference**.
- `setup.html` — the setup steps written out on the page itself, not only in the script: what gets installed and why, the one `curl … | bash` line, what the script prints when it succeeds, how to re-run `check_env.py`, and how to start the material site. Terminal blocks per theme.md.
- `scripts/setup.sh` — the script below.
- `spec.md`, `theme.md` — this spec and the visual system (not linked from the hub).

The script:

1. Detect OS via `/etc/os-release` (`ID=ubuntu` → apt; `ID=arch` or `ID_LIKE` contains `arch` → pacman). Unknown → print message, continue without package install.
2. Install `git curl sqlite3` (Ubuntu) / `git curl sqlite` (Arch). Requires sudo — print one line explaining why before prompting.
3. Check `python3 --version` ≥ 3.12; if lower, stop with a clear message.
4. `git clone https://github.com/aikaryashala/kiet-bootcamp-3 ~/kiet-bootcamp-3`, or `cd` + `git pull` if it exists.
5. Run `python3 ~/kiet-bootcamp-3/check_env.py`.
6. Print next steps: `cd ~/kiet-bootcamp-3/docs && python3 -m http.server 8000` → open `http://localhost:8000`.
7. Idempotent: safe to run twice.

### 5.2 `check_env.py`

Prints a PASS/FAIL table for: python3 version, `curl` on PATH, `sqlite3` CLI on PATH (FAIL here is non-fatal — prints the `python3 -m sqlite3` fallback), `import bottle` from `code/stage3`, open an in-memory SQLite DB and run `SELECT 1`, `code/frontend/index.html` exists (warn only). Exit code 0 only if the fatal ones pass. Students re-run this on bootcamp day.

### 5.3 Material site (`docs/`)

- Plain HTML + one `style.css` + one `script.js`, all in `docs/`. No library. The script does three things only: copy buttons on terminal blocks, the quiz (§5.6), the stepper (§5.7). Pages carry no inline `<style>` or `<script>`.
- Look and feel exactly per `theme.md`: colour tokens, local fonts, flat surfaces, hairline borders, page wraps at 1040px, prose at 70ch, 16px base. Readable on a 1366×768 VM screen.
- Left nav on every page (theme.md §4 "Left nav"): Stage 0 → 8, Reference, Troubleshooting. Current page in rust.
- **Every stage page has exactly these sections, in order** (theme.md §5 is the same list with the CSS):
  1. **Concept** — the one new idea, hooked to C or to the previous stage. 200–400 words. Use the wording in §7–§9 as the basis. Stages listed in §5.7 also carry a stepper visualization here.
  2. **Task** — numbered steps. Each command in a terminal block (theme.md §4 "Terminal block"): dark panel, `pre.term`, one `.ln.cmd` per command with the `$ ` prompt in `.p`. The panel caption names the terminal (`terminal 1 — server`, `terminal 2 — curl`).
  3. **Expected output** — the literal output as plain `.ln` lines in the same terminal block, directly under the command that produces it. Source files shown on the page use the light `pre.code` block with `.ln` lines, never the dark one.
  4. **Check yourself** — the `python3 check.py` command and what all-PASS looks like, one terminal block.
  5. **Takeaway** — 1–3 sentences in a `.callout`.
  6. **Stuck?** — link to the solution folder and the relevant reference pages.
  7. **Quiz** — four questions (§5.6).
- Commands and output are told apart only by the prompt symbol and colour inside one transcript, exactly as the student's own terminal shows them.

### 5.5 Troubleshooting page

Address already in use (how to find and kill: `lsof -i :8080` / `fuser -k 8080/tcp`), `sqlite3: command not found` → `python3 -m sqlite3`, `ModuleNotFoundError: bottle` → you're in the wrong folder, `connection refused` → server not running, `no such table` → you're pointing at the wrong `.db` file, indentation errors, Windows line endings if they edited on another machine, how to stop a server (Ctrl+C) and what happens if you close the terminal instead, CORS error text and what it means.

### 5.6 Quiz

Every stage page ends with four questions, styled per theme.md §4 "Quiz". Rules:

- Each question has 3 or 4 options as buttons, exactly one correct. Click to answer: correct turns teal and reveals a one- or two-sentence explanation; a wrong pick turns rust and the correct one also lights teal, with the same explanation.
- Questions test the Concept and the Takeaway of that stage, not trivia. At least one question per stage shows a command or a line of code and asks what it does or what it prints.
- No score, no storage, no "try again". Answering is the whole interaction.
- Markup is data-driven so `script.js` stays generic: `<div class="quiz">` containing `<div class="q" data-answer="2">` with a `<p>`, the `<button class="opt">`s, and a `<p class="exp">`.

### 5.7 Stepper visualization

Some Concept sections carry a stepper (theme.md §4 "Stepper controls"): a two-column panel where the left side shows code or a transcript with one `.ln.on` active line and the right side shows state slots or a data table, plus Back / Play / Forward, a progress track, and narration in a fixed-min-height block. Arrow keys mirror the buttons. Steps are plain data in the page (`<script type="application/json" class="steps">`), and `script.js` drives them.

| Stage | Stepper shows |
|---|---|
| 1 | `SELECT … WHERE` walking the `students` rows: current row rust, non-matching rows `.skip`, result table filling on the right |
| 2 | `read_all.py` line by line: connection → cursor → `execute` (nothing returned) → `fetchall` (list of tuples appears in a slot) → loop |
| 3 | one `curl` request: request line, path / query string / body highlighted as the three doors, then the server log line and the response |
| 5 | one `/students?college=X` call through unpack → query → pack → return, the dict growing in a slot |
| 8 | a `curl -i` transcript on the left, active line moving down; on the right the Network tab fields (Request URL, Request Method, Status Code, response headers, Response body) lighting up as their `curl -i` line becomes active |

Stages 0, 4, 6 and 7 have no stepper; their Concept is prose only.

## 6. Reference pages (`docs/reference/`)

Each is a one-screen page: short explanation, then copy-pasteable examples using **this bootcamp's schema and routes**, nothing generic.

| Page | Contents |
|---|---|
| `python-cheatsheet` | variables, strings, f-strings, `print`, lists, tuples, unpacking, dicts, `.get`, `for`, `if/elif/else`, `def/return`, `%`, `int()`, `import`, `sys.argv`, `None` |
| `c-to-python` | the translation table from §7 |
| `sqlite-cli` | open, `.tables`, `.schema`, `.headers on`, `.mode column`, `.quit`, `.read file.sql`, running a `.sql` file via `<`, and `python3 -m sqlite3` fallback |
| `sql-for-students-table` | CREATE TABLE, INSERT (single and multi-row), SELECT *, SELECT columns, WHERE with `=`, `AND`, `LIKE`, `DISTINCT`, `COUNT(*)`, `ORDER BY`, UPDATE, DELETE — every example against `students` |
| `json` | syntax, types, Python dict ↔ JSON, `json.dumps`, `json.loads`, nested list of dicts |
| `bottle` | `@route`, path params `<name>`, `request.query.get()`, `request.json`, `method="POST"`, returning str vs dict, `response.status`, `run()`, `@hook('after_request')` |
| `curl` | `curl URL`, `-i`, `-X POST`, `-H "Content-Type: application/json"`, `-d '{...}'`, quoting URLs with `&`, spaces as `+`, `-s` |
| `http-basics` | request line, methods GET/POST, path vs query string vs body, status codes 200/400/404/500, headers, `Content-Type` |

## 7. Stage 0 — Just Enough Python (intro session, ~2 hrs)

**Audience premise:** they know C. Teach Python as deltas from C. Cover only what Stages 1–7 use.

Page structure: same sections as other stages, but the Task section is seven blocks, each with one **complete** example program in `code/stage0/` and a **stepper** that walks it line by line — the active line on the left, the variables and the output appearing on the right. Nothing is written in Stage 0: students step through, then run the file and see the same output. Each file has a header comment stating what it shows and the expected output. No stubs, no solution folder.

| Block | Teach | Exercise file | Feeds |
|---|---|---|---|
| 1 Running a program | `python3 file.py`, no compile/main/semicolons/braces, indentation = block, `x = 5` no types, `print`, f-strings | `01_hello.py` — print name and college | Stage 4 `/hello/<name>` |
| 2 Lists & tuples | `[]`, `len`, `.append`, `for x in items`, `range(n)` and `range(a, b)` as the C counting loop, tuple, unpacking `a, b, c = row`; **SQLite rows are tuples, `fetchall()` is a list of tuples** | `02_rows.py` — list of 3 tuples, print `name — city` | Stage 2 |
| 3 Dicts | `{"k": v}`, `d["k"]`, `d.get("k")` → `None`, a dict *is* JSON; `json.dumps`; **Bottle returns dict as JSON** | `03_dicts.py` — convert the tuples into a list of dicts, print `json.dumps(result)` | Stage 5 response packing |
| 4 Functions, if, % | `def`/`return`, no prototypes, `if/elif/else`, `and`, `==`, `%`, `int("17")` | `04_prime_even.py` — `is_prime(n)`, `is_even(n)` | Stage 3/4 POST routes |
| 5 Imports & argv | `import sys`, `sys.argv` (list of strings, `[0]` is file), `import sqlite3`, `from bottle import route, run`; module = stdlib or a file beside yours | `05_greet.py` — `python3 05_greet.py Ravi` | Stage 2 `by_college.py` |
| 6 Two strange things | decorators: `@route("/hai")` = "register this function at this address", nothing more; `None` and `if x is None:` guard | `06_read_only.py` — a 15-line Bottle server to read and annotate in comments, not run | Stage 3 |
| 7 Put it together | hard-coded list of tuples → filter by city with `if` → list of dicts → `print(json.dumps(...))` | `07_filter_pack.py` | Stage 5 minus SQL minus HTTP |

**C → Python table** (also the `c-to-python` reference page):

| C | Python |
|---|---|
| `int x = 5;` | `x = 5` |
| `{ ... }` | indentation |
| `int arr[3]` | `arr = [1, 2, 3]` |
| `struct` | dict |
| `printf("%s", s)` | `print(f"{s}")` |
| `for (i=0; i<n; i++)` | `for i in range(n):` |
| `for each element` | `for x in items:` |
| `strcmp(a, b) == 0` | `a == b` |
| `atoi(s)` | `int(s)` |
| `#include` | `import` |
| `NULL` | `None` |
| `argv` | `sys.argv` |
| `return 0;` at end of main | nothing |

**Deliberately not covered** (state this on the page, as a "later list"): classes, list comprehensions, try/except, `with`, `__name__`, lambdas, type hints, venv/pip.

`check.py` for Stage 0 runs each example and compares stdout to the expected output — a smoke test that python3 on the machine behaves as the page shows.

## 8. Stage template — concept wording

The Concept sections below are the seed text. Expand each to 200–400 words in the same voice: concrete, C-anchored, no jargon before the thing it names.

## 9. Stages 1–7

### Stage 1 — Data that survives: SQLite and SQL

**Concept.** Start from an array of structs. Close the program, data gone; write to a file; search needs a loop; add a field, rewrite everything; two programs, more code — none of it about your problem. A table is a struct array that lives in a file and does its own searching. A database is a file holding tables plus the search/add/update code. SQLite: one ordinary file, no server, already inside Python and your phone. SQL: four verbs for now — CREATE TABLE (define the struct), INSERT (append), SELECT…WHERE (the loop with the if inside), UPDATE/DELETE later. `SELECT * FROM students WHERE inter_city = 'Vizag'` *is* the for-loop with `strcmp`. Do not mention: relational, ACID, primary keys, joins, normalisation.

**Given.** `data/schema.sql`.

**Task** (Terminal 1, in `~/kiet-bootcamp-3/data`):
1. `sqlite3 team_details.db` (fallback `python3 -m sqlite3 team_details.db`)
2. Paste the CREATE TABLE from `schema.sql`.
3. INSERT one row per team member (name, inter college, city) — their real details.
4. `SELECT * FROM students;`
5. `.headers on` / `.mode column`, repeat.
6. `SELECT student_name FROM students WHERE inter_city = '<one of their cities>';`
7. `.quit`, `ls -l` — see `team_details.db`.
8. Reopen, `SELECT COUNT(*) FROM students;` — data survived.

**Expected output.** Show literal outputs for a 4-row example team (use the names from `sample_team_details.sql`).

**Check.** `python3 ../code/stage1/check.py` — verifies the file exists, table exists with the 3 columns, ≥ 3 rows, no empty strings.

**Takeaway.** "A database is a file that stores tables and does the searching for you. SELECT…WHERE is the for-loop with the if inside it."

### Stage 2 — Python talks to the database

**Concept.** A program can send SQL and get rows back. Three objects: the `sqlite3` module (the driver — like `stdio.h`), the connection (the open file — like `FILE*`), the cursor (where you run queries and read results — like the file position). `execute` *positions*, it does not return rows; `fetchall` reads them, as a list of tuples. Never paste values into SQL strings — use `?`, so the same query serves different data.

**Given.** `read_all.py` — connect, execute `SELECT`, loop and print `name - college - city` (plain hyphens, so the student can type the same). Both Stage 2 scripts accept an optional extra argument: the DB path (`read_all.py [db]`, `by_college.py <college> [db]`); `check.py` uses it to point them at a temp DB. `by_college.py` stub — reads `sys.argv[1]`, has the connection lines, `# TODO (Task 2): execute the query with ? and print each student_name`.

**Task.** Run `read_all.py`; complete `by_college.py`; run it with a college name from their DB, then with a college not in the DB (prints nothing — that's correct).

**Expected output.** Literal for the sample team.

**Check.** `check.py` runs `by_college.py` against `sample_team_details.sql` loaded into a temp DB and compares stdout.

**Takeaway.** "execute positions, fetch reads. Values go in through `?`, never into the string."

### Stage 3 — What a server actually is (observe only)

**Concept.** A server is a program that waits. A client sends a request: method, path, maybe query string, maybe body. The server replies: status code + content. Nothing is written in this stage — the point is to *see* both sides at once: Terminal 1 shows the server logging each request, Terminal 2 shows curl's view. Three places data can arrive: in the path, after the `?`, or in the body; the route decides which.

**Given.** `demo_server.py` on port 8080:

| Route | Response |
|---|---|
| `GET /hai` | text `Namasthey!!!` |
| `GET /hello/<name>` | text `How are you doing <name>` |
| `POST /isprime`, body `{"number": 17}` | `{"number": 17, "is_prime": true}`; missing/invalid → status 400, `{"error": "send JSON like {\"number\": 17}"}` |
| `GET /greet?name=Ravi&lang=te` | `{"greeting": "Namasthey Ravi", "lang": "te"}`; `lang=en` → `Hello Ravi`; `lang` missing → `te`; `name` missing → 400 `{"error": "name is required"}` |

`curl_commands.txt` — the exact commands below, one per line, with a comment above each.

**Task.** Terminal 1: `python3 demo_server.py`. Terminal 2: run each curl, then the extras: `curl -i localhost:8080/hai` (see headers), `curl localhost:8080/nothing` (404), stop the server with Ctrl+C and curl again (`connection refused`), restart.

```
curl localhost:8080/hai
curl localhost:8080/hello/Ravi
curl -X POST localhost:8080/isprime -H "Content-Type: application/json" -d '{"number": 17}'
curl -X POST localhost:8080/isprime -H "Content-Type: application/json" -d '{"number": 18}'
curl "localhost:8080/greet?name=Ravi&lang=te"
curl "localhost:8080/greet?name=Ravi&lang=en"
```

**Expected output.** Literal curl outputs and the matching server log lines (`127.0.0.1 - - [..] "GET /hai HTTP/1.1" 200 12`).

**Check.** `check.py` hits all four routes plus the 404 and 400 cases.

**Takeaway.** "Path, query string, body — three doors into the server. The terminal on the left is the server's view; the one on the right is the client's."

### Stage 4 — Write your own server

**Concept.** A route is a function with an address. `@route("/hai")` says "when this path is asked for, call this function". Return a string → text response; return a dict → Bottle sends JSON automatically. Path parameters become function arguments. `request.json` gives the parsed body. Port 8081 so it can run alongside the Stage 3 server.

**Given.** `server.py` stub on port 8081 with `/hai` → `Namasthey!!!` working, plus TODO blocks for the three tasks with signatures in place.

**Task.**
1. `GET /wish/<name>` → `Good morning <name>` (different text from Stage 3 on purpose).
2. `POST /iseven`, body `{"number": 4}` → `{"number": 4, "is_even": true}`.
3. `GET /about` → their own details: `{"student_name": "...", "inter_college": "...", "inter_city": "..."}` — hard-coded, the exact three keys of the table.
4. Run both servers at once (Stage 3 on 8080, theirs on 8081); curl each to see two programs answering.

**Expected output.** Four curls, literal.

**Check.** `check.py` on 8081 — checks the three routes and that `/about` has exactly those three keys with non-empty strings.

**Takeaway.** "A server is a set of functions; HTTP is how someone else calls them. Return a dict and it's already JSON."

### Stage 5 — Join the two halves

**Concept.** This is the whole backend in one function: unpack the request (`request.query.get("college")`) → run SQL with `?` (Stage 2) → pack the rows into a list of dicts (Stage 0 block 7) → return it (Stage 4). Missing parameter → status 400 with an error dict. Read the given route line by line before writing anything.

**Given.** `server.py` on port 8080, `--db` defaults to `data/team_details.db`, containing:
- a helper `def query(sql, params):` that opens the connection, executes, fetches, closes, returns the rows (students reuse it; it's the only function they don't write),
- a helper `def pack(rows):` → list of dicts with the three keys,
- `GET /students?college=X` → `{"count": n, "students": [ {student_name, inter_college, inter_city}, … ]}`; missing param → 400 `{"error": "college parameter is required"}`,
- the CORS hook:
  ```python
  @hook('after_request')
  def allow_browser():
      response.headers['Access-Control-Allow-Origin'] = '*'   # This line matters in Stage 8. Ignore it for now.
  ```
- TODO blocks for the four tasks.

**Task** — four new GET routes, different paths and parameters:
1. `GET /students/by-location?location=Y` → same shape as the given route.
2. `GET /students/search?college=X&location=Y` → both required, `WHERE inter_college = ? AND inter_city = ?`.
3. `GET /colleges` → `{"colleges": ["...", "..."]}` — the `row[0]` loop and the return are given in the stub; the only TODO is the SQL, `SELECT DISTINCT inter_college … ORDER BY inter_college`.
4. `GET /count?college=X` → `{"college": "X", "count": n}` — unpack, guard and the `rows[0][0]` return are given; the only TODO is the SQL, `SELECT COUNT(*) …`. Until written, the route answers 500 (empty SQL, one binding) and the page says so.

Curl list for all five routes, using values from their team DB. **Spaces in a query value are written as `+`** (`college=Narayana+Junior+College`): curl rejects a URL with a space, and the browser does the same encoding for you. The `curl` and `http-basics` reference pages say this; Stage 5's Task says it before the first curl.

**Expected output.** Literal for the sample team.

**Check.** `check.py` loads `sample_team_details.sql` into a temp DB, starts nothing — instead prints the command to start the server against that temp DB, then checks all five routes and the 400s.

**Takeaway.** "Every endpoint is unpack → query → pack. You have now written all three."

### Stage 6 — Swap the data, not the code

**Concept.** The server never knew which file it read; only the schema mattered. A `.sql` file is a script of statements — the database's equivalent of a `.c` source file; running it builds the `.db` the way compiling builds the binary.

**Given.** `data/all_students.sql` (§10).

**Task.**
1. `cd data && sqlite3 all_students.db < all_students.sql` (fallback with `python3 -m sqlite3` + `.read`).
2. `sqlite3 all_students.db "SELECT COUNT(*) FROM students;"`.
3. Restart the Stage 5 server: `python3 server.py --db ../../data/all_students.db`.
4. Same curls; `/colleges` now returns ~12 names, a city query returns dozens of rows.
5. Try a college name that exists in the big DB but not in their team DB.

**Expected output.** Literal counts from `all_students.sql`.

**Check.** `check.py` verifies `all_students.db` row count and that the server on 8080 is serving it (`/colleges` length matches).

**Takeaway.** "Code depends on the shape of the data, not the data itself. Zero lines changed."

### Stage 7 — Someone else's client: the browser

**Concept.** The backend is now a service. A program you didn't write — a web page — will call it. Two servers on one machine need two ports: 8080 backend, 9000 frontend. The page does exactly what curl did: it builds a URL, sends a GET, reads JSON. `app.js` is short and every `fetch` has the curl command it replaces written above it in a comment. The page's own **Request log** panel prints method, URL, status and time for each click — the same four things you read off `curl -i`. Watch Terminal 1: the server cannot tell curl and the browser apart.

**Given.** `code/frontend/` (§11).

**Task.**
1. Terminal 1: Stage 5 server with `--db ../../data/all_students.db` on 8080.
2. Terminal 2: `cd ~/kiet-bootcamp-3/code/frontend && python3 -m http.server 9000`.
3. Browser: `http://localhost:9000`. The College dropdown is already filled — that was `GET /colleges` on page load. Pick a college, click **Fetch by college** — the table fills, the Request log gets one line.
4. Type a city, click **Fetch by location**; then both, **Search both**. Three lines in the Request log: `/students`, `/students/by-location`, `/students/search`.
5. Terminal 3: `curl -s "localhost:8080/students?college=…"` with the same college — the JSON the table was built from.
6. Watch Terminal 1: the server log lines are identical whether curl or the browser made the request.
7. Open `app.js` in an editor. Read the comment above each `fetch`. Do not change anything.

**Expected output.** The Request log lines, the curl JSON, and the literal server log lines.

**Check.** `check.py` verifies 9000 serves `index.html` and `app.js`, and 8080 answers `/colleges`.

**Takeaway.** "A backend is finished when a program you didn't write can use it. The frontend is curl with buttons."

### Stage 8 — The inspector: curl -i with a mouse

**Concept.** Every browser has curl's `-i` view built in — the **Network** tab of the inspector. One row per request; click a row and you get **Headers** (Request URL, Request Method, Status Code, the request and response headers) and **Response** (the body). Those are exactly the lines `curl -i` prints, in the same order. The **Console** tab is where the browser prints errors the page didn't handle. One new thing lives only in the browser: a page served from port 9000 is not allowed to read a response from port 8080 unless the server says so. That is the `Access-Control-Allow-Origin` line from Stage 5; curl never checked it, the browser always does.

**Given.** Everything from Stage 7 still running.

**Task.**
1. Browser: open the inspector (F12 or Ctrl+Shift+I) → **Network** tab. Click **Fetch by college** again.
2. Click the `students?college=…` row → **Headers**: Request URL, Request Method, Status Code. Scroll: Response Headers include `Content-Type: application/json` and `Access-Control-Allow-Origin: *`.
3. **Response** sub-tab: the JSON.
4. Terminal 3: `curl -i "localhost:8080/students?college=…"` — same status line, same headers, same body. Put the terminal and the inspector side by side.
5. Click **Fetch by location** and **Search both** — two more rows; open each, read the Request URL.
6. **Break it on purpose:** in `code/stage5/server.py` put a `#` in front of **all three lines** of the `allow_browser` hook (the `@hook` line, the `def` line, and the header line — commenting only the header line leaves an empty function and Python refuses to start: `IndentationError: expected an indented block`). Restart the server, click **Fetch by college**. The table does not change, the yellow banner appears, the Request log says `FAILED`. Network tab: the row is red, status `(failed)` or `CORS error`. **Console** tab: `Access to fetch at 'http://localhost:8080/students?college=…' from origin 'http://localhost:9000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.` followed by `TypeError: Failed to fetch`. Terminal 1: the server logged `200` — it answered; only the browser refused to hand the page the answer. Terminal 3: `curl -i` still works. Remove the three `#`s, restart, click again. This is the only time the material shows an error deliberately.
7. Watch Terminal 1 during all of it: the log lines never changed, even during step 6.

**Expected output.** the literal `curl -i` output; the literal Console error text; the literal server log lines.

**Check.** `check.py` verifies 8080 answers `/colleges` **with** the `Access-Control-Allow-Origin: *` header, and prints the `curl -i` command for the student to compare by eye.

**Takeaway.** "curl and the browser are the same client wearing different clothes. The Network tab is `curl -i` with a mouse; CORS is the one rule only the browser enforces."

## 10. Sample data

- `sample_team_details.sql`: 4 students, 2 colleges, 2 cities — used in every Expected Output.
- `all_students.sql`: 200 rows. 12 intermediate colleges commonly known in Andhra Pradesh (e.g. Sri Chaitanya, Narayana, NRI, Bhashyam, Tirumala, Vignan, Sri Gayatri, Krishnaveni, Sasi, Sri Prakash, Aditya, Government Junior College), 8 cities (Visakhapatnam, Vijayawada, Guntur, Kakinada, Rajahmundry, Nellore, Tirupati, Kurnool). Realistic Telugu names, no duplicates, uneven distribution (so COUNT results differ). Include exactly one college that appears in only one city and one city with only one college — useful for search exercises. Document the exact counts in a comment at the top of the file so Expected Output sections can quote them.
- Same `CREATE TABLE` text in all three `.sql` files, byte-identical.

## 11. Frontend — `code/frontend/`

```
code/frontend/
├── README.md        # run: python3 -m http.server 9000 from this folder; backend must be on 8080
├── index.html       # plain HTML; one <style> block of at most 30 lines
└── app.js
```

- Vanilla HTML/JS, no build step, no CDN, no fonts, no theme. Works from `file://` and from `http.server`. Deliberately plain: default browser fonts, a bordered table, a `<pre>` for the request log. The page must look like something a student could have written after this bootcamp; every line of it is meant to be read. `theme.md` does not apply here.
- `app.js` line 1: `const BACKEND = "http://localhost:8080";` with a comment saying this is the only line to change.
- UI: title "KIET Students — Frontend for your backend"; a **College** dropdown filled from `GET /colleges` on page load; a **Location** text input; three buttons: **Fetch by college** (`/students?college=`), **Fetch by location** (`/students/by-location?location=`), **Search both** (`/students/search?college=&location=`); a results table (student_name, inter_college, inter_city) with a row count; a **Request log** panel below listing, per click: method, full URL, status, time in ms — deliberately mirroring `curl -i`.
- On page load, if `/colleges` fails, show a visible banner: *"Cannot reach the backend at http://localhost:8080 — is your Stage 5 server running? Open the Console tab for details."* — this is intended: the frontend only works once Stage 5 is complete.
- Use `fetch` with `.then`; keep `app.js` under 120 lines and heavily commented — students will read it, even though it's JavaScript. Comments map each `fetch` to the curl command it replaces.

## 12. Build order

1. `data/` SQL files (everything else quotes their contents).
2. `code/stage3/demo_server.py` and `code/stage5/solution/server.py` — the two reference servers; then derive stubs.
3. Remaining `code/` stages + solutions + `check.py` for each.
4. `check_env.py`, `.gitignore`, `README.md`.
5. `code/frontend/`.
6. `docs/` — `style.css` from theme.md and `script.js` first, fonts downloaded once into `fonts/`, then reference pages (stage pages link to them), then stage0–8, index, troubleshooting.
7. This folder: `scripts/setup.sh`, `setup.html`, `index.html`.
8. Run §13.

## 13. Definition of done

- [ ] Fresh Ubuntu 24.04 and fresh Omarchy: the `curl … | bash` line from `setup.html` online → disconnect network → `check_env.py` passes → every stage completes using only the material site.
- [ ] Every `check.py` passes against its `solution/` and fails meaningfully against the untouched stub.
- [ ] Every command in `docs/` was run and its Expected Output block is the literal captured output (with the sample data).
- [ ] `grep` the student-facing code for the forbidden constructs in §2.4 — none present.
- [ ] Both servers (8080 + 8081), the material site (8000) and the frontend (9000) run simultaneously on one machine.
- [ ] Stage 7: the three buttons produce three Request log lines and three matching server log lines.
- [ ] Stage 8: Network tab shows the three requests with Headers and Response; removing the CORS line produces the Console error and a red row while `curl -i` still succeeds; restoring it fixes it.
- [ ] No file in the student repo references a URL other than `localhost`, except the README line pointing at the hub setup page.
- [ ] No page has an inline `<style>` or `<script>` block, a `style=` attribute, or a `<link>`/`<script src>` pointing anywhere but `style.css` / `script.js`.
- [ ] Every stage page has exactly four quiz questions and each answers correctly; the five steppers in §5.7 step forward, back, play, and respond to arrow keys.
- [ ] Every stage page renders with the same look with the network disconnected (fonts load from `fonts/`).
