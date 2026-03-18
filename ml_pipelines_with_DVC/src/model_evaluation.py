import numpy as np
import pandas as pd

import pickle
import json
from pathlib import Path

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, roc_auc_score

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FEATURES_DATA_DIR = PROJECT_ROOT / "data" / "features"
MODEL_PATH = PROJECT_ROOT / "model.pkl"
METRICS_PATH = PROJECT_ROOT / "metrics.json"

with MODEL_PATH.open('rb') as model_file:
    clf = pickle.load(model_file)

test_data = pd.read_csv(FEATURES_DATA_DIR / 'test_bow.csv')

X_test = test_data.iloc[:,0:-1].values
y_test = test_data.iloc[:,-1].values

y_pred = clf.predict(X_test)
y_pred_proba = clf.predict_proba(X_test)[:, 1]

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)

metrics_dict={
    'accuracy':accuracy,
    'precision':precision,
    'recall':recall,
    'auc':auc
}

with METRICS_PATH.open('w') as file:
    json.dump(metrics_dict, file, indent=4)
