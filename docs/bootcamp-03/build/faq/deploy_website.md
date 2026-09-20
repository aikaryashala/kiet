# How Do I Deploy a Website So That Other People Can Visit It?

---

## First, Let Us Understand the Problem

You have built your website.

It looks great on your laptop. You open it in Chrome, it works perfectly.
You are proud of it.

Then your friend asks — "Send me the link, I want to see it!"

And you realise — there is no link.

Your website only exists on YOUR laptop. Nobody else in the world can see it.

**Deployment** is the process of taking your website from your laptop and
putting it on the internet — so that anyone, anywhere in the world, can open
it in their browser just by visiting a link.

---

## What Actually Happens When Someone Visits a Website?

Before learning how to deploy, let us understand what is actually happening
when someone visits a website. This will make everything else make much more
sense.

---

### The Simple Explanation

When your friend types `www.yourwebsite.com` in their browser and presses
Enter — here is what happens:

```
1. Their browser asks the internet —
   "Where is the computer that has yourwebsite.com?"

2. The internet looks up the address and replies —
   "It is at IP address 203.0.113.42"

3. Their browser sends a request to that computer —
   "Hey, can you send me the files for yourwebsite.com?"

4. That computer (called a SERVER) receives the request
   and sends back the HTML, CSS, and JavaScript files

5. Their browser receives those files and displays
   your website on their screen
```

So for your website to be accessible to others — it needs to live on a
**server** — a computer that is:

- Connected to the internet at all times
- Has a fixed address (IP address) on the internet
- Can receive requests and send files back

Your laptop is not a server. It is not always on. It does not have a fixed
internet address. It cannot receive requests from strangers.

**Deployment = Putting your website files on a server.**

---

## What is a Domain Name?

A **domain name** is the human-readable address of your website.

Example: `www.google.com`, `www.flipkart.com`, `rahulportfolio.com`

Nobody wants to type `203.0.113.42` to visit a website. So domain names were
created — they are easy-to-remember names that point to the server's IP address.

For most beginner projects — free platforms give you a sub-domain automatically.

Example: `yourname.github.io/my-portfolio`

Here — `github.io` is GitHub's domain, and `yourname.github.io` is your
sub-domain that GitHub gives you for free.

When you are ready to build something more serious — you can buy your own custom
domain name for about ₹500 to ₹1,000 per year from providers like GoDaddy,
Namecheap, or Google Domains.

---

## The Different Ways to Deploy a Website

There are many ways to deploy depending on what kind of website you have built.

---

## Method 1 — GitHub Pages (Free — Best for Beginners)

**Best for:** Simple static websites — portfolios, project pages, club websites,
personal blogs

**Cost:** Completely free

**Difficulty:** Very easy

**Live URL you get:** `https://yourname.github.io/project-name`

---

### What is GitHub Pages?

GitHub Pages is a free service by GitHub that turns your GitHub repository
directly into a live website.

You push your code to GitHub. GitHub reads your files. GitHub serves them as a
website. Done.

No server setup. No payment. No complicated configuration.

---

### Step-by-Step — How to Deploy With GitHub Pages

**Step 1 — Make sure your project is on GitHub**

Your project must already be pushed to a GitHub repository. If it is not — do
git push to the repository first:

---

**Step 2 — Go to your repository on GitHub**

Open `github.com` in your browser. Log in. Go to your repository.

---

**Step 3 — Click Settings**

At the top of your repository, you will see tabs — Code, Issues, Pull requests,
Settings. Click **Settings**.

---

**Step 4 — Click Pages in the left sidebar**

Scroll down the left sidebar until you see **Pages**. Click it.

---

**Step 5 — Set the Source**

Under "Build and deployment" — set Source to **Deploy from a branch**

Under Branch — select **main** and folder **/ (root)**

Click **Save**.

---

**Step 6 — Wait 1 to 2 Minutes**

GitHub is now building your website. Refresh the page after a minute.

You will see a box saying:

```
Your site is live at https://yourname.github.io/my-portfolio/
```

---

**Step 7 — Visit Your Live Website**

Click that link. Your website is now live on the internet.

Share this link with anyone — they can open it on their phone, laptop, anywhere
in the world.

---

### Updating Your Website After Deployment

Every time you make changes and push to GitHub — GitHub Pages automatically
updates your live website within a minute or two.

```bash
# Make changes to your files
# Then:
git add .
git commit -m "updated about section"
git push
```

That is it. No re-deployment needed. Push and it updates automatically.

---

## Method 2 — Netlify (Free — Very Popular, Very Easy)

**Best for:** Static websites — same as GitHub Pages but with more features

**Cost:** Free tier is very generous

**Difficulty:** Very easy

**Live URL you get:** `https://your-chosen-name.netlify.app`

---

### What is Netlify?

Netlify is a platform built specifically for deploying websites. It is loved
by developers worldwide because it is:

- Very simple to use
- Has a drag-and-drop option (no commands needed)
- Automatically deploys every time you push to GitHub
- Gives you a free SSL certificate (the `https://` security that browsers require)
- Allows custom domain names for free

---

### Deploy on Netlify

---

#### Way B — Connect to GitHub (Better for Long-Term Projects)

This is the professional way. Every time you push to GitHub — Netlify
automatically re-deploys your website.

**Step 1** — Go to Netlify → Add new site → Import an existing project

**Step 2** — Choose **GitHub**

**Step 3** — Authorise Netlify to access your GitHub account

**Step 4** — Select the repository you want to deploy

**Step 5** — Netlify shows build settings. For a simple HTML website — leave
everything as default and click **Deploy site**

**Step 6** — Netlify builds and deploys. You get a live URL in about 30 seconds.

From now on — every `git push` automatically updates your live website. You
never have to manually deploy again.

---

## Method 3 — Vercel (Free — Best for React and Next.js Projects)

**Best for:** React apps, Next.js projects, modern JavaScript frameworks

**Cost:** Free tier available

**Difficulty:** Easy

**Live URL you get:** `https://your-project.vercel.app`

---

### What is Vercel?

Vercel is made by the same team that created Next.js (a popular React framework).
It is the go-to platform for deploying React applications.

If you build a React project — deploy it on Vercel. It handles all the build
steps automatically.

---

### How to Deploy on Vercel

**Step 1** — Go to [vercel.com](https://vercel.com) and sign up with your
GitHub account

**Step 2** — Click **Add New Project**

**Step 3** — Import your GitHub repository

**Step 4** — Vercel automatically detects if it is a React, Next.js, or plain
HTML project and sets the right build settings

**Step 5** — Click **Deploy**

Your project is live in about 1 minute at `https://yourproject.vercel.app`

Just like Netlify — every push to GitHub automatically re-deploys.

---

## Understanding SSL — Why Your Website Must Have https://

You will notice all the URLs above start with `https://` not `http://`.

The **S** in https stands for **Secure**.

- `http://` — data between the browser and server is not encrypted. Anyone in
  the middle can read it.
- `https://` — data is encrypted. Safe and secure.

Browsers like Chrome show a **"Not Secure"** warning for websites that use
`http://`. This scares visitors away.

All the platforms we mentioned — GitHub Pages, Netlify, Vercel, Render — give
you a free **SSL certificate** automatically. Your website will always be
`https://` without you doing anything extra.

When you buy a custom domain and use a different hosting service — getting SSL
set up is one of the first things you do.

---

## Buying a Custom Domain (Optional But Professional)

The free URLs you get from these platforms look like:

```
yourname.github.io/portfolio
yourname.netlify.app
yourproject.vercel.app
```

These are fine for learning and student projects. But when you want to look
professional — especially for a portfolio — a custom domain looks much better:

```
rahulkumar.dev
rahulbuilds.in
rahulcodes.com
```

---

### How to Buy a Domain

Go to any domain registrar:

- [GoDaddy.com](https://godaddy.com)
- [Namecheap.com](https://namecheap.com)
- [Google Domains](https://domains.google)
- [BigRock.in](https://bigrock.in) — popular in India

Search for the name you want. If it is available — buy it.

**Price:** `.com` domains cost around ₹800 to ₹1,500 per year.
`.in` domains cost around ₹500 to ₹800 per year.
`.dev` domains cost around ₹1,000 to ₹1,500 per year.

---

### Connecting Your Custom Domain to Netlify or GitHub Pages

Once you buy a domain — you connect it to your deployed website.

**For Netlify:**

Step 1 — Go to your site settings in Netlify → Domain management

Step 2 — Click **Add custom domain**

Step 3 — Type your domain name (example: `rahulkumar.dev`) → Click **Verify**

Step 4 — Netlify shows you the DNS settings to add

Step 5 — Go to your domain registrar (GoDaddy, Namecheap etc.) → Find DNS
settings → Add the records Netlify gave you

Step 6 — Wait 15 minutes to a few hours for DNS to update globally

Step 7 — Your custom domain now shows your Netlify website.
`https://rahulkumar.dev` is live.

---

## Quick Reference — All Platforms at a Glance

| Platform | Best For | Cost | URL Given |
|---|---|---|---|
| **GitHub Pages** | Static HTML/CSS/JS sites | Free | `yourname.github.io/project` |
| **Netlify** | Static sites, more features | Free tier | `project.netlify.app` |
| **Vercel** | React, Next.js projects | Free tier | `project.vercel.app` |
| **Render** | Node.js, Python backends | Free tier | `project.onrender.com` |
| **Railway** | Full stack with database | Free credits | `project.railway.app` |

---

## Summary — Everything in One Paragraph

> Deployment means taking your website from your laptop and putting it on a
> server so anyone on the internet can visit it with a link. For simple static
> websites built with HTML, CSS, and JavaScript — use GitHub Pages (simplest,
> completely free, just change one setting in your repository) or Netlify (free,
> drag-and-drop option, more features). For React or Next.js projects — use
> Vercel. For Node.js or Python backends — use Render. For full-stack projects
> with a database — use Railway or Render. All these platforms give you a free
> URL and a free SSL certificate (https) automatically. Every time you push new
> code to GitHub — these platforms automatically update your live website. For a
> more professional look — buy a custom domain name for around ₹800 to ₹1,500
> per year and connect it to your deployment platform. Always use lowercase file
> names, relative paths, and never push passwords or API keys to GitHub.

---

## What is Next?

Now that you know how to deploy a website — the next questions to explore are:

- How can I use GitHub to improve my developer profile and get noticed by
  recruiters?
- What beginner projects should I actually build and deploy?
- How do I distinguish between genuinely understanding AI vs just using AI
  tools?

You now know the complete journey — plan, build, commit, push, deploy, share.
That is the full cycle of a real developer. Go build something and put it out
there for the world to see! 🚀
