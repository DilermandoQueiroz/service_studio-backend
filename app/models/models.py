from sqlalchemy import (
    Boolean, Column, Integer, String, Numeric,
    ForeignKey, DateTime, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base

class StudioServiceProvider(Base):
    __tablename__ = "studio_service_provider"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    studio_id = Column(ForeignKey("studio.id"), nullable=False)
    service_provider_id = Column(ForeignKey("service_provider.id"), nullable=False)
    comission = Column(Numeric(asdecimal=True), nullable=True)
    studio_accept = Column(Boolean(), nullable=True)
    service_provider_accept = Column(Boolean(), nullable=True)


    service_provider = relationship("ServiceProvider", back_populates="work_in")
    studio = relationship("Studio", back_populates="receive_service_provider")

class OwnerStudio(Base):
    __tablename__ = "owner_studio"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    studio_id = Column(ForeignKey("studio.id"), nullable=False)
    person_id = Column(ForeignKey("person.id"), nullable=False)
    
    person = relationship("Person", back_populates="studio_owner")
    studio = relationship("Studio", back_populates="person_owner")


class Person(Base):
    __tablename__ = "person"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    display_name = Column(String(36), unique=False, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(16), nullable=True)

    sell = relationship("Sell", uselist=False, back_populates="client", cascade="all, delete")
    studio_owner = relationship("OwnerStudio", back_populates="person")
    service_provider = relationship("ServiceProvider", uselist=False, back_populates="person", cascade="all, delete")

class ServiceProvider(Base):
    __tablename__ = "service_provider"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID, ForeignKey("person.id"), nullable=False, unique=True)

    sell = relationship("Sell", uselist=False, back_populates="service_provider")
    work_in = relationship("StudioServiceProvider", back_populates="service_provider")
    person = relationship("Person", back_populates="service_provider")

class Studio(Base):
    __tablename__ = "studio"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    display_name = Column(String(36), unique=True, nullable=False)
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
    receive_service_provider = relationship("StudioServiceProvider", back_populates="studio")
    person_owner = relationship("OwnerStudio", back_populates="studio")

class Sell(Base):
    __tablename__ = "sell"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    studio_id = Column(UUID, ForeignKey("studio.id"), nullable=True, unique=False)
    client_id = Column(UUID, ForeignKey("person.id"), nullable=False, unique=False)
    service_provider_id = Column(UUID, ForeignKey("service_provider.id"), nullable=False, unique=False)

    price = Column(Numeric(asdecimal=True), nullable=False)
    start_time = Column(DateTime(), nullable=False)
    actual_session = Column(Integer(), nullable=True)
    scheduled_time = Column(DateTime(), nullable=True)
    description = Column(String(255), nullable=True)
    finished = Column(Boolean(), nullable=True)

    client = relationship("Person", back_populates="sell")
    service_provider = relationship("ServiceProvider", back_populates="sell")