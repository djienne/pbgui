"""
Exchange.py - Factory for creating exchange-specific instances

This module provides backward compatibility with the original Exchange class
while delegating to specialized exchange implementations in the exchanges/ package.
"""

from exchanges import (
    BaseExchange, Exchanges, Spot, Single, V7, Passphrase,
    Binance, Bybit, Bitget, Hyperliquid, OKX, Kucoin, Gateio, BingX
)
from User import User

# Re-export enums and helper functions for backward compatibility
__all__ = ['Exchange', 'Exchanges', 'Spot', 'Single', 'V7', 'Passphrase']


class Exchange:
    """
    Factory class for creating exchange instances.
    
    This class uses __new__ to return the appropriate exchange-specific subclass
    based on the exchange ID, maintaining backward compatibility with the original
    Exchange class API.
    """
    
    _exchange_map = {
        'binance': Binance,
        'bybit': Bybit,
        'bitget': Bitget,
        'hyperliquid': Hyperliquid,
        'okx': OKX,
        'kucoin': Kucoin,
        'gateio': Gateio,
        'bingx': BingX,
    }
    
    def __new__(cls, id: str, user: User = None):
        """
        Create and return an exchange-specific instance.
        
        Args:
            id: Exchange identifier (e.g., 'binance', 'bybit')
            user: User object containing API credentials
            
        Returns:
            An instance of the appropriate exchange subclass
            
        Raises:
            ValueError: If the exchange ID is not supported
        """
        exchange_class = cls._exchange_map.get(id.lower())
        
        if exchange_class is None:
            raise ValueError(
                f"Unsupported exchange: {id}. "
                f"Supported exchanges: {', '.join(cls._exchange_map.keys())}"
            )
        
        return exchange_class(user)


def main():
    print("Don't Run this Class from CLI")

if __name__ == '__main__':
    main()
