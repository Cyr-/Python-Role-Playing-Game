from EntityManager import EntityManager
from Item import Item


class Armor(Item):
    def __init__(self, id, name, description, defense):
        super(Armor, self).__init__(self, id, name, description)
        self.defense = defense
        self.dodge = dodge

    def construct_from_entity(self, id, json, entity_manager):
        super(Armor, self).construct_from_entity(
            self, id, json, entity_manager)
        self.load(self, json, entity_manager)

    def load(self, json, entity_manager):
        super(Armor, self).load(self, json, entity_manager)
        self.defense = int(json['defense'])
        self.dodge = int(json['dodge'])
