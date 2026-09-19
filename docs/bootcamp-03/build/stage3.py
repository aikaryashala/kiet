from lib import *

LOG = """Serving on http://localhost:8080  — Ctrl+C to stop
Bottle v0.13.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.

127.0.0.1 - - [21/Sep/2026 10:12:03] "GET /hai HTTP/1.1" 200 12
127.0.0.1 - - [21/Sep/2026 10:12:09] "GET /hello/Ravi HTTP/1.1" 200 22
127.0.0.1 - - [21/Sep/2026 10:12:20] "POST /isprime HTTP/1.1" 200 32
127.0.0.1 - - [21/Sep/2026 10:12:31] "POST /isprime HTTP/1.1" 200 33
127.0.0.1 - - [21/Sep/2026 10:12:44] "POST /isprime HTTP/1.1" 400 44
127.0.0.1 - - [21/Sep/2026 10:12:58] "GET /greet?name=Ravi&lang=te HTTP/1.1" 200 44
127.0.0.1 - - [21/Sep/2026 10:13:05] "GET /greet?name=Ravi&lang=en HTTP/1.1" 200 40
127.0.0.1 - - [21/Sep/2026 10:13:12] "GET /greet?name=Ravi HTTP/1.1" 200 44
127.0.0.1 - - [21/Sep/2026 10:13:20] "GET /greet?lang=te HTTP/1.1" 400 29
127.0.0.1 - - [21/Sep/2026 10:13:35] "GET /hai HTTP/1.1" 200 12
127.0.0.1 - - [21/Sep/2026 10:13:50] "GET /nothing HTTP/1.1" 404 741"""

concept = p("""A server is a program that waits. It starts, it prints one line, and then it does nothing until
somebody asks it something. In C you have written programs that run top to bottom and exit. This one
runs a loop you never see: wait for a request, answer it, wait again. <code>Ctrl+C</code> is the only
way it ends.""") + p("""The one asking is the <strong>client</strong>. Today that is <code>curl</code>, a small program
that builds a request, sends it, and prints whatever comes back. A request has a <strong>method</strong>
(<code>GET</code> to ask for something, <code>POST</code> to send something), a <strong>path</strong>
(<code>/hai</code>), maybe a <strong>query string</strong> (everything after the <code>?</code>), and
maybe a <strong>body</strong>. The server answers with a <strong>status code</strong> — <code>200</code>
means fine, <code>400</code> means your request was wrong, <code>404</code> means no such path —
and some content: text, or JSON.""") + p("""Nothing is written in this stage. The point is to see both sides at once. Terminal 1 is the server's
view: one log line per request, with the method, the path, the status and the size of the answer.
Terminal 2 is the client's view: what curl got back. Same event, two windows. Every stage after this
one is you standing in one of those two windows.""") + p("""There are exactly three places data can travel into a server: in the path, after the <code>?</code>,
or in the body. The four routes of <code>demo_server.py</code> use one door each. The route decides
which door it reads from; the client has to use that door. Step through one request below.""")

left = term("terminal 2 — curl", """$ curl "localhost:8080/greet?name=Ravi&lang=en"
{"greeting": "Hello Ravi", "lang": "en"}""", pre_id="s3curl") + term("terminal 1 — server", """127.0.0.1 - - [21/Sep/2026 10:13:05] "GET /greet?name=Ravi&lang=en HTTP/1.1" 200 40""", pre_id="s3log")

right = panel("the request, taken apart", slots([
    ("s3m", "method", "", ""),
    ("s3p", "path", "", ""),
    ("s3q", "query string", "", ""),
    ("s3b", "body", "", ""),
    ("s3r", "route that answers", "", ""),
    ("s3s", "status", "", ""),
    ("s3c", "content", "", ""),
]))

stp = stepper(left, right, [
    {"note": "curl is about to send one request. Nothing has left the machine yet.",
     "hl": {"s3curl": 0}, "slots": {}},
    {"note": "No -X, so the method is GET: \"give me something\". A POST would carry a body instead.",
     "hl": {"s3curl": 0}, "slots": {"s3m": {"v": "GET", "cls": "live"}}},
    {"note": "The path is everything from the first / up to the ?. The server picks a function by this and nothing else.",
     "hl": {"s3curl": 0}, "slots": {"s3m": {"v": "GET", "cls": ""}, "s3p": {"v": "/greet", "cls": "live"}}},
    {"note": "After the ? comes the query string: name=value pairs joined by &. This is why the URL is in quotes — the shell would otherwise treat & as its own instruction.",
     "hl": {"s3curl": 0}, "slots": {"s3p": {"v": "/greet", "cls": ""}, "s3q": {"v": "name=Ravi&lang=en", "cls": "live"}}},
    {"note": "A GET has no body. The third door is closed for this request.",
     "hl": {"s3curl": 0}, "slots": {"s3q": {"v": "name=Ravi&lang=en", "cls": ""}, "s3b": {"v": "(none)", "cls": "dead"}}},
    {"note": "The server receives it and writes one log line: who, when, the request line, then the status and the size. Compare the middle of the log line with the URL you typed.",
     "hl": {"s3curl": None, "s3log": 0}, "slots": {"s3b": {"v": "(none)", "cls": "dead"}, "s3r": {"v": "greet()  via  @route(\"/greet\")", "cls": "live"}}},
    {"note": "greet() reads name and lang from the query string, builds a dict, returns it. Bottle turns the dict into JSON and sets the status to 200.",
     "hl": {"s3log": 0}, "slots": {"s3r": {"v": "greet()  via  @route(\"/greet\")", "cls": ""}, "s3s": {"v": "200 OK", "cls": "live"}}},
    {"note": "curl prints the content it received. 40 bytes — the same 40 at the end of the server's log line.",
     "hl": {"s3curl": 1, "s3log": 0}, "slots": {"s3s": {"v": "200 OK", "cls": ""}, "s3c": {"v": "{\"greeting\": \"Hello Ravi\", \"lang\": \"en\"}", "cls": "live"}}},
])

task = steps([
    p("<strong>Terminal 1 — server.</strong> Go to the Stage 3 folder and start the server. It prints two things and then waits.") +
    term("terminal 1 — server", """$ cd ~/kiet-bootcamp-3/code/stage3
$ python3 demo_server.py
Serving on http://localhost:8080  — Ctrl+C to stop
Bottle v0.13.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.
"""),
    p("<strong>Terminal 2 — curl.</strong> Open a second terminal. Nothing goes in, text comes out.") +
    term("terminal 2 — curl", """$ curl localhost:8080/hai
Namasthey!!!"""),
    p("The name goes in the <strong>path</strong>.") +
    term("terminal 2 — curl", """$ curl localhost:8080/hello/Ravi
How are you doing Ravi"""),
    p("The number goes in the <strong>body</strong>, as JSON. <code>-X POST</code> sets the method, <code>-H</code> says what kind of body it is, <code>-d</code> is the body.") +
    term("terminal 2 — curl", """$ curl -X POST localhost:8080/isprime -H "Content-Type: application/json" -d '{"number": 17}'
{"number": 17, "is_prime": true}
$ curl -X POST localhost:8080/isprime -H "Content-Type: application/json" -d '{"number": 18}'
{"number": 18, "is_prime": false}"""),
    p("Same route, no body at all. The server says no, with status 400 and an error that tells you what to send.") +
    term("terminal 2 — curl", """$ curl -X POST localhost:8080/isprime
{"error": "send JSON like {\\"number\\": 17}"}"""),
    p("<code>name</code> and <code>lang</code> go in the <strong>query string</strong>, after the <code>?</code>. Quote the URL: the shell treats a bare <code>&amp;</code> as its own instruction.") +
    term("terminal 2 — curl", """$ curl "localhost:8080/greet?name=Ravi&lang=te"
{"greeting": "Namasthey Ravi", "lang": "te"}
$ curl "localhost:8080/greet?name=Ravi&lang=en"
{"greeting": "Hello Ravi", "lang": "en"}"""),
    p("Leave <code>lang</code> out: the server picks <code>te</code>. Leave <code>name</code> out: 400 again.") +
    term("terminal 2 — curl", """$ curl "localhost:8080/greet?name=Ravi"
{"greeting": "Namasthey Ravi", "lang": "te"}
$ curl "localhost:8080/greet?lang=te"
{"error": "name is required"}"""),
    p("<code>-i</code> shows the <strong>headers</strong> above the content: the status line first, then <code>Content-Type</code> and <code>Content-Length</code>. Your date and Python version will differ.") +
    term("terminal 2 — curl", """$ curl -i localhost:8080/hai
HTTP/1.0 200 OK
Date: Mon, 21 Sep 2026 04:43:35 GMT
Server: WSGIServer/0.2 CPython/3.12.3
Content-Length: 12
Content-Type: text/html; charset=UTF-8

Namasthey!!!"""),
    p("A path the server does not have. Bottle answers with its own HTML error page; the first line is what matters.") +
    term("terminal 2 — curl", """$ curl -i localhost:8080/nothing
HTTP/1.0 404 Not Found
Date: Mon, 21 Sep 2026 04:43:50 GMT
Server: WSGIServer/0.2 CPython/3.12.3
Content-Length: 741
Content-Type: text/html; charset=UTF-8

~"""),
    p("Go to Terminal 1 and press <kbd>Ctrl+C</kbd>. The server stops. Now ask again from Terminal 2.") +
    term("terminal 2 — curl", """$ curl localhost:8080/hai
curl: (7) Failed to connect to localhost port 8080 after 0 ms: Couldn't connect to server""") +
    p("No program is listening, so there is nobody to answer. Start it again in Terminal 1 with <code>python3 demo_server.py</code> and the same curl works."),
])

expected = p("After all of the above, Terminal 1 shows one line per request. The method, the path with its query string, the status and the byte count are all there. The timestamps are yours.") + \
    term("terminal 1 — server", LOG) + \
    p("Notice what is <em>not</em> in the log: the body of the POST, and the answer. The server logs the request line and the result, nothing more. Notice also that the two 400s and the 404 are logged just like the 200s — an error answer is still an answer.")

check = term("terminal 2 — curl", """$ python3 check.py
PASS: GET /hai -> Namasthey!!!
PASS: GET /hello/Ravi -> How are you doing Ravi
PASS: POST /isprime 17 -> is_prime true
PASS: POST /isprime 18 -> is_prime false
PASS: POST /isprime with no body -> 400 with an error
PASS: GET /greet?name=Ravi&lang=te
PASS: GET /greet?name=Ravi&lang=en
PASS: GET /greet?name=Ravi (lang defaults to te)
PASS: GET /greet without name -> 400
PASS: GET /nothing -> 404

10 passed, 0 failed""") + p("If it prints <code>Cannot connect to localhost:8080 — is the server running?</code>, Terminal 1 is not running the server. Start it and run the check again.")

stuck = p('All the curl lines, with a comment above each, are in <code>~/kiet-bootcamp-3/code/stage3/curl_commands.txt</code>. Open it beside Terminal 2 and copy one line at a time.') + \
    p('Reference: <a href="reference/curl.html">curl</a> · <a href="reference/http-basics.html">HTTP basics</a> · <a href="reference/bottle.html">Bottle</a> · <a href="troubleshooting.html">Troubleshooting</a> (address already in use, connection refused).')

qz = quiz([
    ("Which part of <code>curl \"localhost:8080/greet?name=Ravi&amp;lang=en\"</code> decides which function in the server runs?",
     ["<code>name=Ravi</code>", "<code>/greet</code>", "<code>lang=en</code>", "<code>localhost:8080</code>"], 2,
     "The path picks the route. The query string is data the route then reads; the host and port only pick which server program gets the request."),
    ("The server log shows <code>\"POST /isprime HTTP/1.1\" 400 44</code>. What happened?",
     ["The server crashed", "The server answered, saying the request was wrong", "curl could not connect", "The path does not exist"], 2,
     "400 is an answer. The server ran, decided the request was missing something, and said so. A crash would show a traceback in Terminal 1; a bad path would be 404; no connection would give no log line at all."),
    ("You press Ctrl+C in Terminal 1 and run <code>curl localhost:8080/hai</code>. What do you see?",
     ["<code>404 Not Found</code>", "<code>Namasthey!!!</code> from the last time", "<code>curl: (7) Failed to connect …</code>", "Nothing, curl waits forever"], 3,
     "A 404 needs a server to say it. With the process gone, nothing is listening on 8080, so the connection itself fails."),
    ("Which door does <code>-d '{\"number\": 17}'</code> use?",
     ["The path", "The query string", "The body", "The headers"], 3,
     "-d puts data in the body of the request. That is why it goes with -X POST: a GET has no body."),
])

body = "\n".join([
    section("concept", "Concept", concept + stp),
    section("task", "Task", task),
    section("expected", "Expected output", expected),
    section("check", "Check yourself", check),
    section("takeaway", "Takeaway", callout("Path, query string, body — three doors into the server. The terminal on the left is the server's view; the one on the right is the client's. Same event, two windows.")),
    section("stuck", "Stuck?", stuck),
    section("quiz", "Quiz", qz),
])

write("stage3.html", page("What a server actually is", "stage3.html", body,
                          sub="A server is a program that waits. Nothing to write today: start one, poke it with curl, and read both terminals at once.",
                          artifact="python3 demo_server.py   ·   curl localhost:8080/hai",
                          stage_label="Stage 3 · Session 2 · afternoon · observe only",
                          prev_page=("stage2.html", 'Stage 2 · Python talks to the database'),
                          next_page=("stage4.html", 'Stage 4 · Write your own server')))
