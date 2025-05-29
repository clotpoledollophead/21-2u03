import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar, Text
from PIL import Image, ImageTk
import os

from blackjack_env import BlackjackEnv
from expectimax_agent import ExpectimaxAgent
from random_agent import RandomAgent
from rfc_agent import RFCAgent
from neat_agent import NEATAgent
from basic_strategy_agent import BasicStrategyAgent

env = BlackjackEnv()
agents = {
    "Random": RandomAgent(),
    "RFC": RFCAgent("rfc_model.pkl"),
    "NEAT": NEATAgent("neat_model.pkl", "neat_config.txt"),
    "BasicStrategy": BasicStrategyAgent(),
    "Expectimax": ExpectimaxAgent()
}
AGENTS = ["Manual"] + list(agents.keys())
CARDS = "cards"

BG = "#03421F"
FG = "#FFD700"
BTN_BG = "#DAA520"
BTN_FG = "black"
TITLE_F = ("Papyrus", 28, "bold")
TEXT_F = ("Comic Sans MS", 16)
BTN_F = ("Comic Sans MS", 14, "bold")

class BJGame:
    def __init__(self, root):
        self.root = root
        self.root.title("♠ Blackjack AI Game")
        self.root.configure(bg=BG)
        self.root.geometry("+0+0")
        self.mode = tk.StringVar(value="Manual")
        self.deck_n = tk.IntVar(value=1)
        self.auto_n = tk.IntVar(value=1)
        self.imgs = {}
        self.load_imgs()

        self.hist = []
        self.stats = {"win": 0, "lose": 0, "draw": 0, "games": 0}
        self.started = False
        self.first_disp = True
        self.left_rounds = 0
        self.res = None

        self.main_f = tk.Frame(self.root, bg=BG)
        self.main_f.pack(expand=True)

        tk.Label(self.main_f, text="♠ Blackjack AI Game ♠", font=TITLE_F, fg=FG, bg=BG).pack(pady=10)

        self.p_f = tk.Frame(self.main_f, bg=BG)
        self.p_f.pack(pady=5)
        tk.Label(self.p_f, text="Player's Hand", font=TEXT_F, fg=FG, bg=BG).pack()
        self.p_cards = tk.Frame(self.p_f, bg=BG)
        self.p_cards.pack()

        self.d_f = tk.Frame(self.main_f, bg=BG)
        self.d_f.pack(pady=5)
        tk.Label(self.d_f, text="Dealer's Hand", font=TEXT_F, fg=FG, bg=BG).pack()
        self.d_cards = tk.Frame(self.d_f, bg=BG)
        self.d_cards.pack()

        self.btn_f = tk.Frame(self.main_f, bg=BG)
        self.btn_f.pack(pady=10)

        self.hit_btn = tk.Button(self.btn_f, text="Hit", font=BTN_F, width=8, bg=BTN_BG, fg=BTN_FG, command=self.hit, state="disabled")
        self.hit_btn.pack(side=tk.LEFT, padx=5)

        self.stand_btn = tk.Button(self.btn_f, text="Stand", font=BTN_F, width=8, bg=BTN_BG, fg=BTN_FG, command=self.stand, state="disabled")
        self.stand_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(self.btn_f, text="History", font=BTN_F, width=10, bg="#8B4513", fg="white", command=self.show_hist).pack(side=tk.LEFT, padx=5)

        tk.Label(self.main_f, text="Player Mode:", font=TEXT_F, fg=FG, bg=BG).pack(pady=5)
        self.menu = tk.OptionMenu(self.main_f, self.mode, *AGENTS, command=self.change_mode)
        self.menu.config(font=TEXT_F, bg=BTN_BG, fg=BTN_FG, width=14)
        self.menu.pack(pady=5)

        self.set_f = tk.Frame(self.main_f, bg=BG)
        self.set_f.pack(pady=5)

        tk.Label(self.set_f, text="Decks (1~8):", font=TEXT_F, fg=FG, bg=BG).grid(row=0, column=0, padx=10)
        self.deck_entry = tk.Spinbox(self.set_f, from_=1, to=8, textvariable=self.deck_n, font=TEXT_F, width=5)
        self.deck_entry.grid(row=0, column=1, padx=10)

        tk.Label(self.set_f, text="Auto Play Rounds:", font=TEXT_F, fg=FG, bg=BG).grid(row=0, column=2, padx=10)
        self.auto_entry = tk.Spinbox(self.set_f, from_=1, to=1000, textvariable=self.auto_n, font=TEXT_F, width=5)
        self.auto_entry.grid(row=0, column=3, padx=10)

        self.ctrl_f = tk.Frame(self.main_f, bg=BG)
        self.ctrl_f.pack(pady=5)

        self.start_btn = tk.Button(self.ctrl_f, text="Start", font=BTN_F, width=10, bg="#4169E1", fg="white", command=self.start_game)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(self.ctrl_f, text="Reset", font=BTN_F, width=10, bg="#B22222", fg="white", command=self.reset_all).pack(side=tk.LEFT, padx=5)

        self.stats_lbl = tk.Label(self.main_f, text="", font=TEXT_F, fg=FG, bg=BG)
        self.stats_lbl.pack(pady=5)

        self.win_lbl = tk.Label(self.main_f, text="", font=TEXT_F, fg=FG, bg=BG)
        self.win_lbl.pack(pady=5)

        self.reset_game()

    def load_imgs(self):
        for file in os.listdir(CARDS):
            if file.endswith(".png"):
                k = file.split(".")[0].upper()
                img = Image.open(os.path.join(CARDS, file)).resize((70, 105))
                self.imgs[k] = ImageTk.PhotoImage(img)

    def change_mode(self, _):
        self.start_btn.config(state="normal")
        self.hit_btn.config(state="disabled")
        self.stand_btn.config(state="disabled")

    def start_game(self):
        self.started = True
        self.first_disp = False
        self.res = None
        self.start_btn.config(state="disabled")
        self.hit_btn.config(state="normal" if self.mode.get() == "Manual" else "disabled")
        self.stand_btn.config(state="normal" if self.mode.get() == "Manual" else "disabled")
        self.left_rounds = self.auto_n.get() if self.mode.get() != "Manual" else 0
        self.reset_game()
        if self.mode.get() != "Manual":
            self.root.after(500, self.auto_play)

    def reset_game(self):
        self.env = BlackjackEnv(num_decks=self.deck_n.get())
        self.env.reset()
        self.update_disp()

    def reset_all(self):
        self.stats = {"win": 0, "lose": 0, "draw": 0, "games": 0}
        self.hist = []
        self.start_btn.config(state="normal")
        self.hit_btn.config(state="disabled")
        self.stand_btn.config(state="disabled")
        self.started = False
        self.first_disp = True
        self.left_rounds = 0
        self.res = None
        messagebox.showinfo("Reset", "All statistics and history have been cleared.")
        self.reset_game()

    def update_disp(self, reveal=False):
        for w in self.p_cards.winfo_children(): w.destroy()
        for w in self.d_cards.winfo_children(): w.destroy()
        if self.first_disp:
            for _ in range(2): tk.Label(self.p_cards, image=self.imgs["BACK"], bg=BG).pack(side=tk.LEFT, padx=4)
            tk.Label(self.d_cards, image=self.imgs["BACK"], bg=BG).pack(side=tk.LEFT, padx=4)
        else:
            for c in self.env.player_hand:
                k = self.get_key(c)
                img = self.imgs.get(k, self.imgs["BACK"])
                tk.Label(self.p_cards, image=img, bg=BG).pack(side=tk.LEFT, padx=4)
            if reveal:
                for c in self.env.dealer_hand:
                    k = self.get_key(c)
                    img = self.imgs.get(k, self.imgs["BACK"])
                    tk.Label(self.d_cards, image=img, bg=BG).pack(side=tk.LEFT, padx=4)
            else:
                if self.env.dealer_hand:
                    k = self.get_key(self.env.dealer_hand[0])
                    img = self.imgs.get(k, self.imgs["BACK"])
                    tk.Label(self.d_cards, image=img, bg=BG).pack(side=tk.LEFT, padx=4)
                    for _ in range(1, len(self.env.dealer_hand)):
                        tk.Label(self.d_cards, image=self.imgs["BACK"], bg=BG).pack(side=tk.LEFT, padx=4)
        g, w, l, d = self.stats["games"], self.stats["win"], self.stats["lose"], self.stats["draw"]
        self.stats_lbl.config(text=f"Games: {g} | Wins: {w} | Losses: {l} | Draws: {d}")
        win_rate = (w / g * 100) if g > 0 else 0
        self.win_lbl.config(text=f"Win Rate: {win_rate:.2f}%")

    def get_key(self, c):
        v, s = c
        return f"{'A' if v==1 else 'J' if v==11 else 'Q' if v==12 else 'K' if v==13 else v}{s}"

    def auto_play(self):
        if not self.started: return
        agent = agents.get(self.mode.get())
        if agent:
            s = self.env.get_obs()
            a = agent.act(s['player_sum'], s['dealer_card'], s['is_soft'], s['num_cards'])
            if a == "hit": self.hit()
            else: self.stand()

    def finish_game(self, res):
        self.stats["games"] += 1
        self.stats[res] += 1
        self.hist.append({"player": self.env.player_hand.copy(), "dealer": self.env.dealer_hand.copy(), "result": res, "mode": self.mode.get()})
        self.update_disp(reveal=True)
        self.left_rounds -= 1
        if self.mode.get() == "Manual":
            self.root.after(500, lambda: self.show_manual_end(res))
        else:
            if self.left_rounds > 0:
                self.root.after(500, self.next_ai)
            elif self.left_rounds == 0:
                self.res = res
                self.root.after(500, lambda: self.show_ai_end(self.res))

    def next_ai(self):
        self.reset_game()
        self.root.after(500, self.auto_play)

    def show_ai_end(self, res):
        d = Toplevel(self.root)
        d.title("Game Over")
        d.configure(bg=BG)
        d.geometry("+0+0")
        d.protocol("WM_DELETE_WINDOW", lambda: self.stop_game(d))
        tk.Label(d, text=f"Result: {res.upper()}", font=TEXT_F, fg=FG, bg=BG).pack(pady=20)
        tk.Button(d, text="Continue", font=BTN_F, width=12, bg="#228B22", fg="white", command=lambda: self.continue_ai_next(d)).pack(pady=10)
        tk.Button(d, text="Stop", font=BTN_F, width=12, bg="#8B0000", fg="white", command=lambda: self.stop_game(d)).pack()

    def show_manual_end(self, res):
        d = Toplevel(self.root)
        d.title("Game Over")
        d.configure(bg=BG)
        d.geometry("+0+0")
        d.protocol("WM_DELETE_WINDOW", lambda: self.stop_game(d))
        tk.Label(d, text=f"Result: {res.upper()}", font=TEXT_F, fg=FG, bg=BG).pack(pady=20)
        tk.Button(d, text="Play Again", font=BTN_F, width=12, bg="#228B22", fg="white", command=lambda: self.restart_manual(d)).pack(pady=10)
        tk.Button(d, text="Stop", font=BTN_F, width=12, bg="#8B0000", fg="white", command=lambda: self.stop_game(d)).pack()

    def restart_manual(self, d):
        d.destroy()
        self.reset_game()
        self.hit_btn.config(state="normal")
        self.stand_btn.config(state="normal")

    def continue_ai_next(self, d):
        d.destroy()
        self.left_rounds = self.auto_n.get()
        self.reset_game()
        self.root.after(500, self.auto_play)

    def stop_game(self, d):
        d.destroy()
        self.started = False
        self.start_btn.config(state="normal")
        self.hit_btn.config(state="disabled")
        self.stand_btn.config(state="disabled")

    def hit(self):
        if not self.started: return
        _, res, done = self.env.player_hit()
        self.update_disp()
        if done:
            self.finish_game(res)
        elif self.mode.get() != "Manual":
            self.root.after(500, self.auto_play)

    def stand(self):
        if not self.started: return
        self.dealer_play()

    def dealer_play(self):
        done = self.env.dealer_draw_one()
        self.update_disp(reveal=False)
        if done:
            self.root.after(500, lambda: self.finish_game(self.env.get_game_result()))
        else:
            self.root.after(500, self.dealer_play)

    def show_hist(self):
        sym = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}
        val = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        red = {'♥', '♦'}
        def fmt(c): v, s = c; return f"{sym.get(s,s)}{val.get(v,str(v))}", sym.get(s,s)
        d = Toplevel(self.root)
        d.title("Game History")
        d.geometry("600x400+0+0")
        d.configure(bg=BG)
        t = Text(d, font=("Consolas", 14), bg=BG, fg=FG, wrap=tk.WORD)
        t.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb = Scrollbar(d, command=t.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        t.config(yscrollcommand=sb.set)
        t.tag_config("red", foreground="red")
        t.tag_config("black", foreground="black")
        if not self.hist:
            t.insert(tk.END, "No game history yet.")
        else:
            for i, h in enumerate(self.hist, 1):
                t.insert(tk.END, f"Game {i} ({h.get('mode', 'Manual')}):\n")
                t.insert(tk.END, "Player: [")
                for idx, c in enumerate(h['player']):
                    s, col = fmt(c)
                    t.insert(tk.END, s, "red" if col in red else "black")
                    if idx != len(h['player']) - 1: t.insert(tk.END, ", ")
                t.insert(tk.END, "]\nDealer: [")
                for idx, c in enumerate(h['dealer']):
                    s, col = fmt(c)
                    t.insert(tk.END, s, "red" if col in red else "black")
                    if idx != len(h['dealer']) - 1: t.insert(tk.END, ", ")
                t.insert(tk.END, f"]\nResult: {h['result'].upper()}\n\n")

root = tk.Tk()
BJGame(root)
root.mainloop()
