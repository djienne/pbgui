import os
import sys
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path, PurePath
from time import sleep
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


def log_ts() -> str:
    """Return a human-readable timestamp for log lines."""
    return datetime.now().isoformat(sep=" ", timespec="seconds")


def rotate_log_if_needed(logfile: Path, max_size: int = 10_485_760):
    """Rotate log file if it exceeds max_size bytes. Returns True if rotated."""
    if logfile.exists() and logfile.stat().st_size >= max_size:
        logfile.replace(f'{logfile}.old')
        _log_out = open(logfile, "ab", 0)
        sys.stdout = TextIOWrapper(_log_out, encoding='utf-8', write_through=True)
        _log_err = open(logfile, "ab", 0)
        sys.stderr = TextIOWrapper(_log_err, encoding='utf-8', write_through=True)
        return True
    return False


class PidManager:
    """Mixin for PID file management. Subclass must set self.pidfile."""

    def _init_pid(self, piddir: Path, service_name: str):
        if not piddir.exists():
            piddir.mkdir(parents=True)
        self.pidfile = piddir / f'{service_name}.pid'
        self.my_pid = None

    def load_pid(self):
        if self.pidfile.exists():
            with open(self.pidfile, encoding='utf-8') as f:
                pid = f.read()
                self.my_pid = int(pid) if pid.isnumeric() else None

    def save_pid(self):
        self.my_pid = os.getpid()
        with open(self.pidfile, 'w', encoding='utf-8') as f:
            f.write(str(self.my_pid))


class ServiceBase(PidManager):
    """Base class for background services with run/stop/restart."""
    SERVICE_NAME: str = ""
    SCRIPT_NAME: str = ""
    PROCESS_SUFFIX: str = ""
    MAX_START_WAIT: int = 5

    def _init_service(self, pbgdir: str, piddir: Path, service_name: str):
        self._pbgdir = pbgdir
        self._init_pid(piddir, service_name)

    def run(self):
        if not self.is_running():
            cmd = [sys.executable, '-u', str(PurePath(f'{self._pbgdir}/{self.SCRIPT_NAME}'))]
            if platform.system() == "Windows":
                creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
                subprocess.Popen(cmd, stdout=None, stderr=None, cwd=self._pbgdir, text=True, creationflags=creationflags)
            else:
                subprocess.Popen(cmd, stdout=None, stderr=None, cwd=self._pbgdir, text=True, start_new_session=True)
            for _ in range(self.MAX_START_WAIT):
                sleep(1)
                if self.is_running():
                    return
            print(f'{log_ts()} Error: Can not start {self.SERVICE_NAME}')

    def stop(self):
        if self.is_running():
            print(f'{log_ts()} Stop: {self.SERVICE_NAME}')
            try:
                psutil.Process(self.my_pid).kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            if self.pidfile.exists():
                self.pidfile.unlink(missing_ok=True)

    def restart(self):
        if self.is_running():
            self.stop()
            self.run()

    def is_running(self):
        self.load_pid()
        try:
            if self.my_pid and psutil.pid_exists(self.my_pid) and any(
                sub.lower().endswith(self.PROCESS_SUFFIX) for sub in psutil.Process(self.my_pid).cmdline()
            ):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        return False


class QueueItemBase:
    """Base for backtest/optimize queue items with status tracking."""
    PROCESS_SCRIPT: str = ""
    COMPLETION_MARKER: str = ""

    def status(self, running_label="running", active_label=None):
        if active_label and hasattr(self, f'is_{active_label}'):
            checker = getattr(self, f'is_{active_label}')
            if checker():
                return f"{active_label}..."
        if self.is_running():
            return running_label
        if self.is_finish():
            return "complete"
        if self.is_error():
            return "error"
        return "not started"

    def is_running(self):
        if not self.pid:
            self.load_pid()
        try:
            if self.pid and psutil.pid_exists(self.pid):
                cmdline = safe_process_cmdline(psutil.Process(self.pid))
                if cmdline and any(self.PROCESS_SCRIPT in sub.lower() for sub in cmdline):
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        return False

    def is_finish(self):
        log = self._load_status_log()
        return bool(log and self.COMPLETION_MARKER in log)

    def is_error(self):
        log = self._load_status_log()
        return bool(log and self.COMPLETION_MARKER not in log)

    def _load_status_log(self):
        """Override or set self._status_log_size for custom log size."""
        size = getattr(self, '_status_log_size', None)
        if size:
            return self.load_log(log_size=size)
        return self.load_log()

    def load_pid(self):
        if self.pidfile.exists():
            with open(self.pidfile, encoding='utf-8') as f:
                pid = f.read()
                self.pid = int(pid) if pid.isnumeric() else None

    def save_pid(self):
        with open(self.pidfile, 'w', encoding='utf-8') as f:
            f.write(str(self.pid))
