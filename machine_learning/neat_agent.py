import neat
import pickle

class NEATAgent:
    def __init__(self, model_path="best_neat.pkl", config_path="neat_config.txt"):
        with open(model_path, "rb") as f:
            genome = pickle.load(f)
        config = neat.Config(
            neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)

    def act(self, player_sum, dealer_card, is_soft, num_cards):
        input_vector = [
            player_sum / 21.0,      
            dealer_card / 10.0,     
            int(is_soft),           
            num_cards / 5.0         
        ]
        output = self.net.activate(input_vector)
        return "hit" if output[0] > 0.5 else "stand"
