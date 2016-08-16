from EntityManager import EntityManager
from Item import Item
from Armor import Armor
from Weapon import Weapon
from Inventory import Inventory
from Player import Player
from Dialogue import Dialogue
from Area import Area
from Door import Door
from Battle import Battle
import os.path
import json
import jsonpickle
import copy


class Main:

    def __init__(self):
        self.entity_manager = EntityManager()

        self.entity_manager.loadJson('items.json')
        self.entity_manager.loadJson('armors.json')
        self.entity_manager.loadJson('weapons.json')
        self.entity_manager.loadJson('areas.json')
        self.entity_manager.loadJson('doors.json')
        self.entity_manager.loadJson('creatures.json')

        player = self.start_game()

        player.current_area = 'area_01'

        while(True):
            player.visited_areas.append(player.current_area)
            area = self.entity_manager.get_entity(player.current_area)
            # player.save(self.entity_manager)

            if (len(area.creatures) > 0):
                print('You are attacked by ')

                combatants = []

                for creature in area.creatures:
                    creature = self.entity_manager.get_entity(creature)
                    print(creature.name)
                    combatants.append(creature)

                combatants.append(player)

                battle = Battle(combatants)
                battle.run()

                if (player.hp > 0):
                    experience_points = 0

                    for creature in area.creatures:
                        experience_points += self.entity_manager.get_entity(
                            creature).experience
                        player.experience += experience_points

                    print('You gained {0} experience!'.format(
                        experience_points))

                    del area.creatures[:]
                else:
                    print('----The End---')
                    break

            room_options = copy.deepcopy(area.dialogue)

            for door_identifier in area.doors:
                door = self.entity_manager.get_entity(door_identifier)
                room_options.add_choice('Go through the {0}'.format(
                    door.description))

            room_options.add_choice('Search')

            result = room_options.activate()

            if (result == 0):
                self.dialogue_menu(player)
            elif (result <= area.dialogue.size()):
                pass
            elif (result < room_options.size()):
                door = self.entity_manager.get_entity(
                    area.doors[result - area.dialogue.size()-1])
                flag = player.traverse(door)

                if (flag == 0):
                    print('The {0} is locked'.format(
                        door.description))
                elif (flag == 1):
                    print('You unlock the {0} and go through it'.format(
                        door.description))
                elif (flag == 2):
                    print('You go through the {0}'.format(
                        door.description))
            else:
                print('You find:')
                area.inventory.display(self.entity_manager)
                player.inventory.merge(area.inventory)
                del area.inventory.items[:]

    def start_game(self):
        print('What is your name?')
        name = input()

        if (os.path.isfile(name + '.json')):
            with open(name + '.json', encoding='utf-8') as data_file:
                save_data = json.dumps(json.loads(data_file.read()))

            with open(name + '_areas.json', encoding='utf-8') as data_file:
                area_data = json.dumps(json.loads(data_file.read()))

            return Player.construct_from_entity(
                save_data, area_data, self.entity_manager)
        else:
            dialogue = Dialogue('Choose your class', ['Fighter', 'Rogue'])
            result = dialogue.activate()

            if (result == 1):
                player = Player('player', name,
                                10, 10, 10, 5, 5, 10, 7, 0, 1, 'Fighter')
            elif (result == 2):
                player = Player('player', name,
                                10, 10, 5, 10, 7, 5, 10, 0, 1, 'Rogue')
            return player

    def dialogue_menu(self, player):
        menu_dialogue = Dialogue('Menu', ['Items', 'Equipment', 'Character'])
        menu_result = menu_dialogue.activate()

        if (menu_result == 1):
            print('Items')
            player.inventory.display(self.entity_manager)
        elif (menu_result == 2):
            print('Equipment')
            print('Armor: {0}'.format(getattr(
                player.equipped_armor, 'name', '')))
            print('Weapon: {0}'.format(getattr(
                player.equipped_weapon, 'name', '')))

            equipment_dialogue = Dialogue(
                '', ['Equip Armor', 'Equip Weapon', 'Close'])
            equipment_result = equipment_dialogue.activate()

            if (equipment_result == 1):
                user_input = 0
                armor_count = player.inventory.display(
                    self.entity_manager, True, 'armor')

                print('Equip which item?')
                user_input = input()

                if (int(user_input) >= 1 and int(user_input) <= armor_count):
                    player.equip_armor(player.inventory.get(
                        int(user_input)-1, self.entity_manager, 'armor'))

            elif (equipment_result == 2):
                user_input = 0
                weapon_count = player.inventory.display(
                    self.entity_manager, True, 'weapon')

                print('Equip which item?')
                user_input = input()

                if (int(user_input) >= 1 and int(user_input) <= weapon_count):
                    player.equip_weapon(player.inventory.get(
                        int(user_input)-1, self.entity_manager, 'weapon'))

        elif (menu_result == 3):
            print('Character')
            print('Name: {0}'.format(player.name))
            if (player.class_name != ''):
                print('Class: {0}'.format(player.class_name))
            print('HP: {0}/{1}'.format(player.hp, player.maximum_hp))
            print('AP: {0}/{1}'.format(player.hp, player.maximum_hp))
            print('Strength: {0}'.format(player.strength))
            print('Dexterity: {0}'.format(player.dexterity))
            print('Spirit: {0}'.format(player.spirit))
            print('Constitution: {0}'.format(player.constitution))
            print('Speed: {0}'.format(player.speed))
            print('Level: {0} ({1}/{2})'.format(
                player.level, player.experience,
                player.experience_to_level(player.level)))
        else:
            pass

Main()
