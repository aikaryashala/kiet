# What Happens if I Modify a File After I've Already Committed It?

---

## First, Let Us Set the Scene

You have been working on your project.

You wrote some code. You saved it. You did your first commit:

```bash
git add .
git commit -m "first commit"
```

You feel good. You think — okay, Git has saved my work. Done.

Then you open the file again and make some changes.

Now you are confused —

> "Wait. I already committed this file. What happens now? Did Git automatically
> save my new changes? Is my old commit gone? Did I break something? What is
> happening?"

These are completely normal questions. Let us answer all of them clearly.

---

## The Most Important Thing to Understand First

**Git does NOT automatically track every change you make.**

This is the biggest misunderstanding beginners have.

Git does NOT work like that.

Git only saves a snapshot of your work **when YOU tell it to** — by running
`git add` and `git commit`.

Between your commits, you can change files as many times as you want — Git
watches but does NOT save automatically.

---

## So What Actually Happens When You Modify a File After Committing?

Here is the simple answer:

> **Your old commit stays exactly as it was. Your new changes are NOT saved yet.
> Git knows something changed, but it is waiting for you to tell it what to do.**

Your old commit is safe. Nothing is broken. Nothing is lost.

You just have new **uncommitted changes** sitting in your working area — waiting
to be committed.

---

## Understanding the Three Areas of Git

To fully understand this, you need to know that Git has **three areas** where
your files can exist at any point:

---

### Area 1 — Working Directory (Your Actual Files)

This is simply — your project folder on your computer.

The files you see, open, and edit in VS Code or any editor — those are in the
Working Directory.

When you modify a file after committing — **the change lives here first.**

---

### Area 2 — Staging Area (Also Called Index)

This is a middle zone — a preparation area.

Before Git saves a snapshot, you first tell Git — "these are the files I want
to include in my next commit." That act of telling Git is called **staging**.

You do this with:

```bash
git add filename
```

or

```bash
git add .
```
---

### Area 3 — Repository (Committed History)

This is where Git permanently stores your snapshots — your commits.

Once you run `git commit`, the staged changes move here and are saved forever in
Git's history.

Every commit has a unique ID, a message, a timestamp, and a record of exactly
what changed.

---

### The Flow — How Files Move Between Areas

```
Working Directory  →  (git add)  →  Staging Area  →  (git commit)  →  Repository
   (you edit here)                  (ready to save)                   (saved forever)
```

When you modify a file after committing — you are back in the **Working
Directory** with new changes. Those changes have NOT moved to Staging or
Repository yet.

---

## What Does git diff Show You?

Before you decide what to do, you can see exactly what changed using:

```bash
git diff
```

Output looks something like:

```diff
diff --git a/index.html b/index.html
index 1234567..abcdefg 100644
--- a/index.html
+++ b/index.html
@@ -1 +1,2 @@
 Hello, this is my website
+This is a new line I added
```

Reading this output:

- Lines starting with **`-`** (in red) = what was there before (old version)
- Lines starting with **`+`** (in green) = what is there now (new version)
- Lines with no symbol = unchanged lines (context)

This is very useful — you can review exactly what changed before deciding
whether to commit or discard.

---

## What if You Modified Multiple Files?

Same concept — just with more files.

Let us say you modified `index.html`, `style.css`, and `script.js` after your
last commit.

```bash
git status
```

Output:

```
Changes not staged for commit:
        modified:   index.html
        modified:   style.css
        modified:   script.js
```

Now you have options:

---

**Option 1 — Commit all changes together**

```bash
git add .
git commit -m "updated HTML, CSS and JS files"
```

---

**Option 2 — Commit only some files separately**

Maybe you want to commit the HTML and CSS changes as one commit, and the JS
changes as a separate commit:

```bash
# First commit — only HTML and CSS
git add index.html style.css
git commit -m "updated HTML and CSS layout"

# Second commit — only JS
git add script.js
git commit -m "fixed bug in script.js"
```

This gives you a cleaner, more organised history — each commit has a clear
purpose.

This is actually **good practice** — small, focused commits are much better than
one big commit with everything mixed together.

---

## The Cycle You Will Do Every Day as a Developer

Once you understand all of this, the pattern becomes very clear.

Development is just this cycle, repeated over and over:

```
1. Make changes to your files
         ↓
2. Check what changed → git status
         ↓
3. Review the changes → git diff
         ↓
4. Stage the changes → git add .
         ↓
5. Save a snapshot → git commit -m "message"
         ↓
6. Make more changes to your files
         ↓
   (repeat from Step 1)
```

Every time you finish a small meaningful piece of work — you commit. Then you
continue working. Then you commit again.

Your project history becomes a beautiful timeline of your progress.

---

## A Full Visual of What Git History Looks Like

Imagine you are building a website. Here is what your commit history might look
like after a few days of work:

```
Commit 1 — "initialised project with blank files"
     ↓
Commit 2 — "added basic HTML structure to index.html"
     ↓
Commit 3 — "added CSS styling for navbar"
     ↓
Commit 4 — "fixed navbar colour from blue to white"
     ↓
Commit 5 — "added hero section with heading and button"
     ↓
Commit 6 — "made website mobile responsive"
     ↓
Commit 7 — "added contact form to contact.html"
     ↓
     (you are here, working on the next change)
```

Every dot in this timeline is a safe point. At any moment, you can jump back to
any of these commits and see exactly how your project looked at that point.

This is the power of Git — your entire journey is saved.

---

## Quick Reference — Commands for This Situation

| Situation | Command |
|---|---|
| Check what has changed since last commit | `git status` |
| See the exact lines that changed | `git diff` |
| Stage all changed files | `git add .` |
| Stage one specific file | `git add filename` |
| Save a new commit | `git commit -m "your message"` |
| Throw away changes in a file (go back to last commit) | `git restore filename` |
| Fix the most recent commit message | `git commit --amend -m "new message"` |
| Add a forgotten file to the last commit | `git add file` then `git commit --amend --no-edit` |
| See full commit history | `git log` |
| See commit history in one line each | `git log --oneline` |

---

## Summary — Everything in One Paragraph

> When you modify a file after committing it, nothing bad happens. Your old
> commit stays exactly as it was — safe in Git history. Your new changes sit in
> the Working Directory as "uncommitted changes." Git notices the difference and
> shows it when you run `git status`. You then choose what to do — either stage
> and commit the new changes to create a new snapshot, or discard them with `git
> restore` to go back to the last committed version. This cycle of edit →
> status → add → commit is the heartbeat of working with Git. Every commit is a
> safe checkpoint in your project's journey, and the history of all your commits
> builds up over time into a complete timeline of your entire project.

---

## What is Next?

Now that you understand what happens when you modify a file after committing,
the next natural questions are:

- How does Git help me recover an older version of my project?
- What happens if two developers modify the same part of the same file?
- What is a branch and how does it help me work on new features safely?

Each of these builds directly on what you just learned. Keep going — you are
thinking like a developer now! 🚀
