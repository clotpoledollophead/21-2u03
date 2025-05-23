import random
from typing import List, Optional
import copy

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
    
    def __eq__(self, other):
        return isinstance(other, Card) and self.suit == other.suit and self.rank == other.rank
    
    def __hash__(self):
        return hash((self.suit, self.rank))


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
        self.noshow = True if identity==0 else False

    def add_card(self, card: Card):
        self.hand.append(card)
        # if bust
        if self.calculate_hand_value() > 21:
            self.is_busted = True
            self.is_standing = True

    def calculate_hand_value(self) -> int:
        if self.noshow:
            value = self.hand[0].value
        else:
            value = sum(card.value for card in self.hand)
            # for the value of A
            num_aces = sum(1 for card in self.hand if card.rank == "A")
            # if contain A and the total is greater than 21，change the value of A from 11 to 1
            while value > 21 and num_aces:
                value -= 10
                num_aces -= 1
        return value

    def decide_action(self, op_v:1) -> str:
        if self.id == 0:
            # dealer：if less than 17 hit, or stand
            if len(self.hand) == 2:
                self.noshow = False 
            if self.calculate_hand_value() < 17:
                return "hit"
            else:
                return "stand"
        elif self.id == 1:
            # player
            while True:
                action = input("hit(h)or stand(s)? ").lower()
                if action in ["h", "hit"]:
                    return "hit"
                elif action in ["s", "stand"]:
                    return "stand"
                else:
                    print("invalid")
        elif self.id == 2: #for ai agent
            C = [Card(suit, rank) for suit in SUITS for rank in RANKS]
            for card in self.hand:
                C.remove(card)
            d = op_v
            p = self.calculate_hand_value()
            h = [0, 0]
            s = [0, 0]
            for c in C:
                G = C.copy()
                G.remove(c)
                prd = 0
                if d <= 10:
                    prd = c.value+d
                elif d>10 and c.value == 11:
                    prd = 1+d
                s[0] += p-prd
                s[1] += 1
                for g in G:
                    prp = 0
                    if p <= 10:
                        prp = g.value+p
                    elif p>10 and g.value == 11:
                        prp = 1+p

                    if p > 21:
                        h[0] += -21
                    else:
                        h[0] += prp - prd
                    h[1] += 1
            h1, s1 = h[0]/h[1], s[0]/s[1]
            #print(h1, s1)
            if h1 > s1:
                return "hit"
            else: 
                return "stand"




    def show_hand(self) -> str:
        if self.noshow:
            w = str(self.hand[0])+" hide"
        else:
            w = " ".join(str(card) for card in self.hand)
        return w


class BlackjackGame:
    def __init__(self, ai: False):
        self.deck = Deck()
        self.player = Player("ai player", 2) if ai else Player("human player", 1)
        self.dealer = Player("dealer", 0)
        self.players = [self.player]
        self.pend = False
        self.dend = False 

    def start_game(self, detail: True):
        # start, each one for 2 cards
        for _ in range(2):
            self.dealer.add_card(self.deck.deal())
            for player in self.players:
                player.add_card(self.deck.deal())

        # game main loop
        self.pend = False
        self.dend = False
        while not self.pend and not self.dend:
            if detail:
                print(f"\n{self.dealer.name}:")
                if self.pend:
                    while 1:
                        action = self.dealer.decide_action()
                        if action == "hit":
                            card = self.deck.deal()
                            self.dealer.add_card(card)
                            if self.dealer.is_busted:
                                if detail:
                                    print(f"{self.dealer.name} bust! total:{self.dealer.calculate_hand_value()}")
                                self.dend = True
                                break
                        else:
                            self.dend = True
                            break
                print(f"{self.dealer.name} card:{self.dealer.show_hand()}, total:{self.dealer.calculate_hand_value()}")
            for player in self.players:
                if player.is_standing:
                    continue
                
                if detail:
                    print(f"\n{player.name} turn:")
                    #if player.id != 0:
                    print(f"{player.name} card:{player.show_hand()}, total:{player.calculate_hand_value()}")

                action = player.decide_action(self.dealer.calculate_hand_value())

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
                self.pend = True

        self.dealer.noshow = False
        w = self.determine_winner(detail=detail)

        return w

    def determine_winner(self, detail: True):
        # show the all
        status = "bust" if self.dealer.is_busted else "valid"
        if detail:
            print(f"{self.dealer.name}: {self.dealer.show_hand()} - point:{self.dealer.calculate_hand_value()} ({status})")
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
        c = self.dealer.calculate_hand_value()
        if max_value < c:
            max_value = c
            winners = [self.dealer]
        elif max_value == c:
            winners.append(self.dealer)

        if len(winners) == 1:
            print(f"winner is {winners[0].name}, total: {max_value}")
            if winners[0].name == "dealer":
                return 1
            else:
                return 2
        else:
            print(f"draw, value: {max_value}")
            return 0
