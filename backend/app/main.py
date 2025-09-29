"""
Main FastAPI application file.
Defines API endpoints for customers, products, quotations, and AI features.
"""
import joblib
import pandas as pd
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from . import database, schemas, security
from sqlalchemy.orm import Session

# --- AI Model Loading ---
# Load the trained model and feature columns when the application starts.
try:
    model_data = joblib.load("app/ml_model.joblib")
    model = model_data['model']
    model_columns = model_data['columns']
    print("AI model loaded successfully.")
except FileNotFoundError:
    print("AI model not found. Run train_model.py to create it.")
    model = None
    model_columns = None

app = FastAPI(
    title="Reliant Windows ERP/CRM API",
    description="API for managing customers, products, and quotations.",
    version="0.1.0"
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- AI Endpoints ---
@app.post("/predict_quote", response_model=schemas.QuotePredictionResponse, tags=["AI Features"])
def predict_quote_price(request: schemas.QuotePredictionRequest):
    """
    Predict the price of a single quotation item using the trained AI model.
    """
    if not model or not model_columns:
        raise HTTPException(
            status_code=503, 
            detail="AI Model is not available. Please train the model first."
        )

    # 1. Create a DataFrame from the input request
    input_data = pd.DataFrame([request.dict()])
    
    # 2. One-hot encode the categorical features
    input_data = pd.get_dummies(input_data, columns=['product_type', 'material'])
    
    # 3. Align columns with the training data
    # This ensures the prediction data has the exact same structure as the training data.
    input_data = input_data.reindex(columns=model_columns, fill_value=0)
    
    # 4. Make a prediction
    prediction = model.predict(input_data)[0]
    
    return schemas.QuotePredictionResponse(predicted_price=round(prediction, 2))

# --- User Management Endpoints ---
@app.put("/users/update-role", response_model=schemas.User, tags=["Users"])
def update_user_role(update_data: schemas.UserRoleUpdate, db: Session = Depends(get_db)):
    admin_user = db.query(database.User).filter(database.User.username == update_data.admin_username).first()
    if not admin_user or not security.verify_password(update_data.admin_password, admin_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    if admin_user.role != "Human Resources Head":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Human Resources Head privileges required.")

    target_user = db.query(database.User).filter(database.User.id == update_data.target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail=f"Target user with ID {update_data.target_user_id} not found.")
    
    target_user.role = update_data.new_role.value
    db.commit()
    db.refresh(target_user)
    return target_user

# --- Customer Endpoints ---
@app.post("/customers/", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED, tags=["Customers"])
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = database.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers/", response_model=List[schemas.Customer], tags=["Customers"])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(database.Customer).offset(skip).limit(limit).all()
    return customers

@app.get("/customers/{customer_id}", response_model=schemas.Customer, tags=["Customers"])
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(database.Customer).filter(database.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.put("/customers/{customer_id}", response_model=schemas.Customer, tags=["Customers"])
def update_customer(customer_id: int, update_data: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(database.Customer).filter(database.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    update_data_dict = update_data.dict(exclude_unset=True)
    for key, value in update_data_dict.items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer


# @app.post("/quotations/", response_model=schemas.Quotation, status_code=status.HTTP_201_CREATED, tags=["Quotations"])
# def create_quotation(quotation: schemas.QuotationCreate, db: Session = Depends(get_db)):
#     db_customer = db.query(database.Customer).filter(database.Customer.id == quotation.customer_id).first()
#     if not db_customer:
#         raise HTTPException(status_code=404, detail=f"Customer with ID {quotation.customer_id} not found.")
#     total_price = 0
#     quotation_items = []
#     for item_data in quotation.items:
#         db_product = db.query(database.Product).filter(database.Product.id == item_data.product_id).first()
#         if not db_product:
#             raise HTTPException(status_code=404, detail=f"Product with ID {item_data.product_id} not found.")
#         item_price = (db_product.base_price * item_data.width * item_data.height) * item_data.quantity
#         total_price += item_price
#         quotation_items.append(database.QuotationItem(
#             product_id=item_data.product_id,
#             width=item_data.width,
#             height=item_data.height,
#             quantity=item_data.quantity,
#             price=item_price
#         ))
#     db_quotation = database.Quotation(
#         customer_id=quotation.customer_id,
#         user_id=quotation.user_id,
#         total_price=total_price,
#         status='Draft',
#         items=quotation_items
#     )
#     db.add(db_quotation)
#     db.commit()
#     db.refresh(db_quotation)
#     return db_quotation

 # --- Quotation Endpoints ---
@app.get("/customers/{customer_id}/quotations/", response_model=List[schemas.Quotation], tags=["Quotations"])
def read_customer_quotations(customer_id: int, db: Session = Depends(get_db)):
    quotations = db.query(database.Quotation).filter(database.Quotation.customer_id == customer_id).all()
    return quotations


