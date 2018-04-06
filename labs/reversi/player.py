from node import Node
import reversiutils as ru
import time


class MyPlayer(object):
    """
    Uses MiniMax with alpha-beta pruning for the first 0.5 sec heuristic evaluation afterwards
    """

    MAX_WAITING_TIME = 0.5
    # weights for heuristic evaluation
    SQUARE_WEIGHTS = [
         200, -100, 100,  50,  50, 100, -100,  200,
        -100, -200, -50, -50, -50, -50, -200, -100,
         100,  -50, 100,   0,   0, 100,  -50,  100,
          50,  -50,   0,   0,   0,   0,  -50,   50,
          50,  -50,   0,   0,   0,   0,  -50,   50,
         100,  -50, 100,   0,   0, 100,  -50,  100,
        -100, -200, -50, -50, -50, -50, -200, -100,
         200, -100, 100,  50,  50, 100, -100,  200,
        ]

    def __init__(self, my_color, opponent_color):
        self.name = 'izotomas'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.start_time = 0

    def move(self, board):
        board1d = ru.flatten(board)
        root = Node(board1d, self.my_color, self.opponent_color)
        self.start_time = time.time()
        root.children = root.get_children()
        if not root.children:
            return None
        best_move = self.__alpha_beta_search(root)
        return best_move

    # region Helpers

    def __alpha_beta_search(self, node):
        self.__max_value(node, Node.DEFAULT_SCORE, Node.DEFAULT_SCORE * (-1))
        best_node = max(node.children)
        coordinates = ru.index_to_cartesian(best_node.move)
        return coordinates

    def __max_value(self, node, alpha, beta):
        node.children = node.get_children()
        if self.__is_terminal_state(node):
            return self.__evaluate(node)
        for child in node.children:
            node.score = max(node.score, self.__min_value(child, alpha, beta))
            if node.score >= beta:
                return node.score
            alpha = max(alpha, node.score)
        return node.score

    def __min_value(self, node, alpha, beta):
        node.children = node.get_children()
        if self.__is_terminal_state(node):
            return self.__evaluate(node)
        for child in node.children:
            node.score = min(node.score, self.__max_value(child, alpha, beta))
            if node.score <= alpha:
                return node.score
            beta = min(beta, node.score)
        return node.score

    def __is_terminal_state(self, node):
        move_time = (time.time() - self.start_time)
        time_expired = move_time > MyPlayer.MAX_WAITING_TIME
        no_children = not node.children
        return time_expired or no_children

    @staticmethod
    def __evaluate(node):
        free_position_count = node.board.count(-1)
        if not node.children or free_position_count == 0:
            return ru.utility(node) * 10000

        if free_position_count > 45:
            return ru.mobility(node) + \
                  4 * ru.positional_strength(node, MyPlayer.SQUARE_WEIGHTS) + \
                  100 * ru.corners(node)

        if free_position_count > 30:
            return 10 * ru.parity(node) + \
                   5 * ru.mobility(node) + \
                   10 * ru.positional_strength(node, MyPlayer.SQUARE_WEIGHTS) + \
                   100 * ru.corners(node)

        else:
            return 500 * ru.parity(node) + \
                   1000 * ru.positional_strength(node, MyPlayer.SQUARE_WEIGHTS) + \
                   1000 * ru.corners(node)

    # endregion
