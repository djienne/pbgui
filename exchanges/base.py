import ccxt
import configparser
import json
from pathlib import Path
from time import sleep
from datetime import datetime
from enum import Enum
from User import User, Users
from pbgui.pbgui_purefunc import PBGDIR, save_ini_batch


def is_ascii_symbol(symbol: str) -> bool:
    """
    Check if a symbol contains only ASCII characters (Latin alphabet, numbers, punctuation).
    Returns False for symbols with Chinese, Cyrillic, or other non-Latin characters.
    """
    try:
        symbol.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

def filter_ascii_symbols(symbols: list) -> list:
    """
    Filter a list of symbols to include only those with ASCII characters.
    Logs and discards any symbols with non-ASCII characters.
    """
    filtered = []
    discarded = []
    for symbol in symbols:
        if is_ascii_symbol(symbol):
            filtered.append(symbol)
        else:
            discarded.append(symbol)

    if discarded:
        print(f'WARNING: Discarded {len(discarded)} non-ASCII symbols: {discarded}')

    return filtered

class Exchanges(Enum):
    BINANCE = 'binance'
    BYBIT = 'bybit'
    BITGET = 'bitget'
    GATEIO = 'gateio'
    HYPERLIQUID = 'hyperliquid'
    OKX = 'okx'
    KUCOIN = 'kucoin'
    BINGX = 'bingx'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Exchanges))

class Spot(Enum):
    BINANCE = 'binance'
    BYBIT = 'bybit'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Spot))

class Single(Enum):
    BINANCE = 'binance'
    BYBIT = 'bybit'
    BITGET = 'bitget'
    OKX = 'okx'
    KUCOIN = 'kucoin'
    BINGX = 'bingx'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Single))

class V7(Enum):
    BINANCE = 'binance'
    BYBIT = 'bybit'
    BITGET = 'bitget'
    GATEIO = 'gateio'
    HYPERLIQUID = 'hyperliquid'
    OKX = 'okx'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, V7))

class Passphrase(Enum):
    BITGET = 'bitget'
    OKX = 'okx'
    KUCOIN = 'kucoin'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Passphrase))

class BaseExchange:
    def __init__(self, id: str, user: User = None):
        self.name = id
        self.id = "kucoinfutures" if id == "kucoin" else id
        self.instance = None
        self._markets = None
        self._tf = None
        self.spot = []
        self.swap = []
        self.cpt = []
        self._user = user
        self.error = None

    @property
    def user(self): return self._user

    @property
    def tf(self):
        if not self._tf:
            self.connect()
            self._tf = list(self.instance.timeframes.keys())
            if "1s" in self._tf:
                self._tf.remove('1s')
        return self._tf

    @user.setter
    def user(self, new_user):
        if self._user != new_user:
            self._user = new_user

    def connect(self):
        self.instance = getattr(ccxt, self.id) ()
        if self._user and self.user.key != 'key':
            self.instance.apiKey = self.user.key
            self.instance.secret = self.user.secret
            self.instance.password = self.user.passphrase
            self.instance.walletAddress = self.user.wallet_address
            self.instance.privateKey = self.user.private_key
        try:
            self.instance.checkRequiredCredentials()
        except Exception as e:
            self.error = (str(e))
            return

    def fetch_ohlcv(self, symbol: str, market_type: str, timeframe: str, limit: int, since : int = None):
        if not self.instance: self.connect()
        if since:
            ohlcv = self.instance.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=since, limit=limit)
        else:
            ohlcv = self.instance.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit)
        return ohlcv

    def fetch_price(self, symbol: str, market_type: str):
        if not self.instance: self.connect()
        price = self.instance.fetch_ticker(symbol=symbol)
        return price

    def fetch_prices(self, symbols: list, market_type: str):
        if not self.instance: self.connect()
        prices = self.instance.fetch_tickers(symbols=symbols)
        return prices

    def fetch_open_orders(self, symbol: str, market_type: str):
        if not self.instance: self.connect()
        orders = self.instance.fetch_open_orders(symbol=symbol)
        return orders

    def fetch_all_open_orders(self, symbol: str):
        if not self.instance: self.connect()
        orders = self.instance.fetch_open_orders(symbol=symbol)
        return orders

    def fetch_position(self, symbol: str, market_type: str):
        if not self.instance: self.connect()
        position = self.instance.fetch_position(symbol=symbol)
        return position

    def fetch_positions(self):
        if not self.instance: self.connect()
        positions = self.instance.fetch_positions()
        return positions

    def fetch_balance(self, market_type: str, symbol : str = None):
        if not self.instance: self.connect()
        try:
            balance = self.instance.fetch_balance(params = {"type": market_type})
        except Exception as e:
            return e
        return float(balance["total"]["USDT"])

    def fetch_timestamp(self):
        if not self.instance: self.connect()
        return self.instance.milliseconds()

    def fetch_spot(self, since: int = None):
        if self.user.key == 'key':
            return []
        return []

    def save_income_other(self, history : list, exchange: str):
        dest = Path(f'{PBGDIR}/data/logs')
        if not dest.exists():
            dest.mkdir(parents=True)
        file = Path(f"{PBGDIR}/data/logs/income_other_{exchange}.json")
        with open(file, 'a', encoding='utf-8') as f:
            json.dump(history, f, indent=4)

    def fetch_history(self, since: int = None):
        return []

    def fetch_trades(self, symbol: str, market_type: str, since: int):
        return []

    def symbol_to_exchange_symbol(self, symbol: str, market_type: str):
        if market_type == "spot":
            return f'{symbol[0:-4]}/USDT'
        else:
            return symbol

    def load_market(self):
        if not self.instance: self.connect()
        self._markets = self.instance.load_markets()
        return self._markets

    def fetch_symbol_info(self, symbol: str, market_type: str):
        if not self.instance: self.connect()
        if not self._markets: self._markets = self.instance.load_markets()
        # Default implementation, override in subclasses
        symbol_info = self._markets[symbol]
        min_costs = max(
            5.1, 0.1 if symbol_info["limits"]["cost"]["min"] is None else symbol_info["limits"]["cost"]["min"]
        )
        min_qtys = symbol_info["limits"]["amount"]["min"]
        qty_steps = symbol_info["precision"]["amount"]
        price_steps = symbol_info["precision"]["price"]
        c_mults = symbol_info["contractSize"]
        return symbol_info, min_costs, min_qtys, price_steps, qty_steps, c_mults

    def fetch_copytrading_symbols(self):
        return []

    def fetch_symbols(self):
        # Common logic for fetching and saving symbols
        # This might need to be abstract or have a default implementation that calls load_markets
        pass

    def save_symbols(self):
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} DEBUG: [{self.id}] Saving symbols to pbgui.ini...')
        updates = {
            "exchanges": {
                f'{self.id}.swap': f'{self.swap}'
            }
        }
        if self.spot:
            updates["exchanges"][f'{self.id}.spot'] = f'{self.spot}'
        if self.cpt:
            updates["exchanges"][f'{self.id}.cpt'] = f'{self.cpt}'

        save_ini_batch(updates)
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} DEBUG: [{self.id}] Successfully saved symbols to pbgui.ini')

    def load_symbols(self):
        pb_config = configparser.ConfigParser()
        pb_config.read('pbgui.ini', encoding='utf-8')
        if pb_config.has_option("exchanges", f'{self.id}.spot'):
            self.spot = eval(pb_config.get("exchanges", f'{self.id}.spot'))
            self.spot = filter_ascii_symbols(self.spot)
        if pb_config.has_option("exchanges", f'{self.id}.swap'):
            self.swap = eval(pb_config.get("exchanges", f'{self.id}.swap'))
            self.swap = filter_ascii_symbols(self.swap)
        if not self.spot and not self.swap:
            self.fetch_symbols()

    def fetch_symbol_infos(self, symbol: str):
        # Default implementation
        if not self.instance:
            self.connect()
            self._markets = self.instance.load_markets()

        # Convert from passivbot format (e.g., "SOLUSDT") to CCXT format (e.g., "SOL/USDT:USDT")
        if symbol.endswith('USDT') and '/' not in symbol:
            symbol = f'{symbol[0:-4]}/USDT:USDT'

        if not self._markets:
            try:
                self._markets = self.instance.load_markets()
            except:
                return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        if symbol not in self._markets:
            return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        symbol_info = self._markets[symbol]
        
        if symbol_info["limits"]["leverage"]["max"] is None:
            lev = "unknown"
        else:
            lev = symbol_info["limits"]["leverage"]["max"]

        # Get contract size with fallback
        contractSize = symbol_info.get("contractSize", 1.0)
        if contractSize is None:
            contractSize = 1.0

        # Get min_amount with proper null handling
        min_amount = symbol_info["limits"]["amount"]["min"]
        if min_amount is None:
            min_amount = symbol_info["precision"]["amount"]
        if min_amount is None:
            min_amount = 0.001  # Fallback default

        min_qty = min_amount * contractSize
        price = self.fetch_price(symbol, "swap")['last']
        min_price = min_qty * price

        # Get min_cost with proper default (exchanges typically require 1-5 USDT minimum)
        min_cost = symbol_info["limits"]["cost"]["min"]
        if min_cost is None:
            min_cost = 1.0  # Default minimum cost in USDT

        # Ensure min_price meets the exchange's minimum cost requirement
        if min_cost > min_price:
            min_price = min_cost

        return min_price, price, contractSize, min_amount, min_cost, lev

    def calculate_balance_needed(self, symbols: list, twe: float, entry_initial_qty_pct: float):
        balance_needed = 0.0
        we = twe / len(symbols)
        for symbol in symbols:
            # Note: fetch_symbol_min_order_price was not in the original Exchange.py snippet I saw, 
            # but it was called in main(). I'll assume it's similar to fetch_symbol_infos returning min_price
            # Wait, fetch_symbol_infos returns min_price as first return value.
            min_price, _, _, _, _, _ = self.fetch_symbol_infos(symbol)
            balance_needed_symbol = min_price / we / entry_initial_qty_pct
            balance_needed += balance_needed_symbol
        return balance_needed
