# villages.py
# Village and NPC interaction system for Anime RPG

from typing import *
from quests import *
from character import *
from currency import *
from world import *
from random import *



class Villager:
    def __init__(self, name: str, role: str, dialogue: List[str], quest_id: Optional[str] = None):
        """
        Represents a villager NPC in the village.
        """
        self.name = name
        self.role = role  # Role of the villager (e.g., blacksmith, healer, merchant)
        self.dialogue = dialogue  # List of dialogue lines
        self.quest_id = quest_id  # Optional quest associated with the villager (if any)

    def interact(self):
        """Interact with the villager. Display random dialogue."""
        print(f"Talking to {self.name} the {self.role}:")
        print(choice(self.dialogue))
        if self.quest_id:
            print(f"{self.name} offers you a quest!")
            quest = quest_db.get_quest(self.quest_id)
            if quest and not quest.is_completed:
                quest.display_quest_info()
            else:
                print(f"Quest {self.quest_id} already completed or unavailable.")

class Village:
    def __init__(self, name: str, region: str, population: int, currency: str, villagers: List[Villager], quests: List[str]):
        """
        Represents a village within a region in the game.
        """
        self.name = name
        self.region = region  # Region where the village is located
        self.population = population
        self.currency = currency  # Currency used in the village
        self.villagers = villagers  # List of villagers (NPCs)
        self.quests = quests  # List of quest IDs that are available in the village
        self.merchants = []  # Merchants that may sell items in the village

    def show_village_info(self):
        """Display the information about the village."""
        print(f"\nVillage: {self.name}")
        print(f"Region: {self.region}")
        print(f"Population: {self.population}")
        print(f"Currency: {self.currency}")
        print("Villagers:")
        for villager in self.villagers:
            print(f"- {villager.name}, {villager.role}")
        print("Available Quests:")
        for quest_id in self.quests:
            quest = quest_db.get_quest(quest_id)
            if quest:
                print(f"- {quest.title} ({'Completed' if quest.is_completed else 'In Progress'})")
            else:
                print(f"- Quest {quest_id} not found.")

    def add_merchant(self, merchant_name: str, items_for_sale: List[str]):
        """Add a merchant to the village."""
        self.merchants.append((merchant_name, items_for_sale))
        print(f"Merchant {merchant_name} has arrived in {self.name}!")

    def interact_with_villager(self, player: Character, villager_name: str):
        """Allow the player to interact with a villager."""
        villager = next((v for v in self.villagers if v.name == villager_name), None)
        if villager:
            villager.interact()
            if villager.quest_id and not quest_db.get_quest(villager.quest_id).is_completed:
                quest_db.complete_quest(player, villager.quest_id)
        else:
            print(f"{villager_name} is not in the village.")

    def show_merchant_items(self, villager_name: str):
        """Show the items available for purchase by a merchant in the village."""
        for merchant, items in self.merchants:
            print(f"\n{merchant}'s Items:")
            for item in items:
                print(f"- {item}")

# Village System
class VillageManager:
    def __init__(self):
        self.villages: Dict[str, Village] = {}

    def add_village(self, village: Village):
        """Add a village to the world."""
        self.villages[village.name] = village

    def get_village(self, village_name: str) -> Optional[Village]:
        """Get a village by name."""
        return self.villages.get(village_name)

    def list_villages(self):
        """List all villages in the world."""
        print("Villages in the world:")
        for village in self.villages.values():
            print(f"- {village.name} in {village.region} region")

# Sample Villages and NPCs
def create_sample_villages():
    village1_villagers = [
        Villager("Kaen", "Blacksmith", ["Need some armor? I can forge the best!", "I've got a new sword for you!"], quest_id="quest_1"),
        Villager("Lira", "Healer", ["Come to me if you're hurt, I'll fix you right up!", "Need some healing? I'm your person!"]),
        Villager("Zara", "Merchant", ["I've got some great items for sale today!", "Looking for a deal? I've got plenty!"])
    ]
    
    village2_villagers = [
        Villager("Oren", "Blacksmith", ["I can make you the sharpest blade in the land!", "You need new weapons? I've got just what you need."]),
        Villager("Mira", "Healer", ["A healing potion should do the trick for you.", "I have potions to restore your health."]),
        Villager("Xen", "Merchant", ["I have rare herbs for sale. Don't miss out!", "Come see my unique items."])
    ]
    
    village1 = Village(
        name="Stonebrook",
        region="Forest of Shadows",
        population=150,
        currency="Gold",
        villagers=village1_villagers,
        quests=["quest_1", "quest_2"]
    )

    village2 = Village(
        name="Crystal Haven",
        region="Crystal Mountain",
        population=80,
        currency="Silver",
        villagers=village2_villagers,
        quests=["quest_3"]
    )

    # Add villages to the village manager
    village_manager.add_village(village1)
    village_manager.add_village(village2)

# Village Manager instance
village_manager = VillageManager()

# Create sample villages and NPCs
create_sample_villages()

# Debug Example
if __name__ == "__main__":
    player = Player("Kai")
    
    print("\nWelcome to the village system!\n")
    
    # Display villages in the world
    village_manager.list_villages()

    # Show village info for "Stonebrook"
    stonebrook = village_manager.get_village("Stonebrook")
    if stonebrook:
        stonebrook.show_village_info()

    # Player interacts with a villager
    print("\nPlayer interacts with Kaen the Blacksmith:")
    stonebrook.interact_with_villager(player, "Kaen")

    # Show merchant items in "Stonebrook"
    print("\nMerchant Items in Stonebrook:")
    stonebrook.show_merchant_items("Zara")
