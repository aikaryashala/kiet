from lib import *

concept = p("""Every browser has <code>curl -i</code> built in. It is called the inspector, and its
<strong>Network</strong> tab lists one row per request the page made. Click a row and you get two
sub-tabs. <strong>Headers</strong> shows the Request URL, the Request Method, the Status Code, then the
request headers and the response headers. <strong>Response</strong> shows the body. That is exactly the
text <code>curl -i</code> prints, in the same order, with a mouse instead of a terminal.""") + \
p("""The <strong>Console</strong> tab is where the browser prints errors the page did not handle — the
same role as the traceback in Terminal 1, on the client side.""") + \
p("""One thing lives only in the browser. A page loaded from port 9000 asks port 8080 for data. By
default the browser will send that request and then <em>refuse to hand the answer to the page</em>,
unless the answer carries a header saying the server allows it:
<code>Access-Control-Allow-Origin: *</code>. That is the line in the Stage 5 hook you were told to
ignore. The rule is called CORS. curl never checked it; the browser always does. You will remove the
line, watch the server say 200 and the browser say no, and put it back.""") + \
p("""Step through one request below, matching each <code>curl -i</code> line to the field the Network
tab shows it in.""")

left = term("terminal 3 — curl -i", """$ curl -i "localhost:8080/students?college=Sasi+Junior+College"
HTTP/1.0 200 OK
Date: Mon, 21 Sep 2026 09:37:39 GMT
Server: WSGIServer/0.2 CPython/3.12.3
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 351

{"count": 3, "students": [{"student_name": "Sruthi Sai Ravella", …}, …]}""", pre_id="s8curl")

right = panel("network tab — the same request", slots([
    ("s8url", "Headers · Request URL", "", ""),
    ("s8m", "Headers · Request Method", "", ""),
    ("s8s", "Headers · Status Code", "", ""),
    ("s8ct", "Response Headers · content-type", "", ""),
    ("s8acao", "Response Headers · access-control-allow-origin", "", ""),
    ("s8body", "Response", "", ""),
]))

stp = stepper(left, right, [
    {"note": "The command line is the Request URL. The Network tab shows the same URL, with %20 where you typed +.",
     "hl": {"s8curl": 0}, "slots": {"s8url": {"v": "http://localhost:8080/students?college=Sasi%20Junior%20College", "cls": "live"}, "s8m": {"v": "GET", "cls": "live"}}},
    {"note": "The status line. curl prints it first; the Network tab shows it as Status Code, and colours the row red when it is not 2xx.",
     "hl": {"s8curl": 1}, "slots": {"s8url": {"v": "http://localhost:8080/students?college=Sasi%20Junior%20College", "cls": ""}, "s8m": {"v": "GET", "cls": ""}, "s8s": {"v": "200 OK", "cls": "live"}}},
    {"note": "Response headers, one per line. Date and Server are housekeeping.",
     "hl": {"s8curl": 3}, "slots": {"s8s": {"v": "200 OK", "cls": ""}}},
    {"note": "Content-Type tells the browser the body is JSON — this is why fetch's response.json() works.",
     "hl": {"s8curl": 4}, "slots": {"s8ct": {"v": "application/json", "cls": "live"}}},
    {"note": "The CORS header. Without it the browser still receives everything below, and then refuses to give it to the page.",
     "hl": {"s8curl": 5}, "slots": {"s8ct": {"v": "application/json", "cls": ""}, "s8acao": {"v": "*", "cls": "live"}}},
    {"note": "A blank line ends the headers. Everything after it is the body: the Response sub-tab.",
     "hl": {"s8curl": 8}, "slots": {"s8acao": {"v": "*", "cls": ""}, "s8body": {"v": "{\"count\": 3, \"students\": [...]}", "cls": "live"}}},
])

task = p("Everything from Stage 7 stays running: the backend on 8080 in Terminal 1, the frontend on 9000 in Terminal 2, the page open in the browser.") + steps([
    p("<strong>Browser.</strong> Press <kbd>F12</kbd> (or <kbd>Ctrl+Shift+I</kbd>) to open the inspector. Click the <strong>Network</strong> tab. Now click <strong>Fetch by college</strong> on the page. One row appears: <code>students?college=…</code>."),
    p("Click that row. Under <strong>Headers</strong>: Request URL, Request Method <code>GET</code>, Status Code <code>200</code>. Scroll down to Response Headers: <code>content-type: application/json</code> and <code>access-control-allow-origin: *</code>."),
    p("Click the <strong>Response</strong> sub-tab. The JSON, exactly as curl printed it."),
    p("<strong>Terminal 3 — curl.</strong> The same request with <code>-i</code>. Put the terminal beside the inspector and match line to field.") +
    term("terminal 3 — curl", """$ curl -i "localhost:8080/students?college=Sasi+Junior+College"
HTTP/1.0 200 OK
Date: Mon, 21 Sep 2026 09:37:39 GMT
Server: WSGIServer/0.2 CPython/3.12.3
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 351

{"count": 3, "students": [{"student_name": "Sruthi Sai Ravella", "inter_college": "Sasi Junior College", "inter_city": "Rajahmundry"}, {"student_name": "Sudheer Chandra Gupta", "inter_college": "Sasi Junior College", "inter_city": "Guntur"}, {"student_name": "Tejaswini Harini Achari", "inter_college": "Sasi Junior College", "inter_city": "Guntur"}]}"""),
    p("Click <strong>Fetch by location</strong> and <strong>Search both</strong>. Two more rows in the Network tab. Open each and read its Request URL."),
    p("<strong>Break it on purpose.</strong> In your editor, open <code>code/stage5/server.py</code> and put a <code>#</code> in front of <em>all three</em> lines of the hook — the <code>@hook</code> line, the <code>def</code> line, and the header line. Commenting only the last one leaves an empty function and Python refuses to start.") +
    code("server.py — the three lines, commented", '''# @hook("after_request")
# def allow_browser():
#     response.headers["Access-Control-Allow-Origin"] = "*"   # This line matters in Stage 8. Ignore it for now.''') +
    p("Terminal 1: Ctrl+C, start the server again with <code>--db ../../data/all_students.db</code>. Browser: click <strong>Fetch by college</strong>.") +
    p("The table does not change. The yellow banner appears. The Request log says <code>FAILED (see the Console tab)</code>. In the Network tab the new row is red, with status <code>(failed)</code> or <code>CORS error</code>. Click the <strong>Console</strong> tab:") +
    term("browser — console tab", """Access to fetch at 'http://localhost:8080/students?college=Sasi%20Junior%20College' from origin 'http://localhost:9000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
GET http://localhost:8080/students?college=Sasi%20Junior%20College net::ERR_FAILED 200 (OK)
TypeError: Failed to fetch""") +
    p("Read the second line again: <code>net::ERR_FAILED 200 (OK)</code>. The server said 200. Now look at Terminal 1:") +
    term("terminal 1 — backend", """127.0.0.1 - - [21/Sep/2026 15:07:44] "GET /students?college=Sasi%20Junior%20College HTTP/1.1" 200 351""") +
    p("The server answered, fully, as always. The browser received the answer and then refused to give it to the page, because the answer did not say the page was allowed to have it. Terminal 3: <code>curl -i</code> the same URL — it works, and the <code>Access-Control-Allow-Origin</code> line is simply gone from the headers."),
    p("<strong>Fix it.</strong> Remove the three <code>#</code>s, Ctrl+C, start again, click again. The row is 200, the table fills, the banner goes.") +
    p("Terminal 1 through all of this: identical log lines, before, during and after. The break was never on the server's side."),
])

expected = p("Three requests visible in the Network tab with Headers and Response matching <code>curl -i</code> field for field. During the break: a red row, the Console error above, a 200 in Terminal 1, and curl unaffected. After the fix: back to the Stage 7 state.")

check = term("terminal 3 — curl", """$ cd ~/kiet-bootcamp-3/code/stage8
$ python3 check.py
PASS: GET /colleges -> 200
PASS: response has  Access-Control-Allow-Origin: *  (the browser will accept it)
PASS: response Content-Type is application/json

Compare by eye with:  curl -i localhost:8080/colleges
3 passed, 0 failed""") + p("Run it while the hook is commented out and the second line fails, naming the missing header. That is the whole difference between Stage 7 working and not.")

stuck = p('If the server will not start after commenting: you commented one line, not three — <code>IndentationError: expected an indented block</code> is Python telling you the function has no body. If the page still fails after restoring: check Terminal 1 actually restarted (the start line prints again).') + \
    p('Reference: <a href="reference/http-basics.html">HTTP basics</a> · <a href="reference/curl.html">curl</a> · <a href="reference/bottle.html">Bottle</a> (the hook) · <a href="troubleshooting.html">Troubleshooting</a> (CORS error text).')

qz = quiz([
    ("With the hook commented out, Terminal 1 logs <code>200 351</code> but the table stays empty. Who refused?",
     ["The server", "The browser, after receiving the answer", "curl", "sqlite3"], 2,
     "The server did its job. The browser enforces CORS: a page from one origin may not read another origin's response unless that response allows it."),
    ("Where does <code>curl -i</code>'s status line appear in the inspector?",
     ["Console tab", "Network → Headers → Status Code", "Network → Response", "Nowhere"], 2,
     "Headers holds the request line, the status and both sets of headers; Response holds the body."),
    ("Why did <code>curl -i</code> keep working during the break?",
     ["curl sends the header itself", "curl is not a browser page from another origin, so it does not check CORS", "curl uses a different port", "It did not; it also failed"], 2,
     "CORS is a browser rule about pages. A terminal program has no origin to protect."),
    ("You comment out only the <code>response.headers[...]</code> line and restart. What happens?",
     ["Works, no CORS header", "The server refuses to start: the function has no body", "The browser shows a 404", "Nothing changes"], 2,
     "A def with only a comment under it is a syntax error. Comment all three lines, or none."),
])

body = "\n".join([
    section("concept", "Concept", concept + stp),
    section("task", "Task", task),
    section("expected", "Expected output", expected),
    section("check", "Check yourself", check),
    section("takeaway", "Takeaway", callout("curl and the browser are the same client wearing different clothes. The Network tab is curl -i with a mouse; CORS is the one rule only the browser enforces.")),
    section("stuck", "Stuck?", stuck),
    section("quiz", "Quiz", qz),
])

write("stage8.html", page("The inspector: curl -i with a mouse", "stage8.html", body,
                          sub="The Network tab shows every field curl -i prints. Then break one header on purpose and watch the browser, not the server, say no.",
                          artifact='response.headers["Access-Control-Allow-Origin"] = "*"',
                          stage_label="Stage 8 · Session 3 · after dinner",
                          prev_page=("stage7.html", "Stage 7 · Someone else's client: the browser")))
