"""request-response.html — one request, drawn as a sequence diagram and stepped through.
Every value is real: the Stage 5 server on the sample team_details.db, captured with curl -i."""
from lib import *

CSS = """<style>
.rr{font-family:var(--mono);font-size:11.5px}
.rr .heads,.rr .hop{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
.rr .box{margin:0 5%;padding:8px 6px;border:1px solid var(--line);background:var(--paper);text-align:center;font-family:var(--serif);font-size:15px;font-weight:600;line-height:1.2}
.rr .box small{display:block;font-family:var(--mono);font-weight:400;font-size:10.5px;color:var(--muted);margin-top:3px}
.rr .hops{padding:14px 0 6px;background:
  linear-gradient(to right,transparent calc(16.667% - 1px),var(--line) calc(16.667% - 1px),var(--line) calc(16.667% + 1px),transparent calc(16.667% + 1px)),
  linear-gradient(to right,transparent calc(50% - 1px),var(--line) calc(50% - 1px),var(--line) calc(50% + 1px),transparent calc(50% + 1px)),
  linear-gradient(to right,transparent calc(83.333% - 1px),var(--line) calc(83.333% - 1px),var(--line) calc(83.333% + 1px),transparent calc(83.333% + 1px))}
.rr .hop{margin:0 0 14px}
.rr .hop[hidden]{display:none}
.rr .arrow{position:relative;border-bottom:2px solid var(--rust);padding:0 0 3px;text-align:center}
.rr .arrow span{display:inline-block;background:var(--paper);padding:2px 6px;border:1px solid var(--line2);line-height:1.35;white-space:nowrap;font-size:11px}
.rr .arrow::after{content:"";position:absolute;bottom:-6px;border:5px solid transparent}
.rr .arrow.r::after{right:-2px;border-left:9px solid var(--rust)}
.rr .arrow.l::after{left:-2px;border-right:9px solid var(--rust)}
.rr .s12{grid-column:1/3;margin:0 25%}
.rr .s23{grid-column:2/4;margin:0 25%}
.rr .note{padding:6px 10px;border:1px solid var(--line);background:var(--paper);text-align:left;line-height:1.5;font-size:11px}
.rr .c1{grid-column:1/3;margin:0 44% 0 2%}
.rr .c2{grid-column:1/4;margin:0 19%}
.rr b{color:var(--rust);font-weight:500}
.rrstep .stage{grid-template-columns:minmax(0,1.35fr) minmax(0,1fr)}
.rrstep pre.term .ln,.rrstep pre.code .ln{white-space:pre-wrap;overflow-wrap:break-word}
</style>
"""

HOPS = ["rr1", "rr2", "rr3", "rr4", "rr5", "rr6", "rr7"]

diagram = """<div class="rr">
<div class="heads">
<div class="box">curl / browser<small>terminal 2 · or app.js in Stage 7</small></div>
<div class="box">server.py<small>Bottle · localhost:8080</small></div>
<div class="box">team_details.db<small>SQLite · 4 rows</small></div>
</div>
<div class="hops">
<div class="hop" id="rr1" hidden><div class="arrow r s12"><span>GET /students<br>?college=Narayana+Junior+College</span></div></div>
<div class="hop" id="rr2" hidden><div class="note c2">@route("/students") → <b>students_by_college()</b><br>unpack: college = 'Narayana Junior College'</div></div>
<div class="hop" id="rr3" hidden><div class="arrow r s23"><span>SELECT … FROM students<br>WHERE inter_college = ?</span></div></div>
<div class="hop" id="rr4" hidden><div class="arrow l s23"><span>2 rows, as tuples</span></div></div>
<div class="hop" id="rr5" hidden><div class="note c2">pack: tuples → dicts → <b>{"count": 2, "students": [...]}</b><br>Bottle: dict → JSON text · status 200</div></div>
<div class="hop" id="rr6" hidden><div class="arrow l s12"><span>HTTP/1.0 200 OK<br>Content-Type: application/json · 254 bytes</span></div></div>
<div class="hop" id="rr7" hidden><div class="note c1">curl prints it ·<br>fetch() hands it to app.js</div></div>
</div>
</div>"""

db = table("team_details.db — SELECT * FROM students", ["student_name", "inter_college", "inter_city"], [
    ("Ravi Teja Kanchi", "Sri Chaitanya Junior College", "Visakhapatnam"),
    ("Lakshmi Prasanna Gudla", "Narayana Junior College", "Vijayawada"),
    ("Sai Kiran Bommu", "Sri Chaitanya Junior College", "Visakhapatnam"),
    ("Divya Sree Pothula", "Narayana Junior College", "Vijayawada"),
], table_id="rrdb")

req = term("terminal 2 — the request (the > lines are what curl -v shows going out)", """$ curl -i "localhost:8080/students?college=Narayana+Junior+College"
> GET /students?college=Narayana+Junior+College HTTP/1.1
> Host: localhost:8080""", pre_id="rrreq")

srv = code("server.py — the route that answers /students", '''@route("/students")
def students_by_college():
    college = request.query.get("college")       # unpack
    if college is None:
        response.status = 400
        return {"error": "college parameter is required"}
    rows = query("SELECT student_name, inter_college, inter_city "
                 "FROM students WHERE inter_college = ?", [college])
    # ^ query
    return {"count": len(rows), "students": pack(rows)}   # pack''', pre_id="rrcode", lang="py")

res = term("terminal 2 — the response (curl -i: status line, headers, blank line, body)", """HTTP/1.0 200 OK
Date: Sun, 20 Sep 2026 23:36:37 GMT
Server: WSGIServer/0.2 CPython/3.12.3
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 254

{"count": 2, "students": [{"student_name": "Lakshmi Prasanna Gudla", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}, {"student_name": "Divya Sree Pothula", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}]}""", pre_id="rrres")


def step(note, upto, hl, cur=None):
    s = {"note": note, "show": {h: (k < upto) for k, h in enumerate(HOPS)},
         "hl": {"rrreq": -1, "rrcode": -1, "rrres": -1}}
    s["hl"].update(hl)
    s["table"] = {"rrdb": {"cur": cur or [], "skip": [r for r in range(4) if cur and r not in cur]}}
    return s


steps_json = [
    step("Nothing has happened yet. Three programs, three places: the client in terminal 2, server.py waiting on port 8080, and the database file on disk. Press Forward.", 0, {}),
    step("You type the curl. curl builds an HTTP request: a request line — method GET, the path /students, the query string after the ? — and a Host header. The + is how a space travels in a URL.", 1, {"rrreq": 0}),
    step("The request crosses to port 8080. Bottle reads the path, /students, and calls the one function decorated with @route(\"/students\"). The query string waits inside request.query.", 2, {"rrreq": 1, "rrcode": 0}),
    step("Unpack. request.query.get(\"college\") returns the value with the + turned back into a space: 'Narayana Junior College'. Had the parameter been missing, this would be None and the 400 branch would answer instead.", 2, {"rrcode": 2}),
    step("Query. The function hands SQL to sqlite3, with ? standing in for the value. It is the same SELECT you would type in the sqlite3 shell; only the college is filled in by Python.", 3, {"rrcode": 6}),
    step("SQLite scans the table and returns the two matching rows as a list of tuples, one tuple per row, one item per column. The other two rows never leave the file.", 4, {"rrcode": 7}, cur=[1, 3]),
    step("Pack. Each tuple becomes a dict with the column names as keys. The return value is one dict: the count and the list. That is all the function does; it never mentions HTTP.", 5, {"rrcode": 9}, cur=[1, 3]),
    step("Bottle turns the dict into JSON text, adds the status line 200 OK and Content-Type: application/json, and the after_request hook adds the CORS header. 254 bytes go back the way the request came.", 6, {"rrres": 0}),
    step("curl prints the headers and the body. In Stage 7 the very same bytes arrive in the browser's fetch(), and app.js draws them on the page. The server cannot tell the two clients apart.", 7, {"rrres": 6}),
]

stp = stepper(diagram + db, req + srv + res, steps_json).replace('<div class="stepper">', '<div class="stepper rrstep">', 1)

hops = table("the four crossings", ["#", "from → to", "what crosses", "you see it in"], [
    ("1", "client → server", "<code>GET /students?college=Narayana+Junior+College HTTP/1.1</code>", "<code>curl -v</code>, or the Network tab (Stage 8)"),
    ("2", "server → SQLite", "<code>SELECT … WHERE inter_college = ?</code> with the value", "the sqlite3 shell, typed by hand (Stage 1)"),
    ("3", "SQLite → server", "a list of tuples: <code>[('Lakshmi Prasanna Gudla', 'Narayana Junior College', 'Vijayawada'), …]</code>", "<code>print(rows)</code> in Stage 2"),
    ("4", "server → client", "status line, headers, blank line, JSON body", "<code>curl -i</code> (Stage 3), the browser (Stage 7)"),
], prose=True)

body = "\n".join([
    section("trip", "One request, start to finish", p("""One curl from terminal 2, followed all the way: into the server, down to the
database file, and back. The diagram is a sequence diagram — time runs downward, each column is one program.
Step through it with Forward, or press Play. Everything on the right is real output from the Stage 5 server
on the sample database.""") + stp),
    section("hops", "The four crossings", p("The same trip as a table. Two of the crossings are HTTP (1 and 4), two are function calls inside the server (2 and 3). The stages of Day 1 are exactly these four, one at a time.") + hops),
    section("try", "See it yourself", p("With the Stage 5 server running in terminal 1, ask curl to show the request too. Lines starting with <code>&gt;</code> went out; lines with <code>&lt;</code> came back.") +
            term("terminal 2", """$ curl -v "localhost:8080/students?college=Narayana+Junior+College"
*   Trying 127.0.0.1:8080...
* Connected to localhost (127.0.0.1) port 8080
> GET /students?college=Narayana+Junior+College HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/8.5.0
> Accept: */*
>
< HTTP/1.0 200 OK
< Date: Sun, 20 Sep 2026 23:36:37 GMT
< Server: WSGIServer/0.2 CPython/3.12.3
< Content-Type: application/json
< Access-Control-Allow-Origin: *
< Content-Length: 254
<
{"count": 2, "students": [{"student_name": "Lakshmi Prasanna Gudla", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}, {"student_name": "Divya Sree Pothula", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}]}
* Closing connection""")),
])

write("request-response.html", page("Request and response", "request-response.html", body,
                                    sub="One curl, followed into the server, down to SQLite, and back — as a diagram you can step through.",
                                    artifact="GET /students?college=…  →  SELECT … WHERE ?  →  rows  →  JSON  →  200 OK",
                                    stage_label="Diagram", head_extra=CSS))
