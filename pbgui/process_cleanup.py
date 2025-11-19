import atexit
import logging
import signal
from threading import Lock
from typing import Optional

import psutil

_lock = Lock()
_cleanup_done = False
_registered = False
_previous_sigint = None
_previous_sigterm = None
_LOGGER = logging.getLogger("pbgui.process_cleanup")


def _terminate_children():
    """Terminate all child processes spawned by the current Streamlit run."""
    global _cleanup_done
    with _lock:
        if _cleanup_done:
            return
        _cleanup_done = True

    try:
        parent = psutil.Process()
        children = parent.children(recursive=True)
    except psutil.Error as exc:  # pragma: no cover - defensive
        _LOGGER.debug("Could not enumerate child processes: %s", exc)
        return

    if not children:
        return

    # Ask children to terminate gracefully first.
    for child in children:
        try:
            child.terminate()
        except psutil.Error:
            continue

    gone, alive = psutil.wait_procs(children, timeout=5)

    # Force kill any stubborn children still running.
    for child in alive:
        try:
            child.kill()
        except psutil.Error:
            continue

    if alive:
        _LOGGER.warning("Forced termination of %d lingering subprocesses.", len(alive))


def _forward_signal(previous_handler: Optional[object], signum, frame):
    if previous_handler in (signal.SIG_IGN, None):
        return
    if previous_handler == signal.SIG_DFL:
        raise KeyboardInterrupt
    if callable(previous_handler):
        previous_handler(signum, frame)


def _handle_signal(signum, frame):
    _terminate_children()
    if signum == signal.SIGINT:
        _forward_signal(_previous_sigint, signum, frame)
    elif signum == signal.SIGTERM:
        _forward_signal(_previous_sigterm, signum, frame)


def setup_process_cleanup():
    """Register signal and exit hooks once per interpreter session."""
    global _registered, _previous_sigint, _previous_sigterm
    with _lock:
        if _registered:
            return
        _registered = True

    atexit.register(_terminate_children)

    _previous_sigint = signal.getsignal(signal.SIGINT)
    try:
        signal.signal(signal.SIGINT, _handle_signal)
    except ValueError:
        _LOGGER.debug("SIGINT handler registration failed (likely non-main thread).")

    try:
        _previous_sigterm = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, _handle_signal)
    except (AttributeError, ValueError):
        # SIGTERM may not exist on some Windows environments
        _previous_sigterm = None
