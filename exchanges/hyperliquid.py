from .base import BaseExchange
from datetime import datetime
import json
from time import sleep

class Hyperliquid(BaseExchange):
    def __init__(self, user=None):
        super().__init__("hyperliquid", user)

    def fetch_ohlcv(self, symbol: str, market_type: str, timeframe: str, limit: int, since: int = None):
        if not self.instance: self.connect()
        
        if not since:
            now = int(datetime.now().timestamp() * 1000)
            if timeframe[-1] == 'm':
                since = now - 1000 * 60 * int(timeframe[0:-1]) * limit
            elif timeframe[-1] == 'h':
                since = now - 1000 * 60 * 60 * int(timeframe[0:-1]) * limit
            elif timeframe[-1] == 'd':
                since = now - 1000 * 60 * 60 * 24 * int(timeframe[0:-1]) * limit
            elif timeframe[-1] == 'w':
                since = now - 1000 * 60 * 60 * 24 * 7 * int(timeframe[0:-1]) * limit
            elif timeframe[-1] == 'M':
                since = now - 1000 * 60 * 60 * 24 * 30 * int(timeframe[0:-1]) * limit
                
        ohlcv = self.instance.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=since, limit=limit)
        return ohlcv

    def fetch_prices(self, symbols: list, market_type: str):
        if not self.instance: self.connect()
        
        fetched = self.instance.fetch(
            "https://api.hyperliquid.xyz/info",
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps({"type": "allMids"}),
        )
        prices = {}
        for symbol in symbols:
            sym = symbol[0:-10]
            if sym in fetched:
                prices[symbol] = {
                    "timestamp": int(datetime.now().timestamp() * 1000),
                    "last": fetched[sym]
                }
        return prices

    def fetch_balance(self, market_type: str, symbol: str = None):
        if not self.instance: self.connect()
        try:
            balance = self.instance.fetch_balance(params={"type": market_type})
        except Exception as e:
            return e
        return float(balance["total"]["USDC"])

    def fetch_history(self, since: int = None):
        if self.user.key == 'key':
            return []
        all_histories = []
        all = []
        if not self.instance: self.connect()
        
        hour = 60 * 60 * 1000
        day = 24 * 60 * 60 * 1000
        week = 7 * day
        max_days = 365 * day
        now = self.instance.milliseconds()
        
        if not since:
            since = now - max_days
        else:
            # For make sure not to miss any funding or trading history
            since -= hour
            
        limit = 500
        end = since + week
        since_trades = since
        end_trades = end
        
        # Fetch Funding
        while True:
            fundings = self.instance.fetch(
                "https://api.hyperliquid.xyz/info",
                method="POST",
                headers={"Content-Type": "application/json"},
                body=json.dumps({"type": "userFunding", "user": self.user.wallet_address, "startTime": since, "endTime": end}),
                )
            if fundings:
                first_funding = fundings[0]
                last_funding = fundings[-1]
                all_histories = fundings + all_histories
            if len(fundings) == limit:
                print(f'User:{self.user.name} Fetched', len(fundings), 'fundings from', self.instance.iso8601(int(first_funding['time'])), 'till', self.instance.iso8601(int(last_funding['time'])))
                since = int(fundings[-1]['time'])
            else:
                print(f'User:{self.user.name} Fetched', len(fundings), 'fundings from', self.instance.iso8601(since), 'till', self.instance.iso8601(end))
                since = end
                end = since + week
            if since > now:
                print(f'User:{self.user.name} Done')
                break
            sleep(1)
            
        for history in all_histories:
            income = {}
            income["symbol"] = history["delta"]["coin"] + "USDC"
            income["timestamp"] = history["time"]
            income["income"] = history["delta"]["usdc"]
            income["uniqueid"] = history["time"] + "_" + history["delta"]["coin"]
            all.append(income)
            
        # Fetch Trades
        since = since_trades
        end = end_trades
        all_histories = []
        while True:
            trades = self.instance.fetch_my_trades(since=since, limit=limit, params = {"endTime": end})
            if trades:
                first_trade = trades[0]
                last_trade = trades[-1]
                all_histories = trades + all_histories
            if len(trades) == limit:
                print(f'User:{self.user.name} Fetched', len(trades), 'trades from', self.instance.iso8601(first_trade['timestamp']), 'till', self.instance.iso8601(last_trade['timestamp']))
                since = trades[-1]['timestamp']
            else:
                print(f'User:{self.user.name} Fetched', len(trades), 'trades from', self.instance.iso8601(since), 'till', self.instance.iso8601(end))
                since = end
                end = since + week
            if since > now:
                print(f'User:{self.user.name} Done')
                break
            sleep(1)
            
        for history in all_histories:
            income = {}
            income["symbol"] = history["info"]["coin"] + "USDC"
            income["timestamp"] = history["timestamp"]
            income["income"] = float(history["info"]["closedPnl"]) - float(history["info"]["fee"])
            income["uniqueid"] = history["info"]["tid"]
            all.append(income)
            
        return all

    def symbol_to_exchange_symbol(self, symbol: str, market_type: str):
        return f'{symbol[0:-4]}/USDC:USDC'

    def fetch_symbol_info(self, symbol: str, market_type: str):
        if not self.instance: self.connect()
        if not self._markets: self._markets = self.instance.load_markets()
        
        if symbol[-4:] == 'USDC':
            symbol = f'{symbol[0:-4]}/USDC:USDC'
        else:
            symbol = f'{symbol[0:-4]}/USDT:USDT'
            
        symbol_info = self._markets[symbol]
        
        min_costs = max(
            5.1, 0.1 if symbol_info["limits"]["cost"]["min"] is None else symbol_info["limits"]["cost"]["min"]
        )
        min_qtys = symbol_info["limits"]["amount"]["min"]
        qty_steps = symbol_info["precision"]["amount"]
        price_steps = symbol_info["precision"]["price"]
        c_mults = symbol_info["contractSize"]
        
        return symbol_info, min_costs, min_qtys, price_steps, qty_steps, c_mults

    def fetch_symbols(self):
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} DEBUG: [{self.id}] Connecting to exchange...')
        if not self.instance: self.connect()
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} DEBUG: [{self.id}] Loading markets from exchange...')
        self._markets = self.instance.load_markets()
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} DEBUG: [{self.id}] Loaded {len(self._markets)} markets')
        self.swap = []
        self.spot = []
        
        for (k,v) in list(self._markets.items()):
            if v["swap"] and v["active"] and v["linear"]:
                if v["symbol"].endswith('USDC'):
                    self.swap.append(v["symbol"][0:-5].replace("/", "").replace("-", ""))
        
        self.save_symbols()

    def fetch_symbol_infos(self, symbol: str):
        if not self.instance:
            self.connect()
            self._markets = self.instance.load_markets()
        
        symbol = f'{symbol[0:-4]}/USDC:USDC'
        
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
        contractSize = symbol_info["contractSize"]
        if symbol_info["limits"]["amount"]["min"]:
            min_amount = symbol_info["limits"]["amount"]["min"]
        elif symbol_info["precision"]["amount"]:
            min_amount = symbol_info["precision"]["amount"]
            
        min_qty = min_amount * contractSize
        price = self.fetch_price(symbol, "swap")['last']
        min_price = min_qty * price
        
        if symbol_info["limits"]["cost"]["min"]:
            min_cost = symbol_info["limits"]["cost"]["min"]
        else:
            min_cost = 0.0
        if min_cost > min_price:
            min_price = min_cost
        return min_price, price, contractSize, min_amount, min_cost, lev
