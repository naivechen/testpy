import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# 一、生成数据
X, y = make_classification(n_samples=200, n_features=20, n_informative=5,
                           n_redundant=2, n_classes=2, random_state=42)
feature_names = [f"Feature_{i}" for i in range(X.shape[1])]
X_df = pd.DataFrame(X, columns=feature_names)

# 二、训练模型
rfc = RandomForestClassifier(n_estimators=71, random_state=42)
score = cross_val_score(rfc, X_df, y, cv=5).mean()
print("5折交叉验证 acc =", round(score, 4))

# 三、SHAP 分析
rfc.fit(X_df, y)
explainer = shap.Explainer(rfc, X_df)
shap_values = explainer(X_df)
print("\n[SHAP] 条形图（自动排序 + 特征名）")
shap.plots.bar(shap_values[:, :, 1])
print("\n[SHAP] 蜂群图（包含特征值 + 方向 + 密度）")
shap.plots.beeswarm(shap_values[:, :, 1])
shap.dependence_plot("Feature_0", shap_values.values[:, :, 1], X_df)
sample_explanation = shap_values[0:1, :, 1]  
shap.plots.force(sample_explanation, matplotlib=True)
