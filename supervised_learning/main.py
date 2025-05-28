from blackjack_env import BlackjackEnv
from rfc_agent import RFCAgent
from random_agent import RandomAgent
from neat_agent import NEATAgent
from Qlearning_agent import QLearningAgent
from basic_strategy_agent import BasicStrategyAgent
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

def simulate(agent, env, num_games=1000):
    result = {'win': 0, 'lose': 0, 'draw': 0}
    for _ in range(num_games):
        env.reset()
        done = False
        outcome = None

        while not done:
            state = env.get_obs()
            action = agent.act(state['player_sum'], state['dealer_card'], state['is_soft'], state['num_cards'])
            if action == "hit":
                _, outcome, done = env.player_hit()
                if done:
                    break
            else:
                env.player_stand()
                break

        if not outcome:
            while not env.dealer_is_done():
                env.dealer_draw_one()
            outcome = env.get_game_result()

        result[outcome] += 1

    return result

REPEATS = 5
GAMES = 1000

agents = {
    "RFC AI": RFCAgent("rfc_model.pkl"),
    "Random AI": RandomAgent(),
    "NEAT AI": NEATAgent("neat_model.pkl", "neat_config.txt"),
    "QLearning AI": QLearningAgent(),
    "Basic Strategy AI": BasicStrategyAgent()
}

agents["QLearning AI"].load_qtable("q_table.json")

win_rates = {name: [] for name in agents}

for name, agent in agents.items():
    env = BlackjackEnv(num_decks=1)
    for _ in tqdm(range(REPEATS), desc=f"{name} ", ncols=80):
        result = simulate(agent, env, GAMES)
        win_rates[name].append(result['win'] / GAMES)

x = np.arange(1, REPEATS + 1)
for name in agents:
    plt.plot(x, win_rates[name], label=f"{name}（average {np.mean(win_rates[name]):.2%}）")

plt.title("Blackjack Win Rate Compare: NEAT vs RFC vs Random vs RL vs Basic Strategy", fontsize=10)
plt.ylabel("Win Rate")
plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("compare.png")
plt.show()
