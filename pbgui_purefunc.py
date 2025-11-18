import json
import hjson
import pprint
import configparser
from pathlib import Path
import os
import shutil
from datetime import datetime
import time
import glob
import sys

# Cross-platform file locking support
if sys.platform != 'win32':
    import fcntl
    LOCK_EX = fcntl.LOCK_EX
    LOCK_SH = fcntl.LOCK_SH
else:
    # Windows: File locking is optional since this is typically a single-user desktop app
    # and msvcrt.locking() can cause file access issues
    LOCK_EX = 0x1
    LOCK_SH = 0x0

def _acquire_lock(file_obj, lock_type):
    """Acquire a file lock in a cross-platform way."""
    if sys.platform == 'win32':
        # Windows: Skip file locking to avoid access issues
        # This is acceptable for single-user desktop usage
        pass
    else:
        # Unix locking using fcntl (reliable and necessary for multi-process)
        fcntl.flock(file_obj.fileno(), lock_type)

def ensure_ini_exists():
    """
    Ensure pbgui.ini exists. If not, attempt recovery from recent backup first.
    Only creates from example as last resort to prevent config loss.
    """
    if not os.path.exists('pbgui.ini'):
        print("WARNING: pbgui.ini not found! Attempting recovery...")

        # Try to restore from the most recent timestamped backup first
        backup_files = sorted(glob.glob('pbgui.ini.backup.*'), reverse=True)
        for backup_file in backup_files:
            try:
                backup_age = time.time() - os.path.getmtime(backup_file)
                if backup_age < 3600:  # Less than 1 hour old
                    shutil.copy(backup_file, 'pbgui.ini')
                    print(f"Restored pbgui.ini from recent backup: {backup_file}")
                    return True
            except Exception as e:
                print(f"Could not restore from {backup_file}: {e}")
                continue

        # Try the standard backup file
        if os.path.exists('pbgui.ini.backup'):
            try:
                backup_age = time.time() - os.path.getmtime('pbgui.ini.backup')
                if backup_age < 86400:  # Less than 24 hours old
                    shutil.copy('pbgui.ini.backup', 'pbgui.ini')
                    print("Restored pbgui.ini from backup (less than 24h old)")
                    return True
            except Exception as e:
                print(f"Could not restore from pbgui.ini.backup: {e}")

        # Last resort: copy from example
        if os.path.exists('pbgui.ini.example'):
            shutil.copy('pbgui.ini.example', 'pbgui.ini')
            print("WARNING: Created pbgui.ini from pbgui.ini.example - user config may be lost!")
        else:
            # Create minimal empty config if example doesn't exist
            with open('pbgui.ini', 'w', encoding='utf-8') as f:
                f.write("[main]\n")
            print("WARNING: Created empty pbgui.ini - user config lost!")

    return os.path.exists('pbgui.ini')

def backup_ini():
    """
    Create timestamped backup of pbgui.ini before any write operation.
    Keeps last 10 backups to allow recovery from recent corruption.
    """
    if os.path.exists('pbgui.ini'):
        try:
            # Create timestamped backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f'pbgui.ini.backup.{timestamp}'
            shutil.copy('pbgui.ini', backup_path)

            # Also update the standard backup (for backward compatibility)
            shutil.copy('pbgui.ini', 'pbgui.ini.backup')

            # Clean up old backups (keep last 10)
            backup_files = sorted(glob.glob('pbgui.ini.backup.*'))
            if len(backup_files) > 10:
                for old_backup in backup_files[:-10]:
                    try:
                        os.remove(old_backup)
                    except Exception:
                        pass
        except Exception as e:
            print(f"Warning: Could not create backup of pbgui.ini: {e}")

def save_ini(section: str, parameter: str, value: str):
    """
    Safely save a configuration parameter to pbgui.ini with file locking.
    - Uses exclusive file lock to prevent race conditions
    - Ensures the file exists before writing
    - Creates backup before writing
    - Validates the config was read successfully
    - Preserves all existing settings
    - Warns about overly long values that may cause issues
    """
    # Warn about very long values (>50KB) that may cause parsing issues
    if len(str(value)) > 50000:
        print(f"WARNING: Very long value for [{section}] {parameter} ({len(str(value))} chars)")
        print("This may cause ConfigParser issues. Consider storing large data elsewhere.")

    # Ensure pbgui.ini exists
    ensure_ini_exists()

    # Create backup before writing
    backup_ini()

    # Open with read+write mode to enable atomic operations
    max_retries = 5
    for attempt in range(max_retries):
        try:
            with open('pbgui.ini', 'r+', encoding='utf-8') as f:
                # Acquire exclusive lock (blocks until available)
                _acquire_lock(f, LOCK_EX)

                try:
                    # Read existing config from file
                    f.seek(0)
                    pb_config = configparser.ConfigParser()
                    pb_config.read_file(f)

                    # Validate minimum expected sections
                    if len(pb_config.sections()) < 1:
                        print("Warning: Config has too few sections, may be corrupted")

                    # Add section if it doesn't exist
                    if not pb_config.has_section(section):
                        pb_config.add_section(section)

                    # Set the parameter
                    pb_config.set(section, parameter, value)

                    # Write back to file
                    f.seek(0)
                    f.truncate()
                    pb_config.write(f)
                    f.flush()
                    os.fsync(f.fileno())  # Ensure data is written to disk

                    # Lock released automatically when exiting 'with' block
                    return  # Success!

                except configparser.ParsingError as e:
                    print(f"ERROR: pbgui.ini corrupted during read in save_ini: {e}")
                    print("Attempting to restore from backup before retry...")
                    # Restore from backup and retry
                    if os.path.exists('pbgui.ini.backup'):
                        shutil.copy('pbgui.ini.backup', 'pbgui.ini')
                        if attempt < max_retries - 1:
                            time.sleep(0.1)
                            continue
                    raise

                except Exception as e:
                    print(f"Error during locked write to pbgui.ini: {e}")
                    # Lock will be released, and we'll retry or restore from backup
                    raise

        except (IOError, OSError) as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1}/{max_retries}: Could not acquire lock on pbgui.ini")
                time.sleep(0.1)  # Wait before retry
            else:
                print(f"Error: Could not write to pbgui.ini after {max_retries} attempts: {e}")
                # Attempt to restore from backup
                if os.path.exists('pbgui.ini.backup'):
                    try:
                        shutil.copy('pbgui.ini.backup', 'pbgui.ini')
                        print("Restored pbgui.ini from backup")
                    except Exception:
                        pass

def load_ini(section: str, parameter: str):
    """
    Safely load a configuration parameter from pbgui.ini with file locking.
    - Uses shared file lock to prevent reading during writes
    - Ensures the file exists before reading
    - Handles parsing errors by restoring from backup
    """
    # Ensure pbgui.ini exists
    ensure_ini_exists()

    max_retries = 5
    for attempt in range(max_retries):
        try:
            with open('pbgui.ini', 'r', encoding='utf-8') as f:
                # Acquire shared lock (allows multiple readers, blocks writers)
                _acquire_lock(f, LOCK_SH)

                pb_config = configparser.ConfigParser()
                pb_config.read_file(f)

                # Lock released automatically when exiting 'with' block
                if pb_config.has_option(section, parameter):
                    return pb_config.get(section, parameter)
                else:
                    return ""

        except configparser.ParsingError as e:
            print(f"ERROR: pbgui.ini is corrupted! Parsing error: {e}")
            print("Attempting to restore from backup...")

            # Try to restore from most recent backup
            backup_files = sorted(glob.glob('pbgui.ini.backup.*'), reverse=True)
            for backup_file in backup_files:
                try:
                    shutil.copy(backup_file, 'pbgui.ini')
                    print(f"Restored pbgui.ini from {backup_file}")
                    # Retry reading after restore
                    if attempt < max_retries - 1:
                        time.sleep(0.1)
                        continue
                except Exception:
                    pass

            # If no timestamped backup worked, try standard backup
            if os.path.exists('pbgui.ini.backup'):
                try:
                    shutil.copy('pbgui.ini.backup', 'pbgui.ini')
                    print("Restored pbgui.ini from pbgui.ini.backup")
                    if attempt < max_retries - 1:
                        time.sleep(0.1)
                        continue
                except Exception:
                    pass

            print("ERROR: Could not restore pbgui.ini from any backup!")
            return ""

        except (IOError, OSError) as e:
            if attempt < max_retries - 1:
                time.sleep(0.05)  # Wait before retry
            else:
                print(f"Error: Could not read pbgui.ini after {max_retries} attempts: {e}")
                return ""

def save_ini_batch(updates: dict):
    """
    Safely save multiple configuration parameters to pbgui.ini with file locking.
    Updates is a dict of {section: {parameter: value, ...}, ...}

    Example:
        save_ini_batch({
            "exchanges": {"binance.swap": "['BTCUSDT', 'ETHUSDT']", "binance.spot": "[]"},
            "main": {"pbname": "mynode"}
        })

    - Uses exclusive file lock to prevent race conditions
    - Atomic operation - all updates succeed or all fail
    - Creates backup before writing
    - Warns about overly long values
    """
    # Validate and warn about very long values
    for section, params in updates.items():
        for parameter, value in params.items():
            value_len = len(str(value))
            if value_len > 50000:
                print(f"WARNING: Very long value for [{section}] {parameter} ({value_len} chars)")
                print("This may cause ConfigParser issues. Consider storing large data elsewhere.")

    # Ensure pbgui.ini exists
    ensure_ini_exists()

    # Create backup before writing
    backup_ini()

    # Open with read+write mode to enable atomic operations
    max_retries = 5
    for attempt in range(max_retries):
        try:
            with open('pbgui.ini', 'r+', encoding='utf-8') as f:
                # Acquire exclusive lock (blocks until available)
                _acquire_lock(f, LOCK_EX)

                try:
                    # Read existing config from file
                    f.seek(0)
                    pb_config = configparser.ConfigParser()
                    pb_config.read_file(f)

                    # Apply all updates
                    for section, params in updates.items():
                        if not pb_config.has_section(section):
                            pb_config.add_section(section)
                        for parameter, value in params.items():
                            pb_config.set(section, parameter, str(value))

                    # Write back to file
                    f.seek(0)
                    f.truncate()
                    pb_config.write(f)
                    f.flush()
                    os.fsync(f.fileno())  # Ensure data is written to disk

                    # Lock released automatically when exiting 'with' block
                    return  # Success!

                except configparser.ParsingError as e:
                    print(f"ERROR: pbgui.ini corrupted during read in save_ini_batch: {e}")
                    print("Attempting to restore from backup before retry...")
                    # Restore from backup and retry
                    if os.path.exists('pbgui.ini.backup'):
                        shutil.copy('pbgui.ini.backup', 'pbgui.ini')
                        if attempt < max_retries - 1:
                            time.sleep(0.1)
                            continue
                    raise

                except Exception as e:
                    print(f"Error during locked batch write to pbgui.ini: {e}")
                    raise

        except (IOError, OSError) as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1}/{max_retries}: Could not acquire lock on pbgui.ini")
                time.sleep(0.1)  # Wait before retry
            else:
                print(f"Error: Could not write to pbgui.ini after {max_retries} attempts: {e}")
                # Attempt to restore from backup
                if os.path.exists('pbgui.ini.backup'):
                    try:
                        shutil.copy('pbgui.ini.backup', 'pbgui.ini')
                        print("Restored pbgui.ini from backup")
                    except Exception:
                        pass

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

def load_default_coins():
    """
    Load fallback coin list from default_list.json.
    Returns a dict with 'approved_coins_long' and 'approved_coins_short' lists.
    Returns empty lists if file doesn't exist or is invalid.
    """
    default_file = Path('default_list.json')
    try:
        if default_file.exists():
            with open(default_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    'approved_coins_long': data.get('approved_coins_long', []),
                    'approved_coins_short': data.get('approved_coins_short', [])
                }
    except Exception as e:
        print(f"Warning: Could not load default_list.json: {e}")

    # Return empty lists if any error occurs
    return {'approved_coins_long': [], 'approved_coins_short': []}
