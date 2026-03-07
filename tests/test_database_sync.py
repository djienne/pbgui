import sqlite3
from datetime import datetime as real_datetime
from types import SimpleNamespace

import Database as database_module


class FixedDateTime:
    @classmethod
    def now(cls):
        return real_datetime(2026, 3, 7, 12, 0, 0)


def _make_user(name="alice", exchange="binance"):
    return SimpleNamespace(name=name, exchange=exchange)


def _make_db(tmp_path, monkeypatch):
    monkeypatch.setattr(database_module, "PBGDIR", str(tmp_path))
    (tmp_path / "data").mkdir(exist_ok=True)
    return database_module.Database()


def test_update_history_ignores_duplicate_unique_ids(temp_workspace, monkeypatch):
    db = _make_db(temp_workspace, monkeypatch)
    user = _make_user()

    duplicate_history = [
        {"symbol": "BTCUSDT", "timestamp": 1, "income": 1.0, "uniqueid": "dup"},
        {"symbol": "BTCUSDT", "timestamp": 2, "income": 2.0, "uniqueid": "dup"},
    ]
    monkeypatch.setattr(db, "fetch_history", lambda user_arg: duplicate_history)

    db.update_history(user)

    with sqlite3.connect(db.db) as conn:
        rows = conn.execute("SELECT symbol, timestamp, income, uniqueid FROM history").fetchall()

    assert rows == [("BTCUSDT", 1, 1.0, "dup")]


def test_update_positions_adds_updates_removes_and_normalizes(temp_workspace, monkeypatch):
    class DummyExchange:
        def fetch_positions(self):
            return [
                {
                    "timestamp": None,
                    "contracts": 2,
                    "contractSize": 0.5,
                    "unrealizedPnl": 3.0,
                    "entryPrice": 110.0,
                    "symbol": "BTC/USDT:USDT",
                    "side": "long",
                },
                {
                    "timestamp": 456,
                    "contracts": 4,
                    "contractSize": 0.25,
                    "unrealizedPnl": 1.5,
                    "entryPrice": 210.0,
                    "symbol": "ETH/USDC:USDC",
                    "side": "short",
                },
                {
                    "timestamp": 789,
                    "contracts": 0,
                    "contractSize": 1.0,
                    "unrealizedPnl": 0.0,
                    "entryPrice": 50.0,
                    "symbol": "DOGE/USDT:USDT",
                    "side": "long",
                },
            ]

    monkeypatch.setattr(database_module, "Exchange", lambda exchange_id, user: DummyExchange())
    monkeypatch.setattr(database_module, "datetime", FixedDateTime)

    db = _make_db(temp_workspace, monkeypatch)
    user = _make_user()
    with sqlite3.connect(db.db) as conn:
        db.add_position(conn, [123, 0.25, 0.5, 100.0, "BTCUSDT", user.name, "long"])
        db.add_position(conn, [222, 1.0, 0.0, 50.0, "ADAUSDT", user.name, "long"])

    db.update_positions(user)

    with sqlite3.connect(db.db) as conn:
        rows = conn.execute(
            "SELECT timestamp, psize, upnl, entry, symbol, user, side FROM position ORDER BY symbol, side"
        ).fetchall()

    assert rows == [
        (int(FixedDateTime.now().timestamp() * 1000), 1.0, 3.0, 110.0, "BTCUSDT", user.name, "long"),
        (456, 1.0, 1.5, 210.0, "ETHUSDC", user.name, "short"),
    ]


def test_update_orders_reconciles_open_orders(temp_workspace, monkeypatch):
    class DummyExchange:
        def fetch_all_open_orders(self, symbol):
            return [
                {
                    "timestamp": 999,
                    "amount": 2.0,
                    "price": 101.0,
                    "side": "buy",
                    "id": "live-order",
                    "symbol": symbol,
                },
                {
                    "timestamp": 1000,
                    "amount": 1.0,
                    "price": 202.0,
                    "side": "sell",
                    "id": "new-order",
                    "symbol": symbol,
                },
            ]

    monkeypatch.setattr(database_module, "Exchange", lambda exchange_id, user: DummyExchange())

    db = _make_db(temp_workspace, monkeypatch)
    user = _make_user()
    with sqlite3.connect(db.db) as conn:
        db.add_position(conn, [1, 1.0, 0.0, 100.0, "BTCUSDT", user.name, "long"])
        db.add_order(conn, [111, 0.5, 90.0, "buy", "live-order", "BTCUSDT", user.name])
        db.add_order(conn, [222, 0.5, 91.0, "sell", "stale-order", "BTCUSDT", user.name])

    db.update_orders(user)

    with sqlite3.connect(db.db) as conn:
        rows = conn.execute(
            "SELECT timestamp, amount, price, side, uniqueid, symbol FROM orders ORDER BY uniqueid"
        ).fetchall()

    assert rows == [
        (999, 2.0, 101.0, "buy", "live-order", "BTCUSDT"),
        (1000, 1.0, 202.0, "sell", "new-order", "BTCUSDT"),
    ]


def test_update_prices_normalizes_symbols_and_uses_timestamp_fallback(temp_workspace, monkeypatch):
    class DummyExchange:
        def fetch_prices(self, symbols, market_type):
            assert set(symbols) == {"BTC/USDT:USDT", "ETH/USDC:USDC"}
            return {
                "BTC/USDT:USDT": {"timestamp": None, "last": 101.0},
                "ETH/USDC:USDC": {"timestamp": 555, "last": 202.0},
            }

        def fetch_timestamp(self):
            return 999

    monkeypatch.setattr(database_module, "Exchange", lambda exchange_id, user: DummyExchange())

    db = _make_db(temp_workspace, monkeypatch)
    user = _make_user()
    with sqlite3.connect(db.db) as conn:
        db.add_position(conn, [1, 1.0, 0.0, 100.0, "BTCUSDT", user.name, "long"])
        db.add_position(conn, [2, 1.0, 0.0, 200.0, "ETHUSDC", user.name, "short"])
        db.add_price(conn, [10, 1.0, "BTCUSDT", user.name])
        db.add_price(conn, [10, 1.0, "DOGEUSDT", user.name])

    db.update_prices(user)

    with sqlite3.connect(db.db) as conn:
        rows = conn.execute(
            "SELECT timestamp, price, symbol FROM prices ORDER BY symbol"
        ).fetchall()

    assert rows == [
        (999, 101.0, "BTCUSDT"),
        (555, 202.0, "ETHUSDC"),
    ]


def test_update_balances_writes_successful_balance(temp_workspace, monkeypatch):
    class DummyExchange:
        error = None

        def fetch_balance(self, market_type):
            return 123.45

    monkeypatch.setattr(database_module, "Exchange", lambda exchange_id, user: DummyExchange())
    monkeypatch.setattr(database_module, "datetime", FixedDateTime)

    db = _make_db(temp_workspace, monkeypatch)
    user = _make_user()

    db.update_balances(user)

    with sqlite3.connect(db.db) as conn:
        rows = conn.execute("SELECT timestamp, balance, user FROM balances").fetchall()

    assert rows == [(int(FixedDateTime.now().timestamp() * 1000), 123.45, user.name)]


def test_create_tables_adds_indexes_for_hot_queries(temp_workspace, monkeypatch):
    db = _make_db(temp_workspace, monkeypatch)

    with sqlite3.connect(db.db) as conn:
        indexes = {
            row[1]
            for row in conn.execute(
                "SELECT type, name FROM sqlite_master WHERE type = 'index'"
            ).fetchall()
        }

    assert {
        "idx_history_user_timestamp",
        "idx_history_symbol_timestamp",
        "idx_position_user_symbol_side",
        "idx_orders_user_symbol_uniqueid",
        "idx_prices_user_symbol",
    }.issubset(indexes)
