import json
from datetime import date, datetime
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from datetime import date


class Customers(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    vat_id: int = Field(unique=True)

    offers: list["Offers"] = Relationship(back_populates="customers")
    products: list["Products"] = Relationship(back_populates="customers")


class Products(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float

    customers: list["Customers"] = Relationship(back_populates="products")
    offers: list["Offers"] = Relationship(back_populates="products")


class Offers(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    datum: date

    customer_id: int = Field(foreign_key="customers.id")
    products: list["Products"] = Relationship(back_populates="offers")

    customer: Customers = Relationship(back_populates="offers")


engine = create_engine("sqlite:///refactured.db")
SQLModel.metadata.create_all(engine)


