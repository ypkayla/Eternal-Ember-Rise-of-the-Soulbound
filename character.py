import random
from typing import List, Dict, Optional

class StatusEffect:
    """
    Represents a status effect that can be applied to a character.
    Examples: Poison, Burn, Frozen
    """
    def __init__(self, name: str, duration: int, effect: Dict[str, int]):
        self.name = name
        self.duration = duration
        self.effect = effect

    def tick(self):
        """Decreases duration every turn."""
        self.duration -= 1
        return self.duration <= 0


class Equipment:
    """
    Represents equippable gear.
    """
    def __init__(self, name: str, slot: str, stat_boosts: Dict[str, int]):
        self.name = name
        self.slot = slot  # e.g., head, body, weapon, accessory
        self.stat_boosts = stat_boosts


class Skill:
    """
    Represents an active or passive skill.
    """
    def __init__(self, name: str, mana_cost: int, damage: int, effect: Optional[StatusEffect] = None):
        self.name = name
        self.mana_cost = mana_cost
        self.damage = damage
        self.effect = effect


class PlayerCharacter:
    """
    Main class for the player or party members.
    """

    def __init__(self, name: str, char_class: str):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100

        self.base_stats = {
            'HP': 100,
            'MP': 30,
            'Attack': 10,
            'Defense': 8,
            'Speed': 5,
            'Luck': 3
        }

        self.current_stats = self.base_stats.copy()
        self.current_stats['HP'] = self.max_hp
        self.current_stats['MP'] = self.max_mp

        self.inventory: List[str] = []  # IDs of items
        self.equipment: Dict[str, Optional[Equipment]] = {
            'head': None,
            'body': None,
            'weapon': None,
            'accessory': None
        }

        self.skills: List[Skill] = []
        self.status_effects: List[StatusEffect] = []

    @property
    def max_hp(self):
        return self.base_stats['HP'] + self._equipment_stat_total('HP')

    @property
    def max_mp(self):
        return self.base_stats['MP'] + self._equipment_stat_total('MP')

    def _equipment_stat_total(self, stat: str) -> int:
        total = 0
        for item in self.equipment.values():
            if item:
                total += item.stat_boosts.get(stat, 0)
        return total

    def gain_exp(self, amount: int):
        """
        Add EXP and handle leveling up.
        """
        self.exp += amount
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level_up()

    def level_up(self):
        """
        Increases character level and improves stats.
        """
        self.level += 1
        self.exp_to_next = int(self.exp_to_next * 1.25)
        self.base_stats['HP'] += 10
        self.base_stats['MP'] += 5
        self.base_stats['Attack'] += 2
        self.base_stats['Defense'] += 2
        self.base_stats['Speed'] += 1
        self.base_stats['Luck'] += 1
        print(f"{self.name} leveled up to {self.level}!")

    def take_damage(self, amount: int):
        reduced = max(0, amount - self.base_stats['Defense'])
        self.current_stats['HP'] -= reduced
        print(f"{self.name} took {reduced} damage!")
        if self.current_stats['HP'] <= 0:
            print(f"{self.name} has been defeated.")

    def heal(self, amount: int):
        self.current_stats['HP'] = min(self.max_hp, self.current_stats['HP'] + amount)
        print(f"{self.name} healed {amount} HP!")

    def use_skill(self, skill: Skill, target):
        if self.current_stats['MP'] >= skill.mana_cost:
            self.current_stats['MP'] -= skill.mana_cost
            print(f"{self.name} used {skill.name}!")
            target.take_damage(skill.damage)
            if skill.effect:
                target.apply_status(skill.effect)
        else:
            print(f"Not enough MP to use {skill.name}.")

    def apply_status(self, status: StatusEffect):
        print(f"{self.name} is now affected by {status.name}!")
        self.status_effects.append(status)

    def update_status_effects(self):
        remaining = []
        for effect in self.status_effects:
            for stat, value in effect.effect.items():
                self.current_stats[stat] = max(0, self.current_stats[stat] - value)
            if not effect.tick():
                remaining.append(effect)
        self.status_effects = remaining

    def equip(self, item: Equipment):
        self.equipment[item.slot] = item
        print(f"{self.name} equipped {item.name} to {item.slot}.")

    def unequip(self, slot: str):
        if self.equipment[slot]:
            print(f"{self.name} unequipped {self.equipment[slot].name} from {slot}.")
            self.equipment[slot] = None

    def add_item_to_inventory(self, item_id: str):
        self.inventory.append(item_id)
        print(f"{self.name} received item: {item_id}.")

    def show_stats(self):
        print(f"--- {self.name} ---")
        print(f"Class: {self.char_class} | Level: {self.level}")
        print(f"HP: {self.current_stats['HP']}/{self.max_hp}")
        print(f"MP: {self.current_stats['MP']}/{self.max_mp}")
        for stat in ['Attack', 'Defense', 'Speed', 'Luck']:
            print(f"{stat}: {self.base_stats[stat]} (+{self._equipment_stat_total(stat)})")
        print("Skills:", [skill.name for skill in self.skills])
        print("Status Effects:", [status.name for status in self.status_effects])

    def save_data(self) -> dict:
        """
        Return serializable character data.
        """
        return {
            'name': self.name,
            'char_class': self.char_class,
            'level': self.level,
            'exp': self.exp,
            'base_stats': self.base_stats,
            'inventory': self.inventory,
            'equipment': {
                k: (v.name if v else None) for k, v in self.equipment.items()
            },
            'skills': [skill.name for skill in self.skills],
            'status_effects': [(e.name, e.duration, e.effect) for e in self.status_effects]
        }

    def load_data(self, data: dict):
        """
        Load character data from dictionary.
        """
        self.name = data['name']
        self.char_class = data['char_class']
        self.level = data['level']
        self.exp = data['exp']
        self.base_stats = data['base_stats']
        self.current_stats = self.base_stats.copy()
        self.inventory = data['inventory']
        # Equipment and skills should be loaded with cross-referencing item and skill databases
        # Placeholder: assuming external managers


# Sample usage
if __name__ == "__main__":
    hero = PlayerCharacter("Kaito", "Soul Samurai")
    sword = Equipment("Fire Katana", "weapon", {"Attack": 15, "HP": 10})
    burn = StatusEffect("Burning", 3, {"HP": 2})
    flame_slash = Skill("Flame Slash", 5, 20, burn)

    hero.skills.append(flame_slash)
    hero.equip(sword)
    hero.add_item_to_inventory("potion")
    hero.show_stats()

    enemy = PlayerCharacter("Dummy", "Training Dummy")
    hero.use_skill(flame_slash, enemy)
    enemy.update_status_effects()
    enemy.show_stats()
