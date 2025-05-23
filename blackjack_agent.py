import joblib
import pandas as pd

class BlackjackSupervisedAgent:
    def __init__(self, model_path="blackjack_strategy_model.pkl"):
        self.model = joblib.load(model_path)

    def act(self, player_sum, dealer_card):
        features = pd.DataFrame([[player_sum, dealer_card]], columns=["sumofcards", "dealcard1"])
        return self.model.predict(features)[0]
