from .base import BaseExchange
from datetime import datetime

class Kucoin(BaseExchange):
    def __init__(self, user=None):
        super().__init__("kucoin", user)

    def fetch_history(self, since: int = None):
        if self.user.key == 'key':
            return []
        all_histories = []
        all = []
        if not self.instance: self.connect()
        
        day = 24 * 60 * 60 * 1000
        week = 7 * day
        max_days = 120 * day
        now = self.instance.milliseconds()
        if not since:
            since = now - max_days
        limit = 100
        end = since + week
        while True:
            ledgers = self.instance.fetch_ledger(since=since, limit=limit, params={"end": end})
            if ledgers:
                first_ledger = ledgers[0]
                last_ledger = ledgers[-1]
                all_histories = ledgers + all_histories
            if len(ledgers) == limit:
                print(f'User:{self.user.name} Fetched', len(ledgers), 'ledgers from', self.instance.iso8601(first_ledger['timestamp']), 'till', self.instance.iso8601(last_ledger['timestamp']))
                end = ledgers[0]['timestamp']
            else:
                print(f'User:{self.user.name} Fetched', len(ledgers), 'ledgers from', self.instance.iso8601(since), 'till', self.instance.iso8601(end))
                since = since + week
                end = since + week
            if since > now:
                print(f'User:{self.user.name} Done')
                break
        for history in all_histories:
            if history["type"] in ["RealisedPNL","FundingFee"]:
                income = {}
                income["symbol"] = history["info"]["currency"]
                income["timestamp"] = history["timestamp"]
                income["income"] = history["amount"]
                income["uniqueid"] = history["id"]
                all.append(income)
            else: 
                self.save_income_other(history, self.user.name)
        return all

    def fetch_trades(self, symbol: str, market_type: str, since: int):
        all_trades = []
        if not self.instance: self.connect()
        
        week = 7 * 24 * 60 * 60 * 1000
        now = self.instance.milliseconds()
        limit = 100
        end = since + week
        while True:
            trades = self.instance.fetch_my_trades(symbol=symbol, since=since, limit=limit, params={"endAt": end})
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
        return f'{symbol}M'

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
                if v["id"][-5:] == 'USDTM':
                    self.swap.append(v["id"][:len(v["id"])-1])
        
        self.save_symbols()
