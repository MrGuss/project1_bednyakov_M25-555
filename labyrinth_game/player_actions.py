from .constants import ROOMS
from .utils import random_event


def show_inventory(game_state):
    """Takes game_state and prints the player's inventory."""
    print("Ваш инвентарь:")
    if len(game_state['player_inventory']) == 0:
        print("  Пусто")
    for item in game_state['player_inventory']:
        print(f"- {item}")
    print()


def get_input(prompt="> "):
    """Prompts the user input and returns it."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """Moves the player in the specified direction if possible, applying random events along the way."""
    cur_room = ROOMS[game_state['current_room']]
    if direction in cur_room['exits']:
        if cur_room['exits'][direction] == 'treasure_room':
            if 'rusty_key' not in game_state['player_inventory']:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return
            print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
        game_state['current_room'] = cur_room['exits'][direction]
        game_state['steps_taken'] += 1
        random_event(game_state)
    else:
        print("Вы не можете двигаться в этом направлении.")


def take_item(game_state, item_name):
    """Takes an item from the current room and adds it to the player's inventory if possible."""
    cur_room = ROOMS[game_state['current_room']]
    if item_name in cur_room['items']:
        if item_name == 'treasure_chest':
            print("Вы не можете поднять сундук, он слишком тяжелый.")
            return
        game_state['player_inventory'].append(item_name)
        cur_room['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """Uses an item from the player's inventory if possible."""
    if item_name in game_state['player_inventory']:
        match item_name:
            case 'torch':
                print("Комната вокруг озаряется светом факела.")
            case 'sword':
                print("Ощущая рукоять меча вы наполняетесь решимостью.")
            case 'bronze_box':
                game_state['player_inventory'].remove('bronze_box')
                print("Вам удалось открыть шкатулку. В ней лежит ключ.")
                game_state['player_inventory'].append('rusty_key')
            case _:
                print("Не могу использовать этот предмет.")
    else:
        print("У вас нет такого предмета.")
