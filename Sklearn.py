import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap

from sklearn.datasets import load_breast_cancer, make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# 一、导入自带 breast_cancer 数据集，因为breast_cancer有560个样本，有31个特征值
cancer = load_breast_cancer()
cancer_X = pd.DataFrame(cancer.data, columns=cancer.feature_names)
cancer_y = cancer.target

print("[Breast Cancer]")
print("X shape:", cancer_X.shape)
print("y shape:", cancer_y.shape)

# 二、随机生成一份 20 个 feature 的分类数据
X, y = make_classification(n_samples=200, n_features=20, n_informative=5, 
                                    n_redundant=2, n_classes=2, random_state=42)
feature_names = [f"Feature_{i}" for i in range(X.shape[1])]
X_df = pd.DataFrame(X, columns=feature_names)

# 三、训练 RandomForest 模型
rfc = RandomForestClassifier(n_estimators=71, random_state=42)#这里的71来自另一份文件算出来的结果
score_pre = cross_val_score(rfc, X_df, y, cv=5).mean()
print("\n[Random Forest Evaluation]")
print("5折交叉验证均值 acc =", round(score_pre, 4))#这里选5折交叉验证是因为那篇论文选了5折交叉验证

# 四、使用SHAP 
rfc.fit(X_df, y)
explainer = shap.TreeExplainer(rfc)  
shap_values = explainer.shap_values(X) 
shap.summary_plot(shap_values, X)