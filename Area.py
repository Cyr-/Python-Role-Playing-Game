import jsonpickle


class Area:
    def __init__(self, identifier, dialogue, inventory, creatures):
        entity_manager = EntityManager()
        self.identifier = identifier
        self.dialogue = dialogue
        self.inventory = inventory
        for creature in creatures:
            self.creatures.append(entity_manager.get_entity(creature))

    def construct_from_entity(self, json):
        jsonpickle.decode(json)

    def load(self, json, entity_manager):
        return jsonpickle.decode(json)

    def get_json(self):
        return jsonpickle.encode(self)
