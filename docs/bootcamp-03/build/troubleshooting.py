from lib import *


def item(sid, title, symptom, cause, fix):
    return f'<section id="{sid}"><h2>{esc(title)}</h2>' + term("what you see", symptom) + p(cause) + fix + "</section>"


body = p("Every message below is one you can actually get during the day, with the line that fixes it. Find the text you see on screen; the cause is next to it.") + \
item("inuse", "Address already in use", """$ python3 server.py
Serving on http://localhost:8080  — Ctrl+C to stop
Bottle v0.13.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.

Traceback (most recent call last):
~
OSError: [Errno 98] Address already in use""",
     "Another program already holds that port — almost always an earlier copy of a server you forgot to stop, maybe in a terminal you closed. A closed terminal does not always kill what was running in it.",
     p("Find it and stop it, then start again:") + term("terminal", """$ lsof -i :8080
COMMAND   PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3  4242  kiet    3u  IPv4  31337      0t0  TCP localhost:8080 (LISTEN)
$ kill 4242""") + p("Or in one line: <code>fuser -k 8080/tcp</code>. If you meant to run two servers, give the second one another port: <code>python3 server.py --port 8090</code>.")) + \
item("refused", "Connection refused", """$ curl localhost:8080/hai
curl: (7) Failed to connect to localhost port 8080 after 0 ms: Couldn't connect to server""",
     "Nothing is listening on that port. The server is not running, or it is running on a different port than the one you typed, or it crashed on start (look at its terminal).",
     p("Look at Terminal 1. If it shows a prompt instead of <code>Listening on…</code>, start the server. If it shows a traceback, read the last line. Check the port number in the curl matches the one in the start line.")) + \
item("bottle", "ModuleNotFoundError: No module named 'bottle'", """$ python3 server.py
Traceback (most recent call last):
  File "server.py", line 15, in <module>
    from bottle import route, run, request, response
ModuleNotFoundError: No module named 'bottle'""",
     "Python looks for <code>bottle.py</code> in the same folder as the file you ran. You ran the file from a folder that does not have it, or you copied <code>server.py</code> somewhere on its own.",
     p("Run it from its own folder: <code>cd ~/kiet-bootcamp-3/code/stage5</code> then <code>python3 server.py</code>. Each server folder has its own <code>bottle.py</code>. If you made a new folder, copy <code>bottle.py</code> into it.")) + \
item("notable", "no such table: students", """$ python3 read_all.py
Traceback (most recent call last):
~
sqlite3.OperationalError: no such table: students""",
     "The program opened a database file that has no <code>students</code> table in it. SQLite creates an empty file when the path does not exist, so a wrong path never says 'file not found' — it says this.",
     p("Check where the program is looking. The Stage 5 server prints its DB path on start. For Stage 2, the file must be <code>~/kiet-bootcamp-3/data/team_details.db</code>, built in Stage 1. An empty <code>team_details.db</code> that appeared by accident can be deleted; then redo Stage 1 or run <code>sqlite3 team_details.db &lt; sample_team_details.sql</code>.")) + \
item("sqlite3cmd", "sqlite3: command not found", """$ sqlite3 team_details.db
bash: sqlite3: command not found""",
     "The command-line tool is not installed. Python's own copy does the same job.",
     term("terminal", """$ python3 -m sqlite3 team_details.db
sqlite> """) + p("Everything after the prompt is identical. To run a <code>.sql</code> file: <code>.read all_students.sql</code> inside the shell.")) + \
item("indent", "IndentationError", """$ python3 server.py
  File "server.py", line 52
    response.status = 400
IndentationError: unexpected indent""",
     "In Python the indentation is the syntax. A line indented more or less than its neighbours, or a mix of tabs and spaces, is an error at the line it names. <code>expected an indented block</code> means a <code>def</code> or <code>if</code> has nothing under it — for example after commenting out the only line of a function.",
     p("Go to the line number. Make it line up with the lines around it, using spaces only (four per level, as the given files do). If you commented out a function body, comment out its <code>def</code> line too.")) + \
item("crlf", "SyntaxError or strange ^M after editing on another machine", """$ python3 server.py
  File "server.py", line 1
    # server.py — Stage 5.^M
SyntaxError: invalid non-printable character U+000D""",
     "The file was edited on Windows and saved with Windows line endings. Linux Python sees an extra character at the end of every line.",
     term("terminal", """$ sed -i 's/\\r$//' server.py""") + p("Then run it again. Edit on the machine you run on, and this does not happen.")) + \
item("stop", "How to stop a server, and what happens if you close the terminal instead", """Hit Ctrl-C to quit.
^C
$ """,
     "Ctrl+C in the server's terminal ends the process cleanly and frees the port. Closing the terminal window usually ends it too, but not always — on some desktops the process keeps running invisibly, still holding the port. That is where 'Address already in use' comes from.",
     p("Stop servers with Ctrl+C. If a port is stuck, see <a href=\"#inuse\">Address already in use</a> above.")) + \
item("cors", "The browser says CORS, the server says 200", """Access to fetch at 'http://localhost:8080/students?college=…' from origin 'http://localhost:9000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.""",
     "The page came from port 9000 and asked port 8080. The browser will only hand the page that answer if the answer carries <code>Access-Control-Allow-Origin</code>. curl does not care; the browser always does. The server did its job — Terminal 1 logged a 200.",
     p("The hook in <code>code/stage5/server.py</code> must be present and uncommented, all three lines, and the server restarted after any edit. Stage 8 is about exactly this.")) + \
item("500", "Internal Server Error (500)", """$ curl localhost:8080/count
~
<h1>Error: 500 Internal Server Error</h1>""",
     "Your route crashed while answering. With <code>debug=True</code> the full traceback is printed in Terminal 1, ending in a line that names the file and line number and the kind of error — <code>TypeError</code>, <code>KeyError</code>, <code>NameError</code>.",
     p("Read the last three lines in Terminal 1. A <code>NameError</code> is a variable you did not define; a <code>KeyError</code> is a dict key that is not there (use <code>.get</code>); a <code>TypeError … NoneType</code> usually means <code>request.json</code> or <code>.get()</code> gave None and you used it without the <code>is None</code> guard.")) + \
item("space", "curl: (3) URL rejected: Malformed input", """$ curl "localhost:8080/students?college=Narayana Junior College"
curl: (3) URL rejected: Malformed input to a URL function""",
     "A URL cannot contain a space.",
     p("Write <code>+</code> for each space: <code>college=Narayana+Junior+College</code>. And keep the quotes: without them a bare <code>&amp;</code> makes the shell run curl in the background and drop the rest."))

write("troubleshooting.html", page("Troubleshooting", "troubleshooting.html", body,
                                  sub="The messages you will actually see, what they mean, and the line that fixes them.",
                                  artifact="lsof -i :8080"))
