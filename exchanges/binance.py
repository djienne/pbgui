from .base import BaseExchange
from User import Users
from datetime import datetime

class Binance(BaseExchange):
    def __init__(self, user=None):
        super().__init__("binance", user)

    def fetch_position(self, symbol: str, market_type: str):
        if not self.instance: self.connect()
        position = self.instance.fetch_account_positions(symbols=[symbol])
        return position[0]

    def fetch_balance(self, market_type: str, symbol: str = None):
        if not self.instance: self.connect()
        try:
            balance = self.instance.fetch_balance(params={"type": market_type})
        except Exception as e:
            return e
        
        if market_type == 'swap':
            return float(balance["info"]["totalWalletBalance"])
        else:
            if symbol:
                return float(balance["total"][symbol])
            else:
                return float(balance["total"]["USDT"])

    def fetch_history(self, since: int = None):
        if self.user.key == 'key':
            return []
        all_histories = []
        all = []
        if not self.instance: self.connect()
        
        day = 24 * 60 * 60 * 1000
        week = 7 * day
        max_days = 124 * day
        now = self.instance.milliseconds()
        if not since:
            since = now - max_days
        limit = 1000
        end = since + week
        
        while True:
            imcomes = self.instance.fapiPrivateGetIncome({                        
                                                    "pageSize": "100",
                                                    "startTime": since,
                                                    "limit": limit,
                                                    "endTime": end,
                                                    "timestamp": self.instance.milliseconds()
                                                    })
            if imcomes:
                first_imcome = imcomes[0]
                last_imcome = imcomes[-1]
                all_histories = imcomes + all_histories
            if len(imcomes) == limit:
                print(f'User:{self.user.name} Fetched', len(imcomes), 'incomes from', self.instance.iso8601(int(first_imcome['time'])), 'till', self.instance.iso8601(int(last_imcome['time'])))
                since = int(imcomes[-1]['time'])
            else:
                print(f'User:{self.user.name} Fetched', len(imcomes), 'incomes from', self.instance.iso8601(since), 'till', self.instance.iso8601(end))
                since = end
                end = since + week
            if since > now:
                print(f'User:{self.user.name} Done')
                break
        
        for history in all_histories:
            if history["incomeType"] in ["REALIZED_PNL", "COMMISSION", "FUNDING_FEE"]:
                income = {}
                income["symbol"] = history["symbol"]
                income["timestamp"] = history["time"]
                income["income"] = history["income"]
                if history["incomeType"] == "REALIZED_PNL":
                    income["uniqueid"] = history["tradeId"]
                else:
                    income["uniqueid"] = history["tranId"]
                all.append(income)
            else: 
                self.save_income_other(history, self.user.name)
        return all

    def fetch_trades(self, symbol: str, market_type: str, since: int):
        all_trades = []
        if not self.instance: self.connect()
        
        if market_type == "futures":
            week = 7 * 24 * 60 * 60 * 1000
        else:
            week = 24 * 60 * 60 * 1000
        now = self.instance.milliseconds()
        
        if since == 1577840461000:
            first_trade = self.instance.fetch_my_trades(symbol, None, None, {'fromId': 0})
            if first_trade:
                since = first_trade[0]["timestamp"]
        
        while since < now:
            print(f'User:{self.user.name} Symbol:{symbol} Fetching trades from', self.instance.iso8601(since))
            end_time = since + week
            if end_time > now:
                end_time = now
            trades = self.instance.fetch_my_trades(symbol, since, None, {
                'endTime': end_time,
            })
            if len(trades):
                last_trade = trades[len(trades) - 1]
                since = last_trade['timestamp'] + 1
                all_trades = all_trades + trades
            else:
                since = end_time
        
        if all_trades:
            sort_trades = sorted(all_trades, key=lambda d: d['timestamp'])
            return sort_trades
        return []

    def symbol_to_exchange_symbol(self, symbol: str, market_type: str):
        if not self.instance: self.connect()
        if not self._markets: self._markets = self.instance.load_markets()
        for (k,v) in list(self._markets.items()):
            if market_type == "spot":
                if v["id"] == symbol and v["spot"]:
                    return v["symbol"]
            if market_type == "swap":
                if v["id"] == symbol and v["swap"]:
                    return v["symbol"]
        return symbol

    def fetch_symbol_info(self, symbol: str, market_type: str):
        if not self.instance: self.connect()
        if not self._markets: self._markets = self.instance.load_markets()
        
        # Binance specific symbol formatting for lookup
        if market_type == "spot":
            symbol = f'{symbol[0:-4]}/USDT'
        else:
            if symbol[-4:] == 'USDC':
                symbol = f'{symbol[0:-4]}/USDC:USDC'
            else:
                symbol = f'{symbol[0:-4]}/USDT:USDT'
                
        symbol_info = self._markets[symbol]
        
        if market_type == "futures":
            min_costs = (
                0.1 if symbol_info["limits"]["cost"]["min"] is None else symbol_info["limits"]["cost"]["min"]
            )
            min_qtys = symbol_info["limits"]["amount"]["min"]
            for felm in symbol_info["info"]["filters"]:
                if felm["filterType"] == "PRICE_FILTER":
                    price_steps = float(felm["tickSize"])
                elif felm["filterType"] == "MARKET_LOT_SIZE":
                    qty_steps = float(felm["stepSize"])
            c_mults = symbol_info["contractSize"]
        else:
            for q in symbol_info["info"]["filters"]:
                if q["filterType"] == "LOT_SIZE":
                    min_qtys = symbol_info["min_qty"] = float(q["minQty"])
                    qty_steps = symbol_info["qty_step"] = float(q["stepSize"])
                elif q["filterType"] == "PRICE_FILTER":
                    price_steps = symbol_info["price_step"] = float(q["tickSize"])
                elif q["filterType"] == "NOTIONAL":
                    min_costs = symbol_info["min_cost"] = float(q["minNotional"])
            c_mults = 1.0
            
        return symbol_info, min_costs, min_qtys, price_steps, qty_steps, c_mults

    def fetch_copytrading_symbols(self):
        cpSymbols = []
        users = Users()
        self.user = users.find_binance_user()
        if self.user:
            self.connect()
            try:
                symbols = self.instance.sapiGetCopytradingFuturesLeadsymbol()
            except Exception as e:
                print(f'User:{self.user.name} Error:', e)
                return []
            for symbol in symbols["data"]:
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
                # Only include USDT-margined futures (linear perpetuals)
                # USDC pairs are spot markets and excluded by swap filter
                if v["id"].endswith('USDT'):
                    self.swap.append(v["id"])
            if v["spot"] and v["active"]:
                self.spot.append(v["id"])

        try:
            cpt_result = self.fetch_copytrading_symbols()
            if cpt_result:
                self.cpt = cpt_result
        except Exception as e:
            print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Warning: Could not fetch copytrading symbols for {self.id}: {type(e).__name__}: {str(e)}')

        self.save_symbols()
