"""
One-off script to train the quotation prediction model.

This script connects to the database, fetches all historical quotation items,
trains a simple linear regression model, and saves the trained model
and the feature columns to a file for the main application to use.
"""
import os
import pandas as pd
import joblib
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# --- Database Connection ---
# Read the database URL from the same environment variable as the main app
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@db/erp_crm_db")
engine = create_engine(DATABASE_URL)

print("Connecting to the database...")

# --- Data Loading ---
# A SQL query to get all the data needed for training.
# We join quotation_items with products to get the categorical features.
query = """
SELECT
    qi.width,
    qi.height,
    qi.quantity,
    p.product_type,
    p.material,
    qi.price AS target_price -- This is the value we want to predict
FROM
    quotation_items qi
JOIN
    products p ON qi.product_id = p.id;
"""

df = pd.read_sql(query, engine)
print(f"Successfully loaded {len(df)} records from the database.")

# --- Feature Engineering ---
# Convert categorical variables into dummy/indicator variables (one-hot encoding).
# This is a crucial step for the linear regression model.
features = pd.get_dummies(df, columns=['product_type', 'material'], drop_first=True)

# Separate our features (X) from the target variable (y)
X = features.drop('target_price', axis=1)
y = features['target_price']

# --- Model Training ---
print("Training the Linear Regression model...")
# Split data for a simple validation (optional but good practice)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model on the test set
score = model.score(X_test, y_test)
print(f"Model training complete. R-squared score on test data: {score:.2f}")

# --- Model Saving ---
# It's critical to save not just the model, but also the columns it was trained on.
# This ensures we can recreate the exact same feature set during prediction.
model_data = {
    'model': model,
    'columns': X_train.columns.tolist()
}

# The model will be saved inside the 'app' directory so the main API can access it.
model_path = "app/ml_model.joblib"
joblib.dump(model_data, model_path)

print(f"Model and feature columns saved to {model_path}")
