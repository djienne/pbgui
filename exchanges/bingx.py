from .base import BaseExchange
from datetime import datetime

class BingX(BaseExchange):
    def __init__(self, user=None):
        super().__init__("bingx", user)

    def fetch_trades(self, symbol: str, market_type: str, since: int):
        all_trades = []
        bingx_trades = []
        if not self.instance: self.connect()
        
        week = 7 * 24 * 60 * 60 * 1000
        now = self.instance.milliseconds()
        limit = 100
        end = since + week
        offset = 0
        while True:
            trades = self.instance.fetch_my_trades(symbol=symbol, since=since, limit=limit, params={"offset": offset})
            if trades:
                first_trade = trades[0]
                last_trade = trades[-1]
                bingx_trades = trades + bingx_trades
                print(f'User:{self.user.name} Symbol:{symbol} Fetched', len(trades), 'trades from', first_trade['timestamp'], 'till', last_trade['timestamp'])
            if len(trades) == limit:
                offset += 100
            else:
                print(f'User:{self.user.name} Symbol:{symbol} Fetched', len(trades), 'trades from', self.instance.iso8601(since), 'till', self.instance.iso8601(end))
                since += week
                end = since + week
                offset = 0
            if since > now:
                print(f'User:{self.user.name} Symbol:{symbol} Done')
                break
        
        # BingX returns trades in reverse order sometimes? The original code appended to bingx_trades and then assigned to all_trades
        # Original code:
        # bingx_trades = []
        # ...
        # bingx_trades = trades + bingx_trades
        # ...
        # all_trades = bingx_trades
        
        if bingx_trades:
            sort_trades = sorted(bingx_trades, key=lambda d: d['timestamp'])
            return sort_trades
        return []

    def symbol_to_exchange_symbol(self, symbol: str, market_type: str):
        return f'{symbol[0:-4]}/USDT:USDT'

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
                    self.swap.append(''.join(v["id"].split("-")))
        
        self.save_symbols()
