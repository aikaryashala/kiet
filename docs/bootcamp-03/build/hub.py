"""The online hub in kiet/docs/bootcamp-03/: index.html and setup.html."""
import os
import lib
from lib import *

HUB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MATERIAL = "https://aikaryashala.com/kiet-bootcamp-3/"
GITHUB = "https://github.com/aikaryashala/kiet-bootcamp-3"

HUB_NAV = '''<nav class="nav" aria-label="Pages">
<a href="index.html"{i}>Home</a>
<a href="setup.html"{s}>Setup</a>
<div class="group">On the day</div>
<a href="{m}">Bootcamp guide</a>
<a href="{g}">GitHub repo</a>
<div class="group">Earlier</div>
<a href="../bootcamp-02/">Bootcamp 2</a>
<a href="../bootcamp-01/">Bootcamp 1</a>
</nav>'''


def hub_page(name, title, body, sub, artifact):
    lib.NAV_OVERRIDE = HUB_NAV.format(i=' class="cur"' if name == "index.html" else "",
                                      s=' class="cur"' if name == "setup.html" else "", m=MATERIAL, g=GITHUB)
    html = page(title, name, body, depth=0, sub=sub, artifact=artifact)
    open(f"{HUB}/{name}", "w", encoding="utf-8").write(html)
    print("wrote hub", name, len(html))


def card(num, href, title, desc):
    return (f'<a class="card" href="{href}"><div class="num">{esc(num)}</div><h3>{esc(title)}</h3>'
            f'<p>{desc}</p><div class="go">Open →</div></a>')


# ---------------------------------------------------------------- index
# index.html is hand-written in the bootcamp-02 card style (masthead, logo, inline CSS). Edit it directly.

# ---------------------------------------------------------------- setup
# setup.html is hand-maintained now, like index.html. It is NOT regenerated: edit the HTML directly.
# (The generator that produced it was removed on 20 Sep 2026 after a rebuild overwrote a hand edit.)
