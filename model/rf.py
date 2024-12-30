import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

def predict(arr):
    # df = pd.read_csv("model/dataset.csv")
    # X = df.drop(["shape"], axis=1).copy()
    # y = pd.get_dummies(df["shape"]).copy()

    # rf = RandomForestClassifier(
    #     n_estimators=100,
    #     max_depth=30,
    #     min_samples_leaf=2
    #     )

    # rf.fit(X, y)
    # joblib.dump(rf, "model/model.pkl")
    rf = joblib.load("model/model.pkl")

    arr = np.array(arr).reshape(1, -1)
    pp = rf.predict_proba(arr)

    return getPercentages(pp)


def getPercentages(arr):
    ret = []
    for i in arr:
        ret.append(i[0][1])
    return ret