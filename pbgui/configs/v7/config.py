import json
import traceback
from pathlib import Path
from .logging import Logging
from .backtest import Backtest
from .bot import Bot
from .live import Live
from .optimize import Optimize
from .pbgui import PBGui

class ConfigV7:
    def __init__(self, file_name = None):
        self._config_file = file_name
        self._logging = Logging()
        self._backtest = Backtest()
        self._bot = Bot()
        self._coin_overrides = {}
        self._live = Live()
        self._optimize = Optimize()
        self._pbgui = PBGui()

        self._config = {
            "logging": self._logging._logging,
            "backtest": self._backtest._backtest,
            "bot": self._bot._bot,
            "coin_overrides": self._coin_overrides,
            "live": self._live._live,
            "optimize": self._optimize._optimize,
            "pbgui": self._pbgui._pbgui
        }

    @property
    def config_file(self): return self._config_file
    @config_file.setter
    def config_file(self, new_value):
        self._config_file = new_value

    @property
    def logging(self): return self._logging
    @logging.setter
    def logging(self, new_value):
        self._logging.logging = new_value
        self._config["logging"] = self._logging.logging

    @property
    def backtest(self): return self._backtest
    @backtest.setter
    def backtest(self, new_value):
        self._backtest.backtest = new_value
        self._config["backtest"] = self._backtest.backtest

    @property
    def bot(self): return self._bot
    @bot.setter
    def bot(self, new_value):
        self._bot.bot = new_value
        self._config["bot"] = self._bot.bot

    @property
    def coin_overrides(self): return self._coin_overrides
    @coin_overrides.setter
    def coin_overrides(self, new_value):
        self._coin_overrides = new_value
        self._config["coin_overrides"] = self._coin_overrides

    @property
    def live(self): return self._live
    @live.setter
    def live(self, new_value):
        self._live.live = new_value
        self._config["live"] = self._live.live

    @property
    def optimize(self): return self._optimize
    @optimize.setter
    def optimize(self, new_value):
        self._optimize.optimize = new_value
        self._config["optimize"] = self._optimize.optimize

    @property
    def pbgui(self): return self._pbgui
    @pbgui.setter
    def pbgui(self, new_value):
        self._pbgui.pbgui = new_value
        self._config["pbgui"] = self._pbgui.pbgui

    @property
    def config(self): return self._config
    @config.setter
    def config(self, new_value):
        if "logging" in new_value:
            self.logging = new_value["logging"]
        if "backtest" in new_value:
            self.backtest = new_value["backtest"]
        if "bot" in new_value:
            self.bot = new_value["bot"]
        if "coin_overrides" in new_value:
            self.coin_overrides = new_value["coin_overrides"]
        if "live" in new_value:
            self.live = new_value["live"]
        if "optimize" in new_value:
            self.optimize = new_value["optimize"]
        if "pbgui" in new_value:
            self.pbgui = new_value["pbgui"]
        # Convert coin_flags to coin_overrides
        if "coin_flags" in new_value["live"]:
            if new_value["live"]["coin_flags"]:
                for symbol, flags in new_value["live"]["coin_flags"].items():
                    # remove USDT and USDC from symbol
                    # if symbol.endswith("USDT"):
                    #     symbol = symbol[:-4]
                    # elif symbol.endswith("USDC"):
                    #     symbol = symbol[:-4]
                    # print(symbol, flags)
                    if symbol not in self.coin_overrides:
                        self.coin_overrides[symbol] = {}
                    lm = {
                        "n": "normal",
                        "normal": "normal",
                        "m": "manual",
                        "manual": "manual",
                        "gs": "graceful_stop",
                        "graceful-stop": "graceful_stop",
                        "graceful_stop": "graceful_stop",
                        "p": "panic",
                        "panic": "panic",
                        "t": "tp_only",
                        "tp": "tp_only",
                        "tp-only": "tp_only",
                        "tp_only": "tp_only"
                    }.get(flags.split("-lm")[1].split()[0], "") if "-lm" in flags else ""
                    if lm:
                        if "live" not in self.coin_overrides[symbol]:
                            self.coin_overrides[symbol]["live"] = {}
                        self.coin_overrides[symbol]["live"]["forced_mode_long"] = lm

                    lw = flags.split("-lw")[1].split()[0] if "-lw" in flags else ""
                    if lw:
                        if "bot" not in self.coin_overrides[symbol]:
                            self.coin_overrides[symbol]["bot"] = {}
                        if "long" not in self.coin_overrides[symbol]["bot"]:
                            self.coin_overrides[symbol]["bot"]["long"] = {}
                        self.coin_overrides[symbol]["bot"]["long"]["wallet_exposure_limit"] = float(lw)

                    sm = {
                        "n": "normal",
                        "normal": "normal",
                        "m": "manual",
                        "manual": "manual",
                        "gs": "graceful_stop",
                        "graceful-stop": "graceful_stop",
                        "graceful_stop": "graceful_stop",
                        "p": "panic",
                        "panic": "panic",
                        "t": "tp_only",
                        "tp": "tp_only",
                        "tp-only": "tp_only",
                        "tp_only": "tp_only"
                    }.get(flags.split("-sm")[1].split()[0], "") if "-sm" in flags else ""
                    if sm:
                        if "live" not in self.coin_overrides[symbol]:
                            self.coin_overrides[symbol]["live"] = {}
                        self.coin_overrides[symbol]["live"]["forced_mode_short"] = sm

                    sw = flags.split("-sw")[1].split()[0] if "-sw" in flags else ""
                    if sw:
                        if "bot" not in self.coin_overrides[symbol]:
                            self.coin_overrides[symbol]["bot"] = {}
                        if "short" not in self.coin_overrides[symbol]["bot"]:
                            self.coin_overrides[symbol]["bot"]["short"] = {}
                        self.coin_overrides[symbol]["bot"]["short"]["wallet_exposure_limit"] = float(sw)

                    lev = flags.split("-lev")[1].split()[0] if "-lev" in flags else ""
                    if lev:
                        if "live" not in self.coin_overrides[symbol]:
                            self.coin_overrides[symbol]["live"] = {}
                        self.coin_overrides[symbol]["live"]["leverage"] = float(lev)

                    config = flags.split("-lc")[1].split()[0] if "-lc" in flags else ""
                    if config:
                        self.coin_overrides[symbol]["override_config_path"] = config

    def load_config(self):
        file =  Path(f'{self._config_file}')
        if file.exists():
            try:
                with open(file, "r", encoding='utf-8') as f:
                    config = json.load(f)
                self.config = config
            except Exception as e:
                print(f'Error loding v7 config: {file} {e}')
                traceback.print_exc()


    def save_config(self):
        if self._config != None and self._config_file != None:
            file = Path(f'{self._config_file}')
            file.parent.mkdir(parents=True, exist_ok=True)
            with open(file, "w", encoding='utf-8') as f:
                json.dump(self._config, f, indent=4)

    # UI helpers -------------------------------------------------------------
    def view_coin_overrides(self):
        """Display editable table of coin overrides."""
        from pbgui.ui import config_v7_ui
        return config_v7_ui.view_coin_overrides(self)

    def edit_coin_override(self, symbol):
        """Open editor for a single coin override."""
        from pbgui.ui import config_v7_ui
        return config_v7_ui.edit_coin_override(self, symbol)

    def clean_co_session_state(self):
        """Reset Streamlit session keys used while editing overrides."""
        from pbgui.ui import config_v7_ui
        return config_v7_ui.clean_co_session_state(self)
