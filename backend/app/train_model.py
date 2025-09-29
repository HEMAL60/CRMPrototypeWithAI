import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
# CORRECTED: Import a more robust model
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score
import joblib
import os

# --- Database Connection ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@db/erp_crm_db")
engine = create_engine(DATABASE_URL)

print("Connecting to the database...")

# --- Data Loading and Preparation ---
items_df = pd.read_sql("SELECT * FROM quotation_items", engine)
products_df = pd.read_sql("SELECT id, product_type, material FROM products", engine)

df = pd.merge(items_df, products_df, left_on='product_id', right_on='id', how='left')
print(f"Successfully loaded {len(df)} records from the database.")

# --- Feature Engineering ---
df_encoded = pd.get_dummies(df, columns=['product_type', 'material'])

y = df_encoded['price']
X = df_encoded.drop(columns=['price', 'id_x', 'id_y', 'quotation_id', 'product_id'], errors='ignore')

# --- Model Training ---
print("Training the Gradient Boosting Regressor model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# CORRECTED: Use the more powerful GradientBoostingRegressor model.
# This model is much less likely to produce negative predictions on this type of data.
model = GradientBoostingRegressor(random_state=42)
model.fit(X_train, y_train)

# --- Model Evaluation ---
y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)
print(f"Model training complete. R-squared score on test data: {score:.2f}")

# --- Save the Model ---
joblib.dump((model, X_train.columns), 'app/ml_model.joblib')
print(f"Model and feature columns saved to app/ml_model.joblib")


