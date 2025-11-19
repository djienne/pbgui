import json
from pathlib import Path
from ..v7.config import ConfigV7
from ...utils import validateJSON, config_pretty_str

class Config:
    def __init__(self, file_name = None, config = None):
        self._config_file = file_name
        self._long_we = 1.0
        self._short_we = 1.0
        self._long_enabled = True
        self._short_enabled = False
        self._type = None
        self._preview_grid = False
        self._config_v7 = ConfigV7()
        self._config_v7.bot.long.n_positions = 1.0
        self._config_v7.bot.short.n_positions = 1.0
        if config:
            self.config = config
        else:
            self._config = None

    @property
    def type(self): return self._type

    @property
    def config_file(self): return self._config_file

    @config_file.setter
    def config_file(self, new_config_file):
        if self._config_file != new_config_file:
            self._config_file = new_config_file
        
    @property
    def config(self): return self._config

    @property
    def config_v7(self):
        if self._config:
            # Check if config is a recursive grid config
            config = json.loads(self._config)
            if "long" in config:
                if not "ddown_factor" in config["long"]:
                    return None
            # long settings
            self._config_v7.bot.long.close_grid_markup_start = json.loads(self._config)["long"]["min_markup"] + json.loads(self._config)["long"]["markup_range"]
            self._config_v7.bot.long.close_grid_markup_end = json.loads(self._config)["long"]["min_markup"]
            self._config_v7.bot.long.close_grid_qty_pct = 1.0 / float(json.loads(self._config)["long"]["n_close_orders"])
            self._config_v7.bot.long.close_trailing_grid_ratio = 0
            self._config_v7.bot.long.close_trailing_qty_pct = 1
            self._config_v7.bot.long.close_trailing_retracement_pct = 0
            self._config_v7.bot.long.close_trailing_threshold_pct = 0
            self._config_v7.bot.long.ema_span_0 = json.loads(self._config)["long"]["ema_span_0"]
            self._config_v7.bot.long.ema_span_1 = json.loads(self._config)["long"]["ema_span_1"]
            self._config_v7.bot.long.entry_grid_double_down_factor = json.loads(self._config)["long"]["ddown_factor"]
            self._config_v7.bot.long.entry_grid_spacing_pct = json.loads(self._config)["long"]["rentry_pprice_dist"]
            self._config_v7.bot.long.entry_grid_spacing_weight = json.loads(self._config)["long"]["rentry_pprice_dist_wallet_exposure_weighting"]
            self._config_v7.bot.long.entry_initial_ema_dist = json.loads(self._config)["long"]["initial_eprice_ema_dist"]
            self._config_v7.bot.long.entry_initial_qty_pct = json.loads(self._config)["long"]["initial_qty_pct"]
            self._config_v7.bot.long.entry_trailing_grid_ratio = 0
            self._config_v7.bot.long.entry_trailing_retracement_pct = 0
            self._config_v7.bot.long.entry_trailing_threshold_pct = 0
            self._config_v7.bot.long.entry_trailing_double_down_factor = 0
            # self._config_v7.bot.long.total_wallet_exposure_limit = json.loads(self._config)["long"]["wallet_exposure_limit"]
            try:
                self._config_v7.bot.long.unstuck_close_pct = json.loads(self._config)["long"]["auto_unstuck_qty_pct"]
            except:
                self._config_v7.bot.long.unstuck_close_pct = 0.025
            self._config_v7.bot.long.unstuck_ema_dist = json.loads(self._config)["long"]["auto_unstuck_ema_dist"]
            # short settings
            self._config_v7.bot.short.close_grid_markup_start = json.loads(self._config)["short"]["min_markup"] + json.loads(self._config)["short"]["markup_range"]
            self._config_v7.bot.short.close_grid_markup_end = json.loads(self._config)["short"]["min_markup"]
            self._config_v7.bot.short.close_grid_qty_pct = 1.0 / float(json.loads(self._config)["short"]["n_close_orders"])
            self._config_v7.bot.short.close_trailing_grid_ratio = 0
            self._config_v7.bot.short.close_trailing_qty_pct = 1
            self._config_v7.bot.short.close_trailing_retracement_pct = 0
            self._config_v7.bot.short.close_trailing_threshold_pct = 0
            self._config_v7.bot.short.ema_span_0 = json.loads(self._config)["short"]["ema_span_0"]
            self._config_v7.bot.short.ema_span_1 = json.loads(self._config)["short"]["ema_span_1"]
            self._config_v7.bot.short.entry_grid_double_down_factor = json.loads(self._config)["short"]["ddown_factor"]
            self._config_v7.bot.short.entry_grid_spacing_pct = json.loads(self._config)["short"]["rentry_pprice_dist"]
            self._config_v7.bot.short.entry_grid_spacing_weight = json.loads(self._config)["short"]["rentry_pprice_dist_wallet_exposure_weighting"]
            self._config_v7.bot.short.entry_initial_ema_dist = json.loads(self._config)["short"]["initial_eprice_ema_dist"]
            self._config_v7.bot.short.entry_initial_qty_pct = json.loads(self._config)["short"]["initial_qty_pct"]
            self._config_v7.bot.short.entry_trailing_grid_ratio = 0
            self._config_v7.bot.short.entry_trailing_retracement_pct = 0
            self._config_v7.bot.short.entry_trailing_threshold_pct = 0
            # self._config_v7.bot.short.total_wallet_exposure_limit = json.loads(self._config)["short"]["wallet_exposure_limit"]
            try:
                self._config_v7.bot.short.unstuck_close_pct = json.loads(self._config)["short"]["auto_unstuck_qty_pct"]
            except:
                self._config_v7.bot.short.unstuck_close_pct = 0.025
            self._config_v7.bot.short.unstuck_ema_dist = json.loads(self._config)["short"]["auto_unstuck_ema_dist"]
            return json.dumps(self._config_v7.config, indent=4)
        return None

    @config.setter
    def config(self, new_config):
        if new_config != "None":
            if validateJSON(new_config):
                self._config = new_config
                self.update_config()
                # if "error_config" in st.session_state:
                #     del st.session_state.error_config
            else:
                pass
                # st.session_state.error_config = "Config is invalid"

    @config_file.setter
    def config_file(self, new_config_file):
        if self._config_file != new_config_file:
            self._config_file = new_config_file

    @property
    def long_we(self): return self._long_we

    @long_we.setter
    def long_we(self, new_long_we):
        self._long_we = round(new_long_we,2)
        if self._config:
            t = json.loads(self._config)
            t["long"]["wallet_exposure_limit"] = self._long_we
            self._config = config_pretty_str(t)
    
    @property
    def long_enabled(self): return self._long_enabled

    @long_enabled.setter
    def long_enabled(self, new_long_enabled):
        self._long_enabled = new_long_enabled
        if self._config:
            t = json.loads(self._config)
            t["long"]["enabled"] = self._long_enabled
            self._config = config_pretty_str(t)
            self._config_v7.bot.long.total_wallet_exposure_limit = self.long_we
            if self.long_enabled:
                self._config_v7.bot.long.n_positions = 1.0
            else:
                self._config_v7.bot.long.n_positions = 0.0

    @property
    def short_enabled(self): return self._short_enabled

    @short_enabled.setter
    def short_enabled(self, new_short_enabled):
        self._short_enabled = new_short_enabled
        if self._config:
            t = json.loads(self._config)
            t["short"]["enabled"] = self._short_enabled
            self._config = config_pretty_str(t)
            self._config_v7.bot.short.total_wallet_exposure_limit = self.short_we
            if self.short_enabled:
                self._config_v7.bot.short.n_positions = 1.0
            else:
                self._config_v7.bot.short.n_positions = 0.0

    @property
    def short_we(self): return self._short_we

    @short_we.setter
    def short_we(self, new_short_we):
        self._short_we = round(new_short_we,2)
        if self._config:
            t = json.loads(self._config)
            t["short"]["wallet_exposure_limit"] = self._short_we
            self._config = config_pretty_str(t)

    @property
    def preview_grid(self): return self._preview_grid
    @preview_grid.setter
    def preview_grid(self, new_preview_grid):
        self._preview_grid = new_preview_grid

    def update_config(self):
        self.long_we = json.loads(self._config)["long"]["wallet_exposure_limit"]
        self.short_we = json.loads(self._config)["short"]["wallet_exposure_limit"]
        self._config_v7.bot.long.total_wallet_exposure_limit = self.long_we
        self._config_v7.bot.short.total_wallet_exposure_limit = self.short_we
        self.long_enabled = json.loads(self._config)["long"]["enabled"]
        self.short_enabled = json.loads(self._config)["short"]["enabled"]
        if not self.long_enabled:
            self._config_v7.bot.long.n_positions = 0.0
        if not self.short_enabled:
            self._config_v7.bot.short.n_positions = 0.0
        long = json.loads(self._config)["long"]
        if "ddown_factor" in long:
            self._type = "recursive_grid"
        elif "qty_pct_entry" in long:
            self._type = "clock"
        elif "grid_span" in long:
            self._type = "neat_grid"

    def load_config(self):
        file =  Path(f'{self._config_file}')
        if file.exists():
            with open(file, "r", encoding='utf-8') as f:
                self._config = f.read()
                self.update_config()

    def save_config(self):
        if self._config != None and self._config_file != None:
            file = Path(f'{self._config_file}')
            with open(file, "w", encoding='utf-8') as f:
                f.write(self._config)

    def edit_config(self):
        """Render the legacy v6 config editor."""
        from pbgui.ui import config_v6_ui
        return config_v6_ui.edit_config(self)
