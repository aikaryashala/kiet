"""The online hub in kiet/docs/bootcamp-03/: index.html and setup.html."""
import os
import lib
from lib import *

HUB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MATERIAL = "https://aikaryashala.com/kiet-bootcamp-3/"
GITHUB = "https://github.com/aikaryashala/kiet-bootcamp-3"

HUB_NAV = '''<nav class="nav" aria-label="Pages">
<a href="index.html"{i}>Home</a>
<a href="setup.html"{s}>Setup</a>
<div class="group">On the day</div>
<a href="{m}">Material site</a>
<a href="{g}">GitHub repo</a>
<div class="group">Earlier</div>
<a href="../bootcamp-02/">Bootcamp 2</a>
<a href="../bootcamp-01/">Bootcamp 1</a>
</nav>'''


def hub_page(name, title, body, sub, artifact):
    lib.NAV_OVERRIDE = HUB_NAV.format(i=' class="cur"' if name == "index.html" else "",
                                      s=' class="cur"' if name == "setup.html" else "", m=MATERIAL, g=GITHUB)
    html = page(title, name, body, depth=0, sub=sub, artifact=artifact)
    open(f"{HUB}/{name}", "w", encoding="utf-8").write(html)
    print("wrote hub", name, len(html))


def card(num, href, title, desc):
    return (f'<a class="card" href="{href}"><div class="num">{esc(num)}</div><h3>{esc(title)}</h3>'
            f'<p>{desc}</p><div class="go">Open →</div></a>')


# ---------------------------------------------------------------- index
prep = '<div class="cards">' + "".join([
    card("01 · before the day", "setup.html", "System setup", "One command with internet. Installs the tools and clones the material to your machine."),
    card("02", MATERIAL, "Material site", "The same pages you will serve offline from ~/kiet-bootcamp-3. Read ahead here."),
    card("03", GITHUB, "The repository", "All stage code, data and material. Cloned for you by the setup."),
]) + "</div>"

day1 = '<div class="cards">' + "".join([
    card("Stage 0 · ~2 h", MATERIAL + "stage0.html", "Just enough Python", "C with the ceremony removed. Seven programs, stepped through line by line."),
    card("Stage 1", MATERIAL + "stage1.html", "Data that survives", "SQLite and four SQL verbs. Your team's table, by hand."),
    card("Stage 2", MATERIAL + "stage2.html", "Python talks to the database", "Module, connection, cursor. execute positions, fetchall reads."),
]) + "</div>"

day1b = '<div class="cards">' + "".join([
    card("Stage 3", MATERIAL + "stage3.html", "What a server actually is", "Observe only: a program that waits, poked with curl."),
    card("Stage 4", MATERIAL + "stage4.html", "Write your own server", "Three routes on port 8081."),
    card("Stage 5", MATERIAL + "stage5.html", "Join the two halves", "Unpack, query, pack. The whole backend."),
]) + "</div>"

day2 = '<div class="cards">' + "".join([
    card("Stage 6 · short", MATERIAL + "stage6.html", "Swap the data, not the code", "200 rows, zero lines changed."),
    card("Stage 7", MATERIAL + "stage7.html", "Someone else's client", "A web page calls your backend."),
    card("Stage 8", MATERIAL + "stage8.html", "The inspector", "curl -i with a mouse. Break CORS, fix it."),
]) + "</div>"

refs = '<div class="cards">' + "".join([
    card("ref", MATERIAL + "reference/python-cheatsheet.html", "Python cheatsheet", "Every construct the stages use."),
    card("ref", MATERIAL + "reference/sql-for-students-table.html", "SQL for students", "Every statement, one table."),
    card("ref", MATERIAL + "reference/bottle.html", "Bottle", "route, request, response, run, hook."),
    card("ref", MATERIAL + "reference/curl.html", "curl", "Flags, quoting, + for spaces."),
    card("ref", MATERIAL + "reference/http-basics.html", "HTTP basics", "Request line, status line, three doors."),
    card("help", MATERIAL + "troubleshooting.html", "Troubleshooting", "The messages you will actually see."),
]) + "</div>"

body = "\n".join([
    section("what", "What you will build", p("""A Python program that answers HTTP requests with JSON read from a SQLite database, and a web page
that uses it. You arrive knowing C. One day, three sessions, nine stages, each one idea. Everything runs on your own
machine with the network off — which is why the setup below has to happen <em>before</em> the day.""")),
    section("prep", "Preparation", prep),
    section("day1", "Day 1 · 21 September", (day1 + day1b + day2).replace('</div><div class="cards">', "")),
    section("day2", "Day 2 · 22 September", p("Team presentations of what was built on Day 1, then the Omarchy customization sessions.") + '<div class="cards">' + card("Omarchy", MATERIAL + "omarchy-branding.html", "Make Omarchy yours", "Task 1: your name on the screensaver. Task 2: your photo on the boot and login screens.") + "</div>"),
    section("ref", "Reference", refs),
])
hub_page("index.html", "KIET Bootcamp 3", body,
         sub="Python backend with Bottle + SQLite · 21st & 22nd September 2026 · AI Karyashala",
         artifact="HTTP in  →  SQL in the middle  →  JSON out")

# ---------------------------------------------------------------- setup
body = "\n".join([
    section("need", "What you need", p("""A laptop running Ubuntu 24.04 (a VM is fine) or Omarchy. Internet, once, for the step below. After
that the bootcamp needs no network. If you did the earlier bootcamps, you already have most of it;
run the command anyway — it is safe to repeat.""") +
        p("The script installs three small tools — <code>git</code>, <code>curl</code>, <code>sqlite3</code> — checks that <code>python3</code> is 3.12 or newer, and clones the bootcamp repository to <code>~/kiet-bootcamp-3</code>. Nothing else is installed: no pip, no virtual environment. Bottle, the one library used, is a single file already inside the repository.")),
    section("run", "Run the setup", steps([
        p("Open a terminal and paste this one line. It asks for your password once, for the package install.") +
        term("terminal", """$ curl -sSL https://aikaryashala.com/kiet/bootcamp-03/scripts/setup.sh | bash

==> Installing git, curl and sqlite3
    (sudo will ask for your password: installing packages needs it)
[sudo] password for kiet:

==> Checking python3
    python3 3.12 — ok

==> Cloning into /home/kiet/kiet-bootcamp-3
Cloning into '/home/kiet/kiet-bootcamp-3'...

==> Checking the machine
PASS: python3 is 3.12.3
PASS: curl is on PATH
PASS: sqlite3 command-line tool is on PATH
PASS: bottle.py imports from code/stage3 — 0.13.4
PASS: Python's sqlite3 module works (SELECT 1)
PASS: data/schema.sql is present
PASS: data/sample_team_details.sql is present
PASS: data/all_students.sql is present
PASS: code/frontend/index.html is present (needed in Stage 7)
PASS: docs/index.html is present (the material site)

Ready. Start the material site with:
    cd ~/kiet-bootcamp-3/docs && python3 -m http.server 8000
then open http://localhost:8000 in your browser.

==> Done. On the bootcamp day (no internet needed):

    python3 ~/kiet-bootcamp-3/check_env.py
    cd ~/kiet-bootcamp-3/docs && python3 -m http.server 8000

  and open  http://localhost:8000  in your browser.
"""),
        p("Read the PASS lines. Every line must say PASS except <code>sqlite3 command-line tool</code>, which may say WARN — the material shows the <code>python3 -m sqlite3</code> alternative wherever it matters. A FAIL line says what to do; fix it and run the same command again."),
        p("Prefer to read the script before running it? It is short: <a href=\"scripts/setup.sh\">scripts/setup.sh</a>."),
    ])),
    section("try", "Try the material site now", p("Everything the bootcamp uses is now on your disk. Start the material site and open it — the same pages as <a href=\"" + MATERIAL + "\">" + MATERIAL + "</a>, served from your own machine:") +
        term("terminal", """$ cd ~/kiet-bootcamp-3/docs && python3 -m http.server 8000
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...""") +
        p("Open <code>http://localhost:8000</code>. Leave that terminal running; <kbd>Ctrl+C</kbd> stops it. Read Stage 0 ahead of time if you can — it is the Python you will need on Day 1.")),
    section("day", "On the day", steps([
        p("Run the check again. It needs no network.") + term("terminal", """$ python3 ~/kiet-bootcamp-3/check_env.py
~
Ready. Start the material site with:
    cd ~/kiet-bootcamp-3/docs && python3 -m http.server 8000"""),
        p("Start the material site in one terminal and keep it open all day.") + term("terminal", """$ cd ~/kiet-bootcamp-3/docs && python3 -m http.server 8000"""),
        p("Open <code>http://localhost:8000</code> and begin at Stage 0. You will open two or three more terminals as the stages ask; each page says which terminal a command runs in."),
    ])),
    section("trouble", "If something fails", rules([
        ("<code>curl: command not found</code>", "Install it first: <code>sudo apt install curl</code> (Ubuntu) or <code>sudo pacman -S curl</code> (Arch), then run the setup line."),
        ("<code>python3 is 3.10</code> (or lower)", "You are on an older Ubuntu. The bootcamp needs 3.12, which Ubuntu 24.04 ships. Upgrade, or use the VM image from the earlier setup."),
        ("<code>git clone failed</code>", "No internet, or GitHub blocked on the network you are on. Try another connection and re-run."),
        ("<code>git pull failed</code>", "You edited files inside <code>~/kiet-bootcamp-3</code> after an earlier run. Either <code>cd ~/kiet-bootcamp-3 && git stash</code> or delete the folder, then re-run."),
        ("Windows", "The bootcamp targets Linux. Set up the Ubuntu VM from <a href=\"https://aikaryashala.com/system_setup/\">aikaryashala.com/system_setup</a> first, then run the setup line inside it."),
    ])),
])
hub_page("setup.html", "System setup", body,
         sub="One command, with internet, before the bootcamp. After it, nothing needs the network.",
         artifact="curl -sSL https://aikaryashala.com/kiet/bootcamp-03/scripts/setup.sh | bash")
