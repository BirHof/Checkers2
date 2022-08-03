import checkers_utiles


def inspection_runner(file_path=None, board_state=None, print_board=True):
    with open(file_path, "r") as file:
        moves = [[int(x) for x in line.split(',')] for line in file]

    # ************   Start Game   ************
    if print_board:
        print("\nBoard initial state:")
        checkers_utiles.print_board_state(board_state)

    player = 1
    x_next_start = None
    y_next_start = None
    Illegality_found = False

    for idx, move in enumerate(moves):
        print(f'Move {idx + 1}: {move}')
        x0, y0, x1, y1 = move

        # Check if player apply multiple captures:
        if x_next_start is not None:
            if x0 != x_next_start or y0 != y_next_start:
                print(f"line {idx + 1} illegal move: {move}")
                print(f"You must apply multiple captures")
                Illegality_found = True
                break
        # Check move validity (basic conditions):
        move_validate, message = checkers_utiles.validate_move_basic_conditions(player, move, board_state)
        if not move_validate:
            print(f"\nline {idx + 1} illegal move: {move}")
            print(message)
            Illegality_found = True
            break

        # if it is a move with capture:
        if abs(x1-x0) == 2 or abs(y1-y0) == 2:
            print("capture move")
            # is capture legal?
            if checkers_utiles.validate_single_capture(player, x0, y0, x1, y1, board_state) is False:
                print(f"line {idx + 1} illegal move: {move}")
                print('Capture move is not valid')
                Illegality_found = True
                break

            # apply move:
            board_state = checkers_utiles.apply_single_step(board_state, move, is_capture=True)

            # Check if multiple-capture
            if checkers_utiles.is_additional_capture(player=player, x0=x1, y0=y1, board_state=board_state):
                print("Multiple capture starts here")
                x_next_start = x1
                y_next_start = y1
            else:
                player = -1 * player
                x_next_start = None
                y_next_start = None

        else:   # move without capture:
            print("Simple move")
            # Map capturing potential for all stones:
            potential_map, LL_matrix = checkers_utiles.potential_mapping(player, board_state=board_state)
            # if you or another stone can capture
            if max(max(potential_map)) != 0:
                print(f"line {idx + 1} illegal move: {move}")
                print(f'{checkers_utiles.players[player]} player can make a capture move/s and he did not')
                Illegality_found = True
                break

            # apply move:
            board_state = checkers_utiles.apply_single_step(board_state, move, is_capture=False)
            player = -1 * player
            x_next_start = None
            y_next_start = None

        if print_board:
            checkers_utiles.print_board_state(board_state)
    # ************   End of Game   ************

    # check if game is complete
    if not Illegality_found:
        is_game_complete, message = checkers_utiles.is_game_complete(board_state, player)
        if is_game_complete:
            print("\nGame is complete :)")
        else:
            print("\nGame is NOT complete !!!", '  ', message)

    # Declare the Winner
    if (not Illegality_found) and is_game_complete:
        balance = sum(sum(board_state, []))
        if balance > 0:
            print("White player WIN !!!")
        if balance < 0:
            print("Black player WIN !!!")
        if balance == 0:
            print("Game END in a TIE")


if __name__ == '__main__':
    board_state_initial = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-1, 0, -1, 0, -1, 0, -1, 0],
        [0, -1, 0, -1, 0, -1, 0, -1],
        [-1, 0, -1, 0, -1, 0, -1, 0],
    ]
    files = ["white.txt", "black.txt", "illegal_move.txt", "incomplete.txt", "test.txt"]
    inspection_runner(file_path=files[4], board_state=board_state_initial, print_board=True)
