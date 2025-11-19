class ApprovedCoins:
    def __init__(self):
        self._long = []
        self._short = []
        self._approved_coins = {
            "long": self._long,
            "short": self._short
        }

    def __repr__(self):
        return str(self._approved_coins)
    
    @property
    def approved_coins(self): return self._approved_coins
    @approved_coins.setter
    def approved_coins(self, new_approved_coins):
        if "long" in new_approved_coins:
            self.long = new_approved_coins["long"]
        else:
            self.long = new_approved_coins
        if "short" in new_approved_coins:
            self.short = new_approved_coins["short"]
        else:
            self.short = new_approved_coins
    
    @property
    def long(self): return self._long
    @property
    def short(self): return self._short
    @long.setter
    def long(self, new_long):
        # Add 'USDT' to each coin if it does not already end with 'USDT'
        updated_long = [
            coin if coin.endswith("USDT") or coin.endswith("USDC") else coin + "USDT"
            for coin in new_long
        ]
        self._long = updated_long
        self._approved_coins["long"] = self._long
    @short.setter
    def short(self, new_short):
        # Add 'USDT' to each coin if it does not already end with 'USDT'
        updated_short = [
            coin if coin.endswith("USDT") or coin.endswith("USDC") else coin + "USDT"
            for coin in new_short
        ]
        self._short = updated_short
        self._approved_coins["short"] = self._short

class IgnoredCoins:
    def __init__(self):
        self._long = []
        self._short = []
        self._ignored_coins = {
            "long": self._long,
            "short": self._short
        }
    
    def __repr__(self):
        return str(self._ignored_coins)

    @property
    def ignored_coins(self): return self._ignored_coins
    @ignored_coins.setter
    def ignored_coins(self, new_ignored_coins):
        if "long" in new_ignored_coins:
            self.long = new_ignored_coins["long"]
        else:
            self.long = new_ignored_coins
        if "short" in new_ignored_coins:
            self.short = new_ignored_coins["short"]
        else:
            self.short = new_ignored_coins
    
    @property
    def long(self): return self._long
    @property
    def short(self): return self._short
    @long.setter
    def long(self, new_long):
        self._long = new_long
        self._ignored_coins["long"] = self._long
    @short.setter
    def short(self, new_short):
        self._short = new_short
        self._ignored_coins["short"] = self._short
