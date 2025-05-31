from blackjack_env import BlackjackEnv

class ExpectimaxAgent:
    def __init__(self):
        self.env = None  # 不需要，留空保持一致

    def act(self, player_sum, dealer_card, is_soft, num_cards):
        from blackjack_env import BlackjackEnv
        env = BlackjackEnv()
        env.player_hand = [(player_sum, '')]  # 模擬數值，不重要
        env.dealer_hand = [(dealer_card, '')]

        deck = env.deck.copy()
        for card in env.player_hand + env.dealer_hand:
            if card in deck:
                deck.remove(card)

        h, s = [0, 0], [0, 0]
        d = dealer_card
        p = player_sum

        for c in deck:
            d_sum = d + min(c[0], 10) if c[0] != 1 else d + 1
            s[0] += p - (17 if d_sum <= 17 else d_sum)
            s[1] += 1

            for g in deck:
                if g == c:
                    continue
                p_new = p + (1 if g[0] == 1 and p > 10 else min(g[0], 10))
                if p_new > 21:
                    h[1] += 1
                    continue
                h[0] += p_new - (17 if d_sum <= 17 else d_sum)
                h[1] += 1
        h1 = h[0]/h[1] if h[1] else -float('inf')
        s1 = s[0]/s[1] if s[1] else -float('inf')
        return "hit" if h1 > s1 else "stand"
