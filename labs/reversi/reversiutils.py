import copy


# region Game Logic

def print_board(board):
    cutoff = 8
    text = ''
    for i in range(len(board)):
        if board[i] == -1:
            text += ' -'
        else:
            text += ' ' + str(board[i])
        if (i + 1) % cutoff == 0:
            text += '\n'
    print(text)


def get_all_valid_moves(board, player_color, opponent_color):
    board_size = len(board)
    valid_moves = []

    for move in range(board_size):
        move_vector = __get_move_vector(move, board, player_color, opponent_color)
        if move_vector:
            valid_moves.append(move_vector)

    return valid_moves


def simulate_move(board, valid_move_vector, player_color):
    board_copy = copy.deepcopy(board)
    if valid_move_vector:
        for field_id in valid_move_vector:
            board_copy[field_id] = player_color

    return board_copy


def flatten(board):
    return [j for i in board for j in i]


def index_to_cartesian(index):
    dimension = 8
    row = index // dimension
    col = index % dimension
    return [row, col]


def cartesian_to_index(coordinates):
    dimension = 8
    index = dimension * coordinates[0]
    index += coordinates[1]
    return index


# endregion

# region Heuristics


def utility(node):
    return parity(node)


def parity(node):
    """
    Disc count difference between the two players
    :returns: 100 * (Max Player Coins - Min Player Coins ) / (Max Player Coins + Min Player Coins)
    """
    d1 = node.board.count(node.my_color)
    d2 = node.board.count(node.opponent_color)
    return __get_ratio(node.is_max_node, d1, d2)


def mobility(node):
    """
    Relative difference between # of possible moves between the two players
    :returns zero or 100 * (Max player moves - Min player moves) / (Max player moves + Min player moves)
    """
    m1 = len(get_all_valid_moves(node.board, node.my_color, node.opponent_color))
    m2 = len(get_all_valid_moves(node.board, node.opponent_color, node.my_color))
    return __get_ratio(node.is_max_node, m1, m2)


def positional_strength(node, positional_heuristics):

    s1 = 0
    s2 = 0
    for i in range(len(node.board)):
        if node.board[i] == node.my_color:
            s1 += positional_heuristics[i]
        elif node.board[i] == node.opponent_color:
            s2 += positional_heuristics[i]
    return __get_ratio(node.is_max_node, s1, s2)


def corners(node):
    """
    Corners are valuable as they can't be captured
    :returns zero or 100 * (Max player corner count - Min player corner count) / (Max player corner count + Min player corner count)
    """
    corner_elements = [node.board[0], node.board[7], node.board[56], node.board[63]]
    c1 = corner_elements.count(node.my_color)
    c2 = corner_elements.count(node.opponent_color)
    return __get_ratio(node.is_max_node, c1, c2)


def __get_ratio(is_max, a, b):
    if a + b == 0:
        return 0
    if is_max:
        return 100 * (a - b) / (a + b)
    else:
        return 100 * (b - a) / (a + b)


# endregion

# region Helpers


def __get_move_vector(move, board, player_color, opponent_color):
    # is field free
    if board[move] != -1:
        return None
    di = [7, -1, -9, -8, -7, 1, 9, 8]
    for i in range(len(di)):
        fields = __get_fields_to_change(move, di[i], board, player_color, opponent_color)
        if fields:
            return fields
    return []


def __change_stones_in_direction(move, dx, dy, board, players_color):
    posx = move[0] + dx
    posy = move[1] + dy
    while not (board[posx][posy] == players_color):
        board[posx][posy] = players_color
        posx += dx
        posy += dy
    return board


def __get_fields_to_change(move, di, board, player_color, opponent_color):
    fields_to_change = [move]
    if board[move] != -1:
        return False
    board_len = len(board)
    pos = move + di
    if 0 <= pos < board_len:
        if board[pos] == opponent_color:
            fields_to_change.append(pos)
            while __is_search_in_bounds(pos, di, board_len):
                # print("looking at %s" % index_to_cartesian(pos))
                pos += di
                fields_to_change.append(pos)
                if __is_search_in_bounds(pos, di, board_len):
                    if board[pos] == -1:
                        # print("error at field %s " % index_to_cartesian(pos))
                        return []
                    if board[pos] == player_color:
                        # print("Field %s can move to %s" % (index_to_cartesian(pos), index_to_cartesian(move)))
                        return fields_to_change

    # print("P1: move to %s not possible" % index_to_cartesian(move))
    return []


def __is_search_in_bounds(position, direction, board_len):
    if 0 <= position < board_len:
        # going east
        if direction in (-7, 1, 9):
            return position % 8 != 0
        # going west
        if direction in (7, -1, -9):
            return position % 8 != 7
        if direction in (-8, 8):
            return True
    return False

# endregion

#
# if __name__ == "__main__":
#     board = [-1, -1, -1, -1, -1, -1, -1, -1,
#              -1,  1,  0,  0, -1, -1, -1,  1,
#               0, -1, -1, -1, -1, -1, -1, -1,
#              -1, -1, -1,  0,  1, -1, -1, -1,
#              -1,  1,  0,  0,  0, -1, -1, -1,
#              -1, -1,  0, -1, -1, -1, -1,  1,
#               1,  0, -1, -1, -1, -1,  0,  0,
#              -1, -1, -1, -1, -1, -1, -1, -1]
#     __confirm_direction(cartesian_to_index([7, 6]), -7, board, 1, 0)
#     __confirm_direction(cartesian_to_index([7, 0]), -7, board, 1, 0)
#     __confirm_direction(cartesian_to_index([7, 5]), -7, board, 1, 0)
#
#     print("test horizontal move")
#     __confirm_direction(cartesian_to_index([6, 2]), -1, board, 1, 0)
#     __confirm_direction(cartesian_to_index([2, 1]), -1, board, 1, 0)
#     __confirm_direction(cartesian_to_index([1, 4]), -1, board, 1, 0)
#
#     print("test south-west move")
#     __confirm_direction(cartesian_to_index([6, 3]), -9, board, 1, 0)
#     __confirm_direction(cartesian_to_index([3, 1]), -9, board, 1, 0)
#
#     print("test north/south move")
#     __confirm_direction(cartesian_to_index([5, 4]), -8, board, 1, 0)
