import random

class RandomAgent:
    def act(self, player_sum, dealer_card, is_soft, num_cards):
        return random.choice(['hit', 'stand'])

