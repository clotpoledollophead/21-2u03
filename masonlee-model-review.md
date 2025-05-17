# Review of Mason Lee's BlackJack-AI — An AI trained to play Blackjack using NeuroEvolution of Augmenting Topologies (NEAT)

## Goal of the Model
The goal of this project is to train an AI agent to play Blackjack by evolving its decision-making strategy using NEAT (NeuroEvolution of Augmenting Topologies).

-input: Current game state (player's hand, dealer's visible card, usable ace info, etc.)
-output: AI decides action: hit, stand, double

## Learning method
Evolve neural networks based on fitness (win rate, performance)

## Data Generation 
Unlike supervised learning, this project does not generate labeled data.
Instead, it plays games using evolving agents, and their performance is the feedback.

-Monte Carlo style self-play for fitness evaluation
-No human-labeled dataset involved

## Usage

### Train AI with NEAT
python main.py

-Starts the NEAT evolution process
-Outputs best.pickle (best genome) / output.csv (training log) / stats.png (fitness curve)

## Project Notes

