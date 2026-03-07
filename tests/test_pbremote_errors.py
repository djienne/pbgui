from types import SimpleNamespace

import PBRemote as pbremote_module


class DummyLocalRun:
    pbgui_version = "n/a"
    pbgui_commit = None
    pb7_version = "n/a"
    pb6_version = "n/a"
    pb7_commit = None
    pb6_commit = None
    coindata = SimpleNamespace(credits_left=0)
    upgrades = 0
    reboot = False


class DummyMonitorConfig:
    mem_error_server = 100
    mem_warning_server = 200
    swap_error_server = 100
    swap_warning_server = 200
    disk_error_server = 100
    disk_warning_server = 200
    cpu_error_server = 80
    cpu_warning_server = 60
    mem_error_v7 = 100
    mem_warning_v7 = 80
    swap_error_v7 = 100
    swap_warning_v7 = 80
    cpu_error_v7 = 80
    cpu_warning_v7 = 60
    error_error_v7 = 1
    error_warning_v7 = 0
    traceback_error_v7 = 1
    traceback_warning_v7 = 0
    mem_error_multi = 100
    mem_warning_multi = 80
    swap_error_multi = 100
    swap_warning_multi = 80
    cpu_error_multi = 80
    cpu_warning_multi = 60
    error_error_multi = 1
    error_warning_multi = 0
    traceback_error_multi = 1
    traceback_warning_multi = 0
    mem_error_single = 100
    mem_warning_single = 80
    swap_error_single = 100
    swap_warning_single = 80
    cpu_error_single = 80
    cpu_warning_single = 60
    error_error_single = 1
    error_warning_single = 0
    traceback_error_single = 1
    traceback_warning_single = 0


def _patch_remote_runtime(monkeypatch):
    monkeypatch.setattr(pbremote_module, "PBRun", lambda: DummyLocalRun())
    monkeypatch.setattr(pbremote_module.PBRemote, "load_remote", lambda self: None)


def test_pbremote_init_sets_error_when_no_passivbot_dirs(temp_workspace, monkeypatch):
    _patch_remote_runtime(monkeypatch)
    (temp_workspace / "pbgui.ini").write_text("[main]\npbname=test\n", encoding="utf-8")

    remote = pbremote_module.PBRemote()

    assert remote.error == "No passivbot directory configured in pbgui.ini"


def test_pbremote_init_reports_missing_rclone(temp_workspace, monkeypatch):
    _patch_remote_runtime(monkeypatch)
    monkeypatch.setattr(pbremote_module.PBRemote, "is_rclone_installed", lambda self: False)
    (temp_workspace / "pbgui.ini").write_text("[main]\npbdir=C:/passivbot\n", encoding="utf-8")

    remote = pbremote_module.PBRemote()

    assert remote.error == "rclone not installed"


def test_pbremote_init_reports_missing_buckets(temp_workspace, monkeypatch):
    _patch_remote_runtime(monkeypatch)
    monkeypatch.setattr(pbremote_module.PBRemote, "is_rclone_installed", lambda self: True)
    monkeypatch.setattr(
        pbremote_module.PBRemote,
        "fetch_buckets",
        lambda self: setattr(self, "buckets", []),
    )
    (temp_workspace / "pbgui.ini").write_text("[main]\npbdir=C:/passivbot\n", encoding="utf-8")

    remote = pbremote_module.PBRemote()

    assert remote.error == "Rclone not configured. No buckets found."


def test_pbremote_init_reports_unconfigured_bucket(temp_workspace, monkeypatch):
    _patch_remote_runtime(monkeypatch)
    monkeypatch.setattr(pbremote_module.PBRemote, "is_rclone_installed", lambda self: True)
    monkeypatch.setattr(
        pbremote_module.PBRemote,
        "fetch_buckets",
        lambda self: setattr(self, "buckets", ["demo:"]),
    )
    (temp_workspace / "pbgui.ini").write_text("[main]\npbdir=C:/passivbot\n", encoding="utf-8")

    remote = pbremote_module.PBRemote()

    assert "bucket not configured" in remote.error


def test_pbremote_has_error_aggregates_offline_and_threshold_breaches(monkeypatch):
    monkeypatch.setattr(pbremote_module, "MonitorConfig", DummyMonitorConfig)

    remote = object.__new__(pbremote_module.PBRemote)
    offline_server = SimpleNamespace(
        name="offline",
        is_online=lambda: False,
        mem=[0, 0],
        swap=[0, 0, 0],
        disk=[0, 0, 0],
        cpu=0,
        monitor=[],
    )
    online_server = SimpleNamespace(
        name="busy",
        is_online=lambda: True,
        mem=[0, 50 * 1024 * 1024],
        swap=[0, 0, 50 * 1024 * 1024],
        disk=[0, 0, 50 * 1024 * 1024],
        cpu=90,
        monitor=[],
    )
    remote.remote_servers = [offline_server, online_server]

    errors = pbremote_module.PBRemote.has_error(remote)

    assert {error["server"] for error in errors} == {"offline", "busy"}


def test_pbremote_api_sync_is_disabled_by_default_and_cleans_staged_file(temp_workspace, monkeypatch):
    _patch_remote_runtime(monkeypatch)
    monkeypatch.setattr(pbremote_module.PBRemote, "is_rclone_installed", lambda self: True)
    monkeypatch.setattr(
        pbremote_module.PBRemote,
        "fetch_buckets",
        lambda self: setattr(self, "buckets", ["demo:"]),
    )
    (temp_workspace / "pbgui.ini").write_text(
        "[main]\npbdir=C:/passivbot\n[pbremote]\nbucket=demo:\n",
        encoding="utf-8",
    )
    staged_api = temp_workspace / "data" / "cmd" / "api-keys.json"
    staged_api.parent.mkdir(parents=True, exist_ok=True)
    staged_api.write_text("{}", encoding="utf-8")

    remote = pbremote_module.PBRemote()

    assert remote.sync_api_keys is False
    assert remote.check_if_api_synced() is True
    assert not staged_api.exists()
