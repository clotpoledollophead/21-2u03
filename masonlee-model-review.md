# Review of Mason Lee's BlackJack-AI — An AI trained to play Blackjack using NeuroEvolution of Augmenting Topologies (NEAT)

## Original Work Link
https://github.com/mason-lee19/Blackjack_NEAT

## Goal of the Model
The goal of this project is to train an AI agent to play Blackjack by evolving its decision-making strategy using NEAT (NeuroEvolution of Augmenting Topologies).

- **input**: Current game state (player's hand, dealer's visible card, usable ace info, etc.)
- **output**: AI decides action: hit, stand, double

## Learning method
Evolve neural networks based on fitness (win rate, performance)

## What is NEAT?
NEAT (NeuroEvolution of Augmenting Topologies) is a machine learning method that evolves both the structure (topology) and the weights of neural networks using genetic algorithms. Unlike traditional supervised learning, NEAT does not require labeled data and explores increasingly complex solutions through evolution.

## NEAT Evolution Process
This project uses NEAT (NeuroEvolution of Augmenting Topologies) to evolve the AI's Blackjack playing strategy. NEAT optimizes both the neural network's weights and topology (structure) through genetic algorithms.

### Load Config
```bash
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
```

Load evolution parameters from `config.txt` including population size, mutation rates, etc.

### Initialize Population
```bash
p = neat.Population(config)
```
Create the initial generation of genomes (candidate solutions).

### Add Reporters
```bash
p.add_reporter(neat.StdOutReporter(True))
p.add_reporter(neat.StatisticsReporter())
```
Add console outputs and statistics tracking to monitor evolution progress.

### Run Evolution Process
```bash
winner = p.run(eval_genomes, generations)
```
Start the NEAT evolution loop, running for N generations.


### Evaluate Each Genome
```bash
def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        game = Game(genome, config)
        genome.fitness = game.run()
```
For each genome in the population, simulate a Blackjack game to assess performance.

## Game.run(Blackjack Simulation Flow)

### Initialize Game
```bash
self.player = TablePlayer()
self.dealer = Dealer()
```
Set up the player and dealer hands.

### Player Decision Making
```bash
while not self.player.done:
    action = self.player_decision()
    if action == 'hit':
        self.player.hit(self.deck)
    elif action == 'stand':
        break
```
The player's neural network decides whether to hit, stand, or double based on the current game state.

### Dealer Logic
```bash
while self.dealer.score < 17:
    self.dealer.hit(self.deck)
```
Dealer follows simple rules: hit until reaching 17 or more.

### Determine Result
```bash
result = self.calculate_result()
self.fitness += result
```
Compare player and dealer scores, decide win/lose/draw, apply scoring.

### Return Fitness
```bash
return self.fitness
```
After finishing the round, return the accumulated fitness score.

## Save Best Genome & Logs

### Save the best-performing genome as `best.pickle`.
```bash
pickle.dump(winner, open("best.pickle", "wb"))
```

### Save stats (fitness curve) and output log.
```bash
save_stats(stats)
```

## Usage

### OS
`Linux` on Windows(Ubuntu)

### Download From Github
```bash
git clone https://github.com/mason-lee19/Blackjack_NEAT.git
cd Blackjack_NEAT
```

### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
```

### Install Necessary Requirment
```bash
pip install neat-python numpy pandas matplotlib
```

### Train AI with NEAT
```bash
python main.py
```

- Starts the NEAT evolution process
- Outputs best.pickle (best genome) / output.csv (training log) / stats.png (fitness curve)

## Project Structure
- `main.py`: Runs NEAT training and evolution.
- `game.py`: Manages game logic and flow.
- `deck.py`: Handles card deck operations.
- `player.py`: Defines player and dealer behavior.
- `config.txt`: NEAT configuration parameters.

