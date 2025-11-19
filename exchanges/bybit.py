from .base import BaseExchange
from datetime import datetime
from time import sleep

class Bybit(BaseExchange):
    def __init__(self, user=None):
        super().__init__("bybit", user)

    def fetch_open_orders(self, symbol: str, market_type: str):
        if not self.instance: self.connect()
        if market_type == "spot":
            orders = self.instance.fetch_open_orders(symbol=symbol, params={"type": market_type})
        else:
            orders = self.instance.fetch_open_orders(symbol=symbol)
        return orders

    def fetch_balance(self, market_type: str, symbol: str = None):
        if not self.instance: self.connect()
        try:
            balance = self.instance.fetch_balance(params={"type": market_type})
        except Exception as e:
            return e
        
        if market_type == 'swap':
            balinfo = balance["info"]["result"]["list"][0]
            if balinfo["accountType"] == "UNIFIED":
                return float(balinfo["totalWalletBalance"])
            elif "USDT" in balance["total"]:
                return float(balance["total"]["USDT"])
            else:
                return float(0)
        else:
            if symbol:
                if symbol.endswith('USDT'):
                    symbol = symbol.replace("USDT", "")
                elif symbol.endswith('USDC'):
                    symbol = symbol.replace("USDC", "")
                elif symbol.endswith('BTC'):
                    symbol = symbol.replace("BTC", "")
                elif symbol.endswith('EUR'):
                    symbol = symbol.replace("EUR", "")
                return float(balance["total"][symbol])
            else:
                if "USDT" in balance["total"]:
                    return float(balance["total"]["USDT"])
                else:
                    return float(0)

    def fetch_spot(self, since: int = None):
        if self.user.key == 'key':
            return []
        all_histories = []
        all = []
        if not self.instance: self.connect()
        
        day = 24 * 60 * 60 * 1000
        week = 7 * day
        max_days = 2 * 365 * day - day
        now = self.instance.milliseconds()
        if not since:
            since = now - max_days
        limit = 100
        end = since + week
        while True:
            trades = self.instance.fetch_my_trades(since=since, limit=limit, params={'type': 'spot', "endTime": end})
            if trades:
                first_trade = trades[0]
                last_trade = trades[-1]
                all_histories = trades + all_histories
            if len(trades) == limit:
                print(f'User:{self.user.name} Fetched', len(trades), 'trades from', self.instance.iso8601(first_trade['timestamp']), 'till', self.instance.iso8601(last_trade['timestamp']))
                end = trades[0]['timestamp']
            else:
                print(f'User:{self.user.name} Fetched', len(trades), 'trades from', self.instance.iso8601(since), 'till', self.instance.iso8601(end))
                since = since + week
                end = since + week
            if since > now:
                print(f'User:{self.user.name} Done')
                break
        for history in all_histories:
            income = {}
            income["symbol"] = history["info"]["symbol"]
            income["timestamp"] = history["timestamp"]
            income["side"] = history["side"]
            income["income"] = history["cost"]
            income["fee"] = history["info"]["execFee"]
            income["uniqueid"] = history["info"]["orderId"]
            all.append(income)
        return all

    def fetch_history(self, since: int = None):
        if self.user.key == 'key':
            return []
        all_histories = []
        all = []
        if not self.instance: self.connect()
        
        day = 24 * 60 * 60 * 1000
        week = 7 * day
        max_days = 2 * 365 * day - day
        now = self.instance.milliseconds()
        if not since:
            since = now - max_days
        limit = 50
        end = since + week
        if self.instance.is_unified_enabled()[1]:
            UTA = True
        else:
            UTA = False
        cursor = None
        while True:
            for i in range(5):
                try:
                    if UTA:
                        transactions = self.instance.privateGetV5AccountTransactionLog(params={"limit": limit, "startTime": since, "endTime": end, "cursor": cursor})
                    else:
                        transactions = self.instance.privateGetV5AccountContractTransactionLog(params={"limit": limit, "startTime": since, "endTime": end, "cursor": cursor})
                except Exception as e:
                    print(e)
                    print(f'User:{self.user.name} Fetching transactions failed. Retry in 5 seconds')
                    sleep(5)
                    continue
            cursor = transactions["result"]["nextPageCursor"]
            positions = transactions["result"]["list"]
            
            if positions:
                first_position = positions[0]
                last_position = positions[-1]
                all_histories = positions + all_histories
            if cursor:
                print(f'User:{self.user.name} Fetched', len(positions), 'transactions from', self.instance.iso8601(int(first_position['transactionTime'])), 'till', self.instance.iso8601(int(last_position['transactionTime'])))
            else:
                print(f'User:{self.user.name} Fetched', len(positions), 'transactions from', self.instance.iso8601(since), 'till', self.instance.iso8601(end))
                since = since + week
                end = since + week
            if since > now:
                print(f'User:{self.user.name} Done')
                break
        
        for history in all_histories:
            if history["type"] in ["TRADE","SETTLEMENT"]:
                income = {}
                income["symbol"] = history["symbol"]
                income["timestamp"] = history["transactionTime"]
                income["income"] = history["change"]
                income["uniqueid"] = history["id"]
                all.append(income)
            else: 
                self.save_income_other(history, self.user.name)
        return all

    def fetch_trades(self, symbol: str, market_type: str, since: int):
        all_trades = []
        if not self.instance: self.connect()
        
        day = 24 * 60 * 60 * 1000
        week = 7 * day
        year = 365 * day
        now = self.instance.milliseconds()
        
        if since == 1577840461000:
            since = now - 2 * year + day
            end_time = since + week
            first_trade = self.instance.fetch_my_trades(symbol, since, 100, params={'type': market_type, "paginate": True, 'endTime': end_time })
            if first_trade:
                since = first_trade[0]["timestamp"]
        
        while since < now:
            print(f'User:{self.user.name} Symbol:{symbol} Fetching trades from', self.instance.iso8601(since))
            end_time = since + week
            if end_time > now:
                end_time = now
            trades = self.instance.fetch_my_trades(symbol, since, 100, params={'type': market_type, 'endTime': end_time })
            if len(trades):
                last_trade = trades[len(trades) - 1]
                if "nextPageCursor" in last_trade["info"]:
                    cursor = last_trade["info"]["nextPageCursor"]
                    while True:
                        print(f'User:{self.user.name} Symbol:{symbol} Fetching trades from', cursor)
                        all_trades = all_trades + trades
                        trades = self.instance.fetch_my_trades(symbol, since, 100, params={'type': market_type, 'cursor': cursor, 'endTime': end_time })
                        if len(trades):
                            lpage = trades[len(trades) - 1]
                            if "nextPageCursor" in lpage["info"]:
                                cursor = lpage["info"]["nextPageCursor"]
                            else:
                                break
                        else:
                            break
                since = last_trade['timestamp'] + 1
                all_trades = all_trades + trades
            else:
                since = end_time
        
        if all_trades:
            sort_trades = sorted(all_trades, key=lambda d: d['timestamp'])
            return sort_trades
        return []

    def fetch_symbol_info(self, symbol: str, market_type: str):
        if not self.instance: self.connect()
        if not self._markets: self._markets = self.instance.load_markets()
        
        symbol_info = self._markets[symbol]
        
        if market_type == "futures":
            min_costs = (
                0.1 if symbol_info["limits"]["cost"]["min"] is None else symbol_info["limits"]["cost"]["min"]
            )
            min_qtys = symbol_info["limits"]["amount"]["min"]
            qty_steps = symbol_info["precision"]["amount"]
            price_steps = symbol_info["precision"]["price"]
            c_mults = symbol_info["contractSize"]
        else:
            min_costs = (
                0.1 if symbol_info["limits"]["cost"]["min"] is None else symbol_info["limits"]["cost"]["min"]
            )
            min_qtys = symbol_info["limits"]["amount"]["min"]
            qty_steps = symbol_info["precision"]["amount"]
            price_steps = symbol_info["precision"]["price"]
            c_mults = 1.0
            
        return symbol_info, min_costs, min_qtys, price_steps, qty_steps, c_mults

    def fetch_copytrading_symbols(self):
        cpSymbols = []
        if not self.instance: self.connect()
        symbols = self.instance.publicGetContractV3PublicCopytradingSymbolList()
        for symbol in symbols["result"]["list"]:
            cpSymbols.append(symbol["symbol"])
        cpSymbols.sort()
        return cpSymbols

    def fetch_symbols(self):
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} DEBUG: [{self.id}] Connecting to exchange...')
        if not self.instance: self.connect()
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} DEBUG: [{self.id}] Loading markets from exchange...')
        self._markets = self.instance.load_markets()
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} DEBUG: [{self.id}] Loaded {len(self._markets)} markets')
        self.swap = []
        self.spot = []
        self.cpt = []
        
        for (k,v) in list(self._markets.items()):
            if v["swap"] and v["active"] and v["linear"]:
                if v["id"].endswith('USDT'):
                    if v["info"]["copyTrading"] == "both":
                        self.cpt.append(v["id"])
                    self.swap.append(v["id"])
            if v["spot"] and v["active"]:
                self.spot.append(v["id"])
        
        self.save_symbols()
