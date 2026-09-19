# build/ — page generator (optional)

The HTML in `kiet-bootcamp-3/docs/` and the two hub pages here were produced by these scripts.
The HTML is the artifact and can be edited directly; keep these only if you want to regenerate.

    cd docs/bootcamp-03/build
    python3 reference.py          # docs/reference/*.html
    python3 stage0.py … stage8.py # docs/stageN.html
    python3 index.py troubleshooting.py
    python3 hub.py                # ../index.html and ../setup.html
    python3 gen_data.py           # data/*.sql (deterministic; only if the data must change)

`lib.py` holds the helpers (nav, page, terminal and code blocks, quiz, stepper). Paths assume the
student repo is checked out next to this one as `../kiet-bootcamp-3`.
