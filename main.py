# main.py
# Main game loop and management for the Anime RPG

import time
import random
from character import *
from quests import *
from villages import *
from villagers import *
from shop import *
from currency import *
from chats import *
from world import *

# Initialize all the game components
quest_db = QuestDatabase()
village_manager = VillageManager()
villager_manager = VillagerManager()
currency_manager = CurrencyManager()
world = World()

# Game Settings
game_running = True
current_player = None
chat_manager = ChatManager(villager_manager)
shop = Shop()

# Welcome to the game
def game_intro():
    print("\nWelcome to the Anime RPG!")
    print("Embark on a journey of quests, battles, and treasures!")
    print("\nWhat is your name, adventurer?")
    player_name = input("Enter your name: ")
    global current_player
    current_player = Player(player_name)
    print(f"\nWelcome, {current_player.name}!")

# Main Game Loop
def game_loop():
    global game_running
    while game_running:
        display_main_menu()
        choice = input("\nWhat do you want to do? (Enter a number): ")
        handle_main_menu_choice(choice)

# Main Menu
def display_main_menu():
    print("\n----- Main Menu -----")
    print("1. Explore the World")
    print("2. Chat with Villagers")
    print("3. Check Quests")
    print("4. Visit the Shop")
    print("5. View Inventory")
    print("6. Check Currency")
    print("7. Save and Exit Game")
    print("8. Exit Game Without Saving")

def handle_main_menu_choice(choice: str):
    if choice == '1':
        explore_world()
    elif choice == '2':
        chat_with_villagers()
    elif choice == '3':
        check_quests()
    elif choice == '4':
        visit_shop()
    elif choice == '5':
        view_inventory()
    elif choice == '6':
        check_currency()
    elif choice == '7':
        save_game()
    elif choice == '8':
        exit_game()
    else:
        print("Invalid choice. Please try again.")

# Explore the world (village management and interactions)
def explore_world():
    print("\nYou are now exploring the world...")
    # Choose a random village to visit
    village = random.choice(village_manager.get_all_villages())
    print(f"\nYou have arrived in the village of {village.name}.")
    village.show_village_info()

    # Allow the player to interact with the village
    interaction_choice = input("\nDo you want to interact with the villagers? (y/n): ")
    if interaction_choice.lower() == 'y':
        interact_with_villagers(village)

# Interact with villagers
def interact_with_villagers(village):
    print(f"\nVillagers in {village.name}:")
    for villager in villager_manager.get_villagers_in_village(village.name):
        print(f"- {villager.name} ({villager.role})")

    villager_choice = input("\nEnter the name of the villager you want to chat with: ")
    chat_manager.initiate_chat(current_player, villager_choice)

# Check the quests
def check_quests():
    print("\n----- Quests -----")
    if not current_player.quests:
        print("You don't have any quests at the moment.")
    else:
        for quest_id, quest in current_player.quests.items():
            print(f"Quest: {quest.title}")
            print(f"Description: {quest.description}")
            print(f"Objectives: {', '.join(quest.objectives)}")
            print(f"Progress: {quest.progress}/{len(quest.objectives)}")
            print(f"Reward: {quest.reward_exp} EXP, {quest.reward_gold} gold\n")

# Visit the shop (interact with shops to buy items)
def visit_shop():
    print("\nYou are now in the shop...")
    shop.show_items_for_sale()
    choice = input("\nDo you want to buy something? (y/n): ")
    if choice.lower() == 'y':
        item_choice = input("\nEnter the name of the item you want to buy: ")
        shop.purchase_item(current_player, item_choice)
    else:
        print("Goodbye! Come back soon.")

# View the player's inventory
def view_inventory():
    print("\n----- Inventory -----")
    if not current_player.inventory:
        print("Your inventory is empty.")
    else:
        for item in current_player.inventory:
            print(f"- {item.name} (x{item.quantity})")

# Check the player's currency
def check_currency():
    print("\n----- Currency -----")
    print(f"Current Gold: {currency_manager.get_player_gold(current_player)}")

# Save the player's game progress
def save_game():
    print("\nSaving your progress...")
    # Save logic (in reality, this would write to a file or database)
    with open("save_game.txt", "w") as save_file:
        save_file.write(f"{current_player.name}\n")
        save_file.write(f"Gold: {currency_manager.get_player_gold(current_player)}\n")
        save_file.write("Quests: ")
        for quest_id, quest in current_player.quests.items():
            save_file.write(f"{quest_id}, ")
        save_file.write("\nInventory: ")
        for item in current_player.inventory:
            save_file.write(f"{item.name} (x{item.quantity}), ")
    print("Game saved successfully!")

# Exit the game
def exit_game():
    print("\nThank you for playing the Anime RPG!")
    global game_running
    game_running = False

# Game Initialization
if __name__ == "__main__":
    game_intro()
    game_loop()
