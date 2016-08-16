import jsonpickle


class Item:

    def __init__(self, id, name, description):
        self.identifier = identifier
        self.name = name
        self.description = description

    def construct_from_entity(self, json):
        jsonpickle.decode(json)
