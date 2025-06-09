from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
data = load_breast_cancer()
X = data.data
y = data.target

print("数据维度：", X.shape)
print("标签类别：", data.target_names)
rfc = RandomForestClassifier(n_estimators=100, random_state=90)
score_pre = cross_val_score(rfc, X, y, cv=10).mean()
print("原始模型准确率 acc =", round(score_pre, 4))
scorel = []
for i in range(1, 201, 10):
    clf = RandomForestClassifier(n_estimators=i, n_jobs=-1, random_state=90)
    score = cross_val_score(clf, X, y, cv=10).mean()
    scorel.append(score)

plt.figure(figsize=[20, 5])
plt.plot(range(1, 201, 10), scorel, marker='o')
plt.xlabel("n_estimators")
plt.ylabel("Accuracy (Cross-Validated)")
plt.title("乳腺癌数据集：n_estimators 学习曲线")
plt.grid(True)
plt.show()
best_score = max(scorel)
best_index = scorel.index(best_score)
best_n = (best_index * 10) + 1
print(f"最大准确率：{best_score:.4f}，对应的 n_estimators 为：{best_n}")