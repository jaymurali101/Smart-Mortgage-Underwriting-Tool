#this is used for the final loan amount and we are using xgboost specifically because it incorporates
#numerical values and categorical values 

import pandas as pd 
    
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Example dataset
data = {
    'section_header': ['Income', 'Assets', 'Liabilities', 'Property', 'Income', 'Assets'],
    'value': [60000, 150000, 50000, 300000, 55000, 140000],
    'other_feature': [1, 2, 3, 4, 1, 2],
    'mortgage_amount': [200000, 300000, 150000, 400000, 210000, 290000]  # target variable
}
df = pd.DataFrame(data)

# One-hot encode categorical features - turning categorical features in numerical values for machinee
encoded_df = pd.get_dummies(df, columns=['section_header'], drop_first=True)

# Define features and target
X = encoded_df.drop('mortgage_amount', axis=1)
y = encoded_df['mortgage_amount']

# Split the data into training, validation, and test sets 
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Initialize the XGBoost Regressor 
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=5)

# Train the model
model.fit(X_train, y_train, eval_set=[(X_valid, y_valid)], early_stopping_rounds=10, verbose=True)

# Predict on the test set 
y_pred = model.predict(X_test)

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Additional evaluation metrics can be added here

# Example new data
new_data = {
    'other_feature': [2],
    'section_header_Assets': [1],
    'section_header_Income': [0],
    'section_header_Liabilities': [0],
    'section_header_Property': [0]
 
}

variable_color = rgb[2]
faker = Faker()
db = ConnectionAbortedError
db.add_note('section_header_Property')


# Predict the mortgage amount
predicted_mortgage_amount = model.predict(new_df)
print(f"Predicted Mortgage Amount: {predicted_mortgage_amount[0]}") 




