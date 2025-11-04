from .constants import ROOMS
from .utils import random_event, stupid_print


def show_inventory(game_state):
    stupid_print("Ваш инвентарь:")
    if len(game_state['player_inventory']) == 0:
        stupid_print("  Пусто")
    for item in game_state['player_inventory']:
        stupid_print(f"- {item}")
    stupid_print()


def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        stupid_print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    cur_room = ROOMS[game_state['current_room']]
    if direction in cur_room['exits']:
        game_state['current_room'] = cur_room['exits'][direction]
        game_state['steps_taken'] += 1
        random_event(game_state)
    else:
        stupid_print("Вы не можете двигаться в этом направлении.")


def take_item(game_state, item_name):
    cur_room = ROOMS[game_state['current_room']]
    if item_name in cur_room['items']:
        if item_name == 'treasure_chest':
            stupid_print("Вы не можете поднять сундук, он слишком тяжелый.")
            return
        game_state['player_inventory'].append(item_name)
        cur_room['items'].remove(item_name)
        stupid_print(f"Вы подняли: {item_name}")
    else:
        stupid_print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    if item_name in game_state['player_inventory']:
        match item_name:
            case 'torch':
                stupid_print("Комната вокруг озаряется светом факела.")
            case 'sword':
                stupid_print("Ощущая рукоять меча вы наполняетесь решимостью.")
            case 'bronze_box':
                stupid_print("Вам удалось открыть шкатулку. В ней лежит ключ.")
                game_state['player_inventory'].append('rusty_key')
            case _:
                stupid_print("Не могу использовать этот предмет.")
    else:
        stupid_print("У вас нет такого предмета.")
