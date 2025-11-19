import json
from pathlib import Path
import datetime
import math
import multiprocessing
import traceback
import copy

# Data Model Classes for Config

class Logging:
    LEVEL = {
        0: "warnings",
        1: "info",
        2: "debug",
        3: "trace"}

    def __init__(self):
        self._level = 1
        self._logging = {
            "level": self._level
        }
    
    def __repr__(self):
        return str(self._logging)

    @property
    def logging(self): return self._logging
    @logging.setter
    def logging(self, new_logging):
        if "level" in new_logging:
            self.level = new_logging["level"]
    
    @property
    def level(self): return self._level
    @level.setter
    def level(self, new_level):
        self._level = new_level
        self._logging["level"] = self._level

class Backtest:
    def __init__(self):
        self._base_dir = "backtests"
        self._combine_ohlcvs = True
        self._compress_cache = True
        self._end_date = "now"
        self._exchanges = ["binance", "bybit"]
        self._gap_tolerance_ohlcvs_minutes = 120.0
        self._start_date = "2020-01-01"
        self._starting_balance = 1000.0
        self._use_btc_collateral = False
        self._max_warmup_minutes = 0.0
        self._backtest = {
            "base_dir": self._base_dir,
            "combine_ohlcvs": self._combine_ohlcvs,
            "compress_cache": self._compress_cache,
            "end_date": self._end_date,
            "exchanges": self._exchanges,
            "gap_tolerance_ohlcvs_minutes": self._gap_tolerance_ohlcvs_minutes,
            "start_date": self._start_date,
            "starting_balance": self._starting_balance,
            "use_btc_collateral": self._use_btc_collateral,
            "max_warmup_minutes": self._max_warmup_minutes
        }
    
    def __repr__(self):
        return str(self._backtest)
    
    @property
    def backtest(self): return self._backtest
    @backtest.setter
    def backtest(self, new_backtest):
        if "base_dir" in new_backtest:
            self.base_dir = new_backtest["base_dir"]
        if "combine_ohlcvs" in new_backtest:
            self.combine_ohlcvs = new_backtest["combine_ohlcvs"]
        if "compress_cache" in new_backtest:
            self.compress_cache = new_backtest["compress_cache"]
        if "end_date" in new_backtest:
            self.end_date = new_backtest["end_date"]
        if "exchanges" in new_backtest:
            self.exchanges = new_backtest["exchanges"]
        if "gap_tolerance_ohlcvs_minutes" in new_backtest:
            self.gap_tolerance_ohlcvs_minutes = new_backtest["gap_tolerance_ohlcvs_minutes"]
        if "start_date" in new_backtest:
            self.start_date = new_backtest["start_date"]
        if "starting_balance" in new_backtest:
            self.starting_balance = new_backtest["starting_balance"]
        if "use_btc_collateral" in new_backtest:
            self.use_btc_collateral = new_backtest["use_btc_collateral"]
        if "max_warmup_minutes" in new_backtest:
            self.max_warmup_minutes = new_backtest["max_warmup_minutes"]
    
    @property
    def base_dir(self): return self._base_dir
    @property
    def combine_ohlcvs(self): return self._combine_ohlcvs
    @property
    def compress_cache(self): return self._compress_cache
    @property
    def end_date(self):
        if self._end_date == "now":
            return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        return self._end_date
    @property
    def exchanges(self): return self._exchanges
    @property
    def gap_tolerance_ohlcvs_minutes(self): return self._gap_tolerance_ohlcvs_minutes
    @property
    def start_date(self): return self._start_date
    @property
    def starting_balance(self): return self._starting_balance
    @property
    def use_btc_collateral(self): return self._use_btc_collateral
    @property
    def max_warmup_minutes(self): return self._max_warmup_minutes

    @base_dir.setter
    def base_dir(self, new_base_dir):
        self._base_dir = new_base_dir
        self._backtest["base_dir"] = self._base_dir
    @combine_ohlcvs.setter
    def combine_ohlcvs(self, new_combine_ohlcvs):
        self._combine_ohlcvs = new_combine_ohlcvs
        self._backtest["combine_ohlcvs"] = self._combine_ohlcvs
    @compress_cache.setter
    def compress_cache(self, new_compress_cache):
        self._compress_cache = new_compress_cache
        self._backtest["compress_cache"] = self._compress_cache
    @end_date.setter
    def end_date(self, new_end_date):
        self._end_date = new_end_date
        self._backtest["end_date"] = self._end_date
    @exchanges.setter
    def exchanges(self, new_exchanges):
        self._exchanges = new_exchanges
        self._backtest["exchanges"] = self._exchanges
    @gap_tolerance_ohlcvs_minutes.setter
    def gap_tolerance_ohlcvs_minutes(self, new_gap_tolerance_ohlcvs_minutes):
        self._gap_tolerance_ohlcvs_minutes = new_gap_tolerance_ohlcvs_minutes
        self._backtest["gap_tolerance_ohlcvs_minutes"] = self._gap_tolerance_ohlcvs_minutes
    @start_date.setter
    def start_date(self, new_start_date):
        self._start_date = new_start_date
        self._backtest["start_date"] = self._start_date
    @starting_balance.setter
    def starting_balance(self, new_starting_balance):
        self._starting_balance = new_starting_balance
        self._backtest["starting_balance"] = self._starting_balance
    @use_btc_collateral.setter
    def use_btc_collateral(self, new_use_btc_collateral):
        self._use_btc_collateral = new_use_btc_collateral
        self._backtest["use_btc_collateral"] = self._use_btc_collateral
    @max_warmup_minutes.setter
    def max_warmup_minutes(self, new_max_warmup_minutes):
        self._max_warmup_minutes = new_max_warmup_minutes
        self._backtest["max_warmup_minutes"] = self._max_warmup_minutes

class Long:
    def __init__(self):
        # self._close_grid_markup_range = 0.0015976
        # self._close_grid_min_markup = 0.012839
        self._close_grid_markup_end = 0.001161
        self._close_grid_markup_start = 0.009675
        self._close_grid_qty_pct = 0.8195
        self._close_trailing_grid_ratio = 0.042114
        self._close_trailing_qty_pct = 1
        self._close_trailing_retracement_pct = 0.066097
        self._close_trailing_threshold_pct = 0.06726
        self._ema_span_0 = 469.02
        self._ema_span_1 = 1118.9
        self._enforce_exposure_limit = True
        self._entry_grid_double_down_factor = 2.3738
        self._entry_grid_spacing_log_span_hours = 72
        self._entry_grid_spacing_log_weight = 0.0
        self._entry_grid_spacing_pct = 0.052372
        self._entry_grid_spacing_we_weight = 0.17715
        self._entry_initial_ema_dist = -0.0060574
        self._entry_initial_qty_pct = 0.019955
        self._entry_trailing_double_down_factor = 1.441
        self._entry_trailing_grid_ratio = -0.28053
        self._entry_trailing_retracement_pct = 0.0024762
        self._entry_trailing_threshold_pct = 0.014956
        self._filter_volume_drop_pct = 0.7021
        self._filter_volume_ema_span = 303.6
        self._filter_log_range_ema_span = 303.6
        self._n_positions = 9.6662
        self._total_wallet_exposure_limit = 0.8536
        self._unstuck_close_pct = 0.049593
        self._unstuck_ema_dist = -0.051669
        self._unstuck_loss_allowance_pct = 0.044329
        self._unstuck_threshold = 0.46953
        self._long = {
            "close_grid_markup_end": self._close_grid_markup_end,
            "close_grid_markup_start": self._close_grid_markup_start,
            # "close_grid_markup_range": self._close_grid_markup_range,
            # "close_grid_min_markup": self._close_grid_min_markup,
            "close_grid_qty_pct": self._close_grid_qty_pct,
            "close_trailing_grid_ratio": self._close_trailing_grid_ratio,
            "close_trailing_qty_pct": self._close_trailing_qty_pct,
            "close_trailing_retracement_pct": self._close_trailing_retracement_pct,
            "close_trailing_threshold_pct": self._close_trailing_threshold_pct,
            "ema_span_0": self._ema_span_0,
            "ema_span_1": self._ema_span_1,
            "enforce_exposure_limit": self._enforce_exposure_limit,
            "entry_grid_double_down_factor": self._entry_grid_double_down_factor,
            "entry_grid_spacing_log_span_hours": self._entry_grid_spacing_log_span_hours,
            "entry_grid_spacing_log_weight": self._entry_grid_spacing_log_weight,
            "entry_grid_spacing_pct": self._entry_grid_spacing_pct,
            "entry_grid_spacing_we_weight": self._entry_grid_spacing_we_weight,
            "entry_initial_ema_dist": self._entry_initial_ema_dist,
            "entry_initial_qty_pct": self._entry_initial_qty_pct,
            "entry_trailing_double_down_factor": self._entry_trailing_double_down_factor,
            "entry_trailing_grid_ratio": self._entry_trailing_grid_ratio,
            "entry_trailing_retracement_pct": self._entry_trailing_retracement_pct,
            "entry_trailing_threshold_pct": self._entry_trailing_threshold_pct,
            "filter_log_range_ema_span": self._filter_log_range_ema_span,
            "filter_volume_drop_pct": self._filter_volume_drop_pct,
            "filter_volume_ema_span": self._filter_volume_ema_span,
            "n_positions": self._n_positions,
            "total_wallet_exposure_limit": self._total_wallet_exposure_limit,
            "unstuck_close_pct": self._unstuck_close_pct,
            "unstuck_ema_dist": self._unstuck_ema_dist,
            "unstuck_loss_allowance_pct": self._unstuck_loss_allowance_pct,
            "unstuck_threshold": self._unstuck_threshold
        }

    def __repr__(self):
        return str(self._long)
    
    @property
    def long(self): return self._long
    @long.setter
    def long(self, new_long):
        #Fix for old markup parameters
        if "close_grid_markup_range" in new_long and "close_grid_min_markup" in new_long:
            self.close_grid_markup_start = new_long["close_grid_min_markup"] + new_long["close_grid_markup_range"]
            self.close_grid_markup_end = new_long["close_grid_min_markup"]
        if "close_grid_markup_end" in new_long:
            self.close_grid_markup_end = new_long["close_grid_markup_end"]
        if "close_grid_markup_start" in new_long:
            self.close_grid_markup_start = new_long["close_grid_markup_start"]
        if "close_grid_qty_pct" in new_long:
            self.close_grid_qty_pct = new_long["close_grid_qty_pct"]
        if "close_trailing_grid_ratio" in new_long:
            self.close_trailing_grid_ratio = new_long["close_trailing_grid_ratio"]
        if "close_trailing_qty_pct" in new_long:
            self.close_trailing_qty_pct = new_long["close_trailing_qty_pct"]
        if "close_trailing_retracement_pct" in new_long:
            self.close_trailing_retracement_pct = new_long["close_trailing_retracement_pct"]
        if "close_trailing_threshold_pct" in new_long:
            self.close_trailing_threshold_pct = new_long["close_trailing_threshold_pct"]
        if "ema_span_0" in new_long:
            self.ema_span_0 = new_long["ema_span_0"]
        if "ema_span_1" in new_long:
            self.ema_span_1 = new_long["ema_span_1"]
        if "enforce_exposure_limit" in new_long:
            self.enforce_exposure_limit = new_long["enforce_exposure_limit"]
        if "entry_grid_double_down_factor" in new_long:
            self.entry_grid_double_down_factor = new_long["entry_grid_double_down_factor"]
        if "entry_grid_spacing_log_span_hours" in new_long:
            self.entry_grid_spacing_log_span_hours = new_long["entry_grid_spacing_log_span_hours"]
        if "entry_grid_spacing_log_weight" in new_long:
            self.entry_grid_spacing_log_weight = new_long["entry_grid_spacing_log_weight"]
        if "entry_grid_spacing_pct" in new_long:
            self.entry_grid_spacing_pct = new_long["entry_grid_spacing_pct"]
        if "entry_grid_spacing_we_weight" in new_long:
            self.entry_grid_spacing_we_weight = new_long["entry_grid_spacing_we_weight"]
        # Fix for old configs
        elif "entry_grid_spacing_weight" in new_long:
            self.entry_grid_spacing_we_weight = new_long["entry_grid_spacing_weight"]
        if "entry_initial_ema_dist" in new_long:
            self.entry_initial_ema_dist = new_long["entry_initial_ema_dist"]
        if "entry_initial_qty_pct" in new_long:
            self.entry_initial_qty_pct = new_long["entry_initial_qty_pct"]
        if "entry_trailing_double_down_factor" in new_long:
            self.entry_trailing_double_down_factor = new_long["entry_trailing_double_down_factor"]
        else:
            self.entry_trailing_double_down_factor = self.entry_grid_double_down_factor
        if "entry_trailing_grid_ratio" in new_long:
            self.entry_trailing_grid_ratio = new_long["entry_trailing_grid_ratio"]
        if "entry_trailing_retracement_pct" in new_long:
            self.entry_trailing_retracement_pct = new_long["entry_trailing_retracement_pct"]
        if "entry_trailing_threshold_pct" in new_long:
            self.entry_trailing_threshold_pct = new_long["entry_trailing_threshold_pct"]
        if "filter_log_range_ema_span" in new_long:
            self.filter_log_range_ema_span = new_long["filter_log_range_ema_span"]
        # Fix for old configs
        elif "filter_noisiness_rolling_window" in new_long:
            self.filter_log_range_ema_span = new_long["filter_noisiness_rolling_window"]
        elif "filter_rolling_window" in new_long:
            self.filter_log_range_ema_span = new_long["filter_rolling_window"]
        if "filter_volume_drop_pct" in new_long:
            self.filter_volume_drop_pct = new_long["filter_volume_drop_pct"]
        # Fix for old configs
        elif "filter_relative_volume_clip_pct" in new_long:
            self.filter_volume_drop_pct = new_long["filter_relative_volume_clip_pct"]
        if "filter_volume_ema_span" in new_long:
            self.filter_volume_ema_span = new_long["filter_volume_ema_span"]
        # Fix for old configs
        elif "filter_rolling_window" in new_long:
            self.filter_volume_ema_span = new_long["filter_rolling_window"]
        if "n_positions" in new_long:
            self.n_positions = new_long["n_positions"]
        if "total_wallet_exposure_limit" in new_long:
            self.total_wallet_exposure_limit = new_long["total_wallet_exposure_limit"]
        if "unstuck_close_pct" in new_long:
            self.unstuck_close_pct = new_long["unstuck_close_pct"]
        if "unstuck_ema_dist" in new_long:
            self.unstuck_ema_dist = new_long["unstuck_ema_dist"]
        if "unstuck_loss_allowance_pct" in new_long:
            self.unstuck_loss_allowance_pct = new_long["unstuck_loss_allowance_pct"]
        if "unstuck_threshold" in new_long:
            self.unstuck_threshold = new_long["unstuck_threshold"]

    # @property
    # def close_grid_markup_range(self): return self._close_grid_markup_range
    # @property
    # def close_grid_min_markup(self): return self._close_grid_min_markup
    @property
    def close_grid_markup_end(self): return self._close_grid_markup_end
    @property
    def close_grid_markup_start(self): return self._close_grid_markup_start
    @property
    def close_grid_qty_pct(self): return self._close_grid_qty_pct
    @property
    def close_trailing_grid_ratio(self): return self._close_trailing_grid_ratio
    @property
    def close_trailing_qty_pct(self): return self._close_trailing_qty_pct
    @property
    def close_trailing_retracement_pct(self): return self._close_trailing_retracement_pct
    @property
    def close_trailing_threshold_pct(self): return self._close_trailing_threshold_pct
    @property
    def ema_span_0(self): return self._ema_span_0
    @property
    def ema_span_1(self): return self._ema_span_1
    @property
    def enforce_exposure_limit(self): return self._enforce_exposure_limit
    @property
    def entry_grid_double_down_factor(self): return self._entry_grid_double_down_factor
    @property
    def entry_grid_spacing_log_span_hours(self): return self._entry_grid_spacing_log_span_hours
    @property
    def entry_grid_spacing_log_weight(self): return self._entry_grid_spacing_log_weight
    @property
    def entry_grid_spacing_pct(self): return self._entry_grid_spacing_pct
    @property
    def entry_grid_spacing_we_weight(self): return self._entry_grid_spacing_we_weight
    @property
    def entry_initial_ema_dist(self): return self._entry_initial_ema_dist
    @property
    def entry_initial_qty_pct(self): return self._entry_initial_qty_pct
    @property
    def entry_trailing_double_down_factor(self): return self._entry_trailing_double_down_factor
    @property
    def entry_trailing_grid_ratio(self): return self._entry_trailing_grid_ratio
    @property
    def entry_trailing_retracement_pct(self): return self._entry_trailing_retracement_pct
    @property
    def entry_trailing_threshold_pct(self): return self._entry_trailing_threshold_pct
    @property
    def filter_log_range_ema_span(self): return self._filter_log_range_ema_span
    @property
    def filter_volume_drop_pct(self): return self._filter_volume_drop_pct
    @property
    def filter_volume_ema_span(self): return self._filter_volume_ema_span
    @property
    def n_positions(self): return self._n_positions
    @property
    def total_wallet_exposure_limit(self): return self._total_wallet_exposure_limit
    @property
    def unstuck_close_pct(self): return self._unstuck_close_pct
    @property
    def unstuck_ema_dist(self): return self._unstuck_ema_dist
    @property
    def unstuck_loss_allowance_pct(self): return self._unstuck_loss_allowance_pct
    @property
    def unstuck_threshold(self): return self._unstuck_threshold

    @close_grid_markup_end.setter
    def close_grid_markup_end(self, new_close_grid_markup_end):
        self._close_grid_markup_end = new_close_grid_markup_end
        self._long["close_grid_markup_end"] = self._close_grid_markup_end
    @close_grid_markup_start.setter
    def close_grid_markup_start(self, new_close_grid_markup_start):
        self._close_grid_markup_start = new_close_grid_markup_start
        self._long["close_grid_markup_start"] = self._close_grid_markup_start
    # @close_grid_markup_range.setter
    # def close_grid_markup_range(self, new_close_grid_markup_range):
    #     self._close_grid_markup_range = new_close_grid_markup_range
    #     self._long["close_grid_markup_range"] = self._close_grid_markup_range
    # @close_grid_min_markup.setter
    # def close_grid_min_markup(self, new_close_grid_min_markup):
    #     self._close_grid_min_markup = new_close_grid_min_markup
    #     self._long["close_grid_min_markup"] = self._close_grid_min_markup
    @close_grid_qty_pct.setter
    def close_grid_qty_pct(self, new_close_grid_qty_pct):
        self._close_grid_qty_pct = new_close_grid_qty_pct
        self._long["close_grid_qty_pct"] = self._close_grid_qty_pct
    @close_trailing_grid_ratio.setter
    def close_trailing_grid_ratio(self, new_close_trailing_grid_ratio):
        self._close_trailing_grid_ratio = new_close_trailing_grid_ratio
        self._long["close_trailing_grid_ratio"] = self._close_trailing_grid_ratio
    @close_trailing_qty_pct.setter
    def close_trailing_qty_pct(self, new_close_trailing_qty_pct):
        self._close_trailing_qty_pct = new_close_trailing_qty_pct
        self._long["close_trailing_qty_pct"] = self._close_trailing_qty_pct
    @close_trailing_retracement_pct.setter
    def close_trailing_retracement_pct(self, new_close_trailing_retracement_pct):
        self._close_trailing_retracement_pct = new_close_trailing_retracement_pct
        self._long["close_trailing_retracement_pct"] = self._close_trailing_retracement_pct
    @close_trailing_threshold_pct.setter
    def close_trailing_threshold_pct(self, new_close_trailing_threshold_pct):
        self._close_trailing_threshold_pct = new_close_trailing_threshold_pct
        self._long["close_trailing_threshold_pct"] = self._close_trailing_threshold_pct
    @ema_span_0.setter
    def ema_span_0(self, new_ema_span_0):
        self._ema_span_0 = new_ema_span_0
        self._long["ema_span_0"] = self._ema_span_0
    @ema_span_1.setter
    def ema_span_1(self, new_ema_span_1):
        self._ema_span_1 = new_ema_span_1
        self._long["ema_span_1"] = self._ema_span_1
    @enforce_exposure_limit.setter
    def enforce_exposure_limit(self, new_enforce_exposure_limit):
        self._enforce_exposure_limit = new_enforce_exposure_limit
        self._long["enforce_exposure_limit"] = self._enforce_exposure_limit
    @entry_grid_double_down_factor.setter
    def entry_grid_double_down_factor(self, new_entry_grid_double_down_factor):
        self._entry_grid_double_down_factor = new_entry_grid_double_down_factor
        self._long["entry_grid_double_down_factor"] = self._entry_grid_double_down_factor
    @entry_grid_spacing_log_span_hours.setter
    def entry_grid_spacing_log_span_hours(self, new_entry_grid_spacing_log_span_hours):
        self._entry_grid_spacing_log_span_hours = new_entry_grid_spacing_log_span_hours
        self._long["entry_grid_spacing_log_span_hours"] = self._entry_grid_spacing_log_span_hours
    @entry_grid_spacing_log_weight.setter
    def entry_grid_spacing_log_weight(self, new_entry_grid_spacing_log_weight):
        self._entry_grid_spacing_log_weight = new_entry_grid_spacing_log_weight
        self._long["entry_grid_spacing_log_weight"] = self._entry_grid_spacing_log_weight
    @entry_grid_spacing_pct.setter
    def entry_grid_spacing_pct(self, new_entry_grid_spacing_pct):
        self._entry_grid_spacing_pct = new_entry_grid_spacing_pct
        self._long["entry_grid_spacing_pct"] = self._entry_grid_spacing_pct
    @entry_grid_spacing_we_weight.setter
    def entry_grid_spacing_we_weight(self, new_entry_grid_spacing_we_weight):
        self._entry_grid_spacing_we_weight = new_entry_grid_spacing_we_weight
        self._long["entry_grid_spacing_we_weight"] = self._entry_grid_spacing_we_weight
    @entry_initial_ema_dist.setter
    def entry_initial_ema_dist(self, new_entry_initial_ema_dist):
        self._entry_initial_ema_dist = new_entry_initial_ema_dist
        self._long["entry_initial_ema_dist"] = self._entry_initial_ema_dist
    @entry_initial_qty_pct.setter
    def entry_initial_qty_pct(self, new_entry_initial_qty_pct):
        self._entry_initial_qty_pct = new_entry_initial_qty_pct
        self._long["entry_initial_qty_pct"] = self._entry_initial_qty_pct
    @entry_trailing_double_down_factor.setter
    def entry_trailing_double_down_factor(self, new_entry_trailing_double_down_factor):
        self._entry_trailing_double_down_factor = new_entry_trailing_double_down_factor
        self._long["entry_trailing_double_down_factor"] = self._entry_trailing_double_down_factor
    @entry_trailing_grid_ratio.setter
    def entry_trailing_grid_ratio(self, new_entry_trailing_grid_ratio):
        self._entry_trailing_grid_ratio = new_entry_trailing_grid_ratio
        self._long["entry_trailing_grid_ratio"] = self._entry_trailing_grid_ratio
    @entry_trailing_retracement_pct.setter
    def entry_trailing_retracement_pct(self, new_entry_trailing_retracement_pct):
        self._entry_trailing_retracement_pct = new_entry_trailing_retracement_pct
        self._long["entry_trailing_retracement_pct"] = self._entry_trailing_retracement_pct
    @entry_trailing_threshold_pct.setter
    def entry_trailing_threshold_pct(self, new_entry_trailing_threshold_pct):
        self._entry_trailing_threshold_pct = new_entry_trailing_threshold_pct
        self._long["entry_trailing_threshold_pct"] = self._entry_trailing_threshold_pct
    @filter_log_range_ema_span.setter
    def filter_log_range_ema_span(self, new_filter_log_range_ema_span):
        self._filter_log_range_ema_span = new_filter_log_range_ema_span
        self._long["filter_log_range_ema_span"] = self._filter_log_range_ema_span
    @filter_volume_drop_pct.setter
    def filter_volume_drop_pct(self, new_filter_volume_drop_pct):
        self._filter_volume_drop_pct = new_filter_volume_drop_pct
        self._long["filter_volume_drop_pct"] = self._filter_volume_drop_pct
    @filter_volume_ema_span.setter
    def filter_volume_ema_span(self, new_filter_volume_ema_span):
        self._filter_volume_ema_span = new_filter_volume_ema_span
        self._long["filter_volume_ema_span"] = self._filter_volume_ema_span
    @n_positions.setter
    def n_positions(self, new_n_positions):
        self._n_positions = new_n_positions
        self._long["n_positions"] = self._n_positions
    @total_wallet_exposure_limit.setter
    def total_wallet_exposure_limit(self, new_total_wallet_exposure_limit):
        self._total_wallet_exposure_limit = new_total_wallet_exposure_limit
        self._long["total_wallet_exposure_limit"] = self._total_wallet_exposure_limit
    @unstuck_close_pct.setter
    def unstuck_close_pct(self, new_unstuck_close_pct):
        self._unstuck_close_pct = new_unstuck_close_pct
        self._long["unstuck_close_pct"] = self._unstuck_close_pct
    @unstuck_ema_dist.setter
    def unstuck_ema_dist(self, new_unstuck_ema_dist):
        self._unstuck_ema_dist = new_unstuck_ema_dist
        self._long["unstuck_ema_dist"] = self._unstuck_ema_dist
    @unstuck_loss_allowance_pct.setter
    def unstuck_loss_allowance_pct(self, new_unstuck_loss_allowance_pct):
        self._unstuck_loss_allowance_pct = new_unstuck_loss_allowance_pct
        self._long["unstuck_loss_allowance_pct"] = self._unstuck_loss_allowance_pct
    @unstuck_threshold.setter
    def unstuck_threshold(self, new_unstuck_threshold):
        self._unstuck_threshold = new_unstuck_threshold
        self._long["unstuck_threshold"] = self._unstuck_threshold

class Short:
    def __init__(self):
        # self._close_grid_markup_range = 0.028266
        # self._close_grid_min_markup = 0.013899
        self._close_grid_markup_end = 0.001
        self._close_grid_markup_start = 0.001
        self._close_grid_qty_pct = 0.05
        self._close_trailing_grid_ratio = 0.93658
        self._close_trailing_qty_pct = 1
        self._close_trailing_retracement_pct = 0.098179
        self._close_trailing_threshold_pct = -0.059383
        self._ema_span_0 = 794.32
        self._ema_span_1 = 1176.7
        self._enforce_exposure_limit = True
        self._entry_grid_double_down_factor = 2.1256
        self._entry_grid_spacing_log_span_hours = 72
        self._entry_grid_spacing_log_weight = 0.0
        self._entry_grid_spacing_pct = 0.072906
        self._entry_grid_spacing_we_weight = 0.98867
        self._entry_initial_ema_dist = -0.060333
        self._entry_initial_qty_pct = 0.066426
        self._entry_trailing_double_down_factor = 0.72508
        self._entry_trailing_grid_ratio = -0.026647
        self._entry_trailing_retracement_pct = 0.016626
        self._entry_trailing_threshold_pct = 0.052728
        self._filter_log_range_ema_span = 320.18
        self._filter_volume_drop_pct = 0.57973
        self._filter_volume_ema_span = 320.18
        self._n_positions = 0.0
        self._total_wallet_exposure_limit = 0.0
        self._unstuck_close_pct = 0.052992
        self._unstuck_ema_dist = -0.0465
        self._unstuck_loss_allowance_pct = 0.045415
        self._unstuck_threshold = 0.92228
        self._short = {
            "close_grid_markup_end": self._close_grid_markup_end,
            "close_grid_markup_start": self._close_grid_markup_start,
            # "close_grid_markup_range": self._close_grid_markup_range,
            # "close_grid_min_markup": self._close_grid_min_markup,
            "close_grid_qty_pct": self._close_grid_qty_pct,
            "close_trailing_grid_ratio": self._close_trailing_grid_ratio,
            "close_trailing_qty_pct": self._close_trailing_qty_pct,
            "close_trailing_retracement_pct": self._close_trailing_retracement_pct,
            "close_trailing_threshold_pct": self._close_trailing_threshold_pct,
            "ema_span_0": self._ema_span_0,
            "ema_span_1": self._ema_span_1,
            "enforce_exposure_limit": self._enforce_exposure_limit,
            "entry_grid_double_down_factor": self._entry_grid_double_down_factor,
            "entry_grid_spacing_log_span_hours": self._entry_grid_spacing_log_span_hours,
            "entry_grid_spacing_log_weight": self._entry_grid_spacing_log_weight,
            "entry_grid_spacing_pct": self._entry_grid_spacing_pct,
            "entry_grid_spacing_we_weight": self._entry_grid_spacing_we_weight,
            "entry_initial_ema_dist": self._entry_initial_ema_dist,
            "entry_initial_qty_pct": self._entry_initial_qty_pct,
            "entry_trailing_double_down_factor": self._entry_trailing_double_down_factor,
            "entry_trailing_grid_ratio": self._entry_trailing_grid_ratio,
            "entry_trailing_retracement_pct": self._entry_trailing_retracement_pct,
            "entry_trailing_threshold_pct": self._entry_trailing_threshold_pct,
            "filter_log_range_ema_span": self._filter_log_range_ema_span,
            "filter_volume_drop_pct": self._filter_volume_drop_pct,
            "filter_volume_ema_span": self._filter_volume_ema_span,
            "n_positions": self._n_positions,
            "total_wallet_exposure_limit": self._total_wallet_exposure_limit,
            "unstuck_close_pct": self._unstuck_close_pct,
            "unstuck_ema_dist": self._unstuck_ema_dist,
            "unstuck_loss_allowance_pct": self._unstuck_loss_allowance_pct,
            "unstuck_threshold": self._unstuck_threshold
        }

    def __repr__(self):
        return str(self._short)

    @property
    def short(self): return self._short
    @short.setter
    def short(self, new_short):
        #Fix for old markup parameters
        if "close_grid_markup_range" in new_short and "close_grid_min_markup" in new_short:
            self.close_grid_markup_start = new_short["close_grid_min_markup"] + new_short["close_grid_markup_range"]
            self.close_grid_markup_end = new_short["close_grid_min_markup"]
        if "close_grid_markup_end" in new_short:
            self.close_grid_markup_end = new_short["close_grid_markup_end"]
        if "close_grid_markup_start" in new_short:
            self.close_grid_markup_start = new_short["close_grid_markup_start"]
        if "close_grid_qty_pct" in new_short:
            self.close_grid_qty_pct = new_short["close_grid_qty_pct"]
        if "close_trailing_grid_ratio" in new_short:
            self.close_trailing_grid_ratio = new_short["close_trailing_grid_ratio"]
        if "close_trailing_qty_pct" in new_short:
            self.close_trailing_qty_pct = new_short["close_trailing_qty_pct"]
        if "close_trailing_retracement_pct" in new_short:
            self.close_trailing_retracement_pct = new_short["close_trailing_retracement_pct"]
        if "close_trailing_threshold_pct" in new_short:
            self.close_trailing_threshold_pct = new_short["close_trailing_threshold_pct"]
        if "ema_span_0" in new_short:
            self.ema_span_0 = new_short["ema_span_0"]
        if "ema_span_1" in new_short:
            self.ema_span_1 = new_short["ema_span_1"]
        if "enforce_exposure_limit" in new_short:
            self.enforce_exposure_limit = new_short["enforce_exposure_limit"]
        if "entry_grid_double_down_factor" in new_short:
            self.entry_grid_double_down_factor = new_short["entry_grid_double_down_factor"]
        if "entry_grid_spacing_log_span_hours" in new_short:
            self.entry_grid_spacing_log_span_hours = new_short["entry_grid_spacing_log_span_hours"]
        if "entry_grid_spacing_log_weight" in new_short:
            self.entry_grid_spacing_log_weight = new_short["entry_grid_spacing_log_weight"]
        if "entry_grid_spacing_pct" in new_short:
            self.entry_grid_spacing_pct = new_short["entry_grid_spacing_pct"]
        if "entry_grid_spacing_we_weight" in new_short:
            self.entry_grid_spacing_we_weight = new_short["entry_grid_spacing_we_weight"]
        # Fix for old configs
        elif "entry_grid_spacing_weight" in new_short:
            self.entry_grid_spacing_we_weight = new_short["entry_grid_spacing_weight"]
        if "entry_initial_ema_dist" in new_short:
            self.entry_initial_ema_dist = new_short["entry_initial_ema_dist"]
        if "entry_initial_qty_pct" in new_short:
            self.entry_initial_qty_pct = new_short["entry_initial_qty_pct"]
        if "entry_trailing_double_down_factor" in new_short:
            self.entry_trailing_double_down_factor = new_short["entry_trailing_double_down_factor"]
        else:
            self.entry_trailing_double_down_factor = self.entry_grid_double_down_factor
        if "entry_trailing_grid_ratio" in new_short:
            self.entry_trailing_grid_ratio = new_short["entry_trailing_grid_ratio"]
        if "entry_trailing_retracement_pct" in new_short:
            self.entry_trailing_retracement_pct = new_short["entry_trailing_retracement_pct"]
        if "entry_trailing_threshold_pct" in new_short:
            self.entry_trailing_threshold_pct = new_short["entry_trailing_threshold_pct"]
        if "filter_log_range_ema_span" in new_short:
            self.filter_log_range_ema_span = new_short["filter_log_range_ema_span"]
        # Fix for old configs
        elif "filter_noisiness_rolling_window" in new_short:
            self.filter_log_range_ema_span = new_short["filter_noisiness_rolling_window"]
        elif "filter_rolling_window" in new_short:
            self.filter_log_range_ema_span = new_short["filter_rolling_window"]
        if "filter_volume_drop_pct" in new_short:
            self.filter_volume_drop_pct = new_short["filter_volume_drop_pct"]
        # Fix for old configs
        elif "filter_relative_volume_clip_pct" in new_short:
            self.filter_volume_drop_pct = new_short["filter_relative_volume_clip_pct"]
        if "filter_volume_ema_span" in new_short:
            self.filter_volume_ema_span = new_short["filter_volume_ema_span"]
        # Fix for old configs
        elif "filter_rolling_window" in new_short:
            self.filter_volume_ema_span = new_short["filter_rolling_window"]
        if "n_positions" in new_short:
            self.n_positions = new_short["n_positions"]
        if "total_wallet_exposure_limit" in new_short:
            self.total_wallet_exposure_limit = new_short["total_wallet_exposure_limit"]
        if "unstuck_close_pct" in new_short:
            self.unstuck_close_pct = new_short["unstuck_close_pct"]
        if "unstuck_ema_dist" in new_short:
            self.unstuck_ema_dist = new_short["unstuck_ema_dist"]
        if "unstuck_loss_allowance_pct" in new_short:
            self.unstuck_loss_allowance_pct = new_short["unstuck_loss_allowance_pct"]
        if "unstuck_threshold" in new_short:
            self.unstuck_threshold = new_short["unstuck_threshold"]

    @property
    def close_grid_markup_end(self): return self._close_grid_markup_end
    @property
    def close_grid_markup_start(self): return self._close_grid_markup_start
    # @property
    # def close_grid_markup_range(self): return self._close_grid_markup_range
    # @property
    # def close_grid_min_markup(self): return self._close_grid_min_markup
    @property
    def close_grid_qty_pct(self): return self._close_grid_qty_pct
    @property
    def close_trailing_grid_ratio(self): return self._close_trailing_grid_ratio
    @property
    def close_trailing_qty_pct(self): return self._close_trailing_qty_pct
    @property
    def close_trailing_retracement_pct(self): return self._close_trailing_retracement_pct
    @property
    def close_trailing_threshold_pct(self): return self._close_trailing_threshold_pct
    @property
    def ema_span_0(self): return self._ema_span_0
    @property
    def ema_span_1(self): return self._ema_span_1
    @property
    def enforce_exposure_limit(self): return self._enforce_exposure_limit
    @property
    def entry_grid_double_down_factor(self): return self._entry_grid_double_down_factor
    @property
    def entry_grid_spacing_log_span_hours(self): return self._entry_grid_spacing_log_span_hours
    @property
    def entry_grid_spacing_log_weight(self): return self._entry_grid_spacing_log_weight
    @property
    def entry_grid_spacing_pct(self): return self._entry_grid_spacing_pct
    @property
    def entry_grid_spacing_we_weight(self): return self._entry_grid_spacing_we_weight
    @property
    def entry_initial_ema_dist(self): return self._entry_initial_ema_dist
    @property
    def entry_initial_qty_pct(self): return self._entry_initial_qty_pct
    @property
    def entry_trailing_double_down_factor(self): return self._entry_trailing_double_down_factor
    @property
    def entry_trailing_grid_ratio(self): return self._entry_trailing_grid_ratio
    @property
    def entry_trailing_retracement_pct(self): return self._entry_trailing_retracement_pct
    @property
    def entry_trailing_threshold_pct(self): return self._entry_trailing_threshold_pct
    @property
    def filter_log_range_ema_span(self): return self._filter_log_range_ema_span
    @property
    def filter_volume_drop_pct(self): return self._filter_volume_drop_pct
    @property
    def filter_volume_ema_span(self): return self._filter_volume_ema_span
    @property
    def n_positions(self): return self._n_positions
    @property
    def total_wallet_exposure_limit(self): return self._total_wallet_exposure_limit
    @property
    def unstuck_close_pct(self): return self._unstuck_close_pct
    @property
    def unstuck_ema_dist(self): return self._unstuck_ema_dist
    @property
    def unstuck_loss_allowance_pct(self): return self._unstuck_loss_allowance_pct
    @property
    def unstuck_threshold(self): return self._unstuck_threshold

    @close_grid_markup_end.setter
    def close_grid_markup_end(self, new_close_grid_markup_end):
        self._close_grid_markup_end = new_close_grid_markup_end
        self._short["close_grid_markup_end"] = self._close_grid_markup_end
    @close_grid_markup_start.setter
    def close_grid_markup_start(self, new_close_grid_markup_start):
        self._close_grid_markup_start = new_close_grid_markup_start
        self._short["close_grid_markup_start"] = self._close_grid_markup_start
    # @close_grid_markup_range.setter
    # def close_grid_markup_range(self, new_close_grid_markup_range):
    #     self._close_grid_markup_range = new_close_grid_markup_range
    #     self._short["close_grid_markup_range"] = self._close_grid_markup_range
    # @close_grid_min_markup.setter
    # def close_grid_min_markup(self, new_close_grid_min_markup):
    #     self._close_grid_min_markup = new_close_grid_min_markup
    #     self._short["close_grid_min_markup"] = self._close_grid_min_markup
    @close_grid_qty_pct.setter
    def close_grid_qty_pct(self, new_close_grid_qty_pct):
        self._close_grid_qty_pct = new_close_grid_qty_pct
        self._short["close_grid_qty_pct"] = self._close_grid_qty_pct
    @close_trailing_grid_ratio.setter
    def close_trailing_grid_ratio(self, new_close_trailing_grid_ratio):
        self._close_trailing_grid_ratio = new_close_trailing_grid_ratio
        self._short["close_trailing_grid_ratio"] = self._close_trailing_grid_ratio
    @close_trailing_qty_pct.setter
    def close_trailing_qty_pct(self, new_close_trailing_qty_pct):
        self._close_trailing_qty_pct = new_close_trailing_qty_pct
        self._short["close_trailing_qty_pct"] = self._close_trailing_qty_pct
    @close_trailing_retracement_pct.setter
    def close_trailing_retracement_pct(self, new_close_trailing_retracement_pct):
        self._close_trailing_retracement_pct = new_close_trailing_retracement_pct
        self._short["close_trailing_retracement_pct"] = self._close_trailing_retracement_pct
    @close_trailing_threshold_pct.setter
    def close_trailing_threshold_pct(self, new_close_trailing_threshold_pct):
        self._close_trailing_threshold_pct = new_close_trailing_threshold_pct
        self._short["close_trailing_threshold_pct"] = self._close_trailing_threshold_pct
    @ema_span_0.setter
    def ema_span_0(self, new_ema_span_0):
        self._ema_span_0 = new_ema_span_0
        self._short["ema_span_0"] = self._ema_span_0
    @ema_span_1.setter
    def ema_span_1(self, new_ema_span_1):
        self._ema_span_1 = new_ema_span_1
        self._short["ema_span_1"] = self._ema_span_1
    @enforce_exposure_limit.setter
    def enforce_exposure_limit(self, new_enforce_exposure_limit):
        self._enforce_exposure_limit = new_enforce_exposure_limit
        self._short["enforce_exposure_limit"] = self._enforce_exposure_limit
    @entry_grid_double_down_factor.setter
    def entry_grid_double_down_factor(self, new_entry_grid_double_down_factor):
        self._entry_grid_double_down_factor = new_entry_grid_double_down_factor
        self._short["entry_grid_double_down_factor"] = self._entry_grid_double_down_factor
    @entry_grid_spacing_log_span_hours.setter
    def entry_grid_spacing_log_span_hours(self, new_entry_grid_spacing_log_span_hours):
        self._entry_grid_spacing_log_span_hours = new_entry_grid_spacing_log_span_hours
        self._short["entry_grid_spacing_log_span_hours"] = self._entry_grid_spacing_log_span_hours
    @entry_grid_spacing_log_weight.setter
    def entry_grid_spacing_log_weight(self, new_entry_grid_spacing_log_weight):
        self._entry_grid_spacing_log_weight = new_entry_grid_spacing_log_weight
        self._short["entry_grid_spacing_log_weight"] = self._entry_grid_spacing_log_weight
    @entry_grid_spacing_pct.setter
    def entry_grid_spacing_pct(self, new_entry_grid_spacing_pct):
        self._entry_grid_spacing_pct = new_entry_grid_spacing_pct
        self._short["entry_grid_spacing_pct"] = self._entry_grid_spacing_pct
    @entry_grid_spacing_we_weight.setter
    def entry_grid_spacing_we_weight(self, new_entry_grid_spacing_we_weight):
        self._entry_grid_spacing_we_weight = new_entry_grid_spacing_we_weight
        self._short["entry_grid_spacing_we_weight"] = self._entry_grid_spacing_we_weight
    @entry_initial_ema_dist.setter
    def entry_initial_ema_dist(self, new_entry_initial_ema_dist):
        self._entry_initial_ema_dist = new_entry_initial_ema_dist
        self._short["entry_initial_ema_dist"] = self._entry_initial_ema_dist
    @entry_initial_qty_pct.setter
    def entry_initial_qty_pct(self, new_entry_initial_qty_pct):
        self._entry_initial_qty_pct = new_entry_initial_qty_pct
        self._short["entry_initial_qty_pct"] = self._entry_initial_qty_pct
    @entry_trailing_double_down_factor.setter
    def entry_trailing_double_down_factor(self, new_entry_trailing_double_down_factor):
        self._entry_trailing_double_down_factor = new_entry_trailing_double_down_factor
        self._short["entry_trailing_double_down_factor"] = self._entry_trailing_double_down_factor
    @entry_trailing_grid_ratio.setter
    def entry_trailing_grid_ratio(self, new_entry_trailing_grid_ratio):
        self._entry_trailing_grid_ratio = new_entry_trailing_grid_ratio
        self._short["entry_trailing_grid_ratio"] = self._entry_trailing_grid_ratio
    @entry_trailing_retracement_pct.setter
    def entry_trailing_retracement_pct(self, new_entry_trailing_retracement_pct):
        self._entry_trailing_retracement_pct = new_entry_trailing_retracement_pct
        self._short["entry_trailing_retracement_pct"] = self._entry_trailing_retracement_pct
    @entry_trailing_threshold_pct.setter
    def entry_trailing_threshold_pct(self, new_entry_trailing_threshold_pct):
        self._entry_trailing_threshold_pct = new_entry_trailing_threshold_pct
        self._short["entry_trailing_threshold_pct"] = self._entry_trailing_threshold_pct
    @filter_log_range_ema_span.setter
    def filter_log_range_ema_span(self, new_filter_log_range_ema_span):
        self._filter_log_range_ema_span = new_filter_log_range_ema_span
        self._short["filter_log_range_ema_span"] = self._filter_log_range_ema_span
    @filter_volume_drop_pct.setter
    def filter_volume_drop_pct(self, new_filter_volume_drop_pct):
        self._filter_volume_drop_pct = new_filter_volume_drop_pct
        self._short["filter_volume_drop_pct"] = self._filter_volume_drop_pct
    @filter_volume_ema_span.setter
    def filter_volume_ema_span(self, new_filter_volume_ema_span):
        self._filter_volume_ema_span = new_filter_volume_ema_span
        self._short["filter_volume_ema_span"] = self._filter_volume_ema_span
    @n_positions.setter
    def n_positions(self, new_n_positions):
        self._n_positions = new_n_positions
        self._short["n_positions"] = self._n_positions
    @total_wallet_exposure_limit.setter
    def total_wallet_exposure_limit(self, new_total_wallet_exposure_limit):
        self._total_wallet_exposure_limit = new_total_wallet_exposure_limit
        self._short["total_wallet_exposure_limit"] = self._total_wallet_exposure_limit
    @unstuck_close_pct.setter
    def unstuck_close_pct(self, new_unstuck_close_pct):
        self._unstuck_close_pct = new_unstuck_close_pct
        self._short["unstuck_close_pct"] = self._unstuck_close_pct
    @unstuck_ema_dist.setter
    def unstuck_ema_dist(self, new_unstuck_ema_dist):
        self._unstuck_ema_dist = new_unstuck_ema_dist
        self._short["unstuck_ema_dist"] = self._unstuck_ema_dist
    @unstuck_loss_allowance_pct.setter
    def unstuck_loss_allowance_pct(self, new_unstuck_loss_allowance_pct):
        self._unstuck_loss_allowance_pct = new_unstuck_loss_allowance_pct
        self._short["unstuck_loss_allowance_pct"] = self._unstuck_loss_allowance_pct
    @unstuck_threshold.setter
    def unstuck_threshold(self, new_unstuck_threshold):
        self._unstuck_threshold = new_unstuck_threshold
        self._short["unstuck_threshold"] = self._unstuck_threshold

class Bot:
    def __init__(self):
        self._long = Long()
        self._short = Short()
        self._bot = {
            "long": self._long._long,
            "short": self._short._short
        }    

    def __repr__(self):
        return str(self._bot)
    
    @property
    def bot(self): return self._bot
    @bot.setter
    def bot(self, new_bot):
        if "long" in new_bot:
            self.long = new_bot["long"]
        if "short" in new_bot:
            self.short = new_bot["short"]
    
    @property
    def long(self): return self._long
    @property
    def short(self): return self._short

    @long.setter
    def long(self, new_long):
        self._long.long = new_long
        self._bot["long"] = self._long.long
    @short.setter
    def short(self, new_short):
        self._short.short = new_short
        self._bot["short"] = self._short.short

class ApprovedCoins:
    def __init__(self):
        self._approved_coins = []
    
    def __repr__(self):
        return str(self._approved_coins)

    @property
    def approved_coins(self): return self._approved_coins
    @approved_coins.setter
    def approved_coins(self, new_approved_coins):
        self._approved_coins = new_approved_coins

class IgnoredCoins:
    def __init__(self):
        self._ignored_coins = []
    
    def __repr__(self):
        return str(self._ignored_coins)

    @property
    def ignored_coins(self): return self._ignored_coins
    @ignored_coins.setter
    def ignored_coins(self, new_ignored_coins):
        self._ignored_coins = new_ignored_coins

class Live:
    def __init__(self):
        self._user = None
        self._live = {
            "user": self._user
        }
    
    def __repr__(self):
        return str(self._live)

    @property
    def live(self): return self._live
    @live.setter
    def live(self, new_live):
        if "user" in new_live:
            self.user = new_live["user"]
    
    @property
    def user(self): return self._user
    @user.setter
    def user(self, new_user):
        self._user = new_user
        self._live["user"] = self._user

class Optimize:
    def __init__(self):
        self._n_cpus = multiprocessing.cpu_count()
        self._iters = 10000
        self._passivbot_mode = "recursive_grid"
        self._algorithm = "neat"
        self._optimize = {
            "n_cpus": self._n_cpus,
            "iters": self._iters,
            "passivbot_mode": self._passivbot_mode,
            "algorithm": self._algorithm
        }
    
    def __repr__(self):
        return str(self._optimize)
    
    @property
    def optimize(self): return self._optimize
    @optimize.setter
    def optimize(self, new_optimize):
        if "n_cpus" in new_optimize:
            self.n_cpus = new_optimize["n_cpus"]
        if "iters" in new_optimize:
            self.iters = new_optimize["iters"]
        if "passivbot_mode" in new_optimize:
            self.passivbot_mode = new_optimize["passivbot_mode"]
        if "algorithm" in new_optimize:
            self.algorithm = new_optimize["algorithm"]

    @property
    def n_cpus(self): return self._n_cpus
    @n_cpus.setter
    def n_cpus(self, new_n_cpus):
        self._n_cpus = new_n_cpus
        self._optimize["n_cpus"] = self._n_cpus
    @property
    def iters(self): return self._iters
    @iters.setter
    def iters(self, new_iters):
        self._iters = new_iters
        self._optimize["iters"] = self._iters
    @property
    def passivbot_mode(self): return self._passivbot_mode
    @passivbot_mode.setter
    def passivbot_mode(self, new_passivbot_mode):
        self._passivbot_mode = new_passivbot_mode
        self._optimize["passivbot_mode"] = self._passivbot_mode
    @property
    def algorithm(self): return self._algorithm
    @algorithm.setter
    def algorithm(self, new_algorithm):
        self._algorithm = new_algorithm
        self._optimize["algorithm"] = self._algorithm

class Bounds:
    def __init__(self):
        self._bounds = {}
    
    def __repr__(self):
        return str(self._bounds)

    @property
    def bounds(self): return self._bounds
    @bounds.setter
    def bounds(self, new_bounds):
        self._bounds = new_bounds

class PBGui:
    def __init__(self):
        self._pbgui = {}
    
    def __repr__(self):
        return str(self._pbgui)

    @property
    def pbgui(self): return self._pbgui
    @pbgui.setter
    def pbgui(self, new_pbgui):
        self._pbgui = new_pbgui

class ConfigV7:
    def __init__(self, config_file=None):
        self._config_file = config_file
        self._coin_overrides = {}
        self._logging = Logging()
        self._backtest = Backtest()
        self._bot = Bot()
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





