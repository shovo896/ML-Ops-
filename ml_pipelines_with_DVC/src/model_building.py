import numpy as np
import pandas as pd
import pickle
from pathlib import Path

from sklearn.ensemble import GradientBoostingClassifier

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FEATURES_DATA_DIR = PROJECT_ROOT / "data" / "features"
MODEL_PATH = PROJECT_ROOT / "model.pkl"

# fetch the data from data/processed
train_data = pd.read_csv(FEATURES_DATA_DIR / 'train_bow.csv')

X_train = train_data.iloc[:,0:-1].values
y_train = train_data.iloc[:,-1].values

# Define and train the XGBoost model

clf = GradientBoostingClassifier(n_estimators=50)
clf.fit(X_train, y_train)

# save
with MODEL_PATH.open('wb') as model_file:
    pickle.dump(clf, model_file)
