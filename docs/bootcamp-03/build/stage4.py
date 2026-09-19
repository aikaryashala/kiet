from lib import *

concept = p("""A route is a function with an address. In Stage 3 you saw four addresses answer; today you
give three functions addresses of your own. The line <code>@route("/hai")</code> above
<code>def hai():</code> says one thing: when this path is asked for, call this function. It does not
call it now. It does not change what the function does. It writes the address into Bottle's list, and
<code>run()</code> at the bottom starts the waiting loop that consults that list.""") + \
p("""What the function returns becomes the answer. Return a string and the client gets text. Return a
dict and Bottle turns it into JSON and sets <code>Content-Type: application/json</code> for you — the
<code>json.dumps</code> from Stage 0 block 3, done automatically. You never build the response by hand.""") + \
p("""The three doors from Stage 3 map to three pieces of Bottle. A path parameter,
<code>&lt;name&gt;</code> in the route, becomes a function argument — <code>def wish(name):</code>
receives whatever was in the URL. The query string is <code>request.query.get("k")</code>. The body,
when it is JSON, is <code>request.json</code>, already a dict, or <code>None</code> if nothing was sent.
That <code>None</code> is where the <code>if x is None:</code> guard from Stage 0 earns its place: a
missing body must become a 400 with an error dict, not a crash.""") + \
p("""Your server listens on port 8081, so it can run at the same time as the Stage 3 server on 8080. Two
programs, two ports, one machine; curl picks which one by the number after the colon. Keep both running
for the last step and watch two terminals answer.""")

task = steps([
    p("<strong>Terminal 1 — server.</strong> Start the given file. It already answers <code>/hai</code>. Everything else is a <code>TODO</code>.") +
    term("terminal 1 — server", """$ cd ~/kiet-bootcamp-3/code/stage4
$ python3 server.py
Serving on http://localhost:8081  — Ctrl+C to stop
Bottle v0.13.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:8081/
Hit Ctrl-C to quit.
""") + term("terminal 2 — curl", """$ curl localhost:8081/hai
Namasthey!!!""") + p("Open <code>server.py</code> in your editor. This is the whole file:") + code_file("code/stage4/server.py", "code/stage4/server.py"),
    p("<strong>Task 1.</strong> Fill in <code>wish</code>: the name from the path, in a different sentence from Stage 3 on purpose. <strong>Stop the server with Ctrl+C and start it again</strong> after every edit — it reads the file only once, at start.") +
    term("terminal 2 — curl", """$ curl localhost:8081/wish/Ravi
Good morning Ravi
$ curl localhost:8081/wish/Lakshmi
Good morning Lakshmi"""),
    p("<strong>Task 2.</strong> Fill in <code>iseven</code>: the number from the body. <code>%</code> from Stage 0 block 4. Guard the missing body first, then answer.") +
    term("terminal 2 — curl", """$ curl -X POST localhost:8081/iseven -H "Content-Type: application/json" -d '{"number": 4}'
{"number": 4, "is_even": true}
$ curl -X POST localhost:8081/iseven -H "Content-Type: application/json" -d '{"number": 7}'
{"number": 7, "is_even": false}
$ curl -X POST localhost:8081/iseven
{"error": "send JSON like {\\"number\\": 4}"}"""),
    p("<strong>Task 3.</strong> Fill in <code>about</code>: a dict with exactly the three keys of the <code>students</code> table, holding <em>your</em> details, typed in. This is the first JSON your own server sends, and it has the same shape as one row of Stage 1.") +
    term("terminal 2 — curl", """$ curl localhost:8081/about
{"student_name": "Ravi Teja Kanchi", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}
$ curl -i localhost:8081/about
HTTP/1.0 200 OK
Date: Mon, 21 Sep 2026 09:17:51 GMT
Server: WSGIServer/0.2 CPython/3.12.3
Content-Type: application/json
Content-Length: 116

{"student_name": "Ravi Teja Kanchi", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}""") +
    p("Look at the <code>Content-Type</code>. You returned a dict; Bottle said <code>application/json</code>. In Task 1 you returned a string and it said <code>text/html</code>."),
    p("<strong>Two servers at once.</strong> Terminal 3: start the Stage 3 server. Then from Terminal 2 ask each one the same question.") +
    term("terminal 3 — stage 3 server", """$ cd ~/kiet-bootcamp-3/code/stage3
$ python3 demo_server.py
Serving on http://localhost:8080  — Ctrl+C to stop
~""") + term("terminal 2 — curl", """$ curl localhost:8080/hai
Namasthey!!!
$ curl localhost:8081/hai
Namasthey!!!
$ curl localhost:8080/wish/Ravi
~
$ curl localhost:8081/wish/Ravi
Good morning Ravi""") + p("Same text from <code>/hai</code> on both, because both files have that route. <code>/wish/Ravi</code> on 8080 is a 404 page — the Stage 3 server never heard of it. The port chooses the program; the path chooses the function inside it."),
])

expected = p("Terminal 1 after the five steps. Yours has your timestamps; the sizes match if your JSON matches.") + \
    term("terminal 1 — server", """127.0.0.1 - - [21/Sep/2026 14:47:51] "GET /hai HTTP/1.1" 200 12
127.0.0.1 - - [21/Sep/2026 14:47:51] "GET /wish/Ravi HTTP/1.1" 200 17
127.0.0.1 - - [21/Sep/2026 14:47:51] "GET /wish/Lakshmi HTTP/1.1" 200 20
127.0.0.1 - - [21/Sep/2026 14:47:51] "POST /iseven HTTP/1.1" 200 30
127.0.0.1 - - [21/Sep/2026 14:47:51] "POST /iseven HTTP/1.1" 200 31
127.0.0.1 - - [21/Sep/2026 14:47:51] "POST /iseven HTTP/1.1" 400 43
127.0.0.1 - - [21/Sep/2026 14:47:51] "GET /about HTTP/1.1" 200 116
127.0.0.1 - - [21/Sep/2026 14:47:51] "GET /about HTTP/1.1" 200 116""") + \
    p("If you edit the file and the answer does not change, you did not restart. If Terminal 1 shows a traceback ending in <code>TypeError</code> or <code>KeyError</code> and curl shows a 500 page, read the last line of the traceback: it names the line in your file.")

check = term("terminal 2 — curl", """$ python3 check.py
PASS: GET /hai -> Namasthey!!! (given)
PASS: Task 1: GET /wish/Ravi -> Good morning Ravi
PASS: Task 1: GET /wish/Lakshmi -> Good morning Lakshmi
PASS: Task 2: POST /iseven 4 -> is_even true
PASS: Task 2: POST /iseven 7 -> is_even false
PASS: Task 2: POST /iseven with no body -> 400 with an error
PASS: Task 3: /about has exactly the three keys of the students table
PASS: Task 3: /about values are non-empty strings

8 passed, 0 failed""")

stuck = p('Solution: <code>~/kiet-bootcamp-3/code/stage4/solution/server.py</code>. It has the sample student in <code>/about</code>; yours should have you.') + \
    p('Reference: <a href="reference/bottle.html">Bottle</a> · <a href="reference/json.html">JSON</a> · <a href="reference/curl.html">curl</a> · <a href="troubleshooting.html">Troubleshooting</a> (address already in use, ModuleNotFoundError: bottle).')

qz = quiz([
    ("You change the text in <code>wish()</code>, save, and curl still shows the old text. Why?",
     ["curl caches answers", "The server reads the file only when it starts; restart it", "Bottle needs debug=False", "The route must be renamed"], 2,
     "The running process has the old code in memory. Ctrl+C and python3 server.py again loads the new file."),
    ("A route returns <code>{\"number\": 4, \"is_even\": True}</code>. What does curl print?",
     ["<code>{'number': 4, 'is_even': True}</code>", "<code>{\"number\": 4, \"is_even\": true}</code>", "<code>number=4 is_even=True</code>", "an error, dicts cannot be returned"], 2,
     "Bottle runs json.dumps on the dict: double quotes, lowercase true. That is JSON, not Python."),
    ("<code>curl -X POST localhost:8081/iseven</code> with no <code>-d</code>. What is <code>request.json</code> inside the route?",
     ["<code>{}</code>", "<code>\"\"</code>", "<code>None</code>", "<code>0</code>"], 3,
     "No body means no JSON, and Bottle gives None. Without the is None guard, data.get would crash and the client would see a 500."),
    ("Both servers are running. <code>curl localhost:8080/wish/Ravi</code> gives a 404. Why?",
     ["Port 8080 is the Stage 3 server, which has no /wish route", "8080 is blocked", "The name must be in the body", "Only one server can run at a time"], 1,
     "The port picks the program. The Stage 3 program on 8080 has /hai, /hello, /isprime and /greet — /wish exists only in yours on 8081."),
])

body = "\n".join([
    section("concept", "Concept", concept),
    section("video", "Demo video", video(4, "Starting the stub, filling in wish, restarting, curl; the same for iseven and about; then both servers side by side answering /hai and /wish/Ravi.")),
    section("task", "Task", task),
    section("expected", "Expected output", expected),
    section("check", "Check yourself", check),
    section("takeaway", "Takeaway", callout("A server is a set of functions; HTTP is how someone else calls them. Return a dict and it's already JSON.")),
    section("stuck", "Stuck?", stuck),
    section("quiz", "Quiz", qz),
])

write("stage4.html", page("Write your own server", "stage4.html", body,
                          sub="Three functions, three addresses, port 8081. Return a string for text, a dict for JSON, and guard the body that is not there.",
                          artifact='@route("/wish/<name>")',
                          stage_label="Stage 4 · Session 2 · afternoon"))
