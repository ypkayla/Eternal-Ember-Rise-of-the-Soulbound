# enemies.py
# Enemy system for Anime RPG

import random
import uuid
from typing import List, Dict, Callable
from character import Character
from items import get_random_loot, item_registry

class Enemy:
    def __init__(
        self,
        enemy_id: str,
        name: str,
        level: int,
        max_hp: int,
        atk: int,
        defense: int,
        speed: int,
        exp_reward: int,
        gold_reward: int,
        loot_table: Dict[str, float],  # item_id: drop chance
        special_abilities: List[Callable] = [],
        battle_intro: str = "",
        ascii_art: str = "",
    ):
        self.enemy_id = enemy_id
        self.name = name
        self.level = level
        self.hp = max_hp
        self.max_hp = max_hp
        self.atk = atk
        self.defense = defense
        self.speed = speed
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.loot_table = loot_table
        self.special_abilities = special_abilities
        self.battle_intro = battle_intro
        self.ascii_art = ascii_art

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int):
        reduced = max(1, amount - self.defense)
        self.hp -= reduced
        print(f"{self.name} took {reduced} damage! HP left: {self.hp}")
        if self.hp <= 0:
            print(f"{self.name} has been defeated!")

    def attack_target(self, target: Character):
        print(f"{self.name} attacks {target.name}!")
        target.take_damage(self.atk)

    def drop_loot(self) -> List[str]:
        dropped = []
        for item_id, chance in self.loot_table.items():
            if random.random() < chance:
                dropped.append(item_id)
        return dropped

    def use_special(self, target: Character):
        if self.special_abilities:
            ability = random.choice(self.special_abilities)
            ability(self, target)

    def show_ascii(self):
        if self.ascii_art:
            print(self.ascii_art)

# Example special abilities
def fire_blast(enemy: 'Enemy', target: Character):
    dmg = enemy.atk + 10
    print(f"🔥 {enemy.name} casts Fire Blast!")
    target.take_damage(dmg)

def heal_self(enemy: 'Enemy', target: Character):
    heal_amt = min(20, enemy.max_hp - enemy.hp)
    enemy.hp += heal_amt
    print(f"✨ {enemy.name} heals for {heal_amt} HP!")

# Enemy Factory
class EnemyFactory:
    def __init__(self):
        self.enemy_templates: Dict[str, Enemy] = {}

    def register_template(self, enemy: Enemy):
        self.enemy_templates[enemy.enemy_id] = enemy

    def create_enemy(self, enemy_id: str, level: int = None) -> Enemy:
        template = self.enemy_templates.get(enemy_id)
        if not template:
            raise ValueError("Unknown enemy_id")
        # Scale stats
        scale = level / template.level if level else 1
        new_enemy = Enemy(
            enemy_id=str(uuid.uuid4()),
            name=template.name,
            level=level if level else template.level,
            max_hp=int(template.max_hp * scale),
            atk=int(template.atk * scale),
            defense=int(template.defense * scale),
            speed=int(template.speed * scale),
            exp_reward=int(template.exp_reward * scale),
            gold_reward=int(template.gold_reward * scale),
            loot_table=template.loot_table,
            special_abilities=template.special_abilities,
            battle_intro=template.battle_intro,
            ascii_art=template.ascii_art
        )
        return new_enemy

enemy_factory = EnemyFactory()

# Example Enemies
goblin = Enemy(
    enemy_id="goblin",
    name="Goblin",
    level=1,
    max_hp=40,
    atk=8,
    defense=2,
    speed=5,
    exp_reward=10,
    gold_reward=5,
    loot_table={"potion_hp50": 0.2},
    special_abilities=[fire_blast],
    battle_intro="A wild Goblin appears with a nasty grin!",
    ascii_art="""
    ,      ,
   /(.-""-.)\
   |\_/\_/|
   (_ o o _)
    (  T  )
   .-\_=-_/--.
  /          \
 (  )  .--.  )
  ""   |  |  ""
       |  |
       |_|"""
)

dragon = Enemy(
    enemy_id="dragon",
    name="Fire Dragon",
    level=10,
    max_hp=300,
    atk=35,
    defense=20,
    speed=10,
    exp_reward=200,
    gold_reward=500,
    loot_table={"buff_atk10": 0.5, "iron_sword": 0.1},
    special_abilities=[fire_blast, heal_self],
    battle_intro="🔥 A mighty Fire Dragon descends from the sky!",
    ascii_art="""
              __====-_  _-====__
      _--^^^#####//      \\\#####^^^--_
     -^##########// (    ) \\\##########^-
    _/###\\######//  |\^^/|  \\\######//###\_
   /###\\\\####//   (@::@)   \\\####//\\\\###\
  |####\\\\##//     \\__/     \\\##//\\\\####|
   \######(          \\__/         )######/
    \##\##\ \       __|  |__       / /##/##/
     \######\_____///      \\\_____//######/
      -\#########///        \\\#########/-
         ----____|/          \|____----
"""
)

def register_all_enemies():
    enemy_factory.register_template(goblin)
    enemy_factory.register_template(dragon)

# Example battle simulator
def simulate_battle(player: Character, enemy: Enemy):
    print(enemy.battle_intro)
    enemy.show_ascii()
    print("Battle Start!")

    while player.is_alive() and enemy.is_alive():
        if player.speed >= enemy.speed:
            player.attack(enemy)
            if enemy.is_alive():
                enemy.attack_target(player)
        else:
            enemy.attack_target(player)
            if player.is_alive():
                player.attack(enemy)

    if player.is_alive():
        print(f"{player.name} won! Gained {enemy.exp_reward} EXP and {enemy.gold_reward} gold.")
        loot = enemy.drop_loot()
        for item_id in loot:
            item = item_registry.get_item(item_id)
            if item:
                print(f"Looted: {item.name}")
    else:
        print(f"{player.name} was defeated by {enemy.name}...")

# Debug Example
if __name__ == "__main__":
    from character import Player
    register_all_enemies()
    player = Player("Kai")
    gob = enemy_factory.create_enemy("goblin")
    simulate_battle(player, gob)
