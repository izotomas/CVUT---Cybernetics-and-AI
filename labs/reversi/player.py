from node import Node
import reversiutils
import time


class MyPlayer(object):
    """
    Uses alfa-beta pruning, and heuristic function based on sum of field evaluation if tree lookup takes longer than
    max allowed waiting time
    """

    MAX_WAITING_TIME = 0.85
    # heuristics weights
    """SQUARE_WEIGHTS = [
        [99, -8, 8, 6, 6, 8, -8, 99],
        [-8, -24, -4, -3, -3, -4, -24, -8],
        [8, -4, 7, 4, 4, 7, -4, 8],
        [6, -3, 4, 0, 0, 4, -3, 6],
        [6, -3, 4, 0, 0, 4, -3, 6],
        [8, -4, 7, 4, 4, 7, -4, 8],
        [-8, -24, -4, -3, -3, -4, -24, -8],
        [99, -8, 8, 6, 6, 8, -8, 99],
    ]"""

    SQUARE_WEIGHTS = [
        99, -8, 8, 6, 6, 8, -8, 99,
        -8, -24, -4, -3, -3, -4, -24, -8,
        8, -4, 7, 4, 4, 7, -4, 8,
        6, -3, 4, 0, 0, 4, -3, 6,
        6, -3, 4, 0, 0, 4, -3, 6,
        8, -4, 7, 4, 4, 7, -4, 8,
        -8, -24, -4, -3, -3, -4, -24, -8,
        99, -8, 8, 6, 6, 8, -8, 99
        ]

    def __init__(self, my_color, opponent_color):
        self.name = 'izotomas'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.start_time = 0

    def move(self, board):
        # test
        board1d = reversiutils.flatten(board)
        # test end
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
        coordinates = reversiutils.index_to_cartesian(node.children[0].move)
        return coordinates

    def __max_value(self, node, alpha, beta):
        if self.__is_terminal_state(node):
            return self.__utility(node)
        node.children = node.get_children()
        for child in node.children:
            node.score = max(node.score, self.__min_value(child, alpha, beta))
            if node.score >= beta:
                return node.score
            alpha = max(alpha, node.score)
        return node.score

    def __min_value(self, node, alpha, beta):
        if self.__is_terminal_state(node):
            return self.__utility(node)
        node.children = node.get_children()
        for child in node.children:
            node.score = min(node.score, self.__max_value(child, alpha, beta))
            if node.score <= alpha:
                return node.score
            beta = min(beta, node.score)
        return node.score

    def __utility(self, node):
        state = node.state
        is_max = node.is_max_node
        my_col = node.my_color
        opp_col = node.opponent_color

        s = reversiutils.square_weights(state, MyPlayer.SQUARE_WEIGHTS, is_max, my_col, opp_col)
        # m = reversiutils.mobility(state, is_max, my_col, opp_col)
        return s  # + m

    def __is_terminal_state(self, node):
        move_time = (time.time() - self.start_time)
        max_depth_reached = node.depth == 0
        time_expired = move_time > MyPlayer.MAX_WAITING_TIME
        no_children = not node.children
        return max_depth_reached or no_children
        # return node.depth == 0 or move_time > MyPlayer.MAX_WAITING_TIME or not node.children

    # endregion
