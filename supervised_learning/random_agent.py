import random

class RandomAgent:
    def act(self, player_sum, dealer_card):
        return random.choice(["hit", "stand"])
