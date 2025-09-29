"""
Main FastAPI application file.
Defines all API endpoints for the ERP/CRM system.
"""
import os
import joblib
import pandas as pd
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

# Local imports
from . import database, schemas, security

# --- App and Model State Setup ---
app = FastAPI(
    title="Reliant Windows ERP/CRM API",
    description="API for managing customers, products, and quotations.",
    version="0.1.0"
)

app.state.ml_model = None
app.state.ml_feature_cols = None

# --- FastAPI Startup Event ---
@app.on_event("startup")
async def startup_event():
    """
    This function runs once when the application starts.
    It's the robust way to load the AI model.
    """
    model_path = "app/ml_model.joblib"
    if os.path.exists(model_path):
        try:
            loaded_model, loaded_cols = joblib.load(model_path)
            
            if not hasattr(loaded_model, 'predict'):
                raise TypeError("Loaded object is not a valid model with a 'predict' method.")

            app.state.ml_model = loaded_model
            app.state.ml_feature_cols = loaded_cols
            print("INFO:     AI model loaded successfully into app state.")
        except Exception as e:
            print(f"ERROR:    Could not load AI model: {e}")
            app.state.ml_model = None
            app.state.ml_feature_cols = None
    else:
        print("WARNING:  AI model file not found at startup. Please train the model.")
        print("          Run: docker-compose exec backend python train_model.py")


# --- Database Dependency ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- User Management Endpoints ---
# --- NEW: Endpoint to get all users ---
@app.get("/users/", response_model=List[schemas.User], tags=["Users"])
def read_users(admin_username: str, admin_password: str, db: Session = Depends(get_db)):
    """
    Retrieve a list of all users. Requires admin credentials.
    """
    # Authenticate and authorize the admin user
    admin_user = db.query(database.User).filter(database.User.username == admin_username).first()
    if not admin_user or not security.verify_password(admin_password, admin_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid administrator credentials",
        )
    if admin_user.role != "Human Resources Head":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to view user list.",
        )
    
    # If authorized, return all users
    users = db.query(database.User).all()
    return users

@app.put("/users/update-role", response_model=schemas.User, tags=["Users"])
def update_user_role(update_data: schemas.UserRoleUpdate, db: Session = Depends(get_db)):
    admin_user = db.query(database.User).filter(database.User.username == update_data.admin_username).first()
    if not admin_user or not security.verify_password(update_data.admin_password, admin_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if admin_user.role != "Human Resources Head":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Human Resources Head privileges required to change user roles.",
        )

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

@app.put("/customers/{customer_id}", response_model=schemas.Customer, tags=["Customers"])
def update_customer(customer_id: int, customer_update: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(database.Customer).filter(database.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    update_data = customer_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
        
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

@app.get("/customers/{customer_id}/quotations/", response_model=List[schemas.Quotation], tags=["Quotations"])
def read_customer_quotations(customer_id: int, db: Session = Depends(get_db)):
    quotations = db.query(database.Quotation).filter(database.Quotation.customer_id == customer_id).all()
    return quotations

# --- AI Prediction Endpoint ---
@app.post("/predict_quote", response_model=schemas.QuotePredictionResponse, tags=["AI Features"])
def predict_quote(request: Request, data: schemas.QuotePredictionRequest):
    model = request.app.state.ml_model
    feature_cols = request.app.state.ml_feature_cols

    if model is None or feature_cols is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI model is not available. Please train the model first."
        )

    try:
        input_df = pd.DataFrame([data.dict()])
        input_encoded = pd.get_dummies(input_df)
        input_aligned = input_encoded.reindex(columns=list(feature_cols), fill_value=0)
        
        prediction = model.predict(input_aligned)[0]
        
        return {"predicted_price": round(prediction, 2)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")
