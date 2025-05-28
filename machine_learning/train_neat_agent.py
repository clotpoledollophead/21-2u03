import neat
import os
import pickle
from blackjack_env import BlackjackEnv

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        env = BlackjackEnv()
        fitness = 0

        for _ in range(1000):  
            state = env.reset()
            done = False
            total_reward = 0

            while not done:
                player_sum = state['player_sum']
                dealer_card = state['dealer_card']
                is_soft = state['is_soft']
                num_cards = len(env.player_hand)

                inputs = [player_sum / 21.0, dealer_card / 10.0, int(is_soft), num_cards / 5.0]
                output = net.activate(inputs)
                action = "hit" if output[0] > 0.5 else "stand"

                state, reward, done = env.step(action)
                total_reward += reward

            fitness += total_reward

        genome.fitness = fitness

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    with open('neat_model.pkl', 'wb') as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config.txt')
    run(config_path)
