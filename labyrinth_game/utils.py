from math import sin

from labyrinth_game.constants import EVENT_PROBABILITY, KIND_PROBABILITY, ROOMS


def describe_current_room(game_state):
    cur_room = game_state['current_room']
    print(f"*** {cur_room.upper()} ***", end='\n\n')
    print(ROOMS[cur_room]['description'], end="\n\n")
    if ROOMS[cur_room]['items']:
        print("Заметные предметы:")
        for item in ROOMS[cur_room]['items']:
            print(f"- {item}")
    if ROOMS[cur_room]['exits']:
        print("Выходы:")
        for exit in ROOMS[cur_room]['exits']:
            print(f"- {exit}")
    if ROOMS[cur_room]['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")
    print(f"*** {cur_room.upper()} ***", end='\n\n')


def solve_puzzle(game_state):
    cur_room = ROOMS[game_state['current_room']]
    if game_state['current_room'] == 'treasure_room':
        attempt_open_treasure(game_state)
        return

    if not cur_room['puzzle']:
        print("Загадок здесь нет.")
        return
    print(cur_room['puzzle'][0])
    print("Ваш ответ: ", end="")
    answer = input().lower()
    if answer in cur_room['puzzle'][1]:
        print("Успех!")
        game_state['player_inventory'].append(cur_room['puzzle'][2])
        cur_room['puzzle'] = None
    else:
        print("Неверно. Попробуйте снова.")
        if game_state['current_room'] == 'trap_room':
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        ROOMS['treasure_room']['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    if 'treasure_key' not in game_state['player_inventory']:
        print("Сундук заперт. ... Ввести код? (да/не)", end="")
        answer = input().lower()
        if answer == 'да':
            print("Подсказка:")
            print(ROOMS['treasure_room']['puzzle'][0])
            print("Код: ", end="")
            code = input()
            if code == '10':
                print("Код верный. Сундук открыт!")
                ROOMS['treasure_room']['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Код неверный. Вы отступаете от сундука.")


def show_help(commands):
    print("\nДоступные команды:")
    for command in commands:
        print(f"{command:<16} {commands[command]}")


def pseudo_random(seed, modulo):
    return int(sin(seed*13.776) * 234.123 % 1 * modulo)


def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    if len(game_state['player_inventory']) == 0:
        damag = pseudo_random(game_state['steps_taken'], 9)
        if damag < 3:
            print("Вы умерли!")
            game_state['game_over'] = True
        else:
            print("На сей раз вам удалось избежать смерти...")
        return

    random_index = pseudo_random(game_state['steps_taken'], len(game_state['player_inventory'])-1)
    item = game_state['player_inventory'].pop(random_index)
    print(f"Вы потеряли {item}!")


def random_event(game_state):
    # TODO: Adjust random events
    chance = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
    if chance <= 4:
        kind = pseudo_random(game_state['steps_taken'], KIND_PROBABILITY)
        if kind == 0:
            print("Вы увидели на полу монетку.")
            ROOMS[game_state['current_room']]['items'].append('coin')
        if kind == 1:
            print("Вы слышите шорох в углу комнаты.")
            if 'sword' in game_state['player_inventory']:
                print("Вы отпугнули монстра мечем.")
        if kind > 1:
            if game_state['current_room'] == 'trap_room' and 'torch' not in game_state['player_inventory']:
                trigger_trap(game_state)
