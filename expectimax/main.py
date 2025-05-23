import argparse
import matplotlib.pyplot as plt
import numpy as np
from game import BlackjackGame 


def play_blackjack():
    print("blackjack")
    parser = argparse.ArgumentParser(description="Blackjack")
    parser.add_argument("-n", "--numgames", type=int, default=1, help="Number of runs to simulate.")
    parser.add_argument("-rn", "--rnum", type=int, default=1000, help="Number of games of each run to simulate.")
    parser.add_argument("-a", "--ai", action="store_true", help="Use AI for the player.")
    parser.add_argument("-s", "--skip", action="store_false", help="Skip the datail in game (set to True).")
    # python main.py -n 200 -rn 1000 -a -s (run 100 times, each run 1000 games, use ai agent, skip the detail only maintain the info of win)
    args = parser.parse_args()
    w, l, d = [], [], []
    x = range(1, args.numgames+1)
    for i in range(args.numgames):
        w1, w2, n = 0, 0, 0
        for k in range(args.rnum):
            game = BlackjackGame(args.ai) #ai for true
            status = game.start_game(args.skip) #skip for false
            #print(f'====== run {i+1} ======\n')
            if status == 0:
                n += 1
            elif status == 1:
                w1 += 1
            else:
                w2 += 1
        print(f'dealer:{w1}, player:{w2}, draw:{n}, in {i+1} runs')

        w.append(w2/10)
        l.append(w1/10)
        d.append(n/10)
    
    plt.plot(x, w, "r")
    plt.plot(x, l, "g")
    plt.plot(x, d, "k")
    plt.legend(["win rate", "lose rate", "draw rate"])
    plt.savefig('test.png')
    print(f'{args.numgames} runs, for each run {args.rnum} games:')
    print(f'win: {round(np.mean(w), 2)}±{round(np.std(w), 2)}%')
    print(f'lose: {round(np.mean(l), 2)}±{round(np.std(l), 2)}%')
    print(f'draw: {round(np.mean(d), 2)}±{round(np.std(d), 2)}%')

if __name__ == "__main__":
    play_blackjack()
