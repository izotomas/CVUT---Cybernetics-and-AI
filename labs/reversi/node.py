import reversiutils


class Node:
    DEFAULT_SCORE = -1000000
    DEFAULT_MOVE = None
    DEFAULT_IS_MAX = True
    DEFAULT_MAX_DEPTH = 7

    def __init__(self, board, my_color, opponent_color, move=DEFAULT_MOVE, is_max_node=DEFAULT_IS_MAX, depth=DEFAULT_MAX_DEPTH):
        self.depth = depth
        self.state = board
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.is_max_node = is_max_node
        self.move = move
        self.score = Node.DEFAULT_SCORE if is_max_node else Node.DEFAULT_SCORE * (-1)
        self.children = []

    def get_children(self):
        children = []
        valid_moves = reversiutils.get_all_valid_moves(self.state, self.my_color, self.opponent_color)
        for move in valid_moves:
            board = reversiutils.simulate_move(self.state, move, self.my_color)
            child = Node(board, self.opponent_color, self.my_color, move[0], not self.is_max_node, self.depth-1)
            children.append(child)
        return children

    def __lt__(self, other):
        return self.score <= other.score
