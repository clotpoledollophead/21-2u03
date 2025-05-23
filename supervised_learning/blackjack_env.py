import random

class BlackjackEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = [self.draw_card(), self.draw_card()]
        self.dealer = [self.draw_card(), self.draw_card()]
        return self.get_state()

    def draw_card(self):
        card = random.randint(1, 10)
        return 11 if card == 1 else card  # 1 當作 A=11

    def hand_value(self, hand):
        total = sum(hand)
        # 調整 A 的值（11 -> 1）
        while total > 21 and 11 in hand:
            hand[hand.index(11)] = 1
            total = sum(hand)
        return total

    def get_state(self):
        return {
            "player_sum": self.hand_value(self.player),
            "dealer_card": self.dealer[0],
            "player_hand": self.player,
            "dealer_hand": self.dealer
        }

    def step(self, action):
        if action == "hit":
            self.player.append(self.draw_card())
            if self.hand_value(self.player) > 21:
                return self.get_state(), "lose", True
            return self.get_state(), None, False
        elif action == "stand":
            while self.hand_value(self.dealer) < 17:
                self.dealer.append(self.draw_card())
            return self.get_state(), self.judge(), True

    def judge(self):
        p = self.hand_value(self.player)
        d = self.hand_value(self.dealer)
        if d > 21 or p > d:
            return "win"
        elif p == d:
            return "draw"
        else:
            return "lose"
