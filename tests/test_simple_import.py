from Exchange import Exchange, Exchanges


def test_exchange_module_imports():
    assert "binance" in Exchanges.list()
    assert "hyperliquid" in Exchanges.list()


def test_exchange_factory_creates_binance_instance():
    exchange = Exchange("binance", None)

    assert type(exchange).__name__ == "Binance"
    assert exchange.name == "binance"
