from lib import *

concept = p("""The sqlite3 shell in Stage 1 typed SQL and printed rows. A program can do the same: send SQL, get rows
back, and then do whatever it wants with them. Three objects make that happen, and each has a C
counterpart you already know.""") + \
p("""The <code>sqlite3</code> <strong>module</strong> is the driver — <code>import sqlite3</code> is your
<code>#include &lt;stdio.h&gt;</code>. The <strong>connection</strong> is the open file, your
<code>FILE *</code>: <code>sqlite3.connect("team_details.db")</code> opens it,
<code>connection.close()</code> closes it. The <strong>cursor</strong> is where you run a query and read
what comes back — think of it as the position in the file.""") + \
p("""Two calls, and the difference between them matters. <code>cursor.execute(sql)</code>
<em>positions</em>: it runs the query but hands you nothing. <code>cursor.fetchall()</code>
<em>reads</em>: it gives you every row as a list of tuples — the exact shape from Stage 0, block 2. One
tuple per row, one item per column, in the order you named the columns.""") + \
p("""One rule, starting today and for the rest of your life: never paste a value into the SQL string.
Write <code>?</code> where the value goes and pass the value separately, in a list. The same query then
serves any college, and text with a quote in it cannot break or hijack your SQL. Step through
<code>read_all.py</code> to watch the three objects appear.""")

left = code("read_all.py — the part that matters", '''connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("SELECT student_name, inter_college, inter_city FROM students")
rows = cursor.fetchall()
for row in rows:
    name, college, city = row
    print(f"{name} - {college} - {city}")
connection.close()''', pre_id="s2code")

right = panel("state", slots([
    ("s2conn", "connection", "", ""),
    ("s2cur", "cursor", "", ""),
    ("s2rows", "rows", "", ""),
    ("s2row", "name, college, city", "", ""),
])) + panel("terminal — output so far",
            '<pre class="term" id="s2out">'
            '<span class="ln" id="s2o1" hidden>Ravi Teja Kanchi - Sri Chaitanya Junior College - Visakhapatnam</span>'
            '<span class="ln" id="s2o2" hidden>Lakshmi Prasanna Gudla - Narayana Junior College - Vijayawada</span>'
            '<span class="ln" id="s2o3" hidden>Sai Kiran Bommu - Sri Chaitanya Junior College - Visakhapatnam</span>'
            '<span class="ln" id="s2o4" hidden>Divya Sree Pothula - Narayana Junior College - Vijayawada</span>'
            '<span class="ln dim" id="s2o0"> </span></pre>')

hide_all = {"s2o1": False, "s2o2": False, "s2o3": False, "s2o4": False}
stp = stepper(left, right, [
    {"note": "connect() opens the file. Like fopen: if the file is not there, SQLite creates an empty one — which is why a wrong path gives 'no such table' later, not 'no such file' now.",
     "hl": {"s2code": 0}, "slots": {"s2conn": {"v": "open: team_details.db", "cls": "live"}}, "show": hide_all},
    {"note": "A cursor from the connection. Queries run through it; results come back through it.",
     "hl": {"s2code": 1}, "slots": {"s2conn": {"v": "open: team_details.db", "cls": ""}, "s2cur": {"v": "ready", "cls": "live"}}},
    {"note": "execute() runs the SELECT. Notice: nothing is assigned. The cursor is now positioned at the result, but you have not read anything.",
     "hl": {"s2code": 2}, "slots": {"s2cur": {"v": "positioned at 4 rows", "cls": "live"}, "s2rows": {"v": "", "cls": ""}}},
    {"note": "fetchall() reads. rows is a list of 4 tuples, each with 3 strings, in the column order of the SELECT.",
     "hl": {"s2code": 3}, "slots": {"s2cur": {"v": "positioned at 4 rows", "cls": ""}, "s2rows": {"v": "[('Ravi Teja Kanchi', 'Sri Chaitanya Junior College', 'Visakhapatnam'), ('Lakshmi Prasanna Gudla', …), ('Sai Kiran Bommu', …), ('Divya Sree Pothula', …)]", "cls": "live"}}},
    {"note": "First time through the loop: row is the first tuple. Unpacking gives the three names.",
     "hl": {"s2code": 5}, "slots": {"s2rows": {"v": "4 tuples", "cls": ""}, "s2row": {"v": "'Ravi Teja Kanchi', 'Sri Chaitanya Junior College', 'Visakhapatnam'", "cls": "live"}}},
    {"note": "print writes one line. Then back to the top of the for.",
     "hl": {"s2code": 6}, "show": {"s2o1": True}},
    {"note": "Second tuple, second line.",
     "hl": {"s2code": 6}, "slots": {"s2row": {"v": "'Lakshmi Prasanna Gudla', 'Narayana Junior College', 'Vijayawada'", "cls": "live"}}, "show": {"s2o2": True}},
    {"note": "Third and fourth. The loop ends when the list is exhausted; no index, no length check.",
     "hl": {"s2code": 6}, "slots": {"s2row": {"v": "'Divya Sree Pothula', 'Narayana Junior College', 'Vijayawada'", "cls": "live"}}, "show": {"s2o3": True, "s2o4": True}},
    {"note": "close() releases the file. Like fclose. Do it once, at the end.",
     "hl": {"s2code": 7}, "slots": {"s2conn": {"v": "closed", "cls": "dead"}, "s2cur": {"v": "gone", "cls": "dead"}, "s2row": {"v": "", "cls": ""}}},
])

task = steps([
    p("<strong>Terminal 1.</strong> Run the given program. It reads every row of the database you built in Stage 1.") +
    term("terminal 1", """$ cd ~/kiet-bootcamp-3/code/stage2
$ python3 read_all.py
Ravi Teja Kanchi - Sri Chaitanya Junior College - Visakhapatnam
Lakshmi Prasanna Gudla - Narayana Junior College - Vijayawada
Sai Kiran Bommu - Sri Chaitanya Junior College - Visakhapatnam
Divya Sree Pothula - Narayana Junior College - Vijayawada""") +
    p("Open <code>read_all.py</code> and read it against the stepper above. It is the whole file:") +
    code_file("code/stage2/read_all.py", "code/stage2/read_all.py"),
    p("Open <code>by_college.py</code>. The connection lines are there. The college name comes in from the command line as <code>sys.argv[1]</code>. Your job is the <code>TODO</code> block: run a query with a <code>?</code>, read the rows, print each name.") +
    code_file("code/stage2/by_college.py", "code/stage2/by_college.py"),
    p("Run it with a college from <em>your</em> database. The example team has two Narayana students.") +
    term("terminal 1", """$ python3 by_college.py "Narayana Junior College"
Lakshmi Prasanna Gudla
Divya Sree Pothula"""),
    p("Now a college that is not in your database. It prints nothing — that is correct. Zero rows came back, the loop ran zero times, no error.") +
    term("terminal 1", """$ python3 by_college.py "Vignan Junior College"
$ """),
])

expected = p("The query you need has one <code>?</code> and one value in the list after it:") + \
    code("the shape", '''cursor.execute("SELECT student_name FROM students WHERE inter_college = ?", [college])
rows = cursor.fetchall()
for row in rows:
    print(row[0])''') + \
    p("Each row is a tuple with one item, so <code>row[0]</code> is the name. The quotes around the college name on the command line matter: without them the shell splits it into three arguments and <code>sys.argv[1]</code> is just <code>Narayana</code>.")

check = term("terminal 1", """$ python3 check.py
PASS: read_all.py prints all 4 sample rows as 'name - college - city'
PASS: by_college.py "Narayana Junior College" prints the 2 Narayana names
PASS: by_college.py "Sri Chaitanya Junior College" prints the 2 Sri Chaitanya names
PASS: by_college.py "Vignan Junior College" prints nothing (no such college in the DB)
PASS: by_college.py with no argument prints the usage line

5 passed, 0 failed""") + p("The check does not use your team database. It loads the four-row sample team into a temporary file and runs your program against that, so the names it expects are the sample names.")

stuck = p('Solution: <code>~/kiet-bootcamp-3/code/stage2/solution/by_college.py</code>.') + \
    p('Reference: <a href="reference/python-cheatsheet.html">Python cheatsheet</a> (lists, tuples, sys.argv) · <a href="reference/sql-for-students-table.html">SQL for the students table</a> (the ? section) · <a href="troubleshooting.html">Troubleshooting</a> (no such table means the wrong .db path).')

qz = quiz([
    ("After <code>cursor.execute(\"SELECT * FROM students\")</code>, where are the rows?",
     ["In the variable the call returned", "Not read yet; fetchall() reads them", "Printed on the screen", "In connection"], 2,
     "execute positions, fetch reads. The call returns nothing you need; the rows come from cursor.fetchall()."),
    ("<code>rows = cursor.fetchall()</code> gave <code>[('Ravi Teja Kanchi',), ('Sai Kiran Bommu',)]</code>. What is <code>rows[1][0]</code>?",
     ["<code>('Ravi Teja Kanchi',)</code>", "<code>'Ravi Teja Kanchi'</code>", "<code>'Sai Kiran Bommu'</code>", "<code>2</code>"], 3,
     "rows[1] is the second tuple; [0] is its only item. A one-column SELECT still gives tuples, just with one item each."),
    ("Why <code>WHERE inter_college = ?</code> with <code>[college]</code>, instead of building the string with the name inside?",
     ["It runs faster", "The ? is required by Python", "The value stays data, whatever characters it contains", "Strings cannot be joined in Python"], 3,
     "With ?, a name containing a quote is just a name. Pasted into the string it would end the SQL early — the classic injection bug."),
    ("<code>python3 by_college.py Narayana Junior College</code> (no quotes) prints nothing. Why?",
     ["The college is not in the database", "sys.argv[1] is only 'Narayana'", "The ? was not filled", "Python needs -c"], 2,
     "The shell split the name into three arguments. The query looked for a college called exactly 'Narayana' and found none."),
])

body = "\n".join([
    section("concept", "Concept", concept + stp),
    section("task", "Task", task),
    section("expected", "Expected output", expected),
    section("check", "Check yourself", check),
    section("takeaway", "Takeaway", callout("execute positions, fetch reads. Values go in through ?, never into the string.")),
    section("stuck", "Stuck?", stuck),
    section("quiz", "Quiz", qz),
])

write("stage2.html", page("Python talks to the database", "stage2.html", body,
                          sub="Module, connection, cursor. execute positions, fetchall reads, and the value goes in through a question mark.",
                          artifact='cursor.execute("SELECT student_name FROM students WHERE inter_college = ?", [college])',
                          stage_label="Stage 2 · Session 1 · morning"))
