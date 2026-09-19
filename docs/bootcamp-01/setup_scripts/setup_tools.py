#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import sys
from typing import List, Optional, Tuple

# -----------------------------
# Your required packages/tools
# -----------------------------
PIP_PACKAGES = ["qrcode[pil]", "check50", "style50", "submit50"]

# Linux (Ubuntu/Debian) APT packages
APT_PACKAGES = [
    "sudo",
    "python3",
    "python3-venv",
    "python3-pip",
    "clang",
    "lldb",
    "micro",
    "asciinema",
    "zip",
    "unzip",
    "curl",
]

# macOS Homebrew packages (some tools already exist on macOS, but brew keeps it consistent)
BREW_PACKAGES = [
    "micro",
    "asciinema",
    "llvm",   # provides clang/llc/lldb; macOS also has Apple clang via Xcode tools
    "zip",
    "unzip",
    "curl",
]

# Windows winget package IDs (best-effort; availability can vary by machine)
WINGET_PACKAGES = [
    ("Micro Editor", "zyedidia.micro"),
    ("LLVM (clang/lldb)", "LLVM.LLVM"),
    ("cURL", "cURL.cURL"),
    ("zip/unzip", None),  # usually available via built-in tar; we just verify commands
]

# Where to put the venv:
# - Linux root: /opt/course-venv (shared)
# - Otherwise: ~/course-venv
def choose_venv_path() -> str:
    if is_linux() and is_root():
        return "/opt/course-venv"
    return os.path.join(os.path.expanduser("~"), "course-venv")


# -----------------------------
# Helpers
# -----------------------------
def run(cmd: List[str], check: bool = True, env: Optional[dict] = None) -> subprocess.CompletedProcess:
    print(f"\n==> {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, text=True, env=env)


def is_root() -> bool:
    return hasattr(os, "geteuid") and os.geteuid() == 0


def is_linux() -> bool:
    return platform.system().lower() == "linux"


def is_macos() -> bool:
    return platform.system().lower() == "darwin"


def is_windows() -> bool:
    return platform.system().lower() == "windows"


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def first_line(cmd: List[str]) -> str:
    if not have(cmd[0]):
        return "not available"
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT).strip()
        return out.splitlines()[0] if out else "unknown"
    except Exception:
        return "unknown"


def ensure_admin_linux() -> List[str]:
    """
    Returns prefix for privileged commands:
      - [] if root
      - ['sudo'] if sudo exists
    If sudo missing and not root -> exits with instructions.
    """
    if is_root():
        return []
    if have("sudo"):
        return ["sudo"]
    print("❌ sudo is not installed and you are not root.")
    print("   First run must be as root (or via provider console):")
    print("     python3 setup_tools.py")
    sys.exit(1)


# -----------------------------
# System installs per OS
# -----------------------------
def install_on_ubuntu() -> None:
    env = os.environ.copy()
    env["DEBIAN_FRONTEND"] = "noninteractive"

    prefix = ensure_admin_linux()

    # Important: If sudo is missing, we must be root; prefix would be [].
    run(prefix + ["apt-get", "update", "-y"], env=env)
    run(prefix + ["apt-get", "install", "-y", *APT_PACKAGES], env=env)

    # If we installed sudo just now and user reruns later as non-root, that's fine.


def install_on_macos() -> None:
    if not have("brew"):
        print("❌ Homebrew (brew) not found.")
        print("   Install Homebrew first, then rerun this script.")
        print("   Command (copy/paste in Terminal):")
        print('   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
        return

    run(["brew", "update"])
    # brew install is idempotent; it will skip installed packages
    run(["brew", "install", *BREW_PACKAGES])


def install_on_windows() -> None:
    if not have("winget"):
        print("❌ winget not found. Install 'App Installer' from Microsoft Store or use Windows 10/11 with winget enabled.")
        return

    # Micro, LLVM, curl are installable.
    # zip/unzip are usually covered by built-in tar; we only verify later.
    for name, pkg_id in WINGET_PACKAGES:
        if pkg_id is None:
            continue
        run(["winget", "install", "--id", pkg_id, "-e", "--accept-package-agreements", "--accept-source-agreements"], check=False)

    # asciinema note:
    print("\nℹ️ asciinema is not commonly available for native Windows.")
    print("   Best option: use WSL (Ubuntu) and install asciinema there.")


# -----------------------------
# Python venv + pip installs
# -----------------------------
def ensure_venv(venv_path: str) -> Tuple[str, str]:
    """
    Creates venv if missing and returns (python_bin, pip_bin)
    """
    if not os.path.isdir(venv_path):
        run([sys.executable, "-m", "venv", venv_path])

    if is_windows():
        python_bin = os.path.join(venv_path, "Scripts", "python.exe")
        pip_bin = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        python_bin = os.path.join(venv_path, "bin", "python")
        pip_bin = os.path.join(venv_path, "bin", "pip")

    run([python_bin, "-m", "pip", "install", "-U", "pip", "setuptools", "wheel"])
    return python_bin, pip_bin


def pip_install_in_venv(pip_bin: str) -> None:
    run([pip_bin, "install", "-U", *PIP_PACKAGES])


def symlink_cli_tools_linux_shared(venv_path: str) -> None:
    """
    On Linux when venv is /opt/course-venv, symlink check50/style50/submit50 to /usr/local/bin
    so all users can run them without activating venv.
    """
    if not is_linux():
        return
    if venv_path != "/opt/course-venv":
        return

    prefix = ensure_admin_linux()
    link_dir = "/usr/local/bin"
    tools = ["check50", "style50", "submit50"]

    for tool in tools:
        src = os.path.join(venv_path, "bin", tool)
        dst = os.path.join(link_dir, tool)
        if os.path.exists(src):
            # ln -sf src dst
            run(prefix + ["ln", "-sf", src, dst])
        else:
            print(f"⚠️ Tool not found in venv (skipping link): {src}")


# -----------------------------
# Version reporting
# -----------------------------
def print_versions(venv_python: str) -> None:
    print("\n" + "=" * 60)
    print("✅ Version check")
    print("=" * 60)

    # System commands
    checks = [
        ("python3", ["python3", "--version"]),
        ("pip3", ["pip3", "--version"]),
        ("clang", ["clang", "--version"]),
        ("lldb", ["lldb", "--version"]),
        ("micro", ["micro", "--version"]),
        ("asciinema", ["asciinema", "--version"]),
        ("curl", ["curl", "--version"]),
        ("zip", ["zip", "-v"]),
        ("unzip", ["unzip", "-v"]),
        ("sudo", ["sudo", "--version"]),
    ]

    for name, cmd in checks:
        # On Windows, many are different; we'll still attempt and show "not available" if missing
        print(f"{name}: {first_line(cmd)}")

    # Venv pip package versions
    print("\nPIP packages (inside venv):")
    # Note: qrcode[pil] dist name is "qrcode"
    dists = ["qrcode", "check50", "style50", "submit50"]
    for dist in dists:
        code = (
            "from importlib.metadata import version\n"
            f"print('{dist}=' + version('{dist}'))\n"
        )
        try:
            out = subprocess.check_output([venv_python, "-c", code], text=True).strip()
            print(out)
        except Exception:
            print(f"{dist}=not installed")

    print("\nDone.\n")


# -----------------------------
# Main
# -----------------------------
def main() -> None:
    print(f"==> Detected OS: {platform.system()} {platform.release()}")

    # 1) Install system tools depending on OS
    if is_linux():
        install_on_ubuntu()
    elif is_macos():
        install_on_macos()
    elif is_windows():
        install_on_windows()
    else:
        print("❌ Unsupported OS for automatic system installs.")
        return

    # 2) Create venv + install pip tools safely (avoids Ubuntu 24.04 PEP 668)
    venv_path = choose_venv_path()
    print(f"\n==> Using venv at: {venv_path}")
    venv_python, venv_pip = ensure_venv(venv_path)
    pip_install_in_venv(venv_pip)

    # 3) Optional: Linux shared symlinks (so users can run check50 etc without activating)
    symlink_cli_tools_linux_shared(venv_path)

    # 4) Version report
    print_versions(venv_python)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print("\n❌ Command failed:", e)
        sys.exit(e.returncode)
