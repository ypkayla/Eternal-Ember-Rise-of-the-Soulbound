# villagers.py
# Enhanced Villager system with more interactivity for Anime RPG

from typing import List, Dict, Optional
from quests import QuestDatabase, Quest
from character import Character
from world import Village
from random import choice, randint
import time

class Villager:
    def __init__(self, name: str, role: str, dialogue: List[str], quest_id: Optional[str] = None,
                 items_for_sale: Optional[List[str]] = None, event_trigger: Optional[str] = None):
        """
        Represents a villager NPC in the village.
        """
        self.name = name
        self.role = role  # Role of the villager (e.g., blacksmith, healer, merchant)
        self.dialogue = dialogue  # List of dialogue lines
        self.quest_id = quest_id  # Optional quest associated with the villager (if any)
        self.items_for_sale = items_for_sale or []  # Items the villager might sell
        self.event_trigger = event_trigger  # Optional event that triggers a special interaction (e.g., a special sale)
        self.last_interacted = None  # Track the last time the player interacted

    def interact(self, player: Character):
        """Interact with the villager. Display random dialogue and potential quests."""
        print(f"\nTalking to {self.name} the {self.role}:")
        current_time = time.localtime()
        current_hour = current_time.tm_hour

        # Time-dependent dialogue (e.g., morning, afternoon, night)
        if 6 <= current_hour < 12:
            print(choice(self.dialogue) + " Good morning!")
        elif 12 <= current_hour < 18:
            print(choice(self.dialogue) + " Good afternoon!")
        else:
            print(choice(self.dialogue) + " Good evening!")

        # Event-triggered interaction (special offer or event)
        if self.event_trigger:
            if randint(1, 10) > 8:  # Random chance for event trigger
                print(f"**{self.name} has a special offer today!**")
                self.trigger_event(player)

        if self.quest_id:
            self.give_quest(player)

    def give_quest(self, player: Character):
        """Give the player a quest associated with this villager."""
        if self.quest_id:
            quest = quest_db.get_quest(self.quest_id)
            if quest and not quest.is_completed:
                print(f"{self.name} has given you the quest '{quest.title}'!")
                quest.display_quest_info()
                player.add_quest(quest)
            else:
                print(f"{self.name} has no active quests for you right now.")
        else:
            print(f"{self.name} has no quest for you right now.")

    def trade(self, player: Character):
        """Allow the player to trade items with the villager."""
        if self.items_for_sale:
            print(f"{self.name} is offering the following items for sale:")
            for item in self.items_for_sale:
                print(f"- {item}")
            # Offer a trade interaction (just a simple example)
            item_to_buy = input(f"Would you like to buy an item from {self.name}? Enter item name or 'exit' to cancel: ")
            if item_to_buy in self.items_for_sale:
                print(f"You bought {item_to_buy} from {self.name}.")
                player.add_item_to_inventory(item_to_buy)
            else:
                print(f"Item not available. Try again later or choose 'exit'.")
        else:
            print(f"{self.name} has no items for sale at the moment.")

    def trigger_event(self, player: Character):
        """Trigger special events based on the villager's state or time."""
        if self.event_trigger == "special_sale":
            print(f"{self.name} is holding a special sale! All items are discounted.")
            self.trade(player)
        elif self.event_trigger == "hidden_secret":
            print(f"{self.name} whispers: 'I have a hidden secret for you... investigate the old tree in the forest.'")
        else:
            print(f"{self.name} seems to be quiet today.")

    def update_last_interacted(self):
        """Updates the last interaction time."""
        self.last_interacted = time.time()

class VillagerManager:
    def __init__(self):
        self.villagers: Dict[str, Villager] = {}

    def add_villager(self, villager: Villager):
        """Add a villager to the system."""
        self.villagers[villager.name] = villager

    def get_villager(self, name: str) -> Optional[Villager]:
        """Get a villager by name."""
        return self.villagers.get(name)

    def interact_with_villager(self, player: Character, villager_name: str):
        """Let the player interact with a villager."""
        villager = self.get_villager(villager_name)
        if villager:
            villager.interact(player)
            villager.update_last_interacted()
            # Optionally, allow the player to trade
            if villager.role == "Merchant":
                villager.trade(player)
        else:
            print(f"{villager_name} is not a valid villager.")

# Sample villagers with advanced interactions
def create_sample_villagers():
    villager1 = Villager(
        name="Kaen",
        role="Blacksmith",
        dialogue=["Need some new armor?", "I can make you the best sword in the land!"],
        quest_id="quest_1",
        event_trigger="special_sale"
    )
    villager2 = Villager(
        name="Lira",
        role="Healer",
        dialogue=["Come to me if you're injured, I have potions.", "I can heal your wounds for a small fee."]
    )
    villager3 = Villager(
        name="Zara",
        role="Merchant",
        dialogue=["Looking for something special? I've got items for sale!", "Come see my latest goods!"],
        items_for_sale=["Potion", "Rare Gem", "Magic Scroll"],
        event_trigger="hidden_secret"
    )
    
    villager_manager.add_villager(villager1)
    villager_manager.add_villager(villager2)
    villager_manager.add_villager(villager3)

# Debug Example
if __name__ == "__main__":
    from character import Player
    player = Player("Kai")
    
    # Setup villagers
    villager_manager = VillagerManager()
    create_sample_villagers()

    # Interactions
    print("\nWelcome to the villager interaction system!\n")
    villager_manager.interact_with_villager(player, "Kaen")
    villager_manager.interact_with_villager(player, "Zara")
    villager_manager.interact_with_villager(player, "Lira")
