import datetime

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
