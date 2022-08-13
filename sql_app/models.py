from sqlalchemy import Boolean, Column, Integer, VARCHAR, CHAR, DECIMAL, DATE, TIMESTAMP, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from database import Base

class Studio(Base):
    __tablename__ = "studio"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(32), unique=True, nullable=False)
    display_name = Column(VARCHAR(32), nullable=False)
    country = Column(CHAR(3), nullable=True)
    state = Column(CHAR(2), nullable=True)
    city = Column(VARCHAR(32), nullable=True)
    district = Column(VARCHAR(100), nullable=True)
    address = Column(VARCHAR(100), nullable=True)
    number = Column(Integer, nullable=True)
    zip_code = Column(CHAR(10), nullable=True)
    complement = Column(VARCHAR(15), nullable=True)
    email = Column(VARCHAR(50), nullable=True)
    phone_number = Column(VARCHAR(20), nullable=True)
    description = Column(VARCHAR(255), nullable=True)
    email_owner = Column(VARCHAR(50), nullable=False)


class ServiceProviderStudio(Base):
    __tablename__ = "service_provider_studio"

    studio_name = Column(VARCHAR(32), PrimaryKeyConstraint("studio.name"), unique=True)
    service_provider_name = Column(VARCHAR(32), PrimaryKeyConstraint("service_provider.name"), unique=True)
    comission = Column(DECIMAL, nullable=True)


class ServiceProvider(Base):
    __tablename__ = "service_provider"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(32), unique=True, nullable=False)
    display_name = Column(VARCHAR(32), nullable=False)
    cpf = Column(CHAR(11), nullable=False, unique=True)
    email = Column(VARCHAR(50), nullable=True)
    phone_number = Column(VARCHAR(20), nullable=True)
    signal = Column(DECIMAL, nullable=True)
    deszcription = Column(VARCHAR(255), nullable=True)


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(32), unique=True, nullable=False)
    display_name = Column(VARCHAR(32), nullable=False)
    birth_date = Column(DATE, nullable=False)
    cpf = Column(CHAR(11), nullable=False, unique=True)
    country = Column(CHAR(3), nullable=True)
    state = Column(CHAR(2), nullable=True)
    city = Column(VARCHAR(32), nullable=True)
    district = Column(VARCHAR(100), nullable=True)
    address = Column(VARCHAR(100), nullable=True)
    number = Column(Integer, nullable=True)
    zip_code = Column(CHAR(10), nullable=True)
    complement = Column(VARCHAR(15), nullable=True)
    email = Column(VARCHAR(50), nullable=True)
    phone_number = Column(VARCHAR(20), nullable=True)


class Sell(Base):
    __tablename__ = "sell"

    id = Column(Integer, primary_key=True, index=True)
    service_provider = Column(VARCHAR(32), ForeignKey("service_provider.name"), unique=True)
    studio = Column(VARCHAR(32), ForeignKey("studio.name"), unique=True, nullable=True)
    client = Column(VARCHAR(32), ForeignKey("client.name"), unique=True)
    service_style = Column(VARCHAR(32), ForeignKey("service_style.name"), unique=True)
    tender = relationship("Tender", back_populates="id", nullable=True)
    price = Column(DECIMAL, nullable=False)
    studio_rate = Column(Integer, nullable=True)
    client_rate = Column(Integer, nullable=False)
    service_provider_rate = Column(Integer, nullable=False)
    client_suggestion_desc = Column(VARCHAR(140), nullable=True)
    client_satisfied = Column(Boolean, nullable=False)
    number_of_sessions = Column(Integer, nullable=True)
    client_contract_confirmed = Column(Boolean, nullable=False)
    service_provider_contract_confirmed = Column(Boolean, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    last_update = Column(TIMESTAMP, nullable=False)
    finish_time = Column(TIMESTAMP, nullable=False)


class ServiceStyle(Base):
    __tablename__ = "service_style"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(32), unique=True, nullable=False)
    display_name = Column(VARCHAR(32), nullable=False)
    type = Column(VARCHAR(32), nullable=False)


class ServiceStyleProvider(Base):
    __tablename__ = "service_style_provider"

    service_provider_name = Column(VARCHAR(32), ForeignKey("service_provider.name"), unique=True)
    service_style_id = Column(VARCHAR(32), ForeignKey("service_style.id"), unique=True)


class ServiceTender(Base):
    __tablename__ = "service_tender"

    id = Column(Integer, primary_key=True, index=True)
    signal = Column(DECIMAL, nullable=True)
    body_local = Column(VARCHAR(15), nullable=True)
    price = Column(DECIMAL, nullable=True)
    photo = Column(VARCHAR, nullable=True)
