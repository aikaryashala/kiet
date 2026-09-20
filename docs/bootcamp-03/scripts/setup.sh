#!/usr/bin/env bash
# setup.sh — KIET Bootcamp 3 (21–22 September 2026). Run once, with internet:
#
#     curl -sSL https://aikaryashala.com/kiet/bootcamp-03/scripts/setup.sh | bash
#
# What it does, in order:
#   1. installs git, curl and sqlite3 (asks for your password once, for sudo)
#   2. checks python3 is 3.12 or newer; on an older Ubuntu installs python3.12 (deadsnakes PPA)
#   3. clones https://github.com/aikaryashala/kiet-bootcamp-3 into ~/kiet-bootcamp-3
#      (or pulls the latest if it is already there)
#   4. runs ~/kiet-bootcamp-3/check_env.py
#   5. prints how to start the bootcamp guide
# Safe to run twice. Works on Ubuntu 24.04 and on Arch-based systems such as Omarchy.

set -u

REPO_URL="https://github.com/aikaryashala/kiet-bootcamp-3"
DEST="$HOME/kiet-bootcamp-3"

say()  { printf '\n==> %s\n' "$*"; }
fail() { printf '\nERROR: %s\n' "$*" >&2; exit 1; }

# ---- 1. packages ------------------------------------------------------------
OS_ID=""; OS_LIKE=""
if [ -r /etc/os-release ]; then
    . /etc/os-release
    OS_ID="${ID:-}"; OS_LIKE="${ID_LIKE:-}"
fi

say "Installing git, curl and sqlite3"
echo "    (sudo will ask for your password: installing packages needs it)"
case "$OS_ID $OS_LIKE" in
    *ubuntu*|*debian*)
        sudo apt-get update -qq
        sudo apt-get install -y -qq git curl sqlite3 python3 >/dev/null
        ;;
    *arch*)
        sudo pacman -Sy --needed --noconfirm git curl sqlite python >/dev/null
        ;;
    *)
        echo "    Unknown Linux ($OS_ID). Skipping package install."
        echo "    Make sure git, curl, sqlite3 and python3 (3.12+) are installed, then re-run."
        ;;
esac

# ---- 2. python --------------------------------------------------------------
# The bootcamp needs python3 3.12 or newer. Ubuntu 24.04 ships 3.12; Ubuntu 22.04 ships 3.10.
# On an older Ubuntu we install python3.12 from the deadsnakes PPA and put a `python3` link in
# ~/.local/bin, which comes first on PATH for the student's own shell. The system's /usr/bin/python3
# is left alone, so apt and other system tools keep working.
say "Checking python3"
py_ok() { "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>/dev/null; }
py_ver() { "$1" -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])' 2>/dev/null; }

export PATH="$HOME/.local/bin:$PATH"
if command -v python3 >/dev/null 2>&1 && py_ok python3; then
    echo "    python3 $(py_ver python3) — ok"
else
    echo "    python3 is $(py_ver python3 || echo missing); the bootcamp needs 3.12 or newer."
    case "$OS_ID $OS_LIKE" in
        *ubuntu*|*debian*)
            say "Installing python3.12 (from the deadsnakes PPA)"
            sudo apt-get install -y -qq software-properties-common >/dev/null
            sudo add-apt-repository -y ppa:deadsnakes/ppa >/dev/null 2>&1 || fail "could not add the deadsnakes PPA. Install python3.12 by hand and re-run."
            sudo apt-get update -qq
            sudo apt-get install -y -qq python3.12 >/dev/null || fail "could not install python3.12."
            mkdir -p "$HOME/.local/bin"
            ln -sf "$(command -v python3.12)" "$HOME/.local/bin/python3"
            if ! grep -q 'kiet-bootcamp-3: python3.12' "$HOME/.bashrc" 2>/dev/null; then
                printf '\n# kiet-bootcamp-3: python3.12 first on PATH\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.bashrc"
            fi
            hash -r
            py_ok python3 || fail "python3.12 was installed but python3 still runs $(py_ver python3). Open a new terminal and re-run this script."
            echo "    python3 is now $(py_ver python3) for your shell (/usr/bin/python3 is unchanged)"
            NEW_SHELL_NEEDED=1
            ;;
        *)
            fail "install python 3.12 or newer with your package manager, then re-run this script."
            ;;
    esac
fi

# ---- 3. clone or pull -------------------------------------------------------
if [ -d "$DEST/.git" ]; then
    say "Updating $DEST"
    git -C "$DEST" pull --ff-only || fail "git pull failed. Fix the repository in $DEST or delete it and re-run."
else
    say "Cloning into $DEST"
    git clone --depth 1 "$REPO_URL" "$DEST" || fail "git clone failed. Check your internet connection and try again."
fi

# ---- 4. check ---------------------------------------------------------------
say "Checking the machine"
python3 "$DEST/check_env.py"
STATUS=$?

# ---- 5. next steps ----------------------------------------------------------
if [ "$STATUS" -eq 0 ]; then
    say "Done. On the bootcamp day (no internet needed):"
else
    say "Something is not right — read the FAIL lines above, fix, and re-run this script. Then:"
fi
cat <<EOF

    python3 ~/kiet-bootcamp-3/check_env.py
    cd ~/kiet-bootcamp-3/docs && python3 -m http.server 8000

  and open  http://localhost:8000  in your browser.

EOF
if [ "${NEW_SHELL_NEEDED:-0}" = 1 ]; then
    echo "  python3.12 was installed for you. Close this terminal and open a new one before you start,"
    echo "  so that 'python3' means 3.12 in it. Then run the check above once more."
    echo
fi
exit "$STATUS"
