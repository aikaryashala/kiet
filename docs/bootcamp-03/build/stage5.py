from lib import *

concept = p("""Everything so far was one half. Stage 2 read rows out of a file and printed them. Stage 4
took a request and returned a dict. This stage joins them, and the join is one function long. Read the
given route <code>/students</code> line by line before you write anything, because the four routes you
add are the same function with different SQL.""") + \
p("""<strong>Unpack.</strong> <code>request.query.get("college")</code> pulls the value after
<code>?college=</code>. If it is <code>None</code>, the client forgot it: set the status to 400 and return
an error dict. That is the whole of input checking today.""") + \
p("""<strong>Query.</strong> <code>query(sql, params)</code> is a helper written for you — the only
function in this stage you do not write. It opens the connection, makes the cursor, runs
<code>execute</code> with your <code>?</code> values, does <code>fetchall</code>, closes, and hands back
the list of tuples. Stage 2, folded into five lines you can reuse.""") + \
p("""<strong>Pack.</strong> <code>pack(rows)</code> turns the list of tuples into a list of dicts with
the three column names as keys. Stage 0 block 7, with the loop already written. Then you return a dict
around it: <code>{"count": len(rows), "students": pack(rows)}</code>. Bottle makes it JSON. Step through
one request to watch the dict grow.""") + \
p("""One more line sits in the file: a hook that adds a header to every response. The comment says to
ignore it, and today that is right. Stage 8 is about that line.""")

left = code("server.py — the given route", '''@route("/students")
def students_by_college():
    college = request.query.get("college")
    if college is None:
        response.status = 400
        return {"error": "college parameter is required"}
    rows = query("SELECT student_name, inter_college, inter_city "
                 "FROM students WHERE inter_college = ?", [college])
    return {"count": len(rows), "students": pack(rows)}''', pre_id="s5code") + \
    term("terminal 2 — curl", '''$ curl "localhost:8080/students?college=Narayana+Junior+College"
{"count": 2, "students": [{"student_name": "Lakshmi Prasanna Gudla", …}, {"student_name": "Divya Sree Pothula", …}]}''', pre_id="s5curl")

right = panel("state", slots([
    ("s5q", "request.query", "", ""),
    ("s5c", "college", "", ""),
    ("s5r", "rows  (list of tuples)", "", ""),
    ("s5p", "pack(rows)  (list of dicts)", "", ""),
    ("s5d", "returned dict", "", ""),
]))

stp = stepper(left, right, [
    {"note": "The request arrives. The path /students picked this function; the query string is waiting to be read.",
     "hl": {"s5curl": 0, "s5code": 1}, "slots": {"s5q": {"v": "college=Narayana+Junior+College", "cls": "live"}}},
    {"note": "Unpack. .get gives the value with the + already turned back into spaces. Had it been missing, this would be None.",
     "hl": {"s5code": 2}, "slots": {"s5q": {"v": "college=Narayana+Junior+College", "cls": ""}, "s5c": {"v": "'Narayana Junior College'", "cls": "live"}}},
    {"note": "The guard. college is a string, not None, so the 400 branch is skipped.",
     "hl": {"s5code": 3}, "slots": {"s5c": {"v": "'Narayana Junior College'", "cls": ""}}},
    {"note": "Query. The ? takes the college from the list. query() connects, executes, fetches, closes — Stage 2 in one call.",
     "hl": {"s5code": 6}, "slots": {"s5r": {"v": "[('Lakshmi Prasanna Gudla', 'Narayana Junior College', 'Vijayawada'), ('Divya Sree Pothula', 'Narayana Junior College', 'Vijayawada')]", "cls": "live"}}},
    {"note": "Pack. Each tuple becomes a dict with the three column names as keys.",
     "hl": {"s5code": 8}, "slots": {"s5r": {"v": "2 tuples", "cls": ""}, "s5p": {"v": "[{'student_name': 'Lakshmi Prasanna Gudla', 'inter_college': …, 'inter_city': …}, {'student_name': 'Divya Sree Pothula', …}]", "cls": "live"}}},
    {"note": "Return. The dict wraps the count and the list. Bottle turns it into JSON and sends it with status 200.",
     "hl": {"s5code": 8, "s5curl": 1}, "slots": {"s5p": {"v": "2 dicts", "cls": ""}, "s5d": {"v": "{'count': 2, 'students': [...]}", "cls": "live"}}},
])

task = p("<strong>Before the first curl:</strong> spaces are not allowed in a URL. Write <code>+</code> for each space in a value: <code>college=Narayana+Junior+College</code>. The server turns it back. curl refuses a URL with a bare space in it.") + steps([
    p("<strong>Terminal 1 — server.</strong> Stop the Stage 3 and 4 servers if they are still running (port 8080 must be free). Start the Stage 5 server; it reads your Stage 1 database by default.") +
    term("terminal 1 — server", """$ cd ~/kiet-bootcamp-3/code/stage5
$ python3 server.py
Serving on http://localhost:8080  (DB: /home/kiet/kiet-bootcamp-3/data/team_details.db)  — Ctrl+C to stop
Bottle v0.13.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.
""") + p("Terminal 2: the given route, with a college from your team, then with the parameter left out.") +
    term("terminal 2 — curl", """$ curl "localhost:8080/students?college=Narayana+Junior+College"
{"count": 2, "students": [{"student_name": "Lakshmi Prasanna Gudla", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}, {"student_name": "Divya Sree Pothula", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}]}
$ curl "localhost:8080/students?college=Vignan+Junior+College"
{"count": 0, "students": []}
$ curl localhost:8080/students
{"error": "college parameter is required"}""") +
    p("Now open <code>server.py</code>. This is the whole file. Read <code>query</code>, <code>pack</code>, and the given route against the stepper. Then the four TODOs:") +
    code_file("code/stage5/server.py", "code/stage5/server.py"),
    p("<strong>Task 1.</strong> <code>/students/by-location?location=Y</code>. Same shape as the given route; the parameter is <code>location</code>, the column is <code>inter_city</code>. Restart the server after the edit.") +
    term("terminal 2 — curl", """$ curl "localhost:8080/students/by-location?location=Vijayawada"
{"count": 2, "students": [{"student_name": "Lakshmi Prasanna Gudla", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}, {"student_name": "Divya Sree Pothula", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}]}
$ curl localhost:8080/students/by-location
{"error": "location parameter is required"}"""),
    p("<strong>Task 2.</strong> <code>/students/search?college=X&amp;location=Y</code>. Both required. Two <code>?</code>s, two values in the list, in that order.") +
    term("terminal 2 — curl", """$ curl "localhost:8080/students/search?college=Narayana+Junior+College&location=Vijayawada"
{"count": 2, "students": [{"student_name": "Lakshmi Prasanna Gudla", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}, {"student_name": "Divya Sree Pothula", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}]}
$ curl "localhost:8080/students/search?college=Narayana+Junior+College&location=Visakhapatnam"
{"count": 0, "students": []}
$ curl "localhost:8080/students/search?college=Narayana+Junior+College"
{"error": "college and location parameters are required"}"""),
    p("<strong>Task 3.</strong> <code>/colleges</code>. No parameter, and the loop is already written: each row is a one-item tuple and <code>row[0]</code> goes into the list. Your only line is the SQL — every college once, sorted: <code>SELECT DISTINCT inter_college FROM students ORDER BY inter_college</code>.") +
    term("terminal 2 — curl", """$ curl localhost:8080/colleges
{"colleges": ["Narayana Junior College", "Sri Chaitanya Junior College"]}"""),
    p("<strong>Task 4.</strong> <code>/count?college=X</code>. Unpack, guard and return are given; <code>rows[0][0]</code> is already there because <code>SELECT COUNT(*)</code> gives one row with one number. Your only line is the SQL. Until you write it, this route answers 500 and Terminal 1 says <code>ProgrammingError: Incorrect number of bindings supplied</code> — the empty SQL has no <code>?</code> for the college.") +
    term("terminal 2 — curl", """$ curl "localhost:8080/count?college=Sri+Chaitanya+Junior+College"
{"college": "Sri Chaitanya Junior College", "count": 2}
$ curl "localhost:8080/count?college=Vignan+Junior+College"
{"college": "Vignan Junior College", "count": 0}
$ curl localhost:8080/count
{"error": "college parameter is required"}"""),
])

expected = p("Terminal 1 after the run above, for the example team. Yours shows your team's college names in the query strings and different byte counts.") + \
    term("terminal 1 — server", """127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /students?college=Narayana+Junior+College HTTP/1.1" 200 254
127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /students?college=Vignan+Junior+College HTTP/1.1" 200 28
127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /students HTTP/1.1" 400 42
127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /students/by-location?location=Vijayawada HTTP/1.1" 200 254
127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /students/by-location HTTP/1.1" 400 43
127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /students/search?college=Narayana+Junior+College&location=Vijayawada HTTP/1.1" 200 254
127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /students/search?college=Narayana+Junior+College&location=Visakhapatnam HTTP/1.1" 200 28
127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /students/search?college=Narayana+Junior+College HTTP/1.1" 400 57
127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /colleges HTTP/1.1" 200 73
127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /count?college=Sri+Chaitanya+Junior+College HTTP/1.1" 200 55
127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /count?college=Vignan+Junior+College HTTP/1.1" 200 48
127.0.0.1 - - [21/Sep/2026 10:58:41] "GET /count HTTP/1.1" 400 42""") + \
    p("Three shapes and no others: <code>{\"count\", \"students\"}</code> for the three list routes, <code>{\"colleges\"}</code>, <code>{\"college\", \"count\"}</code>. A wrong college is not an error — it is a correct answer with zero rows. A missing parameter is an error: 400 and <code>{\"error\": …}</code>.")

check = p("This check builds a temporary database with the four-row example team and tells you how to start your server against it, so the expected answers are the same on every machine.") + \
    term("terminal 2 — curl", """$ python3 check.py
Check database: /tmp/kiet_stage5_check.db
Start your server against it in Terminal 1:  python3 server.py --db /tmp/kiet_stage5_check.db

Cannot connect to localhost:8080 — is the server running?
  Terminal 1 (in this folder):  python3 server.py --db /tmp/kiet_stage5_check.db""") + \
    p("Do what it says in Terminal 1 — Ctrl+C the running server, start it with that <code>--db</code> — then run the check again:") + \
    term("terminal 2 — curl", """$ python3 check.py
Check database: /tmp/kiet_stage5_check.db
Start your server against it in Terminal 1:  python3 server.py --db /tmp/kiet_stage5_check.db

PASS: GET /students?college=Narayana+Junior+College (given route, server is on the check DB)
PASS: GET /students without college -> 400
PASS: Task 1: GET /students/by-location?location=Visakhapatnam -> 2 students
PASS: Task 1: GET /students/by-location?location=Guntur -> 0 students
PASS: Task 1: GET /students/by-location without location -> 400
PASS: Task 2: GET /students/search Narayana + Vijayawada -> 2 students
PASS: Task 2: GET /students/search Narayana + Visakhapatnam -> 0 students
PASS: Task 2: GET /students/search with only college -> 400
PASS: Task 3: GET /colleges -> the 2 colleges, sorted
PASS: Task 4: GET /count?college=Sri+Chaitanya+Junior+College -> 2
PASS: Task 4: GET /count?college=Vignan+Junior+College -> 0
PASS: Task 4: GET /count without college -> 400

12 passed, 0 failed""")

stuck = p('Solution: <code>~/kiet-bootcamp-3/code/stage5/solution/server.py</code>. Its default database path has one more <code>..</code> because it sits one folder deeper; everything else should match yours.') + \
    p('Reference: <a href="reference/bottle.html">Bottle</a> · <a href="reference/sql-for-students-table.html">SQL for the students table</a> · <a href="reference/curl.html">curl</a> (spaces as +) · <a href="troubleshooting.html">Troubleshooting</a> (no such table, address already in use).')

qz = quiz([
    ("<code>/students/search?college=Narayana+Junior+College</code> with no location. Which line answers?",
     ["<code>query(...)</code> with one value", "The <code>if college is None or location is None</code> guard, with a 400", "Bottle's 404 page", "<code>pack(rows)</code> with an empty list"], 2,
     "Unpack found location missing. The guard returns the error dict before any SQL runs."),
    ("<code>query(\"SELECT COUNT(*) FROM students WHERE inter_college = ?\", [college])</code> returns what?",
     ["A number", "A list with one tuple holding one number: <code>[(2,)]</code>", "A dict", "<code>None</code>"], 2,
     "query() always returns what fetchall() returns: a list of tuples. COUNT gives one row with one column, so rows[0][0] is the number."),
    ("Why does <code>curl \"localhost:8080/students?college=Narayana Junior College\"</code> fail before reaching the server?",
     ["The server rejects spaces", "A URL cannot contain a space; write + instead", "The college is not in the database", "Missing -X GET"], 2,
     "curl stops with a malformed-URL error. Spaces must be written as + (or %20). The server decodes them back to spaces."),
    ("What does <code>{\"count\": 0, \"students\": []}</code> mean?",
     ["The database is missing", "The parameter was missing", "The query ran and matched no rows", "pack() crashed"], 3,
     "A correct question with an empty answer. Missing parameters give 400; missing files give a traceback; this is a clean 200."),
])

body = "\n".join([
    section("concept", "Concept", concept + stp),
    section("video", "Demo video", video(5, "Starting server.py on the team database, the three curls on the given route, then writing each of the four routes and curling it, then check.py with the --db restart.")),
    section("task", "Task", task),
    section("expected", "Expected output", expected),
    section("check", "Check yourself", check),
    section("takeaway", "Takeaway", callout("Every endpoint is unpack → query → pack. You have now written all three.")),
    section("stuck", "Stuck?", stuck),
    section("quiz", "Quiz", qz),
])

write("stage5.html", page("Join the two halves", "stage5.html", body,
                          sub="Request in, SQL in the middle, JSON out — one function, repeated four times with different SQL.",
                          artifact='rows = query("... WHERE inter_college = ?", [college])',
                          stage_label="Stage 5 · Session 2 · afternoon"))
