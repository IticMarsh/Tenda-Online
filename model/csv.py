from pydantic import BaseModel


class CSVData(BaseModel):
    category_name: str
    subcategory_name: str
    product_name: str
    product_company: str
    product_price: float
    units: int
