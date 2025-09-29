from typing import List, Optional
from pydantic import BaseModel
from enum import Enum as PyEnum

# --- THIS IS THE UPDATED ENUM with all new roles ---
class UserRole(str, PyEnum):
    MANAGER = "Manager"
    REGIONAL_MANAGER = "Regional Manager"
    SALES = "Sales"
    CONSTRUCTION_WORKER = "Construction Worker"
    HUMAN_RESOURCES_HEAD = "Human Resources Head"
    HUMAN_RESOURCES_ASSOCIATE = "Human Resources Associate"

# --- Base Schemas ---
class CustomerBase(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class QuotationItemBase(BaseModel):
    product_id: int
    width: float
    height: float
    quantity: int = 1

# --- Schemas for Creating Records ---
class CustomerCreate(CustomerBase):
    pass

class QuotationCreate(BaseModel):
    customer_id: int
    user_id: int
    items: List[QuotationItemBase]

# --- Schemas for Reading Records (API Responses) ---
class Customer(CustomerBase):
    id: int
    class Config:
        from_attributes = True

class QuotationItem(QuotationItemBase):
    id: int
    price: float
    class Config:
        from_attributes = True

class Quotation(BaseModel):
    id: int
    customer_id: int
    user_id: int
    total_price: Optional[float] = None
    status: str
    items: List[QuotationItem] = []
    class Config:
        from_attributes = True

# --- Schemas for User Management ---
class User(BaseModel):
    id: int
    username: str
    role: UserRole
    class Config:
        from_attributes = True

class UserRoleUpdate(BaseModel):
    admin_username: str
    admin_password: str
    target_user_id: int
    new_role: UserRole

# --- Schema for Debugging ---
class UserDebug(BaseModel):
    username: str
    hashed_password: str
    class Config:
        from_attributes = True

