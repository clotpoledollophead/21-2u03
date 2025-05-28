import pandas as pd
import joblib

class RFCAgent:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def act(self, player_sum, dealer_card, is_soft, num_cards):
        df = pd.DataFrame([
            [player_sum, is_soft, num_cards, dealer_card, 0],
            [player_sum, is_soft, num_cards, dealer_card, 1]
        ], columns=['player_sum', 'is_soft', 'num_cards', 'dealer_up', 'action'])

        probs = self.model.predict_proba(df)[:, 1]

        best_action = 0 if probs[0] > probs[1] else 1
        return 'hit' if best_action == 0 else 'stand'
