from .coins import ApprovedCoins, IgnoredCoins

class Live:
    def __init__(self):
        self._approved_coins = ApprovedCoins()
        self._auto_gs = True
        self._inactive_coin_candle_ttl_minutes = 10.0
        self._empty_means_all_approved = False
        self._execution_delay_seconds = 2.0
        self._filter_by_min_effective_cost = True
        self._forced_mode_long = ""
        self._forced_mode_short = ""
        self._ignored_coins = IgnoredCoins()
        self._leverage = 10.0
        self._market_orders_allowed = True
        self._max_disk_candles_per_symbol_per_tf = 2000000
        self._max_memory_candles_per_symbol = 20000
        self._max_n_cancellations_per_batch = 5
        self._max_n_creations_per_batch = 3
        self._max_n_restarts_per_day = 10
        self._minimum_coin_age_days = 30.0
        self._pnls_max_lookback_days = 30.0
        self._price_distance_threshold = 0.002
        self._time_in_force = "good_till_cancelled"
        self._warmup_ratio = 0.2
        self._user = "bybit_01"

        self._live = {
            "approved_coins": self._approved_coins._approved_coins,
            "auto_gs": self._auto_gs,
            "inactive_coin_candle_ttl_minutes": self._inactive_coin_candle_ttl_minutes,
            "empty_means_all_approved": self._empty_means_all_approved,
            "execution_delay_seconds": self._execution_delay_seconds,
            "filter_by_min_effective_cost": self._filter_by_min_effective_cost,
            "forced_mode_long": self._forced_mode_long,
            "forced_mode_short": self._forced_mode_short,
            "ignored_coins": self._ignored_coins._ignored_coins,
            "leverage": self._leverage,
            "market_orders_allowed": self._market_orders_allowed,
            "max_disk_candles_per_symbol_per_tf": self._max_disk_candles_per_symbol_per_tf,
            "max_memory_candles_per_symbol": self._max_memory_candles_per_symbol,
            "max_n_cancellations_per_batch": self._max_n_cancellations_per_batch,
            "max_n_creations_per_batch": self._max_n_creations_per_batch,
            "max_n_restarts_per_day": self._max_n_restarts_per_day,
            "minimum_coin_age_days": self._minimum_coin_age_days,
            "pnls_max_lookback_days": self._pnls_max_lookback_days,
            "price_distance_threshold": self._price_distance_threshold,
            "time_in_force": self._time_in_force,
            "warmup_ratio": self._warmup_ratio,
            "user": self._user
        }
    
    def __repr__(self):
        return str(self._live)

    @property
    def live(self): return self._live
    @live.setter
    def live(self, new_live):
        if "approved_coins" in new_live:
            self.approved_coins = new_live["approved_coins"]
        if "auto_gs" in new_live:
            self.auto_gs = new_live["auto_gs"]
        if "inactive_coin_candle_ttl_minutes" in new_live:
            self.inactive_coin_candle_ttl_minutes = new_live["inactive_coin_candle_ttl_minutes"]
        if "empty_means_all_approved" in new_live:
            self.empty_means_all_approved = new_live["empty_means_all_approved"]
        if "execution_delay_seconds" in new_live:
            self.execution_delay_seconds = new_live["execution_delay_seconds"]
        if "filter_by_min_effective_cost" in new_live:
            self.filter_by_min_effective_cost = new_live["filter_by_min_effective_cost"]
        if "forced_mode_long" in new_live:
            self.forced_mode_long = new_live["forced_mode_long"]
        if "forced_mode_short" in new_live:
            self.forced_mode_short = new_live["forced_mode_short"]
        if "ignored_coins" in new_live:
            self.ignored_coins = new_live["ignored_coins"]
        if "leverage" in new_live:
            self.leverage = new_live["leverage"]
        if "market_orders_allowed" in new_live:
            self.market_orders_allowed = new_live["market_orders_allowed"]
        if "max_disk_candles_per_symbol_per_tf" in new_live:
            self.max_disk_candles_per_symbol_per_tf = new_live["max_disk_candles_per_symbol_per_tf"]
        if "max_memory_candles_per_symbol" in new_live:
            self.max_memory_candles_per_symbol = new_live["max_memory_candles_per_symbol"]
        if "max_n_cancellations_per_batch" in new_live:
            self.max_n_cancellations_per_batch = new_live["max_n_cancellations_per_batch"]
        if "max_n_creations_per_batch" in new_live:
            self.max_n_creations_per_batch = new_live["max_n_creations_per_batch"]
        if "max_n_restarts_per_day" in new_live:
            self.max_n_restarts_per_day = new_live["max_n_restarts_per_day"]
        if "minimum_coin_age_days" in new_live:
            self.minimum_coin_age_days = new_live["minimum_coin_age_days"]
        if "pnls_max_lookback_days" in new_live:
            self.pnls_max_lookback_days = new_live["pnls_max_lookback_days"]
        if "price_distance_threshold" in new_live:
            self.price_distance_threshold = new_live["price_distance_threshold"]
        if "time_in_force" in new_live:
            self.time_in_force = new_live["time_in_force"]
        if "warmup_ratio" in new_live:
            self._warmup_ratio = new_live["warmup_ratio"]
        if "user" in new_live:
            self.user = new_live["user"]
    
    @property
    def approved_coins(self): return self._approved_coins
    @property
    def auto_gs(self): return self._auto_gs
    @property
    def inactive_coin_candle_ttl_minutes(self): return self._inactive_coin_candle_ttl_minutes
    @property
    def empty_means_all_approved(self): return self._empty_means_all_approved
    @property
    def execution_delay_seconds(self): return self._execution_delay_seconds
    @property
    def filter_by_min_effective_cost(self): return self._filter_by_min_effective_cost
    @property
    def forced_mode_long(self): return self._forced_mode_long
    @property
    def forced_mode_short(self): return self._forced_mode_short
    @property
    def ignored_coins(self): return self._ignored_coins
    @property
    def leverage(self): return self._leverage
    @property
    def market_orders_allowed(self): return self._market_orders_allowed
    @property
    def max_disk_candles_per_symbol_per_tf(self): return self._max_disk_candles_per_symbol_per_tf
    @property
    def max_memory_candles_per_symbol(self): return self._max_memory_candles_per_symbol
    @property
    def max_n_cancellations_per_batch(self): return self._max_n_cancellations_per_batch
    @property
    def max_n_creations_per_batch(self): return self._max_n_creations_per_batch
    @property
    def max_n_restarts_per_day(self): return self._max_n_restarts_per_day
    @property
    def minimum_coin_age_days(self): return self._minimum_coin_age_days
    @property
    def pnls_max_lookback_days(self): return self._pnls_max_lookback_days
    @property
    def price_distance_threshold(self): return self._price_distance_threshold
    @property
    def time_in_force(self): return self._time_in_force
    @property
    def warmup_ratio(self): return self._warmup_ratio
    @property
    def user(self): return self._user

    @approved_coins.setter
    def approved_coins(self, new_approved_coins):
        self._approved_coins.approved_coins = new_approved_coins
        self._live["approved_coins"] = self._approved_coins.approved_coins
    @auto_gs.setter
    def auto_gs(self, new_auto_gs):
        self._auto_gs = new_auto_gs
        self._live["auto_gs"] = self._auto_gs
    @inactive_coin_candle_ttl_minutes.setter
    def inactive_coin_candle_ttl_minutes(self, new_inactive_coin_candle_ttl_minutes):
        self._inactive_coin_candle_ttl_minutes = new_inactive_coin_candle_ttl_minutes
        self._live["inactive_coin_candle_ttl_minutes"] = self._inactive_coin_candle_ttl_minutes
    @empty_means_all_approved.setter
    def empty_means_all_approved(self, new_empty_means_all_approved):
        self._empty_means_all_approved = new_empty_means_all_approved
        self._live["empty_means_all_approved"] = self._empty_means_all_approved
    @execution_delay_seconds.setter
    def execution_delay_seconds(self, new_execution_delay_seconds):
        self._execution_delay_seconds = new_execution_delay_seconds
        self._live["execution_delay_seconds"] = self._execution_delay_seconds
    @filter_by_min_effective_cost.setter
    def filter_by_min_effective_cost(self, new_filter_by_min_effective_cost):
        self._filter_by_min_effective_cost = new_filter_by_min_effective_cost
        self._live["filter_by_min_effective_cost"] = self._filter_by_min_effective_cost
    @forced_mode_long.setter
    def forced_mode_long(self, new_forced_mode_long):
        self._forced_mode_long = new_forced_mode_long
        self._live["forced_mode_long"] = self._forced_mode_long
    @forced_mode_short.setter
    def forced_mode_short(self, new_forced_mode_short):
        self._forced_mode_short = new_forced_mode_short
        self._live["forced_mode_short"] = self._forced_mode_short
    @ignored_coins.setter
    def ignored_coins(self, new_ignored_coins):
        self._ignored_coins.ignored_coins = new_ignored_coins
        self._live["ignored_coins"] = self._ignored_coins.ignored_coins
    @leverage.setter
    def leverage(self, new_leverage):
        self._leverage = new_leverage
        self._live["leverage"] = self._leverage
    @market_orders_allowed.setter
    def market_orders_allowed(self, new_market_orders_allowed):
        self._market_orders_allowed = new_market_orders_allowed
        self._live["market_orders_allowed"] = self._market_orders_allowed
    @max_disk_candles_per_symbol_per_tf.setter
    def max_disk_candles_per_symbol_per_tf(self, new_max_disk_candles_per_symbol_per_tf):
        self._max_disk_candles_per_symbol_per_tf = new_max_disk_candles_per_symbol_per_tf
        self._live["max_disk_candles_per_symbol_per_tf"] = self._max_disk_candles_per_symbol_per_tf
    @max_memory_candles_per_symbol.setter
    def max_memory_candles_per_symbol(self, new_max_memory_candles_per_symbol):
        self._max_memory_candles_per_symbol = new_max_memory_candles_per_symbol
        self._live["max_memory_candles_per_symbol"] = self._max_memory_candles_per_symbol
    @max_n_cancellations_per_batch.setter
    def max_n_cancellations_per_batch(self, new_max_n_cancellations_per_batch):
        self._max_n_cancellations_per_batch = new_max_n_cancellations_per_batch
        self._live["max_n_cancellations_per_batch"] = self._max_n_cancellations_per_batch
    @max_n_creations_per_batch.setter
    def max_n_creations_per_batch(self, new_max_n_creations_per_batch):
        self._max_n_creations_per_batch = new_max_n_creations_per_batch
        self._live["max_n_creations_per_batch"] = self._max_n_creations_per_batch
    @max_n_restarts_per_day.setter
    def max_n_restarts_per_day(self, new_max_n_restarts_per_day):
        self._max_n_restarts_per_day = new_max_n_restarts_per_day
        self._live["max_n_restarts_per_day"] = self._max_n_restarts_per_day
    @minimum_coin_age_days.setter
    def minimum_coin_age_days(self, new_minimum_coin_age_days):
        self._minimum_coin_age_days = new_minimum_coin_age_days
        self._live["minimum_coin_age_days"] = self._minimum_coin_age_days
    @pnls_max_lookback_days.setter
    def pnls_max_lookback_days(self, new_pnls_max_lookback_days):
        self._pnls_max_lookback_days = new_pnls_max_lookback_days
        self._live["pnls_max_lookback_days"] = self._pnls_max_lookback_days
    @price_distance_threshold.setter
    def price_distance_threshold(self, new_price_distance_threshold):
        self._price_distance_threshold = new_price_distance_threshold
        self._live["price_distance_threshold"] = self._price_distance_threshold
    @time_in_force.setter
    def time_in_force(self, new_time_in_force):
        self._time_in_force = new_time_in_force
        self._live["time_in_force"] = self._time_in_force
    @warmup_ratio.setter
    def warmup_ratio(self, new_warmup_ratio):
        self._warmup_ratio = new_warmup_ratio
        self._live["warmup_ratio"] = self._warmup_ratio
    @user.setter
    def user(self, new_user):
        self._user = new_user
        self._live["user"] = self._user
