import numpy as np
import pandas as pd

from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
FEATURES_DATA_DIR = PROJECT_ROOT / "data" / "features"

# fetch the data from data/processed
train_data = pd.read_csv(PROCESSED_DATA_DIR / 'train_processed.csv')
test_data = pd.read_csv(PROCESSED_DATA_DIR / 'test_processed.csv')

train_data.fillna('',inplace=True)
test_data.fillna('',inplace=True)

# apply BoW
X_train = train_data['content'].values
y_train = train_data['sentiment'].values

X_test = test_data['content'].values
y_test = test_data['sentiment'].values

# Apply Bag of Words (CountVectorizer)
vectorizer = CountVectorizer(max_features=50)

# Fit the vectorizer on the training data and transform it
X_train_bow = vectorizer.fit_transform(X_train)

# Transform the test data using the same vectorizer
X_test_bow = vectorizer.transform(X_test)

train_df = pd.DataFrame(X_train_bow.toarray())

train_df['label'] = y_train

test_df = pd.DataFrame(X_test_bow.toarray())

test_df['label'] = y_test

# store the data inside data/features
FEATURES_DATA_DIR.mkdir(parents=True, exist_ok=True)

train_df.to_csv(FEATURES_DATA_DIR / "train_bow.csv", index=False)
test_df.to_csv(FEATURES_DATA_DIR / "test_bow.csv", index=False)
