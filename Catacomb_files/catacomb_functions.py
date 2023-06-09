# import path from screens just like a module
import screens
from inventory import player
import inventory
from inventory import Obstacle
import main
import random
import asyncio


def create_random_world1_screen():
    global random_obstacle  # declare the variable as global inside the function
    """creates a random screen, importing from the screens file"""
    title = random.choice(screens.titles)
    description = random.choice(screens.description)
    obstacle = random.choice(screens.obstacles)
    health = random.randint(1, 5)
    obstacle_type = random.choice(screens.obstacle_types)
    doors = random.sample(screens.doors, 4)
    screen_id = random.randint(1000, 9999)
    damage = random.randint(1, 20)
    screens.screens_id.append(screen_id)  # append screen_id to the list
    # create a string with the screen information
    obstacle_screen_str = f"You are in {title}. This place is {description} You see a {obstacle}, " \
                          f"it has {health} life points." \
                          f"It seems like it is a {obstacle_type}. " \
                          f"What do you do?"
    random_obstacle = Obstacle(obstacle, obstacle_type, 1, health, damage)
    # return the screen string and the Obstacle object
    return obstacle_screen_str, random_obstacle


# obstacle instances related things, maybe this is not the best place for them, but couldn't put them to inventory #
obstacle_instance = None
# Obstacle instances handling#
# Call the create_random_world1_screen function to get the screen string and the Obstacle object
screen_str, random_obstacle = create_random_world1_screen()
# Create an instance of the Obstacle class based on the random_obstacle variable
if random_obstacle:
    obstacle_instance = Obstacle(random_obstacle.name, random_obstacle.type, random_obstacle.level,
                                 random_obstacle.health, random_obstacle.damage)
else:
    # Handle the case where random_obstacle is None
    obstacle_instance = None

    # after an unsuccessful attack or befriend, this gives the player the choice to do an action again


def another_chance():
    global another_chance_action_choice
    another_chance_action_str = input(
        'It seems like this creature is tougher than it looks, you can choose to attack or befriend them again')
    flag = False
    while not flag:
        if another_chance_action_str.lower() not in main.action_choices:
            print('Invalid choice. Please choose "attack" or "befriend".')
            another_chance_action_str = input('Which will it be? ')
        else:
            if another_chance_action_str.lower() == main.action_choices[0]:
                print(attack_world1(obstacle_instance))
            elif another_chance_action_str.lower() == main.action_choices[1]:
                print(befriend_world1())
            flag = True


# action functions related to obstacles

def get_action_choice():
    action_choices = ['attack', 'befriend']
    while True:
        choice_action = input('Which will it be? ')
        if choice_action.lower() not in action_choices:
            print('Invalid choice. Please choose "attack" or "befriend".')
        elif choice_action.lower() == action_choices[0]:
            # create a random obstacle
            screen_str, random_obstacle = create_random_world1_screen()
            attack_world1(obstacle_instance)
            return
        elif choice_action.lower() == action_choices[1]:
            print(befriend_world1())
            return


def attack_world1(obstacle_instance):
    attack_power = random.randint(1, 5)

    if attack_power >= obstacle_instance.health:
        print("You vanquished your enemy!")
        screens.defeated_obstacles.append(obstacle_instance)
    else:
        print(random.choice(screens.attack_sentences))
        obstacle_attack()


def befriend_world1():
    random_number = random.randint(0, 5)

    if random_number == 0:
        print("You became friends with " + random_obstacle.name + ", how lovely!")
    elif random_number == 1:
        print("You became associates, how interesting!")
    elif random_number == 2:
        print("You know each other from now on! Awkwardly wave next time you see each other on the bus!")
    else:
        print("They don't like you!")
        print(obstacle_attack())


def which_door_opens():
    loop = 1

    flag = False  # control mechanism, to exit the loop as conditions are met, common name for that

    while not flag:
        if random.random() < 0.60:
            door_closed_str = random.choice(screens.door_closed_strings)
            print(door_closed_str)
            choice = input('Which door will you take?')
            while choice.lower() not in main.door_choices:
                print('Invalid choice. Please choose A, B, C, or D.')
                choice = input('Which door will you take?')
            chosen_door = main.door_choices[choice.lower()]
            print(f'You chose {chosen_door}.')  # embed the value of the chosen_door inside the string
        else:
            door_open_str = random.choice(main.door_open_strings)
            print(door_open_str)
            flag = True  # set the flag to True to exit the while loop

    while loop == 1:
        print(create_random_world1_screen())

        break


# add something related to obstacle type here, connected to philosophy
def obstacle_attack():
    damage = random.randint(0, 5)
    inventory.player.hp -= damage
    print(f"The enemy strikes for {damage} damage! Your HP is now {inventory.player.hp}.")
    if damage >= inventory.player.hp:
        print("The light of the Valar is fading in you!")
        print(game_over())
    else:
        another_chance()


screen = {
    "id": screens.screens_id,
    "title": screens.titles,
    "description": screens.description,
    "obstacle": screens.obstacles,
    "doors": screens.doors
}


# probably for items?
def lose_health(self, amount):
    """Reduces the player's health by the given amount."""
    self.health -= amount
    if self.health <= 0:
        print(f"{self.name} has died!")
    else:
        print(f"{self.name} has {self.health} health remaining.")


# for items as well?
def gain_health(self, amount):
    """Increases the player's health by the given amount."""
    self.health += amount
    print(f"{self.name} has gained {amount} health. {self.name} now has {self.health} health.")


# after certain number of loops, this should happen
def level_up_obstacles(defeated_obstacles):
    """Levels up the obstacles"""
    global random_obstacle
    count_list_elements = lambda x: len(x)
    for random_obstacle in screens.defeated_obstacles:
        if count_list_elements(defeated_obstacles) > inventory.player.game_level:
            inventory.Obstacle.level += 4
            print('You progress deeper into the unknown, get ready for some tougher enemies!')
    return random_obstacle.level


# functions related to GAME OVER

async def check_player_hp():
    while True:
        await asyncio.sleep(1)  # Check player's HP every second
        if inventory.player.hp < 0:
            game_over()


def game_over():
    """if player is dead, game end"""
    if player.lives == 0:
        print('''
        ┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
        ███▀▀▀██┼███▀▀▀███┼███▀█▄█▀███┼██▀▀▀
        ██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼█┼┼┼██┼██┼┼┼
        ██┼┼┼▄▄▄┼██▄▄▄▄▄██┼██┼┼┼▀┼┼┼██┼██▀▀▀
        ██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██┼┼┼
        ███▄▄▄██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██▄▄▄
        ┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
        ███▀▀▀███┼▀███┼┼██▀┼██▀▀▀┼██▀▀▀▀██▄┼
        ██┼┼┼┼┼██┼┼┼██┼┼██┼┼██┼┼┼┼██┼┼┼┼┼██┼
        ██┼┼┼┼┼██┼┼┼██┼┼██┼┼██▀▀▀┼██▄▄▄▄▄▀▀┼
        ██┼┼┼┼┼██┼┼┼██┼┼█▀┼┼██┼┼┼┼██┼┼┼┼┼██┼
        ███▄▄▄███┼┼┼─▀█▀┼┼─┼██▄▄ ''')
