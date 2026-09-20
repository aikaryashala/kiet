# What Does the mv Command Do?

---

In the terminal, both of these actions — **moving** and **renaming** — are done by **one single command.**

That command is **`mv`.**

---

## What Does mv Stand For?

**mv = Move**

But here is the interesting part that confuses many beginners —

> `mv` does not just move files. It also **renames** files and folders.

Why does one command do two things? Because in Linux, renaming is technically the same operation as moving — you are just changing the file's location or name (or both) in one step.

Once you understand this, `mv` becomes very simple.

---

## The Basic Syntax (Structure) of mv

```bash
mv source destination
```

- **source** = the file or folder you want to move or rename
- **destination** = where you want to move it, or what you want to rename it to

That is it. Two things after `mv` — where it is coming from, and where it is going.

---

## Part 1 — Using mv to RENAME a File

This is the simplest use of `mv`.

### Example — Renaming a File

Let us say you have a file called `notes.txt` and you want to rename it to `final_notes.txt`

```bash
mv notes.txt final_notes.txt
```

That is it. The file is now renamed.

Before:
```
notes.txt
```

After:
```
final_notes.txt
```

The content of the file stays exactly the same. Only the name changed.

---

### Example — Renaming a Folder

The same command works for folders too.

You have a folder called `my_stuff` and you want to rename it to `my_project`:

```bash
mv my_stuff my_project
```

Before:
```
my_stuff/
```

After:
```
my_project/
```

Everything inside the folder stays exactly as it was. Only the folder name changed.

---

## Part 2 — Using mv to MOVE a File to Another Folder

This is the second use of `mv` — actually moving a file from one place to another.

### Example — Moving a File Into a Folder

Let us say you have a file called `index.html` in your current folder.
You also have a folder called `my_website` in the same location.

You want to move `index.html` inside `my_website`:

```bash
mv index.html my_website/
```

Before:
```
index.html
my_website/
```

After:
```
my_website/
    index.html
```

The file `index.html` is now inside `my_website`. It no longer exists in the original location.

---

## Part 3 — Moving Multiple Files at Once

You can move more than one file at a time into a folder:

```bash
mv file1.txt file2.txt file3.txt my_folder/
```

This moves all three files into `my_folder` in one command.

**Important** — when moving multiple files, the last item must always be a **folder** (the destination). You cannot rename multiple files in one command.

---

### Important Point — You Can Accidentally Overwrite Files

```bash
mv file1.txt file2.txt
```

If `file2.txt` already exists — by default, `mv` will **silently overwrite it** with `file1.txt`

The original `file2.txt` is gone forever.

This is why using `mv -i` is a good habit — it will warn you before overwriting.

---

## Part 4 — mv vs cp — What is the Difference?

You will also hear about a command called `cp` (copy). Here is the simple difference:

| Command | What It Does | Original File |
|---|---|---|
| `mv` | Moves or renames a file | Original is GONE from source |
| `cp` | Copies a file | Original STAYS at source |

Think of it like:

- `mv` = **Cut and Paste** (file moves, original gone)
- `cp` = **Copy and Paste** (duplicate created, original stays)

---

## Full Workflow Example — Real Developer Situation

Let us say you are organising a website project. Here is how you would use `mv`:

```bash
# Step 1 — Check where you are
pwd
# Output: /home/yourname

# Step 2 — See what is there
ls
# Output: index.html   style.css   script.js   my_images   website_project

# Step 3 — Move files into the project folder
mv index.html website_project/
mv style.css website_project/
mv script.js website_project/

# Step 4 — Move and rename the images folder into project
mv my_images website_project/images

# Step 5 — Confirm everything is organised
ls website_project/
# Output: images   index.html   script.js   style.css

# Step 6 — Rename the project folder to something better
mv website_project portfolio_website

# Step 7 — Confirm the rename worked
ls
# Output: portfolio_website
```

Clean. Organised. All done with `mv`.

---

## Quick Reference Table

| Command | What It Does |
|---|---|
| `mv oldname.txt newname.txt` | Rename a file |
| `mv old_folder new_folder` | Rename a folder |
| `mv file.txt foldername/` | Move a file into a folder |
| `mv file.txt /full/path/file.txt` | Move file to a specific location |
| `mv file.txt /full/path/newname.txt` | Move AND rename at the same time |
| `mv file1.txt file2.txt folder/` | Move multiple files into a folder |
| `mv -i file.txt folder/` | Move but ask before overwriting |
| `mv -v file.txt folder/` | Move and show what is happening |
| `mv -n file.txt folder/` | Move but never overwrite existing files |

---

## Summary — Everything in One Paragraph

> `mv` stands for Move. It is a command that does two things — it moves files and folders from one location to another, and it renames files and folders. When you use `mv`, the original file disappears from its source location and appears only at the destination — it is like cut-paste, not copy-paste. You can move and rename at the same time by giving a new name at the destination. Always use `mv -i` to be safe, because by default `mv` will silently overwrite existing files without any warning, and there is no Recycle Bin in the Linux terminal to recover them.

---

## What is Next?

Now that you know `mv`, the next things to learn are:

- What is `sudo` and when do we use it?
- How do we create files from the terminal using `touch` and `nano`?
- How do we delete files using `rm`?
- How do all these commands work together in a real Git project?

You are building a strong foundation. Keep going! 💪
