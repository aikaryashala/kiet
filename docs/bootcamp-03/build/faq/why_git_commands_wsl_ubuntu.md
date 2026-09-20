# Why Do We Work With Git Through Commands in WSL Ubuntu?

---

## First, Let Us Understand What Is Happening Here

When you start learning Git, your teacher or tutorial will ask you to open something called **WSL Ubuntu** and start typing commands like:

```bash
git init
git add .
git commit -m "first commit"
```

And you are sitting there thinking —

> "Why are we typing all this? Can't we just click some buttons somewhere? What even is this black screen? Why Ubuntu? I have Windows!"

These are all very valid questions. Let us answer every single one of them, properly.

---

## Part 1 — What is This Black Screen We Are Typing In?

That black screen is called a **Terminal** (also called Command Line or Command Prompt or Shell).

It is a way to talk to your computer **using text commands** instead of clicking buttons.

Normally, you use your computer by:
- Clicking icons
- Opening folders by double-clicking
- Dragging and dropping files

But there is another way — you can **type instructions directly** to your computer, and it will obey those instructions immediately.

The terminal is that place where you type those instructions.

---

### Simple Example

Normally you would:
- Open File Explorer
- Navigate to a folder
- Right-click → New Folder
- Type the name

In the terminal, you just type:

```bash
mkdir my_project
```

And the folder is created. Done. Same result, but much faster.

---

## Part 2 — What is WSL?

**WSL = Windows Subsystem for Linux**

Here is the situation:

You have a **Windows laptop**. But most developers in the real world use a system called **Linux** for their work — because Linux is more powerful, more stable, and almost all servers in the world run on Linux.

Now, earlier, if you had Windows and you wanted to use Linux, you had to:
- Buy a separate computer
- Or delete Windows and install Linux
- Or use complicated virtual machines

Microsoft understood this problem. So they created **WSL** — a way to **run Linux directly inside Windows**, without any of that trouble.

So WSL is basically Microsoft saying:

> "We know developers need Linux. So we are putting Linux inside Windows itself. You do not have to do anything complicated. Just enable WSL and you have Linux running on your Windows machine."

---

## Part 3 — What is Ubuntu?

**Ubuntu** is one type (called a "distribution") of Linux.

Think of it like this:

- **Linux** is like a category — like "Soft Drinks"
- **Ubuntu** is a specific brand inside that category — like "Coca-Cola"

Other Linux distributions exist too — like Fedora, Debian, Kali Linux — but **Ubuntu is the most beginner-friendly** and most popular one, especially in India for learning purposes.

So when your teacher says "Open WSL Ubuntu" — they mean:

> "Open the Ubuntu Linux terminal that is running inside your Windows laptop through WSL."

---

## Part 4 — Why Do We Use Commands Instead of Clicking Buttons?

This is the most important question. Let us answer it properly.

---

### Reason 1 — Git Was Built for the Terminal

Git was created in **2005 by Linus Torvalds** (the same person who created Linux).

He built Git as a **command-line tool** — meaning, it was designed from the beginning to be used by typing commands in a terminal.

This is Git's natural home. This is where Git is most powerful and has all its features available.

GUI tools (graphical tools with buttons and clicks) for Git exist — like GitHub Desktop, GitKraken, Sourcetree — but they are built **on top of** the command line. They are just a visual wrapper around the same commands.

And those GUI tools do not have all the features. The terminal has everything.

---

### Reason 2 — Every Computer in the World Has a Terminal

Whether it is:
- Your Windows laptop
- A Mac
- A Linux server at Amazon or Google
- A cloud machine you are renting online

**Every single one of them has a terminal.**

Not every computer has GitHub Desktop installed. Not every computer has a graphical interface even.

But every computer understands terminal commands.

So once you learn Git through commands, **you can use it anywhere** — on any machine, in any company, in any country.

---

### Reason 3 — Commands Are Faster

Once you get comfortable, typing commands is **much faster** than clicking through menus.

Compare:

**GUI way:**
- Open GitHub Desktop
- Click "Repository" menu
- Click "Open in Terminal"
- Find the "Commit" button
- Type commit message
- Click "Commit to main"
- Click "Push origin"

**Command way:**
```bash
git add .
git commit -m "your message"
git push
```

Three lines. Done. Experienced developers do this in seconds.

---

### Reason 4 — You Understand What Is Actually Happening

When you click a button in a GUI tool, the tool does something behind the scenes — but you do not know what.

When you type a command yourself, you **know exactly what is happening**. You are in control. You understand the process.

This understanding is very important when something goes wrong — because in GUI tools, when there is an error, you have no idea what happened or how to fix it.

In the terminal, the error message tells you exactly what went wrong, and you can fix it.

---

### Reason 5 — Every Company Expects This

In any software job in India or abroad — at TCS, Infosys, Wipro, startups, product companies, or FAANG companies — developers use Git through the terminal every single day.

It is a basic skill that is expected. If you go for an interview and you only know how to use GitHub Desktop and click buttons, it will show that you are a beginner.

But if you can comfortably type Git commands, it shows confidence and real understanding.

---

## Part 5 — Why Specifically Ubuntu and Not Windows Command Prompt?

Good question. Windows has its own terminal too — called **Command Prompt** or **PowerShell**. So why are we using Ubuntu?

Here are the reasons:

---

### Reason 1 — Linux Commands Are the Industry Standard

In professional development, almost every tutorial, documentation, YouTube video, and course uses Linux-style commands.

When you Google "how to do X in Git", the answer will be a Linux command.

When your senior developer or your teacher tells you what to type, it will be a Linux command.

Windows Command Prompt uses **different syntax** for many things. So if you learn on Windows CMD, you will always have to "translate" — which is confusing.

Ubuntu gives you the **same commands** you will see everywhere in the industry.

---

### Reason 2 — Development Tools Work Better on Linux

Many development tools — Node.js, Python, Ruby, Docker, and many others — are built for Linux first.

On Linux (Ubuntu), installing and running these tools is smooth and simple.

On Windows CMD or PowerShell, you often run into permission errors, path issues, and compatibility problems.

WSL Ubuntu solves all of this — you get Linux's smoothness while still using your Windows laptop.

---

### Reason 3 — Real Servers Run Linux

As we mentioned before — web servers run Linux. If you develop on Ubuntu WSL, you are already working in an environment that is **similar to the real server** your project will eventually run on.

This reduces surprises when you deploy your project.

---

### Reason 4 — Ubuntu is Beginner Friendly

Among all Linux distributions, Ubuntu is the easiest to use and learn. It has the largest community, the most tutorials, and the best support for beginners.

That is why your teacher chose Ubuntu specifically.

---

## Part 6 — Some Basic Commands You Will Use Every Day

Here is a quick look at some basic terminal commands — just so the terminal does not feel scary:

| Command | What It Does | Example |
|---|---|---|
| `pwd` | Shows which folder you are currently in | `pwd` → `/home/yourname` |
| `ls` | Lists all files and folders in current location | `ls` |
| `cd` | Move into a folder | `cd Desktop` |
| `cd ..` | Go back one folder | `cd ..` |
| `mkdir` | Create a new folder | `mkdir my_project` |
| `clear` | Clears the terminal screen | `clear` |

And Git commands you will use:

| Git Command | What It Does |
|---|---|
| `git init` | Start tracking a project with Git |
| `git status` | Check what files have changed |
| `git add .` | Stage all changes for saving |
| `git commit -m "message"` | Save a snapshot with a description |
| `git push` | Send your work to GitHub |
| `git pull` | Get latest changes from GitHub |

Do not worry about memorising all of these right now. You will remember them naturally as you use them every day.

---

## Part 7 — Is the Terminal Scary?

Honestly — yes, it feels scary at first. That is completely normal.

When you first saw a computer, clicking a mouse also felt confusing. But now it is second nature.

The terminal is the same. In the beginning:
- Everything looks unfamiliar
- You will make mistakes
- Commands will give errors

That is okay. Every developer in the world went through this same phase.

With just 2-3 weeks of regular practice, the terminal will start feeling comfortable and even fast.

The secret is — **do not just read, keep typing**. Open Ubuntu, type the commands, make mistakes, see the errors, fix them. That is the only way to get comfortable.

---

## Summary — Everything in One Place

> **WSL** is a Microsoft feature that lets you run Linux inside your Windows laptop without any complicated setup. **Ubuntu** is the beginner-friendly version of Linux we use. We work with Git through the **terminal and commands** instead of clicking buttons because — Git was built for the terminal, every computer in the world has a terminal, servers only have terminals (no GUI), commands are faster once you learn them, you understand exactly what is happening, and every company in the real world expects developers to know this. Learning Git through Ubuntu WSL means you are learning the right way from the beginning — the same way professional developers all over the world work every day.

---

## What is Next?

Now that you know why we use the terminal and Ubuntu, the next steps are:

- What do the commands `ls`, `pwd`, `cd`, and `mkdir` do in detail?
- What does `sudo` mean and when do we use it?
- How do we actually use Git commands step by step in Ubuntu?

Let us keep building on this, one step at a time. You are learning the right things! 💪
