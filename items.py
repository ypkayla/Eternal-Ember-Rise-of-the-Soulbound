# items.py
# Core item system for the Anime RPG Game

import json
import random
from typing import Callable, Optional, List, Dict

# Item Effect class
class ItemEffect:
    def __init__(self, effect_func: Callable, description: str):
        self.effect_func = effect_func  # Function that applies the effect
        self.description = description

    def apply(self, target):
        self.effect_func(target)

# Base Item class
class Item:
    def __init__(
        self,
        item_id: str,
        name: str,
        description: str,
        item_type: str,
        rarity: str,
        usable_in_battle: bool,
        usable_outside_battle: bool,
        effect: Optional[ItemEffect] = None,
        value: int = 0,
        max_stack: int = 99,
        is_key_item: bool = False,
    ):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.item_type = item_type  # e.g., consumable, equipment, key
        self.rarity = rarity  # Common, Rare, Epic, Legendary
        self.usable_in_battle = usable_in_battle
        self.usable_outside_battle = usable_outside_battle
        self.effect = effect
        self.value = value
        self.max_stack = max_stack
        self.is_key_item = is_key_item

    def use(self, target):
        if self.effect:
            print(f"Using {self.name} on {target.name}...")
            self.effect.apply(target)
        else:
            print(f"{self.name} has no effect.")

# Equipment class inheriting from Item
class Equipment(Item):
    def __init__(
        self,
        item_id: str,
        name: str,
        description: str,
        equipment_type: str,
        stats_boost: Dict[str, int],
        rarity: str,
        value: int,
    ):
        super().__init__(
            item_id=item_id,
            name=name,
            description=description,
            item_type="equipment",
            rarity=rarity,
            usable_in_battle=False,
            usable_outside_battle=False,
            effect=None,
            value=value,
            max_stack=1,
        )
        self.equipment_type = equipment_type  # e.g., weapon, armor
        self.stats_boost = stats_boost  # e.g., {"atk": 5, "def": 2}

# Item Registry to manage items
class ItemRegistry:
    def __init__(self):
        self.items: Dict[str, Item] = {}

    def register_item(self, item: Item):
        self.items[item.item_id] = item

    def get_item(self, item_id: str) -> Optional[Item]:
        return self.items.get(item_id)

    def get_all_items(self) -> List[Item]:
        return list(self.items.values())

    def load_from_json(self, json_data):
        for item_dict in json_data:
            self.register_item(Item(**item_dict))

# Register the global item registry
item_registry = ItemRegistry()

# Example effects
def heal_50_hp(target):
    if hasattr(target, "heal"):
        target.heal(50)
        print(f"{target.name} healed for 50 HP!")

def buff_attack(target):
    if hasattr(target, "buff_stat"):
        target.buff_stat("atk", 10, 3)
        print(f"{target.name}'s attack increased by 10 for 3 turns!")

# Register some example items
potion = Item(
    item_id="potion_hp50",
    name="Healing Potion",
    description="Restores 50 HP.",
    item_type="consumable",
    rarity="Common",
    usable_in_battle=True,
    usable_outside_battle=True,
    effect=ItemEffect(heal_50_hp, "Restore 50 HP"),
    value=50,
)

atk_buff = Item(
    item_id="buff_atk10",
    name="Attack Tonic",
    description="Boosts attack power by 10 for 3 turns.",
    item_type="consumable",
    rarity="Rare",
    usable_in_battle=True,
    usable_outside_battle=False,
    effect=ItemEffect(buff_attack, "Boost attack +10 (3 turns)"),
    value=150,
)

sword = Equipment(
    item_id="iron_sword",
    name="Iron Sword",
    description="A basic iron sword.",
    equipment_type="weapon",
    stats_boost={"atk": 5},
    rarity="Common",
    value=200,
)

armor = Equipment(
    item_id="leather_armor",
    name="Leather Armor",
    description="Basic leather armor.",
    equipment_type="armor",
    stats_boost={"def": 3},
    rarity="Common",
    value=150,
)

# Register all items
def register_all_items():
    item_registry.register_item(potion)
    item_registry.register_item(atk_buff)
    item_registry.register_item(sword)
    item_registry.register_item(armor)

# Item Drop System
def get_random_loot(rarity: str) -> Optional[Item]:
    eligible = [item for item in item_registry.get_all_items() if item.rarity == rarity]
    if not eligible:
        return None
    return random.choice(eligible)

# Crafting System
class CraftingRecipe:
    def __init__(self, output_item_id: str, required_items: Dict[str, int]):
        self.output_item_id = output_item_id
        self.required_items = required_items  # item_id: amount

    def can_craft(self, inventory: Dict[str, int]) -> bool:
        for item_id, amount in self.required_items.items():
            if inventory.get(item_id, 0) < amount:
                return False
        return True

    def craft(self, inventory: Dict[str, int]) -> Optional[Item]:
        if not self.can_craft(inventory):
            print("Not enough materials.")
            return None
        for item_id, amount in self.required_items.items():
            inventory[item_id] -= amount
        item = item_registry.get_item(self.output_item_id)
        if item:
            print(f"Crafted {item.name}!")
        return item

# Example recipe
iron_blade_recipe = CraftingRecipe(
    output_item_id="iron_sword",
    required_items={"iron_shard": 3, "wood": 1}
)

# Save/Load Item Inventory
class InventoryManager:
    def __init__(self):
        self.inventory: Dict[str, int] = {}

    def add_item(self, item_id: str, quantity: int = 1):
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

    def remove_item(self, item_id: str, quantity: int = 1):
        if item_id in self.inventory:
            self.inventory[item_id] -= quantity
            if self.inventory[item_id] <= 0:
                del self.inventory[item_id]

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        return self.inventory.get(item_id, 0) >= quantity

    def get_all_items(self) -> Dict[str, int]:
        return self.inventory

    def save_inventory(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(self.inventory, f)

    def load_inventory(self, filepath: str):
        try:
            with open(filepath, 'r') as f:
                self.inventory = json.load(f)
        except FileNotFoundError:
            print("Inventory file not found. Starting fresh.")

# Sample usage
if __name__ == "__main__":
    register_all_items()
    inv = InventoryManager()
    inv.add_item("potion_hp50", 5)
    inv.add_item("iron_shard", 3)
    inv.add_item("wood", 1)

    print("Current Inventory:", inv.get_all_items())

    # Try crafting
    crafted_item = iron_blade_recipe.craft(inv.inventory)
    if crafted_item:
        inv.add_item(crafted_item.item_id)

    print("Updated Inventory:", inv.get_all_items())
