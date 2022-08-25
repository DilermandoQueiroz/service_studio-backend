from sqlalchemy import (
    Boolean, Column, Integer, String, Numeric,
    ForeignKey, DateTime, Table, Date
)
from sqlalchemy.orm import relationship

from database import Base


association_table_service_provider_studio = Table(
    "service_provider_studio",
    Base.metadata,
    Column("studio_id", Integer(), ForeignKey("studio.id"), unique=True),
    Column("service_provider_id", Integer(), ForeignKey("service_provider.id"), unique=True),
    Column("comission", Numeric(), nullable=False),
)

association_table_service_style = Table(
    "service_style_provider",
    Base.metadata,
    Column("service_provider_id", Integer(), ForeignKey("service_provider.id"), unique=True),
    Column("service_style_id", Integer(), ForeignKey("service_style.id"), unique=True)
)

class Studio(Base):
    __tablename__ = "studio"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    name = Column(String(36), unique=True, nullable=False)
    display_name = Column(String(32), nullable=False)
    country = Column(String(3), nullable=True)
    state = Column(String(2), nullable=True)
    city = Column(String(32), nullable=True)
    district = Column(String(100), nullable=True)
    address = Column(String(100), nullable=True)
    number = Column(Integer(), nullable=True)
    zip_code = Column(String(10), nullable=True)
    complement = Column(String(15), nullable=True)
    email = Column(String(50), nullable=True)
    phone_number = Column(String(20), nullable=True)
    description = Column(String(255), nullable=True)
    email_owner = Column(String(50), unique=True, nullable=False)

    sell = relationship("Sell", back_populates="studio", uselist=False)
    service_providers = relationship("ServiceProvider", secondary=association_table_service_provider_studio, back_populates="studios")

class ServiceProvider(Base):
    __tablename__ = "service_provider"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    name = Column(String(36), unique=True, nullable=False)
    display_name = Column(String(32), nullable=False)
    birth_date = Column(Date(), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    description = Column(String(255), nullable=True)
    studios = relationship("Studio", secondary=association_table_service_provider_studio, back_populates="service_providers")
    sell = relationship("Sell", back_populates="service_provider", uselist=False)


class Client(Base):
    __tablename__ = "client"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    name = Column(String(36), unique=True, nullable=False)
    display_name = Column(String(32), nullable=False)
    birth_date = Column(Date(), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    country = Column(String(3), nullable=True)
    state = Column(String(2), nullable=True)
    city = Column(String(32), nullable=True)
    district = Column(String(100), nullable=True)
    address = Column(String(100), nullable=True)
    number = Column(Integer(), nullable=True)
    zip_code = Column(String(10), nullable=True)
    complement = Column(String(15), nullable=True)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    sell = relationship("Sell", back_populates="client", uselist=False)


class Sell(Base):
    __tablename__ = "sell"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    """
    ForeignKey Start
    """
    studio_name = Column(String(36), ForeignKey("studio.name"), nullable=True, unique=False)
    client_name = Column(String(36), ForeignKey("client.name"), nullable=False, unique=False)
    service_provider_name = Column(String(36), ForeignKey("service_provider.name"), unique=False)
    service_style_name = Column(String(32), ForeignKey("service_style.name"), unique=False)
    tender_id = Column(Integer(), ForeignKey("service_tender.id"), nullable=True)
    """
    ForeignKey finish
    """
    price = Column(Numeric(asdecimal=True), nullable=False)
    studio_rate = Column(Integer(), nullable=True)
    client_rate = Column(Integer(), nullable=False)
    service_provider_rate = Column(Integer(), nullable=False)
    client_suggestion_desc = Column(String(140), nullable=True)
    client_satisfied = Column(Boolean(), nullable=False)
    number_of_sessions = Column(Integer(), nullable=True)
    client_contract_confirmed = Column(Boolean(), nullable=False)
    service_provider_contract_confirmed = Column(Boolean(), nullable=False)
    start_time = Column(DateTime(), nullable=False)
    last_update = Column(DateTime(), nullable=False)
    finish_time = Column(DateTime(), nullable=False)
    """
    Relationship start
    """
    studio = relationship("Studio", back_populates="sell")
    service_provider = relationship("ServiceProvider", back_populates="sell")
    client = relationship("Client", back_populates="sell")
    service_style = relationship("ServiceStyle", back_populates="sell")
    tender = relationship("ServiceTender", back_populates="sell")


class ServiceStyle(Base):
    __tablename__ = "service_style"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    name = Column(String(36), unique=True, nullable=False)
    display_name = Column(String(32), nullable=False)
    type = Column(String(32), nullable=False)
    sell = relationship("Sell", back_populates="service_style", uselist=False)

class ServiceTender(Base):
    __tablename__ = "service_tender"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    signal = Column(Numeric(asdecimal=True), nullable=True)
    body_local = Column(String(15), nullable=True)
    price = Column(Numeric(asdecimal=True), nullable=True)
    photo = Column(String(8000), nullable=True)
    sell = relationship("Sell", back_populates="tender", uselist=False)
