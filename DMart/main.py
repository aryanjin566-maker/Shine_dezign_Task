from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import DECIMAL

# ---------- DATABASE ----------
DATABASE_URL = "mysql+pymysql://root:1234@localhost/DMart"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ---------- APP ----------
app = FastAPI()

# ---------- MODEL ----------
class Employee(Base):
    __tablename__ = "employee"

    emp_id = Column(Integer, primary_key=True)
    emp_name = Column(String(50), nullable=False)
    role_id = Column(Integer, nullable=False)
    password_hash = Column(String(255), nullable=False)

    emp_contact = Column(String(15))
    emp_address = Column(Text)
    emp_image = Column(String(150))

Base.metadata.create_all(engine)
class EmployeeUpdate(BaseModel):
    name: str
    role_id: int
class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(50), nullable=False)
    product_price = Column(DECIMAL(10,2), nullable=False)
    category_id = Column(Integer, nullable=False)
    created_by = Column(Integer, nullable=False)
class ProductCreate(BaseModel):
    name: str
    price: float
    category_id: int
    created_by: int

class ProductUpdate(BaseModel):
    name: str
    price: float
    category_id: int
# ---------- DB ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- SCHEMAS ----------
class Register(BaseModel):
    name: str
    role_id: int
    password: str

class Login(BaseModel):
    emp_id: int
    password: str

# ---------- APIs ----------
@app.post("/register")
def register(data: Register, db=Depends(get_db)):
    emp = Employee(
        emp_name=data.name,
        role_id=data.role_id,
        password_hash=data.password   # plain text (learning only)
    )
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return {"message": "Registered", "emp_id": emp.emp_id}

@app.post("/login")
def login(data: Login, db=Depends(get_db)):
    emp = db.query(Employee).filter(Employee.emp_id == data.emp_id).first()
    if not emp or emp.password_hash != data.password:
        raise HTTPException(401, "Invalid credentials")
    return {"message": "Login successful", "role_id": emp.role_id}

@app.get("/employees")
def employees(db=Depends(get_db)):
    return db.query(Employee).all()

@app.post("/product")
def add_product(data: ProductCreate, db=Depends(get_db)):
    product = Product(
        product_name=data.name,
        product_price=data.price,
        category_id=data.category_id,
        created_by=data.created_by
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"message": "Product added", "product_id": product.product_id}

@app.get("/products")
def get_products(db=Depends(get_db)):
    return db.query(Product).all()

@app.put("/product/{product_id}")
def update_product(product_id: int, data: ProductUpdate, db=Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    product.product_name = data.name
    product.product_price = data.price
    product.category_id = data.category_id

    db.commit()
    return {"message": "Product updated"}

@app.delete("/product/{product_id}")
def delete_product(product_id: int, db=Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}

@app.put("/employee/{emp_id}")
def update_employee(emp_id: int, data: EmployeeUpdate, db=Depends(get_db)):
    emp = db.query(Employee).filter(Employee.emp_id == emp_id).first()

    if not emp:
        raise HTTPException(404, "Employee not found")

    emp.emp_name = data.name
    emp.role_id = data.role_id
    db.commit()

    return {"message": "Employee updated successfully"}

@app.delete("/employee/{emp_id}")
def delete_employee(emp_id: int, db=Depends(get_db)):
    emp = db.query(Employee).filter(Employee.emp_id == emp_id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()
    return {"message": "Employee deleted successfully"}