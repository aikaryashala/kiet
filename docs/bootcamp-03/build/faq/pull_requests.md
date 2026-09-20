# What is a Pull Request, and What is it Used For?

---

## First, Let Us Start With a Familiar Situation

Imagine you are a new intern at a company.

Your senior gives you a task — "Go and update the company website's homepage
text."

You go and do the work. You are done.

Now — do you directly go and change the live company website yourself?

Of course not.

You go to your senior and say:

> "I have made the changes. Can you please review them, check if everything
> looks correct, and if you are happy — then we will put it on the live
> website."

Your senior reviews your work. Maybe they suggest one small correction. You fix
it. They approve it. Then and only — the change goes live.

**This is exactly what a Pull Request is.**

A Pull Request is a way of saying to your team:

> "I have made some changes in my branch. I am requesting you to please review
> my work, give feedback, and if everything looks good — pull my changes into
> the main project."

That is it. That is the whole idea.

---

## But Wait — Why is it Called "Pull Request"?

The name confuses almost every beginner. Let us clear this up properly.

Remember from earlier — `git pull` means bringing changes from GitHub onto your
local computer.

A **Pull Request** is a **request to someone else to pull your changes** into
their branch — specifically into the `main` branch of the project.

You are not pulling anything yourself. You are **requesting** someone else to
pull your work into the main project after reviewing it.

So the full meaning is:

> **"I request you to pull my branch's changes into the main branch — after
> reviewing them."**

In some platforms like GitLab — it is called a **Merge Request** which is
actually a clearer name. But on GitHub, it is called a Pull Request. Both mean
the same thing.

---

## The Problem Pull Requests Solve

Let us think about what happens without Pull Requests.

Imagine a team of 5 developers all pushing directly to the `main` branch:

- Developer 1 pushes code — introduces a bug
- Developer 2 pushes code — has a typo in an important file
- Developer 3 pushes code — accidentally deletes a function that others need
- Developer 4 pushes code — overwrites Developer 1's fix

Nobody reviewed anything. Nobody caught the mistakes before they went into the
main project. The main branch is now broken. The live website is down.

Everyone is in panic.

This is a real situation that happens in teams without a proper review process.

**Pull Requests solve this by making code review a mandatory step before
anything goes into the main branch.**

No code goes into `main` without at least one other person reviewing and
approving it first.

---

## Understanding the Full Workflow — Step by Step

Let us walk through exactly how a Pull Request works in real life.

---

### Step 1 — You Create a Branch

You never work directly on `main`. You create your own branch for the feature
or fix you are working on:

```bash
git checkout -b feature/add-contact-page
```

This creates a new branch called `feature/add-contact-page` and switches you
to it.

Now you are working in your own safe space — completely separate from `main`.

---

### Step 2 — You Do Your Work and Commit

You write your code, make changes, and commit them on your branch:

```bash
git add .
git commit -m "added contact page with form"
git add .
git commit -m "added CSS styling for contact page"
git add .
git commit -m "added form validation in JavaScript"
```

You can have as many commits as you need on your branch.

---

### Step 3 — You Push Your Branch to GitHub

```bash
git push origin feature/add-contact-page
```

Now your branch — with all your commits — is on GitHub. But it is still
separate from `main`. The main project has not been touched at all.

---

### Step 4 — You Create a Pull Request on GitHub

Now you go to GitHub in your browser.

GitHub will usually show a yellow banner at the top saying:

> **"You recently pushed the branch `feature/add-contact-page`. Would you like
> to compare and create a pull request?"**

You click **"Compare and pull request"**

A form opens where you fill in:

- **Title** — A short clear title describing what you did
  (Example: "Added contact page with form validation")
- **Description** — A detailed explanation of what you changed, why you changed
  it, and anything the reviewer should know
- **Reviewers** — You select which teammates should review your code
- **Base branch** — Usually `main` (the branch you want to merge INTO)
- **Compare branch** — Your branch `feature/add-contact-page` (the branch with
  your changes)

Then you click **"Create Pull Request"**

---

### Step 5 — Your Teammates Review Your Code

The people you assigned as reviewers get a notification — on GitHub and usually
by email.

They go to the Pull Request page on GitHub and see:

- A clear list of all the files you changed
- Exactly which lines were added (shown in green) and removed (shown in red)
- All your commit messages
- Your description of what you did

They can:

- **Leave comments** on specific lines of code
- **Suggest changes** directly in the code
- **Approve** the Pull Request — meaning "looks good, ready to merge"
- **Request changes** — meaning "please fix these issues before I approve"

---

### Step 6 — You Make Changes Based on Feedback

If the reviewer requested changes — you go back to your local computer, make
the fixes, commit them, and push again:

```bash
git add .
git commit -m "fixed variable naming as per review feedback"
git push origin feature/add-contact-page
```

The new commits automatically appear in the same Pull Request on GitHub. The
reviewer can see your updates and review again.

This back-and-forth continues until the reviewer is satisfied.

---

### Step 7 — The Pull Request is Approved and Merged

Once the reviewer approves — either they or you click the **"Merge Pull
Request"** button on GitHub.

GitHub merges your branch into `main`.

Your contact page is now part of the main project. The branch can now be
deleted — its work is done.

---

### Step 8 — Everyone Pulls the Updated Main

Other team members now pull the latest `main` to get your merged changes:

```bash
git checkout main
git pull
```

Everyone is now up to date.

---

## Pull Requests for Open Source Projects

Pull Requests are not just for team projects. They are how the entire
open-source world works.

---

### Step 1 — Fork the Project

**Forking** means creating your own personal copy of someone else's repository.

You click the **Fork** button on their GitHub page.

Now you have your own copy at `github.com/yourname/their-project`

---

### Step 2 — Clone Your Fork and Make Changes

```bash
git clone github.com/yourname/their-project
cd their-project
git checkout -b fix/typo-in-readme
# make your changes
git add .
git commit -m "fixed typo in README introduction"
git push origin fix/typo-in-readme
```

---

### Step 3 — Create a Pull Request to Their Repository

On GitHub, you create a Pull Request from your fork to the original project's
`main` branch.

The project maintainers review your contribution. If they like it — they merge
it. Your code is now part of a project used by thousands of people.

This is how millions of developers contribute to projects like React, VS Code,
Python, and Linux — all through Pull Requests.

---

## A Full Visual of the Pull Request Workflow

```
main branch
    |
    |-- You create a new branch
    |         |
    |    feature/contact-page
    |         |
    |    You write code
    |    You commit changes
    |    You push to GitHub
    |         |
    |    You open a Pull Request
    |         |
    |    Reviewer reads your code
    |    Reviewer leaves comments
    |         |
    |    You make fixes based on feedback
    |    You push again
    |         |
    |    Reviewer approves
    |         |
    |    Pull Request is MERGED
    |         |
    +-- main branch now has your contact page
```

---

## Quick Reference — Pull Request Commands and Actions

| Action | Where it Happens | How |
|---|---|---|
| Create a branch | Terminal | `git checkout -b branch-name` |
| Commit your work | Terminal | `git add .` then `git commit -m "message"` |
| Push branch to GitHub | Terminal | `git push origin branch-name` |
| Create Pull Request | GitHub website | Click "Compare and pull request" button |
| Review someone's PR | GitHub website | Pull Requests tab → open PR → Files Changed |
| Leave a comment on a line | GitHub website | Click the + button on any line |
| Approve a PR | GitHub website | Review changes → Approve → Submit review |
| Merge a PR | GitHub website | Click "Merge pull request" button |
| Delete branch after merge | GitHub website | Click "Delete branch" button |
| Update local main after merge | Terminal | `git checkout main` then `git pull` |

---

## Summary — Everything in One Paragraph

> A Pull Request is a formal request on GitHub to merge your branch's changes
> into the main branch — but only after the team has reviewed and approved your
> work. You create a branch, do your work, commit, push to GitHub, and then open
> a Pull Request where you describe what you changed and why. Teammates are
> assigned as reviewers — they read your code line by line, leave comments,
> suggest improvements, and either approve or request changes. Once approved, the
> PR is merged into main and your work becomes part of the project. Pull Requests
> ensure that no broken, low-quality, or unreviewed code ever enters the main
> branch. They are also the backbone of open-source contribution — where anyone
> in the world can fork a project, make improvements, and submit a Pull Request
> to the original maintainers. Every professional software team in the world uses
> Pull Requests as the standard way to collaborate on code.

---

## What is Next?

Now that you fully understand Pull Requests — the next questions to explore are:

- How do we use GitHub to improve our developer profile?
- How do we build a complete website or project from scratch?
- How do we deploy a website so others can visit it?

You now understand the complete professional Git and GitHub workflow — branches,
commits, Pull Requests, code review, and merging. This is exactly how developers
work at every company in the world. You are well on your way! 🚀
