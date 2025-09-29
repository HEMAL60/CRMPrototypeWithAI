"""
Pydantic models for API data validation.
Defines the shape of data for requests and responses.
"""
from typing import List, Optional
from pydantic import BaseModel
import enum

# --- User Role Enum ---
class UserRole(enum.Enum):
    Manager = "Manager"
    Regional_Manager = "Regional Manager"
    Sales = "Sales"
    Construction_Worker = "Construction Worker"
    Human_Resources_Head = "Human Resources Head"
    Human_Resources_Associate = "Human Resources Associate"

# --- Customer Schemas ---
class CustomerBase(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class Customer(CustomerBase):
    id: int
    class Config:
        from_attributes = True

# --- Quotation Schemas ---
class QuotationItemBase(BaseModel):
    product_id: int
    width: float
    height: float
    quantity: int

class QuotationItemCreate(QuotationItemBase):
    pass

class QuotationItem(QuotationItemBase):
    id: int
    price: float
    class Config:
        from_attributes = True

class QuotationBase(BaseModel):
    customer_id: int
    user_id: int

class QuotationCreate(QuotationBase):
    items: List[QuotationItemCreate]

class Quotation(QuotationBase):
    id: int
    total_price: Optional[float] = None
    status: str
    items: List[QuotationItem] = []
    class Config:
        from_attributes = True

# --- User Schemas ---
class UserRoleUpdate(BaseModel):
    admin_username: str
    admin_password: str
    target_user_id: int
    new_role: UserRole

class User(BaseModel):
    id: int
    username: str
    role: UserRole
    class Config:
        from_attributes = True

# --- Debugging Schema ---
class UserDebug(User):
    hashed_password: str

# --- AI Feature Schemas ---
# Enums to ensure the input for prediction matches the training data categories.
# These must match the values in the `products` table.
class ProductType(str, enum.Enum):
    Window = "Window"
    Door = "Door"

class Material(str, enum.Enum):
    uPVC = "uPVC"
    Aluminium = "Aluminium"
    Timber = "Timber"

class QuotePredictionRequest(BaseModel):
    width: float
    height: float
    quantity: int
    product_type: ProductType
    material: Material

class QuotePredictionResponse(BaseModel):
    predicted_price: float

