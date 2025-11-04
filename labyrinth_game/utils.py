import random
import time

from labyrinth_game.constants import ROOMS


# Attention! For debug you can set delay to zero, it will work like a regular print
# I made this funcction esthetic reasons
def stupid_print(text="", delay=0.02, end="\n"):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay+(random.random()-0.5)*delay)
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
