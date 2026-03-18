import numpy as np
import pandas as pd

from pathlib import Path

import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

# fetch the data from data/raw
train_data = pd.read_csv(RAW_DATA_DIR / 'train.csv')
test_data = pd.read_csv(RAW_DATA_DIR / 'test.csv')

# transform the data
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

def lemmatization(text):
    lemmatizer= WordNetLemmatizer()

    text = text.split()

    text=[lemmatizer.lemmatize(y) for y in text]

    return " " .join(text)

def remove_stop_words(text):
    stop_words = set(stopwords.words("english"))
    Text=[i for i in str(text).split() if i not in stop_words]
    return " ".join(Text)

def removing_numbers(text):
    text=''.join([i for i in text if not i.isdigit()])
    return text

def lower_case(text):

    text = text.split()

    text=[y.lower() for y in text]

    return " " .join(text)

def removing_punctuations(text):
    ## Remove punctuations
    punctuation_chars = string.punctuation + "،؟؛"
    text = re.sub(f"[{re.escape(punctuation_chars)}]", ' ', text)

    ## remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text =  " ".join(text.split())
    return text.strip()

def removing_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def remove_small_sentences(df):
    for i in range(len(df)):
        if len(df.text.iloc[i].split()) < 3:
            df.text.iloc[i] = np.nan

def normalize_text(df):
    df = df.copy()
    df.content=df.content.apply(lambda content : lower_case(content))
    df.content=df.content.apply(lambda content : remove_stop_words(content))
    df.content=df.content.apply(lambda content : removing_numbers(content))
    df.content=df.content.apply(lambda content : removing_punctuations(content))
    df.content=df.content.apply(lambda content : removing_urls(content))
    df.content=df.content.apply(lambda content : lemmatization(content))
    return df

train_processed_data = normalize_text(train_data)
test_processed_data = normalize_text(test_data)

# store the data inside data/processed
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

train_processed_data.to_csv(PROCESSED_DATA_DIR / "train_processed.csv", index=False)
test_processed_data.to_csv(PROCESSED_DATA_DIR / "test_processed.csv", index=False)
