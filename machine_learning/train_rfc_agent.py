import pandas as pd
import ast
import numpy as np
import random
from collections import Counter
from tqdm import tqdm
import json

class DecisionTree:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X, y):
        self.tree = self._build_tree(X, y, depth=0)

    def _gini(self, y):
        counts = Counter(y)
        impurity = 1.0
        for label in counts:
            prob = counts[label] / len(y)
            impurity -= prob ** 2
        return impurity

    def _best_split(self, X, y):
        best_gain = -1
        best_feature, best_threshold = None, None
        current_gini = self._gini(y)

        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_mask = X[:, feature] <= threshold
                right_mask = ~left_mask
                if sum(left_mask) == 0 or sum(right_mask) == 0:
                    continue
                left_y, right_y = y[left_mask], y[right_mask]
                gain = current_gini - (
                    len(left_y) / len(y) * self._gini(left_y) +
                    len(right_y) / len(y) * self._gini(right_y)
                )
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
        return best_feature, best_threshold

    def _build_tree(self, X, y, depth):
        if depth >= self.max_depth or len(set(y)) == 1:
            return int(Counter(y).most_common(1)[0][0])

        feature, threshold = self._best_split(X, y)
        if feature is None:
            return int(Counter(y).most_common(1)[0][0])

        left_mask = X[:, feature] <= threshold
        right_mask = ~left_mask

        return {
            'feature': int(feature),
            'threshold': float(threshold),
            'left': self._build_tree(X[left_mask], y[left_mask], depth+1),
            'right': self._build_tree(X[right_mask], y[right_mask], depth+1)
        }

    def predict_one(self, x, node=None):
        if node is None:
            node = self.tree
        if not isinstance(node, dict):
            return node
        if x[node['feature']] <= node['threshold']:
            return self.predict_one(x, node['left'])
        else:
            return self.predict_one(x, node['right'])

    def predict(self, X):
        return np.array([self.predict_one(x) for x in X])

class RandomForest:
    def __init__(self, n_trees=5, max_depth=5):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.trees = []

    def fit(self, X, y):
        self.trees = []
        for _ in tqdm(range(self.n_trees), desc="Training Trees"):
            indices = np.random.choice(len(X), len(X), replace=True)
            tree = DecisionTree(self.max_depth)
            tree.fit(X[indices], y[indices])
            self.trees.append(tree)

    def predict(self, X):
        all_preds = np.array([tree.predict(X) for tree in self.trees])
        final_preds = []
        for i in range(X.shape[0]):
            votes = all_preds[:, i]
            final_preds.append(int(Counter(votes).most_common(1)[0][0]))
        return np.array(final_preds)

def convert_to_builtin(obj):
    if isinstance(obj, dict):
        return {k: convert_to_builtin(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_builtin(v) for v in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    else:
        return obj

if __name__ == "__main__":
    df = pd.read_csv("blackjack_simulator.csv", nrows=500000)
    X, y = [], []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing Data"):
        try:
            hand = ast.literal_eval(row['initial_hand'])
            actions = ast.literal_eval(row['actions_taken'])[0]
            for action in actions:
                player_sum = sum(hand)
                is_soft = int(11 in hand and player_sum <= 21)
                features = [player_sum, int(row['dealer_up']), is_soft, len(hand)]
                label = 0 if action == 'H' else 1
                X.append(features)
                y.append(label)
                if action == 'H':
                    hand.append(random.choice([2,3,4,5,6,7,8,9,10,11]))
        except:
            continue

    X = np.array(X)
    y = np.array(y)

    model = RandomForest(n_trees=5, max_depth=5)
    model.fit(X, y)
    
    forest_structure = [tree.tree for tree in model.trees]
    forest_structure = convert_to_builtin(forest_structure)

    with open('rfc_model.json', 'w') as f:
        json.dump(forest_structure, f)

    print("RFC model trained and saved as rfc_model.json")
    
    # Calculate and print best accuracy
    accuracies = []
    for tree in model.trees:
        preds = tree.predict(X)
        acc = np.mean(preds == y)
        accuracies.append(acc)

    best_acc = max(accuracies)
    print(f"Best Training Accuracy: {best_acc:.4f}")

