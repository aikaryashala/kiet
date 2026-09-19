from lib import *

D = 1  # depth: reference/ pages sit one folder down


def ref_page(title, cur, body, sub, artifact):
    write(cur, page(title, cur, body, depth=D, sub=sub, artifact=artifact, stage_label="Reference"))


# ---------------------------------------------------------------- python-cheatsheet
body = section("basics", "Running, variables, print", p("No compile step, no main, no semicolons, no braces, no types on variables. Indentation is the block.") +
    code("hello.py", '''name = "Ravi Teja Kanchi"        # a string
count = 4                        # a number, no int keyword
print(name)
print(f"{name} has {count} rows")   # f-string: variables inside text
print("Namasthey " + name)          # + joins strings''', copy=True) +
    term("terminal", """$ python3 hello.py
Ravi Teja Kanchi
Ravi Teja Kanchi has 4 rows
Namasthey Ravi Teja Kanchi""")) + \
section("lists", "Lists, tuples, len, append, for, range", code("rows.py", '''rows = [                                   # a list: [ ... ]
    ("Ravi Teja Kanchi", "Visakhapatnam"), # a tuple: ( ... )
    ("Lakshmi Prasanna Gudla", "Vijayawada"),
]
rows.append(("Sai Kiran Bommu", "Visakhapatnam"))   # add at the end
print(len(rows))                                     # 3

for row in rows:               # for each element, no index
    name, city = row           # unpacking: one name per item of the tuple
    print(f"{name} - {city}")

for i in range(3):             # 0, 1, 2  — the C for(i=0;i<3;i++)
    print(i)
for d in range(2, 10):         # 2 .. 9
    print(d)

print(rows[0])                 # first item
print(rows[0][1])              # second item of the first tuple: "Visakhapatnam"''', copy=True) +
    p("<strong>SQLite gives you exactly this:</strong> <code>fetchall()</code> returns a list of tuples, one tuple per row, one item per column.")) + \
section("dicts", "Dicts", code("dicts.py", '''student = {"student_name": "Ravi Teja Kanchi",      # a dict: { "key": value }
           "inter_college": "Sri Chaitanya Junior College",
           "inter_city": "Visakhapatnam"}

print(student["student_name"])     # by key
print(student.get("phone"))        # missing key: None, no crash
student["inter_city"] = "Vizag"    # change a value
student["phone"] = "9999"          # add a key

import json
print(json.dumps(student))         # the dict as JSON text''', copy=True) +
    p("A dict is a struct whose fields are named by strings. A dict <em>is</em> JSON, near enough. In Bottle, return a dict and the client receives JSON.")) + \
section("functions", "Functions, if, %, int()", code("funcs.py", '''def is_even(n):            # def, a name, the parameters. No types, no prototype.
    return n % 2 == 0      # % is remainder, same as C


def is_prime(n):
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True


def greet(name, lang):
    if lang == "en":
        return f"Hello {name}"
    elif lang == "te":
        return f"Namasthey {name}"
    else:
        return f"? {name}"


print(is_prime(17), is_even(17))   # True False
print(int("17") + 1)               # int(): text to number, like atoi. Prints 18
print("17" + "1")                  # strings: prints 171''', copy=True) +
    p("Comparisons: <code>==</code>, <code>!=</code>, <code>&lt;</code>, <code>&gt;=</code>. Combine with <code>and</code>, <code>or</code>, <code>not</code>. There is no <code>&amp;&amp;</code>.")) + \
section("imports", "import, sys.argv, None", code("greet.py", '''import sys          # the standard library module for argv, exit, etc.
import sqlite3      # the SQLite driver, also standard library
import json         # dict <-> JSON text
from bottle import route, run, request, response   # from the bottle.py file sitting NEXT TO this file

# sys.argv is a list of strings. [0] is the file name, like C's argv.
if len(sys.argv) < 2:
    print("usage: python3 greet.py <name>")
else:
    print(f"Namasthey {sys.argv[1]}")

# None is Python's NULL. Things that find nothing give None.
value = {"a": 1}.get("b")
if value is None:
    print("no b")''', copy=True) +
    term("terminal", """$ python3 greet.py Ravi
Namasthey Ravi
no b""")) + \
section("later", "Deliberately not here", p("You will meet these later; the bootcamp does not use them: classes, list comprehensions, <code>try/except</code>, <code>with</code>, <code>if __name__ == \"__main__\"</code>, lambdas, type hints, virtual environments, pip."))
ref_page("Python cheatsheet", "reference/python-cheatsheet.html", body,
         "Everything the eight stages use, nothing more. Python as deltas from C.", "python3 file.py")

# ---------------------------------------------------------------- c-to-python
rows = [
    ("<code>int x = 5;</code>", "<code>x = 5</code>"),
    ("<code>{ ... }</code>", "indentation"),
    ("<code>int arr[3] = {1, 2, 3};</code>", "<code>arr = [1, 2, 3]</code>"),
    ("<code>struct</code>", "dict: <code>{\"student_name\": \"Ravi\", ...}</code>"),
    ("<code>printf(\"%s\\n\", s);</code>", "<code>print(f\"{s}\")</code>"),
    ("<code>for (i = 0; i &lt; n; i++)</code>", "<code>for i in range(n):</code>"),
    ("for each element", "<code>for x in items:</code>"),
    ("<code>strcmp(a, b) == 0</code>", "<code>a == b</code>"),
    ("<code>atoi(s)</code>", "<code>int(s)</code>"),
    ("<code>#include &lt;stdio.h&gt;</code>", "<code>import sys</code>"),
    ("<code>NULL</code>", "<code>None</code>"),
    ("<code>argv[1]</code>", "<code>sys.argv[1]</code>"),
    ("<code>return 0;</code> at the end of main", "nothing"),
    ("<code>int f(int n) { ... }</code>", "<code>def f(n):</code>"),
    ("<code>a &amp;&amp; b</code>, <code>a || b</code>, <code>!a</code>", "<code>a and b</code>, <code>a or b</code>, <code>not a</code>"),
    ("<code>// comment</code>", "<code># comment</code>"),
    ("<code>FILE *f = fopen(...)</code>", "<code>connection = sqlite3.connect(...)</code>"),
    ("<code>fclose(f)</code>", "<code>connection.close()</code>"),
]
body = section("table", "The translation table", table(None, ["C", "Python"], rows, prose=True)) + \
    section("side", "Side by side", code("filter.c", '''struct student { char name[64]; char city[32]; };
struct student rows[4] = { ... };

for (int i = 0; i < 4; i++) {
    if (strcmp(rows[i].city, "Visakhapatnam") == 0) {
        printf("%s\\n", rows[i].name);
    }
}''') + code("filter.py", '''rows = [("Ravi Teja Kanchi", "Visakhapatnam"), ("Lakshmi Prasanna Gudla", "Vijayawada"), ...]

for row in rows:
    name, city = row
    if city == "Visakhapatnam":
        print(name)''') + p("Same loop, same if. No indexes, no sizes, no string functions. In Stage 1 you see that <code>SELECT student_name FROM students WHERE inter_city = 'Visakhapatnam'</code> is this loop too."))
ref_page("C to Python", "reference/c-to-python.html", body, "The same ideas, the new spelling.", "strcmp(a, b) == 0   →   a == b")

# ---------------------------------------------------------------- sqlite-cli
body = section("open", "Open a database", term("terminal", """$ cd ~/kiet-bootcamp-3/data
$ sqlite3 team_details.db
SQLite version 3.45.1 2024-01-30 16:01:20
Enter ".help" for usage hints.
sqlite> """) + p("The file is created if it does not exist. The prompt changes to <code>sqlite&gt;</code>: you are now typing SQL, not shell. Every SQL statement ends with <code>;</code>. Dot-commands do not.") +
    p("<strong>No <code>sqlite3</code> command?</strong> Python ships the same shell:") + term("terminal", """$ python3 -m sqlite3 team_details.db
sqlite> """)) + \
section("dots", "Dot-commands", p("Lines starting with a dot are settings of the shell, not SQL. No semicolon. The Python fallback shell has none of them and prints rows as tuples.") + term("sqlite> with .mode box", """sqlite> .mode box
sqlite> SELECT student_name, inter_city FROM students WHERE inter_city = 'Vijayawada';
┌────────────────────────┬────────────┐
│      student_name      │ inter_city │
├────────────────────────┼────────────┤
│ Lakshmi Prasanna Gudla │ Vijayawada │
│ Divya Sree Pothula     │ Vijayawada │
└────────────────────────┴────────────┘""") + rules([
    ("<code>.tables</code>", "list the tables in this file"),
    ("<code>.schema</code>", "print the CREATE TABLE statements"),
    ("<code>.mode box</code>", "draw every result as a table with borders and the column names on top — set this first"),
    ("<code>.headers on</code>", "print column names above results (box mode already does)"),
    ("<code>.mode column</code>", "align results in plain columns, no borders (the default is <code>a|b|c</code>)"),
    ("<code>.read schema.sql</code>", "run every statement in a file"),
    ("<code>.quit</code>", "leave (or Ctrl+D)"),
])) + \
section("file", "Run a .sql file", term("terminal", """$ sqlite3 all_students.db < all_students.sql
$ sqlite3 all_students.db "SELECT COUNT(*) FROM students;"
200""") + p("<code>&lt;</code> feeds the file to sqlite3 as if you typed it. The second form runs one statement and exits — handy for a quick count.") +
    p("With the Python fallback, use <code>.read</code> from inside the shell:") + term("terminal", """$ python3 -m sqlite3 all_students.db
sqlite> .read all_students.sql
sqlite> SELECT COUNT(*) FROM students;
200
sqlite> .quit"""))
ref_page("sqlite3 command line", "reference/sqlite-cli.html", body, "Open a .db file, look inside, run a .sql script.", "sqlite3 team_details.db")

# ---------------------------------------------------------------- sql-for-students-table
body = section("create", "CREATE TABLE", code("schema.sql", '''CREATE TABLE students (
    student_name TEXT,
    inter_college TEXT,
    inter_city TEXT
);''', copy=True) + p("Defines the struct. Three columns, all text. Run once per database file.")) + \
section("insert", "INSERT", code("sql", """INSERT INTO students VALUES ('Ravi Teja Kanchi', 'Sri Chaitanya Junior College', 'Visakhapatnam');

INSERT INTO students VALUES
  ('Lakshmi Prasanna Gudla', 'Narayana Junior College', 'Vijayawada'),
  ('Sai Kiran Bommu', 'Sri Chaitanya Junior College', 'Visakhapatnam');""", copy=True) + p("Values in the column order. Text in single quotes. The second form adds several rows in one statement.")) + \
section("select", "SELECT", code("sql", """SELECT * FROM students;                                   -- every column, every row
SELECT student_name FROM students;                        -- one column
SELECT student_name, inter_city FROM students;            -- two columns

SELECT * FROM students WHERE inter_city = 'Vijayawada';   -- the for-loop with the if inside
SELECT student_name FROM students
  WHERE inter_college = 'Narayana Junior College' AND inter_city = 'Vijayawada';
SELECT * FROM students WHERE student_name LIKE 'Sai%';    -- % matches anything: names starting with Sai
SELECT * FROM students WHERE student_name LIKE '%Reddy%';

SELECT DISTINCT inter_college FROM students;              -- each college once
SELECT DISTINCT inter_college FROM students ORDER BY inter_college;
SELECT COUNT(*) FROM students;                            -- how many rows
SELECT COUNT(*) FROM students WHERE inter_city = 'Kurnool';
SELECT * FROM students ORDER BY student_name;             -- sorted""", copy=True) +
    term("sqlite> with .headers on and .mode column", """sqlite> SELECT student_name, inter_city FROM students WHERE inter_city = 'Vijayawada';
student_name            inter_city
----------------------  ----------
Lakshmi Prasanna Gudla  Vijayawada
Divya Sree Pothula      Vijayawada""")) + \
section("update", "UPDATE and DELETE", code("sql", """UPDATE students SET inter_city = 'Visakhapatnam' WHERE inter_city = 'Vizag';
DELETE FROM students WHERE student_name = 'Sai Kiran Bommu';""", copy=True) + p("Both take the same <code>WHERE</code> as SELECT. <strong>Without a WHERE they touch every row.</strong>")) + \
section("q", "The ? in Python", code("python", '''cursor.execute("SELECT student_name FROM students WHERE inter_college = ?", [college])''') + p("Never paste a value into the SQL string. <code>?</code> is the slot; the list after the SQL fills it. One <code>?</code>, one item. Two <code>?</code>s, two items, in order."))
ref_page("SQL for the students table", "reference/sql-for-students-table.html", body, "Every statement this bootcamp uses, all against the one table.", "SELECT * FROM students WHERE inter_city = 'Vijayawada';")

# ---------------------------------------------------------------- json
body = section("what", "What it is", p("JSON is text that looks like a Python dict or list. It is how programs hand each other data over HTTP. Keys are strings in double quotes. Values are strings, numbers, <code>true</code>/<code>false</code>, <code>null</code>, lists <code>[ ]</code>, or objects <code>{ }</code>.") +
    code("json", '''{"count": 2, "students": [
  {"student_name": "Ravi Teja Kanchi", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"},
  {"student_name": "Sai Kiran Bommu", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}
]}''')) + \
section("map", "Python ↔ JSON", table(None, ["Python", "JSON"], [
    ("<code>dict</code>", "<code>{ }</code> object"), ("<code>list</code>", "<code>[ ]</code> array"), ("<code>str</code>", "<code>\"…\"</code> string"),
    ("<code>int</code>, <code>float</code>", "number"), ("<code>True</code> / <code>False</code>", "<code>true</code> / <code>false</code>"), ("<code>None</code>", "<code>null</code>")], prose=True)) + \
section("code", "dumps and loads", code("python", '''import json

answer = {"number": 17, "is_prime": True}
text = json.dumps(answer)          # dict -> text:  {"number": 17, "is_prime": true}
print(text)

data = json.loads('{"number": 4}') # text -> dict
print(data["number"] + 1)          # 5''', copy=True) + p("In Bottle you rarely call these yourself: return a dict from a route and Bottle does <code>dumps</code>; read <code>request.json</code> and Bottle has done <code>loads</code>."))
ref_page("JSON", "reference/json.html", body, "A dict, written down.", "json.dumps(result)")

# ---------------------------------------------------------------- bottle
body = section("min", "The smallest server", code("server.py", '''from bottle import route, run, request, response, hook

@route("/hai")
def hai():
    return "Namasthey!!!"          # a string -> text response

run(host="localhost", port=8080, debug=True)''', copy=True) + p("<code>bottle.py</code> must sit in the same folder as your file. <code>debug=True</code> makes every request print a log line in the terminal.")) + \
section("routes", "Ways to take input", code("server.py", '''@route("/hello/<name>")               # path parameter -> function argument
def hello(name):
    return f"How are you doing {name}"

@route("/greet")                      # query string: /greet?name=Ravi&lang=te
def greet():
    name = request.query.get("name")  # None if it is not there
    if name is None:
        response.status = 400
        return {"error": "name is required"}
    return {"greeting": f"Namasthey {name}"}   # a dict -> JSON response

@route("/isprime", method="POST")     # body: -d '{"number": 17}'
def isprime():
    data = request.json               # the body as a dict, or None
    if data is None:
        response.status = 400
        return {"error": "send JSON like {\\"number\\": 17}"}
    return {"number": data.get("number")}''', copy=True)) + \
section("hook", "After every response", code("server.py", '''@hook("after_request")
def allow_browser():
    response.headers["Access-Control-Allow-Origin"] = "*"''', copy=True) + p("Runs after each route, before the answer leaves. This header is what lets a web page on another port read the answer (Stage 8).")) + \
section("summary", "In one table", rules([
    ("<code>@route(\"/path\")</code>", "register the function below at that path, for GET"),
    ("<code>@route(\"/p\", method=\"POST\")</code>", "same, for POST"),
    ("<code>&lt;name&gt;</code> in a path", "becomes a function argument"),
    ("<code>request.query.get(\"k\")</code>", "value after <code>?k=</code>, or None"),
    ("<code>request.json</code>", "the JSON body as a dict, or None"),
    ("<code>return \"text\"</code>", "text response, 200"),
    ("<code>return {...}</code>", "JSON response, 200"),
    ("<code>response.status = 400</code>", "set the status before returning"),
    ("<code>response.headers[\"X\"] = \"y\"</code>", "add a response header"),
    ("<code>run(host, port, debug)</code>", "start waiting; Ctrl+C stops"),
]))
ref_page("Bottle", "reference/bottle.html", body, "Everything from bottle.py that the stages use.", "from bottle import route, run, request, response, hook")

# ---------------------------------------------------------------- curl
body = section("forms", "The forms you need", term("terminal", """$ curl localhost:8080/hai
Namasthey!!!
$ curl -i localhost:8080/hai
HTTP/1.0 200 OK
Date: Mon, 21 Sep 2026 04:43:35 GMT
Server: WSGIServer/0.2 CPython/3.12.3
Content-Length: 12
Content-Type: text/html; charset=UTF-8

Namasthey!!!
$ curl "localhost:8080/greet?name=Ravi&lang=te"
{"greeting": "Namasthey Ravi", "lang": "te"}
$ curl -X POST localhost:8080/isprime -H "Content-Type: application/json" -d '{"number": 17}'
{"number": 17, "is_prime": true}
$ curl "localhost:8080/students?college=Narayana+Junior+College"
{"count": 2, "students": [...]}
$ curl -s localhost:8080/colleges
{"colleges": ["Narayana Junior College", "Sri Chaitanya Junior College"]}""")) + \
section("flags", "Flags", rules([
    ("<code>-i</code>", "show the response headers (status line first) above the body"),
    ("<code>-X POST</code>", "use the POST method instead of GET"),
    ("<code>-H \"Content-Type: application/json\"</code>", "tell the server the body is JSON"),
    ("<code>-d '{\"number\": 17}'</code>", "the body. Single quotes outside so the double quotes inside survive the shell"),
    ("<code>-s</code>", "silent: no progress bar when you pipe or save the output"),
])) + \
section("quoting", "Quoting and spaces", p("<strong>Quote any URL with <code>&amp;</code> or <code>?</code> in it.</strong> Unquoted, the shell reads <code>&amp;</code> as \"run in background\" and the second parameter never reaches curl.") +
    p("<strong>Spaces are not allowed in a URL.</strong> Write <code>+</code> instead: <code>college=Narayana+Junior+College</code>. The server turns it back into a space. The browser does the same thing for you, spelling it <code>%20</code>."))
ref_page("curl", "reference/curl.html", body, "The client you can see through.", "curl -i localhost:8080/hai")

# ---------------------------------------------------------------- http-basics
body = section("req", "A request", term("what curl sends", """GET /greet?name=Ravi&lang=en HTTP/1.1
Host: localhost:8080
Accept: */*
""") + p("First line: <strong>method</strong>, <strong>path</strong> with its <strong>query string</strong>, protocol version. Then headers, one per line. Then a blank line. Then the body, if any (a GET has none).") +
    term("what curl sends for a POST", """POST /isprime HTTP/1.1
Host: localhost:8080
Content-Type: application/json
Content-Length: 14

{"number": 17}""")) + \
section("res", "A response", term("what the server sends back", """HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 32

{"number": 17, "is_prime": true}""") + p("First line: protocol, <strong>status code</strong>, reason. Then headers. Blank line. Body. <code>curl -i</code> shows exactly this; the browser's Network tab shows the same fields under Headers and Response.")) + \
section("doors", "Three places data can be", rules([
    ("path", "<code>/hello/Ravi</code> — part of the address. Bottle: <code>@route(\"/hello/&lt;name&gt;\")</code>"),
    ("query string", "<code>/greet?name=Ravi&amp;lang=en</code> — after the <code>?</code>. Bottle: <code>request.query.get(\"name\")</code>"),
    ("body", "<code>-d '{\"number\": 17}'</code> — only with POST. Bottle: <code>request.json</code>"),
])) + \
section("codes", "Status codes you will see", rules([
    ("<code>200</code>", "OK. The route ran and returned something."),
    ("<code>400</code>", "Bad request. The route ran and decided your request was missing or wrong. The body says what."),
    ("<code>404</code>", "Not found. No route has that path."),
    ("<code>500</code>", "The route crashed. With <code>debug=True</code> the traceback is in Terminal 1."),
])) + \
section("ct", "Content-Type", p("A header that says what the body is. <code>text/html</code> when a route returns a string, <code>application/json</code> when it returns a dict. When you POST JSON you must send it too, or the server will not parse the body."))
ref_page("HTTP basics", "reference/http-basics.html", body, "The request line, the status line, and the three doors.", "GET /greet?name=Ravi HTTP/1.1")
