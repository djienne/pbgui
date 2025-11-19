from .base import BaseExchange
from datetime import datetime

class Gateio(BaseExchange):
    def __init__(self, user=None):
        super().__init__("gateio", user)

    def fetch_trades(self, symbol: str, market_type: str, since: int):
        all_trades = []
        if not self.instance: self.connect()
        
        week = 7 * 24 * 60 * 60 * 1000
        now = self.instance.milliseconds()
        limit = 100
        end = since + week
        while True:
            trades = self.instance.fetch_my_trades(symbol=symbol, since=since, limit=limit, params={"end": end})
            if trades:
                first_trade = trades[0]
                last_trade = trades[-1]
                all_trades = trades + all_trades
                print(f'User:{self.user.name} Symbol:{symbol} Fetched', len(trades), 'trades from', first_trade['timestamp'], 'till', last_trade['timestamp'])
            if len(trades) == limit:
                end = trades[0]['timestamp']
            else:
                print(f'User:{self.user.name} Symbol:{symbol} Fetched', len(trades), 'trades from', self.instance.iso8601(since), 'till', self.instance.iso8601(end))
                since += week
                end = since + week
            if since > now:
                print(f'User:{self.user.name} Symbol:{symbol} Done')
                break
        
        if all_trades:
            sort_trades = sorted(all_trades, key=lambda d: d['timestamp'])
            return sort_trades
        return []

    def symbol_to_exchange_symbol(self, symbol: str, market_type: str):
        if market_type == "spot":
            return f'{symbol[0:-4]}/USDT'
        else:
            return symbol

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
                if v["id"].endswith('USDT'):
                    self.swap.append(''.join(v["id"].split("_")))
        
        self.save_symbols()
