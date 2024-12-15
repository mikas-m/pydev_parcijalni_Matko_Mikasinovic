from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from datetime import date

class CustomerProductLink(SQLModel, table=True):
    __table__name = "Customer_Product"
    customer_id: int = Field(foreign_key="customer.id", primary_key=True)
    product_id: int = Field(foreign_key="product.id", primary_key=True)

class ProductOfferLink(SQLModel, table=True):
    __table__name = "Product_Offer"
    offer_id: int = Field(foreign_key="offer.id", primary_key=True)
    product_id: int = Field(foreign_key="product.id", primary_key=True)



class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    customer_id: int = Field(default=None, foreign_key="customer.id")

    customers: list["Customer"] = Relationship(back_populates="products", link_model=CustomerProductLink)
    offers: list["Offer"] = Relationship(back_populates="products", link_model=ProductOfferLink)


class Customer(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    vat_id: str = Field(unique=True)
    
    offers: list["Offer"] = Relationship(back_populates="customers")
    products: list["Product"] = Relationship(back_populates="customers", link_model=CustomerProductLink)



class Offer(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    datum: date

    customer_id: int = Field(foreign_key="customer.id")
    products: list["Product"] = Relationship(back_populates="offers", link_model=ProductOfferLink)

    customers: Customer = Relationship(back_populates="offers")



engine = create_engine("sqlite:///refactured.db")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    customer1 = Customer(name="Tech Solutions", email="info@techsolutions.com", vat_id="01234567890")
    session.add(customer1)
    session.commit()

    products1 = Product(name="Laptop", description="15-inch display, 8GB RAM, 256GB SSD", price=800.0, customer_id=customer1.id)
    products2 = Product(name="Smartphone", description="6-inch display, 128GB storage", price=500.0, customer_id=customer1.id)

    session.add(products1)
    session.add(products2)
    session.commit()
