import signal

from pbgui import process_cleanup as cleanup_module


class DummyChild:
    def __init__(self):
        self.terminated = 0
        self.killed = 0

    def terminate(self):
        self.terminated += 1

    def kill(self):
        self.killed += 1


class DummyParent:
    def __init__(self, children):
        self._children = children

    def children(self, recursive=True):
        return self._children


def test_setup_process_cleanup_registers_only_once(monkeypatch):
    registered = []
    signal_calls = []

    monkeypatch.setattr(cleanup_module, "_registered", False)
    monkeypatch.setattr(cleanup_module, "_cleanup_done", False)
    monkeypatch.setattr(cleanup_module.atexit, "register", lambda fn: registered.append(fn))
    monkeypatch.setattr(cleanup_module.signal, "getsignal", lambda signum: signal.SIG_IGN)
    monkeypatch.setattr(cleanup_module.signal, "signal", lambda signum, handler: signal_calls.append(signum))

    cleanup_module.setup_process_cleanup()
    cleanup_module.setup_process_cleanup()

    assert len(registered) == 1
    assert signal_calls == [signal.SIGINT, signal.SIGTERM]


def test_terminate_children_terminates_then_kills_lingering_children(monkeypatch):
    child_gone = DummyChild()
    child_alive = DummyChild()

    monkeypatch.setattr(cleanup_module, "_cleanup_done", False)
    monkeypatch.setattr(cleanup_module.psutil, "Process", lambda: DummyParent([child_gone, child_alive]))
    monkeypatch.setattr(
        cleanup_module.psutil,
        "wait_procs",
        lambda children, timeout: ([child_gone], [child_alive]),
    )

    cleanup_module._terminate_children()

    assert child_gone.terminated == 1
    assert child_gone.killed == 0
    assert child_alive.terminated == 1
    assert child_alive.killed == 1
