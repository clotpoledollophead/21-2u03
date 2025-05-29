# Expectimax agent

## Game Environment 

Refer to [blackjack-ai](https://github.com/korman/blackjack-ai/tree/master) to generate the game environment

## Agent

Calculate the expected value of the agent's hand minus the dealer's after ‘Hit’ and ‘Stand’ respectively.


Two loops are used. 

At the first level, it loops through all the possible values of the dealer, then subtracts the dealer's value from the current agent's hand value. 

And because the dealer is below 17, you need to keep drawing cards. 

Therefore, when calculating the value of the dealer, if it is lower than 17, it will be counted as 17; otherwise, it will be counted as the original value. 

It is stored in the ‘Stand’ expectation.

The second level of the cycle agent can draw all the cards, excluding the stack of the dealer's desired card. 

Calculation continues from the previous loop's dealer value.

It is stored in the ‘Hit’ expectation.

Finally, divide by the respective counts to get the expected value.
## Result
The experimental results have a win rate of about 40%, which I think is quite high for an agent using the expectimax algorithm, given that a large portion of the game is dominated by chance. 

And the variance is not more than 1.5%, so it's a pretty stable agent.
