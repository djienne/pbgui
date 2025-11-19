import streamlit as st
from pathlib import Path
from ..pbgui_func import error_popup
import pbgui_help
from ..configs.v7.config import ConfigV7

def view_coin_overrides(self):
    if self.config["coin_overrides"]:
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
        if self.config["coin_overrides"]:
            for coin in self.config["coin_overrides"]:
                co_data.append({
                    'edit': False,
                    'coin': coin,
                    'override_config_path': self.config["coin_overrides"][coin].get('override_config_path', False),
                    'config.bot.long parameters': self.config["coin_overrides"][coin].get('bot', {}).get('long', {}),
                    'config.bot.short parameters': self.config["coin_overrides"][coin].get('bot', {}).get('short', {}),
                    'config.live parameters': self.config["coin_overrides"][coin].get('live', {}),
                })
        st.session_state.co_data = co_data
        # Display coin_overrides
        if st.session_state.co_data and not "edit_coin_override" in st.session_state:
            d = st.session_state.co_data
            st.data_editor(data=d, height=36+(len(d))*35, key=f'select_coins_{ed_key}', disabled=['coin', 'override_config_path', 'config.bot.long parameters', 'config.bot.short parameters', 'config.live parameters'])
        if "edit_run_v7_add_coin_override_button" in st.session_state:
            if st.session_state.edit_run_v7_add_coin_override_button:
                if self.config_file is None:
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
                        self.config["coin_overrides"][symbol]["bot"][st.session_state.co_parameters[row]["side"]].pop(st.session_state.co_parameters[row]["parameter"])
                        # cleanup empty sections
                        if self.config["coin_overrides"][symbol]["bot"][st.session_state.co_parameters[row]["side"]] == {}:
                            del self.config["coin_overrides"][symbol]["bot"][st.session_state.co_parameters[row]["side"]]
                        if self.config["coin_overrides"][symbol]["bot"] == {}:
                            del self.config["coin_overrides"][symbol]["bot"]
                    elif st.session_state.co_parameters[row]["section"] == "live":
                        self.config["coin_overrides"][symbol]["live"].pop(st.session_state.co_parameters[row]["parameter"])
                        # cleanup empty sections
                        if self.config["coin_overrides"][symbol]["live"] == {}:
                            del self.config["coin_overrides"][symbol]["live"]
                    # clear co_parameters
                    if "co_parameters" in st.session_state:
                        del st.session_state.co_parameters
                    st.rerun()

    config = False
    # Init from config
    if self.config["coin_overrides"] and "edit_run_v7_co_config" not in st.session_state:
        if symbol in self.config["coin_overrides"]:
            if "override_config_path" in self.config["coin_overrides"][symbol]:
                config = True
                if "co_config" not in st.session_state:
                    st.session_state.co_config = ConfigV7(file_name=Path(Path(self.config_file).parent, f'{symbol}.json'))
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
            if symbol not in self.config["coin_overrides"]:
                self.config["coin_overrides"][symbol] = {}
            if "bot" not in self.config["coin_overrides"][symbol]:
                self.config["coin_overrides"][symbol]["bot"] = {}
            if st.session_state.edit_run_v7_co_side not in self.config["coin_overrides"][symbol]["bot"]:
                self.config["coin_overrides"][symbol]["bot"][st.session_state.edit_run_v7_co_side] = {}
            self.config["coin_overrides"][symbol]["bot"][st.session_state.edit_run_v7_co_side][st.session_state.edit_run_v7_co_parameter] = st.session_state.edit_run_v7_co_value
            if "co_parameters" in st.session_state:
                del st.session_state.co_parameters
    if "edit_run_v7_co_parameter_live" in st.session_state:
        if st.session_state.edit_run_v7_co_add_parameter_live and st.session_state.edit_run_v7_co_value_live:
            # Ensure nested dicts exist
            if symbol not in self.config["coin_overrides"]:
                self.config["coin_overrides"][symbol] = {}
            if "live" not in self.config["coin_overrides"][symbol]:
                self.config["coin_overrides"][symbol]["live"] = {}
            self.config["coin_overrides"][symbol]["live"][st.session_state.edit_run_v7_co_parameter_live] = st.session_state.edit_run_v7_co_value_live
            if "co_parameters" in st.session_state:
                del st.session_state.co_parameters
    if not "co_parameters" in st.session_state:
        co_parameters = []
        for parameter in self.config["coin_overrides"].get(symbol, {}).get('bot', {}).get('long', {}):
            co_parameters.append({
                'section': 'bot',
                'parameter': parameter,
                'side': 'long',
                'value': self.config["coin_overrides"][symbol]['bot']['long'][parameter],
                'delete': False,
            })
        for parameter in self.config["coin_overrides"].get(symbol, {}).get('bot', {}).get('short', {}):
            co_parameters.append({
                'section': 'bot',
                'parameter': parameter,
                'side': 'short',
                'value': self.config["coin_overrides"][symbol]['bot']['short'][parameter],
                'delete': False,
            })
        for parameter in self.config["coin_overrides"].get(symbol, {}).get('live', {}):
            co_parameters.append({
                'section': 'live',
                'parameter': parameter,
                'side': 'live',
                'value': self.config["coin_overrides"][symbol]['live'][parameter],
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
        st.session_state.co_config.bot.edit_co()
    # print(self.config.coin_overrides)
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1], vertical_alignment="bottom")
    with col1:
        if st.button("OK"):
            # {"COIN1": {"override_config_path": "path/to/override_config.json"}}
            # {"COIN2": {"override_config_path": "path/to/other_override_config.json", {"bot": {"long": {"close_grid_markup_start": 0.005}}}}}
            # {"COIN3": {"bot": {"short": {"entry_initial_qty_pct": 0.01}}, "live": {"forced_mode_long": "panic"}}}
            if st.session_state.edit_run_v7_co_config:
                st.session_state.co_config.config_file = Path(Path(self.config_file).parent, f'{symbol}.json')
                st.session_state.co_config.save_config()
                if symbol not in self.config["coin_overrides"]:
                    self.config["coin_overrides"][symbol] = {}
                self.config["coin_overrides"][symbol]["override_config_path"] = f'{symbol}.json'
            else:
                Path(Path(self.config_file).parent, f'{symbol}.json').unlink(missing_ok=True)
                if symbol in self.config["coin_overrides"]:
                    if "override_config_path" in self.config["coin_overrides"][symbol]:
                        del self.config["coin_overrides"][symbol]["override_config_path"]
            # Remove symbol from coin_overrides if it has no parameters
            if symbol in self.config["coin_overrides"] and self.config["coin_overrides"][symbol] == {}:
                del self.config["coin_overrides"][symbol]
            # self.save()
            self.clean_co_session_state()
            st.rerun()
    with col2:
        if st.button("Cancel"):
            self.clean_co_session_state()
            st.rerun()
    with col3:
        if st.button("Remove"):
            if self.config["coin_overrides"]:
                if symbol in self.config["coin_overrides"]:
                    del self.config["coin_overrides"][symbol]
            Path(Path(self.config_file).parent, f'{symbol}.json').unlink(missing_ok=True)
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
