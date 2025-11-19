# Repository Guidelines
## Project Structure & Module Organization
- `pbgui.py` is the Streamlit entry point; keep UI wiring and state management there while heavier logic lives under `pbgui/pbgui_purefunc.py`.
- The `pbgui/` package contains UI components (`ui/`), reusable config helpers (`configs/`), and light utilities; mirror this layout when adding screens.
- Exchange adapters live in `exchanges/` and share the `BaseExchange` contract; place any new connector alongside the others and register it through `Exchange._exchange_map`.
- Templates and defaults for Passivbot configs live in `pb_configs/` while user-facing docs, screenshots, and assets belong under `docs/`, `images/`, or `data/`. Root-level `test_*.py` files are quick smoke tests for exchange routing.

## Build, Test, and Development Commands
- `python -m venv venv_pbgui` then `.\venv_pbgui\Scripts\Activate.ps1` (or `source venv_pbgui/bin/activate`) creates an isolated dev environment per README guidance.
- `pip install -r requirements.txt` installs Streamlit, ccxt, Ansible, and monitoring helpers; rerun when this file or `requirements_vps.txt` changes.
- `streamlit run pbgui.py` starts the GUI with hot reload; pass `--server.port 8502` when another instance already occupies 8501.
- `python test_exchange_refactor.py` and `python test_simple_import.py` validate the exchange factory refactor before heavier testing.
- `python -m pytest tests` is the expectation once you introduce formal test modules; keep fixtures lightweight to avoid multi-GB market data pulls.

## Coding Style & Naming Conventions
- Follow PEP 8 with four-space indentation and docstrings similar to `Exchange.py`; add type hints on new public APIs and prefer descriptive parameter names.
- Modules stay snake_case (`balance_calculator.py`), classes stay PascalCase (`BaseExchange`), and constants are UPPER_SNAKE_CASE (`pb_configs/constants.py`).
- Keep Streamlit components declarative by doing data shaping inside helpers such as `pbgui_purefunc.py` or `pb_configs/configs/*.py` and returning serializable objects.
- Prefer f-strings and explicit context managers for file or SSH access, and provide `.example` versions of any new config that carries secrets.

## Testing Guidelines
- Use pytest for unit coverage; store new suites under `tests/` or alongside the module (mirroring `test_exchange_refactor.py`) until a dedicated folder justifies itself.
- Build deterministic fixtures from sanitized configs stored in `pb_configs/` or `docs/` rather than committing live exchange data or SQLite databases.
- Target edge cases around exchange selection, config mutation, and Streamlit helpers; run `python -m pytest -k exchange` plus any targeted smoke scripts before pushing.
- For Ansible or YAML automation under `setup/` and `master-*.yml`, run `ansible-playbook <file> --check` against staging and document the outcome in the PR.

## Commit & Pull Request Guidelines
- Commits follow the Conventional Commits pattern already in history (`feat:`, `fix:`, `chore:`) so release tooling can auto-build changelogs.
- Keep each commit focused (UI tweak, exchange fix, doc change) and reference issues or exchanges impacted in the body for traceability.
- PRs must include a short problem statement, validation list (example: `streamlit run pbgui.py`, `python test_exchange_refactor.py`), and screenshots or GIFs for UI adjustments saved under `docs/images/`.
- Mention any required `pbgui.ini` or config migrations plus backward compatibility notes when behavior changes.

## Configuration & Security Tips
- Never commit populated `pbgui.ini` files; derive new keys from `pbgui.ini.example` and add documentation or defaults in `pb_configs/configs/`.
- When editing `config.json.jinja` or the Ansible playbooks, avoid embedding credentials and test with disposable VPS hosts before targeting production nodes.
- Reuse helpers in `pbgui/utils.py` for filesystem paths and encryption so credentials do not get duplicated across modules.
