"""FAQ: the fifteen student doubts, written up as Markdown in build/faq/*.md and
rendered here into kiet-bootcamp-3/docs/faq/*.html plus the faq.html index.
The Markdown converter is small and knows only what these files use."""
import os
import re
from lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "faq")

# Reading order: each file's "What is Next?" points at the following ones.
ORDER = [
    ("what_is_git", "Git"),
    ("git_vs_github", "Git"),
    ("why_git_commands_wsl_ubuntu", "Terminal"),
    ("ls_pwd_cd_mkdir_commands", "Terminal"),
    ("mv_command", "Terminal"),
    ("sudo_command", "Terminal"),
    ("modify_file_after_commit", "Git"),
    ("recover_older_version_git", "Git"),
    ("merge_conflicts_git", "Git"),
    ("pull_requests", "GitHub"),
    ("build_website_from_scratch", "Building"),
    ("deploy_website", "Building"),
    ("beginner_project_ideas", "Building"),
    ("github_profile_improvement", "GitHub"),
    ("understanding_ai_vs_using_ai", "AI"),
]

# first word of a line inside a ```bash block that makes it a command (gets a $ prompt, hint, copy)
COMMANDS = {"git", "cd", "ls", "pwd", "mkdir", "mv", "cp", "rm", "touch", "code", "sudo", "apt",
            "clear", "python3", "wsl", "passwd", "exit", "whoami", "echo", "cat", "nano"}
CAPTION = {"bash": "terminal", "html": "HTML", "diff": "git diff", "markdown": "README.md", "": "text"}


# ---------------------------------------------------------------- inline
def inline(s):
    s = esc(s)
    codes = []
    def keep(m):
        codes.append(f"<code>{m.group(1)}</code>")
        return f"\x00{len(codes) - 1}\x00"
    s = re.sub(r"`([^`]+)`", keep, s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<em>\1</em>", s)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], s)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "s"


# ---------------------------------------------------------------- blocks
def fence(lang, lines):
    if lang == "bash":
        out = []
        for l in lines:
            w = l.strip().split(" ")[0] if l.strip() else ""
            out.append(("$ " + l) if w in COMMANDS else l)
        return term(CAPTION["bash"], "\n".join(out))
    return code(CAPTION.get(lang, lang), "\n".join(lines))


def table_block(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r":?-+:?", c) for c in r)]
    head, body = cells[0], cells[1:]
    h = "".join(f"<th>{inline(x)}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return f'<div class="panel"><table class="prose"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def quote_block(lines):
    text = [re.sub(r"^>\s?", "", l) for l in lines]
    paras, cur = [], []
    for t in text:
        if t.strip():
            cur.append(t.strip())
        elif cur:
            paras.append(" ".join(cur)); cur = []
    if cur:
        paras.append(" ".join(cur))
    return "<blockquote>" + "".join(f"<p>{inline(x)}</p>" for x in paras) + "</blockquote>"


def list_block(items, ordered):
    """items: list of (text, [nested texts])"""
    tag = "ol" if ordered else "ul"
    out = [f"<{tag}>"]
    for text, sub in items:
        inner = inline(text)
        if sub:
            inner += "<ul>" + "".join(f"<li>{inline(s)}</li>" for s in sub) + "</ul>"
        out.append(f"<li>{inner}</li>")
    out.append(f"</{tag}>")
    return "".join(out)


ITEM = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def convert(md):
    """Markdown text -> (title, body_html). Sections open at every ## heading."""
    lines = md.split("\n")
    title, out, i, n = "", [], 0, len(lines)
    open_section = False

    def close_section():
        nonlocal open_section
        if open_section:
            out.append("</section>")
            open_section = False

    while i < n:
        l = lines[i]
        s = l.strip()
        if not s or s == "---":
            i += 1; continue
        if l.startswith("```"):
            lang = l[3:].strip()
            j = i + 1
            while j < n and not lines[j].startswith("```"):
                j += 1
            out.append(fence(lang, lines[i + 1:j]))
            i = j + 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)$", l)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1:
                title = text
            elif level == 2:
                close_section()
                out.append(f'<section id="{slug(text)}">\n<h2>{inline(text)}</h2>')
                open_section = True
            else:
                out.append(f"<h{level}>{inline(text)}</h{level}>")
            i += 1; continue
        if s.startswith("|"):
            j = i
            while j < n and lines[j].strip().startswith("|"):
                j += 1
            out.append(table_block(lines[i:j]))
            i = j; continue
        if s.startswith(">"):
            j = i
            while j < n and lines[j].strip().startswith(">"):
                j += 1
            out.append(quote_block(lines[i:j]))
            i = j; continue
        im = ITEM.match(l)
        if im and im.group(1) == "":
            ordered = im.group(2)[0].isdigit()
            items = []
            j = i
            while j < n:
                lm = ITEM.match(lines[j])
                if lm and lm.group(1) == "":
                    items.append([lm.group(3).strip(), []]); j += 1
                elif lm and items and lm.group(1):
                    items[-1][1].append(lm.group(3).strip()); j += 1
                elif lines[j].startswith(" ") and lines[j].strip() and items:
                    if items[-1][1]:
                        items[-1][1][-1] += " " + lines[j].strip()
                    else:
                        items[-1][0] += " " + lines[j].strip()
                    j += 1
                elif not lines[j].strip() and j + 1 < n and ITEM.match(lines[j + 1]) and ITEM.match(lines[j + 1]).group(1) == "":
                    j += 1   # blank line between items of the same list
                else:
                    break
            out.append(list_block(items, ordered))
            i = j; continue
        # paragraph: run of plain lines
        j = i
        para = []
        while j < n and lines[j].strip() and not lines[j].startswith(("```", "#", "|", ">")) and not ITEM.match(lines[j]) and lines[j].strip() != "---":
            para.append(lines[j].strip()); j += 1
        if not para:   # a lone stray line; keep it as text
            para, j = [s], i + 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
        i = j
    close_section()
    return title, "\n".join(out)


# ---------------------------------------------------------------- pages
pages = []
for k, (name, topic) in enumerate(ORDER):
    md = open(os.path.join(SRC, name + ".md"), encoding="utf-8").read()
    title, body = convert(md)
    pages.append((name, topic, title, body))

for k, (name, topic, title, body) in enumerate(pages):
    prev_page = (f"{pages[k - 1][0]}.html", pages[k - 1][2]) if k > 0 else ("../faq.html", "All questions")
    next_page = (f"{pages[k + 1][0]}.html", pages[k + 1][2]) if k + 1 < len(pages) else ("../faq.html", "All questions")
    write(f"faq/{name}.html", page(title, "faq.html", f'<div class="faq">\n{body}\n</div>', depth=1,
                                   stage_label=f"FAQ · {k + 1} of {len(pages)} · {topic}",
                                   prev_page=prev_page, next_page=next_page))

# index
intro = p("""Fifteen questions students asked after the earlier bootcamps, each answered from scratch in plain words:
the terminal, Git and GitHub, building and deploying a website, and what it means to understand AI rather than
just use it. They read in order — every answer ends by pointing at the next question — but any one stands on
its own. None of it is needed on the bootcamp day; it is for the weeks after.""")
cards = []
for k, (name, topic, title, body) in enumerate(pages):
    cards.append(f'<a class="card" href="faq/{name}.html"><div class="num">{k + 1:02d} · {esc(topic)}</div><h3>{esc(title)}</h3><div class="go">Read →</div></a>')
body = section("about", "What this is", intro) + section("questions", "The questions, in order", '<div class="cards">' + "".join(cards) + "</div>")
write("faq.html", page("FAQ", "faq.html", body, sub="Doubts asked by students, answered one at a time.", artifact="15 questions · read in order or dip in"))
