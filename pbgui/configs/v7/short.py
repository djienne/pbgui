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
