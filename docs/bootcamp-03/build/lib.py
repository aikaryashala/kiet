"""Helpers that turn page content into HTML for kiet-bootcamp-3/docs.
Build-time only. The emitted HTML is what gets committed."""
import html
import json
import os

# The student repo is a sibling of the kiet repo: <workspace>/kiet-bootcamp-3
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "kiet-bootcamp-3"))
DOCS = os.path.join(REPO, "docs")

NAV = [
    ("group", "Session 1 · morning"),
    ("stage0.html", "Stage 0 · Python"),
    ("stage1.html", "Stage 1 · SQLite"),
    ("stage2.html", "Stage 2 · Python + SQL"),
    ("group", "Session 2 · afternoon"),
    ("stage3.html", "Stage 3 · A server"),
    ("stage4.html", "Stage 4 · Your server"),
    ("stage5.html", "Stage 5 · The backend"),
    ("group", "Session 3 · after dinner"),
    ("stage6.html", "Stage 6 · Big data"),
    ("stage7.html", "Stage 7 · Browser"),
    ("stage8.html", "Stage 8 · Inspector"),
    ("group", "Reference"),
    ("reference/python-cheatsheet.html", "Python cheatsheet"),
    ("reference/c-to-python.html", "C to Python"),
    ("reference/sqlite-cli.html", "sqlite3 CLI"),
    ("reference/sql-for-students-table.html", "SQL for students"),
    ("reference/json.html", "JSON"),
    ("reference/bottle.html", "Bottle"),
    ("reference/curl.html", "curl"),
    ("reference/http-basics.html", "HTTP basics"),
    ("group", "Help"),
    ("troubleshooting.html", "Troubleshooting"),
]


NAV_OVERRIDE = None


def esc(s):
    return html.escape(s, quote=False)


def rel(depth):
    return "../" * depth


def nav(cur, depth):
    if NAV_OVERRIDE:
        return NAV_OVERRIDE
    out = ['<nav class="nav" aria-label="Pages">']
    out.append(f'<a href="{rel(depth)}index.html"{" class=cur" if cur == "index.html" else ""}>Home</a>')
    for href, label in NAV:
        if href == "group":
            out.append(f'<div class="group">{esc(label)}</div>')
        else:
            cls = ' class="cur"' if href == cur else ""
            out.append(f'<a href="{rel(depth)}{href}"{cls}>{esc(label)}</a>')
    out.append("</nav>")
    return "\n".join(out)


def page(title, cur, body, depth=0, sub="", artifact="", stage_label="", head_extra=""):
    r = rel(depth)
    header = ['<header class="page">']
    if stage_label:
        header.append(f'<p class="stage">{esc(stage_label)}</p>')
    header.append(f"<h1>{esc(title)}</h1>")
    if sub:
        header.append(f'<p class="sub">{sub}</p>')
    if artifact:
        header.append(f'<p class="artifact">{esc(artifact)}</p>')
    header.append("</header>")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — KIET Bootcamp 3</title>
<link rel="stylesheet" href="{r}style.css">
<script src="{r}script.js" defer></script>
{head_extra}</head>
<body>
<div class="wrap">
<div class="layout">
{nav(cur, depth)}
<main>
{chr(10).join(header)}
{body}
<footer class="page">
  <span>KIET Bootcamp 3 · 21–22 September 2026</span>
  <span>AI Karyashala</span>
</footer>
</main>
</div>
</div>
</body>
</html>
"""


# ---------- blocks ----------
def panel(caption, inner, cls=""):
    c = f' {cls}' if cls else ""
    return f'<div class="panel{c}">\n<div class="cap">{esc(caption)}</div>\n{inner}\n</div>'


def term(caption, transcript, on=None, pre_id=None):
    """transcript: text; lines starting with '$ ' are commands, others output.
    A line that is exactly '~' renders as a dim ellipsis line '…'."""
    lines = transcript.strip("\n").split("\n")
    out = []
    for i, line in enumerate(lines):
        cls = "ln"
        if i == on:
            cls += " on"
        prompt = None
        for pr in ("$ ", "sqlite> ", "   ...> "):
            if line.startswith(pr):
                prompt = pr
        if prompt:
            out.append(f'<span class="{cls} cmd"><span class="p">{prompt}</span>{esc(line[len(prompt):])}</span>')
        elif line == "~":
            out.append(f'<span class="{cls} dim">…</span>')
        else:
            out.append(f'<span class="{cls}">{esc(line) if line else " "}</span>')
    idattr = f' id="{pre_id}"' if pre_id else ""
    return panel(caption, f'<pre class="term"{idattr}>' + "".join(out) + "</pre>")


def code(caption, text, copy=False, pre_id=None, on=None, lang=None):
    lines = text.strip("\n").split("\n")
    out = []
    for i, line in enumerate(lines):
        cls = "ln on" if i == on else "ln"
        body = esc(line) if line else " "
        if lang == "py" and line.lstrip().startswith("#"):
            body = f'<span class="cm">{body}</span>'
        out.append(f'<span class="{cls}">{body}</span>')
    attrs = ' data-copy=""' if copy else ""
    if pre_id:
        attrs += f' id="{pre_id}"'
    return panel(caption, f'<pre class="code"{attrs}>' + "".join(out) + "</pre>")


def code_file(caption, relpath, copy=False, pre_id=None, on=None, strip_header=False, lines=None):
    text = open(os.path.join(REPO, relpath), encoding="utf-8").read()
    if strip_header:
        body = text.split("\n")
        while body and body[0].startswith("#"):
            body.pop(0)
        while body and body[0].strip() == "":
            body.pop(0)
        text = "\n".join(body)
    if lines:
        a, b = lines
        text = "\n".join(text.split("\n")[a - 1:b])
    lang = "py" if relpath.endswith(".py") else None
    return code(caption, text, copy=copy, pre_id=pre_id, on=on, lang=lang)


def callout(text):
    return f'<div class="callout"><p>{text}</p></div>'


def quiz(items):
    """items: list of (question_html, [option, ...], answer_1based, explanation_html)"""
    out = ['<div class="quiz">']
    for q, opts, ans, exp in items:
        out.append(f'<div class="q" data-answer="{ans}">')
        out.append(f"<p>{q}</p>")
        for o in opts:
            out.append(f'<button class="opt" type="button">{o}</button>')
        out.append(f'<p class="exp">{exp}</p>')
        out.append("</div>")
    out.append("</div>")
    return "\n".join(out)


def stepper(left_html, right_html, steps):
    return f"""<div class="stepper">
<div class="stage">
<div>{left_html}</div>
<div>{right_html}</div>
</div>
<div class="controls">
<button class="back" type="button">Back</button>
<button class="play" type="button">Play</button>
<button class="fwd" type="button">Forward</button>
<span class="counter"></span>
</div>
<div class="track"><span></span></div>
<p class="narration"></p>
<script type="application/json" class="steps">{json.dumps(steps, ensure_ascii=False)}</script>
</div>"""


def slots(items):
    """items: list of (id, key, initial_value, cls)"""
    out = ['<div class="slots">']
    for sid, k, v, cls in items:
        out.append(f'<div class="slot" id="{sid}"><div class="k">{esc(k)}</div><div class="v {cls}">{esc(v)}</div></div>')
    out.append("</div>")
    return "\n".join(out)


def table(caption, headers, rows, table_id=None, prose=False):
    idattr = f' id="{table_id}"' if table_id else ""
    cls = ' class="prose"' if prose else ""
    h = "".join(f"<th>{esc(x)}</th>" for x in headers)
    body = []
    for r in rows:
        body.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    inner = f'<table{idattr}{cls}><thead><tr>{h}</tr></thead><tbody>{"".join(body)}</tbody></table>'
    return panel(caption, inner) if caption else inner


def rules(items):
    out = ['<div class="rules">']
    for c, d in items:
        out.append(f'<div class="rule"><div class="c">{c}</div><div class="d">{d}</div></div>')
    out.append("</div>")
    return "\n".join(out)


def section(sid, heading, inner):
    return f'<section id="{sid}">\n<h2>{esc(heading)}</h2>\n{inner}\n</section>'


def p(text):
    return f"<p>{text}</p>"


def steps(items):
    """items: list of html strings, each one numbered step"""
    return '<ol class="steps">\n' + "\n".join(f"<li>{x}</li>" for x in items) + "\n</ol>"


def write(relpath, content):
    path = os.path.join(DOCS, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(content)
    print("wrote", relpath, len(content))
