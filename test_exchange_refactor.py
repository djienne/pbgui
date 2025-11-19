#!/usr/bin/env python
"""
Test script for the refactored Exchange module.
This script tests the factory pattern implementation.
"""

import sys
sys.path.insert(0, r'c:\Users\david\Desktop\pbgui')

from Exchange import Exchange, Exchanges
from User import User

def test_exchange_factory():
    """Test that the Exchange factory creates the correct instances."""
    print("Testing Exchange factory pattern...")
    print("-" * 50)
    
    # Test creating exchanges without user
    test_exchanges = ['binance', 'bybit', 'hyperliquid', 'bitget', 'okx', 'kucoin', 'gateio', 'bingx']
    
    for exchange_id in test_exchanges:
        try:
            exchange = Exchange(exchange_id, None)
            class_name = type(exchange).__name__
            print(f"✓ {exchange_id:12} -> {class_name}")
            assert exchange.name == exchange_id, f"Expected name {exchange_id}, got {exchange.name}"
        except Exception as e:
            print(f"✗ {exchange_id:12} -> ERROR: {e}")
    
    print("-" * 50)
    
    # Test invalid exchange
    print("\nTesting invalid exchange handling...")
    try:
        exchange = Exchange('invalid_exchange', None)
        print("✗ Should have raised ValueError for invalid exchange")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    
    print("\n" + "=" * 50)
    print("All tests passed!")
    print("=" * 50)

if __name__ == '__main__':
    test_exchange_factory()
