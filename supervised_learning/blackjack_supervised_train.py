import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.base import clone
import joblib
from tqdm import tqdm  # 進度條套件

# 載入資料
df = pd.read_csv("blkjckhands.csv")

# 根據基本策略建立標籤
def basic_strategy(player_sum, dealer_card):
    if player_sum >= 17:
        return "stand"
    elif player_sum <= 11:
        return "hit"
    else:
        return "hit" if dealer_card >= 7 else "stand"

df['action'] = df.apply(lambda r: basic_strategy(r['sumofcards'], r['dealcard1']), axis=1)

# 特徵與標籤
X = df[['sumofcards', 'dealcard1']]
y = df['action']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 模擬逐棵樹訓練進度（自訂 RF 組合）
n_estimators = 100
trees = []
progress_bar = tqdm(total=n_estimators, desc="訓練中", ncols=80)

# 訓練每棵樹（逐步組合成 RandomForest）
for i in range(n_estimators):
    model = RandomForestClassifier(n_estimators=1, warm_start=True, random_state=42)
    if i == 0:
        rf = model
    else:
        rf.n_estimators += 1
    rf.fit(X_train, y_train)
    progress_bar.update(1)

progress_bar.close()

# 預測與評估
y_pred = rf.predict(X_test)
print("\n分類報告：\n", classification_report(y_test, y_pred))

# 儲存模型
joblib.dump(rf, "blackjack_strategy_model.pkl")
print("✅ 模型已儲存為 blackjack_strategy_model.pkl")
