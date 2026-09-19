from lib import *

concept = p("""Until now the only client was curl, and you were typing every request. The backend is
finished when a program you did not write can use it. That program is a web page: a few dozen lines of
HTML and JavaScript that you will run, click, and read — not edit. It is deliberately plain. It builds a
URL, sends a GET, reads the JSON, and puts the rows in a table. curl with buttons.""") + \
p("""Two programs need two ports. Your backend stays on 8080. The page is served by Python's built-in
file server on 9000 — <code>python3 -m http.server</code> is a server too, one that only hands out files.
The browser loads the page from 9000, and the page then talks to 8080. Two servers, two terminals, both
logging.""") + \
p("""Open <code>app.js</code> next to the page and read it. Above every <code>fetch</code> call is a
comment with the curl command it replaces. <code>fetch(url)</code> sends the request;
<code>.then</code> is what runs when the answer arrives. The page's own <strong>Request log</strong>
prints, for each click, the method, the full URL, the status and how long it took — the four things
<code>curl -i</code> shows you. One thing differs: the browser writes a space as <code>%20</code> where
you typed <code>+</code>. The server reads both.""") + \
p("""Keep Terminal 1 in view. When the page asks for <code>/students?college=…</code>, the log line the
server prints is the same line it printed for curl. The server cannot tell who is asking. That is the
whole idea of a backend.""")

task = steps([
    p("<strong>Terminal 1 — backend.</strong> The Stage 5 server on the big database. If it is still running from Stage 6, leave it.") +
    term("terminal 1 — backend", """$ cd ~/kiet-bootcamp-3/code/stage5
$ python3 server.py --db ../../data/all_students.db
Serving on http://localhost:8080  (DB: /home/kiet/kiet-bootcamp-3/data/all_students.db)  — Ctrl+C to stop
~"""),
    p("<strong>Terminal 2 — frontend.</strong> A file server for the page, on port 9000. It logs every file it hands out.") +
    term("terminal 2 — frontend", """$ cd ~/kiet-bootcamp-3/code/frontend
$ python3 -m http.server 9000
Serving HTTP on 0.0.0.0 port 9000 (http://0.0.0.0:9000/) ..."""),
    p("<strong>Browser.</strong> Open <code>http://localhost:9000</code>. The College dropdown is already filled: on load, the page did <code>GET /colleges</code>, and the Request log has one line. Pick a college, click <strong>Fetch by college</strong>. The table fills; the log gets a second line.") +
    term("the page's request log", """GET http://localhost:8080/students?college=Sasi%20Junior%20College  ->  200  (24 ms)
GET http://localhost:8080/colleges  ->  200  (12 ms)"""),
    p("Type a city in Location, click <strong>Fetch by location</strong>. Then with both filled, <strong>Search both</strong>. Three routes, three log lines, newest on top.") +
    term("the page's request log", """GET http://localhost:8080/students/search?college=Sasi%20Junior%20College&location=Guntur  ->  200  (7 ms)
GET http://localhost:8080/students/by-location?location=Guntur  ->  200  (7 ms)
GET http://localhost:8080/students?college=Sasi%20Junior%20College  ->  200  (24 ms)
GET http://localhost:8080/colleges  ->  200  (12 ms)"""),
    p("<strong>Terminal 3 — curl.</strong> Ask the same question by hand. The JSON is what the table was built from.") +
    term("terminal 3 — curl", """$ curl -s "localhost:8080/students/search?college=Sasi+Junior+College&location=Guntur"
{"count": 2, "students": [{"student_name": "Sudheer Chandra Gupta", "inter_college": "Sasi Junior College", "inter_city": "Guntur"}, {"student_name": "Tejaswini Harini Achari", "inter_college": "Sasi Junior College", "inter_city": "Guntur"}]}"""),
    p("<strong>Terminal 1 again.</strong> Four lines from the browser, one from curl. Find the difference.") +
    term("terminal 1 — backend", """127.0.0.1 - - [21/Sep/2026 15:06:26] "GET /colleges HTTP/1.1" 200 341
127.0.0.1 - - [21/Sep/2026 15:06:57] "GET /students?college=Sasi%20Junior%20College HTTP/1.1" 200 351
127.0.0.1 - - [21/Sep/2026 15:07:01] "GET /students/by-location?location=Guntur HTTP/1.1" 200 3271
127.0.0.1 - - [21/Sep/2026 15:07:01] "GET /students/search?college=Sasi%20Junior%20College&location=Guntur HTTP/1.1" 200 242
127.0.0.1 - - [21/Sep/2026 15:07:30] "GET /students/search?college=Sasi+Junior+College&location=Guntur HTTP/1.1" 200 242""") +
    p("Only the spelling of the space. Same route, same status, same 242 bytes."),
    p("Open <code>app.js</code> in your editor and read it top to bottom. Do not change anything. Find the three <code>fetch</code> calls and the curl comment above each.") +
    code_file("code/frontend/app.js", "code/frontend/app.js"),
])

expected = p("A filled dropdown on load, a filled table after each click, one Request log line per click, and one matching line in Terminal 1 per click. Terminal 2 logs only the page files:") + \
    term("terminal 2 — frontend", """127.0.0.1 - - [21/Sep/2026 15:06:26] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2026 15:06:26] "GET /app.js HTTP/1.1" 200 -""") + \
    p("If instead the page shows a yellow banner — <em>Cannot reach the backend at http://localhost:8080</em> — Terminal 1 is not running the Stage 5 server. Start it and reload the page.")

check = term("terminal 3 — curl", """$ cd ~/kiet-bootcamp-3/code/stage7
$ python3 check.py
PASS: port 9000 serves index.html
PASS: port 9000 serves app.js
PASS: port 8080 answers /colleges with JSON

3 passed, 0 failed""")

stuck = p('Nothing to write. If the dropdown is empty and the banner is up: Terminal 1. If the browser says it cannot connect to localhost:9000: Terminal 2, and check you ran <code>http.server</code> inside <code>code/frontend</code>.') + \
    p('Reference: <a href="reference/http-basics.html">HTTP basics</a> · <a href="reference/curl.html">curl</a> · <a href="troubleshooting.html">Troubleshooting</a>.')

qz = quiz([
    ("Which program does the browser talk to when you click <strong>Fetch by college</strong>?",
     ["The file server on 9000", "Your Stage 5 server on 8080", "curl", "sqlite3"], 2,
     "9000 only handed out index.html and app.js. Every click is a fetch to BACKEND, which is http://localhost:8080."),
    ("The server logs <code>college=Sasi%20Junior%20College</code> for the browser and <code>college=Sasi+Junior+College</code> for curl. What is different inside the route?",
     ["Nothing; both arrive as 'Sasi Junior College'", "The browser one has %20 in the string", "The curl one fails", "The browser one needs a different route"], 1,
     "Both are encodings of a space. request.query.get decodes either. The route sees the same string."),
    ("What does <code>.then(function (response) { ... })</code> mean in app.js?",
     ["Run this now", "Run this when the answer arrives", "Retry on failure", "Send the request twice"], 2,
     "fetch sends and returns immediately; the page keeps working. The function in .then runs later, when the response comes back."),
    ("The Request log shows method, URL, status, time. Where have you seen those before?",
     ["In sqlite3", "In <code>curl -i</code> and the server's log line", "In app.js only", "Nowhere"], 2,
     "curl -i prints the status line and headers; the server log prints method, path and status. The page is showing the same request from the client's side."),
])

body = "\n".join([
    section("concept", "Concept", concept),
    section("video", "Demo video", video(7, "Two terminals running two servers, the page loading with the dropdown filled, three clicks with the table and Request log updating, and Terminal 1 logging each one beside a curl.")),
    section("task", "Task", task),
    section("expected", "Expected output", expected),
    section("check", "Check yourself", check),
    section("takeaway", "Takeaway", callout("A backend is finished when a program you didn't write can use it. The frontend is curl with buttons.")),
    section("stuck", "Stuck?", stuck),
    section("quiz", "Quiz", qz),
])

write("stage7.html", page("Someone else's client: the browser", "stage7.html", body,
                          sub="A plain web page calls your backend. Two servers, two ports, and a server log that cannot tell curl from a browser.",
                          artifact="python3 -m http.server 9000",
                          stage_label="Stage 7 · Session 3 · after dinner"))
