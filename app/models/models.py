from sqlalchemy import (
    Boolean, Column, Integer, String, Numeric,
    ForeignKey, DateTime, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base

association_table_owner_studio = Table(
    "owner_studio",
    Base.metadata,
    Column("studio_id", ForeignKey("studio.id")),
    Column("person_id", ForeignKey("person.id")),
)

association_table_service_provider_studio = Table(
   "service_provider_studio",
    Base.metadata,
    Column("studio_id", ForeignKey("studio.id")),
    Column("service_provider_id", ForeignKey("service_provider.id")),
    Column("comission", Numeric(), nullable=False)
)

class Person(Base):
    __tablename__ = "person"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    display_name = Column(String(36), unique=False, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(16), nullable=True)

    sell = relationship("Sell", uselist=False, back_populates="client", cascade="all, delete")
    studio_owner = relationship("Studio", secondary=association_table_owner_studio, back_populates="person_owner")
    service_provider = relationship("ServiceProvider", uselist=False, back_populates="person", cascade="all, delete")

class ServiceProvider(Base):
    __tablename__ = "service_provider"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, unique=True, nullable=False)
    person_id = Column(UUID, ForeignKey("person.id"), nullable=False, unique=True)

    sell = relationship("Sell", uselist=False, back_populates="service_provider")
    studios = relationship("Studio", secondary=association_table_service_provider_studio, back_populates="service_providers")
    person = relationship("Person", back_populates="service_provider")

class Studio(Base):
    __tablename__ = "studio"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    studio_name = Column(String(36), unique=True, nullable=False)
    country = Column(String(3), nullable=True)
    state = Column(String(2), nullable=True)
    city = Column(String(32), nullable=True)
    district = Column(String(100), nullable=True)
    address = Column(String(100), nullable=True)
    number = Column(Integer(), nullable=True)
    zip_code = Column(Integer(), nullable=True)
    complement = Column(String(15), nullable=True)
    email_studio = Column(String(50), nullable=True)
    description = Column(String(255), nullable=True)

    sell = relationship("Sell")
    service_providers = relationship("ServiceProvider", secondary=association_table_service_provider_studio, back_populates="studios")
    person_owner = relationship("Person", secondary=association_table_owner_studio, back_populates="studio_owner")

class Sell(Base):
    __tablename__ = "sell"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    studio_id = Column(UUID, ForeignKey("studio.id"), nullable=True, unique=False)
    client_id = Column(UUID, ForeignKey("person.id"), nullable=False, unique=False)
    service_provider_id = Column(String(36), ForeignKey("service_provider.id"), nullable=False, unique=False)

    price = Column(Numeric(asdecimal=True), nullable=False)
    start_time = Column(DateTime(), nullable=False)
    actual_session = Column(Integer(), nullable=True)
    scheduled_time = Column(DateTime(), nullable=True)
    description = Column(String(255), nullable=True)
    finished = Column(Boolean(), nullable=True)

    client = relationship("Person", back_populates="sell")
    service_provider = relationship("ServiceProvider", back_populates="sell")