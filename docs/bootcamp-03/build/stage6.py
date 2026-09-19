from lib import *

concept = p("""Your server has answered about four people. Now it will answer about two hundred, and you
will not change a line. The server never knew which file it was reading. It knew the <em>shape</em> of
the table — three text columns with three fixed names — and that is all the SQL in it depends on. Point
it at a bigger file with the same shape and every route keeps working, the counts just get bigger.""") + \
p("""The bigger file does not exist yet. What exists is <code>all_students.sql</code>: two hundred
<code>INSERT</code> statements under the same <code>CREATE TABLE</code>, in a text file. A
<code>.sql</code> file is a script — the database's equivalent of a <code>.c</code> source file. Running
it through sqlite3 builds the <code>.db</code> the way compiling builds the binary. The source is small,
readable, and goes in git; the built file is what programs open, and it can always be rebuilt.""") + \
p("""That is also why <code>team_details.db</code> is not in the repository and yours was built by hand
in Stage 1: <code>.db</code> files are outputs. The header of <code>all_students.sql</code> lists the
exact counts per college and per city, so you can check the server's answers against the source.""") + \
p("""The switch happens on the command line. <code>--db</code> is read by the same
<code>sys.argv</code> loop from Stage 0 block 5, and the path it gives replaces the default. Restart
with a different <code>--db</code> and the same code serves different data.""")

task = steps([
    p("<strong>Terminal 1.</strong> Build the big database from its source. The <code>&lt;</code> feeds the file to sqlite3 as if you had typed it. It prints nothing. Then open the new file, set box mode as in Stage 1, and ask it how many rows and how many colleges it has.") +
    term("terminal 1", """$ cd ~/kiet-bootcamp-3/data
$ sqlite3 all_students.db < all_students.sql
$ sqlite3 all_students.db
SQLite version 3.45.1 2024-01-30 16:01:20
Enter ".help" for usage hints.
sqlite> .mode box
sqlite> SELECT COUNT(*) FROM students;
┌──────────┐
│ COUNT(*) │
├──────────┤
│ 200      │
└──────────┘
sqlite> SELECT COUNT(DISTINCT inter_college) FROM students;
┌───────────────────────────────┐
│ COUNT(DISTINCT inter_college) │
├───────────────────────────────┤
│ 12                            │
└───────────────────────────────┘
sqlite> .quit""") + p("No <code>sqlite3</code> command? <code>python3 -m sqlite3 all_students.db</code>, then <code>.read all_students.sql</code>, then the two SELECTs (no <code>.mode</code> there; it prints tuples), then <code>.quit</code>."),
    p("Look at the top of the source file. The counts you are about to see from the server are written there.") +
    term("terminal 1", """$ head -30 all_students.sql
-- all_students.sql — 200 students across 12 intermediate colleges and 8 cities.
-- Build the database:   sqlite3 all_students.db < all_students.sql
--
-- Exact counts (quoted by the material's Expected output blocks):
--   total rows: 200
--
--   per college (SELECT inter_college, COUNT(*) FROM students GROUP BY inter_college ORDER BY inter_college):
--     Aditya Junior College             13
--     Bhashyam Junior College           12
--     Government Junior College          6
--     Krishnaveni Junior College         5
--     NRI Junior College                18
--     Narayana Junior College           49
--     Sasi Junior College                3
--     Sri Chaitanya Junior College      57
--     Sri Gayatri Junior College        14
--     Sri Prakash Junior College         4
--     Tirumala Junior College            9
--     Vignan Junior College             10
--
--   per city (SELECT inter_city, COUNT(*) FROM students GROUP BY inter_city ORDER BY inter_city):
--     Guntur                            30
--     Kakinada                          24
--     Kurnool                            9
--     Nellore                           16
--     Rajahmundry                       20
--     Tirupati                          14
--     Vijayawada                        41
--     Visakhapatnam                     46
--"""),
    p("<strong>Terminal 1 — server.</strong> Go to Stage 5, stop the running server with Ctrl+C, and start it again with <code>--db</code> pointing at the new file. The start line names the file it will read. <em>Do not edit server.py.</em>") +
    term("terminal 1 — server", """$ cd ~/kiet-bootcamp-3/code/stage5
$ python3 server.py --db ../../data/all_students.db
Serving on http://localhost:8080  (DB: /home/kiet/kiet-bootcamp-3/data/all_students.db)  — Ctrl+C to stop
Bottle v0.13.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.
"""),
    p("<strong>Terminal 2.</strong> The same curls as Stage 5. Twelve colleges instead of two; a city query returns dozens of rows.") +
    term("terminal 2 — curl", """$ curl localhost:8080/colleges
{"colleges": ["Aditya Junior College", "Bhashyam Junior College", "Government Junior College", "Krishnaveni Junior College", "NRI Junior College", "Narayana Junior College", "Sasi Junior College", "Sri Chaitanya Junior College", "Sri Gayatri Junior College", "Sri Prakash Junior College", "Tirumala Junior College", "Vignan Junior College"]}
$ curl "localhost:8080/count?college=Narayana+Junior+College"
{"college": "Narayana Junior College", "count": 49}
$ curl "localhost:8080/count?college=Sri+Chaitanya+Junior+College"
{"college": "Sri Chaitanya Junior College", "count": 57}
$ curl "localhost:8080/students/by-location?location=Kurnool"
{"count": 9, "students": [{"student_name": "Ravi Rama Ravella", "inter_college": "Narayana Junior College", "inter_city": "Kurnool"}, {"student_name": "Gayathri Sri Gudla", "inter_college": "Narayana Junior College", "inter_city": "Kurnool"}, {"student_name": "Supriya Varshini Nalluri", "inter_college": "Narayana Junior College", "inter_city": "Kurnool"}, {"student_name": "Vasavi Prasanna Bommu", "inter_college": "Narayana Junior College", "inter_city": "Kurnool"}, {"student_name": "Venkat Satya Kota", "inter_college": "Narayana Junior College", "inter_city": "Kurnool"}, {"student_name": "Mounika Kumari Kondapalli", "inter_college": "Narayana Junior College", "inter_city": "Kurnool"}, {"student_name": "Yamini Sai Sastry", "inter_college": "Narayana Junior College", "inter_city": "Kurnool"}, {"student_name": "Rajesh Charan Kanchi", "inter_college": "Narayana Junior College", "inter_city": "Kurnool"}, {"student_name": "Arun Rama Sunkara", "inter_college": "Narayana Junior College", "inter_city": "Kurnool"}]}"""),
    p("<strong>Terminal 3 — the same questions in the shell.</strong> Open the big file with box mode on and ask what the three curls asked. Twelve colleges, 49 Narayana students, nine names in Kurnool: the server was only ever running these statements.") +
    term("terminal 3 — sqlite>", """$ sqlite3 ~/kiet-bootcamp-3/data/all_students.db
SQLite version 3.45.1 2024-01-30 16:01:20
Enter ".help" for usage hints.
sqlite> .mode box
sqlite> SELECT DISTINCT inter_college FROM students ORDER BY inter_college;
┌──────────────────────────────┐
│        inter_college         │
├──────────────────────────────┤
│ Aditya Junior College        │
│ Bhashyam Junior College      │
│ Government Junior College    │
│ Krishnaveni Junior College   │
│ NRI Junior College           │
│ Narayana Junior College      │
│ Sasi Junior College          │
│ Sri Chaitanya Junior College │
│ Sri Gayatri Junior College   │
│ Sri Prakash Junior College   │
│ Tirumala Junior College      │
│ Vignan Junior College        │
└──────────────────────────────┘
sqlite> SELECT COUNT(*) FROM students WHERE inter_college = 'Narayana Junior College';
┌──────────┐
│ COUNT(*) │
├──────────┤
│ 49       │
└──────────┘
sqlite> SELECT student_name FROM students WHERE inter_city = 'Kurnool';
┌───────────────────────────┐
│       student_name        │
├───────────────────────────┤
│ Ravi Rama Ravella         │
│ Gayathri Sri Gudla        │
│ Supriya Varshini Nalluri  │
│ Vasavi Prasanna Bommu     │
│ Venkat Satya Kota         │
│ Mounika Kumari Kondapalli │
│ Yamini Sai Sastry         │
│ Rajesh Charan Kanchi      │
│ Arun Rama Sunkara         │
└───────────────────────────┘
sqlite> .quit"""),
    p("A college that exists in the big file but not in your team's. In Stage 5 this gave <code>count 0</code>; the code is identical, the data is not.") +
    term("terminal 2 — curl", """$ curl "localhost:8080/students?college=Sri+Prakash+Junior+College"
{"count": 4, "students": [{"student_name": "Sruthi Varshini Boddu", "inter_college": "Sri Prakash Junior College", "inter_city": "Kakinada"}, {"student_name": "Lakshmi Sai Gudla", "inter_college": "Sri Prakash Junior College", "inter_city": "Kakinada"}, {"student_name": "Pavan Kiran Puli", "inter_college": "Sri Prakash Junior College", "inter_city": "Kakinada"}, {"student_name": "Rohith Reddy Boddu", "inter_college": "Sri Prakash Junior College", "inter_city": "Kakinada"}]}
$ curl "localhost:8080/students/search?college=Sri+Prakash+Junior+College&location=Vijayawada"
{"count": 0, "students": []}
$ curl "localhost:8080/students/search?college=Sasi+Junior+College&location=Guntur"
{"count": 2, "students": [{"student_name": "Sudheer Chandra Gupta", "inter_college": "Sasi Junior College", "inter_city": "Guntur"}, {"student_name": "Tejaswini Harini Achari", "inter_college": "Sasi Junior College", "inter_city": "Guntur"}]}""") +
    p("Sri Prakash exists in exactly one city and Kurnool has exactly one college — the source file says so in its header. Use them to predict a search result before you run it."),
])

expected = p("Every number the server returns matches the header of <code>all_students.sql</code>: 12 names from <code>/colleges</code>, 49 for Narayana, 57 for Sri Chaitanya, 9 rows for Kurnool, 4 for Sri Prakash. Terminal 1 logs the same shapes as Stage 5 with bigger byte counts:") + \
    term("terminal 1 — server", """127.0.0.1 - - [21/Sep/2026 11:58:47] "GET /colleges HTTP/1.1" 200 341
127.0.0.1 - - [21/Sep/2026 11:58:47] "GET /count?college=Narayana+Junior+College HTTP/1.1" 200 51
127.0.0.1 - - [21/Sep/2026 11:58:47] "GET /count?college=Sri+Chaitanya+Junior+College HTTP/1.1" 200 56
127.0.0.1 - - [21/Sep/2026 11:58:48] "GET /students/by-location?location=Kurnool HTTP/1.1" 200 1021
127.0.0.1 - - [21/Sep/2026 11:58:47] "GET /students?college=Sri+Prakash+Junior+College HTTP/1.1" 200 478
127.0.0.1 - - [21/Sep/2026 11:58:48] "GET /students/search?college=Sri+Prakash+Junior+College&location=Vijayawada HTTP/1.1" 200 28
127.0.0.1 - - [21/Sep/2026 11:58:48] "GET /students/search?college=Sasi+Junior+College&location=Guntur HTTP/1.1" 200 242""")

check = term("terminal 2 — curl", """$ python3 ../stage6/check.py
PASS: all_students.db exists at /home/kiet/kiet-bootcamp-3/data/all_students.db
PASS: all_students.db has 200 rows
PASS: all_students.db has 12 colleges
PASS: server on 8080 serves all_students.db: /colleges lists the same 12 colleges
PASS: /count?college=Narayana+Junior+College matches the file (49)

5 passed, 0 failed""") + p("If the fourth line says <code>2 — the server is still on team_details.db</code>, you restarted without <code>--db</code>.")

stuck = p('Nothing to write in this stage, so there is no solution folder. If <code>all_students.db</code> came out with 0 rows, delete it and run the build line again — a typo in the redirect creates an empty file.') + \
    p('Reference: <a href="reference/sqlite-cli.html">sqlite3 CLI</a> (running a .sql file) · <a href="troubleshooting.html">Troubleshooting</a> (no such table means the server opened a path that did not exist and SQLite created an empty file there).')

qz = quiz([
    ("How many lines of <code>server.py</code> changed between Stage 5 and Stage 6?",
     ["One: the database path", "Four: one per route", "Zero", "All the SQL"], 3,
     "The path came in through --db on the command line. The code depends on the table's shape, not on which file holds it."),
    ("What is <code>all_students.sql</code>?",
     ["The database", "A text file of SQL statements that builds the database", "A backup of team_details.db", "A Python script"], 2,
     "Source, not output. sqlite3 all_students.db < all_students.sql runs every statement and produces the .db file."),
    ("You started the server with <code>--db ../../data/all_students.db</code> but <code>/colleges</code> still shows two names. Most likely cause?",
     ["The big file has two colleges", "You did not stop the old server; the old process on 8080 is still answering", "curl caches", "The query needs ORDER BY"], 2,
     "If the old process still holds port 8080, the new one fails to start with 'Address already in use' and the old one keeps answering. Ctrl+C the old one first."),
    ("Which query can you predict from the file header without running it?",
     ["<code>/students/search?college=Sri+Prakash+Junior+College&location=Kakinada</code> → 4", "<code>/students?college=Narayana+Junior+College</code> → the names", "<code>/colleges</code> → the order", "None of them"], 1,
     "The header says Sri Prakash appears only in Kakinada with 4 rows. Names and byte counts you have to run for."),
])

body = "\n".join([
    section("concept", "Concept", concept),
    section("task", "Task", task),
    section("expected", "Expected output", expected),
    section("check", "Check yourself", check),
    section("takeaway", "Takeaway", callout("Code depends on the shape of the data, not the data itself. Zero lines changed.")),
    section("stuck", "Stuck?", stuck),
    section("quiz", "Quiz", qz),
])

write("stage6.html", page("Swap the data, not the code", "stage6.html", body,
                          sub="Build a 200-row database from its .sql source, point the same server at it, and change nothing else.",
                          artifact="python3 server.py --db ../../data/all_students.db",
                          stage_label="Stage 6 · Session 3 · after dinner · short",
                          prev_page=("stage5.html", 'Stage 5 · Join the two halves'),
                          next_page=("stage7.html", "Stage 7 · Someone else's client: the browser")))
