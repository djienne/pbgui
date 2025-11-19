import streamlit as st
import json
import math
from time import sleep
from .configs.v7.config import ConfigV7

try:
    from .Exchange import Exchange, V7
except ImportError:
    from Exchange import Exchange, V7

try:
    from .PBCoinData import CoinData
except ImportError:
    from PBCoinData import CoinData

try:
    from .pbgui_func import error_popup
except ImportError:
    from pbgui_func import error_popup

class BalanceCalculator:
    def __init__(self, config_file: str = None):
        self.config = ConfigV7()
        if config_file:
            self.config.config_file = config_file
            self.config.load_config()
        self.exchange = Exchange("binance", None)
        self.coin_infos = []
        self.balance_long = []
        self.balance_short = []
    
    @property
    def balance(self):
        return self.balance_long + self.balance_short

    def init_coindata(self):
        if "pbcoindata" not in st.session_state:
            st.session_state.pbcoindata = CoinData()
        pbcoindata = st.session_state.pbcoindata
        pbcoindata.exchange = self.exchange.id
        # Refresh the cached CoinData selection so approved/ignored lists are up to date
        pbcoindata.list_symbols()
        if self.config.pbgui.dynamic_ignore:
            pbcoindata.tags = self.config.pbgui.tags
            pbcoindata.only_cpt = self.config.pbgui.only_cpt
            pbcoindata.market_cap = self.config.pbgui.market_cap
            pbcoindata.vol_mcap = self.config.pbgui.vol_mcap
            pbcoindata.notices_ignore = self.config.pbgui.notices_ignore
            self.config.live.approved_coins = pbcoindata.approved_coins
        elif not (self.config.live.approved_coins.long or self.config.live.approved_coins.short):
            # Fall back to CoinData's current approval list if the config has none
            self.config.live.approved_coins = pbcoindata.approved_coins

    def view(self):
        # Init coindata
        self.init_coindata()
        if "edit_bc_config" in st.session_state:
            if st.session_state.edit_bc_config != json.dumps(self.config.config, indent=4):
                try:
                    self.config.config = json.loads(st.session_state.edit_bc_config)
                    self.init_coindata()
                except:
                    error_popup("Invalid JSON")
                    st.session_state.edit_bc_config = json.dumps(self.config.config, indent=4)
        else:
            st.session_state.edit_bc_config = json.dumps(self.config.config, indent=4)

        if "bc_exchange_id" in st.session_state:
            if st.session_state.bc_exchange_id != self.exchange.id:
                self.exchange = Exchange(st.session_state.bc_exchange_id, None)
        else:
            if self.config.backtest.exchanges:
                st.session_state.bc_exchange_id = self.config.backtest.exchanges[0]
        col1, col2 = st.columns([1, 1])
        with col1:
            st.text_area(f'config', key="edit_bc_config", height=500)
        with col2:
            st.markdown("### Balance Calculator")
            st.markdown("This tool allows you to calculate the balance for a given configuration.")
            st.markdown("You can edit the configuration in the left text area and click on 'Calculate' to see the results.")
            st.selectbox("Exchange", V7.list(), key="bc_exchange_id")
            if st.button("Calculate"):
                coins = set(self.config.live.approved_coins.long + self.config.live.approved_coins.short)
                if not coins:
                    st.info("No approved coins available. Paste a config or configure Coin Data to populate the list.")
                    return
                self.coin_infos = []
                self.balance_long = []
                self.balance_short = []
                with st.spinner(text=f'fetching coin infos from exchange...'):
                    with st.empty():
                        for counter, coin in enumerate(coins):
                            st.text(f'{counter + 1}/{len(coins)}: {coin}')
                            min_order_price, price, contractSize, min_amount, min_cost, lev = self.exchange.fetch_symbol_infos(coin)
                            self.coin_infos.append({
                                "coin": coin,
                                "currentPrice": price,
                                "contractSize": contractSize,
                                "min_amount": min_amount,
                                "min_cost": min_cost,
                                "min_order_price": min_order_price,
                                "max lev": lev
                            })
                            if coin in self.config.live.approved_coins.long:
                                if self.config.bot.long.n_positions > 0 and self.config.bot.long.total_wallet_exposure_limit > 0:
                                    we = self.config.bot.long.total_wallet_exposure_limit / self.config.bot.long.n_positions
                                    balance = min_order_price / (we * self.config.bot.long.entry_initial_qty_pct)
                                    self.balance_long.append({
                                        "coin": coin,
                                        "balance": balance
                                    })
                            if coin in self.config.live.approved_coins.short:
                                if self.config.bot.short.n_positions > 0 and self.config.bot.short.total_wallet_exposure_limit > 0:
                                    we = self.config.bot.short.total_wallet_exposure_limit / self.config.bot.short.n_positions
                                    balance = min_order_price / (we * self.config.bot.short.entry_initial_qty_pct)
                                    self.balance_short.append({
                                        "coin": coin,
                                        "balance": balance
                                    })
                            sleep(0.1)  # to avoid rate limit issues

        # sort coin_infos by min_order_price
        self.coin_infos = sorted(self.coin_infos, key=lambda x: x['min_order_price'], reverse=True)
        if self.coin_infos:
            st.write("### Coin Information")
            st.dataframe(self.coin_infos, hide_index=True)

        # find highest balance in short and long
        self.balance_long = sorted(self.balance_long, key=lambda x: x['balance'], reverse=True)
        self.balance_short = sorted(self.balance_short, key=lambda x: x['balance'], reverse=True)
        side = None
        if self.balance_long:
            if self.balance_short:
                if self.balance_long[0]['balance'] > self.balance_short[0]['balance']:
                    side = "long"
                else:
                    side = "short"
            else:
                side = "long"
        else:
            if self.balance_short:
                side = "short"
        if side in ["long", "short"]:
            # Select the correct attributes based on side
            balance_list = self.balance_long if side == "long" else self.balance_short
            bot_side = self.config.bot.long if side == "long" else self.config.bot.short
            # Get symbol name with highest balance
            symbol = balance_list[0]['coin']
            # get min order price for symbol from coin_infos
            min_order_price = next((coin['min_order_price'] for coin in self.coin_infos if coin['coin'] == symbol), 0)
            # Display calculated balance with formula
            st.write(f"### Balance needed for {symbol} ({side.capitalize()} Side)")
            st.write(f"**Minimum Order Price:** `{min_order_price:.2f}`")
            st.write(f"**Total Wallet Exposure Limit:** `{bot_side.total_wallet_exposure_limit:.2f}`")
            st.write(f"**Number of Positions:** `{bot_side.n_positions}`")
            st.write(f"**Entry Initial Quantity Percentage:** `{bot_side.entry_initial_qty_pct:.2f}`")
            st.write(f"To calculate the balance needed for {symbol} on the {side} side, use the formula:")
            st.write(f"**Formula:** `min_order_price / ((total_wallet_exposure_limit / n_positions) * entry_initial_qty_pct)`")
            result = min_order_price / ((bot_side.total_wallet_exposure_limit / bot_side.n_positions) * bot_side.entry_initial_qty_pct)
            st.write(f"**Calculation:** `{min_order_price} / (({bot_side.total_wallet_exposure_limit} / {bot_side.n_positions}) * {bot_side.entry_initial_qty_pct}) = {result:.2f}`")
            recommended_balance = math.ceil(result * 1.1 / 10) * 10
            st.write(f"### Recommended Balance (10% more): :green[{int(recommended_balance)} USDT]")
