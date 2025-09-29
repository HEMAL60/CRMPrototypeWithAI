from typing import List, Optional
# NEW: Import the datetime type
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

# --- Enums for API validation ---
class UserRole(str, Enum):
    Manager = "Manager"
    Regional_Manager = "Regional Manager"
    Sales = "Sales"
    Construction_Worker = "Construction Worker"
    Human_Resources_Head = "Human Resources Head"
    Human_Resources_Associate = "Human Resources Associate"

class ProductType(str, Enum):
    Window = "Window"
    Door = "Door"

class Material(str, Enum):
    uPVC = "uPVC"
    Aluminium = "Aluminium"
    Timber = "Timber"


# --- Base Schemas ---
class CustomerBase(BaseModel):
    full_name: str
    email: str
    phone_number: str
    address: Optional[str] = None

# --- Schemas for Creating/Updating Data ---
class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class UserRoleUpdate(BaseModel):
    admin_username: str
    admin_password: str
    target_user_id: int
    new_role: UserRole

# --- Schemas for API Responses ---
class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True

class QuotationItem(BaseModel):
    id: int
    product_id: int
    width: float
    height: float
    quantity: int
    price: float

    class Config:
        from_attributes = True

class Quotation(BaseModel):
    id: int
    customer_id: int
    user_id: int
    total_price: Optional[float] = None
    status: str
    # CORRECTED: The created_at field is now included in the API response model.
    created_at: datetime
    items: List[QuotationItem] = []

    class Config:
        from_attributes = True

# --- Schemas for AI Features ---
class QuotePredictionRequest(BaseModel):
    width: float
    height: float
    quantity: int
    product_type: ProductType
    material: Material

class QuotePredictionResponse(BaseModel):
    predicted_price: float

# --- Schemas for Debugging ---
class UserDebug(User):
    hashed_password: str

    

