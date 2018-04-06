import copy


# region Game Logic

def print_board(board):
    cutoff = 8
    text = '1D from 2D:\n'
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


def get_all_valid_moves2d(board, player_color, opponent_color):
    board_size = len(board)
    valid_moves = []
    for x in range(board_size):
        for y in range(board_size):
            if (board[x][y] == -1) and __is_correct_move2d([x, y], board, board_size, player_color, opponent_color):
                valid_moves.append((x, y))

    return valid_moves


def simulate_move(board, valid_move_vector, player_color):
    board_copy = list(board)
    if valid_move_vector:
        for field_id in valid_move_vector:
            board_copy[field_id] = player_color

    return board_copy





# endregion

# region Heuristics

def parity(state, is_max, my_col, opp_col):
    """
    Disc count difference between the two players
    :returns: 100 * (Max Player Coins - Min Player Coins ) / (Max Player Coins + Min Player Coins)
    """
    d1 = sum(row.count(my_col) for row in state)
    d2 = sum(row.count(opp_col) for row in state)
    return __get_ratio(is_max, d1, d2)


def mobility(state, is_max, my_col, opp_col):
    """
    Relative difference between # of possible moves between the two players
    :returns zero or 100 * (Max player moves - Min player moves) / (Max player moves + Min player moves)
    """
    m1 = len(get_all_valid_moves2d(state, my_col, opp_col))
    m2 = len(get_all_valid_moves2d(state, opp_col, my_col))
    if m1 + m2 != 0:
        return __get_ratio(is_max, m1, m2)
    else:
        return 0


def square_weights(state, field_values, is_max, my_col, opp_col):
    f1 = 0
    f2 = 0
    for i in range(len(state)):
        if state[i] == my_col:
            f1 += field_values[i]
        elif state[i] == opp_col:
            f2 += field_values[i]
    if f1 + f2 != 0:
        return __get_ratio(is_max, f1, f2)
    return 0


def square_weights2d(state, field_values, is_max, my_col, opp_col):
    """
    Ratio of all square weights between the two players
    :returns zero or 100 * (Max Player pts - Min Player pts) / (Max Player pts + Min Player pts)
    """
    f1 = 1
    f2 = 1
    for i in range(8):
        for j in range(8):
            if state[i][j] == my_col:
                f1 += field_values[i][j]

            elif state[i][j] == opp_col:
                f2 += field_values[i][j]

    if f1 + f2 != 0:
        return __get_ratio(is_max, f1, f2)
    return 0


def corners(state, is_max, my_col, opp_col):
    """
    Corners are valuable as they can't be captured
    :returns zero or 100 * (Max player corner count - Min player corner count) / (Max player corner count + Min player corner count)
    """
    corner_elements = [state[0][0], state[7][0], state[0][7], state[7][7]]
    c1 = len([x for x in corner_elements if x == my_col])
    c2 = len([x for x in corner_elements if x == opp_col])
    if c1 + c2 != 0:
        return __get_ratio(is_max, c1, c2)
    return 0


def edges(state, is_max, my_col, opp_col):
    """
    Edges can't be captured too
    :returns 100 * (Max player edge count - Min player edge count) / (Max player edge count + Min player edge count)
    """
    edge_elements = state[0][1:7] + \
                    state[1][0::7] + \
                    state[2][0::7] + \
                    state[3][0::7] + \
                    state[4][0::7] + \
                    state[5][0::7] + \
                    state[6][0::7] + \
                    state[7][1:7]
    e1 = len([x for x in edge_elements if x == my_col])
    e2 = len([x for x in edge_elements if x == opp_col])
    if e1 + e2 != 0:
        return __get_ratio(is_max, e1, e2)
    return 0


def __get_ratio(is_max, a, b):
    if is_max:
        return 100 * (a - b) / (a + b)
    else:
        return 100 * (b - a) / (a + b)


# endregion

# region Helpers


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


def __is_correct_move2d(move, board, board_size, player_color, opponent_color):
    dx = [-1, -1, -1, 0, 1, 1, 1, 0]
    dy = [-1, 0, 1, 1, 1, 0, -1, -1]
    for i in range(len(dx)):
        if __confirm_direction2d(move, dx[i], dy[i], board, board_size, player_color, opponent_color):
            return True
    return False


def simulate_move2d(board, move, player_color, opponent_color):
    board_copy = copy.deepcopy(board)
    board_size = len(board)
    board_copy[move[0]][move[1]] = player_color
    dx = [-1, -1, -1, 0, 1, 1, 1, 0]
    dy = [-1, 0, 1, 1, 1, 0, -1, -1]
    for i in range(len(dx)-7):
        if __confirm_direction2d(move, dx[i], dy[i], board_copy, board_size, player_color, opponent_color):
            __change_stones_in_direction(move, dx[i], dy[i], board_copy, player_color)
    return board_copy


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


def __confirm_direction2d(move, dx, dy, board, board_size, player_color, opponent_color):
    posx = move[0] + dx
    posy = move[1] + dy
    if (posx >= 0) and (posx < board_size) and (posy >= 0) and (posy < board_size):
        if board[posx][posy] == opponent_color:
            while (posx >= 0) and (posx <= (board_size - 1)) and (posy >= 0) and (posy <= (board_size - 1)):
                posx += dx
                posy += dy
                if (posx >= 0) and (posx < board_size) and (posy >= 0) and (posy < board_size):
                    if board[posx][posy] == -1:
                        return False
                    if board[posx][posy] == player_color:
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
