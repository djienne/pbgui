import ast
import streamlit as st
import json
import hjson
import pprint
import uuid
import requests
import configparser
import os
import hashlib
import hmac
import secrets
from time import sleep, time
from pathlib import Path
from pbgui_purefunc import load_ini, save_ini
from Log import LogHandler
from PBRemote import PBRemote
from MonitorConfig import MonitorConfig
import toml

AUTH_PASSWORD_KEY = "password"
AUTH_PASSWORD_HASH_KEY = "password_hash"
AUTH_HASH_SCHEME = "pbkdf2_sha256"
AUTH_HASH_ITERATIONS = 390000

def open_native_file_dialog(initial_dir=".", title="Select File", filetypes=None):
    """
    Open a native file dialog using tkinter.
    Returns the selected file path or None if cancelled.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog

        # Create a hidden root window
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        # Open file dialog
        if filetypes is None:
            filetypes = [("All files", "*.*")]

        file_path = filedialog.askopenfilename(
            parent=root,
            initialdir=initial_dir,
            title=title,
            filetypes=filetypes
        )

        root.destroy()
        return file_path if file_path else None

    except Exception as e:
        st.error(f"Could not open native file dialog: {e}")
        return None

def open_native_folder_dialog(initial_dir=".", title="Select Folder"):
    """
    Open a native folder dialog using tkinter.
    Returns the selected folder path or None if cancelled.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog

        # Create a hidden root window
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        # Open folder dialog
        folder_path = filedialog.askdirectory(
            parent=root,
            initialdir=initial_dir,
            title=title
        )

        root.destroy()
        return folder_path if folder_path else None

    except Exception as e:
        st.error(f"Could not open native folder dialog: {e}")
        return None

@st.dialog("Select Path", width="large")
def change_ini(section, parameter):
    """
    Opens a native file/folder selector dialog based on the parameter type.
    Directory parameters (pbdir, pb7dir) -> folder selector
    File parameters (pbvenv, pb7venv) -> file selector
    """
    st.write(f"Click the button below to open the native file/folder selector for **{parameter}**")

    # Determine initial directory
    initial_path = st.session_state.get(parameter, ".")
    if initial_path and os.path.exists(initial_path):
        if os.path.isfile(initial_path):
            initial_dir = os.path.dirname(initial_path)
        else:
            initial_dir = initial_path
    else:
        initial_dir = os.getcwd()

    # Determine if we need folder or file selector
    is_directory = parameter.endswith('dir')
    is_venv = 'venv' in parameter

    col1, col2 = st.columns([1,1])

    with col1:
        if st.button("🗂️ Open File/Folder Browser", use_container_width=True):
            if is_directory:
                # Open folder dialog for directory parameters
                selected_path = open_native_folder_dialog(
                    initial_dir=initial_dir,
                    title=f"Select {parameter.upper()} Directory"
                )
            elif is_venv:
                # Open file dialog for venv parameters (Python executables)
                selected_path = open_native_file_dialog(
                    initial_dir=initial_dir,
                    title=f"Select {parameter.upper()} Python Interpreter",
                    filetypes=[
                        ("Python Executable", "python*"),
                        ("Executable Files", "*.exe"),
                        ("All files", "*.*")
                    ]
                )
            else:
                # Default to file dialog
                selected_path = open_native_file_dialog(
                    initial_dir=initial_dir,
                    title=f"Select {parameter}"
                )

            if selected_path:
                selected_path = os.path.abspath(selected_path)
                st.session_state[parameter] = selected_path
                st.session_state[f'input_{parameter}'] = selected_path
                save_ini(section, parameter, selected_path)
                st.success(f"✅ Selected: {selected_path}")
                sleep(1)
                st.rerun()
            else:
                st.info("Selection cancelled")

    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

    # Fallback: Show current path and manual input option
    st.markdown("---")
    st.write("**Current path:**")
    st.code(st.session_state.get(parameter, "Not set"), language=None)

    with st.expander("📝 Or enter path manually"):
        manual_path = st.text_input(
            "Enter path manually",
            value=st.session_state.get(parameter, ""),
            key=f'manual_{parameter}'
        )
        if st.button("💾 Save Manual Path"):
            if manual_path:
                manual_path = os.path.abspath(manual_path)
                st.session_state[parameter] = manual_path
                st.session_state[f'input_{parameter}'] = manual_path
                save_ini(section, parameter, manual_path)
                st.success(f"✅ Saved: {manual_path}")
                sleep(1)
                st.rerun()

@st.dialog("Select file")
def select_file(parameter):
    filename = st_file_selector(st, path=st.session_state[parameter], key = f'file_change_{parameter}', label = f'select {parameter}')
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button(":green[OK]"):
            filename = os.path.abspath(filename)
            st.session_state[parameter] = filename
            st.rerun()
    with col2:
        if st.button(":red[Cancel]"):
            st.rerun()

def pbdir(): return load_ini("main", "pbdir")

def pbvenv(): return load_ini("main", "pbvenv")

def is_pb_installed():
    if Path(f"{pbdir()}/passivbot.py").exists():
        return True
    return False

def pb7dir(): return load_ini("main", "pb7dir")

def pb7venv(): return load_ini("main", "pb7venv")

def is_pb7_installed():
    if Path(f"{pb7dir()}/src/passivbot.py").exists():
        return True
    return False

PBGDIR = Path.cwd()

def is_authenticted():
    if 'password_correct' in st.session_state:
        if st.session_state['password_correct']:
            return True   
    return False

def _auth_secrets_path() -> Path:
    return Path(".streamlit/secrets.toml")


def _load_auth_settings():
    secrets_path = _auth_secrets_path()
    if not secrets_path.exists():
        return {}, None
    try:
        with secrets_path.open("r", encoding="utf-8") as file:
            return toml.load(file), None
    except (OSError, toml.TomlDecodeError) as exc:
        return {}, str(exc)


def _write_auth_settings(settings: dict):
    secrets_path = _auth_secrets_path()
    secrets_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = secrets_path.with_suffix(".toml.tmp")
    with temp_path.open("w", encoding="utf-8") as file:
        toml.dump(settings, file)
    os.replace(temp_path, secrets_path)


def hash_auth_password(password: str, *, salt: str = None, iterations: int = AUTH_HASH_ITERATIONS) -> str:
    if not password:
        raise ValueError("Password can not be empty")
    salt = salt or secrets.token_hex(16)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    )
    return f"{AUTH_HASH_SCHEME}${iterations}${salt}${derived_key.hex()}"


def verify_password_hash(password: str, password_hash: str) -> bool:
    try:
        scheme, iterations, salt, expected = password_hash.split("$", 3)
        iterations = int(iterations)
    except ValueError:
        return False
    if scheme != AUTH_HASH_SCHEME:
        return False
    candidate = hash_auth_password(password, salt=salt, iterations=iterations)
    return hmac.compare_digest(candidate, password_hash)


def auth_is_configured() -> bool:
    settings, error = _load_auth_settings()
    if error:
        return False
    return bool(settings.get(AUTH_PASSWORD_HASH_KEY) or settings.get(AUTH_PASSWORD_KEY))


def set_auth_password(password: str):
    settings, _ = _load_auth_settings()
    settings[AUTH_PASSWORD_HASH_KEY] = hash_auth_password(password)
    settings.pop(AUTH_PASSWORD_KEY, None)
    _write_auth_settings(settings)


def verify_auth_password(password: str) -> bool:
    settings, error = _load_auth_settings()
    if error:
        return False

    password_hash = settings.get(AUTH_PASSWORD_HASH_KEY)
    if password_hash:
        return verify_password_hash(password, password_hash)

    return False


LOGIN_MAX_ATTEMPTS = 5
LOGIN_COOLDOWN_SECONDS = 30

def check_password():
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # Rate limiting: check cooldown
        failed = st.session_state.get("login_failed_attempts", 0)
        last_fail = st.session_state.get("login_last_failed_time", 0)
        if failed >= LOGIN_MAX_ATTEMPTS:
            elapsed = time() - last_fail
            if elapsed < LOGIN_COOLDOWN_SECONDS:
                st.session_state["password_correct"] = False
                return
            # Cooldown expired, reset
            st.session_state["login_failed_attempts"] = 0

        if verify_auth_password(st.session_state.get("password", "")):
            st.session_state["password_correct"] = True
            st.session_state.pop("password", None)
            st.session_state.pop("login_failed_attempts", None)
            st.session_state.pop("login_last_failed_time", None)
        else:
            st.session_state["password_correct"] = False
            st.session_state["login_failed_attempts"] = st.session_state.get("login_failed_attempts", 0) + 1
            st.session_state["login_last_failed_time"] = time()

    settings, error = _load_auth_settings()
    if error or not (settings.get(AUTH_PASSWORD_HASH_KEY) or settings.get(AUTH_PASSWORD_KEY)):
        st.session_state["password_correct"] = False
        st.session_state["password_missing"] = True
        if error:
            st.error(f"Authentication config is invalid: {error}")
        else:
            st.warning("PBGUI requires an admin password before it can be used.")
        with st.form("setup_password_form"):
            new_password = st.text_input(
                "Create Admin Password",
                type="password",
                autocomplete="new-password",
            )
            confirm_password = st.text_input(
                "Confirm Admin Password",
                type="password",
                autocomplete="new-password",
            )
            submit_setup = st.form_submit_button("Save Password")
        if submit_setup:
            if not new_password:
                st.error("Password can not be empty.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                set_auth_password(new_password)
                st.success("Password saved. Please log in.")
                st.session_state.clear()
                st.rerun()
        return False

    st.session_state.pop("password_missing", None)

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password", autocomplete="current-password"
        )
        st.info("Please enter your password to continue.")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        failed = st.session_state.get("login_failed_attempts", 0)
        last_fail = st.session_state.get("login_last_failed_time", 0)
        if failed >= LOGIN_MAX_ATTEMPTS:
            remaining = LOGIN_COOLDOWN_SECONDS - (time() - last_fail)
            if remaining > 0:
                st.error(f"Too many failed attempts. Try again in {int(remaining)} seconds.")
                return False
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password", autocomplete="current-password"
        )
        st.error("Password incorrect")
        return False
    else:
        # Password correct.
        return True

def set_page_config(page : str = "Start"):
    st.session_state.page = page
    st.set_page_config(
        page_title=f"PBGUI - {page}",
        page_icon=":screwdriver:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get help': 'https://github.com/msei99/pbgui/#readme',
            'About': "Passivbot GUI v1.37 [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y216Q3QS)"
        }
    )
    # Check VPS Errors
    has_vps_errors()
    
    with st.sidebar:
        st.write(f"### {page} Options")
        
def get_navi_paths():
    NAVI_BASE_DIR = "navi/"
    paths = {
        "SYSTEM_LOGIN":        os.path.join(NAVI_BASE_DIR, "system_login.py"),
        "SYSTEM_API_KEYS":     os.path.join(NAVI_BASE_DIR, "system_api_keys.py"),
        "SYSTEM_SERVICES":     os.path.join(NAVI_BASE_DIR, "system_services.py"),
        "SYSTEM_VPS_MANAGER":  os.path.join(NAVI_BASE_DIR, "system_vps_manager.py"),
        "SYSTEM_DEBUGLOG":     os.path.join(NAVI_BASE_DIR, "system_debuglog.py"),

        "INFO_DASHBOARDS":     os.path.join(NAVI_BASE_DIR, "info_dashboards.py"),
        "INFO_COIN_DATA":      os.path.join(NAVI_BASE_DIR, "info_coin_data.py"),

        "V6_SINGLE_RUN":       os.path.join(NAVI_BASE_DIR, "v6_single_run.py"),
        "V6_SINGLE_BACKTEST":  os.path.join(NAVI_BASE_DIR, "v6_single_backtest.py"),
        "V6_SINGLE_OPTIMIZE":  os.path.join(NAVI_BASE_DIR, "v6_single_optimize.py"),
        "V6_SPOT_VIEW":        os.path.join(NAVI_BASE_DIR, "v6_spot_view.py"),

        "V6_MULTI_RUN":        os.path.join(NAVI_BASE_DIR, "v6_multi_run.py"),
        "V6_MULTI_BACKTEST":   os.path.join(NAVI_BASE_DIR, "v6_multi_backtest.py"),
        "V6_MULTI_OPTIMIZE":   os.path.join(NAVI_BASE_DIR, "v6_multi_optimize.py"),

        "V7_RUN":              os.path.join(NAVI_BASE_DIR, "v7_run.py"),
        "V7_BACKTEST":         os.path.join(NAVI_BASE_DIR, "v7_backtest.py"),
        "V7_OPTIMIZE":         os.path.join(NAVI_BASE_DIR, "v7_optimize.py"),
        "V7_GRID_VISUALIZER":  os.path.join(NAVI_BASE_DIR, "v7_grid_visualizer.py"),
        "V7_BALANCE_CALC":     os.path.join(NAVI_BASE_DIR, "v7_balance_calc.py"),
    }
    return paths

def build_navigation():
    paths = get_navi_paths()

    # Single Pages
    pM1 = st.Page(paths["SYSTEM_LOGIN"], title="Welcome", icon=":material/logout:")
    pM2 = st.Page(paths["SYSTEM_API_KEYS"], title="API-Keys", icon=":material/key:")
    pM3 = st.Page(paths["SYSTEM_SERVICES"], title="PBGUI Services", icon=":material/build:")
    pM4 = st.Page(paths["SYSTEM_VPS_MANAGER"], title="VPS Manager", icon=":material/computer:")
    pM5 = st.Page(paths["SYSTEM_DEBUGLOG"], title="DEBUGLOG", icon=":material/terminal:")

    pSe1 = st.Page(paths["INFO_DASHBOARDS"], title="Dashboards", icon=":material/dashboard:")
    pSe2 = st.Page(paths["INFO_COIN_DATA"], title="Coin Data", icon=":material/monetization_on:")

    pS1 = st.Page(paths["V6_SINGLE_RUN"], title="Run", icon=":material/play_arrow:")
    pS2 = st.Page(paths["V6_SINGLE_BACKTEST"], title="Backtest", icon=":material/history:")
    pS3 = st.Page(paths["V6_SINGLE_OPTIMIZE"], title="Optimize", icon=":material/tune:")
    pS4 = st.Page(paths["V6_SPOT_VIEW"], title="Spot View", icon=":material/remove_red_eye:")

    p61 = st.Page(paths["V6_MULTI_RUN"], title="Run", icon=":material/play_arrow:")
    p62 = st.Page(paths["V6_MULTI_BACKTEST"], title="Backtest", icon=":material/history:")
    p63 = st.Page(paths["V6_MULTI_OPTIMIZE"], title="Optimize", icon=":material/tune:")

    p71 = st.Page(paths["V7_RUN"], title="Run", icon=":material/play_arrow:")
    p72 = st.Page(paths["V7_BACKTEST"], title="Backtest", icon=":material/history:")
    p73 = st.Page(paths["V7_OPTIMIZE"], title="Optimize", icon=":material/tune:")
    p74 = st.Page(paths["V7_GRID_VISUALIZER"], title="Grid Visualizer", icon=":material/remove_red_eye:")
    p75 = st.Page(paths["V7_BALANCE_CALC"], title="Balance Calculator", icon=":material/attach_money:")

       
    # Page Groups
    SystemPages = [pM1, pM2, pM3, pM4]
    
    if get_debuglog().logfile_exists():
        SystemPages.append(pM5)
                
    InfotmationPages = [pSe1, pSe2]
    v7Pages = [p71, p72, p73, p74, p75]
    v6Pages = [p61, p62, p63]
    SinglePages = [pS1, pS2, pS3, pS4]

    # Navigation
    navi = st.navigation(
        {
            "System": SystemPages,
            "Information": InfotmationPages,
            "PBv7": v7Pages,
            "PBv6 Multi": v6Pages,
            "PBv6 Single": SinglePages,
        },position="top"
    )
    st.session_state.navigation = navi
    navi.run()
    
    
def init_debuglog():
    if "debuglog" not in st.session_state:
        st.session_state.debuglog = LogHandler(
            logger_name="debug_logger",
            log_filename="debug.log",
            backup_filename="debug.log.old",
            base_dir=Path(f'{PBGDIR}/data/logs'),
            max_bytes=100_000,
            backup_count=1,
        )
        
def get_debuglog() -> LogHandler:
    if "debuglog" not in st.session_state:
        init_debuglog()
    return st.session_state.debuglog
    
def is_session_state_not_initialized():
    # Init Services
    if (
        'pbdir' not in st.session_state or
        'services' not in st.session_state or
        'pbgui_instances' not in st.session_state or
        'multi_instances' not in st.session_state or
        'users' not in st.session_state or
        'pbcoindata' not in st.session_state
    ):
        return True
    return False

def replace_special_chars(input:str):
    # Replace chars that can cause trouble in filenames
    return input.replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_")
    
def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except (ValueError,TypeError) as err:
        return False
    return True

def validateHJSON(hjsonData):
    try:
        hjson.loads(hjsonData)
    except (ValueError) as err:
        return False
    return True

def config_pretty_str(config: dict):
    pretty_str = pprint.pformat(config)
    for r in [("'", '"'), ("True", "true"), ("False", "false")]:
        pretty_str = pretty_str.replace(*r)
    return pretty_str

def upload_pbconfigdb(config: str, symbol: str, source_name : str):
    if validateJSON(config):
        uniq = str(uuid.uuid4().hex)
        url = 'https://pbconfigdb.scud.dedyn.io/uploads/b1ea37f7cfa0ebf9b67c2f6b30b95b8b1a92e249/'
        headers = {
            'Content-Type': 'application/json',
            'data': json.dumps(json.loads(config)),
            'filename': f'{symbol}-{source_name}-{uniq}.json' # {symbol}-{username}-{unique}.json
        }
        response = requests.put(url, headers=headers)
        st.info(response.text, icon="ℹ️")
    else:
        st.error("Invalid config", icon="🚨")

def load_symbols_from_ini(exchange: str, market_type: str):
    pb_config = configparser.ConfigParser()
    pb_config.read('pbgui.ini', encoding='utf-8')
    if pb_config.has_option("exchanges", f'{exchange}.{market_type}'):
        return ast.literal_eval(pb_config.get("exchanges", f'{exchange}.{market_type}'))
    else:
        return []

def update_dir(key):
    choice = st.session_state[key]
    if os.path.isdir(os.path.join(st.session_state[key+'curr_dir'], choice)):
        st.session_state[key+'curr_dir'] = os.path.normpath(os.path.join(st.session_state[key+'curr_dir'], choice))
        files = sorted(os.listdir(st.session_state[key+'curr_dir']))
        files.insert(0, '..')
        files.insert(0, '.')
        st.session_state[key+'files'] = files

def st_file_selector(st_placeholder, path='.', label='Select a file/folder', key = 'selected'):
    if key+'curr_dir' not in st.session_state:
        base_path = '.' if path is None or path == '' else path
        base_path = base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
        base_path = '.' if base_path is None or base_path == '' else base_path

        files = sorted(os.listdir(base_path))
        files.insert(0, '..')
        files.insert(0, '.')
        st.session_state[key+'files'] = files
        st.session_state[key+'curr_dir'] = base_path
    else:
        base_path = st.session_state[key+'curr_dir']
    selected_file = st_placeholder.selectbox(label=label, 
                                        options=st.session_state[key+'files'], 
                                        key=key, 
                                        on_change = lambda: update_dir(key))
    selected_path = os.path.normpath(os.path.join(base_path, selected_file))
    st_placeholder.write(os.path.abspath(selected_path))
    return selected_path

def sync_api():
    pbremote = st.session_state.pbremote
    if not getattr(pbremote, "sync_api_keys", False):
        st.info("Remote API key sync is disabled.")
        return
    if not pbremote.check_if_api_synced():
        st.warning('API not in sync')
        if st.button("Sync API"):
            pbremote.sync_api_up()
            timeout = 180
            with st.spinner(text=f'syncing...'):
                with st.empty():
                    while not pbremote.check_if_api_synced():
                        st.text(f'{timeout} sec ({pbremote.unsynced_api} server to go)')
                        sleep(1)
                        timeout -= 1
                        if timeout == 0:
                            break
                    st.text(f'{timeout} sec ({pbremote.unsynced_api} server to go)')
                st.text(f'')
                if timeout == 0:
                    error_popup("Syncing API failed")
                else:
                    info_popup("API synced")
    else:
        st.success('API in sync')

@st.dialog("Error", width="large")
def error_popup(message):
    st.error(f'{message}', icon="⚠️")
    if st.button(":green[OK]"):
        st.rerun()

@st.dialog("Info", width="large")
def info_popup(message):
    st.info(f'{message}', icon="✅")
    if st.button(":green[OK]"):
        st.rerun()

def has_vps_errors():
    if "pbremote" not in st.session_state:
        st.session_state.pbremote = PBRemote()
    st.session_state.pbremote.update_remote_servers()
    errors = st.session_state.pbremote.has_error()
    if errors:
        with st.expander("VPS Errors", expanded=True):
            for error in errors:
                if error["name"] == "offline":
                    st.error(f'Server: {error["server"]} is offline')
                elif error["name"] == "system":
                    st.warning(f'Server: {error["server"]} Instance: {error["name"]} Mem: {error["mem"]} Swap: {error["swap"]} CPU: {error["cpu"]} Disk: {error["disk"]}')
                else:
                    st.warning(f'Server: {error["server"]} Instance: {error["name"]} Mem: {error["mem"]} Swap: {error["swap"]} CPU: {error["cpu"]} Error: {error["error"]} Traceback: {error["traceback"]}')
