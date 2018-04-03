import random

class MyPlayer:
    def __init__(self, answer = 'R'): # answer - input arg
        self.answer = answer
        self.oppplays = [] # empty list()

    def play(self):
        return self.answer

    def record_opp_move(self, move):
        self.oppplays.append(move)

class RandomPlayer(MyPlayer):
    def play(self):
        return random.choice(['R', 'S', 'P'])

if __name__ == "__main__": #if run from main (not imported as a library)....
    p1 = MyPlayer('R')
    p2 = RandomPlayer()
    for i in range(10):
        answer2 = p2.play() # same thing: MyPlayer.play(p1)
        p1.record_opp_move(answer2)
    print(p1.play(), p2.play())
    print(p1.oppplays)

