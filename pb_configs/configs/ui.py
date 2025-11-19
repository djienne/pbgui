import streamlit as st
import pandas as pd
import json
from pathlib import Path
from time import sleep
import math
import traceback
from pbgui.configs.model import ConfigV7
from pbgui_help import pbgui_help
from pbgui_func import error_popup
from exchanges.constants import V7
from Exchange import Exchange
from PBCoinData import CoinData
from pbgui_func import validateJSON

class ConfigUI:
    def __init__(self, config_model: ConfigV7 = None):
        self.config_model = config_model

    def edit_config(self, config_instance):
        # Init session_state for keys
        if "config_long_enabled" in st.session_state:
            if st.session_state.config_long_enabled != config_instance.long_enabled:
                config_instance.long_enabled = st.session_state.config_long_enabled
                if config_instance.config:
                    st.session_state.config_instance_config = config_instance.config
        if "config_short_enabled" in st.session_state:
            if st.session_state.config_short_enabled != config_instance.short_enabled:
                config_instance.short_enabled = st.session_state.config_short_enabled
                if config_instance.config:
                    st.session_state.config_instance_config = config_instance.config
        if "config_long_we" in st.session_state:
            if st.session_state.config_long_we != config_instance.long_we:
                config_instance.long_we = st.session_state.config_long_we
                if config_instance.config:
                    st.session_state.config_instance_config = config_instance.config
        if "config_short_we" in st.session_state:
            if st.session_state.config_short_we != config_instance.short_we:
                config_instance.short_we = st.session_state.config_short_we
                if config_instance.config:
                    st.session_state.config_instance_config = config_instance.config
        if "config_preview_grid" in st.session_state:
            if st.session_state.config_preview_grid != config_instance.preview_grid:
                config_instance.preview_grid = st.session_state.config_preview_grid
        if "config_instance_config" in st.session_state:
            if st.session_state.config_instance_config != config_instance.config:
                config_instance.config = st.session_state.config_instance_config
                st.session_state.config_long_enabled = config_instance.long_enabled
                st.session_state.config_short_enabled = config_instance.short_enabled
                st.session_state.config_long_we = config_instance.long_we
                st.session_state.config_short_we = config_instance.short_we
            else:
                if validateJSON(st.session_state.config_instance_config):
                    if "error_config" in st.session_state:
                        del st.session_state.error_config
        # if config_instance.config:
        #     config_instance.config = st.session_state.config_instance_config
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.toggle("Long enabled", value=config_instance.long_enabled, key="config_long_enabled", help=None)
            st.number_input("LONG_WALLET_EXPOSURE_LIMIT", min_value=0.0, max_value=100.0, value=float(round(config_instance.long_we,2)), step=0.05, format="%.2f", key="config_long_we", help=pbgui_help.exposure)
        with col2:
            st.toggle("Short enabled", value=config_instance.short_enabled, key="config_short_enabled", help=None)
            st.number_input("SHORT_WALLET_EXPOSURE_LIMIT", min_value=0.0, max_value=100.0, value=float(round(config_instance.short_we,2)), step=0.05, format="%.2f", key="config_short_we", help=pbgui_help.exposure)
        with col3:
            st.toggle("Preview Grid", value=config_instance.preview_grid, key="config_preview_grid", help=None)
            st.selectbox("Config Type", [config_instance.type], index=0, key="config_type", help=None, disabled=True)
        # Init height and color with defaults
        height = 600
        color = None
        # Display Error
        if "error_config" in st.session_state:
            st.error(st.session_state.error_config, icon="🚨")
            color = "red"
        if not config_instance.config is None:
            height = len(config_instance.config.splitlines()) *23
        if height < 600:
            height = 600
        if not config_instance.config:
            color = "red"
        col1, col2 = st.columns([1,1])
        with col1:
            if color:
                st.text_area(f':{color}[config]', config_instance.config, key="config_instance_config", height=height)
            else:
                st.text_area(f'config', config_instance.config, key="config_instance_config", height=height)
        with col2:
            st.text_area(f'config converted to v7', str(config_instance.config_v7), key="config_instance_config_v7", height=height, disabled=True)


    @st.fragment
    def edit_bot(self):
        # Init session_state for keys
        if "edit_configv7_long_twe" in st.session_state:
            if st.session_state.edit_configv7_long_twe != self.config_model.bot.long.total_wallet_exposure_limit:
                self.config_model.bot.long.total_wallet_exposure_limit = round(st.session_state.edit_configv7_long_twe,2)
                st.session_state.edit_configv7_long = json.dumps(self.config_model.bot.bot["long"], indent=4)
            if "edit_configv7_long" in st.session_state:
                try:
                    long = json.loads(st.session_state.edit_configv7_long)
                    if st.session_state.edit_configv7_long_twe != float(long["total_wallet_exposure_limit"]):
                        st.session_state.edit_configv7_long_twe = float(long["total_wallet_exposure_limit"])
                except:
                    st.session_state.edit_configv7_long = json.dumps(self.config_model.bot.bot["long"], indent=4)
                    error_popup("Invalid JSON long | RESET")
        else:
            st.session_state.edit_configv7_long_twe = float(self.config_model.bot.long.total_wallet_exposure_limit)

        if "edit_configv7_long_positions" in st.session_state:
            if st.session_state.edit_configv7_long_positions != self.config_model.bot.long.n_positions:
                self.config_model.bot.long.n_positions = round(st.session_state.edit_configv7_long_positions,0)
                st.session_state.edit_configv7_long = json.dumps(self.config_model.bot.bot["long"], indent=4)
            if "edit_configv7_long" in st.session_state:
                try:
                    long = json.loads(st.session_state.edit_configv7_long)
                    if st.session_state.edit_configv7_long_positions != float(long["n_positions"]):
                        st.session_state.edit_configv7_long_positions = float(long["n_positions"])
                except:
                    st.session_state.edit_configv7_long = json.dumps(self.config_model.bot.bot["long"], indent=4)
                    error_popup("Invalid JSON long | RESET")
        else:
            st.session_state.edit_configv7_long_positions = float(self.config_model.bot.long.n_positions)

        if "edit_configv7_short_twe" in st.session_state:
            if st.session_state.edit_configv7_short_twe != self.config_model.bot.short.total_wallet_exposure_limit:
                self.config_model.bot.short.total_wallet_exposure_limit = round(st.session_state.edit_configv7_short_twe,2)
                st.session_state.edit_configv7_short = json.dumps(self.config_model.bot.bot["short"], indent=4)
            if "edit_configv7_short" in st.session_state:
                try:
                    short = json.loads(st.session_state.edit_configv7_short)
                    if st.session_state.edit_configv7_short_twe != float(short["total_wallet_exposure_limit"]):
                        st.session_state.edit_configv7_short_twe = float(short["total_wallet_exposure_limit"])
                except:
                    st.session_state.edit_configv7_short = json.dumps(self.config_model.bot.bot["short"], indent=4)
                    error_popup("Invalid JSON short | RESET")
        else:
            st.session_state.edit_configv7_short_twe = float(self.config_model.bot.short.total_wallet_exposure_limit)

        if "edit_configv7_short_positions" in st.session_state:
            if st.session_state.edit_configv7_short_positions != self.config_model.bot.short.n_positions:
                self.config_model.bot.short.n_positions = round(st.session_state.edit_configv7_short_positions,0)
                st.session_state.edit_configv7_short = json.dumps(self.config_model.bot.bot["short"], indent=4)
            if "edit_configv7_short" in st.session_state:
                try:
                    short = json.loads(st.session_state.edit_configv7_short)
                    if st.session_state.edit_configv7_short_positions != float(short["n_positions"]):
                        st.session_state.edit_configv7_short_positions = float(short["n_positions"])
                except:
                    st.session_state.edit_configv7_short = json.dumps(self.config_model.bot.bot["short"], indent=4)
                    error_popup("Invalid JSON short | RESET")   
        else:
            st.session_state.edit_configv7_short_positions = float(self.config_model.bot.short.n_positions)

        if "edit_configv7_long" in st.session_state:
            if st.session_state.edit_configv7_long != json.dumps(self.config_model.bot.bot["long"], indent=4):
                try:
                    self.config_model.bot.long.long = json.loads(st.session_state.edit_configv7_long)
                except:
                    st.session_state.edit_configv7_long = json.dumps(self.config_model.bot.bot["long"], indent=4)
                    error_popup("Invalid JSON long | RESET")
        else:
            st.session_state.edit_configv7_long = json.dumps(self.config_model.bot.bot["long"], indent=4)

        if "edit_configv7_short" in st.session_state:
            if st.session_state.edit_configv7_short != json.dumps(self.config_model.bot.bot["short"], indent=4):
                try:
                    self.config_model.bot.short.short = json.loads(st.session_state.edit_configv7_short)
                except:
                    st.session_state.edit_configv7_short = json.dumps(self.config_model.bot.bot["short"], indent=4)
                    error_popup("Invalid JSON short | RESET")
        else:
            st.session_state.edit_configv7_short = json.dumps(self.config_model.bot.bot["short"], indent=4)
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

    def edit_bot_cf(self):
        # Init session_state for keys
        if "edit_cf_configv7_long" in st.session_state:
            if st.session_state.edit_cf_configv7_long != json.dumps(self.config_model.bot.bot["long"], indent=4):
                try:
                    self.config_model.bot.long.long = json.loads(st.session_state.edit_cf_configv7_long)
                except:
                    error_popup("Invalid JSON | RESET")
        else:
            st.session_state.edit_cf_configv7_long = json.dumps(self.config_model.bot.bot["long"], indent=4)
        if "edit_cf_configv7_short" in st.session_state:
            if st.session_state.edit_cf_configv7_short != json.dumps(self.config_model.bot.bot["short"], indent=4):
                try:
                    self.config_model.bot.short.short = json.loads(st.session_state.edit_cf_configv7_short)
                except:
                    error_popup("Invalid JSON | RESET")
        else:
            st.session_state.edit_cf_configv7_short = json.dumps(self.config_model.bot.bot["short"], indent=4)
        col1, col2 = st.columns([1,1])
        with col1:
            st.text_area(f'long', key="edit_cf_configv7_long", height=640)
        with col2:
            st.text_area(f'short', key="edit_cf_configv7_short", height=640)
    
    def edit_bot_co(self):
        # Init session_state for keys
        if "edit_co_configv7_long" in st.session_state:
            if st.session_state.edit_co_configv7_long != json.dumps(self.config_model.bot.bot["long"], indent=4):
                try:
                    self.config_model.bot.long.long = json.loads(st.session_state.edit_co_configv7_long)
                except:
                    error_popup("Invalid JSON | RESET")
        else:
            st.session_state.edit_co_configv7_long = json.dumps(self.config_model.bot.bot["long"], indent=4)
        if "edit_co_configv7_short" in st.session_state:
            if st.session_state.edit_co_configv7_short != json.dumps(self.config_model.bot.bot["short"], indent=4):
                try:
                    self.config_model.bot.short.short = json.loads(st.session_state.edit_co_configv7_short)
                except:
                    error_popup("Invalid JSON | RESET")
        else:
            st.session_state.edit_co_configv7_short = json.dumps(self.config_model.bot.bot["short"], indent=4)
        col1, col2 = st.columns([1,1])
        with col1:
            st.text_area(f'long', key="edit_co_configv7_long", height=640)
        with col2:
            st.text_area(f'short', key="edit_co_configv7_short", height=640)

    def view_coin_overrides(self):
        if self.config_model.config["coin_overrides"]:
            overrides = True
        else:
            overrides = False
        with st.expander("Coin Overrides", expanded=overrides):
            # Init
            if not "ed_key" in st.session_state:
                st.session_state.ed_key = 0
            ed_key = st.session_state.ed_key
            if f'select_coins_{ed_key}' in st.session_state:
                ed = st.session_state[f'select_coins_{ed_key}']
                for row in ed["edited_rows"]:
                    if "edit" in ed["edited_rows"][row]:
                        if ed["edited_rows"][row]["edit"]:
                            st.session_state.edit_coin_override = st.session_state.co_data[row]["coin"]
            # if not "co_data" in st.session_state:
            co_data = []
            if self.config_model.config["coin_overrides"]:
                for coin in self.config_model.config["coin_overrides"]:
                    co_data.append({
                        'edit': False,
                        'coin': coin,
                        'override_config_path': self.config_model.config["coin_overrides"][coin].get('override_config_path', False),
                        'config.bot.long parameters': self.config_model.config["coin_overrides"][coin].get('bot', {}).get('long', {}),
                        'config.bot.short parameters': self.config_model.config["coin_overrides"][coin].get('bot', {}).get('short', {}),
                        'config.live parameters': self.config_model.config["coin_overrides"][coin].get('live', {}),
                    })
            st.session_state.co_data = co_data
            # Display coin_overrides
            if st.session_state.co_data and not "edit_coin_override" in st.session_state:
                d = st.session_state.co_data
                st.data_editor(data=d, height=36+(len(d))*35, key=f'select_coins_{ed_key}', disabled=['coin', 'override_config_path', 'config.bot.long parameters', 'config.bot.short parameters', 'config.live parameters'])
            if "edit_run_v7_add_coin_override_button" in st.session_state:
                if st.session_state.edit_run_v7_add_coin_override_button:
                    if self.config_model.config_file is None:
                        error_popup("Please save config, before editing coin overrides.")
                    else:
                        st.session_state.edit_coin_override = st.session_state.edit_run_v7_add_coin_override
                        st.rerun()
            if "edit_coin_override" in st.session_state:
                self.edit_coin_override(st.session_state.edit_coin_override)
            else:
                col1, col2, col3, col4 = st.columns([1,1,1,1], vertical_alignment="bottom")
                with col1:
                    st.selectbox('Symbol', st.session_state.pbcoindata.symbols, key="edit_run_v7_add_coin_override")
                with col2:
                    st.button("Add Coin Override", key="edit_run_v7_add_coin_override_button")

    def edit_coin_override(self, symbol):
        # reove USDT or USDC from symbol
        # if symbol.endswith("USDT"):
        #     symbol = symbol[:-4]
        # elif symbol.endswith("USDC"):
        #     symbol = symbol[:-4]
        OVERRIDES_LIVE = [
            "forced_mode_long",
            "forced_mode_short",
            "leverage"
        ]
        OVERRIDES = [
            "close_grid_markup_end",
            "close_grid_markup_start",
            "close_grid_qty_pct",
            "close_trailing_grid_ratio",
            "close_trailing_qty_pct",
            "close_trailing_retracement_pct",
            "close_trailing_threshold_pct",
            "ema_span_0",
            "ema_span_1",
            "enforce_exposure_limit",
            "entry_grid_double_down_factor",
            "entry_grid_spacing_log_span_hours",
            "entry_grid_spacing_log_weight",
            "entry_grid_spacing_pct",
            "entry_grid_spacing_we_weight",
            "entry_initial_ema_dist",
            "entry_initial_qty_pct",
            "entry_trailing_double_down_factor",
            "entry_trailing_grid_ratio",
            "entry_trailing_retracement_pct",
            "entry_trailing_threshold_pct",
            "unstuck_close_pct",
            "unstuck_ema_dist",
            "unstuck_threshold",
            "wallet_exposure_limit"
        ]
        MODE = [
            "normal",
            "manual",
            "graceful_stop",
            "panic",
            "tp_only"
        ]
        # Init
        if not "ed_key" in st.session_state:
            st.session_state.ed_key = 0
        ed_key = st.session_state.ed_key
        if f'edit_run_v7_co_parameters_{ed_key}' in st.session_state:
            ed = st.session_state[f'edit_run_v7_co_parameters_{ed_key}']
            for row in ed["edited_rows"]:
                if "delete" in ed["edited_rows"][row]:
                    if ed["edited_rows"][row]["delete"]:
                        if st.session_state.co_parameters[row]["section"] == "bot":
                            self.config_model.config["coin_overrides"][symbol]["bot"][st.session_state.co_parameters[row]["side"]].pop(st.session_state.co_parameters[row]["parameter"])
                            # cleanup empty sections
                            if self.config_model.config["coin_overrides"][symbol]["bot"][st.session_state.co_parameters[row]["side"]] == {}:
                                del self.config_model.config["coin_overrides"][symbol]["bot"][st.session_state.co_parameters[row]["side"]]
                            if self.config_model.config["coin_overrides"][symbol]["bot"] == {}:
                                del self.config_model.config["coin_overrides"][symbol]["bot"]
                        elif st.session_state.co_parameters[row]["section"] == "live":
                            self.config_model.config["coin_overrides"][symbol]["live"].pop(st.session_state.co_parameters[row]["parameter"])
                            # cleanup empty sections
                            if self.config_model.config["coin_overrides"][symbol]["live"] == {}:
                                del self.config_model.config["coin_overrides"][symbol]["live"]
                        # clear co_parameters
                        if "co_parameters" in st.session_state:
                            del st.session_state.co_parameters
                        st.rerun()

        config = False
        # Init from config
        if self.config_model.config["coin_overrides"] and "edit_run_v7_co_config" not in st.session_state:
            if symbol in self.config_model.config["coin_overrides"]:
                if "override_config_path" in self.config_model.config["coin_overrides"][symbol]:
                    config = True
                    if "co_config" not in st.session_state:
                        st.session_state.co_config = ConfigV7(file_name=Path(Path(self.config_model.config_file).parent, f'{symbol}.json'))
                        st.session_state.co_config.load_config()
                        if "edit_co_configv7_long" in st.session_state:
                            del st.session_state.edit_co_configv7_long
                        if "edit_co_configv7_short" in st.session_state:
                            del st.session_state.edit_co_configv7_short
        # Init session_state for keys
        if "edit_run_v7_co_config" in st.session_state:
            if st.session_state.edit_run_v7_co_config != config:
                config = st.session_state.edit_run_v7_co_config
        if "edit_run_v7_co_parameter" in st.session_state:
            if st.session_state.edit_run_v7_co_add_parameter and st.session_state.edit_run_v7_co_side and st.session_state.edit_run_v7_co_value:
                # Ensure nested dicts exist
                if symbol not in self.config_model.config["coin_overrides"]:
                    self.config_model.config["coin_overrides"][symbol] = {}
                if "bot" not in self.config_model.config["coin_overrides"][symbol]:
                    self.config_model.config["coin_overrides"][symbol]["bot"] = {}
                if st.session_state.edit_run_v7_co_side not in self.config_model.config["coin_overrides"][symbol]["bot"]:
                    self.config_model.config["coin_overrides"][symbol]["bot"][st.session_state.edit_run_v7_co_side] = {}
                self.config_model.config["coin_overrides"][symbol]["bot"][st.session_state.edit_run_v7_co_side][st.session_state.edit_run_v7_co_parameter] = st.session_state.edit_run_v7_co_value
                if "co_parameters" in st.session_state:
                    del st.session_state.co_parameters
        if "edit_run_v7_co_parameter_live" in st.session_state:
            if st.session_state.edit_run_v7_co_add_parameter_live and st.session_state.edit_run_v7_co_value_live:
                # Ensure nested dicts exist
                if symbol not in self.config_model.config["coin_overrides"]:
                    self.config_model.config["coin_overrides"][symbol] = {}
                if "live" not in self.config_model.config["coin_overrides"][symbol]:
                    self.config_model.config["coin_overrides"][symbol]["live"] = {}
                self.config_model.config["coin_overrides"][symbol]["live"][st.session_state.edit_run_v7_co_parameter_live] = st.session_state.edit_run_v7_co_value_live
                if "co_parameters" in st.session_state:
                    del st.session_state.co_parameters
        if not "co_parameters" in st.session_state:
            co_parameters = []
            for parameter in self.config_model.config["coin_overrides"].get(symbol, {}).get('bot', {}).get('long', {}):
                co_parameters.append({
                    'section': 'bot',
                    'parameter': parameter,
                    'side': 'long',
                    'value': self.config_model.config["coin_overrides"][symbol]['bot']['long'][parameter],
                    'delete': False,
                })
            for parameter in self.config_model.config["coin_overrides"].get(symbol, {}).get('bot', {}).get('short', {}):
                co_parameters.append({
                    'section': 'bot',
                    'parameter': parameter,
                    'side': 'short',
                    'value': self.config_model.config["coin_overrides"][symbol]['bot']['short'][parameter],
                    'delete': False,
                })
            for parameter in self.config_model.config["coin_overrides"].get(symbol, {}).get('live', {}):
                co_parameters.append({
                    'section': 'live',
                    'parameter': parameter,
                    'side': 'live',
                    'value': self.config_model.config["coin_overrides"][symbol]['live'][parameter],
                    'delete': False,
                })
            st.session_state.co_parameters = co_parameters
        # Display coin_overrides
        st.write(f"{symbol}")
        if st.session_state.co_parameters:
            d = st.session_state.co_parameters
            st.data_editor(data=d, height=36+(len(d))*35, key=f'edit_run_v7_co_parameters_{ed_key}', disabled=['parameter', 'side', 'value'])
        # config.live parameters
        col1, col2, col3, col4 = st.columns([1,1,1,3], vertical_alignment="bottom")
        with col1:
            st.selectbox('config.live override parameter', OVERRIDES_LIVE, key="edit_run_v7_co_parameter_live")
        with col2:
            if st.session_state.edit_run_v7_co_parameter_live == "leverage":
                st.number_input("value", min_value=0.0, max_value=100.0, step=1.0, format="%.1f", key="edit_run_v7_co_value_live")
            else:
                st.selectbox("mode", MODE, key="edit_run_v7_co_value_live")
        with col3:
            st.button("Add", key="edit_run_v7_co_add_parameter_live")

        # config.bot parameters
        col1, col2, col3, col4 = st.columns([1,1,1,3], vertical_alignment="bottom")
        with col1:
            st.selectbox('config.bot override parameter', OVERRIDES, key="edit_run_v7_co_parameter")
        with col2:
            st.selectbox("side", ["long", "short"], key="edit_run_v7_co_side")
        with col3:
            if st.session_state.edit_run_v7_co_parameter == "enforce_exposure_limit":
                st.selectbox("enforce_exposure_limit", ["true", "false"], key="edit_run_v7_co_value")
            else:
                st.number_input("value", format="%.8f", key="edit_run_v7_co_value")
        with col4:
            st.button("Add", key="edit_run_v7_co_add_parameter")

        st.checkbox("Config", value=config, key="edit_run_v7_co_config", help=pbgui_help.coin_overrides_config)
        if config:
            if "co_config" not in st.session_state:
                st.session_state.co_config = ConfigV7()
            # Create a temporary ConfigUI for the co_config to edit it
            co_config_ui = ConfigUI(st.session_state.co_config)
            co_config_ui.edit_bot_co()
        # print(self.config.coin_overrides)
        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1], vertical_alignment="bottom")
        with col1:
            if st.button("OK"):
                # {"COIN1": {"override_config_path": "path/to/override_config.json"}}
                # {"COIN2": {"override_config_path": "path/to/other_override_config.json", {"bot": {"long": {"close_grid_markup_start": 0.005}}}}}
                # {"COIN3": {"bot": {"short": {"entry_initial_qty_pct": 0.01}}, "live": {"forced_mode_long": "panic"}}}
                if st.session_state.edit_run_v7_co_config:
                    st.session_state.co_config.config_file = Path(Path(self.config_model.config_file).parent, f'{symbol}.json')
                    st.session_state.co_config.save_config()
                    if symbol not in self.config_model.config["coin_overrides"]:
                        self.config_model.config["coin_overrides"][symbol] = {}
                    self.config_model.config["coin_overrides"][symbol]["override_config_path"] = f'{symbol}.json'
                else:
                    Path(Path(self.config_model.config_file).parent, f'{symbol}.json').unlink(missing_ok=True)
                    if symbol in self.config_model.config["coin_overrides"]:
                        if "override_config_path" in self.config_model.config["coin_overrides"][symbol]:
                            del self.config_model.config["coin_overrides"][symbol]["override_config_path"]
                # Remove symbol from coin_overrides if it has no parameters
                if symbol in self.config_model.config["coin_overrides"] and self.config_model.config["coin_overrides"][symbol] == {}:
                    del self.config_model.config["coin_overrides"][symbol]
                # self.save()
                self.clean_co_session_state()
                st.rerun()
        with col2:
            if st.button("Cancel"):
                self.clean_co_session_state()
                st.rerun()
        with col3:
            if st.button("Remove"):
                if self.config_model.config["coin_overrides"]:
                    if symbol in self.config_model.config["coin_overrides"]:
                        del self.config_model.config["coin_overrides"][symbol]
                Path(Path(self.config_model.config_file).parent, f'{symbol}.json').unlink(missing_ok=True)
                # self.save()
                self.clean_co_session_state()
                st.rerun()

    def clean_co_session_state(self):
        if "co_config" in st.session_state:
            del st.session_state.co_config
        if "edit_run_v7_co_config" in st.session_state:
            del st.session_state.edit_run_v7_co_config
        if "edit_coin_override" in st.session_state:
            del st.session_state.edit_coin_override
        if "co_data" in st.session_state:
            del st.session_state.co_data
        if "ed_key" in st.session_state:
            st.session_state.ed_key += 1
        if "co_parameters" in st.session_state:
            del st.session_state.co_parameters
        if "edit_run_v7_co_parameter" in st.session_state:
            del st.session_state.edit_run_v7_co_parameter
        if "edit_run_v7_co_parameter_live" in st.session_state:
            del st.session_state.edit_run_v7_co_parameter_live
        if "edit_run_v7_co_side" in st.session_state:
            del st.session_state.edit_run_v7_co_side
        if "edit_run_v7_co_value" in st.session_state:
            del st.session_state.edit_run_v7_co_value
        if "edit_run_v7_co_value_live" in st.session_state:
            del st.session_state.edit_run_v7_co_value_live

class BalanceCalculator:
    def __init__(self, config_file: str = None):
        self.config = ConfigV7()
        if config_file:
            self.config.config_file = config_file
            self.config.load_config()
        self.exchange = Exchange("binance", None)
        self.coin_infos = []
        self.balance_long = []
        self.balance_short = []
    
    @property
    def balance(self):
        return self.balance_long + self.balance_short

    def init_coindata(self):
        if "pbcoindata" not in st.session_state:
            st.session_state.pbcoindata = CoinData()
        st.session_state.pbcoindata.exchange = self.exchange.id
        if self.config.pbgui.dynamic_ignore:
            st.session_state.pbcoindata.tags = self.config.pbgui.tags
            st.session_state.pbcoindata.only_cpt = self.config.pbgui.only_cpt
            st.session_state.pbcoindata.market_cap = self.config.pbgui.market_cap
            st.session_state.pbcoindata.vol_mcap = self.config.pbgui.vol_mcap
            st.session_state.pbcoindata.notices_ignore = self.config.pbgui.notices_ignore
            self.config.live.approved_coins = st.session_state.pbcoindata.approved_coins

    def view(self):
        # Init coindata
        self.init_coindata()
        if "edit_bc_config" in st.session_state:
            if st.session_state.edit_bc_config != json.dumps(self.config.config, indent=4):
                try:
                    self.config.config = json.loads(st.session_state.edit_bc_config)
                    self.init_coindata()
                except:
                    error_popup("Invalid JSON")
                    st.session_state.edit_bc_config = json.dumps(self.config.config, indent=4)
        else:
            st.session_state.edit_bc_config = json.dumps(self.config.config, indent=4)

        if "bc_exchange_id" in st.session_state:
            if st.session_state.bc_exchange_id != self.exchange.id:
                self.exchange = Exchange(st.session_state.bc_exchange_id, None)
                # st.session_state.bc_exchange = bc_exchange
        else:
            if self.config.backtest.exchanges:
                st.session_state.bc_exchange_id = self.config.backtest.exchanges[0]
        col1, col2 = st.columns([1, 1])
        with col1:
            st.text_area(f'config', key="edit_bc_config", height=500)
        with col2:
            st.markdown("### Balance Calculator")
            st.markdown("This tool allows you to calculate the balance for a given configuration.")
            st.markdown("You can edit the configuration in the left text area and click on 'Calculate' to see the results.")
            st.selectbox("Exchange", V7.list(), key="bc_exchange_id")
            if st.button("Calculate"):
                coins = set(self.config.live.approved_coins.long + self.config.live.approved_coins.short)
                self.coin_infos = []
                self.balance_long = []
                self.balance_short = []
                with st.spinner(text=f'fetching coin infos from exchange...'):
                    with st.empty():
                        for counter, coin in enumerate(coins):
                            st.text(f'{counter + 1}/{len(coins)}: {coin}')
                            min_order_price, price, contractSize, min_amount, min_cost, lev = self.exchange.fetch_symbol_infos(coin)
                            self.coin_infos.append({
                                "coin": coin,
                                "currentPrice": price,
                                "contractSize": contractSize,
                                "min_amount": min_amount,
                                "min_cost": min_cost,
                                "min_order_price": min_order_price,
                                "max lev": lev
                            })
                            if coin in self.config.live.approved_coins.long:
                                if self.config.bot.long.n_positions > 0 and self.config.bot.long.total_wallet_exposure_limit > 0:
                                    we = self.config.bot.long.total_wallet_exposure_limit / self.config.bot.long.n_positions
                                    balance = min_order_price / (we * self.config.bot.long.entry_initial_qty_pct)
                                    self.balance_long.append({
                                        "coin": coin,
                                        "balance": balance
                                    })
                            if coin in self.config.live.approved_coins.short:
                                if self.config.bot.short.n_positions > 0 and self.config.bot.short.total_wallet_exposure_limit > 0:
                                    we = self.config.bot.short.total_wallet_exposure_limit / self.config.bot.short.n_positions
                                    balance = min_order_price / (we * self.config.bot.short.entry_initial_qty_pct)
                                    self.balance_short.append({
                                        "coin": coin,
                                        "balance": balance
                                    })
                            sleep(0.1)  # to avoid rate limit issues

        # sort coin_infos by min_order_price
        self.coin_infos = sorted(self.coin_infos, key=lambda x: x['min_order_price'], reverse=True)
        if self.coin_infos:
            st.write("### Coin Information")
            st.dataframe(self.coin_infos, hide_index=True)

        # find highest balance in short and long
        self.balance_long = sorted(self.balance_long, key=lambda x: x['balance'], reverse=True)
        self.balance_short = sorted(self.balance_short, key=lambda x: x['balance'], reverse=True)
        side = None
        if self.balance_long:
            if self.balance_short:
                if self.balance_long[0]['balance'] > self.balance_short[0]['balance']:
                    side = "long"
                else:
                    side = "short"
            else:
                side = "long"
        else:
            if self.balance_short:
                side = "short"
        if side in ["long", "short"]:
            # Select the correct attributes based on side
            balance_list = self.balance_long if side == "long" else self.balance_short
            bot_side = self.config.bot.long if side == "long" else self.config.bot.short
            # Get symbol name with highest balance
            symbol = balance_list[0]['coin']
            # get min order price for symbol from coin_infos
            min_order_price = next((coin['min_order_price'] for coin in self.coin_infos if coin['coin'] == symbol), 0)
            # Display calculated balance with formula
            st.write(f"### Balance needed for {symbol} ({side.capitalize()} Side)")
            st.write(f"**Minimum Order Price:** `{min_order_price:.2f}`")
            st.write(f"**Total Wallet Exposure Limit:** `{bot_side.total_wallet_exposure_limit:.2f}`")
            st.write(f"**Number of Positions:** `{bot_side.n_positions}`")
            st.write(f"**Entry Initial Quantity Percentage:** `{bot_side.entry_initial_qty_pct:.2f}`")
            st.write(f"To calculate the balance needed for {symbol} on the {side} side, use the formula:")
            st.write(f"**Formula:** `min_order_price / ((total_wallet_exposure_limit / n_positions) * entry_initial_qty_pct)`")
            result = min_order_price / ((bot_side.total_wallet_exposure_limit / bot_side.n_positions) * bot_side.entry_initial_qty_pct)
            st.write(f"**Calculation:** `{min_order_price} / (({bot_side.total_wallet_exposure_limit} / {bot_side.n_positions}) * {bot_side.entry_initial_qty_pct}) = {result:.2f}`")
            recommended_balance = math.ceil(result * 1.1 / 10) * 10
            st.write(f"### Recommended Balance (10% more): :green[{int(recommended_balance)} USDT]")
