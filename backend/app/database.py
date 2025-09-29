"""
Database connection, session management, and ORM models.
"""
import enum
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

# This enum is no longer needed for the ORM but is kept for clarity.
# The validation now happens at the application/schema level.
class UserRole(enum.Enum):
    Manager = "Manager"
    Regional_Manager = "Regional Manager"
    Sales = "Sales"
    Construction_Worker = "Construction Worker"
    Human_Resources_Head = "Human Resources Head"
    Human_Resources_Associate = "Human Resources Associate"

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # --- THIS IS THE FINAL, SIMPLIFIED FIX ---
    # Treat the role as a simple String. This avoids all Enum mapping errors.
    role = Column(String, nullable=False)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone_number = Column(String(20))
    address = Column(Text)
    quotations = relationship("Quotation", back_populates="customer")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    product_type = Column(String, nullable=False)
    material = Column(String, nullable=False)
    base_price = Column(Float, nullable=False)

class Quotation(Base):
    __tablename__ = "quotations"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=True)
    status = Column(String(20), default="Draft", nullable=False)
    customer = relationship("Customer", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation", cascade="all, delete-orphan")

class QuotationItem(Base):
    __tablename__ = "quotation_items"
    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, nullable=False)
    quotation = relationship("Quotation", back_populates="items")

