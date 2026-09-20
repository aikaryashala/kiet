from lib import *


def card(num, href, title, desc):
    return (f'<a class="card" href="{href}"><div class="num">{esc(num)}</div><h3>{esc(title)}</h3>'
            f'<p>{desc}</p><div class="go">Open →</div></a>')


intro = p("""One day, nine stages. You arrive knowing C. You leave with a Python program that answers HTTP requests
with JSON read from a SQLite database, and a web page that uses it. Every stage is one new idea, one
task, one self-check, one quiz. Everything on this site and in <code>~/kiet-bootcamp-3</code> works
with the network off. Day 2 is team presentations, then making the Omarchy laptop your own.""")

ports = table("port plan — four programs, one machine", ["port", "program", "started in", "used from"], [
    ("8000", "this guide", "<code>docs/</code> · <code>python3 -m http.server 8000</code>", "your browser, all day"),
    ("8080", "the given servers", "<code>code/stage3</code>, <code>code/stage5</code>", "Stage 3, 5, 6, 7, 8"),
    ("8081", "your own server", "<code>code/stage4</code>", "Stage 4"),
    ("9000", "the frontend page", "<code>code/frontend</code> · <code>python3 -m http.server 9000</code>", "Stage 7, 8"),
])

day1 = '<div class="cards">' + "".join([
    card("Stage 0 · ~2 h", "stage0.html", "Just enough Python", "C with the ceremony removed. Seven complete programs, each stepped through line by line — nothing to write."),
    card("Stage 1", "stage1.html", "Data that survives", "SQLite and four SQL verbs. Build your team's table by hand and watch it outlive the program."),
    card("Stage 2", "stage2.html", "Python talks to the database", "Module, connection, cursor. execute positions, fetchall reads, ? carries the value."),
]) + "</div>"

day1b = '<div class="cards">' + "".join([
    card("Stage 3", "stage3.html", "What a server actually is", "Observe only. A program that waits, poked with curl, both terminals in view."),

    card("Stage 4", "stage4.html", "Write your own server", "Three routes on port 8081. Return a string for text, a dict for JSON."),
    card("Stage 5", "stage5.html", "Join the two halves", "Unpack, query, pack. The whole backend in one function, four times."),
]) + "</div>"

day2 = '<div class="cards">' + "".join([
    card("Stage 6 · short", "stage6.html", "Swap the data, not the code", "200 rows from a .sql source. Zero lines changed."),
    card("Stage 7", "stage7.html", "Someone else's client", "A plain web page calls your backend. The server cannot tell it from curl."),
    card("Stage 8", "stage8.html", "The inspector", "The Network tab is curl -i with a mouse. Break CORS on purpose, then fix it."),
]) + "</div>"

refs = '<div class="cards">' + "".join([
    card("ref", "reference/python-cheatsheet.html", "Python cheatsheet", "Every construct the stages use."),
    card("ref", "reference/c-to-python.html", "C to Python", "The translation table."),
    card("ref", "reference/sqlite-cli.html", "sqlite3 CLI", "Open, look, run a script, quit."),
    card("ref", "reference/sql-for-students-table.html", "SQL for students", "Every statement, against the one table."),
    card("ref", "reference/json.html", "JSON", "A dict, written down."),
    card("ref", "reference/bottle.html", "Bottle", "route, request, response, run, hook."),
    card("ref", "reference/curl.html", "curl", "The flags, the quoting, the + for spaces."),
    card("ref", "reference/http-basics.html", "HTTP basics", "Request line, status line, three doors."),
    card("help", "troubleshooting.html", "Troubleshooting", "Address in use, connection refused, no such table, CORS."),
]) + "</div>"

before = p("""Before the bootcamp, on a machine with internet: run the setup from
<a href="https://aikaryashala.com/kiet/bootcamp-03/setup.html">aikaryashala.com/kiet/bootcamp-03/setup.html</a>.
It installs git, curl and sqlite3, clones this repository to <code>~/kiet-bootcamp-3</code>, and runs
<code>check_env.py</code>. On the day, run the check again, then start this site:""") + \
    term("terminal", """$ python3 ~/kiet-bootcamp-3/check_env.py
~
Ready. Start the bootcamp guide with:
    cd ~/kiet-bootcamp-3/docs && python3 -m http.server 8000
$ cd ~/kiet-bootcamp-3/docs && python3 -m http.server 8000
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...""") + \
    p("Then open <a href=\"http://localhost:8000\">http://localhost:8000</a>. That is this page, served from your own machine.")

body = "\n".join([
    section("about", "What this is", intro + ports),
    section("before", "Before you start", before),
    section("day1", "Day 1 · 21 September", (day1 + day1b + day2).replace('</div><div class="cards">', "")),
    section("day2", "Day 2 · 22 September", p("Each team presents what it built on Day 1. Then the Omarchy customization sessions, on the Omarchy laptop:") + '<div class="cards">' + card("Omarchy", "omarchy-branding.html", "Make Omarchy yours", "Task 1: your name on the screensaver, in the wordmark's block letters. Task 2: your photo on the boot and login screens.") + "</div>"),
    section("reference", "Reference and help", refs),
])

write("index.html", page("Python backend with Bottle + SQLite", "index.html", body,
                         sub="KIET Bootcamp 3 · 21–22 September 2026 · AI Karyashala",
                         artifact="HTTP in  →  SQL in the middle  →  JSON out"))
