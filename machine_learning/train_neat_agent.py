import math, random, os, json
from collections import defaultdict
from blackjack_env import BlackjackEnv

def sigmoid(x): return 1 / (1 + math.exp(-x))

class Node:
    def __init__(self, key, bias=None, layer=None):
        self.key = key
        self.bias = random.uniform(-1, 1) if bias is None else bias
        self.layer = layer

class Conn:
    def __init__(self, src, dst, weight=None, enabled=True, tag=None):
        self.src = src
        self.dst = dst
        self.weight = random.uniform(-1, 1) if weight is None else weight
        self.enabled = enabled
        self.tag = tag

class Tracker:
    def __init__(self):
        self.next_id = 0
        self.records = {}
    def get(self, src, dst):
        k = (src, dst)
        if k not in self.records:
            self.next_id += 1
            self.records[k] = self.next_id
        return self.records[k]
tracker = Tracker()

class Genome:
    def __init__(self, gid, cfg):
        self.gid, self.cfg, self.fitness = gid, cfg, None
        self.nodes = {}
        self.conns = {}
        for k in cfg.inputs:
            self.nodes[k] = Node(k, layer=0)
        for k in cfg.outputs:
            self.nodes[k] = Node(k, layer=1)
        for i in cfg.inputs:
            for o in cfg.outputs:
                self.conns[(i, o)] = Conn(i, o, tag=tracker.get(i, o))
    def add_conn(self):
        src = random.choice(list(self.nodes))
        dst = random.choice(list(self.nodes))
        if src == dst or (src, dst) in self.conns: return
        if self.nodes[src].layer >= self.nodes[dst].layer:
            self.nodes[dst].layer = self.nodes[src].layer + 1
        self.conns[(src, dst)] = Conn(src, dst, tag=tracker.get(src, dst))
    def add_node(self):
        if not self.conns: return
        c = random.choice(list(self.conns.values()))
        if not c.enabled: return
        c.enabled = False
        new_k = max(self.nodes) + 1
        self.nodes[new_k] = Node(new_k, layer=self.nodes[c.src].layer + 1)
        self.conns[(c.src, new_k)] = Conn(c.src, new_k, weight=1.0, tag=tracker.get(c.src, new_k))
        self.conns[(new_k, c.dst)] = Conn(new_k, c.dst, weight=c.weight, tag=tracker.get(new_k, c.dst))
    def mutate_weights(self):
        for c in self.conns.values():
            if random.random() < 0.9:
                c.weight += random.gauss(0, 0.3)
            else:
                c.weight = random.uniform(-1, 1)
            c.weight = max(min(c.weight, 5), -5)
    def mutate_biases(self):
        for n in self.nodes.values():
            if random.random() < 0.9:
                n.bias += random.gauss(0, 0.3)
            else:
                n.bias = random.uniform(-1, 1)
            n.bias = max(min(n.bias, 5), -5)
    def mutate(self):
        if random.random() < 0.8: self.mutate_weights()
        if random.random() < 0.8: self.mutate_biases()
        if random.random() < 0.03: self.add_conn()
        if random.random() < 0.05: self.add_node()
    @staticmethod
    def crossover(p1, p2, cfg):
        if p2.fitness > p1.fitness: p1, p2 = p2, p1
        child = Genome(None, cfg)
        child.nodes = {k: Node(k, n.bias, n.layer) for k, n in p1.nodes.items()}
        child.conns = {}
        for k, c in p1.conns.items():
            other = p2.conns.get(k, c)
            chosen = other if random.random() < 0.5 else c
            child.conns[k] = Conn(chosen.src, chosen.dst, chosen.weight, chosen.enabled, chosen.tag)
        return child
    def to_dict(self):
        return {
            "nodes": {str(k): {"bias": n.bias, "layer": n.layer} for k, n in self.nodes.items()},
            "connections": [[c.src, c.dst, c.weight, c.enabled] for c in self.conns.values()],
            "input_keys": self.cfg.inputs,
            "output_keys": self.cfg.outputs
        }

class Config:
    def __init__(self, path):
        self.params = {}
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line: continue
                k, v = line.split("=", 1)
                self.params[k.strip()] = v.strip()
        self.inputs = list(range(int(self.params["num_inputs"])))
        self.outputs = [i + len(self.inputs) for i in range(int(self.params["num_outputs"]))]
        self.pop_size = int(self.params["pop_size"])
        self.compat_thresh = float(self.params["compatibility_threshold"])
        self.elitism = int(self.params["elitism"])

class Species:
    def __init__(self, rep): self.rep = rep; self.members = []

class SpeciesSet:
    def __init__(self, cfg): self.cfg = cfg; self.species = []
    def distance(self, g1, g2):
        c1, c2 = g1.conns, g2.conns
        disjoint = len(set(c1) ^ set(c2))
        w_diff = sum(abs(c1[k].weight - c2[k].weight) for k in c1 if k in c2) / (len(c1) + 1e-6)
        return disjoint + w_diff
    def speciate(self, pop):
        self.species.clear()
        for g in pop:
            placed = False
            for s in self.species:
                if self.distance(g, s.rep) < self.cfg.compat_thresh:
                    s.members.append(g)
                    placed = True
                    break
            if not placed:
                s = Species(g); s.members.append(g); self.species.append(s)
        for s in self.species:
            s.rep = random.choice(s.members)

class Population:
    def __init__(self, cfg):
        self.cfg = cfg
        self.genomes = {i: Genome(i, cfg) for i in range(cfg.pop_size)}
        self.species = SpeciesSet(cfg)
        self.gen = 0
    def evaluate(self):
        env = BlackjackEnv()
        for g in self.genomes.values():
            net = Network(g)
            total = 0
            for _ in range(1000):
                state, done = env.reset(), False
                while not done:
                    x = [state["player_sum"]/21, state["dealer_card"]/10, int(state["is_soft"]), len(env.player_hand)/5]
                    action = "hit" if net.activate(x)[0] > 0.5 else "stand"
                    state, reward, done = env.step(action)
                    total += reward
            g.fitness = total
    def reproduce(self):
        self.species.speciate(list(self.genomes.values()))
        total_fit = max(sum(max(0, g.fitness) for g in self.genomes.values()), 1e-6)
        spawn = {}
        for s in self.species.species:
            s_fit = sum(max(0, g.fitness) for g in s.members)
            spawn[s] = max(1, int(s_fit / total_fit * self.cfg.pop_size))
        new_gen = {}
        gid = 0
        for s in self.species.species:
            s.members.sort(key=lambda g: g.fitness, reverse=True)
            elites = s.members[:self.cfg.elitism]
            for e in elites:
                c = Genome(gid, self.cfg)
                c.nodes = {k: Node(k, n.bias, n.layer) for k, n in e.nodes.items()}
                c.conns = {k: Conn(v.src, v.dst, v.weight, v.enabled, v.tag) for k, v in e.conns.items()}
                new_gen[gid] = c; gid += 1
            for _ in range(spawn[s] - len(elites)):
                p1, p2 = random.sample(s.members, 2)
                child = Genome.crossover(p1, p2, self.cfg)
                child.gid = gid
                child.mutate()
                new_gen[gid] = child; gid += 1
        while len(new_gen) < self.cfg.pop_size:
            g = Genome(len(new_gen), self.cfg)
            new_gen[g.gid] = g
        self.genomes = new_gen
        self.gen += 1

class Network:
    def __init__(self, g):
        self.bias = {k: n.bias for k, n in g.nodes.items()}
        self.layer = {k: n.layer for k, n in g.nodes.items()}
        self.weights = {(c.src, c.dst): c.weight for c in g.conns.values() if c.enabled}
        self.inputs, self.outputs = g.cfg.inputs, g.cfg.outputs
        self.layers = defaultdict(list)
        for k, l in self.layer.items(): self.layers[l].append(k)
    def activate(self, x):
        vals = {k: v for k, v in zip(self.inputs, x)}
        for l in sorted(k for k in self.layers if k):
            for nid in self.layers[l]:
                s = self.bias[nid]
                for (src, dst), w in self.weights.items():
                    if dst == nid: s += vals.get(src, 0) * w
                vals[nid] = sigmoid(s)
        return [vals.get(k, 0) for k in self.outputs]

def train(cfg_path="neat_config.txt", gens=50, out="neat_model.json"):
    cfg = Config(cfg_path)
    pop = Population(cfg)
    best = None
    for _ in range(gens):
        pop.evaluate()
        top = max(pop.genomes.values(), key=lambda g: g.fitness)
        if best is None or top.fitness > best.fitness: best = top
        print(f"Gen {pop.gen:3d}  Best {top.fitness:10.3f}")
        pop.reproduce()
    with open(out, "w", encoding="utf-8") as f: json.dump(best.to_dict(), f)
    print("Saved", out)

if __name__ == "__main__":
    train(os.path.join(os.path.dirname(__file__), "neat_config.txt"))
