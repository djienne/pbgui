#!/usr/bin/env python
"""
Simple import test for the refactored Exchange module.
Run this from the pbgui directory to test imports.
"""

# When running as a script from the pbgui directory, Python automatically
# adds the current directory to sys.path, allowing imports to work
from Exchange import Exchange, Exchanges

print("✓ Successfully imported Exchange and Exchanges")
print(f"✓ Available exchanges: {', '.join(Exchanges.list())}")

# Test creating an instance
try:
    exchange = Exchange('binance', None)
    print(f"✓ Created {type(exchange).__name__} instance for 'binance'")
    print("\nAll imports working correctly!")
except Exception as e:
    print(f"✗ Error creating exchange: {e}")
