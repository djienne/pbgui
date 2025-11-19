from enum import Enum

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
