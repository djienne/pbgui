import json
import hjson
import pprint
import configparser
from pathlib import Path
import os
import shutil
from datetime import datetime

def ensure_ini_exists():
    """
    Ensure pbgui.ini exists. If not, create it from pbgui.ini.example.
    This prevents config loss during startup or when services write to the file.
    """
    if not os.path.exists('pbgui.ini'):
        if os.path.exists('pbgui.ini.example'):
            shutil.copy('pbgui.ini.example', 'pbgui.ini')
            print("Created pbgui.ini from pbgui.ini.example")
        else:
            # Create minimal empty config if example doesn't exist
            with open('pbgui.ini', 'w', encoding='utf-8') as f:
                f.write("[main]\n")
            print("Created empty pbgui.ini")
    return os.path.exists('pbgui.ini')

def backup_ini():
    """
    Create a backup of pbgui.ini before any write operation.
    Keeps only the last backup to avoid clutter.
    """
    if os.path.exists('pbgui.ini'):
        try:
            backup_path = 'pbgui.ini.backup'
            shutil.copy('pbgui.ini', backup_path)
        except Exception as e:
            print(f"Warning: Could not create backup of pbgui.ini: {e}")

def save_ini(section: str, parameter: str, value: str):
    """
    Safely save a configuration parameter to pbgui.ini.
    - Ensures the file exists before writing
    - Creates a backup before writing
    - Validates the config was read successfully
    - Preserves all existing settings
    """
    # Ensure pbgui.ini exists
    ensure_ini_exists()

    # Create backup before writing
    backup_ini()

    # Read existing config
    pb_config = configparser.ConfigParser()
    files_read = pb_config.read('pbgui.ini', encoding='utf-8')

    # Validate that the file was actually read
    if not files_read:
        print("Warning: pbgui.ini could not be read, attempting to restore from backup")
        if os.path.exists('pbgui.ini.backup'):
            shutil.copy('pbgui.ini.backup', 'pbgui.ini')
            files_read = pb_config.read('pbgui.ini', encoding='utf-8')
            if not files_read:
                print("Error: Could not read pbgui.ini even after restore. Creating new file.")
                ensure_ini_exists()
                pb_config.read('pbgui.ini', encoding='utf-8')

    # Add section if it doesn't exist
    if not pb_config.has_section(section):
        pb_config.add_section(section)

    # Set the parameter
    pb_config.set(section, parameter, value)

    # Write to file
    try:
        with open('pbgui.ini', 'w', encoding='utf-8') as pbgui_configfile:
            pb_config.write(pbgui_configfile)
    except Exception as e:
        print(f"Error writing to pbgui.ini: {e}")
        # Attempt to restore from backup
        if os.path.exists('pbgui.ini.backup'):
            shutil.copy('pbgui.ini.backup', 'pbgui.ini')
            print("Restored pbgui.ini from backup")

def load_ini(section: str, parameter: str):
    """
    Safely load a configuration parameter from pbgui.ini.
    - Ensures the file exists before reading
    """
    # Ensure pbgui.ini exists
    ensure_ini_exists()

    pb_config = configparser.ConfigParser()
    pb_config.read('pbgui.ini', encoding='utf-8')
    if pb_config.has_option(section, parameter):
        return pb_config.get(section, parameter)
    else:
        return ""

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

def load_symbols_from_ini(exchange: str, market_type: str):
    pb_config = configparser.ConfigParser()
    pb_config.read('pbgui.ini', encoding='utf-8')
    if pb_config.has_option("exchanges", f'{exchange}.{market_type}'):
        return eval(pb_config.get("exchanges", f'{exchange}.{market_type}'))
    else:
        return []
