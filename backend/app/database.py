import enum
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    Enum,
    DateTime, # NEW: Import DateTime
    func # NEW: Import func for server-side defaults
)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

from .config import settings

# --- Database Setup ---
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ORM Models ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # The role is stored as a simple string for maximum robustness
    role = Column(String, nullable=False)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    address = Column(String)
    quotations = relationship("Quotation", back_populates="customer")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    product_type = Column(String, nullable=False)
    material = Column(String, nullable=False)
    base_price = Column(Float, nullable=False)

class Quotation(Base):
    __tablename__ = "quotations"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float)
    status = Column(String, nullable=False, default='Draft')
    # CORRECTED: The created_at column is now defined in the ORM model
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    customer = relationship("Customer", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation", cascade="all, delete-orphan")

class QuotationItem(Base):
    __tablename__ = "quotation_items"
    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)
    
    quotation = relationship("Quotation", back_populates="items")

