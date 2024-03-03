from typing import List
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from db import productDB
from model.product import Product
from model.csv import CSVData
from schema.producte import product_schema, products_schema
from typing import Annotated


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/product/")
def read_products():

    data = productDB.consulta()

    return product_schema(data)


@app.get("/product/{product_id}")
def read_product(product_id: int):
    data = productDB.get_product_by_id(product_id)

    if not data:
        raise HTTPException(status_code=404, detail="Product not found")

    return product_schema(data)

@app.post("/product/")
def create_product(prod: Product):
    success = productDB.insert(prod)
    if success:
        return {"message": "Product added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add product to database")

@app.put("/product/{product_id}")
def update_product(product_id: int, prod: Product):
    success = productDB.update_product(product_id, prod)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully"}

@app.delete("/product/{product_id}")
def delete_product(product_id: int):
    success = productDB.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@app.get("/productAll/")
def read_products_all():
    data = productDB.get_all_products()

    return products_schema(data)

######   PART 2 IMPORTACIO CSV   #####

@app.post("/loadProducts/")
async def create_upload_file(file: UploadFile):
    productDB.load(file)
    return {"filename": file.filename, "message": "cargado con éxito"}
