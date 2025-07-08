import random
import sys
import time

#Player Constructor
player = {
    "name": "Xalthir",
    "level": 1,
    "attack": 10,
    "defense": 10,
    "speed": 20,
    "health": 100,
    "max_health": 100,
    "stamina": 100,
    "max_stamina": 100,
    "is_defending": False
}

#Monster Names list
monster_names = ['Serpent', 'Roach', 'Drake', 'Lesser Demon', 'Crawling Horror', 'Beast of the Wild', 'Bandit', 'Warlock', 'Great Old One', 'A Foul Creature', 'The Faithless God of Lost Wonder', 'A simple bat', 'A wolf', 'A deer', 'A goat', 'An undead hound', 'A Ghoul', 'A Wight']

#Monster Template
class Monster:
    def __init__(self, name, attack, damage, speed, health, defense):
        if player['level'] != 1:
            self.level = player['level'] + random.randint(-1, 1)
        else:
            self.level = player['level']
        self.name = name
        self.attack = attack
        self.damage = damage
        self.speed = speed
        self.health = health
        self.defense = defense

#Take Damage (Monster)
def take_damage(monster):
    print("You strike your foe!")
    crit_roll = random.randint(1,100)
    damage = (player['attack'] + random.randint(0, player['attack']) + player['level']) - monster.defense
    if damage < 0:
        print("You deal no damage!")
        time.sleep(1)
        return
    if crit_roll <= player['speed']:
        damage = damage * 2
        print("[✴] A CRITICAL HIT! [✴]")
    time.sleep(1)
    print(f"You deal {damage} to the {monster.name}")
    monster.health -= damage
    print(f"The {monster.name} has: {monster.health} [HP]")
    call_vitals()
    time.sleep(2)

# Monster Attack (Player)
def monster_attack(monster):
    print(f"{monster.name} strikes back!")
    monster_damage = (monster.damage + random.randint(0,monster.attack) + monster.level) - player['defense']
    if monster_damage <= 0:
        print("It deals no damage!")
        call_vitals()
    else:
        print(f"The monster deals {monster_damage} to you!")
        call_vitals()
        player['health'] -= monster_damage
    # Conditional Block Check
    if player['is_defending'] == True:
            player['is_defending'] = False
            player['defense'] -= 5
    time.sleep(1)

def defend_action():
    if player['stamina'] > 0:
        player['stamina'] -= 10
        print("You block! It consumes some stamina...")
        player['defense'] += 5
        player['is_defending'] = True
        call_vitals()
        time.sleep(2)
    else:
        print("You don't have enough stamina.")
        call_vitals()


## Combat Handler
def combat_handler(monster):
    valid_choices = ["1", "2", "3"]
    print(f"The Battle Begins: [ {player['name']} vs. {monster.name} ]")
    while monster.health > 0 and player['health'] > 0:
        print("== Battle Menu ==")
        print("1. Attack")
        print("2. Defend")
        print("3. Items")
        print("4. Flee")
        choice = input("Command: ")
        if choice not in valid_choices:
            print("Try again, that's not a valid option.")
        elif choice == "1":
            take_damage(monster)
            monster_attack(monster)
            continue
        elif choice == '2':
            defend_action()
            monster_attack(monster)
        else:
            print("In development.")
            continue
    if player['health'] < 0:
        print("Game Over")
        time.sleep(3)
        sys.exit()
    elif monster.health < 0:
        print(f"The {monster.name} has been defeated!")
    pass
    

#Visual Updater For Stats:
def call_vitals():
    
    print(f"Health: {player['health']} | Stamina: {player['stamina']}")
    
    if player['health'] > (player['max_health'] * .95):
        print('Health:  [==========]')
    elif player['health'] >= (player['max_health'] * .9):
        print('Health:  [========= ]')
    elif player['health'] >= (player['max_health'] * .8):
        print('Health:  [========  ]')
    elif player['health'] >= (player['max_health'] * .7):
        print('Health:  [=======   ]')
    elif player['health'] >= (player['max_health'] * .6):
        print('Health:  [======    ]')
    elif player['health'] >= (player['max_health'] * .5):
        print('Health:  [=====     ]')
    elif player['health'] >= (player['max_health'] * .4):
        print('Health:  [====      ]')
    elif player['health'] >= (player['max_health'] * .3):
        print('Health:  [===       ]')
    elif player['health'] >= (player['max_health'] * .2):
        print('Health:  [==        ]')
    elif player['health'] <= (player['max_health'] * .1):
        print('Health:  [=         ]')
    
    if player['stamina'] > (player['max_stamina'] * .95):
        print('Stamina: [==========]')
    elif player['stamina'] >= (player['max_stamina'] * .9):
        print('Stamina: [========= ]')
    elif player['stamina'] >= (player['max_stamina'] * .8):
        print('Stamina: [========  ]')
    elif player['stamina'] >= (player['max_stamina'] * .7):
        print('Stamina: [=======   ]')
    elif player['stamina'] >= (player['max_stamina'] * .6):
        print('Stamina: [======    ]')
    elif player['stamina'] >= (player['max_stamina'] * .5):
        print('Stamina: [=====     ]')
    elif player['stamina'] >= (player['max_stamina'] * .4):
        print('Stamina: [====      ]')
    elif player['stamina'] >= (player['max_stamina'] * .3):
        print('Stamina: [===       ]')
    elif player['stamina'] >= (player['max_stamina'] * .2):
        print('Stamina: [==        ]')
    elif player['stamina'] <= (player['max_stamina'] * .1):
        print('Stamina: [=         ]')
# End of Visual Updater

#Call stats:
def call_stats():
    print(f"{player['name'].center(30)}")
    print("=========== Stats =============")
    print(f"Attack: {player['attack']}")
    print(f"Defense: {player['defense']}")
    print(f"Speed: {player['speed']}")
# End of call_stats

#Game Loop
while True:
    valid_choices = ["1", "2", "3", "4"]
    print("Welcome to The Battleground:")
    print("This is a game where I try to make some complex mechanics to see if I can!")
    print("--------------------------------------------------------------------------")
    print("1. Hunt")
    print("2. Stats")
    print("3. Shop/Inventory")
    print("4. Quit")
    menu_choice = input("Command: ")
    if menu_choice not in valid_choices:
        print("That is not a valid command.")
        continue
    elif menu_choice == "1":
        print("You begin your hunt...")
        time.sleep(2)
        print("You hear something in the distance... you think...")
        time.sleep(2)
        print("A twig snaps...")
        time.sleep(1)
        print("A hurried series of steps, it's close!")
        time.sleep(1)
        print("It attacks!")
        print("= ==== =")
        print("===  ===")
        print("== == ==")
        current_monster = Monster(
            monster_names[random.randint(0, len(monster_names) - 1)],
            random.randint(1, 10),
            random.randint(1, 15),
            random.randint(1, 5),
            random.randint(50, 200),
            random.randint(1, 10)
        )
        combat_handler(current_monster)
        
    elif menu_choice == "2":
        call_stats()
        time.sleep(3)
        print("---------------------------------")
    elif menu_choice == "3":
        print("This feature is under construction.")
    elif menu_choice == "4":
        print("Thank you for playing!")
        sys.exit()
        
    
 