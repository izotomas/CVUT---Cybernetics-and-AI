import dummyplayer

class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def run(self):
        draw = True

        while draw:
            a1 = self.p1.play()
            a2 = self.p2.play()
            print(a1, a2)
            draw = (a1 == a2)

        winner_index = self.evaluate_moves(a1, a2)
        return winner_index

    def evaluate_moves(self, m1, m2):
        if (m1, m2) in [('R', 'S'), ('P', 'R'), ('S', 'P')]:
            return 0
        else:
            return 1

if __name__ == "__main__":
    p1 = dummyplayer.MyPlayer()
    p2 = dummyplayer.RandomPlayer()
    g = Game(p1,  p2)
    winner = g.run()
    print(winner)
