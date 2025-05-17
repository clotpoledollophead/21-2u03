import argparse
from game import BlackjackGame 


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