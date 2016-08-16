from EntityManager import EntityManager
from Item import Item


class Weapon(Item):
    def __init__(self, id, name, description, damage):
        super(Weapon, self).__init__(self, id, name, description)
        self.damage = damage

    def construct_from_entity(self, id, json, entity_manager):
        super(Weapon, self).construct_from_entity(
            self, id, json, entity_manager)
        self.load(self, json, entity_manager)

    def load(self, json, entity_manager):
        super(Weapon, self).load(self, json, entity_manager)
        self.damage = int(json['damage'])
