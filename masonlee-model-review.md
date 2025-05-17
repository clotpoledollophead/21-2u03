# Review of Mason Lee's BlackJack-AI — An AI trained to play Blackjack using NeuroEvolution of Augmenting Topologies (NEAT)

## Goal of the Model
The goal of this project is to train an AI agent to play Blackjack by evolving its decision-making strategy using NEAT (NeuroEvolution of Augmenting Topologies).

- **input**: Current game state (player's hand, dealer's visible card, usable ace info, etc.)
- **output**: AI decides action: hit, stand, double

## Learning method
Evolve neural networks based on fitness (win rate, performance)

## NEAT Evolution Process
This project uses NEAT (NeuroEvolution of Augmenting Topologies) to evolve the AI's Blackjack playing strategy. NEAT optimizes both the neural network's weights and topology (structure) through genetic algorithms.

### Initialization
- Random neural networks (genomes) are generated.
- Each genome represents a possible Blackjack strategy.

### Evaluation (Fitness Computation)
- Each genome plays multiple Blackjack hands.
- Performance metrics (e.g., win rate, final balance) are used to calculate fitness.

### Selection & Reproduction
- Genomes with higher fitness are selected.
- Crossover (recombining structures) and mutation (random changes) create new offspring.

### Speciation
- Similar genomes are grouped into species.
- Diversity is preserved by allowing niche species to evolve.

### Repeat Until Convergence
- The process repeats across generations.
- Stops when maximum generations are reached or desired performance is achieved.

## Data Generation 
Unlike supervised learning, this project does not generate labeled data.
Instead, it plays games using evolving agents, and their performance is the feedback.

## Usage

### Train AI with NEAT
```bash
python main.py
```

- Starts the NEAT evolution process
- Outputs best.pickle (best genome) / output.csv (training log) / stats.png (fitness curve)

## Project Notes

