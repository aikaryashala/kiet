# What Do the Commands ls, pwd, cd, and mkdir Do, and When Would I Use Each One?

---

## First, Let Us Set the Scene

You have opened your **WSL Ubuntu** terminal.

You see a black screen with something like this:

```bash
yourname@DESKTOP:~$
```

And you are just staring at it. No icons. No folders. No mouse clicks. Nothing familiar.

Now what?

This is exactly where these four commands come in —
**`ls`, `pwd`, `cd`, and `mkdir`**

Let us understand each one — properly, from scratch.

---

## The Big Picture First — What Are We Even Doing Here?

When you use Windows normally, you navigate your computer like this:

- Open **File Explorer**
- See folders like Desktop, Downloads, Documents
- Double-click to go inside a folder
- See what files are inside
- Create a new folder by right-clicking

**In the terminal, you do all of these exact same things — but by typing commands.**

There is no File Explorer here. The terminal is your File Explorer.

These four commands are basically:

| Command | What It Replaces in File Explorer |
|---|---|
| `pwd` | The address bar at the top of File Explorer (shows where you are) |
| `ls` | The main window of File Explorer (shows what is inside) |
| `cd` | Double-clicking a folder to go inside it |
| `mkdir` | Right-click → New → Folder |

Now let us go deep into each one.

---

## Command 1 — `pwd`

### What Does pwd Stand For?

**pwd = Print Working Directory**

"Working Directory" means — the folder you are currently inside right now.
"Print" means — show it on the screen.

So `pwd` simply answers one question:

> **"Where am I right now?"**

---

### How to Use It

Just type `pwd` and press Enter:

```bash
pwd
```

Output will look something like:

```
/home/yourname
```

This is telling you — right now, you are inside the folder called `yourname`, which is inside the folder called `home`.

---

### When Would You Use pwd?

You will use `pwd` when:

- You opened the terminal and you are not sure which folder you are in
- You copied a path from somewhere and want to confirm you are in the right place
- You are about to run an important command and want to double-check your location first
- You get confused after moving between many folders

Think of it like looking at Google Maps to check **"where am I right now?"** before deciding where to go next.

---

## Command 2 — `ls`

### What Does ls Stand For?

**ls = List**

It lists all the files and folders inside the folder you are currently in.

So `ls` simply answers:

> **"What is inside here?"**

---

### How to Use It

Just type `ls` and press Enter:

```bash
ls
```

Output will look something like:

```
Desktop  Documents  Downloads  Music  Pictures  projects
```

These are all the folders and files inside your current location.

---

### Useful Variations of ls

`ls` has some extra options that make it more useful:

---

**`ls -l` — Long format (shows more details)**
**`ls -a` — Show hidden files also**
**`ls -la` — Long format AND hidden files**

---

### When Would You Use ls?

You will use `ls` when:

- You just opened the terminal and want to see what folders are available
- You moved into a folder and want to see what is inside
- You created a file and want to confirm it was actually created
- You want to check if a particular folder or file exists before doing something

---

## Command 3 — `cd`

### What Does cd Stand For?

**cd = Change Directory**

"Directory" is just another word for "folder."

So `cd` means — move from one folder to another.

`cd` answers the question:

> **"How do I go somewhere else?"**

---

### How to Use It — Basic

Example — if you want to go into a folder called `projects`:

```bash
cd projects
```
---

### Going Back — cd ..

Two dots `..` means "go back one folder" (go to the parent folder).

```bash
cd ..
```

If you were in `/home/yourname/projects`, after `cd ..` you will be in `/home/yourname`.

### Going Back Multiple Steps

```bash
cd ../..
```

This goes back two folders at once.

### Going Directly to Home Folder

```bash
cd ~
```

The `~` (called tilde) always means your home folder — `/home/yourname`.
---

### When Would You Use cd?

You will use `cd` when:

- You want to go inside a project folder to start working
- You want to navigate to a specific folder to run a command there
- You want to go back to the previous folder
- You want to return to your home folder quickly

`cd` is the command you will type **most often** out of all four. You will constantly be moving between folders as you work.

---

### Practice This Pattern

This is the most common pattern you will do every time you open the terminal:

```bash
pwd               # Check where I am
ls                # See what is available
cd projects       # Go into the projects folder
ls                # See what is inside projects
cd my_website     # Go into the specific project
pwd               # Confirm I am in the right place
```

Read this pattern a few times. You will do this dozens of times every day.

---

## Command 4 — `mkdir`

### What Does mkdir Stand For?

**mkdir = Make Directory**

"Make Directory" simply means — create a new folder.

`mkdir` answers:

> **"How do I create a new folder?"**

---

### How to Use It — Basic

Example — create a folder called `my_project`:

```bash
mkdir my_project
```

Now a new folder called `my_project` has been created in your current location.

You can verify by typing `ls` — you will see `my_project` listed there.

---

### Creating Multiple Folders at Once

```bash
mkdir folder1 folder2 folder3
```

This creates three folders in one command.

### Creating Nested Folders (Folder Inside Folder)

```bash
mkdir -p projects/my_website/css
```
---

### When Would You Use mkdir?

You will use `mkdir` when:

- You are starting a new project and need to create a project folder
- You want to organise your files into separate folders
- You are setting up a folder structure for a website (like separate folders for HTML, CSS, JavaScript)
- You are following a tutorial that asks you to create a folder

---

## Quick Reference Table

| Command | Full Form | What It Does | Simple Meaning |
|---|---|---|---|
| `pwd` | Print Working Directory | Shows your current folder location | "Where am I?" |
| `ls` | List | Shows files and folders in current location | "What is here?" |
| `ls -l` | List (long) | Shows detailed information | "What is here, with details?" |
| `ls -a` | List (all) | Shows hidden files too | "Show me everything, including hidden" |
| `cd foldername` | Change Directory | Move into a folder | "Take me inside this folder" |
| `cd ..` | Change Directory up | Go back one folder | "Take me back" |
| `cd ~` | Change Directory home | Go to home folder | "Take me home" |
| `mkdir foldername` | Make Directory | Create a new folder | "Create a new folder here" |
| `mkdir -p a/b/c` | Make Directory (parents) | Create nested folders | "Create all these folders at once" |

---

## Summary — Everything in One Paragraph

> `pwd` tells you which folder you are currently in — your location in the terminal. `ls` shows you all the files and folders inside your current location. `cd` moves you from one folder to another — forward into a folder, backward with `..`, or home with `~`. `mkdir` creates a brand new folder wherever you currently are. These four commands together are your complete navigation toolkit for the terminal. Every time you open Ubuntu, you will use some combination of these four commands before doing anything else.

---

## What is Next?

Now that you know your basic navigation commands, the next things to learn are:

- What does `sudo` mean and when do we need it?
- How do we create files (not just folders) from the terminal?
- How do we use these commands together with Git?

Keep practising these four commands every day — even if just for 10 minutes. Open Ubuntu, navigate around, create folders, check where you are. Repetition is the only teacher here. 🙌
