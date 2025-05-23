from blackjack_env import BlackjackEnv
from blackjack_agent import BlackjackSupervisedAgent
from random_agent import RandomAgent
from collections import Counter
import numpy as np

def simulate(agent, num_games=1000):
    results = []
    for _ in range(num_games):
        env = BlackjackEnv()
        state = env.reset()
        done = False
        while not done:
            action = agent.act(state['player_sum'], state['dealer_card'])
            state, result, done = env.step(action)
        results.append(result)
    counter = Counter(results)
    return {
        'win': counter['win'],
        'lose': counter['lose'],
        'draw': counter['draw']
    }

def average_results(results_list):
    keys = ['win', 'lose', 'draw']
    avg = {}
    for key in keys:
        values = [r[key] for r in results_list]
        avg[key] = {
            'mean': np.mean(values),
            'std': np.std(values)
        }
    return avg

def print_summary(agent_name, stats, total_games):
    print(f"\n{agent_name}（平均每 {total_games} 局）：")
    for key in ['win', 'lose', 'draw']:
        mean = stats[key]['mean']
        std = stats[key]['std']
        print(f"{key.capitalize():>5}: {mean:.1f} ± {std:.1f}（{mean / total_games:.2%}）")

# === 主程式開始 ===
GAMES_PER_RUN = 1000
REPEATS = 10

trained_agent = BlackjackSupervisedAgent("blackjack_strategy_model.pkl")
random_agent = RandomAgent()

trained_results = [simulate(trained_agent, GAMES_PER_RUN) for _ in range(REPEATS)]
random_results = [simulate(random_agent, GAMES_PER_RUN) for _ in range(REPEATS)]

trained_stats = average_results(trained_results)
random_stats = average_results(random_results)

print_summary("訓練 AI", trained_stats, GAMES_PER_RUN)
print_summary("隨機 AI", random_stats, GAMES_PER_RUN)
