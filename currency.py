# currency.py
# Currency and exchange system for the Anime RPG

import random
from typing import Dict, List, Callable

class Currency:
    """Represents a currency in the game world."""
    def __init__(self, name: str, symbol: str, exchange_rate: float):
        self.name = name
        self.symbol = symbol
        self.exchange_rate = exchange_rate  # Rate relative to the base currency (e.g., Gold)

    def convert_to(self, amount: float, target_currency: 'Currency') -> float:
        """Convert an amount of this currency to another."""
        converted = amount * self.exchange_rate / target_currency.exchange_rate
        return round(converted, 2)

    def __repr__(self):
        return f"{self.name} ({self.symbol})"

class CurrencyManager:
    """Manages all currencies in the game world."""
    def __init__(self):
        self.currencies: Dict[str, Currency] = {}

    def add_currency(self, currency: Currency):
        """Add a new currency to the system."""
        self.currencies[currency.name] = currency

    def get_currency(self, name: str) -> Currency:
        """Get a currency by its name."""
        return self.currencies.get(name)

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """Get the exchange rate between two currencies."""
        from_cur = self.get_currency(from_currency)
        to_cur = self.get_currency(to_currency)
        if from_cur and to_cur:
            return from_cur.exchange_rate / to_cur.exchange_rate
        return 1.0

currency_manager = CurrencyManager()

# Base currency is Gold (standard currency)
gold = Currency(name="Gold", symbol="G", exchange_rate=1.0)
currency_manager.add_currency(gold)

# Other currencies specific to different regions
silver = Currency(name="Silver", symbol="S", exchange_rate=0.5)  # 1 Gold = 2 Silver
currency_manager.add_currency(silver)

platinum = Currency(name="Platinum", symbol="P", exchange_rate=2.0)  # 1 Gold = 0.5 Platinum
currency_manager.add_currency(platinum)

# Debug Example
if __name__ == "__main__":
    # Example of currency conversion
    amount_in_gold = 100
    amount_in_silver = currency_manager.get_currency("Gold").convert_to(amount_in_gold, currency_manager.get_currency("Silver"))
    amount_in_platinum = currency_manager.get_currency("Gold").convert_to(amount_in_gold, currency_manager.get_currency("Platinum"))

    print(f"{amount_in_gold} Gold = {amount_in_silver} Silver")
    print(f"{amount_in_gold} Gold = {amount_in_platinum} Platinum")
