# Review of Justin Bodnar's **BlackJack-AI — Machine Learning Library for Card Games**
## Goal of the Model
The goal of Bodnar's model is to train a neural network that mimcs a basic blackjack strategy, that has:
- input: information regarding the current game state (e.g., player's hand value)
- output: decision to *hit* or *stay*

## Data Generation
The model proposed uses Monte Carlo simulations of Blackjack games to create training data, as seen in the snippet below:
```python
blackjack.gen_data_set(num_hands, file_name, info_level, shuffle)
```
- `num_hands`: number of hands to simulate
- `file_name`: output filepath
- `info_level`: how much info the dataset includes for the model
    * level `1`: only the player's hand value is known
    * level `2`: includes both the player's hand value and the dealer's face-up card (which is visible to a player in real life)
    * level `3`: includes all cards

This function then outputs two files:
- `.data`: outputs the input features
- `.tags`: the decision whether to play `h` (hit: to ask for another card) or `s` (stay: to not take another card)

For example, if we see a decision such as `15, h`, this means that the agent has 15 points and should hit for another card; if we see `20, s`, this means that the agent has 20 points and stays its hand.

## Data Preprocessing
The `.data` and `.tags` files are cleaned and split for training/testing sets.
- Input features are converted to numbers
- Tags for decisions:
    * `h` $\rarr$ 1.0
    * `s` $\rarr$ 0.0

## Model Architecture
The model runs on a neural network:
```python
model = keras.Sequential()
model.add( keras.layers.Dense(4096, input_dim=2) )
model.add( keras.layers.Dense(2, activation=tf.nn.softmax) )
```
### Level 1 (just player hand value):
- input: an integer such as `[16]`
- output: returns probabilities to *stay* or *hit*
### Level 2 (player hand + dealer's face-up card):
- input: `[player_hand_value, dealer_visible_card_value]`
- output: to *stay* or *hit*

This way of playing is the closest to what players in real life observe the cards, and this model allows for the learning of conditional strategies, for example:
```text
Hit on 12 if the dealer shows a 7 or higher
```
### Level 3 (all cards seen):
- input: a vector of 54 elements representing the player handm visible cards of the dealer, and all other seen cards. This simulates what the players of Blackjack who use the *card-counting* strategy in real life aim to achieve, where one tracks what's already been dealt to make more optimal decisions.

## Training
The model is trained using:
```python
model.compile(optimizer='adam',
	loss='sparse_categorical_crossentropy',
	metrics=['accuracy'])
model.fit(train_data, train_tags, epochs=10)
```
- Sparce Categorical Cross Entropy (SCCE): produces a category index of the most likely matching category

## Evaluation and Accuracy
After training, the model is evaluated by its `win percentage` and `accuracy`.
$$
\text{total} = \text{wins} + \text{losses} + \text{ties} \\ \text{win percentage} = \frac{\text{wins}} {\text{total}} \times 100\%
$$

## Using the Model
Once trained, the model can predict decisions for any hand value in the game.

## Our Review of the Model
### What is being learned?
The model implemented here is learning a policy based on the outcome of simulated games—that is, it is not hard-coded, and discovers patterns based on what leads to win/losses during simulation.