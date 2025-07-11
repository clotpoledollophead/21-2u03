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
    "RFC": RFCAgent("rfc_model.json"),
    "NEAT": NEATAgent("neat_model.json"),
    "BasicStrategy": BasicStrategyAgent(),
    "Expectimax": ExpectimaxAgent()
}
AGENT_OPTIONS = ["Manual"] + list(agents.keys())
CARD_DIR = "cards"

BG_COLOR = "#03421F"
TEXT_COLOR = "#FFD700"
BUTTON_COLOR = "#DAA520"
BUTTON_TEXT_COLOR = "black"
TITLE_FONT = ("Papyrus", 28, "bold")
LABEL_FONT = ("Comic Sans MS", 16)
BUTTON_FONT = ("Comic Sans MS", 14, "bold")

class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("♠ Blackjack AI Game")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("+0+0")

        self.ai_choice = tk.StringVar(value="Manual")
        self.num_decks = tk.IntVar(value=1)
        self.auto_rounds = tk.IntVar(value=1)
        self.card_images = {}
        self.load_card_images()

        self.history = []
        self.stats = {"win": 0, "lose": 0, "draw": 0, "games": 0}
        self.game_started = False
        self.initial_display = True
        self.remaining_auto_rounds = 0
        self.final_result = None

        self.main_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(expand=True)

        tk.Label(self.main_frame, text="♠ Blackjack AI Game ♠", font=TITLE_FONT, fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)

        self.player_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.player_frame.pack(pady=5)
        tk.Label(self.player_frame, text="Player's Hand", font=LABEL_FONT, fg=TEXT_COLOR, bg=BG_COLOR).pack()
        self.player_cards_frame = tk.Frame(self.player_frame, bg=BG_COLOR)
        self.player_cards_frame.pack()

        self.dealer_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.dealer_frame.pack(pady=5)
        tk.Label(self.dealer_frame, text="Dealer's Hand", font=LABEL_FONT, fg=TEXT_COLOR, bg=BG_COLOR).pack()
        self.dealer_cards_frame = tk.Frame(self.dealer_frame, bg=BG_COLOR)
        self.dealer_cards_frame.pack()

        self.button_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.button_frame.pack(pady=10)

        self.hit_button = tk.Button(self.button_frame, text="Hit", font=BUTTON_FONT, width=8, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=self.hit, state="disabled")
        self.hit_button.pack(side=tk.LEFT, padx=5)

        self.stand_button = tk.Button(self.button_frame, text="Stand", font=BUTTON_FONT, width=8, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=self.stand, state="disabled")
        self.stand_button.pack(side=tk.LEFT, padx=5)

        tk.Button(self.button_frame, text="History", font=BUTTON_FONT, width=10, bg="#8B4513", fg="white", command=self.show_history).pack(side=tk.LEFT, padx=5)

        tk.Label(self.main_frame, text="Player Mode:", font=LABEL_FONT, fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=5)
        self.ai_menu = tk.OptionMenu(self.main_frame, self.ai_choice, *AGENT_OPTIONS, command=self.on_ai_mode_change)
        self.ai_menu.config(font=LABEL_FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, width=14)
        self.ai_menu.pack(pady=5)

        self.settings_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.settings_frame.pack(pady=5)

        tk.Label(self.settings_frame, text="Decks (1~8):", font=LABEL_FONT, fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=0, padx=10)
        self.deck_entry = tk.Spinbox(self.settings_frame, from_=1, to=8, textvariable=self.num_decks, font=LABEL_FONT, width=5)
        self.deck_entry.grid(row=0, column=1, padx=10)

        tk.Label(self.settings_frame, text="Auto Play Rounds:", font=LABEL_FONT, fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=2, padx=10)
        self.auto_round_entry = tk.Spinbox(self.settings_frame, from_=1, to=1000, textvariable=self.auto_rounds, font=LABEL_FONT, width=5)
        self.auto_round_entry.grid(row=0, column=3, padx=10)

        self.control_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.control_frame.pack(pady=5)

        self.start_button = tk.Button(self.control_frame, text="Start", font=BUTTON_FONT, width=10, bg="#4169E1", fg="white", command=self.start_game)
        self.start_button.pack(side=tk.LEFT, padx=5)

        tk.Button(self.control_frame, text="Reset", font=BUTTON_FONT, width=10, bg="#B22222", fg="white", command=self.reset_all).pack(side=tk.LEFT, padx=5)

        self.stats_label = tk.Label(self.main_frame, text="", font=LABEL_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
        self.stats_label.pack(pady=5)

        self.win_rate_label = tk.Label(self.main_frame, text="", font=LABEL_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
        self.win_rate_label.pack(pady=5)

        self.reset_game()

    def load_card_images(self):
        for file in os.listdir(CARD_DIR):
            if file.endswith(".png"):
                key = file.split(".")[0].upper()
                img = Image.open(os.path.join(CARD_DIR, file)).resize((70, 105))
                self.card_images[key] = ImageTk.PhotoImage(img)

    def on_ai_mode_change(self, selection):
        self.start_button.config(state="normal")
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")

    def start_game(self):
        self.game_started = True
        self.initial_display = False
        self.final_result = None
        self.start_button.config(state="disabled")
        self.hit_button.config(state="normal" if self.ai_choice.get() == "Manual" else "disabled")
        self.stand_button.config(state="normal" if self.ai_choice.get() == "Manual" else "disabled")
        self.remaining_auto_rounds = self.auto_rounds.get() if self.ai_choice.get() != "Manual" else 0
        self.reset_game()
        if self.ai_choice.get() != "Manual":
            self.root.after(500, self.auto_play)

    def reset_game(self):
        self.env = BlackjackEnv(num_decks=self.num_decks.get())
        self.env.reset()
        self.update_display()

    def reset_all(self):
        self.stats = {"win": 0, "lose": 0, "draw": 0, "games": 0}
        self.history = []
        self.start_button.config(state="normal")
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")
        self.game_started = False
        self.initial_display = True
        self.remaining_auto_rounds = 0
        self.final_result = None
        messagebox.showinfo("Reset", "All statistics and history have been cleared.")
        self.reset_game()

    def update_display(self, reveal_dealer=False):
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        if self.initial_display:
            for _ in range(2):
                tk.Label(self.player_cards_frame, image=self.card_images["BACK"], bg=BG_COLOR).pack(side=tk.LEFT, padx=4)
            tk.Label(self.dealer_cards_frame, image=self.card_images["BACK"], bg=BG_COLOR).pack(side=tk.LEFT, padx=4)
        else:
            for card in self.env.player_hand:
                card_key = self.get_card_key(card)
                img = self.card_images.get(card_key, self.card_images["BACK"])
                tk.Label(self.player_cards_frame, image=img, bg=BG_COLOR).pack(side=tk.LEFT, padx=4)
            if reveal_dealer:
                for card in self.env.dealer_hand:
                    card_key = self.get_card_key(card)
                    img = self.card_images.get(card_key, self.card_images["BACK"])
                    tk.Label(self.dealer_cards_frame, image=img, bg=BG_COLOR).pack(side=tk.LEFT, padx=4)
            else:
                if self.env.dealer_hand:
                    card_key = self.get_card_key(self.env.dealer_hand[0])
                    img = self.card_images.get(card_key, self.card_images["BACK"])
                    tk.Label(self.dealer_cards_frame, image=img, bg=BG_COLOR).pack(side=tk.LEFT, padx=4)
                    for _ in range(1, len(self.env.dealer_hand)):
                        tk.Label(self.dealer_cards_frame, image=self.card_images["BACK"], bg=BG_COLOR).pack(side=tk.LEFT, padx=4)
        total = self.stats["games"]
        wins = self.stats["win"]
        losses = self.stats["lose"]
        draws = self.stats["draw"]
        self.stats_label.config(text=f"Games: {total} | Wins: {wins} | Losses: {losses} | Draws: {draws}")
        win_rate = (wins / total * 100) if total > 0 else 0
        self.win_rate_label.config(text=f"Win Rate: {win_rate:.2f}%")

    def get_card_key(self, card):
        value, suit = card
        if value == 1:
            val_str = "A"
        elif value == 11:
            val_str = "J"
        elif value == 12:
            val_str = "Q"
        elif value == 13:
            val_str = "K"
        else:
            val_str = str(value)
        return f"{val_str}{suit}"

    def auto_play(self):
        if not self.game_started:
            return
        agent_name = self.ai_choice.get()
        if agent_name in agents:
            agent = agents[agent_name]
            state = self.env.get_obs()
            action = agent.act(state['player_sum'], state['dealer_card'], state['is_soft'], state['num_cards'])
            if action == "hit":
                self.hit()
            else:
                self.stand()

    def finish_game(self, result):
        self.stats["games"] += 1
        self.stats[result] += 1
        self.history.append({
            "player": self.env.player_hand.copy(),
            "dealer": self.env.dealer_hand.copy(),
            "result": result,
            "mode": self.ai_choice.get()
        })
        self.update_display(reveal_dealer=True)  

        self.remaining_auto_rounds -= 1

        if self.ai_choice.get() == "Manual":
            self.root.after(500, lambda: self.show_manual_end_dialog(result))
        else:
            if self.remaining_auto_rounds > 0:
                self.root.after(500, self.next_ai_game)
            elif self.remaining_auto_rounds == 0:
                self.final_result = result
                self.root.after(500, lambda: self.show_continue_dialog(self.final_result))

    def next_ai_game(self):
        self.reset_game()
        self.root.after(500, self.auto_play)


    def show_continue_dialog(self, result):
        dialog = Toplevel(self.root)
        dialog.title("Game Over")
        dialog.configure(bg=BG_COLOR)
        dialog.geometry("+0+0")
        dialog.protocol("WM_DELETE_WINDOW", lambda: self.stop_game(dialog))
        tk.Label(dialog, text=f"Result: {result.upper()}", font=LABEL_FONT, fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)
        tk.Button(dialog, text="Continue", font=BUTTON_FONT, width=12, bg="#228B22", fg="white", command=lambda: self.continue_ai_next(dialog)).pack(pady=10)
        tk.Button(dialog, text="Stop", font=BUTTON_FONT, width=12, bg="#8B0000", fg="white", command=lambda: self.stop_game(dialog)).pack()
        
    def show_manual_end_dialog(self, result):
        dialog = Toplevel(self.root)
        dialog.title("Game Over")
        dialog.configure(bg=BG_COLOR)
        dialog.geometry("+0+0")
        tk.Label(dialog, text=f"Result: {result.upper()}", font=LABEL_FONT, fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)
        tk.Button(dialog, text="Play Again", font=BUTTON_FONT, width=12, bg="#228B22", fg="white", command=lambda: self.restart_manual(dialog)).pack(pady=10)
        tk.Button(dialog, text="Stop", font=BUTTON_FONT, width=12, bg="#8B0000", fg="white", command=lambda: self.stop_game(dialog)).pack()

    def restart_manual(self, dialog):
        dialog.destroy()
        self.reset_game()
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")
     
    def continue_ai_next(self, dialog):
        dialog.destroy()
        self.remaining_auto_rounds = self.auto_rounds.get()
        self.reset_game()
        self.root.after(500, self.auto_play)

    def stop_game(self, dialog):
        dialog.destroy()
        self.game_started = False
        self.start_button.config(state="normal")
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")

    def hit(self):
        if not self.game_started:
            return
        self.state, result, done = self.env.player_hit()
        self.update_display()
        if done:
            self.finish_game(result)
        elif self.ai_choice.get() != "Manual":
            self.root.after(500, self.auto_play)

    def stand(self):
        if not self.game_started:
            return
        self.dealer_play()

    def dealer_play(self):
        done = self.env.dealer_draw_one()
        self.update_display(reveal_dealer=False)
        if done:
            self.root.after(500, lambda: self.finish_game(self.env.get_game_result()))
        else:
            self.root.after(500, self.dealer_play)

    def show_history(self):
        suit_symbols = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}
        value_map = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        red_suits = {'♥', '♦'}
        def format_card(card):
            value, suit = card
            return f"{suit_symbols.get(suit, suit)}{value_map.get(value, str(value))}", suit_symbols.get(suit, suit)
        history_win = Toplevel(self.root)
        history_win.title("Game History")
        history_win.geometry("600x400+0+0")
        history_win.configure(bg=BG_COLOR)
        text = Text(history_win, font=("Consolas", 14), bg=BG_COLOR, fg=TEXT_COLOR, wrap=tk.WORD)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = Scrollbar(history_win, command=text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.config(yscrollcommand=scrollbar.set)
        text.tag_config("red", foreground="red")
        text.tag_config("black", foreground="black")
        if not self.history:
            text.insert(tk.END, "No game history yet.")
        else:
            for i, h in enumerate(self.history, 1):
                text.insert(tk.END, f"Game {i} ({h.get('mode', 'Manual')}):\n")
                text.insert(tk.END, "Player: [")
                for idx, c in enumerate(h['player']):
                    card_str, suit_symbol = format_card(c)
                    tag = "red" if suit_symbol in red_suits else "black"
                    text.insert(tk.END, card_str, tag)
                    if idx != len(h['player']) - 1:
                        text.insert(tk.END, ", ")
                text.insert(tk.END, "]\n")
                text.insert(tk.END, "Dealer: [")
                for idx, c in enumerate(h['dealer']):
                    card_str, suit_symbol = format_card(c)
                    tag = "red" if suit_symbol in red_suits else "black"
                    text.insert(tk.END, card_str, tag)
                    if idx != len(h['dealer']) - 1:
                        text.insert(tk.END, ", ")
                text.insert(tk.END, "]\n")
                text.insert(tk.END, f"Result: {h['result'].upper()}\n\n")

root = tk.Tk()
gui = BlackjackGUI(root)
root.mainloop()


