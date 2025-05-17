import random
import time
from typing import List, Optional
import argparse

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}


class Card:
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank
        self.value = VALUES[rank]

    def __str__(self):
        return f"{self.suit}{self.rank}"


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self) -> Optional[Card]:
        if not self.cards:
            return None
        return self.cards.pop()


class Player:
    def __init__(self, name: str, identity):
        self.name = name
        self.hand: List[Card] = []
        self.id = identity # 0dealer 1humanplayer 2aiagent
        self.is_standing = False
        self.is_busted = False

    def add_card(self, card: Card):
        self.hand.append(card)
        # if bust
        if self.calculate_hand_value() > 21:
            self.is_busted = True
            self.is_standing = True

    def calculate_hand_value(self) -> int:
        value = sum(card.value for card in self.hand)
        # for the value of A
        num_aces = sum(1 for card in self.hand if card.rank == "A")
        # if contain A and the total is greater than 21，change the value of A from 11 to 1
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

    def decide_action(self) -> str:
        if self.id == 0:
            # dealer：if less than 17 hit, or stand
            if self.calculate_hand_value() < 17:
                return "hit"
            else:
                return "stand"
        elif self.id == 1:
            # player
            while True:
                action = input(f"{self.name}, your card:{self.show_hand()}, total:{self.calculate_hand_value()}\nhit(h)or stand(s)? ").lower()
                if action in ["h", "hit"]:
                    return "hit"
                elif action in ["s", "stand"]:
                    return "stand"
                else:
                    print("invalid")
        elif self.id == 2: #for ai agent
            if self.calculate_hand_value() < 18:
                return "hit"
            else:
                return "stand"

    def show_hand(self) -> str:
        return " ".join(str(card) for card in self.hand)


class BlackjackGame:
    def __init__(self, ai: False):
        self.deck = Deck()
        self.player = Player("ai player", 2) if ai else Player("human player", 1)
        self.dealer = Player("dealer", 0)
        self.players = [self.dealer, self.player]

    def start_game(self, detail: True):
        # start, each one for 2 cards
        for _ in range(2):
            for player in self.players:
                player.add_card(self.deck.deal())

        # game main loop
        game_over = False
        while not game_over:
            for player in self.players:
                if player.is_standing:
                    continue
                
                if detail:
                    print(f"\n{player.name} turn:")
                    if player.id != 1:
                        print(f"{player.name} card:{player.show_hand()}, total:{player.calculate_hand_value()}")

                action = player.decide_action()

                if action == "hit":
                    card = self.deck.deal()
                    player.add_card(card)
                    if detail:
                        print(f"{player.name} get card:{card}, total:{player.calculate_hand_value()}")
                        if player.is_busted:
                            print(f"{player.name} bust! total:{player.calculate_hand_value()}")
                else:  # stand
                    player.is_standing = True
                    if detail:
                        print(f"{player.name} stand. total:{player.calculate_hand_value()}")

            # if end
            if all(player.is_standing for player in self.players):
                game_over = True

        w = self.determine_winner(detail=detail)

        return w

    def determine_winner(self, detail: True):
        # show the all
        for player in self.players:
            status = "bust" if player.is_busted else "valid"
            if detail:
                print(f"{player.name}: {player.show_hand()} - point:{player.calculate_hand_value()} ({status})")

        # find if any player is not bust
        valid_players = [p for p in self.players if not p.is_busted]

        if not valid_players:
            print("all bust, no winner.")
            return 0

        # find the player with highest point
        max_value = max(p.calculate_hand_value() for p in valid_players)
        winners = [p for p in valid_players if p.calculate_hand_value() == max_value]

        if len(winners) == 1:
            print(f"winner is {winners[0].name}, total: {max_value}")
            if winners[0].name == "dealer":
                return 1
            else:
                return 2
        else:
            print(f"draw, value: {max_value}")
            return 0


def play_blackjack():
    print("blackjack")
    parser = argparse.ArgumentParser(description="Blackjack")
    parser.add_argument("-n", "--numgames", type=int, default=1, help="Number of games to simulate.")
    parser.add_argument("-a", "--ai", action="store_true", help="Use AI for the player.")
    parser.add_argument("-s", "--skip", action="store_false", help="Skip the datail in game (set to True).")
    # python main.py -n 200 -a -s (run 100 times, use ai agent, skip the detail only maintain the info of win)
    args = parser.parse_args()
    w1, w2, n = 0, 0, 0
    for i in range(args.numgames):
        game = BlackjackGame(args.ai) #ai for true
        status = game.start_game(args.skip) #skip for false
        print(f'====== run {i+1} ======\n')
        if status == 0:
            n += 1
        elif status == 1:
            w1 += 1
        else:
            w2 += 1
    print(f'dealer:{w1}, player:{w2}, draw:{n}, in {args.numgames} runs')



if __name__ == "__main__":
    play_blackjack()