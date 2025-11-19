import sys
from pathlib import Path

# Ensure repository root (and the package directory) are importable even when
# Streamlit launches the script from an arbitrary working directory.
ROOT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = ROOT_DIR / "pbgui"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if PACKAGE_DIR.is_dir() and str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

import streamlit as st
from pbgui_func import build_navigation
from disable_autocomplete import set_proper_autocomplete_attributes
from pbgui.process_cleanup import setup_process_cleanup
from pbgui.compat_patches import apply_runtime_patches

setup_process_cleanup()
apply_runtime_patches()

st.logo("images/logo.png", size="large")

# Prevent browser password managers from incorrectly flagging text inputs
set_proper_autocomplete_attributes()

build_navigation()
