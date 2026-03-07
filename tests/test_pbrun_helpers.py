from datetime import date as real_date
from datetime import datetime as real_datetime

import PBRun as pbrun_module


class FixedDate(real_date):
    @classmethod
    def today(cls):
        return cls(2026, 3, 7)


class FixedDateTime(real_datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 3, 7, 12, 0, 0)


def test_extract_flag_value_handles_missing_and_valid_flags():
    assert pbrun_module.extract_flag_value("-lm n -lw 0.5", "-lm") == "n"
    assert pbrun_module.extract_flag_value("-lm n -lw 0.5", "-lw") == "0.5"
    assert pbrun_module.extract_flag_value("-lm n -lw 0.5", "-x") == ""
    assert pbrun_module.extract_flag_value("-lm", "-lm") == ""


def test_clean_log_file_rotates_and_truncates(monkeypatch, temp_workspace):
    monkeypatch.setattr(pbrun_module, "FILE_SIZE_10MB", 5)
    log_file = temp_workspace / "passivbot.log"
    log_file.write_text("123456789", encoding="utf-8")

    pbrun_module.clean_log_file(str(temp_workspace))

    assert log_file.read_text(encoding="utf-8") == ""
    assert (temp_workspace / "passivbot.log.old").read_text(encoding="utf-8") == "123456789"


def test_monitor_watch_log_tracks_today_errors_tracebacks_and_pnl(monkeypatch, temp_workspace):
    monkeypatch.setattr(pbrun_module, "date", FixedDate)
    monkeypatch.setattr(pbrun_module, "datetime", FixedDateTime)

    log_file = temp_workspace / "passivbot.log"
    log_file.write_text(
        "\n".join(
            [
                "2026-03-07T10:00:00 INFO balance 10 -> 12",
                "Traceback (most recent call last):",
                "ValueError: boom",
                "2026-03-07T10:01:00 ERROR broken",
            ]
        ),
        encoding="utf-8",
    )

    monitor = pbrun_module.Monitor()
    monitor.path = str(temp_workspace)
    monitor.user = "alice"
    monitor.version = "s"
    monitor.pb_version = "6"
    monitor.watch_log()

    assert monitor.infos_today == 1
    assert monitor.errors_today == 1
    assert monitor.tracebacks_today == 1
    assert monitor.pnl_today == 2.0
    assert monitor.pnl_counter_today == 1


def test_monitor_watch_log_rolls_daily_counters_forward(monkeypatch, temp_workspace):
    monkeypatch.setattr(pbrun_module, "date", FixedDate)
    monkeypatch.setattr(pbrun_module, "datetime", FixedDateTime)

    (temp_workspace / "passivbot.log").write_text(
        "2026-03-07T11:00:00 INFO balance 5 -> 7",
        encoding="utf-8",
    )

    monitor = pbrun_module.Monitor()
    monitor.path = str(temp_workspace)
    monitor.user = "alice"
    monitor.version = "s"
    monitor.pb_version = "6"
    monitor.log_watch_ts = int(real_datetime(2026, 3, 6, 23, 0, 0).timestamp())
    monitor.errors_today = 2
    monitor.infos_today = 3
    monitor.tracebacks_today = 4
    monitor.pnl_today = 5.5
    monitor.pnl_counter_today = 6
    monitor.watch_log()

    assert monitor.errors_yesterday == 2
    assert monitor.infos_yesterday == 3
    assert monitor.tracebacks_yesterday == 4
    assert monitor.pnl_yesterday == 5.5
    assert monitor.pnl_counter_yesterday == 6
    assert monitor.infos_today == 1
    assert monitor.pnl_today == 2.0


def test_monitor_watch_log_recovers_after_log_truncation(monkeypatch, temp_workspace):
    monkeypatch.setattr(pbrun_module, "date", FixedDate)
    monkeypatch.setattr(pbrun_module, "datetime", FixedDateTime)

    log_file = temp_workspace / "passivbot.log"
    log_file.write_text("2026-03-07T10:00:00 INFO balance 10 -> 11\n", encoding="utf-8")

    monitor = pbrun_module.Monitor()
    monitor.path = str(temp_workspace)
    monitor.user = "alice"
    monitor.version = "s"
    monitor.pb_version = "6"
    monitor.watch_log()

    log_file.write_text("2026-03-07T10:05:00 INFO ok\n", encoding="utf-8")
    monitor.watch_log()

    assert monitor.infos_today == 2
    assert monitor.pnl_today == 1.0
