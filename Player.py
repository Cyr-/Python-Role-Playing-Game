from Creature import Creature
import jsonpickle
import json


class Player(Creature):

    def __init__(self, identifier, name, hp, ap, strength, dexterity, spirit,
                 constitution, speed, experience, level, class_name):
        super(Player, self).__init__(identifier, name, hp, ap, strength,
                                     dexterity, spirit, constitution,
                                     speed, experience)
        self.level = level
        self.class_name = class_name
        self.visited_areas = []
        self.equipped_armor = ''
        self.equipped_weapon = ''

    def construct_from_entity(self, player_data, area_data):
        jsonpickle.decode(player_data)
        jsonpickle.decode(area_data)

    def experience_to_level(self, level):
        return 1.5 * level**3

    def level_up(self):
        if (self.experience < self.experience_to_level(self.level + 1)):
            return False

        self.level += 1

        return True

    def to_json(self):
        return jsonpickle.encode(self)

    def save(self, entity_manager):
        player_data = jsonpickle.encode(self)
        with open('{0}.json'.format(self.name), 'w') as f:
            f.write(player_data)

        area_data = {}
        for area in self.visited_areas:
            area_data[area] = entity_manager.get_entity(
                area).get_json()

        with open('{0}_areas.json'.format(self.name), 'w') as f:
            f.write(area_data)

    def load(self, json):
        pass

    def load_area(self, area_data, entity_manager):
        area_data.getObject()
        for area in area_data:
            key = area[0]
            entity_manager.get_entity(key)
            self.visited_areas.append(key)
