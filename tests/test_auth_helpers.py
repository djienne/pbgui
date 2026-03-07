from pathlib import Path

import toml

import pbgui_func as pbgui_func_module


def test_set_auth_password_stores_hash_and_verifies(temp_workspace):
    assert not pbgui_func_module.auth_is_configured()

    pbgui_func_module.set_auth_password("secret-pass")

    secrets_path = temp_workspace / ".streamlit" / "secrets.toml"
    secrets = toml.loads(secrets_path.read_text(encoding="utf-8"))

    assert "password_hash" in secrets
    assert "password" not in secrets
    assert pbgui_func_module.verify_auth_password("secret-pass") is True
    assert pbgui_func_module.verify_auth_password("wrong-pass") is False


def test_verify_auth_password_rejects_plaintext_password(temp_workspace):
    """Legacy plaintext passwords are no longer accepted for security."""
    secrets_path = temp_workspace / ".streamlit" / "secrets.toml"
    secrets_path.parent.mkdir(parents=True, exist_ok=True)
    secrets_path.write_text('password = "legacy-pass"\n', encoding="utf-8")

    assert pbgui_func_module.verify_auth_password("legacy-pass") is False
