import streamlit as st
import json
from ..pbgui_func import validateJSON, error_popup
import pbgui_help

def edit_config(self):
    # Init session_state for keys
    if "config_long_enabled" in st.session_state:
        if st.session_state.config_long_enabled != self.long_enabled:
            self.long_enabled = st.session_state.config_long_enabled
            if self.config:
                st.session_state.config_instance_config = self.config
    if "config_short_enabled" in st.session_state:
        if st.session_state.config_short_enabled != self.short_enabled:
            self.short_enabled = st.session_state.config_short_enabled
            if self.config:
                st.session_state.config_instance_config = self.config
    if "config_long_we" in st.session_state:
        if st.session_state.config_long_we != self.long_we:
            self.long_we = st.session_state.config_long_we
            if self.config:
                st.session_state.config_instance_config = self.config
    if "config_short_we" in st.session_state:
        if st.session_state.config_short_we != self.short_we:
            self.short_we = st.session_state.config_short_we
            if self.config:
                st.session_state.config_instance_config = self.config
    if "config_preview_grid" in st.session_state:
        if st.session_state.config_preview_grid != self.preview_grid:
            self.preview_grid = st.session_state.config_preview_grid
    if "config_instance_config" in st.session_state:
        if st.session_state.config_instance_config != self.config:
            self.config = st.session_state.config_instance_config
            st.session_state.config_long_enabled = self.long_enabled
            st.session_state.config_short_enabled = self.short_enabled
            st.session_state.config_long_we = self.long_we
            st.session_state.config_short_we = self.short_we
        else:
            if validateJSON(st.session_state.config_instance_config):
                if "error_config" in st.session_state:
                    del st.session_state.error_config
    # if self.config:
    #     self.config = st.session_state.config_instance_config
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.toggle("Long enabled", value=self.long_enabled, key="config_long_enabled", help=None)
        st.number_input("LONG_WALLET_EXPOSURE_LIMIT", min_value=0.0, max_value=100.0, value=float(round(self.long_we,2)), step=0.05, format="%.2f", key="config_long_we", help=pbgui_help.exposure)
    with col2:
        st.toggle("Short enabled", value=self.short_enabled, key="config_short_enabled", help=None)
        st.number_input("SHORT_WALLET_EXPOSURE_LIMIT", min_value=0.0, max_value=100.0, value=float(round(self.short_we,2)), step=0.05, format="%.2f", key="config_short_we", help=pbgui_help.exposure)
    with col3:
        st.toggle("Preview Grid", value=self.preview_grid, key="config_preview_grid", help=None)
        st.selectbox("Config Type", [self.type], index=0, key="config_type", help=None, disabled=True)
    # Init height and color with defaults
    height = 600
    color = None
    # Display Error
    if "error_config" in st.session_state:
        st.error(st.session_state.error_config, icon="🚨")
        color = "red"
    if not self.config is None:
        height = len(self.config.splitlines()) *23
    if height < 600:
        height = 600
    if not self.config:
        color = "red"
    col1, col2 = st.columns([1,1])
    with col1:
        if color:
            st.text_area(f':{color}[config]', self.config, key="config_instance_config", height=height)
        else:
            st.text_area(f'config', self.config, key="config_instance_config", height=height)
    with col2:
        st.text_area(f'config converted to v7', self.config_v7, key="config_instance_config_v7", height=height, disabled=True)
