from sqlalchemy import Column, Integer, Boolean, Text, Date, DateTime, ForeignKey, Numeric, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role = Column(Text, nullable=False)

    user = relationship("User", back_populates="roles")


class SellerRequest(Base):
    __tablename__ = "seller_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    full_name = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    property_title = Column(Text, nullable=False)
    property_address = Column(Text, nullable=False)
    district = Column(Text, default="CHENNAI")
    property_type = Column(Text, nullable=False)
    bedrooms = Column(Integer, default=1)
    monthly_rent = Column(Numeric, nullable=False)
    description = Column(Text, default="")
    doc_type = Column(Text, nullable=False)
    doc_url = Column(Text)
    image_urls = Column(JSON)
    declaration_accepted = Column(Boolean, default=False)
    status = Column(Text, default="PENDING", index=True)
    reason = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    property_type = Column(Text, nullable=False)
    bedrooms = Column(Integer, default=1)
    bathrooms = Column(Integer, default=1)
    monthly_rent = Column(Numeric, nullable=False)
    status = Column(Text, default="PENDING", index=True)
    is_available = Column(Boolean, default=True)
    reason = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), index=True)
    applicant_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    full_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, index=True)
    phone = Column(Text, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    marital_status = Column(Text, nullable=False)
    employment_type = Column(Text, nullable=False)
    college_name = Column(Text)
    company_name = Column(Text)
    monthly_income = Column(Numeric)
    current_address = Column(Text, nullable=False)
    move_in_date = Column(Date, nullable=False)
    lease_duration = Column(Integer, nullable=False)
    num_occupants = Column(Integer, default=1)
    gov_id_url = Column(Text)
    additional_notes = Column(Text)
    status = Column(Text, default="PENDING", index=True)
    reason = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class Lease(Base):
    __tablename__ = "leases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), index=True)
    tenant_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    monthly_rent = Column(Numeric, nullable=False)
    status = Column(Text, default="ACTIVE", index=True)
    created_at = Column(DateTime, server_default=func.now())


class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lease_id = Column(Integer, ForeignKey("leases.id", ondelete="CASCADE"), index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), index=True)
    tenant_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    priority = Column(Text, default="LOW")
    description = Column(Text, nullable=False)
    image_urls = Column(JSON)
    status = Column(Text, default="OPEN", index=True)
    comment = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    full_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, index=True)
    phone = Column(Text, nullable=False)
    purpose = Column(Text, nullable=False)
    preferred_date = Column(Date, nullable=False)
    preferred_time = Column(Text, nullable=False)
    additional_notes = Column(Text)
    status = Column(Text, default="PENDING", index=True)
    meet_url = Column(Text)
    reason = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
