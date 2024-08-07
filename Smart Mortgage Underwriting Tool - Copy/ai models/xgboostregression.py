import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd

from sklearn.model_selection import train_test_split

# Load the synthetic data
df = pd.read_csv("synthetic_mortgage_data.csv")

# Define features and target variable
X = df.drop(columns=['Mortgage_Amount'])
y = df['Mortgage_Amount']

# Split the data
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)  # 60% train, 40% temp
X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)  # 50% of temp for valid and test

# Save to CSV
X_train.to_csv("X_train.csv", index=False)
X_valid.to_csv("X_valid.csv", index=False)
X_test.to_csv("X_test.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_valid.to_csv("y_valid.csv", index=False)
y_test.to_csv("y_test.csv", index=False)


# Load training and validation data
X_train = pd.read_csv("X_train.csv")
y_train = pd.read_csv("y_train.csv")
X_valid = pd.read_csv("X_valid.csv")
y_valid = pd.read_csv("y_valid.csv")

# Initialize and train the XGBoost model
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_valid)
mse = mean_squared_error(y_valid, y_pred)
print(f"Validation Mean Squared Error: {mse}")

# Test the model
X_test = pd.read_csv("X_test.csv")
y_test = pd.read_csv("y_test.csv")
y_test_pred = model.predict(X_test)
test_mse = mean_squared_error(y_test, y_test_pred)
print(f"Test Mean Squared Error: {test_mse}")
print(y_test_pred)

