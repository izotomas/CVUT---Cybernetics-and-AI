from random import randint


class MyPlayer(object):
    """
    Random reversi player class.
    """
   
    def __init__(self, my_color, opponent_color):
        self.name = 'random'
        self.my_color = my_color
        self.opponentColor = opponent_color
        self.moveCount = 1
        print('Random player created')
        
    def move(self, board):
        board_size = len(board)
        possible = []
        for x in range(board_size):
            for y in range(board_size):
                if (board[x][y] == -1) and self.is_correct_move([x, y], board, board_size):
                    possible.append((x, y))

        possible_moves = len(possible)-1
        if possible_moves < 0:
            print('No possible move!')
            return None
        my_move = randint(0, possible_moves)
        return possible[my_move]

    def is_correct_move(self, move, board, board_size):
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.confirm_direction(move, dx[i], dy[i], board, board_size):
                return True
        return False

    def confirm_direction(self, move, dx, dy, board, board_size):
        posx = move[0]+dx
        posy = move[1]+dy
        if (posx >= 0) and (posx < board_size) and (posy >= 0) and (posy < board_size):
            if board[posx][posy] == self.opponentColor:
                while (posx >= 0) and (posx <= (board_size-1)) and (posy >= 0) and (posy <= (board_size-1)):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < board_size) and (posy >= 0) and (posy < board_size):
                        if board[posx][posy] == -1:
                            return False
                        if board[posx][posy] == self.my_color:
                            return True

        return False
