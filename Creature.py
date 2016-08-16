from random import randint
from EntityManager import EntityManager
from Inventory import Inventory


class Creature:
    def __init__(self, identifier, name, hp, ap, strength, dexterity,
                 spirit, constitution, speed, experience):
        self.identifier = identifier
        self.name = name
        self.hp = hp
        self.maximum_hp = hp
        self.ap = ap
        self.maximum_ap = ap
        self.strength = strength
        self.dexterity = dexterity
        self.spirit = spirit
        self.constitution = constitution
        self.speed = speed
        self.experience = experience
        self.inventory = Inventory('{"items": []}')
        self.equipped_armor = ''
        self.equipped_weapon = ''

    def equip_weapon(self, weapon):
        self.equipped_weapon = weapon

    def equip_armor(self, armor):
        self.equipped_armor = armor

    def attack(self, target):
        damage = 0
        print(self.dexterity/2 + self.speed/2 + self.strength/4)
        print(target.dexterity/2 + target.speed/2 + target.strength/4)

        if (True):
            attack = self.strength + (EntityManager().get_entity(
                self.equipped_weapon).damage
                if self.equipped_weapon is None else 0)

            defense = target.speed + (EntityManager().get_entity(
                target.equipped_armor).defense
                if target.equipped_armor is None else 0)

            if (randint(0, 32) == 32):
                damage = randint(round(attack / 2), round(attack))
            else:
                base_damage = round(attack - defense / 2)
                damage = randint(round(base_damage / 4),
                                 round(base_damage / 2))

                if (damage < 1):
                    damage = 0

            target.hp -= damage

        return damage

    def traverse(self, door):
        flag = 2

        if (door.locked == 0):
            door.locked = -1
            flag = 2
        elif (door.locked > 0):
            if (self.inventory.count(door.key)):
                door.locked = -1
                flag = 1
            else:
                return 0

        if (door.areas[0] == self.current_area):
            self.current_area = door.areas[1]
        elif (door.areas[1] == self.current_area):
            self.current_area = door.areas[0]

        return flag

    def to_json(self):
        data = {}
        data['name'] = self.name
        data['hp'] = self.hp
        data['maximum_hp'] = self.maximum_hp
        data['ap'] = self.ap
        data['maximum_ap'] = self.maximum_ap
        data['strength'] = self.strength
        data['dexterity'] = self.dexterity
        data['spirit'] = self.spirit
        data['constitution'] = self.constitution
        data['speed'] = self.speed
        data['experience'] = self.experience
        data['inventory'] = self.inventory
        data['equipped_armor'] = self.equipped_armor
        data['equipped_weapon'] = self.equipped_weapon

        return json.dumps(data)
