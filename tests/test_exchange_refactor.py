import sqlite3
from types import SimpleNamespace

import pytest

import Database as database_module
from Exchange import Exchange, Exchanges
from Status import InstanceStatus, InstancesStatus
from exchanges.hyperliquid import Hyperliquid


@pytest.mark.parametrize(
    ("exchange_id", "class_name"),
    [
        ("binance", "Binance"),
        ("bybit", "Bybit"),
        ("hyperliquid", "Hyperliquid"),
        ("bitget", "Bitget"),
        ("okx", "OKX"),
        ("kucoin", "Kucoin"),
        ("gateio", "Gateio"),
        ("bingx", "BingX"),
    ],
)
def test_exchange_factory_creates_expected_class(exchange_id, class_name):
    exchange = Exchange(exchange_id, None)

    assert type(exchange).__name__ == class_name
    assert exchange.name == exchange_id
    assert exchange_id in Exchanges.list()


def test_exchange_factory_rejects_invalid_exchange():
    with pytest.raises(ValueError):
        Exchange("invalid_exchange", None)


def test_instances_status_iterates_like_a_standard_container(tmp_path):
    status_file = tmp_path / "status.json"
    statuses = InstancesStatus(str(status_file))
    instance_status = InstanceStatus()
    instance_status.name = "test"
    statuses.add(instance_status)

    collected = list(statuses)

    assert collected == [instance_status]


def test_hyperliquid_fetch_symbol_infos_returns_defaults_on_market_load_failure():
    class FailingInstance:
        def load_markets(self):
            raise RuntimeError("boom")

    exchange = Hyperliquid(None)
    exchange.instance = FailingInstance()

    assert exchange.fetch_symbol_infos("BTCUSDC") == (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)


def test_hyperliquid_fetch_history_builds_string_unique_ids(monkeypatch):
    class DummyInstance:
        def __init__(self):
            self._funding_called = False
            self._trades_called = False

        def milliseconds(self):
            return 1_000_000

        def iso8601(self, value):
            return str(value)

        def fetch(self, url, method=None, headers=None, body=None):
            if not self._funding_called:
                self._funding_called = True
                return [{"time": 123, "delta": {"coin": "BTC", "usdc": 1.5}}]
            return []

        def fetch_my_trades(self, since=None, limit=None, params=None):
            if not self._trades_called:
                self._trades_called = True
                return []
            return []

    monkeypatch.setattr("exchanges.hyperliquid.sleep", lambda _: None)

    exchange = Hyperliquid(SimpleNamespace(key=None, wallet_address="0xabc", name="alice"))
    exchange.instance = DummyInstance()

    history = exchange.fetch_history(100)

    assert history[0]["uniqueid"] == "123_BTC"


def test_database_skips_balance_write_when_fetch_fails(monkeypatch, tmp_path):
    class DummyExchange:
        error = "balance fetch failed"

        def fetch_balance(self, market_type):
            return None

    monkeypatch.setattr(database_module, "PBGDIR", str(tmp_path))
    monkeypatch.setattr(database_module, "Exchange", lambda exchange_id, user: DummyExchange())
    (tmp_path / "data").mkdir()

    db = database_module.Database()
    user = SimpleNamespace(exchange="binance", name="alice")

    db.update_balances(user)

    with sqlite3.connect(db.db) as conn:
        row_count = conn.execute(
            "SELECT COUNT(*) FROM balances WHERE user = ?",
            (user.name,),
        ).fetchone()[0]

    assert row_count == 0
