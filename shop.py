# shop.py
# Extended Shop system with currencies and exchange rates

import random
from typing import List, Dict
from items import item_registry, Item
from character import Character
from currency import currency_manager, Currency

class ShopItem:
    def __init__(self, item_id: str, price: float, quantity: int, currency: str):
        self.item_id = item_id
        self.price = price
        self.quantity = quantity  # The number of items available in the shop
        self.currency = currency  # Currency used for the item price

    def purchase(self, character: Character):
        """Allow character to purchase the item if they have enough gold."""
        currency = currency_manager.get_currency(self.currency)
        if character.get_balance(currency) >= self.price:
            character.deduct_currency(self.currency, self.price)
            character.add_to_inventory(self.item_id)
            self.quantity -= 1
            print(f"Purchased {item_registry.get_item(self.item_id).name} for {self.price} {currency.symbol}.")
        else:
            print(f"Not enough {currency.symbol} to purchase this item.")

class Shop:
    def __init__(self, name: str, stock: List[ShopItem], currency: str):
        self.name = name
        self.stock = stock
        self.currency = currency

    def show_stock(self):
        """Show the available stock of the shop."""
        currency = currency_manager.get_currency(self.currency)
        print(f"{self.name}'s Shop")
        print(f"Currency: {currency.symbol}")
        print("--------------------")
        for item in self.stock:
            item_data = item_registry.get_item(item.item_id)
            print(f"{item_data.name} - {item.price} {currency.symbol} (x{item.quantity})")

    def purchase_item(self, character: Character, item_id: str):
        """Purchase an item by item_id."""
        item = next((item for item in self.stock if item.item_id == item_id), None)
        if item:
            item.purchase(character)
        else:
            print("Item not found in stock.")

    def restock(self):
        """Restock shop with random items."""
        for item in self.stock:
            item.quantity = random.randint(1, 5)  # Randomize stock quantity between 1-5

# Example of available items in the game
health_potion = Item(item_id="potion_health", name="Health Potion", description="Restores 50 HP.", effect="heal", value=50)
mana_potion = Item(item_id="potion_mana", name="Mana Potion", description="Restores 30 MP.", effect="mana", value=30)
iron_sword = Item(item_id="sword_iron", name="Iron Sword", description="A basic sword for beginners.", effect="atk", value=10)

item_registry.register_item(health_potion)
item_registry.register_item(mana_potion)
item_registry.register_item(iron_sword)

# Create the shop with initial stock and currency set to "Gold"
shop_items = [
    ShopItem(item_id="potion_health", price=50, quantity=3, currency="Gold"),
    ShopItem(item_id="potion_mana", price=40, quantity=5, currency="Silver"),
    ShopItem(item_id="sword_iron", price=150, quantity=2, currency="Gold")
]

shop = Shop(name="Village Shop", stock=shop_items, currency="Gold")

# Debug Example
if __name__ == "__main__":
    from character import Player

    # Create a player character with initial gold and silver
    player = Player(name="Kai")
    player.set_currency_balance("Gold", 200)  # Starting gold
    player.set_currency_balance("Silver", 100)  # Starting silver

    # Show stock and try to purchase items
    shop.show_stock()
    shop.purchase_item(player, "potion_health")
    shop.purchase_item(player, "sword_iron")

    # Show updated stock and player's inventory
    shop.show_stock()
    player.show_inventory()
    player.show_balances()
