#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

AIK_BT_URL = "https://raw.githubusercontent.com/aikaryashala/practice/refs/heads/main/lldb/aik_bt.py"
AIK_RENDERER_URL = "https://raw.githubusercontent.com/aikaryashala/practice/refs/heads/main/lldb/aik_renderer.py"

def run(cmd, check=True):
    print(f"\n>>> {' '.join(cmd)}")
    return subprocess.run(cmd, check=check)

def have_cmd(cmd):
    from shutil import which
    return which(cmd) is not None

def ensure_line_in_file(file_path: Path, line: str):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if file_path.exists():
        existing = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        if line in existing:
            print(f"OK: Line already present in {file_path}")
            return
    else:
        existing = []

    # Append with newline safety
    with file_path.open("a", encoding="utf-8") as f:
        if existing and not file_path.read_text(encoding="utf-8", errors="ignore").endswith("\n"):
            f.write("\n")
        f.write(line + "\n")
    print(f"OK: Added line to {file_path}")

def download_to(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not have_cmd("curl"):
        print("ERROR: curl not found. Install it with: sudo apt install -y curl")
        sys.exit(1)

    run(["curl", "-fsSL", url, "-o", str(dest)], check=True)
    # Basic sanity check
    if not dest.exists() or dest.stat().st_size < 10:
        print(f"ERROR: Download seems failed or file too small: {dest}")
        sys.exit(1)
    print(f"OK: Downloaded {dest} ({dest.stat().st_size} bytes)")

def is_root():
    return os.geteuid() == 0

def apt_install(packages):
    # Use sudo if not root
    if is_root():
        run(["apt", "update"], check=True)
        run(["apt", "install", "-y"] + packages, check=True)
    else:
        if not have_cmd("sudo"):
            print("ERROR: sudo not found. Install sudo as root, or run this script as root.")
            sys.exit(1)
        run(["sudo", "apt", "update"], check=True)
        run(["sudo", "apt", "install", "-y"] + packages, check=True)

def setup_update_alternatives():
    # Make lldb-15 default if update-alternatives exists and lldb-15 exists
    if not have_cmd("update-alternatives"):
        print("NOTE: update-alternatives not found; skipping.")
        return

    lldb15 = Path("/usr/bin/lldb-15")
    if not lldb15.exists():
        print("NOTE: /usr/bin/lldb-15 not found; skipping update-alternatives step.")
        return

    if is_root():
        run(["update-alternatives", "--install", "/usr/bin/lldb", "lldb", "/usr/bin/lldb-15", "100"], check=False)
    else:
        run(["sudo", "update-alternatives", "--install", "/usr/bin/lldb", "lldb", "/usr/bin/lldb-15", "100"], check=False)

    print("OK: update-alternatives attempted (lldb -> lldb-15)")

def main():
    home = Path.home()
    lldb_dir = home / ".lldb"
    aik_bt_path = lldb_dir / "aik_bt.py"
    aik_renderer_path = lldb_dir / "aik_renderer.py"
    lldbinit_path = home / ".lldbinit"
    bashrc_path = home / ".bashrc"

    print("=== AIK BT (LLDB) Installer for Ubuntu ===")

    # 1) Install required packages
    print("\n[1/5] Installing LLDB + Python LLDB bindings (llvm-15)...")
    apt_install(["lldb-15", "python3-lldb-15", "curl"])

    # 2) Download scripts
    print("\n[2/5] Downloading aik_bt.py and aik_renderer.py to ~/.lldb/ ...")
    download_to(AIK_BT_URL, aik_bt_path)
    download_to(AIK_RENDERER_URL, aik_renderer_path)

    # 3) Configure ~/.lldbinit
    print("\n[3/5] Configuring ~/.lldbinit ...")
    import_line = f"command script import {aik_bt_path}"
    ensure_line_in_file(lldbinit_path, import_line)

    # 4) Make lldb-15 default (optional)
    print("\n[4/5] Setting lldb-15 as default (optional) ...")
    setup_update_alternatives()

    # 5) Add PYTHONPATH to ~/.bashrc
    print("\n[5/5] Adding PYTHONPATH to ~/.bashrc ...")
    py_line = 'export PYTHONPATH=/usr/lib/llvm-15/lib/python3.10/dist-packages:$PYTHONPATH'
    ensure_line_in_file(bashrc_path, py_line)

    print("\n=== DONE ===")
    print("Now run:")
    print("  source ~/.bashrc")
    print("  lldb")
    print("\nInside LLDB you should see:")
    print("  Loaded: aik bt")
    print("\nThen try:")
    print("  (lldb) aik bt")
    print("  (lldb) aik bt 5")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)
