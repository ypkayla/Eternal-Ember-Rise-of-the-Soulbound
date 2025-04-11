# quests.py
# Quest system for Anime RPG (revised to integrate additional quests)

import random
from typing import List, Dict, Optional
from character import *
from items import item_registry
from items import item_registry
from quest_templates import create_quests_from_data

class Quest:
    def __init__(
        self,
        quest_id: str,
        title: str,
        description: str,
        reward_exp: int,
        reward_gold: int,
        reward_items: List[str] = [],
        quest_giver: str = "",
        prerequisites: Optional[List[str]] = None,
        objectives: List[str] = [],
        is_completed: bool = False
    ):
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.reward_exp = reward_exp
        self.reward_gold = reward_gold
        self.reward_items = reward_items
        self.quest_giver = quest_giver
        self.prerequisites = prerequisites or []
        self.objectives = objectives
        self.is_completed = is_completed

    def check_completion(self, player: PlayerCharacter) -> bool:
        """
        Check if the quest objectives are completed by the player.
        This can be expanded to check against the player's inventory or actions.
        """
        return all(obj in player.completed_objectives for obj in self.objectives)

    def give_rewards(self, player: PlayerCharacter):
        """
        Give the rewards for completing the quest: experience, gold, and items.
        """
        player.add_experience(self.reward_exp)
        player.add_gold(self.reward_gold)

        for item_id in self.reward_items:
            item = item_registry.get_item(item_id)
            if item:
                player.add_item_to_inventory(item)
                print(f"{player.name} received {item.name} as a reward!")

        print(f"{player.name} has completed the quest: {self.title}")
        print(f"Rewards: {self.reward_exp} EXP, {self.reward_gold} gold.")

    def display_quest_info(self):
        """
        Display the basic information about the quest.
        """
        print(f"Quest: {self.title}")
        print(f"Description: {self.description}")
        print(f"Quest Giver: {self.quest_giver}")
        print(f"Objectives: {', '.join(self.objectives)}")
        print(f"Reward: {self.reward_exp} EXP, {self.reward_gold} gold")
        if self.reward_items:
            print(f"Items Rewarded: {', '.join(self.reward_items)}")

# Quest Database
class QuestDatabase:
    def __init__(self):
        self.quests: Dict[str, Quest] = {}
        self.completed_quests: Dict[str, Quest] = {}

    def add_quest(self, quest: Quest):
        self.quests[quest.quest_id] = quest

    def get_quest(self, quest_id: str) -> Optional[Quest]:
        return self.quests.get(quest_id)

    def complete_quest(self, player: PlayerCharacter, quest_id: str):
        quest = self.get_quest(quest_id)
        if quest and not quest.is_completed and quest.check_completion(player):
            quest.is_completed = True
            quest.give_rewards(player)
            self.completed_quests[quest_id] = quest
            print(f"{player.name} has completed the quest {quest.title}!")
        else:
            print(f"Quest {quest_id} is not completed yet or already finished.")

# Quest Database and Player Integration
quest_db = QuestDatabase()

# Load quests from external data (this will be populated by quels from `aquests.py`)
def load_quests_from_data():
    create_quests_from_data(quest_db)

# Debug Example
if __name__ == "__main__":
    from character import *
    player = player("Kai")
    load_quests_from_data()
    player.start_quest("quest_1")
    player.complete_objective("Goblin x 10")
    quest_db.complete_quest(player, "quest_1")
    player.start_quest("quest_2")
    player.complete_objective("Fire Dragon x 1")
    quest_db.complete_quest(player, "quest_2")
