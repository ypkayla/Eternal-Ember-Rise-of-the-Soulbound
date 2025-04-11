# aquest.py
# External quest data management for Anime RPG

from quests import QuestDatabase
from typing import List

def create_quests_from_data(quest_db: QuestDatabase):
    quest_data = get_quest_data()
    for quest_info in quest_data:
        quest = Quest(
            quest_id=quest_info["quest_id"],
            title=quest_info["title"],
            description=quest_info["description"],
            reward_exp=quest_info["reward_exp"],
            reward_gold=quest_info["reward_gold"],
            reward_items=quest_info["reward_items"],
            quest_giver=quest_info["quest_giver"],
            prerequisites=quest_info["prerequisites"],
            objectives=quest_info["objectives"],
            is_completed=False
        )
        quest_db.add_quest(quest)

def get_quest_data() -> List[dict]:
    """
    This function returns quest data in the format required for the Quest class.
    Add new quests here.
    """
    return [
        {
            "quest_id": "quest_1",
            "title": "Goblin Slayer",
            "description": "Defeat 10 Goblins to protect the village.",
            "reward_exp": 100,
            "reward_gold": 50,
            "reward_items": ["potion_hp50"],
            "quest_giver": "Village Elder",
            "prerequisites": [],
            "objectives": ["Goblin x 10"]
        },
        {
            "quest_id": "quest_2",
            "title": "Dragon Hunt",
            "description": "Slay the Fire Dragon that terrorizes the countryside.",
            "reward_exp": 500,
            "reward_gold": 200,
            "reward_items": ["iron_sword", "buff_atk10"],
            "quest_giver": "Knight Commander",
            "prerequisites": ["quest_1"],
            "objectives": ["Fire Dragon x 1"]
        },
        {
            "quest_id": "quest_3",
            "title": "Treasure Hunt",
            "description": "Find the hidden treasure in the Forbidden Forest.",
            "reward_exp": 300,
            "reward_gold": 100,
            "reward_items": ["golden_ring"],
            "quest_giver": "Treasure Hunter",
            "prerequisites": [],
            "objectives": ["Treasure x 1"]
        },



    ]
