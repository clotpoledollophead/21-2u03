import json, math
from collections import defaultdict
from typing import List

def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))

class Network:
    def __init__(self, data):
        self.bias = {int(k): v["bias"] for k, v in data["nodes"].items()}
        self.layer = {int(k): v["layer"] for k, v in data["nodes"].items()}
        self.weights = {(src, dst): w for src, dst, w, en in data["connections"] if en}
        self.inp, self.out = data["input_keys"], data["output_keys"]
        self.layers = defaultdict(list)
        for k, l in self.layer.items(): self.layers[l].append(k)
    def activate(self, x: List[float]) -> float:
        val = {k: v for k, v in zip(self.inp, x)}
        for l in sorted(k for k in self.layers if k):
            for nid in self.layers[l]:
                s = self.bias[nid]
                for (src, dst), w in self.weights.items():
                    if dst == nid: s += val.get(src, 0) * w
                val[nid] = sigmoid(s)
        return val[self.out[0]]

class NEATAgent:
    def __init__(self, model_path="neat_model.json"):
        with open(model_path, encoding="utf-8") as f: data = json.load(f)
        self.net = Network(data)
    def act(self, player_sum, dealer_card, is_soft, num_cards):
        x = [player_sum/21, dealer_card/10, int(is_soft), num_cards/5]
        return "hit" if self.net.activate(x) > 0.5 else "stand"












