import binary_tree


board_BW = [
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
]

players = ['', 'White', 'Black']


def print_board_state(board_state):
    visualized_board = [["   "] * 8 for _ in range(8)]
    for line_idx, line in enumerate(board_BW):
        for item_idx, item in enumerate(line):
            if item == 1:
                visualized_board[line_idx][item_idx] = "___"

    for x in range(8):
        for y in range(8):
            if board_state[y][x] == 1:
                visualized_board[y][x] = '_W_'
            elif board_state[y][x] == -1:
                visualized_board[y][x] = '_B_'

    for idx, line in enumerate(reversed(visualized_board)):
        print(line[::-1], '  ', str(7-idx))
        print('')
    print('   7      6      5      4      3      2      1      0    X  Y')
    print('')


def validate_move_basic_conditions(player, move, board_state):
    """
    player = 1 for white / -1 for black

    return True if (all conditions are met):
        1. Both source and target indexes are inside board boundaries [0,7].
        2. Both source and target boxes are dark.
        3. Stone exist in source position.
        4. move turn match the player color: white- even, black- odd.
        5. Player move forward.
        6. Player move diagonally.
        7. player not moving more than 2 boxes.
        8. Target box is empty.
    """
    x0, y0, x1, y1 = move
    if True in [idx < 0 or idx > 7 for idx in move]:
        message = 'Index exceed board boundaries'
        return False, message
    if board_BW[y0][x0] == 0 or board_BW[y1][x1] == 0:
        message = 'Stones shall be on a dark box only'
        return False, message
    if board_state[y0][x0] == 0:
        message = "Source box is empty"
        return False, message
    if board_state[y0][x0] != player:
        message = "Wrong player in source box"
        return False, message
    if player*(y1-y0) <= 0:
        message = players[player] + " player was not moving forward"
        return False, message
    if abs(y1-y0) != abs(x1-x0):
        message = players[player] + " player was not moving diagonally"
        return False, message
    if player*(y1-y0) > 2:
        message = players[player] + " player was moving to far"
        return False, message
    if board_state[y1][x1] != 0:
        message = "Target box is occupied"
        return False, message

    return True, "OK. move meet basic conditions"


def validate_single_capture(player, x0, y0, x1, y1, board_state):
    # Board boundaries:
    if x1 > 7 or y1 > 7 or x1 < 0 or y1 < 0:
        return False
    # Box is not dark:
    if board_BW[y1][x1] != 1:
        return False
    # Box is not empty:
    if board_state[y1][x1] != 0:
        return False
    # there is no opponent to eat:
    if board_state[int((y0+y1)/2)][int((x0+x1)/2)] != (-1)*player:
        return False

    return True


    return True


def is_additional_capture(player, x0, y0, board_state):
    # Check to the left:
    x1 = x0 + 2 * player
    y1 = y0 + 2 * player
    left = validate_single_capture(player=player, x0=x0, y0=y0, x1=x1, y1=y1, board_state=board_state)

    # Check to the right:
    x1 = x0 - 2 * player
    y1 = y0 + 2 * player
    right = validate_single_capture(player=player, x0=x0, y0=y0, x1=x1, y1=y1, board_state=board_state)
    if left or right:
        return True
    else:
        return False


def chain_all_optional_captures(node, player, board_state):
    """
    this function: chain nodes(board boxes) to form all optional captures binary tree
    """
    # chain to the left:
    x1 = node.x + 2 * player
    y1 = node.y + 2 * player
    if validate_single_capture(player=player, x0=node.x, y0=node.y, x1=x1, y1=y1, board_state=board_state):
        new_node = binary_tree.Node(x=x1, y=y1)
        node.left = new_node
        chain_all_optional_captures(node=new_node, player=player, board_state=board_state)

    # chain to the right:
    x1 = node.x - 2 * player
    y1 = node.y + 2 * player
    if validate_single_capture(player=player, x0=node.x, y0=node.y, x1=x1, y1=y1, board_state=board_state):
        new_node = binary_tree.Node(x=x1, y=y1)
        node.right = new_node
        chain_all_optional_captures(node=new_node, player=player, board_state=board_state)


def potential_mapping(player, board_state=None):
    potential_map = [[0] * 8 for _ in range(8)]
    LL_matrix = [[None] * 8 for _ in range(8)]
    for y in range(8):
        for x in range(8):
            if board_state[y][x] == player:
                potential_tree = binary_tree.BinaryTree(x=x, y=y)
                chain_all_optional_captures(potential_tree.root, player=player, board_state=board_state)
                LL_matrix[y][x] = potential_tree
                potential_map[y][x] = potential_tree.maxDepth(potential_tree.root)

    return potential_map, LL_matrix


def apply_single_step(board_state, move, is_capture):
    x0, y0, x1, y1 = move
    # Update target:
    board_state[y1][x1] = board_state[y0][x0]
    # Update target:
    board_state[y0][x0] = 0
    # if captured, remove stone from board:
    if is_capture:
        board_state[int((y0+y1)/2)][int((x0+x1)/2)] = 0

    return board_state


def apply_multiple_steps(board_state, move, origin_tree):
    x0, y0, x1, y1 = move
    """
    This function apply apply multiple steps (when capture)
    :return: "True" if all correct 
    :return: The final state of the board 
    """
    # make sure if target is a leaf (capture is fully made):
    ans = origin_tree.nodesToTargetLeaf(origin_tree.root, x1, y1)
    if ans is False:
        return False, board_state
    else:
        current_node = origin_tree.root
        while current_node.next:
            #print(f"node   X,Y = {current_node.x},{current_node.y}")
            move = [current_node.x, current_node.y, current_node.next.x, current_node.next.y]
            board_state = apply_single_step(board_state, move, is_capture=True)
            current_node = current_node.next
        return True, board_state


def simple_move_exist(board_state, player):
    for y0, row in enumerate(board_state):
        for x0, item in enumerate(row):
            if item == player:

                # Check to the left:
                x1 = x0 + 2 * player
                y1 = y0 + 2 * player
                move = [x0, y0, x1, y1]
                if validate_move_basic_conditions(player=player, move=move, board_state=board_state):
                    return True

                # Check to the right:
                x1 = x0 - 2 * player
                y1 = y0 + 2 * player
                move = [x0, y0, x1, y1]
                if validate_move_basic_conditions(player=player, move=move, board_state=board_state):
                    return True
    return False


def is_game_complete(board_state, player):
    # is player present on the board?
    if not any(player in sublist for sublist in board_state):
        message = players[player] + ' player is absence from the the board'
        return True, message

    # is player has additional capture move to make?
    potential_map, _ = potential_mapping(player=player, board_state=board_state)
    if max(max(potential_map)) != 0:
        message = players[player] + ' plater has an optional captures to make'
        return False, message

    # is player has additional simple moves to make?
    if simple_move_exist(board_state, player):
        message = players[player] + ' plater has an optional simple move to make'
        return False, message

    return True, "Bye"


if __name__ == '__main__':
    state_1 = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-1, 0, -1, 0, -1, 0, -1, 0],
        [0, -1, 0, -1, 0, -1, 0, -1],
        [-1, 0, -1, 0, -1, 0, -1, 0],
    ]
    print(validate_single_capture(player=1, x0=1, y0=2, x1=3, y1=4, board_state=state_1))

    state_2 = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, -1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, -1, 0, 0, 0, 0],
        [-1, 0, -1, 0, -1, 0, -1, 0],
        [0, -1, 0, 0, 0, -1, 0, 0],
        [-1, 0, -1, 0, -1, 0, -1, 0],
    ]

    tree = binary_tree.BinaryTree(x=3, y=2)
    #tree = binary_tree.BinaryTree(x=0, y=0)
    chain_all_optional_captures(tree.root, player=1, board_state=state_2)

    ind_x = 3
    ind_y = 6
    print(f"is x={ind_x} y={ind_y} in Leaf? {tree.isIndexInLeaf(tree.root, ind_x, ind_y)}")

    tree_depth = tree.maxDepth(tree.root)
    print(f"Max depth: {tree_depth}")

    ans = tree.nodesToTargetLeaf(tree.root, ind_x, ind_y)

    board_state = state_2
    while_node = tree.root
    print(f"origin node   X,Y = {while_node.x},{while_node.y}")
    while while_node.next:
        print(f"move to node   X,Y = {while_node.next.x},{while_node.next.y}")
        move = [while_node.x, while_node.y, while_node.next.x, while_node.next.y]
        board_state = apply_single_step(board_state, move, is_capture=True)
        while_node = while_node.next
