# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    github_org = Column(String(100))
    slack_channel = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="company")
    employees = relationship("Employee", back_populates="company")
    settings = relationship("CompanySettings", back_populates="company", uselist=False)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    role = Column(String(20), default="admin")  # admin, hr, manager
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="users")

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    team = Column(String(50))
    monthly_salary = Column(Float, nullable=False)
    github_username = Column(String(50))
    slack_user_id = Column(String(50))
    is_ghost = Column(Boolean, default=False)
    status = Column(String(20), default="active")
    ghost_score = Column(Float, default=0.0)
    last_github_commit = Column(String(20))
    last_slack_activity = Column(String(20))
    recovered_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="employees")

class CompanySettings(Base):
    __tablename__ = "company_settings"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, unique=True)
    github_token_encrypted = Column(String(255))
    slack_token_encrypted = Column(String(255))
    openrouter_key_encrypted = Column(String(255))
    test_mode = Column(Boolean, default=True)
    auto_recover_enabled = Column(Boolean, default=False)
    notification_channel = Column(String(50))
    
    # Relationships
    company = relationship("Company", back_populates="settings")