

class MyPlayer(object):
    """
    Docstring for MyPlayer
    """

    def __init__(self, my_color, opponent_color):
        self.name = 'izotomas'
        self.my_color = my_color
        self.opponent_color = opponent_color

    def move(self, board):
        board_size = len(board)
        possible = []
        for x in range(board_size):
            for y in range(board_size):
                if (board[x][y] == -1) and self.__is_correct_move([x, y], board, board_size):
                    possible.append((x, y))

        possible_moves = len(possible) - 1
        if possible_moves < 0:
            print('No possible move!')
            return None
        my_move = 0
        return possible[my_move]

    def __is_correct_move(self, move, board, board_size):
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.__confirm_direction(move, dx[i], dy[i], board, board_size):
                return True
        return False

    def __confirm_direction(self, move, dx, dy, board, board_size):
        posx = move[0]+dx
        posy = move[1]+dy
        if (posx >= 0) and (posx < board_size) and (posy >= 0) and (posy < board_size):
            if board[posx][posy] == self.opponent_color:
                while (posx >= 0) and (posx <= (board_size-1)) and (posy >= 0) and (posy <= (board_size-1)):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < board_size) and (posy >= 0) and (posy < board_size):
                        if board[posx][posy] == -1:
                            return False
                        if board[posx][posy] == self.my_color:
                            return True

        return False

    def get_all_valid_moves(self, board):
        board_size = len(board)
        valid_moves = []
        for x in range(board_size):
            for y in range(board_size):
                if (board[x][y] == -1) and self.__is_correct_move([x, y], board, board_size):
                    valid_moves.append((x, y))

        if len(valid_moves) <= 0:
            print('No possible move!')
            return None
        return valid_moves
