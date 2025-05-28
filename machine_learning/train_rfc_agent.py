import pandas as pd
import ast
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("blackjack_simulator.csv", nrows=100000)

data_rows = []

for idx, row in tqdm(df.iterrows(), total=len(df), desc="整理決策資料"):
    try:
        initial_hand = ast.literal_eval(row['initial_hand'])
        dealer_up = row['dealer_up']
        actions_taken = ast.literal_eval(row['actions_taken'])[0]
        win_label = 1 if row['win'] > 0 else 0

        player_cards = initial_hand.copy()
        for action in actions_taken:
            player_sum = sum(player_cards)
            is_soft = int(11 in player_cards and player_sum <= 21)
            num_cards = len(player_cards)
            action_num = 0 if action == 'H' else 1

            data_rows.append({
                'player_sum': player_sum,
                'is_soft': is_soft,
                'num_cards': num_cards,
                'dealer_up': dealer_up,
                'action': action_num,
                'win': win_label
            })

            if action == 'H':
                player_cards.append(0)
            elif action == 'S':
                break
    except Exception:
        continue

train_df = pd.DataFrame(data_rows)

X = train_df[['player_sum', 'is_soft', 'num_cards', 'dealer_up', 'action']]
y = train_df['win']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\n分類報告:")
print(classification_report(y_test, y_pred))

joblib.dump(model, "rfc_model.pkl")
print("模型已儲存為 rfc_model.pkl")
