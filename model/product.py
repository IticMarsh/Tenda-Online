from pydantic import BaseModel

#clase producte

class Product(BaseModel):
    id:int
    name:str
    description: str
    company: str
    price: float
    units:int
    subcategory_id:int