from lib import *

what = p("""Omarchy's screensaver is a text file run through random terminal effects: ASCII art in
<code>~/.config/omarchy/branding/screensaver.txt</code>, one copy per monitor, until you touch a key.
Out of the box that file holds the Omarchy logo. Put your own name there and the screensaver is yours.
This page draws the name in the same block letters as the Omarchy wordmark and hands you the file.""") + \
p("""Everything here is for the Omarchy laptop, not the Ubuntu VM. The commands are Omarchy 4.0's; if you
are on an older release and a menu entry is missing, the commands in the last section still work.""")

generator = '''<div class="omk-stage" aria-live="polite"><h3 id="preview" class="omk-preview empty">YOUR NAME</h3></div>
<div class="omk-controls">
  <div><label for="nameInput">name</label><input type="text" id="nameInput" placeholder="Type a name or word" autocomplete="off" maxlength="60"></div>
  <button id="downloadBtn" type="button" disabled>Download screensaver.txt</button>
</div>
<div class="panel omk-file"><div class="cap">screensaver.txt <span id="byteCount" style="margin-left:auto">0 bytes</span></div><pre id="fileContents"></pre></div>
<p id="status" class="omk-status" role="status"></p>'''.replace(' style="margin-left:auto"', '')

gen_text = p("""Type your name. The big preview is the Omarchy Font; the panel under it is the exact text that goes
into the file: each block character is two half-rows of the letter bitmap, which is how the wordmark itself
is drawn. Letters, digits and punctuation all work. Press Enter or the button to download.""")

place = steps([
    p("The browser saved the file to <code>~/Downloads</code>. Move it over the logo. There is no backup to make: <em>Restore Default</em> below brings the logo back any time.") +
    term("terminal", """$ mv ~/Downloads/screensaver.txt ~/.config/omarchy/branding/screensaver.txt"""),
    p("See it now. This forces the screensaver up even if the idle one is switched off. Any key or mouse movement exits it.") +
    term("terminal", """$ omarchy-launch-screensaver force""") +
    p("Or from the keyboard: <kbd>Super</kbd>+<kbd>Esc</kbd> opens the Omarchy menu at <em>System</em>; pick <em>Screensaver</em>. Left alone, it comes up by itself after two and a half minutes idle."),
])

without = p("Two ways that never leave the machine.") + \
    p("<strong>The menu.</strong> <kbd>Super</kbd>+<kbd>Space</kbd> opens the Omarchy menu. <em>Style › Screensaver › Edit Text</em> opens <code>screensaver.txt</code> in your editor; save and quit, and the screensaver fires up so you see the result. <em>Set From Image</em> converts a png or svg to ASCII instead. <em>Restore Default</em> puts the Omarchy logo back.") + \
    p("<strong>The command.</strong> <code>omarchy ascii</code> draws text in the same FIGlet font the wordmark uses, Delta Corps Priest 1. That font has letters and spaces only; digits and punctuation are dropped and named on stderr, which is the one reason to prefer the generator above.") + \
    term("terminal", """$ omarchy ascii "Ravi Teja" > ~/.config/omarchy/branding/screensaver.txt
$ omarchy-launch-screensaver force""") + \
    p("The same three menu entries, and <code>omarchy branding screensaver reset</code>, exist for the About screen: the file is <code>~/.config/omarchy/branding/about.txt</code> and the window that pops up is the one from <em>About</em> in the Omarchy menu.")

boot_intro = p("""The screen you see while Omarchy boots, and the login screen after it, share one logo and two
colours. Omarchy lets you swap all three with <code>omarchy plymouth</code>. Pick a photo of yourself,
turn it into a small PNG, preview the result without touching the boot setup, then apply it. This one needs
your password, because the boot screen lives in system folders.""")

boot = steps([
    p("<strong>Pick a photo.</strong> Any jpg or png: from your phone over USB, from the camera app, or from <code>~/Pictures</code>. Copy it somewhere short. The examples use <code>~/Pictures/me.jpg</code>.") +
    term("terminal", """$ ls ~/Pictures
me.jpg"""),
    p("<strong>Make a small PNG.</strong> The boot logo must be a PNG, and it sits on a 1920×1080 canvas, so 400 pixels wide is plenty. ImageMagick is already on Omarchy: <code>magick</code> resizes and converts in one go.") +
    term("terminal", """$ magick ~/Pictures/me.jpg -resize 400x400 ~/Pictures/me.png
$ magick identify ~/Pictures/me.png
/home/kiet/Pictures/me.png PNG 400x300 400x300+0+0 8-bit sRGB 187452B 0.000u 0:00.000""") +
    p("The second line shows the size it came out at. A photo works as is; a logo with a transparent background looks best, but that is a job for another day."),
    p("<strong>Preview.</strong> Two colours and the photo: background first, then text, both as <code>#RRGGBB</code>. This renders the boot screen into a PNG and opens it in the image viewer. Nothing is changed yet. Press <kbd>q</kbd> to close the viewer.") +
    term("terminal", """$ omarchy plymouth preview '#1d2021' '#ebdbb2' ~/Pictures/me.png ~/Pictures/boot-preview.png""") +
    p("Change the two colours until it looks right. Dark background, light text is the safe pair; the two above are the Gruvbox theme's."),
    p("<strong>Apply it.</strong> Same two colours, same photo, no output file. It asks for your password once, rebuilds the Plymouth theme and gives the SDDM login screen the same look.") +
    term("terminal", """$ omarchy plymouth set '#1d2021' '#ebdbb2' ~/Pictures/me.png
[sudo] password for kiet:"""),
    p("<strong>See it.</strong> The login screen shows it as soon as you log out: <kbd>Super</kbd>+<kbd>Space</kbd>, then <em>System › Logout</em>. The boot screen shows it on the next restart.") +
    term("terminal", """$ omarchy plymouth current"""),
    p("<strong>Back to normal</strong>, whenever you like. This restores the Omarchy logo and colours for both screens, and asks for your password again.") +
    term("terminal", """$ omarchy plymouth reset"""),
])

body = "\n".join([
    section("what", "What you are changing", what),
    section("generate", "Task 1 · your name on the screensaver", gen_text + generator),
    section("place", "Put it in place", place),
    section("without", "Without the browser", without),
    section("boot", "Task 2 · your photo on the boot and login screens", boot_intro + boot),
    section("credit", "Credits", p('Block letters from <a href="https://github.com/markcuda/Omarchy-Font">Omarchy Font</a> by Mark Cuda, MIT licence, embedded in this page so it works offline. Omarchy is by 37signals.')),
])

write("omarchy-branding.html", page("Make Omarchy yours", "omarchy-branding.html", body,
                                    sub="Day 2, on the Omarchy laptop. Task 1: your name in the wordmark's block letters on the screensaver. Task 2: your photo on the boot and login screens.",
                                    artifact="~/.config/omarchy/branding/screensaver.txt",
                                    stage_label="Day 2 · Omarchy customization",
                                    head_extra='<link rel="stylesheet" href="omarchy.css">\n<script src="omarchy.js" defer></script>\n'))
