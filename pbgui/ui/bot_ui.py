import streamlit as st
import json
from ..pbgui_func import error_popup
import pbgui_help

def edit(self):
    # Init session_state for keys
    if "edit_configv7_long_twe" in st.session_state:
        if st.session_state.edit_configv7_long_twe != self.long.total_wallet_exposure_limit:
            self.long.total_wallet_exposure_limit = round(st.session_state.edit_configv7_long_twe,2)
            st.session_state.edit_configv7_long = json.dumps(self.bot["long"], indent=4)
        if "edit_configv7_long" in st.session_state:
            try:
                long = json.loads(st.session_state.edit_configv7_long)
                if st.session_state.edit_configv7_long_twe != float(long["total_wallet_exposure_limit"]):
                    st.session_state.edit_configv7_long_twe = float(long["total_wallet_exposure_limit"])
            except:
                st.session_state.edit_configv7_long = json.dumps(self.bot["long"], indent=4)
                error_popup("Invalid JSON long | RESET")
    else:
        st.session_state.edit_configv7_long_twe = float(self.long.total_wallet_exposure_limit)

    if "edit_configv7_long_positions" in st.session_state:
        if st.session_state.edit_configv7_long_positions != self.long.n_positions:
            self.long.n_positions = round(st.session_state.edit_configv7_long_positions,0)
            st.session_state.edit_configv7_long = json.dumps(self.bot["long"], indent=4)
        if "edit_configv7_long" in st.session_state:
            try:
                long = json.loads(st.session_state.edit_configv7_long)
                if st.session_state.edit_configv7_long_positions != float(long["n_positions"]):
                    st.session_state.edit_configv7_long_positions = float(long["n_positions"])
            except:
                st.session_state.edit_configv7_long = json.dumps(self.bot["long"], indent=4)
                error_popup("Invalid JSON long | RESET")
    else:
        st.session_state.edit_configv7_long_positions = float(self.long.n_positions)

    if "edit_configv7_short_twe" in st.session_state:
        if st.session_state.edit_configv7_short_twe != self.short.total_wallet_exposure_limit:
            self.short.total_wallet_exposure_limit = round(st.session_state.edit_configv7_short_twe,2)
            st.session_state.edit_configv7_short = json.dumps(self.bot["short"], indent=4)
        if "edit_configv7_short" in st.session_state:
            try:
                short = json.loads(st.session_state.edit_configv7_short)
                if st.session_state.edit_configv7_short_twe != float(short["total_wallet_exposure_limit"]):
                    st.session_state.edit_configv7_short_twe = float(short["total_wallet_exposure_limit"])
            except:
                st.session_state.edit_configv7_short = json.dumps(self.bot["short"], indent=4)
                error_popup("Invalid JSON short | RESET")
    else:
        st.session_state.edit_configv7_short_twe = float(self.short.total_wallet_exposure_limit)

    if "edit_configv7_short_positions" in st.session_state:
        if st.session_state.edit_configv7_short_positions != self.short.n_positions:
            self.short.n_positions = round(st.session_state.edit_configv7_short_positions,0)
            st.session_state.edit_configv7_short = json.dumps(self.bot["short"], indent=4)
        if "edit_configv7_short" in st.session_state:
            try:
                short = json.loads(st.session_state.edit_configv7_short)
                if st.session_state.edit_configv7_short_positions != float(short["n_positions"]):
                    st.session_state.edit_configv7_short_positions = float(short["n_positions"])
            except:
                st.session_state.edit_configv7_short = json.dumps(self.bot["short"], indent=4)
                error_popup("Invalid JSON short | RESET")   
    else:
        st.session_state.edit_configv7_short_positions = float(self.short.n_positions)

    if "edit_configv7_long" in st.session_state:
        if st.session_state.edit_configv7_long != json.dumps(self.bot["long"], indent=4):
            try:
                self.long = json.loads(st.session_state.edit_configv7_long)
            except:
                st.session_state.edit_configv7_long = json.dumps(self.bot["long"], indent=4)
                error_popup("Invalid JSON long | RESET")
    else:
        st.session_state.edit_configv7_long = json.dumps(self.bot["long"], indent=4)

    if "edit_configv7_short" in st.session_state:
        if st.session_state.edit_configv7_short != json.dumps(self.bot["short"], indent=4):
            try:
                self.short = json.loads(st.session_state.edit_configv7_short)
            except:
                st.session_state.edit_configv7_short = json.dumps(self.bot["short"], indent=4)
                error_popup("Invalid JSON short | RESET")
    else:
        st.session_state.edit_configv7_short = json.dumps(self.bot["short"], indent=4)
    # Display config
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        st.number_input("long twe", min_value=0.0, max_value=100.0, step=0.05, format="%.2f", key="edit_configv7_long_twe", help=pbgui_help.total_wallet_exposure_limit)
    with col2:
        st.number_input("long positions", min_value=0.0, max_value=100.0, step=1.0, format="%.2f", key="edit_configv7_long_positions", help=pbgui_help.n_positions)
    with col3:
        st.number_input("short twe", min_value=0.0, max_value=100.0, step=0.05, format="%.2f", key="edit_configv7_short_twe", help=pbgui_help.total_wallet_exposure_limit)
    with col4:
        st.number_input("short positions", min_value=0.0, max_value=100.0, step=1.0, format="%.2f", key="edit_configv7_short_positions", help=pbgui_help.n_positions)
    col1, col2 = st.columns([1,1])
    with col1:
        st.text_area(f'long', key="edit_configv7_long", height=600)
    with col2:
        st.text_area(f'short', key="edit_configv7_short", height=600)

def edit_cf(self):
    # Init session_state for keys
    if "edit_cf_configv7_long" in st.session_state:
        if st.session_state.edit_cf_configv7_long != json.dumps(self.bot["long"], indent=4):
            try:
                self.long = json.loads(st.session_state.edit_cf_configv7_long)
            except:
                error_popup("Invalid JSON | RESET")
    else:
        st.session_state.edit_cf_configv7_long = json.dumps(self.bot["long"], indent=4)
    if "edit_cf_configv7_short" in st.session_state:
        if st.session_state.edit_cf_configv7_short != json.dumps(self.bot["short"], indent=4):
            try:
                self.short = json.loads(st.session_state.edit_cf_configv7_short)
            except:
                error_popup("Invalid JSON | RESET")
    else:
        st.session_state.edit_cf_configv7_short = json.dumps(self.bot["short"], indent=4)
    col1, col2 = st.columns([1,1])
    with col1:
        st.text_area(f'long', key="edit_cf_configv7_long", height=640)
    with col2:
        st.text_area(f'short', key="edit_cf_configv7_short", height=640)

def edit_co(self):
    # Init session_state for keys
    if "edit_co_configv7_long" in st.session_state:
        if st.session_state.edit_co_configv7_long != json.dumps(self.bot["long"], indent=4):
            try:
                self.long = json.loads(st.session_state.edit_co_configv7_long)
            except:
                error_popup("Invalid JSON | RESET")
    else:
        st.session_state.edit_co_configv7_long = json.dumps(self.bot["long"], indent=4)
    if "edit_co_configv7_short" in st.session_state:
        if st.session_state.edit_co_configv7_short != json.dumps(self.bot["short"], indent=4):
            try:
                self.short = json.loads(st.session_state.edit_co_configv7_short)
            except:
                error_popup("Invalid JSON | RESET")
    else:
        st.session_state.edit_co_configv7_short = json.dumps(self.bot["short"], indent=4)
    col1, col2 = st.columns([1,1])
    with col1:
        st.text_area(f'long', key="edit_co_configv7_long", height=640)
    with col2:
        st.text_area(f'short', key="edit_co_configv7_short", height=640)
