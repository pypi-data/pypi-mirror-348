import random


class RandomStrategy:

    name = "RandomStrategy_Base_ToCheck"
    author = "admin"

    def play(self):
        return random.choice(["rock", "paper", "scissors"])

    def handle_moves(self, own, opponent):
        pass
