"""
Converted from `branch project.ipynb`.
This script follows the notebook cell order; useful markdown kept as comments.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import re
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Load branch dataset
data = pd.read_csv('branch.csv')

# Inspect dataset
data.info()
data.head()

# Normalize text columns to lowercase
data['Country_lowercase'] = data['Country'].str.lower()
data['State_lowercase'] = data['State'].str.lower()
data['City_lowercase'] = data['City'].str.lower()
data['Address_lowercase'] = data['Address'].str.lower()
data.head()

# Tokenize text columns
data['Country_tokenized'] = data.apply(lambda x: word_tokenize(x['Country_lowercase']), axis=1)
data['City_tokenized'] = data.apply(lambda x: word_tokenize(x['City_lowercase']), axis=1)
data['State_tokenized'] = data.apply(lambda x: word_tokenize(x['State_lowercase']), axis=1)
data['Address_tokenized'] = data.apply(lambda x: word_tokenize(x['Address_lowercase']), axis=1)
data.head()

# Lemmatize tokens
lemmatizer = WordNetLemmatizer()

data['Country_lemmatized'] = data['Country_tokenized'].apply(
    lambda tokens: [lemmatizer.lemmatize(token) for token in tokens]
)
data['City_lemmatized'] = data['City_tokenized'].apply(
    lambda tokens: [lemmatizer.lemmatize(token) for token in tokens]
)
data['State_lemmatized'] = data['State_tokenized'].apply(
    lambda tokens: [lemmatizer.lemmatize(token) for token in tokens]
)
data['Address_lemmatized'] = data['Address_tokenized'].apply(
    lambda tokens: [lemmatizer.lemmatize(token) for token in tokens]
)
data.head()

# Combine tokens for spaCy processing
tokens_clean = sum(data['Country_lemmatized'], []) + sum(data['State_lemmatized'], []) + sum(data['Address_lemmatized'], []) + sum(data['City_lemmatized'], [])
data.head()

# Load spaCy model (ensure 'en_core_web_sm' is installed)
nlp = spacy.load("en_core_web_sm")
spacy_doc = nlp(' '.join(tokens_clean))

# POS tagging dataframe
pos_df = pd.DataFrame(columns=['token', 'pos_tag'])
for token in spacy_doc:
    pos_df = pd.concat([
        pos_df,
        pd.DataFrame.from_records([{'token': token.text, 'pos_tag': token.pos_}])
    ], ignore_index=True)

pos_df_counts = pos_df.groupby(['token', 'pos_tag']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
pos_df_counts.head(10)
pos_df_counts.head()

# Named-entity recognition dataframe
ner_df = pd.DataFrame(columns=['token', 'ner_tag'])
for ent in spacy_doc.ents:
    if pd.isna(ent.label_) is False:
        ner_df = pd.concat([
            ner_df,
            pd.DataFrame.from_records([{'token': ent.text, 'ner_tag': ent.label_}])
        ], ignore_index=True)

ner_df.head()
ner_df_counts = ner_df.groupby(['token', 'ner_tag']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
ner_df_counts.head(10)

# Iris dataset example and Logistic Regression
iris = load_iris()
x = iris.data
y = iris.target

print(x)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=45)
lr = LogisticRegression()
lr.fit(x_train, y_train)
y_pred = lr.predict(x_test)
accuracy_score(y_pred, y_test)
print(classification_report(y_test, y_pred))

predicted_species = iris.target_names[y_pred]
actual_species = iris.target_names[y_test]
print("Predicted Species:", predicted_species)
print("Actual Species:", actual_species)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Interactive prediction (keeps original notebook behavior)
print("Enter flower measurement: ")
sepal_length = float(input("Sepal length(cm): "))
sepal_width = float(input("Sepal width(cm):  "))
petal_length = float(input("Petal length(cm): "))
petal_width = float(input("Petal width(cm):  "))
user_input = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
prediction = lr.predict(user_input)
species_name = iris.target_names[prediction[0]]
print("Predicted Species: ", species_name)
