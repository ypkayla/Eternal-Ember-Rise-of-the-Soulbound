# chats.py
# Advanced Chat system with various interactions and dialogue choices

import time
from typing import List, Dict, Optional
from character import Character
from villagers import Villager, VillagerManager
from quests import QuestDatabase
from random import choice, randint


class Chat:
    def __init__(self, character: Villager, player: Character):
        """
        Initializes the chat system between the player and a villager.
        """
        self.character = character
        self.player = player
        self.dialogue_options: List[str] = self.generate_dialogue_options()

    def generate_dialogue_options(self):
        """
        Generate different dialogue options based on the villager's role,
        player's quests, and other variables.
        """
        options = []

        if self.character.role == "Blacksmith":
            options.append("Tell me about your best weapons.")
            options.append("Do you have any special offers?")
            options.append("I need to upgrade my armor.")
        
        elif self.character.role == "Merchant":
            options.append("What are you selling today?")
            options.append("Can I buy something?")
            options.append("Do you have any special items?")
        
        elif self.character.role == "Healer":
            options.append("Can you heal me?")
            options.append("Tell me about your potions.")
            options.append("Are there any diseases spreading in the village?")
        
        # Quest-related options
        if self.character.quest_id:
            quest = quest_db.get_quest(self.character.quest_id)
            if quest and not quest.is_completed:
                options.append(f"Tell me more about your quest '{quest.title}'.")

        # Special event-related options
        if self.character.event_trigger == "special_sale":
            options.append("I heard about your special sale!")
        
        if self.character.event_trigger == "hidden_secret":
            options.append("Is there something hidden in the village?")

        # General options
        options.append("Goodbye.")
        return options

    def start_chat(self):
        """
        Starts the chat session and displays the available options.
        """
        print(f"\n{self.character.name} is ready to chat!")
        while True:
            print(f"\n{self.character.name}: {choice(self.character.dialogue)}")
            print("\nWhat do you want to talk about?")
            
            for idx, option in enumerate(self.dialogue_options, 1):
                print(f"{idx}. {option}")

            try:
                choice_index = int(input("\nChoose an option (Enter the number): "))
                if choice_index < 1 or choice_index > len(self.dialogue_options):
                    print("Invalid choice. Please try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice_index == len(self.dialogue_options):
                print(f"\n{self.character.name}: Farewell, traveler!")
                break

            # Handle dialogue options based on the player's choice
            self.handle_choice(choice_index)

    def handle_choice(self, choice_index: int):
        """
        Handle the chosen dialogue option and interact with the player.
        """
        choice = self.dialogue_options[choice_index - 1]

        if choice == "Tell me about your best weapons.":
            print(f"\n{self.character.name}: I have the finest weapons in the land!")
            print("Would you like to buy one?")
            self.character.trade(self.player)

        elif choice == "Do you have any special offers?":
            if self.character.event_trigger == "special_sale":
                print(f"\n{self.character.name}: Yes, today I have a special offer!")
                self.character.trade(self.player)
            else:
                print(f"\n{self.character.name}: Sorry, no special offers today.")

        elif choice == "I need to upgrade my armor.":
            print(f"\n{self.character.name}: You should check my best armor! I can upgrade it for you.")
            # Call an upgrade system (Could be extended in the future)
            print("Armor upgrade: 100 gold")

        elif choice == "What are you selling today?":
            print(f"\n{self.character.name}: Today I have these items for sale:")
            self.character.trade(self.player)

        elif choice == "Can I buy something?":
            print(f"\n{self.character.name}: I have the following items in stock:")
            self.character.trade(self.player)

        elif choice == "Do you have any special items?":
            print(f"\n{self.character.name}: I've got a few rare items today. Have a look!")
            self.character.trade(self.player)

        elif choice == "Can you heal me?":
            print(f"\n{self.character.name}: I can heal you, for a price of 50 gold.")
            # Handle healing
            self.player.add_gold(-50)
            print("You have been healed!")

        elif choice == "Tell me about your potions.":
            print(f"\n{self.character.name}: I brew the finest potions. Health potions, mana potions, and more!")
            print("Would you like to purchase one?")
            self.character.trade(self.player)

        elif choice == "Are there any diseases spreading in the village?":
            print(f"\n{self.character.name}: Fortunately, no diseases right now, but I am keeping a watchful eye.")

        elif "Tell me more about your quest" in choice:
            quest = quest_db.get_quest(self.character.quest_id)
            if quest:
                print(f"\n{self.character.name}: You have a quest: '{quest.title}'")
                print(f"Quest Description: {quest.description}")
                print(f"Objectives: {', '.join(quest.objectives)}")
                print(f"Reward: {quest.reward_exp} EXP, {quest.reward_gold} Gold.")

        elif choice == "I heard about your special sale!":
            print(f"\n{self.character.name}: Yes, everything is discounted today. Come and see!")
            self.character.trade(self.player)

        elif choice == "Is there something hidden in the village?":
            print(f"\n{self.character.name}: Hmm, there are always rumors about hidden treasures...")
            print("Try exploring the forest and talk to the elders. You might find something.")

        elif choice == "Goodbye.":
            print(f"\n{self.character.name}: Take care, adventurer.")

class ChatManager:
    def __init__(self, villager_manager: VillagerManager):
        """
        Manages the chat interactions for multiple villagers.
        """
        self.villager_manager = villager_manager

    def initiate_chat(self, player: Character, villager_name: str):
        """
        Start a chat with a villager.
        """
        villager = self.villager_manager.get_villager(villager_name)
        if villager:
            chat = Chat(villager, player)
            chat.start_chat()
        else:
            print(f"{villager_name} is not available for a chat right now.")

# Example usage
if __name__ == "__main__":
    from character import Player
    from villagers import VillagerManager

    player = Player("Kai")
    villager_manager = VillagerManager()

    # Create sample villagers and add them to the system
    villager_manager.add_villager(Villager(name="Kaen", role="Blacksmith", dialogue=["Need some new armor?", "I can make you the best sword in the land!"]))
    villager_manager.add_villager(Villager(name="Zara", role="Merchant", dialogue=["Looking for something special? I've got items for sale!", "Come see my latest goods!"]))
    villager_manager.add_villager(Villager(name="Lira", role="Healer", dialogue=["Come to me if you're injured, I have potions.", "I can heal your wounds for a small fee."]))

    # Chat Manager
    chat_manager = ChatManager(villager_manager)

    # Initiate chat with villagers
    chat_manager.initiate_chat(player, "Kaen")
    chat_manager.initiate_chat(player, "Zara")
    chat_manager.initiate_chat(player, "Lira")
