import jsonpickle
import json


class EntityManager:

    data = {}

    def loadJson(self, filename):
        with open(filename, encoding='utf-8') as data_file:
            json_data = json.loads(data_file.read())

        for key, value in json_data.items():
            self.data[key] = jsonpickle.decode(json.dumps(value))

    def get_entity(self, identifier):
        return self.data[identifier]
