from lib import *

concept = p("""Start from an array of structs — four students, each with a name, a college, a city. It works
until the program ends: then the data is gone. So you write it to a file. Now searching needs a loop that
reads the file. Add a field and you rewrite the file format and every loop. A second program wants the same
data and you copy the loops there too. None of this code is about students; all of it is about
storage.""") + \
p("""A <strong>table</strong> is that struct array, living in a file, that does its own searching.
A <strong>database</strong> is a file holding tables plus the search, add and update code, so no program
has to write those loops again. <strong>SQLite</strong> is a database that is one ordinary file on disk,
no server, no install: it is already inside Python, and inside your phone.""") + \
p("""You talk to it in <strong>SQL</strong>. Four verbs for now. <code>CREATE TABLE</code> defines the
struct. <code>INSERT</code> appends a row. <code>SELECT … WHERE</code> is the for-loop with the if inside
it. <code>UPDATE</code> and <code>DELETE</code> come later. Look at
<code>SELECT student_name FROM students WHERE inter_city = 'Vijayawada'</code> and then at the C loop
next to it below: same walk over the rows, same comparison, same output. The database runs the loop so
you do not have to write it. Step through it.""")

left = code("sql", "SELECT student_name FROM students WHERE inter_city = 'Vijayawada';", pre_id="s1sql") + \
    code("the same thing in C", '''for (int i = 0; i < 4; i++) {
    if (strcmp(rows[i].city, "Vijayawada") == 0) {
        printf("%s\\n", rows[i].name);
    }
}''', pre_id="s1c")

students_tbl = table("students", ["student_name", "inter_college", "inter_city"], [
    ("Ravi Teja Kanchi", "Sri Chaitanya Junior College", "Visakhapatnam"),
    ("Lakshmi Prasanna Gudla", "Narayana Junior College", "Vijayawada"),
    ("Sai Kiran Bommu", "Sri Chaitanya Junior College", "Visakhapatnam"),
    ("Divya Sree Pothula", "Narayana Junior College", "Vijayawada"),
], table_id="s1t")
result_tbl = panel("result", '<table id="s1r"><thead><tr><th>student_name</th></tr></thead><tbody>'
                   '<tr id="s1r1" hidden><td>Lakshmi Prasanna Gudla</td></tr>'
                   '<tr id="s1r2" hidden><td>Divya Sree Pothula</td></tr></tbody></table>')
right = students_tbl + result_tbl

stp = stepper(left, right, [
    {"note": "One statement. FROM names the table, WHERE gives the test, SELECT student_name says which column to keep. Nothing has run yet.",
     "hl": {"s1sql": 0, "s1c": 0}, "show": {"s1r1": False, "s1r2": False}},
    {"note": "Row 0. The database looks at inter_city — Visakhapatnam. The test is false. The C version is the strcmp on this row.",
     "hl": {"s1c": 1}, "table": {"s1t": {"cur": [0]}}},
    {"note": "Row 0 is skipped. It fades; it is still in the table, just not in this answer.",
     "hl": {"s1c": 0}, "table": {"s1t": {"skip": [0]}}},
    {"note": "Row 1. inter_city is Vijayawada. The test is true.",
     "hl": {"s1c": 1}, "table": {"s1t": {"cur": [1], "skip": [0]}}},
    {"note": "So student_name from row 1 goes into the result. That is the printf.",
     "hl": {"s1c": 2}, "table": {"s1t": {"cur": [1], "skip": [0]}}, "show": {"s1r1": True}},
    {"note": "Row 2. Visakhapatnam again. Skipped.",
     "hl": {"s1c": 1}, "table": {"s1t": {"cur": [2], "skip": [0]}}},
    {"note": "Row 3. Vijayawada. Kept — the second row of the result.",
     "hl": {"s1c": 2}, "table": {"s1t": {"cur": [3], "skip": [0, 2]}}, "show": {"s1r2": True}},
    {"note": "No more rows. The result has two names. You wrote one line; the database wrote the loop.",
     "hl": {"s1sql": 0}, "table": {"s1t": {"skip": [0, 2]}}, "show": {"s1r1": True, "s1r2": True}},
])

task = steps([
    p("<strong>Terminal 1.</strong> Go to the data folder and open a new database file. The prompt changes to <code>sqlite&gt;</code>: from here on you are typing SQL, and every statement ends with <code>;</code>.") +
    term("terminal 1", """$ cd ~/kiet-bootcamp-3/data
$ sqlite3 team_details.db
SQLite version 3.45.1 2024-01-30 16:01:20
Enter ".help" for usage hints.
sqlite> """) + p("No <code>sqlite3</code> command? Use <code>python3 -m sqlite3 team_details.db</code> instead. The SQL is the same; that shell has no dot-commands, so skip the <code>.mode</code> and <code>.headers</code> lines, and it prints each row as a Python tuple."),
    p("First, tell the shell how to draw results. A line starting with a dot is a shell setting, not SQL: no semicolon.") +
    term("terminal 1 — sqlite>", """sqlite> .mode box
sqlite> """),
    p("Paste the <code>CREATE TABLE</code> from <code>schema.sql</code>. This defines the struct: three text columns.") +
    term("terminal 1 — sqlite>", """sqlite> CREATE TABLE students (
   ...>     student_name TEXT,
   ...>     inter_college TEXT,
   ...>     inter_city TEXT
   ...> );
sqlite> """),
    p("<code>INSERT</code> one row per person on your team — real name, real intermediate college, real city. The example team has four. Text goes in single quotes.") +
    term("terminal 1 — sqlite>", """sqlite> INSERT INTO students VALUES ('Ravi Teja Kanchi', 'Sri Chaitanya Junior College', 'Visakhapatnam');
sqlite> INSERT INTO students VALUES ('Lakshmi Prasanna Gudla', 'Narayana Junior College', 'Vijayawada');
sqlite> INSERT INTO students VALUES ('Sai Kiran Bommu', 'Sri Chaitanya Junior College', 'Visakhapatnam');
sqlite> INSERT INTO students VALUES ('Divya Sree Pothula', 'Narayana Junior College', 'Vijayawada');
sqlite> """),
    p("Read everything back. <code>*</code> means every column. Box mode draws the table with its column names on top.") +
    term("terminal 1 — sqlite>", """sqlite> SELECT * FROM students;
┌────────────────────────┬──────────────────────────────┬───────────────┐
│      student_name      │        inter_college         │  inter_city   │
├────────────────────────┼──────────────────────────────┼───────────────┤
│ Ravi Teja Kanchi       │ Sri Chaitanya Junior College │ Visakhapatnam │
│ Lakshmi Prasanna Gudla │ Narayana Junior College      │ Vijayawada    │
│ Sai Kiran Bommu        │ Sri Chaitanya Junior College │ Visakhapatnam │
│ Divya Sree Pothula     │ Narayana Junior College      │ Vijayawada    │
└────────────────────────┴──────────────────────────────┴───────────────┘"""),
    p("Two more dot-commands give the plainer look you will see in other tools: names on top, no borders. Try them, then run the SELECT again.") +
    term("terminal 1 — sqlite>", """sqlite> .headers on
sqlite> .mode column
sqlite> SELECT * FROM students;
student_name            inter_college                 inter_city
----------------------  ----------------------------  -------------
Ravi Teja Kanchi        Sri Chaitanya Junior College  Visakhapatnam
Lakshmi Prasanna Gudla  Narayana Junior College       Vijayawada
Sai Kiran Bommu         Sri Chaitanya Junior College  Visakhapatnam
Divya Sree Pothula      Narayana Junior College       Vijayawada   """),
    p("The loop with the if inside. Use one of your own cities.") +
    term("terminal 1 — sqlite>", """sqlite> SELECT student_name FROM students WHERE inter_city = 'Vijayawada';
student_name
----------------------
Lakshmi Prasanna Gudla
Divya Sree Pothula    """),
    p("Leave, and look at the folder. There is a new file. That file <em>is</em> the database.") +
    term("terminal 1", """sqlite> .quit
$ ls -l
total 56
-rw-r--r-- 1 kiet kiet 21593 Sep 21 09:40 all_students.sql
-rw-r--r-- 1 kiet kiet   697 Sep 21 09:40 sample_team_details.sql
-rw-r--r-- 1 kiet kiet   238 Sep 21 09:40 schema.sql
-rw-r--r-- 1 kiet kiet  8192 Sep 21 10:02 team_details.db"""),
    p("Open it again. The rows are still there — they were never in the program, they were in the file.") +
    term("terminal 1", """$ sqlite3 team_details.db
SQLite version 3.45.1 2024-01-30 16:01:20
Enter ".help" for usage hints.
sqlite> SELECT COUNT(*) FROM students;
4
sqlite> .quit"""),
])

expected = p("Your names and cities will differ; the shape will not. Four things to confirm: the <code>CREATE TABLE</code> printed nothing (silence is success in SQL), each <code>INSERT</code> printed nothing, <code>SELECT *</code> drew exactly one row per person inside the box, and <code>COUNT(*)</code> after reopening equals the number of people.") + \
    p("The file size will be 8192 or 12288 bytes — SQLite writes in 4 KB pages. Your date and user name replace <code>kiet</code>.")

check = term("terminal 1 — in the data folder", """$ python3 ../code/stage1/check.py
PASS: database file exists at /home/kiet/kiet-bootcamp-3/data/team_details.db
PASS: table 'students' exists
PASS: students has the three columns in order
PASS: at least 3 rows (one per team member)
PASS: no empty names, colleges or cities

5 passed, 0 failed""")

stuck = p('Skipped the typing? <code>sqlite3 team_details.db &lt; sample_team_details.sql</code> in the data folder builds the four-row example team in one go. Made a typo in the table? <code>DROP TABLE students;</code> and paste the CREATE again, or delete the file and start over.') + \
    p('Reference: <a href="reference/sqlite-cli.html">sqlite3 CLI</a> · <a href="reference/sql-for-students-table.html">SQL for the students table</a> · <a href="troubleshooting.html">Troubleshooting</a> (no such table, sqlite3 not found).')

qz = quiz([
    ("Which C construct is <code>SELECT student_name FROM students WHERE inter_city = 'Vijayawada'</code> closest to?",
     ["A struct definition", "A for loop with an if inside, printing one field", "A function prototype", "A file open"], 2,
     "FROM is the array, WHERE is the if, SELECT student_name is what gets printed for each row that passes."),
    ("You run <code>CREATE TABLE students (...)</code> and nothing is printed. What happened?",
     ["It failed silently", "It worked; SQL says nothing on success", "It is waiting for more input", "The file is read-only"], 2,
     "CREATE and INSERT print nothing when they succeed. An error would print a message starting with 'Parse error' or 'Runtime error'."),
    ("After <code>.quit</code>, where are the four rows?",
     ["Gone — the program ended", "In the terminal's memory", "In the file team_details.db", "In schema.sql"], 3,
     "The database is the file. Reopening it and running COUNT(*) proves the rows were written to disk."),
    ("Which line is not SQL?",
     ["<code>SELECT COUNT(*) FROM students;</code>", "<code>.headers on</code>", "<code>INSERT INTO students VALUES (...);</code>", "<code>CREATE TABLE students (...);</code>"], 2,
     "Lines starting with a dot are sqlite3 shell settings. They do not end with ; and they would mean nothing to Python's sqlite3 module."),
])

demo = ('<div class="panel media">\n<div class="cap">videos/stage1_demo.mp4</div>\n'
        '<video controls preload="metadata" src="videos/stage1_demo.mp4"></video>\n</div>\n'
        + p("A walk through this stage: opening the database, box mode, the table, four rows, the queries, and the file that is left behind."))

body = "\n".join([
    section("demo", "Demo", demo),
    section("concept", "Concept", concept + stp),
    section("task", "Task", task),
    section("expected", "Expected output", expected),
    section("check", "Check yourself", check),
    section("takeaway", "Takeaway", callout("A database is a file that stores tables and does the searching for you. SELECT … WHERE is the for-loop with the if inside it.")),
    section("stuck", "Stuck?", stuck),
    section("quiz", "Quiz", qz),
])

write("stage1.html", page("Data that survives: SQLite and SQL", "stage1.html", body,
                          sub="An array of structs that lives in a file and does its own searching. Build your team's table by hand, then watch it outlive the program.",
                          artifact="SELECT student_name FROM students WHERE inter_city = 'Vijayawada';",
                          stage_label="Stage 1",
                          prev_page=("stage0.html", 'Stage 0 · Just enough Python'),
                          next_page=("stage2.html", 'Stage 2 · Python talks to the database')))
