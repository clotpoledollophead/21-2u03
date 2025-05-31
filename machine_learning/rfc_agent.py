import json

class RFCAgent:
    def __init__(self, model_file):
        with open(model_file, 'r') as f:
            self.forest = json.load(f)

    def act(self, player_sum, dealer_card, is_soft, num_cards):
        features = [player_sum, dealer_card, int(is_soft), num_cards]
        votes = []
        for tree in self.forest:
            votes.append(self.predict_tree(features, tree))
        decision = max(set(votes), key=votes.count)
        return "hit" if decision == 0 else "stand"

    def predict_tree(self, x, node):
        if not isinstance(node, dict):
            return node
        if x[node['feature']] <= node['threshold']:
            return self.predict_tree(x, node['left'])
        else:
            return self.predict_tree(x, node['right'])

