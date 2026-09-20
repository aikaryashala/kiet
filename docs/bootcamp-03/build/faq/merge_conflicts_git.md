# What Happens if Two Developers Modify the Same Part of the Same File? How Does Git Handle That?

---

## First, Let Us Start With a Real Life Story

Imagine you and your classmate Ravi are working together on a college project.

You both have a copy of the same Word document — `project_report.docx`

You open the document and change the introduction paragraph.
At the same time, Ravi also opens the same document and changes the same
introduction paragraph — but writes something completely different.

Now you both try to save your versions.

Whose version do we keep?
Do we keep yours?
Do we keep Ravi's?
Do we somehow combine both?

If you were sharing a single file on Google Docs — Google would handle this
automatically, because only one file exists online and everyone edits the same
copy in real time.

But in Git — everyone works on their own **local copy** of the project. Changes
are only shared when someone pushes to GitHub. So it is very possible for two
people to change the same part of a file at the same time — without knowing the
other person also changed it.

When this happens — Git calls it a **MERGE CONFLICT.**

And this is exactly what we are going to understand today — completely, from
scratch.

---

## What is a Merge Conflict?

A **merge conflict** happens when:

1. Two people (or even you yourself on two branches) changed the **same lines**
   in the **same file**
2. Both changes were committed separately
3. Now Git is trying to combine (merge) those two versions
4. Git does not know which version to keep — so it **stops and asks you to
   decide**

Git is very smart — it can automatically combine most changes. But when two
people changed the **exact same lines** — Git genuinely cannot decide whose
version is correct. Only a human can make that call.

So Git marks the conflict clearly in the file and says:

> "I found a conflict here. You two figure it out. Tell me what the final
> version should look like and I will continue."

---

### The Setup — Two Developers, One Project

Let us say you and your friend Priya are both working on the same project that
is on GitHub.

Both of you cloned (downloaded) the project on Monday morning.

At that moment — both your laptops have the exact same code.

---

### What You Did

You opened `index.html` and changed line 5 from:

```html
<h1>Welcome to Our Website</h1>
```

to:

```html
<h1>Welcome to Our Amazing Portfolio</h1>
```

You committed this change:

```bash
git add index.html
git commit -m "updated heading to Amazing Portfolio"
```

---

### What Priya Did — At the Same Time

Priya also opened `index.html` and changed the same line 5 from:

```html
<h1>Welcome to Our Website</h1>
```

to:

```html
<h1>Welcome to Team Innovators</h1>
```

Priya committed her change:

```bash
git add index.html
git commit -m "updated heading to Team Innovators"
```

---

### Now the Conflict Happens

Priya pushes her changes to GitHub first:

```bash
git push
```

Priya's version is now on GitHub.

Now you try to push your changes:

```bash
git push
```

Git gives you an error:

```
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com/yourproject'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. Integrate the remote changes before pushing.
```

Git is saying — "Wait. Someone else already pushed changes to GitHub that you
do not have on your laptop. You need to get those changes first before you can
push yours."

So you do:

```bash
git pull
```

And THIS is when the conflict appears:

```
Auto-merging index.html
CONFLICT (content): Merge conflict in index.html
Automatic merge failed; fix conflicts and then commit the result.
```

Git tried to combine Priya's changes with your changes — but both of you changed
the same line. Git could not automatically decide which one to keep.

So it stopped. It modified the file to show you exactly where the conflict is.
And it is waiting for you to fix it.

---

## What Does the Conflicted File Actually Look Like?

This is the most important part to understand. Open `index.html` now and you
will see something like this:

```
<<<<<<< HEAD
<h1>Welcome to Our Amazing Portfolio</h1>
=======
<h1>Welcome to Team Innovators</h1>
>>>>>>> b2c3d4e (updated heading to Team Innovators)
```

Let us break down every single part of this:

---

### `<<<<<<< HEAD`

This marker means — **"Here starts YOUR version"** (the version on your local
machine, your current branch)

Everything between `<<<<<<< HEAD` and `=======` is **your change.**

```
<h1>Welcome to Our Amazing Portfolio</h1>
```

This is what YOU wrote.

---

### `=======`

This is the **dividing line** — it separates your version from the other
person's version.

---

### `>>>>>>> b2c3d4e (updated heading to Team Innovators)`

This marker means — **"Here ends the OTHER person's version"** (the version that
came from GitHub — Priya's commit)

Everything between `=======` and `>>>>>>> b2c3d4e` is **Priya's change.**

```
<h1>Welcome to Team Innovators</h1>
```

This is what Priya wrote.

---

### The Full Picture

```
<<<<<<< HEAD                              ← Your version starts here
<h1>Welcome to Our Amazing Portfolio</h1> ← Your change
=======                                   ← Dividing line
<h1>Welcome to Team Innovators</h1>       ← Priya's change
>>>>>>> b2c3d4e (Priya's commit)          ← Priya's version ends here
```

Git is showing you both versions side by side and saying:

> "Both of you changed this line. I do not know which one is right.
> You decide. Then clean up these markers and tell me the final version."

---

## How Do You Fix a Merge Conflict?

Now comes the part where YOU take over from Git.

Fixing a conflict has 3 steps:

---

### Step 1 — Open the Conflicted File and Decide

Open the file in your editor. Find all the conflict markers (`<<<<<<<`,
`=======`, `>>>>>>>`).

Now you have four choices for what the final version should look like:

---

**Choice A — Keep YOUR version only**

Delete Priya's version and all the markers. Keep only your line:

```html
<h1>Welcome to Our Amazing Portfolio</h1>
```

---

**Choice B — Keep PRIYA's version only**

Delete your version and all the markers. Keep only Priya's line:

```html
<h1>Welcome to Team Innovators</h1>
```

---

**Choice C — Keep BOTH versions (combine them)**

Sometimes both changes make sense together. You can keep both:

```html
<h1>Welcome to Our Amazing Portfolio — Team Innovators</h1>
```

Or arrange them differently — whatever makes sense for the project.

---

**Choice D — Write something completely new**

Sometimes neither version is right and you need a fresh version that considers
both people's ideas:

```html
<h1>Team Innovators — Building Amazing Things</h1>
```

---

### The Only Rule — Remove ALL the Conflict Markers

After you decide, the final file should have:

- ✅ The content you decided on
- ❌ NO `<<<<<<<` lines
- ❌ NO `=======` lines
- ❌ NO `>>>>>>>` lines

If you leave even one marker in the file — Git will not accept the commit and
your code will also have those ugly markers in it.

---

### Step 2 — Stage the Fixed File

After fixing the conflict in the file and saving it — tell Git you have resolved
it:

```bash
git add index.html
```

If there were conflicts in multiple files — fix all of them, then:

```bash
git add .
```

---

### Step 3 — Complete the Merge With a Commit

```bash
git commit -m "resolved merge conflict in index.html"
```

Git will create a special **merge commit** that combines both people's histories
together.

Now push to GitHub:

```bash
git push
```

Done. The conflict is resolved. Both your change and Priya's change are part of
the history — and the final agreed version is in the file.

---

## What if There Are Conflicts in Multiple Files?

Same process — just repeated for each file.

When you run `git pull` and there are conflicts in 3 files:

```
CONFLICT (content): Merge conflict in index.html
CONFLICT (content): Merge conflict in style.css
CONFLICT (content): Merge conflict in script.js
```

You need to:

1. Open `index.html` — fix conflict — save
2. Open `style.css` — fix conflict — save
3. Open `script.js` — fix conflict — save
4. `git add .`
5. `git commit -m "resolved all merge conflicts"`

Fix one file at a time. Do not rush. Read both versions carefully before
deciding.

---

## Using VS Code to Resolve Conflicts Easily

If you are using VS Code as your editor — it has a very helpful built-in tool
for resolving conflicts.

When you open a conflicted file in VS Code, it highlights the conflict and shows
you four clickable options right above the conflict markers:

```
Accept Current Change | Accept Incoming Change | Accept Both Changes | Compare Changes
```

- **Accept Current Change** — keeps your version (HEAD), removes Priya's
- **Accept Incoming Change** — keeps Priya's version, removes yours
- **Accept Both Changes** — keeps both versions one after the other
- **Compare Changes** — opens a side-by-side view of both versions

You just click the option you want — VS Code removes all the markers and applies
your choice automatically.

This is much easier than manually editing the markers in the file. Most
beginners find this very helpful when starting out.

---

## Quick Reference — All Commands for Conflicts

| Situation | Command |
|---|---|
| Get latest changes from GitHub | `git pull` |
| See which files have conflicts | `git status` |
| After fixing all conflicts — stage them | `git add .` |
| Complete the merge | `git commit -m "resolved conflict"` |
| Cancel the merge — go back to before | `git merge --abort` |
| See the conflict markers in a file | Open the file in any editor |
| Push after resolving | `git push` |

---

## Summary — Everything in One Paragraph

> A merge conflict happens when two developers change the same lines in the same
> file, commit their changes separately, and then try to combine (merge) those
> changes. Git is smart enough to automatically merge changes in different parts
> of a file — but when the exact same lines are changed by two people, Git
> cannot decide which version is correct, so it stops and marks the conflict
> inside the file using special markers — `<<<<<<<` for your version, `=======`
> as the divider, and `>>>>>>>` for the other person's version. You then open
> the file, read both versions, decide what the final version should look like,
> remove all the markers, save the file, run `git add` and `git commit`, and
> push. The conflict is resolved and both histories are merged together. Conflicts
> can be reduced by pulling before starting work every day, communicating with
> teammates, using branches, and dividing work clearly across different files.

---

## What is Next?

Now that you understand merge conflicts — the next things to learn are:

- What is a branch and how does it help avoid conflicts in a team?
- What is a pull request and how do teams review each other's code before
  merging?
- How do you use GitHub to improve your developer profile?

You now understand one of the most important and most feared concepts in Git.
And it is not scary at all once you understand what is actually happening.
Well done! 🎉
