# What is sudo, and When Do I Actually Need It?

---

## First, Let Us Start With a Story

Imagine you are a new employee at a company.

You have your own desk, your own computer, your own files. You can do whatever
you want with your own stuff — open files, create documents, delete your own
notes. No problem.

But one day you need to install a new software on the office computer. You try
to install it and suddenly you get a message:

> **"You do not have permission to do this. Please contact your system
> administrator."**

You cannot install it yourself. Only the **system administrator** — the person
who manages the entire office computer system — has the power to install
software, change system settings, and touch files that affect everyone.

So you go to the administrator, explain what you need, they verify it is
legitimate, and then they do it for you — or they give you temporary permission
to do it yourself.

**This is exactly what `sudo` does in Linux.**

---

## So What is sudo?

**sudo = Superuser Do**

In simple words —

> `sudo` is a way to temporarily run a command **with administrator level
> powers** — even if you are a normal user.

The "superuser" in Linux is called **root**. The root user has complete and
total control over the entire system. Root can install software, delete system
files, change any setting, access any file — there are literally zero
restrictions for root.

When you type `sudo` before a command, you are saying:

> "Run this command as if I am the root (administrator) — give me full power
> just for this one command."

---

## Why Does Linux Have This System?

This is a very good question. Why not just give everyone full power all the
time?

Because **full power is dangerous.**

Imagine if every person in the office could install any software, delete any
file, change any system setting — without any check or verification. It would be
chaos. Someone could accidentally delete an important system file. Someone could
install a virus thinking it is a useful tool. Someone could change settings that
break the computer for everyone.

Linux protects against this by separating users into two types:

| Type | Who They Are | What They Can Do |
|---|---|---|
| **Normal User** | You, in everyday use | Manage your own files and folders only |
| **Root / Superuser** | The administrator | Everything — no restrictions at all |

`sudo` is the bridge between these two. It lets a normal user do ONE
administrator-level task at a time — after verifying with a password.

---

## How Does sudo Work — Step by Step

When you type a command with `sudo`:

```bash
sudo apt install git
```

Here is what happens:

1. Linux sees that you want to run something as administrator
2. Linux asks — **"What is your password?"**
3. You type your password (note — you will not see any letters or stars while
   typing, this is normal in Linux)
4. Linux checks — are you allowed to use sudo? (Not every user can use sudo —
   only users who are in the "sudo group")
5. If yes — the command runs with full administrator power
6. After the command finishes — you go back to being a normal user

The administrator power is only active **during that one command.** After it
finishes, you are a regular user again automatically.

---

## What Does the sudo Password Look Like While Typing?

This confuses almost every beginner.

When you type your password after `sudo`, the terminal shows **absolutely
nothing** — no letters, no stars, no dots. The cursor just sits there blinking.

```bash
sudo apt install git
[sudo] password for yourname:
```

You type your password here but nothing appears on screen.

This is **intentional** — Linux hides even the number of characters you are
typing, for security. Even someone looking over your shoulder cannot count how
many characters your password has.

Just type your password normally and press Enter. It is working even though you
cannot see anything.

---

## When Do You NOT Need sudo?

You do NOT need `sudo` for things inside your own home folder and your own
files.

```bash
mkdir my_project          # No sudo needed — your own folder
cd my_project             # No sudo needed — your own folder
git init                  # No sudo needed — working in your folder
git add .                 # No sudo needed — your own project
git commit -m "message"   # No sudo needed — your own project
mv file.txt Documents/    # No sudo needed — your own files
ls                        # No sudo needed — just looking
pwd                       # No sudo needed — just checking location
```

**Rule of thumb:**

> If you are working inside `/home/yourname/` — you almost never need `sudo`
>
> If you are installing software or touching folders outside your home — you
> probably need `sudo`

---

### The General Rule for sudo Safety

> **Never copy-paste a `sudo` command from the internet without understanding
> what it does.**

If someone online tells you to type a `sudo` command and you do not understand
what it does — Google it first. Ask someone you trust. Make sure you know what
will happen before you press Enter.

Many scammers and bad tutorials trick beginners into running dangerous `sudo`
commands by making them look helpful.

---

## What if You Get "Permission Denied"?

If you run a command and get this error:

```bash
Permission denied
```

or

```bash
bash: /path/to/file: Permission denied
```

This usually means you need `sudo`. Try adding `sudo` before your command:

```bash
sudo your_command_here
```

But first — think about WHY you are getting permission denied. If you are trying
to do something in your own home folder and getting permission denied, `sudo` is
probably not the right solution — there may be a different problem.

If you are trying to install software or modify system files — then yes, `sudo`
is exactly what you need.

---

## Quick Reference — When to Use sudo and When Not To

| Task | Need sudo? |
|---|---|
| Installing software with `apt install` | ✅ Yes |
| Updating system with `apt update` | ✅ Yes |
| Editing system config files in `/etc/` | ✅ Yes |
| Creating folders in system directories | ✅ Yes |
| Navigating folders with `cd`, `ls`, `pwd` | ❌ No |
| Creating folders in your home directory | ❌ No |
| Using Git commands | ❌ No |
| Renaming or moving your own files | ❌ No |
| Running your own scripts | ❌ Usually No |

---

## Summary — Everything in One Paragraph

> `sudo` stands for Superuser Do. It temporarily gives your normal user account
> the power of the root (administrator) user — just for one specific command.
> You need `sudo` when you are doing things that affect the whole system — like
> installing software, updating the system, or editing system configuration
> files. You do not need `sudo` for everyday things like navigating folders,
> working with your own files, or using Git in your own project. Always type
> your password carefully when `sudo` asks — even though nothing appears on
> screen while you type. And never run a `sudo` command you do not understand,
> especially ones from unknown sources on the internet, because `sudo` has the
> power to seriously damage or completely destroy your system.

---

## What is Next?

Now that you understand `sudo`, you have covered all the essential terminal
commands for a beginner. The next natural steps are:

- How do we create files from the terminal using `touch` and `nano`?
- How do we use all these commands together in a real Git workflow?
- What happens when you `git commit` and then modify the file again?

You are now comfortable with the terminal. That is a big milestone. Well done!
🎉
