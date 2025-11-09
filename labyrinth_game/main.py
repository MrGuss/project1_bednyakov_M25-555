#!/usr/bin/env python3

from .constants import COMMANDS
from .player_actions import get_input, move_player, show_inventory, take_item, use_item
from .utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle, stupid_print

game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0  # Количество шагов
}


def process_command(game_state, command):
    tool, *args = command.split()
    match tool:
        case 'quit':
            game_state['game_over'] = True
        case 'inventory':
            show_inventory(game_state)
        case 'go':
            if len(args) != 1:
                stupid_print("go принимает один аргумент: go <направление>.")
                return
            move_player(game_state, args[0].lower())
        case 'north':
            move_player(game_state, 'north')
        case 'south':
            move_player(game_state, 'south')
        case 'east':
            move_player(game_state, 'east')
        case 'west':
            move_player(game_state, 'west')
        case 'take':
            if len(args) != 1:
                stupid_print("take принимает один аргумент: take <название предмета>.")
                return
            take_item(game_state, args[0].lower())
        case 'use':
            if len(args) != 1:
                stupid_print("use принимает один аргумент: use <название предмета>.")
                return
            use_item(game_state, args[0].lower())
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case 'look':
            describe_current_room(game_state)
        case 'help':
            show_help(COMMANDS)
        case _:
            stupid_print("Непонятная команда.")


def main():
    stupid_print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    while not game_state['game_over']:
        player_input = get_input()
        process_command(game_state, player_input)

    stupid_print("Спасибо за игру!")


if __name__ == "__main__":
    main()
