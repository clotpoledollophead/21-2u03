import random

class BlackjackEnv:
    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.reset_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.done = False

    def reset_deck(self):
        suits = ['H', 'D', 'S', 'C']
        values = list(range(1, 14))  # 1=A, 11=J, 12=Q, 13=K
        self.deck = []
        for _ in range(self.num_decks):
            for suit in suits:
                for value in values:
                    self.deck.append((value, suit))
        random.shuffle(self.deck)

    def draw_card(self):
        if not self.deck:
            self.reset_deck()
        return self.deck.pop()

    def hand_value(self, hand):
        total = sum(min(card[0], 10) for card in hand)
        num_aces = sum(1 for card in hand if card[0] == 1)
        soft = False
        while num_aces > 0:
            if total + 10 <= 21:
                total += 10
                soft = True
            num_aces -= 1
        return total, soft

    def reset(self):
        if len(self.deck) < 10:
            self.reset_deck()
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card()]
        self.done = False
        return self.get_obs()

    def get_obs(self):
        player_sum, is_soft = self.hand_value(self.player_hand)
        dealer_card = min(self.dealer_hand[0][0], 10)
        num_cards = len(self.player_hand)
        return {
            "player_sum": player_sum,
            "dealer_card": dealer_card,
            "is_soft": int(is_soft),
            "num_cards": num_cards
        }
        
    def step(self, action):
        """
        For NEAT or other agents: step(action)
        action: "hit" or "stand"
        Returns: obs, reward, done
        """
        if self.done:
            return self.get_obs(), 0, True

        reward = 0
        if action == "hit":
            obs, result, done = self.player_hit()
            if done:
                reward = -1 if result == "lose" else (1 if result == "win" else 0)
        else:  
            self.player_stand()
            while not self.dealer_is_done():
                self.dealer_draw_one()
            result = self.get_game_result()
            done = True
            reward = -1 if result == "lose" else (1 if result == "win" else 0)

        self.done = done
        return self.get_obs(), reward, done


    def player_hit(self):
        if self.done:
            return self.get_obs(), "game_over", True
        self.player_hand.append(self.draw_card())
        player_sum, _ = self.hand_value(self.player_hand)
        if player_sum > 21:
            self.done = True
            return self.get_obs(), "lose", True
        return self.get_obs(), None, False

    def player_stand(self):
        return self.get_obs(), None, False

    def dealer_draw_one(self):
        if self.done:
            return True
        self.dealer_hand.append(self.draw_card())
        return self.dealer_is_done()

    def dealer_is_done(self):
        dealer_sum, dealer_soft = self.hand_value(self.dealer_hand)
        if dealer_sum >= 17 and not (dealer_sum == 17 and dealer_soft):
            self.done = True
            return True
        return False

    def get_game_result(self):
        player_sum, _ = self.hand_value(self.player_hand)
        dealer_sum, _ = self.hand_value(self.dealer_hand)
        if dealer_sum > 21 or player_sum > dealer_sum:
            return "win"
        elif player_sum < dealer_sum:
            return "lose"
        else:
            return "draw"
