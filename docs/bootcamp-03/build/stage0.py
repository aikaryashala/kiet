import os
from lib import *

# ---------------------------------------------------------------- helpers for the seven steppers
def outpanel(pid, lines, caption="terminal — output so far"):
    """A dark terminal whose lines start hidden; ids pid + 'o' + index. '$ ' lines are commands."""
    spans = []
    for i, line in enumerate(lines):
        if line.startswith("$ "):
            spans.append(f'<span class="ln cmd" id="{pid}o{i}" hidden><span class="p">$ </span>{esc(line[2:])}</span>')
        else:
            spans.append(f'<span class="ln" id="{pid}o{i}" hidden>{esc(line)}</span>')
    spans.append('<span class="ln dim"> </span>')
    return panel(caption, f'<pre class="term">{"".join(spans)}</pre>')


def shown(pid, n, total):
    return {f"{pid}o{i}": i < n for i in range(total)}


def S(note, hl=None, slots=None, show=None, table=None):
    d = {"note": note}
    if hl is not None: d["hl"] = hl
    if slots: d["slots"] = slots
    if show: d["show"] = show
    if table: d["table"] = table
    return d


def v(val, cls="live"):
    return {"v": val, "cls": cls}


def body_of(relpath):
    text = open(os.path.join(REPO, relpath), encoding="utf-8").read().split("\n")
    while text and text[0].startswith("#"):
        text.pop(0)
    while text and text[0].strip() == "":
        text.pop(0)
    return "\n".join(text).rstrip("\n")


# ---------------------------------------------------------------- Block 1
c1 = code("01_hello.py", body_of("code/stage0/01_hello.py"), pre_id="b1c", lang="py")
o1 = ["My name is Ravi Teja Kanchi", "I studied at Sri Chaitanya Junior College, Visakhapatnam"]
r1 = panel("variables", slots([("b1n", "name", "", ""), ("b1g", "college", "", ""), ("b1t", "city", "", "")])) + outpanel("b1", o1)
st1 = stepper(c1, r1, [
    S("python3 01_hello.py starts at the first line. No compile, no main. A name on the left, a value on the right: that is a variable, and it has no declared type.",
      {"b1c": 0}, {"b1n": v('"Ravi Teja Kanchi"')}, shown("b1", 0, 2)),
    S("Two more strings. Quotes make text; the variable takes whatever is on the right.",
      {"b1c": 1}, {"b1n": v('"Ravi Teja Kanchi"', ""), "b1g": v('"Sri Chaitanya Junior College"')}),
    S("The block ends when the indentation ends — here there is no block at all, just lines run in order.",
      {"b1c": 2}, {"b1g": v('"Sri Chaitanya Junior College"', ""), "b1t": v('"Visakhapatnam"')}),
    S("print writes one line. The f before the quote makes an f-string: {name} inside it is replaced by the variable's value. This replaces every printf format you know.",
      {"b1c": 4}, {"b1t": v('"Visakhapatnam"', "")}, shown("b1", 1, 2)),
    S("Two variables in one f-string. The program ends after the last line; there is no return 0.",
      {"b1c": 5}, None, shown("b1", 2, 2)),
])

# ---------------------------------------------------------------- Block 2
c2 = code("02_rows.py", body_of("code/stage0/02_rows.py"), pre_id="b2c", lang="py")
o2 = ["Ravi Teja Kanchi - Visakhapatnam", "Lakshmi Prasanna Gudla - Vijayawada", "Sai Kiran Bommu - Visakhapatnam", "Divya Sree Pothula - Vijayawada", "4 rows"]
t2 = panel("rows", '<table id="b2t"><thead><tr><th>[0]</th><th>[1]</th><th>[2]</th></tr></thead><tbody>'
           '<tr><td>Ravi Teja Kanchi</td><td>Sri Chaitanya Junior College</td><td>Visakhapatnam</td></tr>'
           '<tr><td>Lakshmi Prasanna Gudla</td><td>Narayana Junior College</td><td>Vijayawada</td></tr>'
           '<tr><td>Sai Kiran Bommu</td><td>Sri Chaitanya Junior College</td><td>Visakhapatnam</td></tr>'
           '<tr id="b2r4" hidden><td>Divya Sree Pothula</td><td>Narayana Junior College</td><td>Vijayawada</td></tr></tbody></table>')
r2 = t2 + panel("variables", slots([("b2row", "row", "", ""), ("b2u", "name, college, city", "", ""), ("b2len", "len(rows)", "", "")])) + outpanel("b2", o2)
sh2 = lambda n: dict(shown("b2", n, 5), b2r4=True)
st2 = stepper(c2, r2, [
    S("A list: square brackets, items separated by commas. Each item is a tuple: round brackets, three strings. This is the shape SQLite will hand you in Stage 2.",
      {"b2c": 0}, {"b2len": v("3", "")}, dict(shown("b2", 0, 5), b2r4=False)),
    S(".append adds one item at the end. The list grows; nothing else to declare.",
      {"b2c": 6}, {"b2len": v("4")}, sh2(0)),
    S("for row in rows: no index, no length. row is the first tuple, whole.",
      {"b2c": 8}, {"b2len": v("4", ""), "b2row": v("('Ravi Teja Kanchi', 'Sri Chaitanya Junior College', 'Visakhapatnam')")}, None, {"b2t": {"cur": [0]}}),
    S("Unpacking: three names on the left, a three-item tuple on the right. Each name takes one item.",
      {"b2c": 9}, {"b2row": v("(…)", ""), "b2u": v("'Ravi Teja Kanchi', 'Sri Chaitanya Junior College', 'Visakhapatnam'")}, None, {"b2t": {"cur": [0]}}),
    S("print uses two of the three. college was unpacked but not used — that is fine.",
      {"b2c": 10}, {"b2u": v("'Ravi Teja Kanchi', …", "")}, sh2(1), {"b2t": {"cur": [0]}}),
    S("Back to the for line. row is now the second tuple.",
      {"b2c": 9}, {"b2row": v("('Lakshmi Prasanna Gudla', …)"), "b2u": v("'Lakshmi Prasanna Gudla', 'Narayana Junior College', 'Vijayawada'")}, None, {"b2t": {"cur": [1]}}),
    S("Second line printed.", {"b2c": 10}, {"b2row": v("(…)", ""), "b2u": v("…", "")}, sh2(2), {"b2t": {"cur": [1]}}),
    S("Third.", {"b2c": 10}, {"b2u": v("'Sai Kiran Bommu', 'Sri Chaitanya Junior College', 'Visakhapatnam'")}, sh2(3), {"b2t": {"cur": [2]}}),
    S("Fourth — the one that was appended. The loop then ends by itself: no more items.",
      {"b2c": 10}, {"b2u": v("'Divya Sree Pothula', 'Narayana Junior College', 'Vijayawada'")}, sh2(4), {"b2t": {"cur": [3]}}),
    S("len gives the number of items. No sizeof, no counter variable.",
      {"b2c": 12}, {"b2u": v("", ""), "b2len": v("4")}, sh2(5)),
])

# ---------------------------------------------------------------- Block 3
c3 = code("03_dicts.py", body_of("code/stage0/03_dicts.py"), pre_id="b3c", lang="py")
o3 = ["Ravi Teja Kanchi", "None",
      '[{"student_name": "Ravi Teja Kanchi", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}, {"student_name": "Lakshmi Prasanna Gudla", …}, {"student_name": "Sai Kiran Bommu", …}]']
r3 = panel("variables", slots([("b3res", "result", "", ""), ("b3row", "name, college, city", "", ""), ("b3first", "first", "", "")])) + outpanel("b3", o3)
st3 = stepper(c3, r3, [
    S("import json brings in the standard-library module that turns dicts into JSON text.", {"b3c": 0}, None, shown("b3", 0, 3)),
    S("The same three tuples as Block 2.", {"b3c": 2}),
    S("An empty list. It will hold dicts.", {"b3c": 8}, {"b3res": v("[]")}),
    S("Loop and unpack, exactly as before.", {"b3c": 10}, {"b3res": v("[]", ""), "b3row": v("'Ravi Teja Kanchi', 'Sri Chaitanya Junior College', 'Visakhapatnam'")}),
    S("A dict: curly braces, \"key\": value pairs. A struct whose field names are strings. Appended to the list.",
      {"b3c": 11}, {"b3row": v("…", ""), "b3res": v("[{'student_name': 'Ravi Teja Kanchi', 'inter_college': 'Sri Chaitanya Junior College', 'inter_city': 'Visakhapatnam'}]")}),
    S("Two more times round the loop. Three dicts in the list.",
      {"b3c": 11}, {"b3res": v("[{…Ravi…}, {…Lakshmi…}, {…Sai Kiran…}]")}),
    S("result[0] is the first dict.", {"b3c": 13}, {"b3res": v("3 dicts", ""), "b3first": v("{'student_name': 'Ravi Teja Kanchi', 'inter_college': …, 'inter_city': …}")}),
    S("Square brackets with a key read one field.", {"b3c": 14}, {"b3first": v("{…}", "")}, shown("b3", 1, 3)),
    S(".get with a key that is not there gives None — Python's NULL — instead of crashing. first[\"phone\"] would have crashed.",
      {"b3c": 15}, None, shown("b3", 2, 3)),
    S("json.dumps turns the whole list into JSON text: double quotes, one line. In Stage 4, Bottle does this for you when a route returns a dict.",
      {"b3c": 17}, None, shown("b3", 3, 3)),
])

# ---------------------------------------------------------------- Block 4
c4 = code("04_prime_even.py", body_of("code/stage0/04_prime_even.py"), pre_id="b4c", lang="py")
o4 = ["18", "2 prime=True even=True", "4 prime=False even=True", "17 prime=True even=False", "18 prime=False even=True", "1 prime=False even=False"]
r4 = panel("variables", slots([("b4n", "n", "", ""), ("b4d", "d", "", ""), ("b4m", "n % d", "", ""), ("b4p", "is_prime(n)", "", ""), ("b4e", "is_even(n)", "", "")])) + outpanel("b4", o4)
st4 = stepper(c4, r4, [
    S("def defines a function; nothing runs yet. No return type, no parameter types, no prototype.", {"b4c": 0}, None, shown("b4", 0, 6)),
    S("A second function. Python reads both definitions and moves on.", {"b4c": 9}),
    S("int(\"17\") turns the text into the number 17 — atoi. Plus 1, printed.", {"b4c": 13}, None, shown("b4", 1, 6)),
    S("for n in a list of numbers. First n = 2.", {"b4c": 15}, {"b4n": v("2")}),
    S("is_prime(2): 2 is not less than 2. range(2, 2) is empty, so the loop body never runs. Straight to return True.",
      {"b4c": 6}, {"b4n": v("2", ""), "b4d": v("(range empty)", "dead"), "b4p": v("True")}),
    S("is_even(2): 2 % 2 is 0, so the comparison is True. Both results go into the f-string.",
      {"b4c": 10}, {"b4d": v("", ""), "b4p": v("True", ""), "b4e": v("True")}, shown("b4", 2, 6)),
    S("n = 4. is_prime(4): range(2, 4) is 2, 3. First d = 2.", {"b4c": 3}, {"b4n": v("4"), "b4d": v("2"), "b4p": v("", ""), "b4e": v("", "")}),
    S("4 % 2 is 0: a divisor. return False leaves the function at once; d never reaches 3.",
      {"b4c": 5}, {"b4n": v("4", ""), "b4d": v("2", ""), "b4m": v("0"), "b4p": v("False")}),
    S("is_even(4) is True. Second line printed.", {"b4c": 16}, {"b4m": v("", ""), "b4p": v("False", ""), "b4e": v("True")}, shown("b4", 3, 6)),
    S("n = 17. d goes 2, 3, 4 … 16 and 17 % d is never 0. The for ends, and the line after it runs: return True.",
      {"b4c": 6}, {"b4n": v("17"), "b4d": v("2 … 16", ""), "b4m": v("never 0", ""), "b4p": v("True"), "b4e": v("False")}, shown("b4", 4, 6)),
    S("n = 18: 18 % 2 is 0 at the first d. False, and even.",
      {"b4c": 5}, {"b4n": v("18"), "b4d": v("2"), "b4m": v("0"), "b4p": v("False"), "b4e": v("True")}, shown("b4", 5, 6)),
    S("n = 1: the first if catches it. return False before any loop. Not even either. The list is exhausted; the program ends.",
      {"b4c": 2}, {"b4n": v("1"), "b4d": v("", ""), "b4m": v("", ""), "b4p": v("False"), "b4e": v("False")}, shown("b4", 6, 6)),
])

# ---------------------------------------------------------------- Block 5
c5 = code("05_greet.py", body_of("code/stage0/05_greet.py"), pre_id="b5c", lang="py")
o5 = ["$ python3 05_greet.py Ravi", "Namasthey Ravi", "$ python3 05_greet.py", "usage: python3 05_greet.py <name>"]
r5 = panel("variables", slots([("b5a", "sys.argv", "", ""), ("b5l", "len(sys.argv)", "", "")])) + outpanel("b5", o5, "terminal")
st5 = stepper(c5, r5, [
    S("The command line: the file name and one word after it.", None, None, shown("b5", 1, 4)),
    S("import sys: the standard-library module that holds argv. sys.argv is a list of strings, [0] is the file name — C's argv.",
      {"b5c": 0}, {"b5a": v("['05_greet.py', 'Ravi']"), "b5l": v("2")}),
    S("2 is not less than 2. The if is false.", {"b5c": 2}, {"b5a": v("['05_greet.py', 'Ravi']", ""), "b5l": v("2", "")}),
    S("So the else branch: sys.argv[1] is the word after the file name.", {"b5c": 5}, None, shown("b5", 2, 4)),
    S("Run again with nothing after the file name.", None, {"b5a": v("['05_greet.py']"), "b5l": v("1")}, shown("b5", 3, 4)),
    S("1 is less than 2: the if is true.", {"b5c": 2}, {"b5a": v("['05_greet.py']", ""), "b5l": v("1", "")}),
    S("The usage line. sys.argv[1] would have crashed with IndexError — the if is the guard.", {"b5c": 3}, None, shown("b5", 4, 4)),
])

# ---------------------------------------------------------------- Block 6
c6 = code("06_read_only.py", '''from bottle import route, run, request

@route("/hai")
def hai():
    return "Namasthey!!!"

@route("/greet")
def greet():
    name = request.query.get("name")
    if name is None:
        return "name is required"
    return f"Namasthey {name}"

run(host="localhost", port=8080)''', pre_id="b6c", lang="py")
r6 = panel("bottle's address book", slots([("b6r1", "/hai", "", ""), ("b6r2", "/greet", "", "")])) + \
     panel("one request", slots([("b6req", "request", "", ""), ("b6name", "name", "", ""), ("b6ans", "answer", "", "")]))
st6 = stepper(c6, r6, [
    S("from bottle import …: three names from the file bottle.py sitting next to this one. Not the standard library — a file beside yours.", {"b6c": 0}),
    S("The line starting with @ is a decorator. Here it means exactly one thing: write this function's name next to /hai in Bottle's address book. The function does not run.",
      {"b6c": 2}, {"b6r1": v("hai()")}),
    S("Same for /greet. Two entries in the book. Still nothing has run.", {"b6c": 6}, {"b6r1": v("hai()", ""), "b6r2": v("greet()")}),
    S("run() starts the waiting loop. From here the program only does something when a request arrives.", {"b6c": 13}, {"b6r2": v("greet()", "")}),
    S("A request for /greet?name=Ravi arrives. Bottle looks up /greet in the book and calls greet().", {"b6c": 7}, {"b6req": v("GET /greet?name=Ravi")}),
    S(".get finds name in the query string.", {"b6c": 8}, {"b6req": v("GET /greet?name=Ravi", ""), "b6name": v("'Ravi'")}),
    S("Not None, so the guard is skipped.", {"b6c": 9}, {"b6name": v("'Ravi'", "")}),
    S("The f-string is the answer. Bottle sends it back.", {"b6c": 11}, {"b6ans": v("Namasthey Ravi")}),
    S("Another request, this time with no name in it. greet() again.", {"b6c": 7}, {"b6req": v("GET /greet"), "b6name": v("", ""), "b6ans": v("", "")}),
    S(".get finds nothing. That is None — Python's NULL.", {"b6c": 8}, {"b6req": v("GET /greet", ""), "b6name": v("None", "warn")}),
    S("is None is true. Without this line, the f-string below would build 'Namasthey None' — or worse, crash on a method call.", {"b6c": 9}, {"b6name": v("None", "warn")}),
    S("The guard's answer goes back instead. Then Bottle waits again.", {"b6c": 10}, {"b6ans": v("name is required", "warn")}),
])

# ---------------------------------------------------------------- Block 7
c7 = code("07_filter_pack.py", body_of("code/stage0/07_filter_pack.py"), pre_id="b7c", lang="py")
o7 = ['{"count": 2, "students": [{"student_name": "Ravi Teja Kanchi", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}, {"student_name": "Sai Kiran Bommu", …}]}']
t7 = table("rows", ["student_name", "inter_college", "inter_city"], [
    ("Ravi Teja Kanchi", "Sri Chaitanya Junior College", "Visakhapatnam"),
    ("Lakshmi Prasanna Gudla", "Narayana Junior College", "Vijayawada"),
    ("Sai Kiran Bommu", "Sri Chaitanya Junior College", "Visakhapatnam"),
    ("Divya Sree Pothula", "Narayana Junior College", "Vijayawada")], table_id="b7t")
r7 = t7 + panel("variables", slots([("b7w", "wanted_city", "", ""), ("b7s", "students", "", ""), ("b7a", "answer", "", "")])) + outpanel("b7", o7)
st7 = stepper(c7, r7, [
    S("Four tuples. This is the whole database, in a list, for now.", {"b7c": 2}, None, shown("b7", 0, 1)),
    S("The value we filter on. In Stage 5 it will come from the URL instead of being typed here.", {"b7c": 9}, {"b7w": v('"Visakhapatnam"')}),
    S("An empty list for the matches.", {"b7c": 11}, {"b7w": v('"Visakhapatnam"', ""), "b7s": v("[]")}),
    S("Row 0: unpack, then the if. Visakhapatnam equals wanted_city.", {"b7c": 14}, {"b7s": v("[]", "")}, None, {"b7t": {"cur": [0]}}),
    S("True, so a dict for this row is appended. The for-loop with the if inside: that is SELECT … WHERE, written by hand.",
      {"b7c": 15}, {"b7s": v("[{…Ravi Teja Kanchi…}]")}, None, {"b7t": {"cur": [0]}}),
    S("Row 1: Vijayawada. The if is false; nothing appended; the row is skipped.", {"b7c": 14}, {"b7s": v("1 dict", "")}, None, {"b7t": {"cur": [1]}}),
    S("Row 2 matches.", {"b7c": 15}, {"b7s": v("[{…Ravi…}, {…Sai Kiran…}]")}, None, {"b7t": {"cur": [2], "skip": [1]}}),
    S("Row 3 is skipped. The loop ends.", {"b7c": 14}, {"b7s": v("2 dicts", "")}, None, {"b7t": {"cur": [3], "skip": [1]}}),
    S("The answer is one dict around the list: a count and the students. Exactly the shape Stage 5 returns.",
      {"b7c": 17}, {"b7a": v("{'count': 2, 'students': [{…}, {…}]}")}, None, {"b7t": {"skip": [1, 3]}}),
    S("json.dumps prints it as JSON. Take away the print and put a @route above it, and you have a backend route.",
      {"b7c": 18}, {"b7a": v("{…}", "")}, shown("b7", 1, 1), {"b7t": {"skip": [1, 3]}}),
])

# ---------------------------------------------------------------- page
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
p("""Nothing to write in this stage. Seven short programs follow, each complete. For each one, step through
it with the Forward button or the arrow keys and watch the variables and the output appear on the right;
then run the file yourself and see the same output. Everything <em>not</em> here — classes, try/except,
list comprehensions, <code>with</code>, virtual environments — is deliberately left for later.""")

table_html = table("C to Python", ["C", "Python"], [
    ("<code>int x = 5;</code>", "<code>x = 5</code>"), ("<code>{ ... }</code>", "indentation"),
    ("<code>int arr[3]</code>", "<code>arr = [1, 2, 3]</code>"), ("<code>struct</code>", "dict"),
    ("<code>printf(\"%s\", s)</code>", "<code>print(f\"{s}\")</code>"),
    ("<code>for (i=0; i&lt;n; i++)</code>", "<code>for i in range(n):</code>"), ("for each element", "<code>for x in items:</code>"),
    ("<code>strcmp(a, b) == 0</code>", "<code>a == b</code>"), ("<code>atoi(s)</code>", "<code>int(s)</code>"),
    ("<code>#include</code>", "<code>import</code>"), ("<code>NULL</code>", "<code>None</code>"),
    ("<code>argv</code>", "<code>sys.argv</code>"), ("<code>return 0;</code> at the end of main", "nothing"),
], prose=True)


def block(n, title, teach, stp, run_cmd, feeds):
    return f"<h3>Block {n} — {title}</h3>" + p(teach) + stp + term("terminal", run_cmd) + p(f"<em>Feeds:</em> {feeds}")


task = p("Open a terminal in the Stage 0 folder. For each block: step through the visualization, then run the file and compare.") + \
    term("terminal", "$ cd ~/kiet-bootcamp-3/code/stage0\n$ ls\n01_hello.py  02_rows.py  03_dicts.py  04_prime_even.py  05_greet.py  06_read_only.py  07_filter_pack.py  check.py") + \
    block(1, "Running a program", "No compile, no main, no semicolons. <code>print</code> writes a line. An f-string puts variables inside text.",
          st1, "$ python3 01_hello.py\nMy name is Ravi Teja Kanchi\nI studied at Sri Chaitanya Junior College, Visakhapatnam", "Stage 4, <code>/wish/&lt;name&gt;</code>") + \
    block(2, "Lists and tuples", "A list of tuples is exactly what SQLite gives back in Stage 2. <code>.append</code> adds to the end, <code>len</code> counts, <code>for row in rows</code> visits each one, <code>name, college, city = row</code> takes a tuple apart.",
          st2, "$ python3 02_rows.py\nRavi Teja Kanchi - Visakhapatnam\nLakshmi Prasanna Gudla - Vijayawada\nSai Kiran Bommu - Visakhapatnam\nDivya Sree Pothula - Vijayawada\n4 rows", "Stage 2") + \
    block(3, "Dicts", "A dict is a struct with string field names, and it is JSON near enough: <code>json.dumps</code> turns it into JSON text. <code>d[\"k\"]</code> reads a field; <code>d.get(\"k\")</code> gives <code>None</code> instead of crashing when the field is not there.",
          st3, '$ python3 03_dicts.py\nRavi Teja Kanchi\nNone\n[{"student_name": "Ravi Teja Kanchi", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}, {"student_name": "Lakshmi Prasanna Gudla", "inter_college": "Narayana Junior College", "inter_city": "Vijayawada"}, {"student_name": "Sai Kiran Bommu", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}]', "Stage 5, packing rows for the browser") + \
    block(4, "Functions, if, %, range, int()", "<code>def</code> starts a function; no prototype, no return type. <code>%</code> is remainder. <code>range(2, n)</code> is the C counting loop. <code>int(\"17\")</code> is <code>atoi</code>.",
          st4, "$ python3 04_prime_even.py\n18\n2 prime=True even=True\n4 prime=False even=True\n17 prime=True even=False\n18 prime=False even=True\n1 prime=False even=False", "Stage 3, the <code>/isprime</code> route") + \
    block(5, "Imports and argv", "<code>import</code> brings in a module: from the standard library, or a file sitting next to yours. <code>sys.argv</code> is C's <code>argv</code>, a list of strings.",
          st5, "$ python3 05_greet.py Ravi\nNamasthey Ravi\n$ python3 05_greet.py\nusage: python3 05_greet.py <name>", "Stage 2, <code>by_college.py</code>") + \
    "<h3>Block 6 — Two strange things</h3>" + p("Read only. Do not run it: <code>bottle.py</code> is not in this folder, on purpose. Step through what Bottle does with the two <code>@route</code> lines, and what <code>None</code> does in <code>greet</code>.") + st6 + \
    p("The file has four questions and their answers at the bottom. Read them after stepping through.") + p("<em>Feeds:</em> Stage 3, reading <code>demo_server.py</code>.") + \
    block(7, "Put it together", "Rows in, a filter with <code>if</code>, dicts out, JSON printed. This is Stage 5 with the SQL and the HTTP taken away.",
          st7, '$ python3 07_filter_pack.py\n{"count": 2, "students": [{"student_name": "Ravi Teja Kanchi", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}, {"student_name": "Sai Kiran Bommu", "inter_college": "Sri Chaitanya Junior College", "inter_city": "Visakhapatnam"}]}', "Stage 5, every route")

expected = p("Each file prints exactly what the terminal block under its stepper shows, and the same text is in the comment at the top of the file. If yours differs, the Python version is the first thing to check: <code>python3 --version</code> must say 3.12 or newer.")

check = term("terminal", """$ python3 check.py
PASS: 01_hello.py prints the expected output
PASS: 02_rows.py prints the expected output
PASS: 03_dicts.py prints the expected output
PASS: 04_prime_even.py prints the expected output
PASS: 05_greet.py Ravi prints the expected output
PASS: 05_greet.py prints the expected output
PASS: 06_read_only.py is present (read it; it is not run)
PASS: 07_filter_pack.py prints the expected output

8 passed, 0 failed""") + p("Nothing to fix here: this confirms that python3 on your machine runs the seven files the way the page shows them.")

stuck = p('Reference: <a href="reference/python-cheatsheet.html">Python cheatsheet</a> · <a href="reference/c-to-python.html">C to Python</a> · <a href="reference/json.html">JSON</a>. The files themselves are in <code>~/kiet-bootcamp-3/code/stage0/</code>; open them in an editor beside the page.')

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
    ("In <code>is_prime(4)</code>, why does <code>d</code> never reach 3?",
     ["range(2, 4) has only one number", "return False leaves the function as soon as 4 % 2 == 0", "3 is not in the list", "The for loop runs once by default"], 2,
     "return ends the function immediately, wherever it is. The loop does not finish; the function is already over."),
])

body = "\n".join([
    section("concept", "Concept", concept + table_html),
    section("task", "Task", task),
    section("expected", "Expected output", expected),
    section("check", "Check yourself", check),
    section("takeaway", "Takeaway", callout("Python is C with the ceremony removed. A list of tuples comes out of the database; a list of dicts goes to the browser; a for-loop with an if inside connects them.")),
    section("stuck", "Stuck?", stuck),
    section("quiz", "Quiz", qz),
])

write("stage0.html", page("Just enough Python", "stage0.html", body,
                          sub="You know C. Here is Python as a set of differences from C — seven complete programs, each one stepped through line by line.",
                          artifact="python3 01_hello.py",
                          stage_label="Stage 0 · about 2 hours"))
