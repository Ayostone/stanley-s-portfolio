"""
Converted from `diabetes dataset project.ipynb`.
This script contains the code cells in execution order.
"""

import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
data = pd.read_csv('diabetes.csv')

# Display information about the dataset
data.info()

# display the first few rows of the dataset
data.head()

# Check for missing values
data.isna().sum().sum()

# analyze the outcome variable distribution
data['Outcome'].value_counts(normalize=True)

# Split the dataset into features and target variable
x = data.drop('Outcome', axis=1)
y = data['Outcome']

# Split the dataset into training and testing sets with stratification
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

# Initialize the XGBoost classifier
xg = XGBClassifier(use_label_encoder=False, eval_metric='logloss', scale_pos_weight= 1.85)

# Set up RandomizedSearchCV
xg_parameters = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 6, 9],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0],
    'objective': ['binary:logistic'],
    'eval_metric': ['logloss'],
    'scale_pos_weight': [1, 10, 25, 50, 75, 100]
    }

# Set up RandomizedSearchCV
xg_random = RandomizedSearchCV(estimator=xg,
                                 param_distributions=xg_parameters,
                                 n_iter=50,
                                 scoring='recall',
                                 cv=5,
                                 verbose=1,
                                 random_state=42,
                                 n_jobs=-1,
                                 )

# Fit the RandomizedSearchCV to the training data
xg_random.fit(x_train, y_train)

# Output the best hyperparameters and score
print("Best Hyperparameters:", xg_random.best_params_)
print("Best Score:", xg_random.best_score_)

# Retrieve the best estimator
xg_random_new = xg_random.best_estimator_

# Make predictions on the test set
y_pred = xg_random_new.predict(x_test)

# Evaluate the model
print("XGBoost classifier results:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
