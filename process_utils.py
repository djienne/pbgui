from pathlib import Path
import platform
import subprocess

import psutil


def safe_process_cmdline(process: psutil.Process):
    try:
        return process.cmdline()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


def launch_logged_process(cmd, cwd, logfile, mode="a"):
    logfile = Path(logfile)
    logfile.parent.mkdir(parents=True, exist_ok=True)
    with logfile.open(mode, encoding="utf-8") as log:
        kwargs = {
            "stdout": log,
            "stderr": log,
            "cwd": cwd,
            "text": True,
        }
        if platform.system() == "Windows":
            creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
            kwargs["creationflags"] = creationflags
        else:
            kwargs["start_new_session"] = True
        return subprocess.Popen(cmd, **kwargs)


def run_logged_command(cmd, cwd, logfile, mode="a"):
    logfile = Path(logfile)
    logfile.parent.mkdir(parents=True, exist_ok=True)
    with logfile.open(mode, encoding="utf-8") as log:
        kwargs = {
            "stdout": log,
            "stderr": log,
            "cwd": cwd,
            "text": True,
        }
        if platform.system() == "Windows":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        return subprocess.run(cmd, **kwargs)
