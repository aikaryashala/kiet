# How Do I Build a Website or an App From Scratch — What Are the Actual Steps?

---

## First, Let Us Kill the Biggest Myth

Most beginners think building a website looks like this:

> "I will sit down, open my laptop, and magically start writing code until a
> beautiful website appears."

That is not how it works. Not for beginners. Not for experienced developers
either.

Every professional — whether they are building a simple portfolio page or a
full app like Swiggy — follows a **process**. A clear sequence of steps.

Without a process, you will:

- Start coding without knowing what you are building
- Get confused halfway through
- Rewrite everything from scratch three times
- Give up and say "this is too hard"

With a process, you will:

- Know exactly what to build before you write a single line of code
- Move forward step by step without getting lost
- Finish something you are actually proud of

This entire document is about giving you that process — in the most simple,
honest, practical way possible.

---

## The Two Types of Things You Can Build

Before we get into steps, let us be clear about what we are actually talking
about.

---

### Type 1 — A Website (Static)

A **static website** is a collection of pages that show information.

Examples:

- Your personal portfolio — "Hi, I am Rahul. Here are my projects."
- A college club website — "Welcome to the Photography Club. Here are our events."
- A restaurant menu page — "Here are our dishes and prices."

Static websites are built with three things:

- **HTML** — The structure and content (like the walls and rooms of a house)
- **CSS** — The styling and design (like the paint, furniture, and decoration)
- **JavaScript** — The behaviour and interactivity (like the lights, fans, and
  switches)

This is where every beginner should start. No database. No server. Just these
three files.

---

### Type 2 — A Web App (Dynamic)

A **web app** is a website that does something — it has logic, it saves data,
it changes based on who is using it.

Examples:

- A to-do list app — you add tasks, mark them done, delete them
- A login system — you create an account, log in, see your personal dashboard
- A weather app — it fetches real weather data and shows it to you

Web apps need more tools:

- **HTML + CSS + JavaScript** — Still the frontend (what the user sees)
- **A backend language** — Like Node.js, Python, or PHP (the server logic)
- **A database** — Like MySQL or MongoDB (where data is stored)

For a complete beginner — start with Type 1 (static website) first. Once you
are comfortable, move to Type 2. Do not try to run before you can walk.

---

## The 10 Steps to Build a Website From Scratch

These steps apply whether you are building a simple portfolio or a full web app.
The depth of each step changes — but the sequence stays the same.

---

## Step 1 — Decide WHAT You Are Building

This sounds obvious but most beginners skip this step entirely. They open VS
Code and start typing without a clear picture of what they want.

Before writing one line of code — answer these questions in writing:

**What is this website for?**

Examples:
- "This is my personal portfolio to show my projects to recruiters."
- "This is a website for my college fest with event schedule and registration."
- "This is a to-do list app where I can add, complete, and delete tasks."

**Who will use it?**

Examples:
- "Recruiters and HR managers who look at my profile."
- "College students looking for fest information."
- "Just me, for personal use."

**What pages or sections does it need?**

Examples for a portfolio:
- Home page — with my name, photo, and a short intro
- About section — who I am, my skills, my education
- Projects section — cards showing each project with a link
- Contact section — my email and social media links

**This planning document is the most important thing you will create before
coding.**

---

## Step 2 — Sketch a Rough Layout (Wireframe)

A **wireframe** is a simple rough sketch of how your website will look — like
a blueprint before a building is constructed.

You do NOT need fancy software for this. A pen and paper is perfect.

Draw boxes and labels. Like this:

```
+------------------------------------------+
|           NAVBAR — Logo | Home | About   |
+------------------------------------------+
|                                          |
|        BIG HEADING — "Hi, I am Rahul"   |
|        Short intro text here            |
|        [ See My Work ] button           |
|                                          |
+------------------------------------------+
|  ABOUT SECTION                           |
|  [ Photo ]   My story text here         |
|              Skills list here           |
+------------------------------------------+
|  PROJECTS SECTION                        |
|  [ Card 1 ]  [ Card 2 ]  [ Card 3 ]     |
+------------------------------------------+
|  CONTACT SECTION                         |
|  Email | GitHub | LinkedIn              |
+------------------------------------------+
|  FOOTER — Copyright 2026               |
+------------------------------------------+
```

This sketch takes 10 minutes. But it saves you hours of confusion later
because you can see the structure before you code it.

---

## Step 3 — Set Up Your Tools

Now you set up the tools you will use to actually build the website.

Here is what every beginner needs:

---

### Tool 1 — VS Code (Code Editor)

**VS Code** (Visual Studio Code) is where you write your code. It is free,
made by Microsoft, and used by developers all over the world.

Download from: [code.visualstudio.com](https://code.visualstudio.com)

Useful VS Code extensions to install:

- **Prettier** — automatically formats your code so it looks clean
- **Live Server** — opens your website in the browser and auto-refreshes every
  time you save a file (very useful)
- **GitLens** — helps you see Git history inside VS Code

---

### Tool 2 — A Browser

**Google Chrome** or **Mozilla Firefox** — for viewing and testing your website.

---

### Tool 3 — Git and GitHub

You already know these from our earlier topics. Set up Git on your machine and
create a GitHub account if you have not already.

Every project you build should go on GitHub from day one — not after you finish.

---

### Tool 4 — WSL Ubuntu Terminal

For running commands — which you already know how to use from our earlier
topics.

---

## Step 4 — Create Your Project Folder and Set Up Git

Now open your WSL Ubuntu terminal and create a proper project structure:

```bash
# Go to your home folder
cd ~

# Create a projects folder if you do not have one yet
mkdir projects
cd projects

# Create a folder for this specific project
mkdir my-portfolio
cd my-portfolio

# Initialise Git — start tracking this project
git init
```

Now create your basic files:

```bash
# Create the main HTML file
touch index.html

# Create a folder for styles
mkdir css
touch css/style.css

# Create a folder for JavaScript
mkdir js
touch js/script.js

# Create a folder for images
mkdir images
```

Your project structure now looks like this:

```
my-portfolio/
    index.html
    css/
        style.css
    js/
        script.js
    images/
```

This is the standard folder structure for a simple website. Every web
developer uses this same pattern.

Now open this folder in VS Code:

```bash
code .
```

The `.` means "open VS Code in the current folder." Your entire project
will appear in the VS Code sidebar.

---

## Step 5 — Write the HTML First (Structure)

HTML is always the first thing you write. Before any CSS or JavaScript.

HTML gives your page its structure — all the content, in the right order.

Open `index.html` in VS Code and type the code which you want by your basic structure:

Save the file. Right-click on `index.html` in VS Code and click
**"Open with Live Server"** — your website opens in the browser.

It looks plain right now — just text on a white background. That is perfectly
fine. Structure first. Design later.

---

## Step 6 — Add CSS (Design and Styling)

Now you make it look good.

Open `css/style.css` and start adding styles which you want to add to the correct structures:

Save and look at your browser — it should look much better now.

CSS is all about experimenting. Change colours, sizes, spacing — and see the
result instantly in the browser. Do not be afraid to break things. You can
always undo.

---

## Step 7 — Add JavaScript (Behaviour and Interactivity)

For a simple portfolio, you may not need much JavaScript. But let us add one
small thing — a smooth scroll effect and a simple active link highlight.

Open `js/script.js`:

and write the script like which the website/portfolio should be worked:

Save and test in the browser. Click the nav links — the page scrolls smoothly
to each section.

This is a small but real piece of JavaScript interactivity. As you learn more
JavaScript, you will add more powerful features.

---

## Step 8 — Commit Your Work Regularly to Git

As you build — commit your work in small pieces. Do not wait until the whole
website is done.

```bash
# After setting up the folder structure
git add .
git commit -m "initial project setup — folder structure and blank files"

# After writing the HTML
git add .
git commit -m "added complete HTML structure for portfolio"

# After adding CSS
git add .
git commit -m "added CSS styling for navbar, hero, and project card"

# After adding JavaScript
git add .
git commit -m "added smooth scroll and active nav link with JavaScript"
```

Each commit is a save point. If something breaks — you can always go back.

---

## Step 9 — Push to GitHub

Create a new repository on GitHub (github.com → New Repository → give it a
name → do not initialise with README since you already have files).

Then connect your local project to GitHub and push:

```bash
git remote add origin https://github.com/yourname/my-portfolio.git
git branch -M main
git push -u origin main
```

Your project is now on GitHub. Anyone with the link can see your code.

This is also your backup — even if your laptop crashes, your project is safe on
GitHub.

---

## Step 10 — Deploy — Make It Live on the Internet

Your website is built. It is on GitHub. But right now — only the code is
visible on GitHub. To make it a real website that anyone can visit with a link
— you need to **deploy** it.

The easiest and completely free way to deploy a simple static website is
**GitHub Pages**.

---

## Summary — Everything in One Paragraph

> To build a website from scratch — start by deciding clearly what you are
> building, who it is for, and what pages it needs. Sketch a rough wireframe on
> paper before touching the keyboard. Set up VS Code, Git, and your terminal.
> Create a proper project folder, initialise Git, and make your files. Write
> HTML first for structure, then CSS for design, then JavaScript for
> interactivity. Commit your work to Git in small pieces as you go. Push to
> GitHub to back up your code online. Finally, deploy on GitHub Pages to make
> your website live with a real URL anyone can visit. Learn in the right order —
> HTML and CSS first, then JavaScript, then React, then backend. Start with
> small projects, finish and deploy them, then move to the next level. The key
> is to build real things from day one, not just watch tutorials.

---

## What is Next?

Now that you know how to build a website — the next questions are:

- How do I deploy a website properly (beyond GitHub Pages)?
- How can I use GitHub to improve my developer profile?
- What beginner project should I actually build first?

You have the full roadmap now. The only thing left is to open VS Code and
start. One step at a time. 💪
