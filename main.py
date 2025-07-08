import random
import sys
import time
import copy

#Player Constructor
player = {
    "name": "Xalthir",
    "level": 1,
    "exp": 0,
    "attack": 10,
    "defense": 10,
    "speed": 20,
    "health": 100,
    "max_health": 100,
    "stamina": 100,
    "max_stamina": 100,
    "regen": 2,
    "is_defending": False
}

inventory = {
    "minor_health_potions": 0,
    "major_health_potions": 0,
    "gold_coins": 0,
}

## Potion Declaration
major_hp_value = player['level'] * 10
minor_hp_value = player['level'] * 5
## Want to find a better way to do this.

##SUMMON INVENTORY
def call_inventory():
    print("==Inventory==")
    print(f"1. Minor Health Potions: {inventory['minor_health_potions']}")
    print(f"2. Major Health Potions: {inventory['major_health_potions']}")
    print(f"Gold Coins:              {inventory['gold_coins']}")
    time.sleep(2)

## LEVEL UP
def level_check():
    experience_needed = player['level'] * 100
    if player['exp'] >= experience_needed:
        player['level'] += 1
        player['exp'] = 0
        player['max_health'] += 10
        player['max_stamina'] += 10
        player['attack'] += random.randint(0,3)
        player['defense'] += random.randint(0,3)
        player['speed'] += random.randint(0,1)
        player['regen'] += random.randint(0,1)
        print(f"You have leveled up! You are now: Level [{player['level']}]")
        time.sleep(1)
    pass

#Monster Names list
monster_names = ['Serpent', 'Roach', 'Drake', 'Lesser Demon', 'Crawling Horror', 'Beast of the Wild', 'Bandit', 'Warlock', 'Great Old One', 'A Foul Creature', 'The Faithless God of Lost Wonder', 'A simple bat', 'A wolf', 'A deer', 'A goat', 'An undead hound', 'A Ghoul', 'A Wight']
bestiary = {}

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

## POPULATE BESTIARY
def populate_bestiary():
    local_bestiary = {}
    for name in monster_names:
        new_monster = Monster(
            name=name,
            attack=random.randint(5, 13),
            damage=random.randint(5, 13),
            speed=random.randint(1, 15),
            health=random.randint(30, 150),
            defense=random.randint(1, 10)
        )
        local_bestiary[name] = new_monster
        print(f"Name: {new_monster.name}")
        print(f"HP: {new_monster.health}")
        print(f"Attack: {new_monster.attack}")
        print(f"Defense: {new_monster.defense}")
        print(f"Speed: {new_monster.speed}")
    print ("Your bestiary has been generated for this run.")
    return local_bestiary
    
## Combat Handler
def combat_handler(monster):
    valid_choices = ["1", "2", "3"]
    print(f"The Battle Begins: [ {player['name']} vs. {monster.name} Lv. {monster.level}]")
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
            continue
        elif choice == '3':
            item_menu()
            continue
        else:
            print("In development.")
            continue
    if player['health'] <= 0 and monster.health <= 0:
        print("It's a draw, unfortunately, dead is dead.")
        time.sleep(1)
        print("Game Over")
        sys.exit()
    elif player['health'] <= 0:
        print("Game Over")
        time.sleep(3)
        sys.exit()
    elif monster.health <= 0:
        print(f"The {monster.name} has been defeated!")
        gained_exp = monster.level * 5
        player['exp'] += gained_exp
        print(f"You gain: {gained_exp} experience.")
        level_check()
        gold_acquired = random.randint(0, monster.level)
        inventory['gold_coins'] += gold_acquired
        time.sleep(2)
        print(f"You gain: {gold_acquired} gold.")
        time.sleep(2)
    pass

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
    print(f"{monster.name} has: {monster.health} [HP]")
    time.sleep(2)

# Monster Attack (Player)
def monster_attack(monster):
    print(f"{monster.name} strikes back!")
    crit_roll = random.randint(0, 100)
    monster_damage = (monster.damage + random.randint(0,monster.attack) + monster.level) - player['defense']
    if crit_roll <= monster.speed:
        monster_damage = monster_damage * 2
        print("[✴] A CRITICAL HIT! [✴]")
    if monster_damage <= 0:
        print("It deals no damage!")
    else:
        print(f"The monster deals {monster_damage} to you!")
        player['health'] -= monster_damage
    # Conditional Block Check
    if player['is_defending'] == True:
            player['is_defending'] = False
            player['defense'] -= 5
    call_vitals()
    time.sleep(1)

## DEFEND ACTION
def defend_action():
    if player['stamina'] > 0:
        player['stamina'] -= 10
        print("You block! It consumes some stamina and heals a small amount of health.")
        print(f"DEBUG: Player Current HP: {player['health']}")
        if player['health'] <= player['max_health']:
            player['health'] += player['regen'] * player['level']
            print(f"DEBUG: Player Current HP: {player['health']}")
        player['defense'] += 5
        player['is_defending'] = True
        time.sleep(2)
    else:
        print("You don't have enough stamina.")
        call_vitals()
        
## ITEM MENU        
def item_menu():
    valid_choices = ['1', '2']
    call_inventory()
    print("What item would you like to use?")
    choice = input("Command: ")
    if choice in valid_choices:
        if choice == '1' and inventory['minor_health_potions'] > 0:
            inventory['minor_health_potions'] -= 1
            player['health'] += minor_hp_value
            print(f"You heal: {minor_hp_value}")
            time.sleep(2)
        elif choice == '2' and inventory['major_health_potions'] > 0:
            inventory['major_health_potions'] -= 1
            player['health'] += major_hp_value
            print(f"You heal: {major_hp_value}")
            time.sleep(2)
        else:
            print("You either do not have enough potions or you did not use a valid input.")
    
    

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
    print(f"Level:   [{player['level']}]")
    print(f"Exp:     [{player['exp']} | {player['exp'] * 100}]")
    print(f"Stamina: {player['stamina']}/{player['max_stamina']}")
    print(f"Health:  {player['health']}/{player['max_health']}")
    print(f"Attack:  {player['attack']}")
    print(f"Defense: {player['defense']}")
    print(f"Speed:   {player['speed']}")
# End of call_stats

def call_shop():
    print("=== The Shop ===")
    mhp_for_sale = random.randint(0,3)
    mhp_value = random.randint(0,10)
    mjhp_for_sale = random.randint(0,1)
    mjhp_value = random.randint(0,10)
    valid_choices = ['1', '2', '3']
    while True:
        print(f"1. Minor HP Potions: {mhp_for_sale}")
        print(f"2. Major HP Potions: {mjhp_for_sale}")
        print("3. Done")
        print("What would you like to buy?")
        choice = input("Command: ")
        if choice in valid_choices:
            if choice == '1' and inventory['gold_coins'] > mhp_value:
                inventory['minor_health_potions'] += 1
                inventory['gold_coins'] -= mhp_value
                continue
            elif choice == '2' and inventory['gold_coins'] > mjhp_value:
                inventory['major_health_potions'] += 1
                inventory['gold_coins'] -= mjhp_value
                continue
            elif choice == '3':
                print("Done")
                time.sleep(1)
                break
            else:
                print("Not enough gold.")
                time.sleep(1)
        else:
            print("Not a valid choice.")
            time.sleep(1)
            continue
        


# Game Loop
# Summon beastiary
bestiary = populate_bestiary()
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
        available_monsters = list(bestiary.keys())
        chosen_monster_name = random.choice(available_monsters)
        monster_template = bestiary[chosen_monster_name]
        current_monster = copy.deepcopy(monster_template)
        print("A twig snaps...")
        time.sleep(1)
        print("A hurried series of steps, it's close!")
        time.sleep(1)
        print("It attacks!")
        print("= ==== =")
        print("===  ===")
        print("== == ==")
        combat_handler(current_monster)
        if player['stamina'] <= player['max_stamina']:
            player['stamina'] += player['regen'] * player['level']
        
    elif menu_choice == "2":
        call_stats()
        print("---------------------------------")
        time.sleep(3)
    elif menu_choice == "3":
        call_inventory()
        call_shop()
        time.sleep(2)
    elif menu_choice == "4":
        final_choice = input("Are you sure? Y/N")
        final_choice = final_choice.upper()
        if final_choice == "Y":
            print("Thank you for playing!")
            sys.exit()
        continue
        