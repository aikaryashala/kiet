from lib import *

concept = p("""You know C. Python is the same ideas with less typing. There is no compile step:
<code>python3 file.py</code> runs the file top to bottom, and that is the whole build. There is no
<code>main()</code>, no semicolons, no braces. A block is whatever is indented under a line that ends
with a colon, so the indentation you already do for readability is now the syntax.""") + \
p("""Variables have no declared type: <code>x = 5</code> and later <code>x = "five"</code> are both fine.
Strings are text in quotes, and an <em>f-string</em> puts a variable inside text:
<code>f"Namasthey {name}"</code>. That replaces every <code>printf</code> format you have ever written.""") + \
p("""Three containers do all the work in this bootcamp. A <strong>list</strong> is <code>[1, 2, 3]</code>: an
array that grows with <code>.append</code>. A <strong>tuple</strong> is <code>("Ravi", "Vizag")</code>: a fixed
group of values that you take apart with <code>name, city = row</code>. A <strong>dict</strong> is
<code>{"student_name": "Ravi"}</code>: a struct whose fields are strings. Why these three? Because in
Stage 2 SQLite hands you a list of tuples, and in Stage 5 you hand the browser a list of dicts. Everything
between is a <code>for</code> loop with an <code>if</code> inside.""") + \
p("""Two things will look strange. A line starting with <code>@</code> above a function is a
<em>decorator</em>; in this bootcamp it means exactly one thing, "register this function at this
address", and nothing more. And <code>None</code> is Python's <code>NULL</code>: what you get back when a
lookup finds nothing, guarded with <code>if x is None:</code>.""") + \
p("""Seven short exercises follow. Each is one file with a goal at the top and the expected output in a
comment. Do them in order; each feeds a later stage. Everything <em>not</em> here — classes, try/except,
list comprehensions, <code>with</code>, virtual environments — is deliberately left for later.""")


def block(n, title, teach, filename, run_cmd, expected, feeds):
    return (f"<h3>Block {n} — {title}</h3>" + p(teach) +
            code_file(f"code/stage0/{filename}", f"code/stage0/{filename}") +
            term("terminal", f"$ {run_cmd}\n{expected}") +
            p(f"<em>Feeds:</em> {feeds}"))


task = p("Open a terminal in the Stage 0 folder. Each block: read the file, fill in the <code>TODO</code> lines with any editor, run it, compare with the expected output shown under the command.") + \
    term("terminal", "$ cd ~/kiet-bootcamp-3/code/stage0\n$ ls\n01_hello.py  03_dicts.py       05_greet.py      07_filter_pack.py  solution\n02_rows.py   04_prime_even.py  06_read_only.py  check.py") + \
    block(1, "Running a program", "No compile, no main, no semicolons. <code>print</code> writes a line. An f-string puts variables inside text. Use the sample name first; once the check passes, put your own details in.",
          "01_hello.py", "python3 01_hello.py", "My name is Ravi Teja Kanchi\nI studied at Sri Chaitanya Junior College, Visakhapatnam", "Stage 4, <code>/wish/&lt;name&gt;</code>") + \
    block(2, "Lists and tuples", "A list of tuples is exactly what SQLite gives back in Stage 2. <code>.append</code> adds to the end, <code>len</code> counts, <code>for row in rows</code> visits each one, <code>name, college, city = row</code> takes a tuple apart.",
          "02_rows.py", "python3 02_rows.py", "Ravi Teja Kanchi - Visakhapatnam\nLakshmi Prasanna Gudla - Vijayawada\nSai Kiran Bommu - Visakhapatnam\nDivya Sree Pothula - Vijayawada\n4 rows", "Stage 2") + \
    block(3, "Dicts", "A dict is a struct with string field names, and it is JSON near enough: <code>json.dumps</code> turns it into JSON text. <code>d[\"k\"]</code> reads a field; <code>d.get(\"k\")</code> gives <code>None</code> instead of crashing when the field is not there.",
          "03_dicts.py", "python3 03_dicts.py", 'Ravi Teja Kanchi\nNone\n[{"student_name": "Ravi Teja Kanchi", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}, {"student_name": "Lakshmi Prasanna Gudla", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}, {"student_name": "Sai Kiran Bommu", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}]', "Stage 5, packing rows for the browser") + \
    block(4, "Functions, if, %, range, int()", "<code>def</code> starts a function; no prototype, no return type. <code>%</code> is remainder. <code>range(2, n)</code> is the C counting loop. <code>int(\"17\")</code> is <code>atoi</code>.",
          "04_prime_even.py", "python3 04_prime_even.py", "18\n2 prime=True even=True\n4 prime=False even=True\n17 prime=True even=False\n18 prime=False even=True\n1 prime=False even=False", "Stage 3 and 4, the POST routes") + \
    block(5, "Imports and argv", "<code>import</code> brings in a module: from the standard library, or a file sitting next to yours. <code>sys.argv</code> is C's <code>argv</code>, a list of strings.",
          "05_greet.py", "python3 05_greet.py Ravi\nNamasthey Ravi\n$ python3 05_greet.py", "usage: python3 05_greet.py <name>", "Stage 2, <code>by_college.py</code>") + \
    "<h3>Block 6 — Two strange things</h3>" + p("Read only. Do not run it: <code>bottle.py</code> is not in this folder, on purpose. Answer the four questions at the bottom of the file in the comments.") + \
    code_file("code/stage0/06_read_only.py", "code/stage0/06_read_only.py") + p("<em>Feeds:</em> Stage 3, reading <code>demo_server.py</code>.") + \
    block(7, "Put it together", "Rows in, a filter with <code>if</code>, dicts out, JSON printed. This is Stage 5 with the SQL and the HTTP taken away.",
          "07_filter_pack.py", "python3 07_filter_pack.py", '{"count": 2, "students": [{"student_name": "Ravi Teja Kanchi", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}, {"student_name": "Sai Kiran Bommu", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}]}', "Stage 5, every route")

expected = p("The output of each file is shown under its command above and repeated in the comment at the top of the file. The two lines of Block 1 will differ once you put your own name in; everything else must match exactly, character for character. Spaces and capital letters count.")

check = term("terminal", """$ python3 check.py
PASS: 01_hello.py prints 'My name is ...' and 'I studied at ..., ...'
PASS: 02_rows.py prints the expected output
PASS: 03_dicts.py prints the expected output
PASS: 04_prime_even.py prints the expected output
PASS: 05_greet.py Ravi prints the expected output
PASS: 05_greet.py prints the expected output
PASS: 06_read_only.py has all four answers filled in
PASS: 07_filter_pack.py prints the expected output

8 passed, 0 failed""") + p("A FAIL line names the file and shows the first line that differs. Before you start, running the check shows eight FAILs — that is the starting point, not a problem.")

stuck = p('Solutions: <code>~/kiet-bootcamp-3/code/stage0/solution/</code>. Compare line by line before copying. <code>python3 check.py solution</code> runs the check against them.') + \
    p('Reference: <a href="reference/python-cheatsheet.html">Python cheatsheet</a> · <a href="reference/c-to-python.html">C to Python</a> · <a href="reference/json.html">JSON</a>.')

table_html = table("C to Python", ["C", "Python"], [
    ("<code>int x = 5;</code>", "<code>x = 5</code>"), ("<code>{ ... }</code>", "indentation"),
    ("<code>int arr[3]</code>", "<code>arr = [1, 2, 3]</code>"), ("<code>struct</code>", "dict"),
    ("<code>printf(\"%s\", s)</code>", "<code>print(f\"{s}\")</code>"),
    ("<code>for (i=0; i&lt;n; i++)</code>", "<code>for i in range(n):</code>"), ("for each element", "<code>for x in items:</code>"),
    ("<code>strcmp(a, b) == 0</code>", "<code>a == b</code>"), ("<code>atoi(s)</code>", "<code>int(s)</code>"),
    ("<code>#include</code>", "<code>import</code>"), ("<code>NULL</code>", "<code>None</code>"),
    ("<code>argv</code>", "<code>sys.argv</code>"), ("<code>return 0;</code> at the end of main", "nothing"),
], prose=True)

qz = quiz([
    ("<code>rows = [(\"Ravi\", \"Vizag\"), (\"Divya\", \"Vijayawada\")]</code>. What is <code>rows[1][0]</code>?",
     ["<code>\"Ravi\"</code>", "<code>\"Vizag\"</code>", "<code>\"Divya\"</code>", "<code>(\"Divya\", \"Vijayawada\")</code>"], 3,
     "rows[1] is the second tuple; [0] is its first item. Indexes start at 0, as in C."),
    ("<code>d = {\"name\": \"Ravi\"}</code>. Which line crashes?",
     ["<code>d[\"name\"]</code>", "<code>d.get(\"city\")</code>", "<code>d[\"city\"]</code>", "<code>d.get(\"name\")</code>"], 3,
     "d[\"city\"] raises KeyError because there is no such key. d.get(\"city\") returns None instead."),
    ("What does <code>@route(\"/hai\")</code> above a function do?",
     ["Calls the function once, now", "Registers the function at the address /hai", "Makes the function return JSON", "Starts the server"], 2,
     "A decorator here means one thing: register this function at that path. It runs later, when a request for /hai arrives."),
    ("What does <code>print(int(\"4\") + 1)</code> print?",
     ["<code>41</code>", "<code>5</code>", "an error", "<code>4 + 1</code>"], 2,
     "int() turns the text \"4\" into the number 4. Without int(), \"4\" + 1 would be an error: you cannot add a string and a number."),
])

body = "\n".join([
    section("concept", "Concept", concept + table_html),
    section("video", "Demo video", video(0, "Running 01_hello.py before and after filling in the TODO, then the same for 02, 04 and 07, then check.py going from eight FAILs to eight PASSes.")),
    section("task", "Task", task),
    section("expected", "Expected output", expected),
    section("check", "Check yourself", check),
    section("takeaway", "Takeaway", callout("Python is C with the ceremony removed. A list of tuples comes out of the database; a list of dicts goes to the browser; a for-loop with an if inside connects them.")),
    section("stuck", "Stuck?", stuck),
    section("quiz", "Quiz", qz),
])

write("stage0.html", page("Just enough Python", "stage0.html", body,
                          sub="You know C. Here is Python as a set of differences from C — only the parts the next eight stages use.",
                          artifact="python3 01_hello.py",
                          stage_label="Stage 0 · Session 1 · morning · about 2 hours"))
