from Dialogue import Dialogue
from operator import attrgetter


class BattleEvent:
    def __init__(self, source_creature, target_creature, event_type):
        self.source_creature = source_creature
        self.target_creature = target_creature
        self.event_type = event_type

    def run(self):
        if (self.event_type == 'attack'):
            return self.source_creature.attack(self.target_creature)
        elif (self.event_type == 'defend'):
            return 0
        else:
            return 0


class Battle:
    def __init__(self, combatants):
        self.combatants = combatants
        self.battle_options = Dialogue(
            'What will you do?', ['Attack', 'Defend'])

        names = {}
        for combatant in self.combatants:
            if (combatant.identifier == 'player'):
                pass
            if (combatant.name not in names):
                names[combatant.name] = 0
            elif (combatant.name in names):
                names[combatant.name] = 1

        for combatant in self.combatants:
            new_name = combatant.name

            if (combatant.name in names and names[combatant.name] > 0):
                new_name += ' ({0})'.format(names[combatant.name])
                names[combatant.name] += 1

            combatant.name = new_name

    def kill(self, creature):
        if (creature in self.combatants):
            print('{0} is slain!'.format(creature.name))
            creature.hp = 0
            self.combatants.remove(creature)

    def run(self):
        while (True):
            for combatant in self.combatants:
                if (combatant.identifier == 'player'):
                    player = combatant
            end = self.combatants[-1]

            self.next_turn()

            if(player == end and len(self.combatants) <= 1):
                break

    def next_turn(self):
        events = []
        sorted(self.combatants, key=attrgetter('speed'), reverse=True)

        for combatant in self.combatants:
            if (combatant.identifier == 'player'):
                target_selection = Dialogue('Who?', [])

                for target in self.combatants:
                    if (target.identifier != 'player'):
                        target_selection.add_choice(target.name)
                    else:
                        player_position = self.combatants.index(target)

                choice = self.battle_options.activate()

                if (choice == 1):
                    position = target_selection.activate()

                    if (position > player_position):
                        position += 1

                    target = self.combatants[position - 1]

                    events.append(BattleEvent(combatant, target, 'attack'))
                elif (choice == 2):
                    events.append(BattleEvent(combatant, None, 'defend'))
            else:
                for target in self.combatants:
                    if (target.identifier == 'player'):
                        player = target
                events.append(BattleEvent(combatant, player, 'attack'))
        while(events != []):
            event = events[0]

            if (event.event_type == 'attack'):
                if (event.source_creature not in self.combatants or
                        event.target_creature not in self.combatants):
                    break

                print('{0} attacks {1} for {2} damage!'.format(
                    event.source_creature.name,
                    event.target_creature.name,
                    event.run()))

                if (event.target_creature.hp <= 0):
                    self.kill(event.target_creature)

            elif (event.event_type == 'defend'):
                print('{0} defends!'.format(event.source_creature.name))
            else:
                pass

            events.pop(0)
