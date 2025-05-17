import numpy as np
import random
import sys
from game import BlackjackGame, Player

def alphabeta(game, depth, maximizingPlayer, alpha, beta, dep=4):
    last_card = game.desk
    if depth == dep or game.end:
      score = get_heuristic(game)
      return (score, set_of_col)
    if maximizingPlayer:
      score = -sys.maxsize
    else:
      score = sys.maxsize
    for col in range(7):
      if game.table[0][col] == 0:
        newgame = game.drop_piece(game, col)
        Tuple = alphabeta(newgame, depth+1, not maximizingPlayer, alpha, beta, dep)
        if not maximizingPlayer : #min
          if score > Tuple[0]:
            score = Tuple[0]
            set_of_col = {col}
          if score <= alpha :
            return (score, set_of_col)
          else:
            beta = min(beta, score)
        else:                  #max
          if score < Tuple[0]:
            score = Tuple[0]
            set_of_col = {col}         
          elif score == Tuple[0]:
            set_of_col.add(col)
          if score >= beta :
            return (score, set_of_col)
          else:
            alpha = max(alpha, score)

    return (score, set_of_col)

def agent(game):
    return random.choice(list(alphabeta(game, 0, False, -np.inf, np.inf)[1]))

def get_heuristic(game):
    w1 = game.dealer.calculate_hand_value()
    w2 = game.player.calculate_hand_value()

    score = ()
    return score