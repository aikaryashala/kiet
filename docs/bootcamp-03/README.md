# bootcamp-03 — the online hub for KIET Bootcamp 3

Published at https://aikaryashala.com/kiet/bootcamp-03/. The bootcamp guide students use on the day lives in the
separate repository `aikaryashala/kiet-bootcamp-3` (hosted at https://aikaryashala.com/kiet-bootcamp-3/);
this folder holds only what is needed online: the hub page, the setup page and script, and the results.

## Pages

| File | What it is |
|---|---|
| `index.html` | The hub: preparation, Day 1 stages, Day 2, results, reference. Hand-written in the bootcamp-02 card style; edit it directly. |
| `setup.html` | The setup steps, written out. Hand-maintained; edit the HTML directly. |
| `scripts/setup.sh` | The one-line setup students run online: `curl -sSL https://aikaryashala.com/kiet/bootcamp-03/scripts/setup.sh \| bash` |
| `results.html` | Winning teams by prize, then every team. Reads `participants.csv` and `winners.csv`. |
| `rising-talent.html` | Individuals who stood out. Reads `rising-talent.csv` and looks the roll numbers up in `participants.csv`. |

The two results pages read their CSV files in the browser, so updating a CSV updates the page. They must be
served over http (GitHub Pages, or `python3 -m http.server` locally); opened as a file from disk the browser
blocks the read and the page says so.

## Data files

### `participants.csv` — everyone who took part

One row per student. Header, in this order:

```
ID,Type,HTNO,Student Name,Gender,Class ID,Team Name,Role,College,Program,Academic Batch
```

- `Team Name` groups members into teams on the results page. `HTNO` is the key the other files use.
- `Role` containing "lead" marks the team leader.
- `Class ID`, `College`, `Program`, `Academic Batch` appear under the team name. `ID`, `Type`, `Gender` are read but not shown.
- Header matching ignores case, spaces and underscores, so `team_name` or `Team` also work.
- An optional `Status` column (Completed / Not completed) adds completion badges; without it none are shown.

### `winners.csv` — the prizes

```
team,prize
KIET_3,1st prize
KIET_1,2nd prize
KIET_4,2nd prize
```

- `team` must match a `Team Name` in `participants.csv` (case-insensitive). Unmatched names are listed at the bottom of the page.
- Several teams may share a prize. Prizes are ordered by the number or word in the text ("1st", "2nd", "First"…).
- If the file is missing or empty the results page still lists every team, with "winners not announced yet".

### `rising-talent.csv` — individuals

```
HTNO,Note
25B21A4590,Built the frontend filter before it was asked for
25B21A4502,
```

- Only `HTNO` is required. `Note` is optional; when no row has one, the column shows class and program instead.
- Name, class and program come from `participants.csv`. A roll number not found there is still shown, tinted, so a typo is visible.
- Duplicated roll numbers are shown once.

## Generator

`build/` holds the Python scripts that produced the guide pages in `kiet-bootcamp-3/docs/` and `setup.html`
here. The HTML is the artifact; edit it directly, or edit the script and rerun it. See `build/README.md`.
`spec.md`, `plan.md` and `theme.md` are the design documents the build followed.
