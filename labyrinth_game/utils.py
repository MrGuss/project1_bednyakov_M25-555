import time
from math import sin

from labyrinth_game.constants import ROOMS


# Attention! For debug you can set delay to zero, it will work like a regular print
# I made this function for aesthetic reasons
def stupid_print(text="", delay=0.02, end="\n"):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print(end=end)


def describe_current_room(game_state):
    cur_room = game_state['current_room']
    stupid_print(f"*** {cur_room.upper()} ***", end='\n\n')
    stupid_print(ROOMS[cur_room]['description'], end="\n\n")
    if ROOMS[cur_room]['items']:
        stupid_print("Заметные прдметы:")
        for item in ROOMS[cur_room]['items']:
            stupid_print(f"- {item}")
    if ROOMS[cur_room]['exits']:
        stupid_print("Выходы:")
        for exit in ROOMS[cur_room]['exits']:
            stupid_print(f"- {exit}")
    if ROOMS[cur_room]['puzzle']:
        stupid_print("Кажется, здесь есть загадка (используйте команду solve).")
    stupid_print(f"*** {cur_room.upper()} ***", end='\n\n')


def solve_puzzle(game_state):
    cur_room = ROOMS[game_state['current_room']]
    if game_state['current_room'] == 'treasure_room':
        attempt_open_treasure(game_state)
        return

    if not cur_room['puzzle']:
        stupid_print("Загадок здесь нет.")
        return
    stupid_print(cur_room['puzzle'][0])
    stupid_print("Ваш ответ: ", end="")
    answer = input().lower()
    if answer == cur_room['puzzle'][1]:
        stupid_print("Успех!")
        game_state['player_inventory'].append(cur_room['puzzle'][2])
        cur_room['puzzle'] = None
    else:
        stupid_print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    if 'treasure_key' in game_state['player_inventory']:
        stupid_print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        ROOMS['treasure_room']['items'].remove('treasure_chest')
        stupid_print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    if 'treasure_key' not in game_state['player_inventory']:
        stupid_print("Сундук заперт. ... Ввести код? (да/не)", end="")
        answer = input().lower()
        if answer == 'да':
            stupid_print("Подсказка:")
            stupid_print(ROOMS['treasure_room']['puzzle'][0])
            stupid_print("Код: ", end="")
            code = input()
            if code == '10':
                stupid_print("Код верный. Сундук открыт!")
                ROOMS['treasure_room']['items'].remove('treasure_chest')
                stupid_print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                stupid_print("Код неверный. Вы отступаете от сундука.")


def show_help():
    stupid_print("\nДоступные команды:")
    stupid_print("  go <direction>  - перейти в направлении (north/south/east/west)")
    stupid_print("  look            - осмотреть текущую комнату")
    stupid_print("  take <item>     - поднять предмет")
    stupid_print("  use <item>      - использовать предмет из инвентаря")
    stupid_print("  inventory       - показать инвентарь")
    stupid_print("  solve           - попытаться решить загадку в комнате")
    stupid_print("  quit            - выйти из игры")
    stupid_print("  help            - показать это сообщение")


def pseudo_random(seed, modulo):
    return int(sin(seed*13.776) * 234.123 % 1 * modulo)


def trigger_trap(game_state):
    stupid_print("Ловушка активирована! Пол стал дрожать...")
    if len(game_state['inventory']) == 0:
        damag = pseudo_random(game_state['steps_taken'], 9)
        if damag < 3:
            stupid_print("Вы умерли!")
            game_state['game_over'] = True
        else:
            stupid_print("На сей раз вам удалось избежать смерти...")
        return

    random_index = pseudo_random(game_state['steps_taken'], len(game_state['inventory'])-1)
    item = game_state['inventory'].pop(random_index)
    stupid_print(f"Вы потеряли {item}!")


def random_event(game_state):
    chance = pseudo_random(game_state['steps_taken'], 10)
    if chance == 0:
        kind = pseudo_random(game_state['steps_taken'], 2)
        if kind == 0:
            stupid_print("Вы увидели на полу монетку.")
            ROOMS[game_state['current_room']]['items'].append('coin')
        if kind == 1:
            stupid_print("Вы слышите шорох в углу комнаты.")
            if 'sword' in game_state['inventory']:
                stupid_print("Вы отпугнули монстра мечем.")
        if kind == 2:
            if game_state['current_room'] == 'trap_room' and 'torch' not in game_state['inventory']:
                trigger_trap(game_state)
