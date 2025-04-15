import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
df = pd.read_json("Results.json")
y = df["Patient Category"]
X = df.select_dtypes(include=["int64", "float64"])
X = X.fillna(X.mean())
rfc = RandomForestClassifier(n_estimators=38, random_state=42)
score_pre = cross_val_score(rfc, X, y, cv=7).mean()
print("基础模型的平均准确率 acc =", score_pre)