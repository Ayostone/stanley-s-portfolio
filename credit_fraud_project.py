"""
Converted from `credit fraud project.ipynb`.
This script contains the code cells in execution order.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load your dataset
data = pd.read_csv('creditcard.csv')

# Display basic information about the dataset
data.info()

data.head(30)

# Check for missing values
data.isna().sum().sum()

# Show a summary of the dataset
data.describe

# Analyze the class distribution
data['Class'].value_counts(normalize=True)

# The dataset is highly imbalanced, so accuracy is not a reliable metric, and class imbalance handling is required.

# Split the data into features (x) and target variable (y)
x = data.drop(columns=['Class'])
y = data['Class']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

# Initialize the XGBoost classifier
xg = XGBClassifier()

# Define hyperparameter grid for RandomizedSearchCV
param_dist_xg = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 6, 9],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0],
    'objective': ['binary:logistic'],
    'eval_metric': ['logloss'],
    'scale_pos_weight': [1, 10, 25, 50, 75, 100]
    }

# Set up RandomizedSearchCV for XGBoost
xg_random = RandomizedSearchCV(estimator=xg,
                               param_distributions=param_dist_xg,   
                               n_iter=10,
                               cv=3,
                               verbose=2,
                               random_state=42,
                               scoring='roc_auc',
                               n_jobs=-1
                               )

# Fit the RandomizedSearchCV to the training data
xg_random.fit(x_train, y_train)

# Get the best estimator from the random search
xg_random_new = xg_random.best_estimator_
print(xg_random.best_params_)
print(xg_random.best_score_)

# Make predictions on the test set
y_pred_xg = xg_random_new.predict(x_test)

# Evaluate the model
print("XGBoost Classifier Results:")
print(classification_report(y_test, y_pred_xg))
print("Accuracy:", accuracy_score(y_test, y_pred_xg))
