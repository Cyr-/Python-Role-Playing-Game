from EntityManager import EntityManager
from Item import Item
from Armor import Armor
from Weapon import Weapon
import json


class Inventory:
    def __init__(self, json_string):
        json_data = json.loads(json_string)
        self.items = []
        self.load(json_data['items'])

    def load(self, json_data):
        for item in json_data:
            item_identifier = item[0]
            count = item[1]
            self.items.append([item_identifier, count])

    def json_array(self):
        data = {}
        for item in self.items:
            pass

    def add(self, new_item, count):
        for item in self.items:
            if (item[0] == new_item):
                item[1] += count
                return

        self.items.append([new_item, count])

    def remove(self, item, count):
        pass

    def count(self, requested_item):
        for item in self.items:
            if (item[0] == requested_item):
                return item[1]
        return 0

    def get(self, index, entity_manager, item_type=None):
        if (item_type is not None):
            subset_list = [item for item in self.items
                           if item[0].startswith(item_type)]
            return entity_manager.get_entity(subset_list[index][0])
        else:
            return entity_manager.get_entity(self.items[index][0])

    def display(self, entity_manager, label=False, item_type=None):
        count = 1
        for item in self.items:
            if (item_type is not None):
                if (item[0].startswith(item_type)):
                    item_entity = entity_manager.get_entity(item[0])
                else:
                    continue
            else:
                item_entity = entity_manager.get_entity(item[0])

            display_line = ''
            if (label):
                display_line += '{0}: '.format(count)
                count += 1
            display_line += '{0} ({1}) - {2}'.format(
                item_entity.name, item[1], item_entity.description)
            print(display_line)

        return len(self.items)

    def clear(self):
        del self.items[:]

    def merge(self, inventory):
        if(inventory == self):
            return

        for item in inventory.items:
            self.add(item[0], item[1])

    def get_json(self):
        # data = {}
        # data['items'] =
        # data['armors'] =
        # data['weapons'] =

        # return json.dumps(data)
        pass
