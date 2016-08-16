class Dialogue:

    def __init__(self, description, choices):
        self.description = description
        self.choices = choices

    def construct_from_entity(self, json):
        self.description = json['description']
        for choice in json['choices']:
            self.choices.append(choice)

    def activate(self):
        user_input = -1
        while(1):
            print(self.description)

            count = 0
            for choice in self.choices:
                count += 1
                print('{0}: {1}'.format(count, choice))

            user_input = input()

            try:
                if (int(user_input) >= 0 and int(user_input) <= self.size()):
                    return int(user_input)
            except ValueError:
                print('Dialogue ValueError')
                pass

    def add_choice(self, choice):
        self.choices.append(choice)

    def size(self):
        return len(self.choices)
