import json
from pathlib import Path

import User as user_module


def _patch_user_paths(monkeypatch, tmp_path, pb_installed=True, pb7_installed=True):
    pbdir = tmp_path / "pb6"
    pb7dir = tmp_path / "pb7"
    pbdir.mkdir()
    pb7dir.mkdir()
    monkeypatch.setattr(user_module, "pbdir", lambda: str(pbdir))
    monkeypatch.setattr(user_module, "pb7dir", lambda: str(pb7dir))
    monkeypatch.setattr(user_module, "PBGDIR", str(tmp_path))
    monkeypatch.setattr(user_module, "is_pb_installed", lambda: pb_installed)
    monkeypatch.setattr(user_module, "is_pb7_installed", lambda: pb7_installed)
    return pbdir, pb7dir


def test_users_load_merges_sources_sorts_and_keeps_special_fields(temp_workspace, monkeypatch):
    pbdir, pb7dir = _patch_user_paths(monkeypatch, temp_workspace)
    (Path(pbdir) / "api-keys.json").write_text(
        json.dumps(
            {
                "zeta": {"exchange": "binance", "key": "k1", "secret": "s1"},
                "alpha": {
                    "exchange": "hyperliquid",
                    "wallet_address": "0xabc",
                    "private_key": "priv",
                    "is_vault": True,
                },
            }
        ),
        encoding="utf-8",
    )
    (Path(pb7dir) / "api-keys.json").write_text(
        json.dumps(
            {
                "beta": {"exchange": "bitget", "key": "k2", "secret": "s2", "passphrase": "p2"},
            }
        ),
        encoding="utf-8",
    )

    users = user_module.Users()

    assert users.list() == ["alpha", "beta", "zeta"]
    alpha = users.find_user("alpha")
    beta = users.find_user("beta")
    assert alpha.wallet_address == "0xabc"
    assert alpha.private_key == "priv"
    assert alpha.is_vault is True
    assert beta.passphrase == "p2"


def test_users_load_tolerates_corrupted_secondary_file(temp_workspace, monkeypatch):
    pbdir, pb7dir = _patch_user_paths(monkeypatch, temp_workspace)
    (Path(pbdir) / "api-keys.json").write_text(
        json.dumps({"alpha": {"exchange": "binance", "key": "k", "secret": "s"}}),
        encoding="utf-8",
    )
    (Path(pb7dir) / "api-keys.json").write_text("{not valid json", encoding="utf-8")

    users = user_module.Users()

    assert users.list() == ["alpha"]
    assert users.find_user("alpha").exchange == "binance"


def test_users_save_writes_expected_fields_and_backups(temp_workspace, monkeypatch):
    pbdir, pb7dir = _patch_user_paths(monkeypatch, temp_workspace)
    (Path(pbdir) / "api-keys.json").write_text("{}", encoding="utf-8")
    (Path(pb7dir) / "api-keys.json").write_text("{}", encoding="utf-8")

    users = user_module.Users()
    users.users = []

    hyper = user_module.User()
    hyper.name = "hyper"
    hyper.exchange = "hyperliquid"
    hyper.wallet_address = "0xabc"
    hyper.private_key = "priv"
    hyper.is_vault = True

    bitget = user_module.User()
    bitget.name = "bitget_user"
    bitget.exchange = "bitget"
    bitget.key = "key"
    bitget.secret = "secret"
    bitget.passphrase = "pass"

    users.users.extend([hyper, bitget])
    users.save()

    saved_pb6 = json.loads((Path(pbdir) / "api-keys.json").read_text(encoding="utf-8"))
    saved_pb7 = json.loads((Path(pb7dir) / "api-keys.json").read_text(encoding="utf-8"))
    backups = list((temp_workspace / "data" / "api-keys").glob("*.json"))

    assert saved_pb6 == saved_pb7
    assert saved_pb6["hyper"]["wallet_address"] == "0xabc"
    assert saved_pb6["hyper"]["private_key"] == "priv"
    assert saved_pb6["hyper"]["is_vault"] is True
    assert saved_pb6["bitget_user"]["passphrase"] == "pass"
    assert len(backups) == 2
